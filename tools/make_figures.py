"""Figures for the concept pages (computed with the template where possible) -> figures/*.png"""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import ufl

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK / 'GEMS_FEniCSx_OGS5_Template'
sys.path.insert(0, str(ROOT))
from ogs_io import read_msh, read_constant_blocks, read_restart, read_primary_values
from fe_mesh import OGSMesh
from transport import Transport
from gems_ogs import OGSGEMS, Kinetic
from ogs_models import harmonic_mean
from reactive_transport import run

OUT = BOOK / 'figures'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size': 9, 'axes.grid': True, 'grid.alpha': 0.3})
which = sys.argv[1:] or ['snia', 'bvector', 'kinetics', 'fct', 'water']


def box(ax, xy, w, h, text, color):
    ax.add_patch(FancyBboxPatch(xy, w, h, boxstyle='round,pad=0.02,rounding_size=0.04', fc=color, ec='0.3', lw=1))
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha='center', va='center', fontsize=9)


def arrow(ax, a, b, text='', rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=12, lw=1.2, color='0.25',
                                 connectionstyle=f'arc3,rad={rad}'))
    if text:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.05, text, ha='center', fontsize=8, color='0.25')


# ------------------------------------------------------------------ 1. SNIA loop
if 'snia' in which:
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.set_xlim(0, 9); ax.set_ylim(0, 3.2); ax.axis('off')
    box(ax, (0.1, 1.6), 1.6, 1.0, 'prepare\nφ → K, D_e,\nboundary values', '#eef3fb')
    box(ax, (2.0, 1.6), 1.6, 1.0, 'flow\n−∇·(K∇h) = Q\n(optional)', '#e8f4ea')
    box(ax, (3.9, 1.6), 1.6, 1.0, 'transport\nφ∂c/∂t + q·∇c\n− ∇·(D∇c) = 0', '#e8f4ea')
    box(ax, (5.8, 1.6), 1.6, 1.0, 'chemistry\nGEMS at every\nnode', '#fdf0e6')
    box(ax, (7.6, 1.6), 1.3, 1.0, 'record /\nnext step', '#f2f2f2')
    for a, b in [((1.7, 2.1), (2.0, 2.1)), ((3.6, 2.1), (3.9, 2.1)), ((5.5, 2.1), (5.8, 2.1)), ((7.4, 2.1), (7.6, 2.1))]:
        arrow(ax, a, b)
    arrow(ax, (6.4, 1.58), (2.8, 1.58), '', rad=-0.3)
    arrow(ax, (6.8, 1.58), (0.9, 1.58), '', rad=-0.3)
    ax.text(4.6, 1.12, 'excess GEMS water → flow source (next step)', fontsize=8, color='0.25', ha='center')
    ax.text(3.9, 0.42, 'new porosity → φ, K, D_e of the next step', fontsize=8, color='0.25', ha='center')
    ax.text(4.5, 3.05, 'one time step Δt (sequential non-iterative approach, SNIA)', ha='center', fontsize=10, weight='bold')
    fig.savefig(OUT / 'snia.png', dpi=160, bbox_inches='tight')
    plt.close(fig)

# ------------------------------------------------------------------ 2. b vector of a cement node (ConcreteCrack, concrete)
if 'bvector' in which:
    case = ROOT / 'cases' / '5_concretecrack'
    chem = OGSGEMS(case / 'gems' / 'cement_bc-dat.lst', 1)
    comps = [f'{i + 1}-{e}' for i, e in enumerate(chem.elements)]
    b = np.zeros(chem.nIC)
    for pcs, var, geo, val in read_constant_blocks(case / 'ogs_input' / 'decal.ic', '#INITIAL_CONDITION'):
        if var in comps and geo == 'DOMAIN':
            b[comps.index(var)] = val
    chem.init_from_bulk(b[None, :], normalize=True, lower=np.zeros(chem.nDC), upper=np.full(chem.nDC, 1e10))
    fluid = chem.c[0] * chem.Vf[0]
    fluid[chem.iH] += 2 * chem.water[0]
    fluid[chem.iO] += chem.water[0]
    keep = [k for k, e in enumerate(chem.elements) if e not in ('Zz',)]
    fig, ax = plt.subplots(figsize=(8, 3.2))
    xx = np.arange(len(keep))
    ax.bar(xx - 0.2, np.maximum(chem.b_fix[0, keep], 1e-12), 0.4, label='b_fix: solids (stay at the node)', color='0.55')
    ax.bar(xx + 0.2, np.maximum(fluid[keep], 1e-12), 0.4, label='pore water: solutes + solvent (transported)', color='C0')
    ax.set_yscale('log'); ax.set_ylim(1e-6, 1e5)
    ax.set_xticks(xx); ax.set_xticklabels([chem.elements[k] for k in keep])
    ax.set_ylabel('mol per m³ of concrete')
    ax.set_title(f'Element amounts of one concrete node after GEMS (porosity {chem.phi[0]:.3f}, pH {chem.pH[0]:.2f})')
    ax.legend(fontsize=8)
    fig.savefig(OUT / 'bvector.png', dpi=160, bbox_inches='tight')
    plt.close(fig)

