"""A dolfinx mesh built from OGS nodes and elements, plus the index maps between them.

All state arrays of the template (concentrations, porosity, GEMS amounts) are
kept in OGS node order and OGS element order. FEniCSx numbers its degrees of
freedom and cells differently; OGSMesh holds both maps so that transport.py and
flow.py can translate at their boundary and nothing else has to care.

    mesh = OGSMesh(points, cells, 'quadrilateral')
    mesh.domain, mesh.V (CG1), mesh.Q (DG0)
    mesh.node2dof[i]   dof of OGS node i            mesh.dof2node[d]  OGS node of dof d
    mesh.cell_of_dof0  OGS element of each DG0 dof  (write cell data:  f.x.array[:] = values[mesh.cell_of_dof0])
    mesh.cells         OGS connectivity (m, k)      mesh.node_volume  OGS GetNodeAdjacentVolume
"""
import numpy as np
import ufl
import basix.ufl
from mpi4py import MPI
from scipy.spatial import cKDTree
from dolfinx import mesh as dmesh, fem
import dolfinx.cpp.io as _cio

_TYPES = {'interval': (dmesh.CellType.interval, 2), 'triangle': (dmesh.CellType.triangle, 3),
          'quadrilateral': (dmesh.CellType.quadrilateral, 4)}


class OGSMesh:
    def __init__(self, points, cells, cell_type):
        """points: (n, d) node coordinates with d = 1 or 2 (pass the two in-plane
        columns of a 2D OGS mesh, e.g. x and z for a vertical section);
        cells: (m, k) OGS connectivity, nodes counter-clockwise; cell_type:
        'interval', 'triangle' or 'quadrilateral'."""
        if MPI.COMM_WORLD.size != 1:
            raise ValueError('Run with one MPI process.')
        self.points = np.asarray(points, float).reshape(len(points), -1)
        self.cells = np.asarray(cells, np.int64)
        self.n_nodes, self.n_cells = len(self.points), len(self.cells)
        gdim = self.points.shape[1]
        ctype, k = _TYPES[cell_type]
        perm = np.asarray(_cio.perm_vtk(ctype, k))          # OGS = VTK vertex order
        element = ufl.Mesh(basix.ufl.element('Lagrange', ctype.name, 1, shape=(gdim,)))
        try:                                                # dolfinx >= 0.10
            self.domain = dmesh.create_mesh(MPI.COMM_WORLD, self.cells[:, perm], element, self.points)
        except TypeError:                                   # dolfinx 0.8 / 0.9
            self.domain = dmesh.create_mesh(MPI.COMM_WORLD, self.cells[:, perm], self.points, element)
        self.V = fem.functionspace(self.domain, ('Lagrange', 1))
        self.Q = fem.functionspace(self.domain, ('DG', 0))
        dof_xyz = self.V.tabulate_dof_coordinates()[:, :gdim]
        dist, self.dof2node = cKDTree(self.points).query(dof_xyz)
        assert dist.max() < 1e-9 * max(1.0, np.abs(self.points).max()), 'dof and node coordinates do not match'
        self.node2dof = np.empty(self.n_nodes, int)
        self.node2dof[self.dof2node] = np.arange(self.n_nodes)
        self.cell_of_dof0 = np.asarray(self.domain.topology.original_cell_index)[
            np.argsort(np.asarray(self.Q.dofmap.list).ravel())]
        # nodal control volume as OGS GetNodeAdjacentVolume: element volume / number of element nodes
        self.cell_volume = self._cell_volumes()
        self.node_volume = np.zeros(self.n_nodes)
        np.add.at(self.node_volume, self.cells, (self.cell_volume / self.cells.shape[1])[:, None])
        self.dim = gdim

    def _cell_volumes(self):
        p = self.points[self.cells]
        if p.shape[1] == 2:                                 # interval
            return np.linalg.norm(p[:, 1] - p[:, 0], axis=1)
        x, y = p[..., 0], p[..., 1]                         # polygon area (shoelace)
        return 0.5 * np.abs((x * np.roll(y, -1, axis=1) - y * np.roll(x, -1, axis=1)).sum(1))

    def cell_function(self, values=None):
        """DG0 Function holding one value per OGS element."""
        f = fem.Function(self.Q)
        if values is not None:
            self.set_cells(f, values)
        return f

    def set_cells(self, f, values):
        f.x.array[:] = np.broadcast_to(values, (self.n_cells,))[self.cell_of_dof0]

    def nodes_where(self, condition):
        """OGS node indices where condition(points) is True, e.g. lambda p: np.isclose(p[:, 0], 0)."""
        return np.flatnonzero(condition(self.points))
