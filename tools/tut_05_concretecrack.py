from nb import NB

nb = NB()
nb.md(en=r"""
# 5 · ConcreteCrack: a fracture in concrete, FEM-FCT and the limits of reproduction

**What you learn here**

- 1D fracture elements embedded in a 2D mesh (`LineElements`, OGS `GEOMETRY_AREA`)
- porosity-dependent permeability (Kozeny–Carman) and diffusion (`$DIFFUSION 8`)
- FEM-FCT for advection-dominated transport, and the OGS sign convention
- what **cannot** be reproduced: a head driven by GEMS round-off in an ill-conditioned flow problem

## The problem

A vertical x–z section of 2.5 × 10.5 cm (OGS5GEMDEV `PETSc/ConcreteCrack`, "decal"): 10 cm of concrete, a 5 mm
surface layer on top, and a 0.5 mm wide crack reaching 5 cm deep at the left edge. The top is in contact with a
solution containing nitrate (head 10.105 m), the bottom has head 10.0 m. The benchmark runs 10 steps of 1 s — it tests
the initialisation and the crack–matrix coupling rather than actual leaching.

| quantity | value | OGS file |
|---|---|---|
| mesh | 20 × 84 quadrilaterals + 40 line elements (crack) | `decal.msh` |
| crack aperture | 0.5 mm (`GEOMETRY_AREA`) | `decal.mmp` |
| $K_0$ | 10⁻⁹ (surface layer), 5·10⁻¹¹ (concrete), 0.41 m/s (crack); Kozeny–Carman | `decal.mmp` |
| diffusion | $D = 10^{-9}\,\phi^3/\phi_0^2$ × tortuosity (0.0383 / 1) | `decal.mcp`, `.mmp` |
| dispersivity | 10⁻⁵ / 10⁻⁶ m | `decal.mmp` |
| numerics | FEM-FCT, 3×3 Gauss | `decal.num` |
| initial chemistry | four zones: concrete, crack, surface layer, top boundary | `decal.ic` |
""", zh=r"""
# 5 · ConcreteCrack：混凝土裂缝、FEM-FCT 和复现的边界

**这一篇学什么**

- 嵌在二维网格里的一维裂缝单元（`LineElements`，OGS `GEOMETRY_AREA`）
- 随孔隙率变化的渗透率（Kozeny–Carman）和扩散（`$DIFFUSION 8`）
- 对流占优输运的 FEM-FCT，以及 OGS 的符号约定
- **不能**复现的东西：病态水流问题里由 GEMS 舍入误差驱动的水头

## 问题

2.5 × 10.5 cm 的竖直 x–z 剖面（OGS5GEMDEV `PETSc/ConcreteCrack`，“decal”）：10 cm 混凝土，上面 5 mm 表层，
左边一条 0.5 mm 宽、5 cm 深的裂缝。顶部接触含硝酸根的溶液（水头 10.105 m），底部水头 10.0 m。基准只算 10 步 × 1 s——
检验的是初始化和裂缝–基质耦合，而不是真正的溶蚀。

| 量 | 值 | OGS 文件 |
|---|---|---|
| 网格 | 20 × 84 四边形 + 40 个线单元（裂缝） | `decal.msh` |
| 裂缝开度 | 0.5 mm（`GEOMETRY_AREA`） | `decal.mmp` |
| $K_0$ | 10⁻⁹（表层）、5·10⁻¹¹（混凝土）、0.41 m/s（裂缝）；Kozeny–Carman | `decal.mmp` |
| 扩散 | $D = 10^{-9}\,\phi^3/\phi_0^2$ × 曲折度（0.0383 / 1） | `decal.mcp`、`.mmp` |
| 弥散度 | 10⁻⁵ / 10⁻⁶ m | `decal.mmp` |
| 数值方法 | FEM-FCT，3×3 Gauss | `decal.num` |
| 初始化学 | 四个区：混凝土、裂缝、表层、顶边 | `decal.ic` |
""", de=r"""
# 5 · ConcreteCrack: ein Riss im Beton, FEM-FCT und die Grenzen der Reproduktion

**Was Sie hier lernen**

- 1D-Risselemente, eingebettet in ein 2D-Netz (`LineElements`, OGS `GEOMETRY_AREA`)
- porositätsabhängige Permeabilität (Kozeny–Carman) und Diffusion (`$DIFFUSION 8`)
- FEM-FCT für advektionsdominierten Transport und die Vorzeichenkonvention von OGS
- was sich **nicht** reproduzieren lässt: eine Druckhöhe, die in einem schlecht konditionierten Strömungsproblem
  vom Rundungsrauschen von GEMS bestimmt wird

## Das Problem

Ein senkrechter x–z-Schnitt von 2,5 × 10,5 cm (OGS5GEMDEV `PETSc/ConcreteCrack`, „decal“): 10 cm Beton, darüber eine
5 mm dicke Oberflächenschicht und am linken Rand ein 0,5 mm breiter, 5 cm tiefer Riss. Oben steht eine nitrathaltige Lösung an
(Druckhöhe 10,105 m), unten 10,0 m. Der Benchmark rechnet 10 Schritte zu 1 s — er prüft die Initialisierung und die
Kopplung Riss–Matrix, nicht die eigentliche Auslaugung.

| Größe | Wert | OGS-Datei |
|---|---|---|
| Netz | 20 × 84 Vierecke + 40 Linienelemente (Riss) | `decal.msh` |
| Rissöffnung | 0,5 mm (`GEOMETRY_AREA`) | `decal.mmp` |
| $K_0$ | 10⁻⁹ (Oberflächenschicht), 5·10⁻¹¹ (Beton), 0,41 m/s (Riss); Kozeny–Carman | `decal.mmp` |
| Diffusion | $D = 10^{-9}\,\phi^3/\phi_0^2$ × Tortuosität (0,0383 / 1) | `decal.mcp`, `.mmp` |
| Dispersivität | 10⁻⁵ / 10⁻⁶ m | `decal.mmp` |
| Numerik | FEM-FCT, 3×3 Gauß | `decal.num` |
| Anfangschemie | vier Zonen: Beton, Riss, Oberflächenschicht, oberer Rand | `decal.ic` |
""")

