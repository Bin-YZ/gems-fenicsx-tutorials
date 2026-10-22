"""Read OGS5-GEM input, restart and output files into NumPy arrays.

Nothing here knows about FEniCSx or GEMS; every function returns plain arrays
in the node order of the OGS mesh file, which is the order used by all state
arrays of the template.

    read_msh(path)                      nodes, cells by type, material ids
    read_constant_blocks(path, key)     ($PRIMARY_VARIABLE, geometry, value) of CONSTANT blocks (.ic, .bc, .st)
    read_restart(prefix, n, nIC, nDC)   GEMS restart files written by OGS ($RELOAD)
    read_primary_values(prefix, names)  *_primary_value.asc restart files of the transport processes
    read_vtk(path)                      POINTS, POINT_DATA and CELL_DATA scalars of a legacy ASCII vtk
    nodes_on_polyline(points, vertices) nodes lying on a polyline (OGS GEO_TYPE POLYLINE)
"""
from pathlib import Path
import numpy as np


def read_msh(path):
    """Read an OGS5 ASCII mesh (#FEM_MSH with $NODES / $ELEMENTS).

    Returns
    -------
    points : (n, 3) float array, node coordinates in file order.
    cells : dict {element type: (m, k) int array}, e.g. 'line', 'tri', 'quad'.
    materials : dict {element type: (m,) int array}, the material group of each element.
    order : dict {element type: (m,) int array}, position of each element in the file (OGS element number).
    """
    lines = Path(path).read_text().split('\n')
    k = next(i for i, l in enumerate(lines) if l.strip() == '$NODES')
    n = int(lines[k + 1].split()[0])
    points = np.array([[float(v) for v in lines[k + 2 + i].split()[1:4]] for i in range(n)])
    k = next(i for i, l in enumerate(lines) if l.strip() == '$ELEMENTS')
    m = int(lines[k + 1].split()[0])
    cells, materials, order = {}, {}, {}
    for e in range(m):
        tok = lines[k + 2 + e].split()
        cells.setdefault(tok[2], []).append([int(v) for v in tok[3:]])
        materials.setdefault(tok[2], []).append(int(tok[1]))
        order.setdefault(tok[2], []).append(e)
    return (points, {t: np.array(c) for t, c in cells.items()},
            {t: np.array(v) for t, v in materials.items()}, {t: np.array(v) for t, v in order.items()})


def read_constant_blocks(path, key):
    """Blocks of an .ic / .bc / .st file that use $DIS_TYPE CONSTANT (or CONSTANT_NEUMANN).

    key is the block keyword, e.g. '#INITIAL_CONDITION' or '#BOUNDARY_CONDITION'.
    Only the text before #STOP is read, as OGS does.
    Returns a list of (process, primary variable, geometry name, value); geometry
    name is 'DOMAIN' or the name after POLYLINE / POINT / SURFACE / POLYGON.
    """
    text = Path(path).read_text(errors='replace').split('#STOP')[0]
    out = []
    for block in text.split(key)[1:]:
        tok = [t for line in block.split('\n') for t in line.split(';')[0].split()]
        if '$DIS_TYPE' not in tok:
            continue
        d = tok.index('$DIS_TYPE')
        if not tok[d + 1].startswith('CONSTANT'):
            continue
        g = tok.index('$GEO_TYPE')
        geo = 'DOMAIN' if tok[g + 1] == 'DOMAIN' else tok[g + 2]
        out.append((tok[tok.index('$PCS_TYPE') + 1], tok[tok.index('$PRIMARY_VARIABLE') + 1], geo, float(tok[d + 2])))
    return out


