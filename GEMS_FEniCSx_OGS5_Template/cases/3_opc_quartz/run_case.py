"""算例 3：OPC 混凝土 + 石英骨料（OGS5GEMDEV LookUp-Table Case1，bench.*）

10 m 一维柱，成分处处相同、两端封闭（只有扩散），石英按 Palandri 速率慢慢溶解，
和水泥相反应（碱–硅反应），1 万年。参考：OGS 在 4 个节点上的时间序列 reference/node*.dat（0 – 919 年）。

和模板的对应：
    初值        bench.ic 的总 b 向量 -> init_from_bulk（两遍平衡 + V_s 归一化，动力学相钉住）
                $CONSTRAINT_GEMS：Al 在 160–180 mol 之间的节点 Qtz >= 31999.95 mol，Amor-Sl = 0
    输运        Transport(lumped=True)，无边界条件；只输运 bench.mcp 标为可动的组分（不含 Inrt、Zz）
    化学        OGSGEMS(hydrology='none')（$FLAG_COUPLING_HYDROLOGY 0），石英、无定形硅两个动力学相

用法：python run_case.py [结束年份，默认 10000]
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from ogs_io import read_msh, read_constant_blocks
from fe_mesh import OGSMesh
from transport import Transport
from gems_ogs import OGSGEMS, Kinetic
from reactive_transport import run

OGS = HERE / 'ogs_input'
OUT = HERE / 'results'
OUT.mkdir(exist_ok=True)

YR = 3.156e7                         # OGS 输入里的 1 年
t_end = float(sys.argv[1]) * YR if len(sys.argv) > 1 else 10000.0 * YR
D_pore, tau = 2.0e-10, 1.0           # bench.mcp / .mmp
monitor_x = [0.1, 1.0, 5.0, 10.0]    # 参考 node1 / node10 / node50 / node100
# 步长：前 1000 年 1 年，之后 10 年（OGS 用 <= 1e5 s 的自适应步长；石英速率的时间尺度是几十年）
steps, t = [], 0.0
while t < t_end - 1.0:
    steps.append(min(1.0 * YR if t < 1000.0 * YR - 1.0 else 10.0 * YR, t_end - t))
    t += steps[-1]

points, cells, _, _ = read_msh(OGS / 'bench.msh')
mesh = OGSMesh(points[:, :1], cells['line'], 'interval')
x = mesh.points[:, 0]
monitor = [int(np.argmin(np.abs(x - xm))) for xm in monitor_x]

quartz = Kinetic('Qtz', logk=(-13.99, -16.29), n_H=(0.0, -0.5), area_model=1, area=4000.0)
amorph = Kinetic('Amor-Sl', area_model=1, area=0.0)                 # Silica-amorph：表面积 0
chem = OGSGEMS(HERE / 'gems' / 'OPC-norm-gas-dat.lst', mesh.n_nodes, hydrology='none', min_porosity=1e-4,
               kinetics=[quartz, amorph], retry=True)
comps = [f'{i + 1}-{e}' for i, e in enumerate(chem.elements)]
b_ic = np.zeros(chem.nIC)
for pcs, var, geo, val in read_constant_blocks(OGS / 'bench.ic', '#INITIAL_CONDITION'):
    if var in comps:
        b_ic[comps.index(var)] = val
lower = np.zeros((mesh.n_nodes, chem.nDC))
upper = np.full((mesh.n_nodes, chem.nDC), 1.0e6)
iQ, iA = chem.species.index('Qtz'), chem.species.index('Amor-Sl')
if 160.0 <= b_ic[chem.elements.index('Al')] <= 180.0:                # $CONSTRAINT_GEMS（判据：元素 0 = Al）
    lower[:, iQ], upper[:, iQ] = 3.19999541657500e+04, 1.0e6
lower[:, iA] = upper[:, iA] = 0.0
chem.init_from_bulk(b_ic, normalize=True, lower=lower, upper=upper, pin=['Qtz', 'Amor-Sl'])

mobile = [k for k, e in enumerate(chem.elements) if e not in ('Inrt', 'Zz')]
tr = Transport(mesh, lumped=True)

key_solids = ['Qtz', 'Portlandite', 'ECSH2-JenCa', 'ECSH2-TobCa', 'ECSH2-KSH', 'ECSH2-NaSH', 'ettringite',
              'Cal', 'hydrotalcite', 'Gp', 'Chabazite', 'Scolecite', 'Inert_Qtz']
history, profiles = [], {}


def prepare(step, t, dt):
    tr.phi_cell = chem.phi[mesh.cells].mean(1)
    tr.De_cell = tr.phi_cell * tau * D_pore


def record(step, t, dt):
    for xm, i in zip(monitor_x, monitor):
        row = {'time_yr': t / YR, 'x_m': xm, 'porosity': chem.phi[i], 'pH': chem.pH[i],
               'rate_qtz_mol_m3_yr': chem.dmdt[i, 0] * YR, 'omega_qtz': chem.omega[i, 0]}
        row.update({f'c_{e}': chem.c[i, k] for k, e in enumerate(chem.elements)})
        row.update({f'b_{e}': chem.b_fix[i, k] + chem.c[i, k] * chem.phi[i] for k, e in enumerate(chem.elements)})
        row.update({s: chem.amounts(s)[i] for s in key_solids})
        history.append(row)
    for ty in [10, 100, 300, 919, 3000, 10000]:
        if ty not in profiles and t >= ty * YR - 1.0:
            o = np.argsort(x)
            profiles[ty] = pd.DataFrame({'x_m': x[o], 'porosity': chem.phi[o], 'pH': chem.pH[o],
                                         **{s: chem.amounts(s)[o] for s in key_solids}})


record(0, 0.0, 0.0)
log = run(chem, tr, steps, mobile=mobile, prepare=prepare, record=record, print_every=200)
history = pd.DataFrame(history)
history.to_csv(OUT / 'monitor_timeseries.csv', index=False)
for ty, prof in profiles.items():
    prof.to_csv(OUT / f'profile_{ty}yr.csv', index=False)
print(f'{len(log)} steps, {log.wall_s.iloc[-1]:.0f} s, failed GEMS nodes {log.failed.sum()}')

# ---- 和 OGS 的时间序列比较（0 – 919 年，四个节点）
ref = {}
for xm, name in zip(monitor_x, ['node1', 'node10', 'node50', 'node100']):
    d = pd.read_csv(HERE / 'reference' / f'{name}.dat', sep=r'\s+', skiprows=1)
    d = d.sort_values('time').drop_duplicates('time').reset_index(drop=True).copy()
    d['time_yr'] = d['time'] / YR
    ref[xm] = d
compare = [('Qtz', 'Qtz'), ('Portlandite', 'Portlandite'), ('ECSH2-JenCa', 'ECSH2-JenCa'), ('ECSH2-TobCa', 'ECSH2-TobCa'),
           ('ECSH2-KSH', 'ECSH2-KSH'), ('ECSH2-NaSH', 'ECSH2-NaSH'), ('ettringite', 'ettringite'),
           ('Chabazite', 'Chabazite'), ('Scolecite', 'Scolecite'), ('Gp', 'Gp'), ('pH', 'pH'),
           ('porosity', 'NodePorosity'), ('c_Si', '14-Si'), ('c_Ca', '4-Ca'), ('c_Na', '11-Na'), ('c_K', '9-K'),
           ('c_Cl', '5-Cl'), ('b_H', 'H'), ('b_Cl', 'Cl')]
rows = []
for ours_key, ref_key in compare:
    worst_abs, worst_n = 0.0, 0.0
    for xm in monitor_x:
        o_ = history[history.x_m == xm]
        rr = ref[xm]
        a = np.interp(rr.time_yr.values, o_.time_yr.values, o_[ours_key].values)
        b = rr[ref_key].values
        worst_abs = max(worst_abs, float(np.max(np.abs(a - b))))
        if b.max() - b.min() > 1e-9:
            worst_n = max(worst_n, 100 * float(np.sqrt(np.mean((a - b) ** 2))) / (b.max() - b.min()))
    rows.append({'quantity': ref_key, 'max_abs_err': worst_abs, 'nRMSE_%': worst_n})
table = pd.DataFrame(rows)
table.to_csv(OUT / 'error_vs_ogs.csv', index=False)
print('\nvs OGS node time series (0 – 919 yr)\n' + table.to_string(index=False))

prev = HERE.parents[2] / 'OPC_quartz_GEMS_FEniCSx' / 'results' / 'monitor_timeseries.csv'
if prev.exists():
    p = pd.read_csv(prev)
    n = min(len(p), len(history))
    d = {k: np.abs(history[k].values[:n] - p[k].values[:n]).max() / max(np.abs(p[k].values[:n]).max(), 1e-300)
         for k in ['Qtz', 'Portlandite', 'ECSH2-TobCa', 'Chabazite', 'pH', 'porosity', 'c_Ca', 'c_Si']}
    print(f'\nvs earlier notebook (OPC_quartz_GEMS_FEniCSx): largest relative difference {max(d.values()):.2e}')
    print(pd.Series(d, name='max_rel_diff').to_string())