nb.code(r"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.path import Path as MplPath

ROOT = next(p / 'GEMS_FEniCSx_OGS5_Template' for p in [Path.cwd(), *Path.cwd().parents]
            if (p / 'GEMS_FEniCSx_OGS5_Template').exists())
sys.path.insert(0, str(ROOT))
from ogs_io import read_msh, read_constant_blocks
from fe_mesh import OGSMesh
from flow import Darcy
from transport import Transport
from gems_ogs import OGSGEMS
from ogs_models import element_mean, harmonic_mean, porosity_diffusion_8, kozeny_carman_4, LineElements
from reactive_transport import run

CASE = ROOT / 'cases' / '5_concretecrack'
OGS = CASE / 'ogs_input'
plt.rcParams.update({'figure.dpi': 110, 'font.size': 9})
""")

nb.md(en="""
## Mesh with a fracture, and the four initial zones

The quadrilaterals become the dolfinx mesh. The 40 line elements of the crack share their nodes with the 2D mesh
at x = 0; `LineElements` assembles their contributions (every integral multiplied by the aperture) as sparse matrices that
are added to the 2D matrices. Their volume also enters the node volumes used for the excess-water source.

`decal.ic` overwrites the initial b vectors zone by zone: whole domain → crack nodes → surface layer → top edge.
""", zh="""
## 带裂缝的网格和四个初始区

四边形组成 dolfinx 网格。裂缝的 40 个线单元和二维网格共用 x = 0 上的节点；`LineElements` 把它们的贡献（所有积分乘开度）
组装成稀疏矩阵，加到二维矩阵上。它们的体积也计入多余水源项用的节点体积。

`decal.ic` 按区依次覆盖初始 b 向量：整个区域 → 裂缝节点 → 表层 → 顶边。
""", de="""
## Netz mit Riss und die vier Anfangszonen

Die Vierecke bilden das dolfinx-Netz. Die 40 Linienelemente des Risses teilen ihre Knoten mit dem 2D-Netz bei x = 0;
`LineElements` assembliert ihre Beiträge (jedes Integral mit der Öffnungsweite multipliziert) als dünnbesetzte Matrizen, die
zu den 2D-Matrizen addiert werden. Ihr Volumen geht auch in die Knotenvolumina für die Überschusswasser-Quelle ein.

`decal.ic` überschreibt die Anfangs-b-Vektoren zonenweise: ganzes Gebiet → Rissknoten → Oberflächenschicht → oberer Rand.
""")

nb.code(r"""
points, cells, mats, _ = read_msh(OGS / 'decal.msh')
xz = points[:, [0, 2]]
mesh = OGSMesh(xz, cells['quad'], 'quadrilateral')
mat = mats['quad']
crack = LineElements(mesh.n_nodes, xz, cells['line'], 0.5e-3)
node_volume = mesh.node_volume + crack.node_volume()

in_crack = (np.abs(xz[:, 0]) < 1e-6) & (xz[:, 1] >= -0.05 - 1e-6) & (xz[:, 1] <= 1e-4 + 1e-6)
top = MplPath(np.array([[0, .005], [0, .001], [.0005, 1e-4], [.025, .001], [.025, .005]]))
in_top = top.contains_points(xz, radius=1e-6) | top.contains_points(xz, radius=-1e-6)
upper = np.flatnonzero(np.isclose(xz[:, 1], 0.005))
lower = np.flatnonzero(np.isclose(xz[:, 1], -0.1))
zone = {'DOMAIN': np.ones(mesh.n_nodes, bool), 'SURF_1': in_crack, 'TOP': in_top, 'UPPER_BOUNDARY': np.isclose(xz[:, 1], 0.005)}

chem = OGSGEMS(CASE / 'gems' / 'cement_bc-dat.lst', mesh.n_nodes, hydrology='full', min_porosity=1e-6, boundary_nodes=upper)
comps = [f'{i + 1}-{e}' for i, e in enumerate(chem.elements)]
b_init = np.zeros((mesh.n_nodes, chem.nIC))
for pcs, var, geo, val in read_constant_blocks(OGS / 'decal.ic', '#INITIAL_CONDITION'):
    if var in comps:
        b_init[zone[geo], comps.index(var)] = val
c_upper, heads = np.zeros(chem.nIC), {}
for pcs, var, geo, val in read_constant_blocks(OGS / 'decal.bc', '#BOUNDARY_CONDITION'):
    if var in comps:
        c_upper[comps.index(var)] = val
    elif var == 'HEAD':
        heads[geo] = val
chem.init_from_bulk(b_init, normalize=True, lower=np.zeros(chem.nDC), upper=np.full(chem.nDC, 1e10))
state0 = {k: np.copy(getattr(chem, k)) for k in ('c', 'b_fix', 'water', 'Vf', 'phi', 'phi0', 'x', 'dll', 'dul', 'excess', 'pH')}
good0 = dict(chem._good)

p = xz * 1000
tri = mtri.Triangulation(p[:, 0], p[:, 1], np.vstack([mesh.cells[:, [0, 1, 2]], mesh.cells[:, [0, 2, 3]]]))
fig, ax = plt.subplots(1, 2, figsize=(9, 5))
m = ax[0].tripcolor(tri, chem.phi, shading='gouraud', cmap='viridis', vmax=0.2); fig.colorbar(m, ax=ax[0])
ax[0].plot(p[in_crack, 0], p[in_crack, 1], 'r-', lw=3, label='crack nodes'); ax[0].legend(fontsize=7)
ax[0].set_title('initial porosity (crack φ ≈ 1 not shown)')
m = ax[1].tripcolor(tri, chem.c[:, comps.index('7-N')], shading='gouraud', cmap='magma'); fig.colorbar(m, ax=ax[1])
ax[1].set_title('initial N in the pore water [mol/m³]'); ax[1].set_ylim(-15, 5.5)
for a in ax: a.set_aspect('equal'); a.set_xlabel('x [mm]'); a.set_ylabel('z [mm]')
plt.tight_layout(); plt.show()
""")

nb.md(en="""
## Coefficients that follow the porosity

In `prepare` the element permeability is the harmonic mean of the Kozeny–Carman values of its nodes, and the element
diffusion coefficient the harmonic mean of $10^{-9}\\phi^3/\\phi_0^2$ times the tortuosity. The crack gets the same laws
on its own elements. In `after_flow` (after the head is known) the crack velocity and its transport matrices are built.
""", zh="""
## 跟随孔隙率变化的系数

在 `prepare` 里，单元渗透系数是各节点 Kozeny–Carman 值的调和平均，单元扩散系数是 $10^{-9}\\phi^3/\\phi_0^2$ 的调和平均乘曲折度。
裂缝在自己的单元上用同样的规律。在 `after_flow` 里（水头已知之后）计算裂缝流速并组装它的输运矩阵。
""", de="""
## Koeffizienten, die der Porosität folgen

In `prepare` ist die Elementdurchlässigkeit das harmonische Mittel der Kozeny–Carman-Werte seiner Knoten, der
Elementdiffusionskoeffizient das harmonische Mittel von $10^{-9}\\phi^3/\\phi_0^2$ mal Tortuosität. Der Riss erhält dieselben
Gesetze auf seinen eigenen Elementen. In `after_flow` (nach Kenntnis der Druckhöhe) werden die Rissgeschwindigkeit und seine
Transportmatrizen aufgebaut.
""")

nb.code(r"""
k0_mat, tau_mat = np.array([1.0e-9, 5.0e-11, 0.41]), np.array([0.0383, 0.0383, 1.0])

def simulate(use_fct=True, ogs_sign=True, gems_source=True):
    chem = OGSGEMS(CASE / 'gems' / 'cement_bc-dat.lst', mesh.n_nodes, hydrology='full', min_porosity=1e-6, boundary_nodes=upper)
    for k, v in state0.items():
        setattr(chem, k, v.copy())
    chem._good = dict(good0)
    flow = Darcy(mesh, fixed_nodes=np.r_[upper, lower], quadrature_degree=5)
    flow.fixed_values = np.r_[np.full(len(upper), heads['UPPER_BOUNDARY']), np.full(len(lower), heads['LOWER_BOUNDARY'])]
    tr = Transport(mesh, fixed_nodes=upper, q=flow.q, alpha_L=1e-5, alpha_T=1e-6, fct=use_fct, fct_ogs_sign=ogs_sign, quadrature_degree=5)
    tr.fixed_values = c_upper
    lc, coef = crack.lines, {}

    def prepare(step, t, dt):
        phi, phi0 = chem.phi, chem.phi0
        tr.phi_cell = element_mean(phi, mesh.cells)
        tr.De_cell = tau_mat[mat] * harmonic_mean(porosity_diffusion_8(1e-9, phi, phi0, 2.0), mesh.cells)
        flow.K_cell = harmonic_mean(kozeny_carman_4(k0_mat[mat][:, None], phi0[mesh.cells], phi[mesh.cells]))
        coef.update(phi=element_mean(phi, lc), De=tau_mat[2] * harmonic_mean(porosity_diffusion_8(1e-9, phi, phi0, 2.0), lc),
                    K=harmonic_mean(kozeny_carman_4(k0_mat[2], phi0[lc], phi[lc])))
        flow.extra = crack.flow_matrix(coef['K'])

    def after_flow(step, t, dt):
        tr.M_extra, tr.K_extra = crack.transport_matrices(coef['phi'], coef['De'], 1e-5, crack.velocity(coef['K'], flow.head))

    log = run(chem, tr, [1.0] * 10, flow=flow, prepare=prepare, after_flow=after_flow,
              water_source=gems_source, node_volume=node_volume, print_every=0)
    return dict(c=chem.c.copy(), phi=chem.phi.copy(), pH=chem.pH.copy(), portlandite=chem.amounts('Portlandite').copy(),
                head=flow.head.copy(), excess=chem.excess.copy(), wall=log.wall_s.iloc[-1])

variants = {'OGS FCT': dict(), 'textbook FCT': dict(ogs_sign=False), 'no FCT': dict(use_fct=False),
            'no water source': dict(gems_source=False)}
runs = {}
for name, opt in variants.items():
    runs[name] = simulate(**opt)
    print(f'{name:16s} {runs[name]["wall"]:.0f} s')
""")

nb.md(en="""
## Comparison with OGS at t = 10 s
""", zh="""
## 和 OGS 比较（t = 10 s）
""", de="""
## Vergleich mit OGS bei t = 10 s
""")

nb.code(r"""
ref = np.load(CASE / 'reference' / 'ref_t10s.npz')
rows = []
for j, cn in enumerate(comps[:-2]):
    r_ = ref['node__' + cn]
    rows.append({'quantity': cn, **{n: np.abs(r['c'][:, j] - r_).max() / np.abs(r_).max() for n, r in runs.items()}})
for nm, key, rk in [('porosity', 'phi', 'NodePorosity'), ('pH', 'pH', 'Ph'), ('Portlandite', 'portlandite', 'Portlandite')]:
    r_ = ref['node__' + rk]
    rows.append({'quantity': nm, **{n: np.abs(r[key] - r_).max() / np.abs(r_).max() for n, r in runs.items()}})
r_ = ref['node__HEAD']
rows.append({'quantity': 'head − 10 m', **{n: np.abs(r['head'] - r_).max() / np.abs(r_ - 10).max() for n, r in runs.items()}})
display(pd.DataFrame(rows).set_index('quantity').style.format('{:.1e}').set_caption('max relative difference to OGS'))

main = runs['OGS FCT']
fig, ax = plt.subplots(1, 3, figsize=(12, 5))
for a, (title, val, cmap) in zip(ax, [('head − 10 m, OGS [mm]', (ref['node__HEAD'] - 10) * 1e3, 'Blues'),
                                       ('head − 10 m, template [mm]', (main['head'] - 10) * 1e3, 'Blues'),
                                       ('Ca: template − OGS [mol/m³]', main['c'][:, 2] - ref['node__3-Ca'], 'RdBu_r')]):
    lim = np.abs(val).max() if 'Ca' in title else None
    m = a.tripcolor(tri, val, shading='gouraud', cmap=cmap, vmin=-lim if lim else None, vmax=lim)
    fig.colorbar(m, ax=a); a.set_title(title); a.set_aspect('equal'); a.set_xlabel('x [mm]')
plt.tight_layout(); plt.show()
""")

nb.md(en="""
Concentrations, porosity, pH and portlandite agree to the level of GEMS's own scatter (nodes with identical composition
differ by ~10⁻³ in OGS itself). The **head does not agree**, in any variant. The next cell shows why.