def read_restart(prefix, n_nodes, n_ic, n_dc, rank=None):
    """GEMS restart files written by OGS-GEM ($RELOAD 1/3), one value set per node.

    prefix is the path without the suffix, e.g. 'ogs_input/cement2d'. With rank=r
    the PETSc files '<prefix>_m_xDC_gem_<r>.asc' are read instead.

    Returns dict with
        porosity (n,), fluid_volume (n,),
        b_fix (n, nIC)      m_bIC: element amounts of all non-aqueous phases [mol per node volume]
        solute (n, nIC)     m_soluteB: concentrations, mol per m3 fluid, solvent water excluded
        xDC, dll, dul (n, nDC)  species amounts and their lower / upper limits
    """
    s = '' if rank is None else f'_{rank}'
    f = lambda name: np.loadtxt(f'{prefix}_{name}_gem{s}.asc')
    bic = f('m_bIC').reshape(n_nodes, n_ic, 2)
    xdc = f('m_xDC').reshape(n_nodes, n_dc, 3)
    return dict(porosity=f('m_porosity').ravel(), fluid_volume=f('m_fluid_volume').ravel(),
                b_fix=bic[:, :, 0].copy(), solute=bic[:, :, 1].copy(),
                xDC=xdc[:, :, 0].copy(), dll=xdc[:, :, 1].copy(), dul=xdc[:, :, 2].copy())


def read_primary_values(prefix, process, names, column=1):
    """Restart primary values '<prefix>_<process>_<name>_primary_value.asc' as an (n, len(names)) array.

    Each file has two columns (previous and current time level); column=1 is the current one.
    """
    return np.column_stack([np.loadtxt(f'{prefix}_{process}_{name}_primary_value.asc')[:, column] for name in names])


def read_vtk(path):
    """Legacy ASCII vtk written by OGS: returns dict with 'points', 'time' and
    'node__<name>' / 'cell__<name>' arrays for every SCALARS field."""
    lines = Path(path).read_text().split('\n')
    out, where, k = {}, 'node', 0
    while k < len(lines):
        tok = lines[k].split()
        if not tok:
            k += 1
            continue
        if tok[0] == 'POINTS':
            npts = int(tok[1])
            vals = np.array(' '.join(lines[k + 1:k + 1 + npts]).split(), float)
            out['points'] = vals.reshape(-1, 3)
            k += 1 + npts
            continue
        if tok[0] == 'POINT_DATA':
            where, size = 'node', int(tok[1])
        elif tok[0] == 'CELL_DATA':
            where, size = 'cell', int(tok[1])
        elif tok[0] == 'SCALARS':
            out[f'{where}__{tok[1]}'] = np.array([float(lines[k + 2 + m].split()[0]) for m in range(size)])
            k += 2 + size
            continue
        elif tok[0] == 'TIME':                # FIELD TimesAndCycles: "TIME 1 1 double" then the value
            out['time'] = float(lines[k + 1].split()[0])
        k += 1
    return out


def read_gli(path):
    """Points and polylines of an OGS .gli file.

    Returns (points, polylines): points {name or id: (3,) coordinates} (each point
    is stored under its id and, if given, its $NAME), polylines {name: (k, 3) vertices}.
    """
    text = Path(path).read_text(errors='replace')
    points, by_id = {}, {}
    block = text.split('#POINTS')[1].split('#')[0] if '#POINTS' in text else ''
    for line in block.split('\n'):
        tok = line.split()
        if len(tok) >= 4 and tok[0].lstrip('-').isdigit():
            xyz = np.array([float(v) for v in tok[1:4]])
            by_id[int(tok[0])] = xyz
            points[int(tok[0])] = xyz
            if '$NAME' in tok:
                points[tok[tok.index('$NAME') + 1]] = xyz
    polylines = {}
    for blk in text.split('#POLYLINE')[1:]:
        tok = blk.split('#')[0].split()
        name = tok[tok.index('$NAME') + 1]
        k = tok.index('$POINTS') + 1
        ids = []
        while k < len(tok) and tok[k].lstrip('-').isdigit():
            ids.append(int(tok[k])); k += 1
        polylines[name] = np.array([by_id[i] for i in ids])
    return points, polylines


def nodes_on_polyline(points, vertices, tol=1e-6):
    """Indices of the nodes within tol of a polyline given by its vertices (k, d)."""
    p = np.asarray(points)[:, :np.shape(vertices)[1]]
    hit = np.zeros(len(p), bool)
    for a, b in zip(np.asarray(vertices, float)[:-1], np.asarray(vertices, float)[1:]):
        s = np.clip(((p - a) @ (b - a)) / ((b - a) @ (b - a)), 0.0, 1.0)
        hit |= np.linalg.norm(p - (a + s[:, None] * (b - a)), axis=1) < tol
    return np.flatnonzero(hit)
