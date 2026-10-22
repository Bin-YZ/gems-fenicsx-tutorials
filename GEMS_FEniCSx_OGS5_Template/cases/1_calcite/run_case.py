"""算例 1：calcite_gems（OGS5GEMDEV benchmarks/C/calcite_gems）

0.5 m 方解石柱，左端注入 MgCl2 溶液：方解石溶解，白云石在前锋后成带沉淀又溶掉。
一维、恒定 Darcy 通量、CG1 对流-弥散、无动力学。参考：calcite0210.vtk（t = 21000 s）。

和模板的对应：
    网格        ogs_input/calcite.msh  -> OGSMesh('interval')
    输运        Transport(q = 常数, alpha_L)，入口 Dirichlet
    化学        OGSGEMS(hydrology='full')，每节点一个 GEMS、热启动（warm_start）
    初值/边界   calcite.ic（DOMAIN + POINT0），calcite.bc（POINT0）
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import ufl

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from ogs_io import read_msh, read_constant_blocks, read_gli, read_vtk
from fe_mesh import OGSMesh
from transport import Transport
from gems_ogs import OGSGEMS
from reactive_transport import run
from compare import error_table, compare_previous

OGS = HERE / 'ogs_input'
OUT = HERE / 'results'
OUT.mkdir(exist_ok=True)

# ---- 参数（calcite.mmp / .mcp / .st / .tim / .gem）
q = 2.9984e-6            # m/s，.st 左端源项 / 截面积 1 m2
alpha_L = 0.0067         # m
Dm, tau = 1.0e-10, 1.0   # m2/s，.mcp；曲折度 .mmp
dt, n_steps = 100.0, 210

# ---- 网格
points, cells, _, _ = read_msh(OGS / 'calcite.msh')
mesh = OGSMesh(points[:, :1], cells['line'], 'interval')
gli, _ = read_gli(OGS / 'calcite.gli')
inlet = mesh.nodes_where(lambda p: np.isclose(p[:, 0], gli['POINT0'][0]))

# ---- 化学
chem = OGSGEMS(HERE / 'gems' / 'BC-dat.lst', mesh.n_nodes, hydrology='full', min_porosity=1e-4,
               accept=(2, 6), retry=True, warm_start=True, boundary_nodes=inlet)
comps = [f'{i + 1}-{e}' for i, e in enumerate(chem.elements)]          # 1-C 2-Ca ... 8-Zz
b_init = np.zeros((mesh.n_nodes, chem.nIC))
c_inlet = np.zeros(chem.nIC)
for pcs, var, geo, val in read_constant_blocks(OGS / 'calcite.ic', '#INITIAL_CONDITION'):
    if var in comps:
        sel = slice(None) if geo == 'DOMAIN' else inlet
        b_init[sel, comps.index(var)] = val
for pcs, var, geo, val in read_constant_blocks(OGS / 'calcite.bc', '#BOUNDARY_CONDITION'):
    if var in comps:
        c_inlet[comps.index(var)] = val
chem.init_from_bulk(b_init, normalize=False)          # calcite：一遍平衡，不做 V_s 归一化
chem.c[inlet] = c_inlet

# ---- 输运
tr = Transport(mesh, fixed_nodes=inlet, q=ufl.as_vector([q]), alpha_L=alpha_L)
tr.fixed_values = c_inlet


def prepare(step, t, dt):
    tr.phi_cell = chem.phi[mesh.cells].mean(1)            # ConvPorosityNodeValue2Elem
    tr.De_cell = tr.phi_cell * tau * Dm                   # phi * tau * Dm（弥散 alpha_L |q| 在 Transport 里）


log = run(chem, tr, [dt] * n_steps, prepare=prepare, print_every=30)

# ---- 结果与比较
x = mesh.points[:, 0]
o = np.argsort(x)
res = pd.DataFrame({'x_m': x[o], 'pH': chem.pH[o], 'NodePorosity': chem.phi[o],
                    **{cn: chem.c[o, k] for k, cn in enumerate(comps[:6])},
                    **{s: chem.amounts(s)[o] for s in ['Cal', 'Dis-Dol', 'Ca+2', 'Mg+2', 'Cl-', 'HCO3-', 'CO3-2', 'OH-']}})
res.to_csv(OUT / 'profiles_21000s.csv', index=False)
ref = read_vtk(HERE / 'reference' / 'calcite0210.vtk')
ro = np.argsort(ref['points'][:, 0])
assert np.allclose(ref['points'][ro, 0], x[o])
table = error_table(res, {k: ref['node__' + k][ro] for k in res.columns if 'node__' + k in ref})
table.to_csv(OUT / 'error_vs_ogs.csv', index=False)
print(table.to_string(index=False))
compare_previous(res, HERE.parents[2] / 'OGS5_calcite_GEMS_FEniCSx' / 'results' / 'profiles_21000s.csv',
                 rename=lambda k: f'{k}_fenicsx')