## Why the head cannot be reproduced

The flow matrix couples a crack with $K = 0.41$ m/s to concrete with $K = 5\\times10^{-11}$ m/s — ten orders of magnitude.
Below, *the same matrix* is solved twice, once in OGS node order and once in dolfinx order:
""", zh="""
浓度、孔隙率、pH 和 portlandite 一致到 GEMS 自身离散的水平（OGS 自己的结果里，成分完全相同的节点之间也差约 10⁻³）。
**水头对不上**，哪个变体都一样。下一个单元格说明原因。

## 为什么水头无法复现

水流矩阵把 $K = 0.41$ m/s 的裂缝和 $K = 5\\times10^{-11}$ m/s 的混凝土耦合在一起——差十个数量级。
下面把*同一个矩阵*解两次，一次按 OGS 节点顺序，一次按 dolfinx 顺序：
""", de="""
Konzentrationen, Porosität, pH und Portlandit stimmen bis auf die Eigenstreuung von GEMS überein (Knoten mit identischer
Zusammensetzung unterscheiden sich schon in OGS um ~10⁻³). Die **Druckhöhe stimmt nicht überein**, in keiner Variante. Die
nächste Zelle zeigt, warum.

## Warum sich die Druckhöhe nicht reproduzieren lässt

Die Strömungsmatrix koppelt einen Riss mit $K = 0.41$ m/s an Beton mit $K = 5\\times10^{-11}$ m/s — zehn Größenordnungen.
Unten wird *dieselbe Matrix* zweimal gelöst, einmal in OGS-Knotenreihenfolge und einmal in dolfinx-Reihenfolge:
""")

nb.code(r"""
import scipy.sparse.linalg as spla
from dolfinx import fem
flow = Darcy(mesh, fixed_nodes=np.r_[upper, lower], quadrature_degree=5)
flow.K_cell = harmonic_mean(kozeny_carman_4(k0_mat[mat][:, None], state0['phi0'][mesh.cells], state0['phi'][mesh.cells]))
mesh.set_cells(flow._K, flow.K_cell)
lc = crack.lines
A_dof = fem.assemble_matrix(flow._form).to_scipy().tocsr()
A_ogs = A_dof[mesh.node2dof][:, mesh.node2dof] + crack.flow_matrix(harmonic_mean(kozeny_carman_4(0.41, state0['phi0'][lc], state0['phi'][lc])))
A_dof = A_ogs[mesh.dof2node][:, mesh.dof2node]
fixed = np.r_[upper, lower]
hb = np.r_[np.full(len(upper), heads['UPPER_BOUNDARY']), np.full(len(lower), heads['LOWER_BOUNDARY'])]
def solve(A, fixed, hb):
    free = np.setdiff1d(np.arange(A.shape[0]), fixed)
    h = np.zeros(A.shape[0]); h[fixed] = hb
    h[free] = spla.spsolve(A[free][:, free].tocsc(), -A[free][:, fixed] @ hb)
    return h
