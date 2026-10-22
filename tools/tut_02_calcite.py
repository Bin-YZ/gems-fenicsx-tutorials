from nb import NB

nb = NB()
nb.md(en=r"""
# 2 · Calcite column: an equilibrium front moving with the flow

**What you learn here**

- advection–dispersion of all element totals with a constant Darcy flux
- a pure **equilibrium** problem (no kinetics): dissolution and precipitation fronts
- the OGS rules converting between transported concentrations and node amounts (`hydrology='full'`)
- why the differences to OGS sit almost entirely at one node

## The problem

A 0.5 m column filled with calcite and an inert filler (OGS5GEMDEV `C/calcite_gems`, the classic
benchmark of Engesgaard & Kipp). A MgCl₂ solution is injected at the left end. Calcite dissolves, Mg
precipitates as **dolomite** in a band just behind the dissolution front, and the dolomite is dissolved
again when the front has passed.

$$\phi\,\frac{\partial c}{\partial t} + q\,\frac{\partial c}{\partial x}
 - \frac{\partial}{\partial x}\Big(\phi\,D\,\frac{\partial c}{\partial x}\Big) = 0,
\qquad \phi D = \phi\,\tau D_m + \alpha_L\,q$$

| quantity | value | OGS file |
|---|---|---|
| column, mesh | 0.5 m, 100 line elements | `calcite.msh` |
| Darcy flux $q$ | 2.9984·10⁻⁶ m/s (source at x = 0, area 1 m²) | `calcite.st` |
| dispersivity $\alpha_L$ | 0.0067 m | `calcite.mmp` |
| molecular diffusion | 10⁻¹⁰ m²/s, tortuosity 1 | `calcite.mcp` |
| time | 210 × 100 s | `calcite.tim` |
| initial / inlet chemistry | total b vectors (column, inlet node) | `calcite.ic` |
| inlet concentration | mol per m³ fluid, solvent water excluded | `calcite.bc` |
""", zh=r"""
# 2 · 方解石柱：随水流移动的平衡前锋

**这一篇学什么**

- 恒定 Darcy 通量下所有元素总量的对流–弥散
- 纯**平衡**问题（没有动力学）：溶解前锋和沉淀前锋
- OGS 在输运浓度和节点物质的量之间换算的规则（`hydrology='full'`）
- 为什么和 OGS 的差几乎全在一个节点上

## 问题

0.5 m 的柱子，装着方解石和惰性填料（OGS5GEMDEV `C/calcite_gems`，Engesgaard & Kipp 的经典基准）。左端注入 MgCl₂ 溶液。
方解石溶解，Mg 在溶解前锋后面以**白云石**的形式成带沉淀，前锋过去后白云石又被溶掉。

$$\phi\,\frac{\partial c}{\partial t} + q\,\frac{\partial c}{\partial x}
 - \frac{\partial}{\partial x}\Big(\phi\,D\,\frac{\partial c}{\partial x}\Big) = 0,
\qquad \phi D = \phi\,\tau D_m + \alpha_L\,q$$

| 量 | 值 | OGS 文件 |
|---|---|---|
| 柱长、网格 | 0.5 m，100 个线单元 | `calcite.msh` |
| Darcy 通量 $q$ | 2.9984·10⁻⁶ m/s（x = 0 的源项，截面 1 m²） | `calcite.st` |
| 弥散度 $\alpha_L$ | 0.0067 m | `calcite.mmp` |
| 分子扩散 | 10⁻¹⁰ m²/s，曲折度 1 | `calcite.mcp` |
| 时间 | 210 × 100 s | `calcite.tim` |
| 初始 / 入口化学 | 总 b 向量（柱内、入口节点） | `calcite.ic` |
| 入口浓度 | 每 m³ 流体的 mol，不含溶剂水 | `calcite.bc` |
""", de=r"""
# 2 · Calcitsäule: eine Gleichgewichtsfront, die mit der Strömung wandert

**Was Sie hier lernen**

- Advektion–Dispersion aller Elementsummen bei konstantem Darcy-Fluss
- ein reines **Gleichgewichts**problem (keine Kinetik): Lösungs- und Fällungsfronten
- die OGS-Regeln für die Umrechnung zwischen transportierten Konzentrationen und Knotenmengen (`hydrology='full'`)
- warum die Abweichungen zu OGS fast vollständig an einem Knoten liegen

## Das Problem

Eine 0,5 m lange Säule mit Calcit und inertem Füllstoff (OGS5GEMDEV `C/calcite_gems`, der klassische Benchmark
von Engesgaard & Kipp). Am linken Ende wird MgCl₂-Lösung eingeleitet. Calcit löst sich, Mg fällt in einem Band
direkt hinter der Lösungsfront als **Dolomit** aus, und der Dolomit wird wieder gelöst, sobald die Front vorbei ist.

$$\phi\,\frac{\partial c}{\partial t} + q\,\frac{\partial c}{\partial x}
 - \frac{\partial}{\partial x}\Big(\phi\,D\,\frac{\partial c}{\partial x}\Big) = 0,
\qquad \phi D = \phi\,\tau D_m + \alpha_L\,q$$

| Größe | Wert | OGS-Datei |
|---|---|---|
| Säule, Netz | 0,5 m, 100 Linienelemente | `calcite.msh` |
| Darcy-Fluss $q$ | 2,9984·10⁻⁶ m/s (Quelle bei x = 0, Fläche 1 m²) | `calcite.st` |
| Dispersivität $\alpha_L$ | 0,0067 m | `calcite.mmp` |
| molekulare Diffusion | 10⁻¹⁰ m²/s, Tortuosität 1 | `calcite.mcp` |
| Zeit | 210 × 100 s | `calcite.tim` |
| Anfangs-/Zuflusschemie | b-Gesamtvektoren (Säule, Zuflussknoten) | `calcite.ic` |
| Zuflusskonzentration | mol pro m³ Fluid, ohne Lösungsmittel Wasser | `calcite.bc` |
""")

