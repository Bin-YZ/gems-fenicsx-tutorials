"""算例 5：ConcreteCrack（OGS5GEMDEV benchmarks/PETSc/ConcreteCrack，带裂缝混凝土的溶蚀 decal）

x–z 竖直剖面 2.5 × 10.5 cm：下面 10 cm 混凝土，上面 5 mm 表层，左边一条 5 cm 深、0.5 mm 宽的裂缝
（40 个一维线单元，和二维网格共用 x = 0 的节点）。顶部浸泡溶液（含 N），水头 10.105 m，底部 10.0 m。
10 步 × 1 s，和 decal0010.vtk 比较（reference/ref_t10s.npz）。

和模板的对应：
    网格        四边形 + 线单元：OGSMesh（二维）+ ogs_models.LineElements（裂缝，乘开度 5e-4）
    流动        Darcy（上下定水头）；K = Kozeny–Carman（模型 4），节点值的调和平均；每步重算
    输运        Transport(q = 流动通量，alpha_L / alpha_T 张量，3x3 Gauss，FEM-FCT 照 OGS 的符号)
                扩散模型 8：节点 D = 1e-9 phi^3 / phi0^2，单元调和平均，乘曲折度
    化学        OGSGEMS(hydrology='full')，无动力学；init_from_bulk 两遍平衡（V_s 归一化）
    多余水      GEMS 水相体积 - 孔隙率 -> 下一步流动的源项（节点体积含裂缝单元）

主结果之外再算三个对照：教科书 FCT 符号、不用 FCT、不加 GEMS 多余水源项。
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from matplotlib.path import Path as MplPath

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from ogs_io import read_msh, read_constant_blocks
from fe_mesh import OGSMesh
from flow import Darcy
from transport import Transport
from gems_ogs import OGSGEMS
from ogs_models import element_mean, harmonic_mean, porosity_diffusion_8, kozeny_carman_4, LineElements
from reactive_transport import run
from compare import error_table, compare_previous

OGS = HERE / 'ogs_input'
OUT = HERE / 'results'
OUT.mkdir(exist_ok=True)

dt, n_steps = 1.0, 10
k0_mat = np.array([1.0e-9, 5.0e-11, 0.41])      # .mmp 初始渗透系数 m/s：表层 / 混凝土 / 裂缝
tau_mat = np.array([0.0383, 0.0383, 1.0])        # 曲折度
aperture = 0.5e-3                                # 裂缝 GEOMETRY_AREA
D_pore, m_archie = 1.0e-9, 2.0                   # $DIFFUSION 8
alpha_L, alpha_T = 1.0e-5, 1.0e-6

points, cells, mats, _ = read_msh(OGS / 'decal.msh')
xz = points[:, [0, 2]]
mesh = OGSMesh(xz, cells['quad'], 'quadrilateral')
mat = mats['quad']
crack = LineElements(mesh.n_nodes, xz, cells['line'], aperture)
node_volume = mesh.node_volume + crack.node_volume()

# 初值的四个区（decal.ic 依次覆盖）和边界
in_crack = (np.abs(xz[:, 0]) < 1e-6) & (xz[:, 1] >= -0.05 - 1e-6) & (xz[:, 1] <= 1e-4 + 1e-6)     # SURF_1
top_polygon = MplPath(np.array([[0, .005], [0, .001], [.0005, 1e-4], [.025, .001], [.025, .005]]))   # PLY_TOP
in_top = top_polygon.contains_points(xz, radius=1e-6) | top_polygon.contains_points(xz, radius=-1e-6)
upper = np.flatnonzero(np.isclose(xz[:, 1], 0.005))
lower = np.flatnonzero(np.isclose(xz[:, 1], -0.1))
zone = {'DOMAIN': np.ones(mesh.n_nodes, bool), 'SURF_1': in_crack, 'TOP': in_top, 'UPPER_BOUNDARY': np.isclose(xz[:, 1], 0.005)}

chem_options = dict(hydrology='full', min_porosity=1e-6, boundary_nodes=upper)
probe = OGSGEMS(HERE / 'gems' / 'cement_bc-dat.lst', 1)
comps = [f'{i + 1}-{e}' for i, e in enumerate(probe.elements)]
b_init = np.zeros((mesh.n_nodes, probe.nIC))
for pcs, var, geo, val in read_constant_blocks(OGS / 'decal.ic', '#INITIAL_CONDITION'):
    if var in comps:
        b_init[zone[geo], comps.index(var)] = val
c_upper = np.zeros(probe.nIC)
heads = {}
for pcs, var, geo, val in read_constant_blocks(OGS / 'decal.bc', '#BOUNDARY_CONDITION'):
    if var in comps:
        c_upper[comps.index(var)] = val
    elif var == 'HEAD':
        heads[geo] = val

# 初始化一次（两遍平衡、不受约束），四个变体都从这个状态出发
chem0 = OGSGEMS(HERE / 'gems' / 'cement_bc-dat.lst', mesh.n_nodes, **chem_options)
chem0.init_from_bulk(b_init, normalize=True, lower=np.zeros(chem0.nDC), upper=np.full(chem0.nDC, 1e10))
state0 = {k: np.copy(getattr(chem0, k)) for k in ('c', 'b_fix', 'water', 'Vf', 'phi', 'phi0', 'x', 'dll', 'dul', 'excess', 'pH')}
good0 = dict(chem0._good)


def run_case(use_fct=True, ogs_sign=True, gems_source=True):
    chem = OGSGEMS(HERE / 'gems' / 'cement_bc-dat.lst', mesh.n_nodes, **chem_options)
    for k, v in state0.items():
        setattr(chem, k, v.copy())
    chem._good = dict(good0)
    flow = Darcy(mesh, fixed_nodes=np.r_[upper, lower], quadrature_degree=5)
    flow.fixed_values = np.r_[np.full(len(upper), heads['UPPER_BOUNDARY']), np.full(len(lower), heads['LOWER_BOUNDARY'])]
    tr = Transport(mesh, fixed_nodes=upper, q=flow.q, alpha_L=alpha_L, alpha_T=alpha_T,
                   fct=use_fct, fct_ogs_sign=ogs_sign, quadrature_degree=5)
    tr.fixed_values = c_upper
    lc = crack.lines
    coef = {}

    def prepare(step, t, dt):
        phi, phi0 = chem.phi, chem.phi0
        tr.phi_cell = element_mean(phi, mesh.cells)
        tr.De_cell = tau_mat[mat] * harmonic_mean(porosity_diffusion_8(D_pore, phi, phi0, m_archie), mesh.cells)
        flow.K_cell = harmonic_mean(kozeny_carman_4(k0_mat[mat][:, None], phi0[mesh.cells], phi[mesh.cells]))
        coef['phi'] = element_mean(phi, lc)
        coef['De'] = tau_mat[2] * harmonic_mean(porosity_diffusion_8(D_pore, phi, phi0, m_archie), lc)
        coef['K'] = harmonic_mean(kozeny_carman_4(k0_mat[2], phi0[lc], phi[lc]))
        flow.extra = crack.flow_matrix(coef['K'])

    def after_flow(step, t, dt):
        v = crack.velocity(coef['K'], flow.head)
        tr.M_extra, tr.K_extra = crack.transport_matrices(coef['phi'], coef['De'], alpha_L, v)

    log = run(chem, tr, [dt] * n_steps, flow=flow, prepare=prepare, after_flow=after_flow,
              water_source=gems_source, node_volume=node_volume, print_every=0)
    return dict(c=chem.c.copy(), phi=chem.phi.copy(), pH=chem.pH.copy(), portlandite=chem.amounts('Portlandite').copy(),
                head=flow.head.copy(), failed=int(log.failed.sum()))


variants = {'OGS FCT (main)': dict(), 'textbook FCT sign': dict(ogs_sign=False),
            'no FCT': dict(use_fct=False), 'no GEMS water source': dict(gems_source=False)}
runs = {}
for name, opt in variants.items():
    runs[name] = run_case(**opt)
    print(f'{name}: failed GEMS nodes {runs[name]["failed"]}')

ref = np.load(HERE / 'reference' / 'ref_t10s.npz')
assert np.abs(ref['xz'] - xz).max() < 1e-9
rows = []
for j, cn in enumerate(comps[:-2]):             # Sn（溶液里为 0）和 Zz（电荷噪声）不比较
    r_val = ref['node__' + cn]
    rows.append({'quantity': cn, **{n: np.abs(r['c'][:, j] - r_val).max() / np.abs(r_val).max() for n, r in runs.items()}})
for nm, key, rk in [('porosity', 'phi', 'NodePorosity'), ('pH', 'pH', 'Ph'), ('Portlandite', 'portlandite', 'Portlandite')]:
    r_val = ref['node__' + rk]
    rows.append({'quantity': nm, **{n: np.abs(r[key] - r_val).max() / np.abs(r_val).max() for n, r in runs.items()}})
r_val = ref['node__HEAD']
rows.append({'quantity': 'head - 10 m', **{n: np.abs(r['head'] - r_val).max() / np.abs(r_val - 10).max() for n, r in runs.items()}})
table = pd.DataFrame(rows)
table.to_csv(OUT / 'error_vs_ogs.csv', index=False)
pd.set_option('display.float_format', '{:.2e}'.format)
print('\nmax relative difference to OGS (t = 10 s)\n' + table.to_string(index=False))
main = runs['OGS FCT (main)']
np.savez_compressed(OUT / 'concretecrack_t10s.npz', **{k: v for k, v in main.items() if k != 'failed'})
compare_previous({k: main[k] for k in ('c', 'phi', 'pH', 'portlandite', 'head')},
                 HERE.parents[2] / 'ConcreteCrack_GEMS_FEniCSx' / 'results' / 'concretecrack_t10s.npz')