h1 = solve(A_ogs, fixed, hb)
h2 = solve(A_dof, mesh.node2dof[fixed], hb)[mesh.node2dof]
print(f'same matrix, two orderings: max head difference {np.abs(h1 - h2).max():.1e} m '
      f'(head range {np.ptp(h1) * 1e3:.0f} mm, conductivity contrast {0.41 / 5e-11:.0e})')
concrete = (xz[:, 1] < -0.051) & (xz[:, 0] > 0.003)
print(f'excess water V_aq - phi after the last step: concrete median {np.median(np.abs(main["excess"][concrete])):.0e}, '
      f'whole domain max {np.abs(main["excess"]).max():.0e} m³ per m³')
""")

nb.md(en="""
## Pitfalls found while reproducing this case

1. **The vtk has more points than the mesh.** `decal0010.vtk` was written by 4 PETSc processes one after another, ghost nodes
   included (1915 points for 1785 nodes). Map by coordinates; the `NodeVolume` field in it is GEMS's system volume, *not* the
   node volume used for the source term.
2. **Fracture elements** are multiplied by `GEOMETRY_AREA` in every integral (mass, diffusion, advection, flow). In the
   template they are plain 2×2 element matrices added to the global matrices.
3. **Kozeny–Carman at φ ≈ 1.** The crack porosity is 0.9999989 (only traces of inert solid), so $(1-\\phi_0)/(1-\\phi)$ is a
   ratio of two numbers of order 10⁻⁶. A tiny change of porosity changes the crack K from 0.41 to 0.4655 m/s — OGS does the
   same.