nb.code(r"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ufl

ROOT = next(p / 'GEMS_FEniCSx_OGS5_Template' for p in [Path.cwd(), *Path.cwd().parents]
            if (p / 'GEMS_FEniCSx_OGS5_Template').exists())
sys.path.insert(0, str(ROOT))
from ogs_io import read_msh, read_constant_blocks, read_gli, read_vtk
from fe_mesh import OGSMesh
from transport import Transport
from gems_ogs import OGSGEMS
from reactive_transport import run
from compare import error_table

CASE = ROOT / 'cases' / '1_calcite'
OGS = CASE / 'ogs_input'
plt.rcParams.update({'figure.dpi': 110, 'font.size': 9, 'axes.grid': True, 'grid.alpha': 0.3})
""")

nb.md(en="""
## Mesh, chemistry and initial state

The initial condition file gives **total b vectors per m³ of porous medium** — one for the column and one
for the inlet node `POINT0`. The boundary condition file gives the inlet **concentrations in mol per m³ of
fluid without the solvent water** — a different unit, easy to mix up.

GEMS runs at every node with its own engine and warm starts (`warm_start=True`), as in the earlier
stand-alone reproduction. One GEMS pass, no volume normalisation.
""", zh="""
## 网格、化学和初始状态

初始条件文件给的是**每 m³ 多孔介质的总 b 向量**——柱内一个、入口节点 `POINT0` 一个。边界条件文件给的是入口**浓度，
单位是每 m³ 流体的 mol，不含溶剂水**——单位不同，容易搞混。

GEMS 在每个节点用各自的引擎、热启动（`warm_start=True`），和之前单独复现时一样。算一遍，不做体积归一化。
""", de="""
## Netz, Chemie und Anfangszustand

Die Anfangsbedingungsdatei enthält **b-Gesamtvektoren pro m³ porösem Medium** — einen für die Säule und einen
für den Zuflussknoten `POINT0`. Die Randbedingungsdatei enthält die Zufluss**konzentrationen in mol pro m³ Fluid
ohne das Lösungsmittel Wasser** — eine andere Einheit, leicht zu verwechseln.

GEMS rechnet an jedem Knoten mit einer eigenen Engine und Warmstarts (`warm_start=True`), wie in der früheren
eigenständigen Reproduktion. Ein GEMS-Durchlauf, keine Volumennormierung.
""")

nb.code(r"""
points, cells, _, _ = read_msh(OGS / 'calcite.msh')
mesh = OGSMesh(points[:, :1], cells['line'], 'interval')
gli, _ = read_gli(OGS / 'calcite.gli')
inlet = mesh.nodes_where(lambda p: np.isclose(p[:, 0], gli['POINT0'][0]))

chem = OGSGEMS(CASE / 'gems' / 'BC-dat.lst', mesh.n_nodes, hydrology='full', min_porosity=1e-4,
               accept=(2, 6), retry=True, warm_start=True, boundary_nodes=inlet)
comps = [f'{i + 1}-{e}' for i, e in enumerate(chem.elements)]
b_init = np.zeros((mesh.n_nodes, chem.nIC))
c_inlet = np.zeros(chem.nIC)
for pcs, var, geo, val in read_constant_blocks(OGS / 'calcite.ic', '#INITIAL_CONDITION'):
    if var in comps:
        b_init[slice(None) if geo == 'DOMAIN' else inlet, comps.index(var)] = val
for pcs, var, geo, val in read_constant_blocks(OGS / 'calcite.bc', '#BOUNDARY_CONDITION'):
    if var in comps:
        c_inlet[comps.index(var)] = val
chem.init_from_bulk(b_init, normalize=False)
chem.c[inlet] = c_inlet

j = int(np.argmax(mesh.points[:, 0]))
display(pd.DataFrame({'b vector, column [mol/m³]': b_init[j], 'pore water c, column [mol/m³ water]': chem.c[j],
                      'inlet c (calcite.bc)': c_inlet}, index=chem.elements).style.format('{:.4g}'))
print(f'porosity {chem.phi[j]:.5f}, pH {chem.pH[j]:.3f}, calcite {chem.amounts("Cal")[j]:.4f} mol/m³')
""")

nb.md(en="""
## Transport and run

The Darcy flux is a constant here, so it is passed to `Transport` as a UFL vector. The element
coefficient is $\\phi_e\\tau D_m$; the dispersion $\\alpha_L|q|$ is added by `Transport` itself.
""", zh="""
## 输运和计算

这里 Darcy 通量是常数，直接以 UFL 向量传给 `Transport`。单元系数是 $\\phi_e\\tau D_m$；弥散 $\\alpha_L|q|$ 由 `Transport` 自己加。
""", de="""
## Transport und Lauf

Der Darcy-Fluss ist hier konstant und wird `Transport` als UFL-Vektor übergeben. Der Elementkoeffizient ist
$\\phi_e\\tau D_m$; die Dispersion $\\alpha_L|q|$ fügt `Transport` selbst hinzu.
""")

nb.code(r"""
q, alpha_L, Dm, tau = 2.9984e-6, 0.0067, 1.0e-10, 1.0
tr = Transport(mesh, fixed_nodes=inlet, q=ufl.as_vector([q]), alpha_L=alpha_L)
tr.fixed_values = c_inlet
x = mesh.points[:, 0]
o = np.argsort(x)
snaps = {}

def prepare(step, t, dt):
    tr.phi_cell = chem.phi[mesh.cells].mean(1)
    tr.De_cell = tr.phi_cell * tau * Dm

def record(step, t, dt):
    if step % 70 == 0:
        snaps[t] = {s: chem.amounts(s)[o].copy() for s in ('Cal', 'Dis-Dol')} | {'pH': chem.pH[o].copy()}

log = run(chem, tr, [100.0] * 210, prepare=prepare, record=record, print_every=0)
print(f'{len(log)} steps in {log.wall_s.iloc[-1]:.1f} s; v t = {q / chem.phi.mean() * 21000:.3f} m')

fig, ax = plt.subplots(1, 3, figsize=(12, 3.2))
for t_, s in snaps.items():
    for a, key in zip(ax, ('Cal', 'Dis-Dol', 'pH')):
        a.plot(x[o], s[key], label=f't = {t_:.0f} s')
for a, title in zip(ax, ('calcite [mol/m³]', 'dolomite [mol/m³]', 'pH')):
    a.set_title(title); a.set_xlabel('x [m]'); a.legend(fontsize=7)
plt.tight_layout(); plt.show()
""")

nb.md(en="""
## Comparison with OGS at t = 21 000 s
""", zh="""
## 和 OGS 比较（t = 21 000 s）
""", de="""
## Vergleich mit OGS bei t = 21 000 s
""")

nb.code(r"""
ref = read_vtk(CASE / 'reference' / 'calcite0210.vtk')
ro = np.argsort(ref['points'][:, 0])
ours = {'pH': chem.pH[o], 'NodePorosity': chem.phi[o], **{cn: chem.c[o, k] for k, cn in enumerate(comps[:6])},
        **{s: chem.amounts(s)[o] for s in ['Cal', 'Dis-Dol', 'Ca+2', 'Mg+2', 'Cl-']}}
refd = {k: ref['node__' + k][ro] for k in ours}
display(error_table(ours, refd).style.hide(axis='index').format({'ref_max': '{:.4g}', 'max_abs_diff': '{:.2e}', 'max_rel_diff': '{:.2e}'}))

fig, ax = plt.subplots(1, 3, figsize=(12, 3.2))
for a, keys in zip(ax, (['Cal', 'Dis-Dol'], ['Ca+2', 'Mg+2', 'Cl-'], ['pH'])):
    for k in keys:
        a.plot(x[o], ours[k], label=f'{k} template')
        a.plot(x[o][::3], refd[k][::3], 'o', ms=3, mfc='none', color=a.lines[-1].get_color(), label=f'{k} OGS')
    a.set_xlabel('x [m]'); a.legend(fontsize=7)
ax[0].set_title('minerals [mol/m³]'); ax[1].set_title('aqueous species [mol/m³]'); ax[2].set_title('pH')
plt.tight_layout(); plt.show()
d = np.abs(ours['Cal'] - refd['Cal'])
print(f'largest calcite difference at x = {x[o][np.argmax(d)]:.3f} m (the dissolution front); '
      f'away from the front it is {np.sort(d)[-3]:.1e} mol/m³')
""")

nb.md(en="""
## Pitfalls found while reproducing this case

1. **Two units for the same element.** `calcite.ic` gives total amounts per m³ of porous medium *including*
   the water and the inert filler (Sn); `calcite.bc` gives concentrations per m³ of fluid *without* the
   solvent water. The inlet node is initialised from the `.ic` values, then its concentration is
   overwritten by the `.bc` values.
2. **The remaining error sits at one node.** The node at the dissolution front is exactly between
   "calcite left" and "calcite gone"; it reacts most to small differences (GEMS version, round-off).
   Calcite and dolomite are 5 % off there and differ by less than 10⁻⁴ mol/m³ elsewhere.
3. **Not modelled:** OGS turns GEMS's excess water into a flow source; here $q$ is constant. The mineral
   amounts are ~0.1 mol/m³, so the volume change is ~10⁻⁶ m³ — negligible. `$MY_SMART_GEMS` (skip nodes that
   hardly change) is not implemented either.
4. **Same numbers as the stand-alone reproduction?** Up to $7\\times10^{-4}$ (dolomite) — GEMS answers a change of
   the input in the 15th digit with a change of about 10⁻⁶ in the solution, so changing the order of sums
   is enough. The error against OGS is the same.
""", zh="""
## 复现时遇到的坑

1. **同一个元素两种单位。** `calcite.ic` 给的是每 m³ 多孔介质的总量，*包括*水和惰性填料（Sn）；`calcite.bc` 给的是每 m³ 流体的浓度，
   *不含*溶剂水。入口节点先用 `.ic` 的值初始化，再用 `.bc` 的值覆盖它的浓度。
2. **剩下的误差在一个节点上。** 溶解前锋上的那个节点正好处在“方解石还有”和“方解石没了”之间，对微小差别（GEMS 版本、舍入）最敏感。
   那里方解石和白云石差 5 %，其它地方差不到 10⁻⁴ mol/m³。
3. **没有模拟的部分：** OGS 把 GEMS 的多余水当作水流源项；这里 $q$ 是常数。矿物量约 0.1 mol/m³，体积变化约 10⁻⁶ m³，可以忽略。
   `$MY_SMART_GEMS`（变化很小的节点跳过）也没实现。
4. **和单独复现的结果一样吗？** 差到 $7\\times10^{-4}$（白云石）——GEMS 对输入第 15 位有效数字的变化会给出约 10⁻⁶ 的解的变化，
   改变求和顺序就够了。和 OGS 的误差不变。
""", de="""
## Stolpersteine bei der Reproduktion

1. **Zwei Einheiten für dasselbe Element.** `calcite.ic` enthält Gesamtmengen pro m³ porösem Medium *einschließlich*
   Wasser und inertem Füllstoff (Sn); `calcite.bc` enthält Konzentrationen pro m³ Fluid *ohne* das Lösungsmittel
   Wasser. Der Zuflussknoten wird mit den `.ic`-Werten initialisiert, danach wird seine Konzentration durch die
   `.bc`-Werte überschrieben.
2. **Der restliche Fehler sitzt an einem Knoten.** Der Knoten an der Lösungsfront liegt genau zwischen „Calcit noch
   da“ und „Calcit weg“; er reagiert am stärksten auf kleine Unterschiede (GEMS-Version, Rundung). Calcit und Dolomit
   weichen dort um 5 % ab, überall sonst um weniger als 10⁻⁴ mol/m³.
3. **Nicht modelliert:** OGS macht aus dem Überschusswasser von GEMS eine Strömungsquelle; hier ist $q$ konstant. Die
   Mineralmengen liegen bei ~0,1 mol/m³, die Volumenänderung bei ~10⁻⁶ m³ — vernachlässigbar. `$MY_SMART_GEMS`
   (kaum veränderte Knoten überspringen) ist ebenfalls nicht umgesetzt.
4. **Dieselben Zahlen wie die eigenständige Reproduktion?** Bis auf $7\\times10^{-4}$ (Dolomit) — GEMS antwortet auf eine
   Änderung der Eingabe in der 15. Stelle mit einer Änderung von etwa 10⁻⁶ in der Lösung; eine andere Summationsreihenfolge
   reicht dafür. Der Fehler gegenüber OGS bleibt gleich.
""")

nb.md(en="""
## Exercises

1. Halve the mesh size (200 elements; build the mesh with `OGSMesh(np.linspace(0, 0.5, 201)[:, None], ...)` and set
   the initial b vectors yourself). Does the front-node error shrink?
2. Switch on FEM-FCT (`Transport(..., fct=True)`). Does anything change, and why (look at the cell Péclet number)?
3. Use `warm_start=False`. Compare run time and results.
""", zh="""
## 练习

1. 网格加密一倍（200 个单元；用 `OGSMesh(np.linspace(0, 0.5, 201)[:, None], ...)` 建网格，自己设初始 b 向量）。前锋节点的误差变小了吗？
2. 打开 FEM-FCT（`Transport(..., fct=True)`）。有变化吗？为什么（看网格 Péclet 数）？
3. 用 `warm_start=False`。比较计算时间和结果。
""", de="""
## Übungen

1. Halbieren Sie die Elementgröße (200 Elemente; Netz mit `OGSMesh(np.linspace(0, 0.5, 201)[:, None], ...)` erzeugen
   und die Anfangs-b-Vektoren selbst setzen). Wird der Fehler am Frontknoten kleiner?
2. Schalten Sie FEM-FCT ein (`Transport(..., fct=True)`). Ändert sich etwas, und warum (Gitter-Péclet-Zahl ansehen)?
3. Verwenden Sie `warm_start=False`. Vergleichen Sie Laufzeit und Ergebnisse.
""")

nb.save('02_calcite')
