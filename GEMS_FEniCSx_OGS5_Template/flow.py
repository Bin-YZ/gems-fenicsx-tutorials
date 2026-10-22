"""Steady saturated groundwater flow (OGS5 GROUNDWATER_FLOW), CG1.

    -div(K grad h) = sources,      q = -K grad h

    K        element hydraulic conductivity, m/s (set K_cell before each solve)
    h        hydraulic head, m
    sources  nodal volume sources, m3/s per node, OGS node order (point sources,
             and the GEMS excess-water source term added by reactive_transport.run)

Interface:
    flow.K_cell, flow.fixed_values, flow.sources, flow.extra (sparse, OGS node order, e.g. fracture)
    flow.solve(extra_sources=None) -> head in OGS node order
    flow.q                          UFL Darcy flux for transport.Transport(q=flow.q)
    flow.head_function              the CG1 Function behind q
"""
import numpy as np
import scipy.sparse.linalg as spla
import ufl
from dolfinx import fem


class Darcy:
    def __init__(self, mesh, fixed_nodes, quadrature_degree=None):
        self.mesh = mesh
        self.fixed = mesh.node2dof[np.asarray(fixed_nodes, int)]
        self.free = np.setdiff1d(np.arange(mesh.n_nodes), self.fixed)
        self.K_cell = np.ones(mesh.n_cells)
        self.fixed_values = np.zeros(len(self.fixed))
        self.sources = np.zeros(mesh.n_nodes)
        self.extra = None
        self._K = mesh.cell_function()
        self.head_function = fem.Function(mesh.V)
        u, v = ufl.TrialFunction(mesh.V), ufl.TestFunction(mesh.V)
        dx = ufl.dx(domain=mesh.domain) if quadrature_degree is None else \
            ufl.Measure('dx', domain=mesh.domain, metadata={'quadrature_degree': quadrature_degree})
        self._form = fem.form(self._K * ufl.inner(ufl.grad(u), ufl.grad(v)) * dx)
        self.q = -self._K * ufl.grad(self.head_function)
        self.head = np.zeros(mesh.n_nodes)

    def solve(self, extra_sources=None):
        m = self.mesh
        m.set_cells(self._K, self.K_cell)
        A = fem.assemble_matrix(self._form).to_scipy().tocsr()
        if self.extra is not None:
            A = A + self.extra.tocsr()[m.dof2node][:, m.dof2node]
        rhs = np.asarray(self.sources, float).copy()
        if extra_sources is not None:
            rhs = rhs + extra_sources
        rhs = rhs[m.dof2node]
        h = np.zeros(m.n_nodes)
        h[self.fixed] = self.fixed_values
        h[self.free] = spla.spsolve(A[self.free][:, self.free].tocsc(), rhs[self.free] - A[self.free][:, self.fixed] @ h[self.fixed])
        self.head_function.x.array[:] = h
        self.head = h[m.node2dof]
        return self.head