4. **FCT sign.** OGS adds $+f_{ij}$ to row $j$. Against this reference the OGS sign and the textbook sign cannot be told apart:
   the differences are smaller than the effect of the head round-off.
5. **The head.** The excess water $V_{aq}-\\phi$ is GEMS round-off ($10^{-10}$–$10^{-7}$), but with $K = 5\\times10^{-11}$ m/s it
   lifts the head by centimetres. Different GEMS versions give different noise, and the ill-conditioned flow matrix adds
   ~10⁻⁵ m by itself — a node-by-node head comparison is meaningless here.
""", zh="""
## 复现时遇到的坑

1. **vtk 的点比网格多。** `decal0010.vtk` 由 4 个 PETSc 进程依次写出，含 ghost 节点（1785 个节点写了 1915 个点）。要按坐标映射；
   里面的 `NodeVolume` 字段是 GEMS 的体系体积，*不是*源项用的节点体积。
2. **裂缝单元**的每个积分（质量、扩散、对流、水流）都乘 `GEOMETRY_AREA`。模板里它们就是加到全局矩阵上的 2×2 单元矩阵。
3. **φ ≈ 1 时的 Kozeny–Carman。** 裂缝孔隙率是 0.9999989（只有微量惰性固相），所以 $(1-\\phi_0)/(1-\\phi)$ 是两个 10⁻⁶ 量级的数相除。
   孔隙率一点点变化，裂缝 K 就从 0.41 变成 0.4655 m/s——OGS 也是这样。