# ------------------------------------------------------------------ 3. kinetic window (HAYEKIT, one node)
if 'kinetics' in which:
    case = ROOT / 'cases' / '2_hayekit'
    OGS = case / 'ogs_input'
    points, cells, _, _ = read_msh(OGS / 'ab1d.msh')
    mesh = OGSMesh(points[:, :1], cells['line'], 'interval')
    x = mesh.points[:, 0]
    left, right = int(np.argmin(x)), int(np.argmax(x))
    comps = ['1-Ael', '2-Bel', '3-H', '4-Inrt', '5-O', '6-Zz']
    curves = []
    for blk in (OGS / 'ab1d.rfd').read_text().split('#CURVES')[1:]:
        rows = [l.split()[:2] for l in blk.split('\n') if l.strip() and l.split()[0][0].isdigit()]
        curves.append(np.array(rows, float))
    bc = {'POINT0': np.zeros(6), 'POINT1': np.zeros(6)}
    for pcs, var, geo, val in read_constant_blocks(OGS / 'ab1d.bc', '#BOUNDARY_CONDITION'):
        if var in comps:
            bc[geo][comps.index(var)] = val
    chem = OGSGEMS(case / 'gems' / 'TestSolub-dat.lst', mesh.n_nodes, hydrology='hayekit', min_porosity=1e-15,
                   kinetics=[Kinetic('AB(s)', logk=(-7.69897,), area_model=4, area=1.0e4)], boundary_nodes=[left, right])
    chem.init_from_restart(read_restart(OGS / 'ab1d', mesh.n_nodes, chem.nIC, chem.nDC),
                           read_primary_values(OGS / 'ab1d', 'MASS_TRANSPORT', comps),
                           nodes=np.flatnonzero(~chem.boundary), update_porosity=True)
    tr = Transport(mesh, fixed_nodes=[left, right])
    node = int(np.argmin(np.abs(x - 0.0003)))
    j = chem.species.index('AB(s)')
    hist = []
    orig = chem.calc_limits

    def calc_limits(i, dt):                     # record the window that GEMS is given at this node
        orig(i, dt)
        if i == node:
            hist.append([chem.dll[i, j], chem.dul[i, j]])
    chem.calc_limits = calc_limits
    amounts = [chem.x[node, j]]

    def prepare(step, t, dt):
        tr.phi_cell = chem.phi[mesh.cells].mean(1)
        tr.De_cell = harmonic_mean(1e-10 * chem.phi, mesh.cells)
        v = np.vstack([bc['POINT0'], bc['POINT1']])
        v[0, :2] = [np.interp(t, *curves[0].T), np.interp(t, *curves[1].T)]
        v[1, :2] = [np.interp(t, *curves[2].T), np.interp(t, *curves[3].T)]
        tr.fixed_values = v

    run(chem, tr, [100.0] * 30, prepare=prepare, record=lambda s, t, dt: amounts.append(chem.x[node, j]), print_every=0)
    hist = np.array(hist)
    t = np.arange(len(amounts)) * 100.0
    fig, ax = plt.subplots(figsize=(7, 3.2))
    for k in range(len(hist)):
        ax.fill_between([t[k], t[k + 1]], hist[k, 0], hist[k, 1], color='C1', alpha=0.25, lw=0,
                        label='allowed window [dll, dul] given to GEMS' if k == 0 else None)
    ax.step(t, amounts, where='post', color='C0', label='AB(s) amount after GEMS')
    ax.set_xlabel('time [s]'); ax.set_ylabel('AB(s) [mol per m³]')
    ax.set_title(f'Kinetic limits at x = {x[node] * 1e3:.2f} mm (HAYEKIT, Δt = 100 s)')
    ax.legend(fontsize=8)
    fig.savefig(OUT / 'kinetics_window.png', dpi=160, bbox_inches='tight')
    plt.close(fig)

