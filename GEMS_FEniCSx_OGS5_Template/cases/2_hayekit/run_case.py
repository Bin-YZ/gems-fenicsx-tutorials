"""算例 2：HAYEKIT（Hayek et al. 2011 的反应-扩散解析解，OGS5GEMDEV benchmarks/HAYEKIT）

2 mm 一维柱，两端 A、B 的浓度随时间变化，A + B -> AB(s) 动力学沉淀，孔隙率随之变化，
扩散系数 D0 * phi。参考：OGS 输出 ab1d0100.vtk（t = 10000 s）和解析解（hayekit_tables.npz）。

和模板的对应：
    初值        OGS 重启文件（ab1d_m_*_gem.asc + *_primary_value.asc） -> init_from_restart
    输运        Transport，无对流，两端 Dirichlet（rfd 曲线），单元 De = 节点 D0*phi 的调和平均
    化学        OGSGEMS(hydrology='hayekit')，Kinetic('AB(s)', 表面积模型 4)

用法：python run_case.py [dt ...]      默认 100 10 1（100 s 是 OGS 的步长，10、1 s 看时间步收敛）
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from ogs_io import read_msh, read_constant_blocks, read_restart, read_primary_values, read_vtk
from fe_mesh import OGSMesh
from transport import Transport
from gems_ogs import OGSGEMS, Kinetic
from ogs_models import harmonic_mean
from reactive_transport import run
from compare import error_table, compare_previous

OGS = HERE / 'ogs_input'
OUT = HERE / 'results'
OUT.mkdir(exist_ok=True)
dt_list = [float(a) for a in sys.argv[1:]] or [100.0, 10.0, 1.0]

D0, archie_m = 1.0e-10, 1.0          # ab1d.mcp：$DIFFUSION 9（D0 * phi^m）
t_end = 1.0e4

points, cells, _, _ = read_msh(OGS / 'ab1d.msh')
mesh = OGSMesh(points[:, :1], cells['line'], 'interval')
x = mesh.points[:, 0]
left, right = int(np.argmin(x)), int(np.argmax(x))

# 两端边界：常数（ab1d.bc）+ A、B 的时间曲线（ab1d.rfd 曲线 1–4：左 A、左 B、右 A、右 B）
curves = []
for blk in (OGS / 'ab1d.rfd').read_text().split('#CURVES')[1:]:
    rows = [l.split()[:2] for l in blk.split('\n') if l.strip() and l.split()[0][0].isdigit()]
    curves.append(np.array(rows, float))
comps = ['1-Ael', '2-Bel', '3-H', '4-Inrt', '5-O', '6-Zz']
bc = {'POINT0': np.zeros(6), 'POINT1': np.zeros(6)}
for pcs, var, geo, val in read_constant_blocks(OGS / 'ab1d.bc', '#BOUNDARY_CONDITION'):
    if var in comps:
        bc[geo][comps.index(var)] = val


def boundary_values(t):
    v = np.vstack([bc['POINT0'], bc['POINT1']])
    v[0, :2] = [np.interp(t, *curves[0].T), np.interp(t, *curves[1].T)]
    v[1, :2] = [np.interp(t, *curves[2].T), np.interp(t, *curves[3].T)]
    return v


def make_chemistry():
    chem = OGSGEMS(HERE / 'gems' / 'TestSolub-dat.lst', mesh.n_nodes, hydrology='hayekit', min_porosity=1e-15,
                   kinetics=[Kinetic('AB(s)', logk=(-7.69897,), n_H=(0.0,), area_model=4, area=1.0e4)],
                   boundary_nodes=[left, right])
    restart = read_restart(OGS / 'ab1d', mesh.n_nodes, chem.nIC, chem.nDC)
    c0 = read_primary_values(OGS / 'ab1d', 'MASS_TRANSPORT', comps)
    inner = np.flatnonzero(~chem.boundary)
    chem.init_from_restart(restart, c0, nodes=inner, update_porosity=True)
    return chem


runs = {}
for dt in dt_list:
    chem = make_chemistry()
    tr = Transport(mesh, fixed_nodes=[left, right])
    snaps = {}

    def prepare(step, t, dt):
        tr.phi_cell = chem.phi[mesh.cells].mean(1)
        tr.De_cell = harmonic_mean(D0 * chem.phi ** archie_m, mesh.cells)
        tr.fixed_values = boundary_values(t)

    def record(step, t, dt):
        if abs(t - 1000.0) < 1e-9 or abs(t - t_end) < 1e-9:
            snaps[t] = dict(A=chem.c[:, 0].copy(), B=chem.c[:, 1].copy(), phi=chem.phi.copy(), AB=chem.amounts('AB(s)').copy())

    log = run(chem, tr, [dt] * int(round(t_end / dt)), prepare=prepare, record=record, print_every=0)
    runs[dt] = snaps
    print(f'dt = {dt:g} s: {len(log)} steps, {log.wall_s.iloc[-1]:.1f} s, failed GEMS nodes {log.failed.sum()}')

# ---- 和 OGS（dt = 100 s）比较
o = np.argsort(x)
sel = o[1:-1]
ogs = read_vtk(HERE / 'reference' / 'ab1d0100.vtk')
assert np.allclose(np.sort(ogs['points'][:, 0]), x[o])
ro = np.argsort(ogs['points'][:, 0])[1:-1]
if 100.0 in runs:
    r = runs[100.0][t_end]
    table = error_table({'A': r['A'][sel], 'B': r['B'][sel], 'AB(s)': r['AB'][sel], 'porosity': r['phi'][sel]},
                        {'A': ogs['node__1-Ael'][ro], 'B': ogs['node__2-Bel'][ro], 'AB(s)': ogs['node__AB(s)'][ro],
                         'porosity': ogs['node__NodePorosity'][ro]})
    table.to_csv(OUT / 'error_vs_ogs.csv', index=False)
    print('\nvs OGS (dt = 100 s, t = 10000 s)\n' + table.to_string(index=False))

# ---- 和解析解比较
tab = np.load(HERE / 'reference' / 'hayekit_tables.npz')
rows = []
for tt, key in [(1000.0, 'analytical1000s'), (t_end, 'analytical10ks')]:
    for dt, snaps in runs.items():
        for q, k in [('A', '__C1x0'), ('B', '__C2x0'), ('phi', '__Porox0')]:
            ana = tab[key + k][1:-1]
            rows.append({'time_s': tt, 'dt_s': dt, 'quantity': q,
                         'max_rel_err': np.max(np.abs(snaps[tt][q][sel] - ana) / np.abs(ana))})
ana_table = pd.DataFrame(rows)
ana_table.to_csv(OUT / 'error_vs_analytical.csv', index=False)
print('\nvs analytical solution\n' + ana_table.pivot_table(index=['time_s', 'quantity'], columns='dt_s',
                                                             values='max_rel_err').to_string())

np.savez_compressed(OUT / 'profiles.npz', x=x[o], **{f'dt{int(dt)}_{int(t)}s_{q}': v[o] for dt, s in runs.items()
                                                    for t, d in s.items() for q, v in d.items()})
if 100.0 in runs:
    r = runs[100.0][t_end]
    compare_previous({'c': np.column_stack([r['A'][o], r['B'][o]]), 'phi': r['phi'][o], 'AB': r['AB'][o]},
                     HERE.parents[2] / 'HAYEKIT_GEMS_FEniCSx' / 'results' / 'profiles.npz',
                     rename=lambda k: f'dt100_10000s_{k}')