4. **FCT 的符号。** OGS 在第 $j$ 行加 $+f_{ij}$。和这个参考比，OGS 符号和教科书符号分辨不出来：它们的差别比水头舍入误差的影响还小。
5. **水头。** 多余水 $V_{aq}-\\phi$ 是 GEMS 的舍入误差（$10^{-10}$–$10^{-7}$），但在 $K = 5\\times10^{-11}$ m/s 的混凝土里能把水头抬高几厘米。
   不同的 GEMS 版本噪声不同，病态的水流矩阵本身还带来约 10⁻⁵ m 的误差——这里逐节点比较水头没有意义。
""", de="""
## Stolpersteine bei der Reproduktion

1. **Die vtk hat mehr Punkte als das Netz.** `decal0010.vtk` wurde von 4 PETSc-Prozessen nacheinander geschrieben,
   einschließlich Geisterknoten (1915 Punkte für 1785 Knoten). Über Koordinaten zuordnen; das Feld `NodeVolume` darin ist das
   GEMS-Systemvolumen, *nicht* das Knotenvolumen für den Quellterm.
2. **Risselemente** werden in jedem Integral (Masse, Diffusion, Advektion, Strömung) mit `GEOMETRY_AREA` multipliziert. In der
   Vorlage sind sie einfache 2×2-Elementmatrizen, die zu den globalen Matrizen addiert werden.