# ------------------------------------------------------------------ 4. FCT on a 1D pulse
if 'fct' in which:
    n = 200
    pts = np.linspace(0, 1, n + 1)[:, None]
    cells = np.column_stack([np.arange(n), np.arange(1, n + 1)])
    mesh = OGSMesh(pts, cells, 'interval')
    xx = mesh.points[:, 0]
    c0 = ((xx > 0.1) & (xx < 0.25)).astype(float)[:, None]
    q, dt, steps = 1.0, 0.0005, 800
    res = {}
    for label, fct in [('Galerkin (no FCT)', False), ('FEM-FCT', True)]:
        tr = Transport(mesh, fixed_nodes=[0], q=ufl.as_vector([q]), fct=fct, fct_ogs_sign=False)
        tr.phi_cell, tr.De_cell, tr.fixed_values = np.ones(n), np.full(n, 1e-6), 0.0
        c = c0.copy()
        for _ in range(steps):
            c = tr.step(c, dt)
        res[label] = c[:, 0]
    o = np.argsort(xx)
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(xx[o], (((xx > 0.1 + q * dt * steps) & (xx < 0.25 + q * dt * steps)).astype(float))[o], 'k-', lw=3, alpha=0.2, label='exact (pure advection)')
    ax.plot(xx[o], res['Galerkin (no FCT)'][o], 'C3', label='Galerkin: spurious wiggles')
    ax.plot(xx[o], res['FEM-FCT'][o], 'C0', label='FEM-FCT: bounded')
    ax.axhline(0, color='0.5', lw=0.6)
    ax.set_xlabel('x'); ax.set_ylabel('c'); ax.set_title(f'A square pulse after {steps} steps (cell Péclet ≈ {q / n / 2e-6:.0f}, Courant 0.1)')
    ax.legend(fontsize=8)
    fig.savefig(OUT / 'fct.png', dpi=160, bbox_inches='tight')
    plt.close(fig)

# ------------------------------------------------------------------ 5. excess water of comedy2d after the restart run
if 'water' in which:
    import matplotlib.tri as mtri
    case = ROOT / 'cases' / '4_comedy2d'
    points, cells, mats, _ = read_msh(case / 'ogs_input' / 'cement2d.msh')
    mesh = OGSMesh(points[:, :2], cells['quad'], 'quadrilateral')
    chem = OGSGEMS(case / 'gems' / 'I1SetUp-dat.lst', mesh.n_nodes, hydrology='full', min_porosity=1e-6,
                   kinetics=[Kinetic('Portlandite', logk=(-5.0,), area_model=3, area=1000.0),
                             Kinetic('CaOxaHyd', logk=(-5.0,), area_model=3, area=1000.0)])
    restart = read_restart(case / 'ogs_input' / 'cement2d', mesh.n_nodes, chem.nIC, chem.nDC)
    chem.init_from_restart(restart, restart['solute'], update_porosity=False, pin_kinetic=True)
    from ogs_io import read_gli, nodes_on_polyline
    _, lines = read_gli(case / 'ogs_input' / 'cement2d.gli')
    for name in ('INLET_1', 'INLET_2'):                 # Dirichlet nodes get no source in OGS
        chem.excess[nodes_on_polyline(mesh.points, lines[name][:, :2], 1e-4)] = 0.0
    p = mesh.points
    tri = mtri.Triangulation(p[:, 0] * 100, p[:, 1] * 100, np.vstack([mesh.cells[:, [0, 1, 2]], mesh.cells[:, [0, 2, 3]]]))
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    m = ax[0].tripcolor(tri, chem.phi, shading='gouraud', cmap='viridis'); fig.colorbar(m, ax=ax[0])
    ax[0].set_title('porosity φ')
    lim = np.abs(chem.excess).max()
    m = ax[1].tripcolor(tri, chem.excess, shading='gouraud', cmap='RdBu_r', vmin=-lim, vmax=lim); fig.colorbar(m, ax=ax[1])
    ax[1].set_title('excess water V_aq − φ  [m³ per m³]')
    for a in ax:
        a.set_aspect('equal'); a.set_xlabel('x [cm]'); a.set_ylabel('y [cm]'); a.grid(False)
    fig.suptitle('comedy2d after the restart GEMS run: GEMS fluid volume minus porosity, the source term of the next flow step', fontsize=9)
    fig.savefig(OUT / 'excess_water.png', dpi=160, bbox_inches='tight')
    plt.close(fig)
print('figures in', OUT)
