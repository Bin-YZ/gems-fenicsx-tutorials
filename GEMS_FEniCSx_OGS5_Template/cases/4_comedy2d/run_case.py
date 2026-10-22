"""算例 4：comedy2d（OGS5GEMDEV benchmarks/PETSc/comedy2d，多组分水泥反应运移）

14 x 14 cm 二维饱和区，中间一条水泥带；左上注入 NaCl、顶部注入草酸钠，右侧出口定水头。
Portlandite、CaOxaHyd 两个动力学相；GEMS 的多余水作为下一步流动的源项。
从 OGS 重启文件开始算 6 步（10 s × 1.05^k，共 68 s），和 cement2d0006.vtk 比较（reference/ref_t68s.npz）。

和模板的对应：
    流动        Darcy(出口定水头，入口节点源项)，K 按材料
    输运        Transport(q = 流动的 Darcy 通量，alpha_L = alpha_T = 0.02 m)，入口 Dirichlet
    化学        OGSGEMS(hydrology='full')，Kinetic(表面积模型 3)，CheckConstraints、MaxDtKinetics 子步、
                种子判据 Omega >= 1.1 —— 这些是 2015 年 OGS-GEM 的写法
    初值        OGS 重启文件 -> init_from_restart(pin_kinetic=True)

retry_perturb=1e-12：不是 OGS 的规则。新版 GEMS3K 在个别前沿节点上会因为舍入误差返回 ERR（同样的输入改动第 12 位
有效数字就收敛），不加这一条，那个节点整步保持旧值，局部 Ca 差 10%，水头差 1e-6。

用 limits='loose' 和 'strict' 各算一次（OGS 的 $LOOSE_KINETICS 开关），loose 是和参考一致的那个。
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from ogs_io import read_msh, read_restart, read_gli, nodes_on_polyline
from fe_mesh import OGSMesh
from flow import Darcy
from transport import Transport
from gems_ogs import OGSGEMS, Kinetic
from reactive_transport import run
from compare import error_table, compare_previous

OGS = HERE / 'ogs_input'
OUT = HERE / 'results'
OUT.mkdir(exist_ok=True)

D0, alpha = 3.333333e-9, 0.02                      # .mcp 扩散系数；.mmp 弥散度
K_mat = np.array([1.0e-5, 1.64e-6, 1.0e-5])        # .mmp 渗透系数 m/s，材料 0 / 1（水泥）/ 2
tau_mat = np.array([1.0, 1.578949, 1.0])
q_inlet1, q_inlet2 = 5.7143e-10, 11.429e-10        # .st，每个入口节点 m3/s
h_outlet = 10.0
bc_inlet1 = np.array([9.96740295734440e-04, 1.99348059146888e-03, 1.99362013511029e+01, 1.01064827675428e-03,
                      1.99348059146889e+01, 2.27326337437258e-02, 9.96740295734440e-04, 0.0])   # .bc，C Ca Cl H Na O Oxa Si
bc_inlet2 = np.array([9.86453094520442e-06, 9.86453094519933e-06, 1.68789503224731e-05, 1.58035254545903e-01,
                      7.89162492495330e+02, 1.98600359071739e-02, 3.94660154055751e+02, 0.0])
time_steps = [10.0 * 1.05 ** k for k in range(6)]

points, cells, mats, _ = read_msh(OGS / 'cement2d.msh')
mesh = OGSMesh(points[:, :2], cells['quad'], 'quadrilateral')
mat = mats['quad']
_, lines = read_gli(OGS / 'cement2d.gli')
inlet1 = nodes_on_polyline(mesh.points, lines['INLET_1'][:, :2], 1e-4)
inlet2 = nodes_on_polyline(mesh.points, lines['INLET_2'][:, :2], 1e-4)
outlet = nodes_on_polyline(mesh.points, lines['OUTLET'][:, :2], 1e-4)
inlets = np.r_[inlet1, inlet2]

flow = Darcy(mesh, fixed_nodes=outlet)
flow.K_cell = K_mat[mat]
flow.fixed_values = h_outlet
flow.sources[inlet1] = q_inlet1
flow.sources[inlet2] = q_inlet2
tr = Transport(mesh, fixed_nodes=inlets, q=flow.q, alpha_L=alpha, alpha_T=alpha)
tr.fixed_values = np.vstack([np.tile(bc_inlet1, (len(inlet1), 1)), np.tile(bc_inlet2, (len(inlet2), 1))])
mobile = list(range(8))                            # 9-Zz 不动

# OGS 输出的单元速度在第 0 个高斯点（2x2 Gauss，ξ = η = +0.7746）
gp = 0.774596669241483
dN_r = 0.25 * np.array([1 + gp, -(1 + gp), -(1 - gp), 1 - gp])
dN_s = 0.25 * np.array([1 + gp, 1 - gp, -(1 - gp), -(1 + gp)])
X_e, Y_e = mesh.points[mesh.cells, 0], mesh.points[mesh.cells, 1]
J11, J12, J21, J22 = X_e @ dN_r, Y_e @ dN_r, X_e @ dN_s, Y_e @ dN_s
detJ = J11 * J22 - J12 * J21


def run_comedy(limits):
    chem = OGSGEMS(HERE / 'gems' / 'I1SetUp-dat.lst', mesh.n_nodes, hydrology='full', min_porosity=1e-6,
                   kinetics=[Kinetic('Portlandite', logk=(-5.0,), n_H=(0.0,), area_model=3, area=1000.0),
                             Kinetic('CaOxaHyd', logk=(-5.0,), n_H=(0.0,), area_model=3, area=1000.0)],
                   limits=limits, seed_omega=1.1, seed_needs_rate=True, check_lower_limits=True,
                   substep_kinetics=True, retry_perturb=1e-12, boundary_nodes=inlets)
    restart = read_restart(OGS / 'cement2d', mesh.n_nodes, chem.nIC, chem.nDC)
    chem.init_from_restart(restart, restart['solute'], update_porosity=False, pin_kinetic=True)

    def prepare(step, t, dt):
        tr.phi_cell = chem.phi[mesh.cells].mean(1)
        tr.De_cell = tr.phi_cell * D0 * tau_mat[mat]

    log = run(chem, tr, time_steps, flow=flow, mobile=mobile, prepare=prepare, print_every=0)
    h = flow.head
    hx = (J22 * (h[mesh.cells] @ dN_r) - J12 * (h[mesh.cells] @ dN_s)) / detJ
    hy = (-J21 * (h[mesh.cells] @ dN_r) + J11 * (h[mesh.cells] @ dN_s)) / detJ
    print(f'limits = {limits}: t = {log.t.iloc[-1]:.6f} s, {log.wall_s.iloc[-1]:.0f} s, '
          f'failed {log.failed.tolist()}, sub-stepped {log.substepped.tolist()}')
    return dict(c=chem.c.copy(), phi=chem.phi.copy(), x=chem.x.copy(), pH=chem.pH.copy(), head=h.copy(),
                vx=-K_mat[mat] * hx, vy=-K_mat[mat] * hy, phi_elem=chem.phi[mesh.cells].mean(1), species=chem.species)


runs = {lim: run_comedy(lim) for lim in ('loose', 'strict')}
ref = np.load(HERE / 'reference' / 'ref_t68s.npz')
assert np.abs(ref['points'][:, :2] - mesh.points).max() < 1e-6
names = ['1-C', '2-Ca', '3-Cl', '4-H', '5-Na', '6-O', '7-Oxa']
tables = []
for lim, r in runs.items():
    sp_ = r['species']
    ours = {**{n: r['c'][:, k] for k, n in enumerate(names)}, 'NodePorosity': r['phi'], 'pH': r['pH'], 'HEAD': r['head'],
            'Portlandite': r['x'][:, sp_.index('Portlandite')], 'CaOxaHyd': r['x'][:, sp_.index('CaOxaHyd')],
            'VELOCITY1_X': r['vx'], 'VELOCITY1_Y': r['vy'], 'POROSITY': r['phi_elem']}
    refd = {k: ref[('cell__' if k in ('VELOCITY1_X', 'VELOCITY1_Y', 'POROSITY') else 'node__') + k] for k in ours}
    t = error_table(ours, refd)
    t.insert(0, 'limits', lim)
    tables.append(t)
table = pd.concat(tables)
table.to_csv(OUT / 'error_vs_ogs.csv', index=False)
print('\nvs OGS (t = 68 s)\n' + table.to_string(index=False))
np.savez_compressed(OUT / 'comedy2d_t68s.npz', **{f'{lim}_{q}': v for lim, r in runs.items()
                                                   for q, v in r.items() if q != 'species'})
r = runs['loose']
compare_previous({'c': r['c'], 'phi': r['phi'], 'x': r['x'], 'head': r['head'], 'vx': r['vx']},
                 HERE.parents[2] / 'COMEDY2D_GEMS_FEniCSx' / 'results' / 'comedy2d_t68s.npz',
                 rename=lambda k: f'loose1_{k}')