3. **Kozeny–Carman bei φ ≈ 1.** Die Rissporosität ist 0,9999989 (nur Spuren inerten Feststoffs), $(1-\\phi_0)/(1-\\phi)$ ist also
   ein Quotient zweier Zahlen der Größenordnung 10⁻⁶. Eine winzige Porositätsänderung ändert das K des Risses von 0,41 auf
   0,4655 m/s — OGS tut dasselbe.
4. **FCT-Vorzeichen.** OGS addiert $+f_{ij}$ in Zeile $j$. Gegenüber dieser Referenz lassen sich OGS- und Lehrbuchvorzeichen nicht
   unterscheiden: die Unterschiede sind kleiner als der Effekt des Rundungsfehlers der Druckhöhe.
5. **Die Druckhöhe.** Das Überschusswasser $V_{aq}-\\phi$ ist Rundungsrauschen von GEMS ($10^{-10}$–$10^{-7}$), hebt aber bei
   $K = 5\\times10^{-11}$ m/s die Druckhöhe um Zentimeter. Verschiedene GEMS-Versionen erzeugen verschiedenes Rauschen, und die
   schlecht konditionierte Strömungsmatrix allein trägt ~10⁻⁵ m bei — ein knotengenauer Vergleich der Druckhöhe ist hier sinnlos.
""")

nb.md(en="""
## Exercises

1. Run 1000 steps of 1 s (or 100 steps of 100 s). Where does leaching start first, along the crack or at the surface?
2. Close the crack: give the line elements the concrete permeability. How do head and N penetration change?
3. Replace the direct solver of `Darcy` by scaling the matrix rows (Jacobi) before solving. Does the ordering
   dependence of the head shrink?
""", zh="""
## 练习

1. 算 1000 步 × 1 s（或 100 步 × 100 s）。溶蚀先从哪里开始，沿裂缝还是在表面？
2. 把裂缝“封上”：线单元用混凝土的渗透系数。水头和 N 的侵入深度怎么变？
3. 在 `Darcy` 求解前先按行缩放矩阵（Jacobi）。水头对节点顺序的依赖变小了吗？
""", de="""
## Übungen

1. Rechnen Sie 1000 Schritte zu 1 s (oder 100 Schritte zu 100 s). Wo beginnt die Auslaugung zuerst, entlang des Risses oder an der Oberfläche?
2. Schließen Sie den Riss: geben Sie den Linienelementen die Durchlässigkeit des Betons. Wie ändern sich Druckhöhe und Eindringen von N?
3. Skalieren Sie in `Darcy` die Matrixzeilen (Jacobi) vor dem Lösen. Wird die Abhängigkeit der Druckhöhe von der Reihenfolge kleiner?
""")

nb.save('05_concretecrack')
