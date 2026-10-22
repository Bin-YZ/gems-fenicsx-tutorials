from nb import NB

nb = NB()
nb.md(en=r"""
# 1 · HAYEKIT: diffusion, precipitation and porosity feedback

**What you learn here**

- how a reactive-transport step is split into *transport* and *chemistry* (SNIA)
- how a **kinetic** mineral is handled with GEMS: lower / upper limits that move by $r\,\Delta t$
- how porosity changes feed back into diffusion
- why the time step matters even for a "converged" chemical solver

This is the best first case: it is one-dimensional, has no flow, and an **analytical solution**
exists (Hayek, Kosakowski & Churakov, *Water Resour. Res.* 2011, 2012).

## The problem

A 2 mm column. Two dissolved species A and B diffuse in from opposite ends (their boundary values
change with time, taken from the analytical solution) and precipitate as a solid

$$\mathrm{A + B \;\rightleftharpoons\; AB(s)}, \qquad \log K = -6.41 .$$

The precipitate fills the pore space, the porosity $\phi$ drops, and with it the effective diffusion
coefficient $D_e = D_0\,\phi$.

$$\frac{\partial (\phi c_i)}{\partial t} = \nabla\cdot\big(D_0\,\phi\,\nabla c_i\big) - \nu_i\, r ,\qquad
r = A_s\, k\,(1-\Omega),\quad A_s = 10^4\,\phi,\quad k = 10^{-7.69897}\ \mathrm{mol\,m^{-2}\,s^{-1}}$$

| quantity | value | OGS file |
|---|---|---|
| length, mesh | 2 mm, 100 line elements | `ab1d.msh` |
| $D_0$ | $10^{-10}$ m²/s, $D_e = D_0\phi$ (`$DIFFUSION 9`) | `ab1d.mcp` |
| kinetics | rate model 1, surface model 4: $A_s = 10^4\phi$ | `ab1d.gem` |
| time step | 100 s × 100 (OGS) | `ab1d.tim` |
| initial state | OGS restart files at $t=0$ | `ab1d_*_gem.asc` |
| boundary values of A, B | 4 time curves | `ab1d.rfd`, `ab1d.bc` |
""", zh=r"""
# 1 · HAYEKIT：扩散、沉淀与孔隙率反馈

**这一篇学什么**

- 一个反应运移时间步怎样拆成**输运**和**化学**两步（SNIA）
- GEMS 里**动力学**矿物怎么处理：上下限每步移动 $r\,\Delta t$
- 孔隙率变化怎样反过来影响扩散
- 为什么化学求解器“收敛”了，时间步仍然重要

这是最适合入门的算例：一维、没有水流，而且有**解析解**
（Hayek, Kosakowski & Churakov, *Water Resour. Res.* 2011, 2012）。

## 问题

2 mm 的柱子。溶解物 A、B 从两端扩散进来（边界值随时间变化，取自解析解），生成固相

$$\mathrm{A + B \;\rightleftharpoons\; AB(s)}, \qquad \log K = -6.41 .$$

沉淀占据孔隙，孔隙率 $\phi$ 下降，有效扩散系数 $D_e = D_0\,\phi$ 也随之下降。

$$\frac{\partial (\phi c_i)}{\partial t} = \nabla\cdot\big(D_0\,\phi\,\nabla c_i\big) - \nu_i\, r ,\qquad
r = A_s\, k\,(1-\Omega),\quad A_s = 10^4\,\phi,\quad k = 10^{-7.69897}\ \mathrm{mol\,m^{-2}\,s^{-1}}$$

| 量 | 值 | OGS 文件 |
|---|---|---|
| 长度、网格 | 2 mm，100 个线单元 | `ab1d.msh` |
| $D_0$ | $10^{-10}$ m²/s，$D_e = D_0\phi$（`$DIFFUSION 9`） | `ab1d.mcp` |
| 动力学 | 速率模型 1，表面积模型 4：$A_s = 10^4\phi$ | `ab1d.gem` |
| 时间步 | 100 s × 100（OGS） | `ab1d.tim` |
| 初始状态 | OGS 在 $t=0$ 的重启文件 | `ab1d_*_gem.asc` |
| A、B 的边界值 | 4 条时间曲线 | `ab1d.rfd`、`ab1d.bc` |
""", de=r"""
# 1 · HAYEKIT: Diffusion, Fällung und Porositätsrückkopplung

**Was Sie hier lernen**

- wie ein reaktiver Transportschritt in *Transport* und *Chemie* aufgeteilt wird (SNIA)
- wie ein **kinetisch** kontrolliertes Mineral in GEMS behandelt wird: untere/obere Schranken, die sich um $r\,\Delta t$ verschieben
- wie die Porositätsänderung auf die Diffusion zurückwirkt
- warum der Zeitschritt auch bei einem „konvergierten“ Chemielöser wichtig ist

Der beste Einstieg: eindimensional, keine Strömung, und es gibt eine **analytische Lösung**
(Hayek, Kosakowski & Churakov, *Water Resour. Res.* 2011, 2012).

## Das Problem

Eine 2 mm lange Säule. Die gelösten Stoffe A und B diffundieren von beiden Enden hinein
(Randwerte zeitabhängig, aus der analytischen Lösung) und fallen als Feststoff aus

$$\mathrm{A + B \;\rightleftharpoons\; AB(s)}, \qquad \log K = -6.41 .$$

Der Niederschlag füllt den Porenraum, die Porosität $\phi$ sinkt und damit der effektive
Diffusionskoeffizient $D_e = D_0\,\phi$.

$$\frac{\partial (\phi c_i)}{\partial t} = \nabla\cdot\big(D_0\,\phi\,\nabla c_i\big) - \nu_i\, r ,\qquad
r = A_s\, k\,(1-\Omega),\quad A_s = 10^4\,\phi,\quad k = 10^{-7.69897}\ \mathrm{mol\,m^{-2}\,s^{-1}}$$

| Größe | Wert | OGS-Datei |
|---|---|---|
| Länge, Netz | 2 mm, 100 Linienelemente | `ab1d.msh` |
| $D_0$ | $10^{-10}$ m²/s, $D_e = D_0\phi$ (`$DIFFUSION 9`) | `ab1d.mcp` |
| Kinetik | Ratenmodell 1, Oberflächenmodell 4: $A_s = 10^4\phi$ | `ab1d.gem` |
| Zeitschritt | 100 s × 100 (OGS) | `ab1d.tim` |
| Anfangszustand | OGS-Restartdateien bei $t=0$ | `ab1d_*_gem.asc` |
| Randwerte von A, B | 4 Zeitkurven | `ab1d.rfd`, `ab1d.bc` |
""")

nb.md(en="""
## Setup

The notebook only uses the template modules; all case data (OGS input, GEMS files, reference
results) sit in `GEMS_FEniCSx_OGS5_Template/cases/2_hayekit`.
""", zh="""
## 准备

notebook 只用模板里的模块；算例数据（OGS 输入、GEMS 文件、参考结果）都在
`GEMS_FEniCSx_OGS5_Template/cases/2_hayekit`。
""", de="""
## Vorbereitung

Das Notebook verwendet nur die Module der Vorlage; alle Falldaten (OGS-Eingabe, GEMS-Dateien,
Referenzergebnisse) liegen in `GEMS_FEniCSx_OGS5_Template/cases/2_hayekit`.
""")

nb.code(r"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = next(p / 'GEMS_FEniCSx_OGS5_Template' for p in [Path.cwd(), *Path.cwd().parents]
            if (p / 'GEMS_FEniCSx_OGS5_Template').exists())
sys.path.insert(0, str(ROOT))
from ogs_io import read_msh, read_constant_blocks, read_restart, read_primary_values, read_vtk
from fe_mesh import OGSMesh
from transport import Transport
from gems_ogs import OGSGEMS, Kinetic
from ogs_models import harmonic_mean
from reactive_transport import run
from compare import error_table

CASE = ROOT / 'cases' / '2_hayekit'
OGS = CASE / 'ogs_input'
plt.rcParams.update({'figure.dpi': 110, 'font.size': 9, 'axes.grid': True, 'grid.alpha': 0.3})
""")

nb.md(en="""
## Mesh and boundary values

`OGSMesh` builds a dolfinx mesh from the OGS nodes and elements and keeps the maps between OGS node
numbers and FEniCSx degrees of freedom. **All state arrays of the template are in OGS node order.**

At both ends A and B are prescribed as functions of time (four curves in `ab1d.rfd`); H, O and the
inert component are constants from `ab1d.bc`.
""", zh="""
## 网格和边界值

`OGSMesh` 用 OGS 的节点和单元建 dolfinx 网格，并保存 OGS 节点编号和 FEniCSx 自由度之间的映射。
**模板里所有状态数组都按 OGS 节点编号。**

两端 A、B 的值随时间变化（`ab1d.rfd` 里 4 条曲线）；H、O 和惰性组分取 `ab1d.bc` 的常数。
""", de="""
## Netz und Randwerte

`OGSMesh` erzeugt aus den OGS-Knoten und -Elementen ein dolfinx-Netz und speichert die Zuordnung
zwischen OGS-Knotennummern und FEniCSx-Freiheitsgraden. **Alle Zustandsarrays der Vorlage sind in OGS-Knotenreihenfolge.**

An beiden Enden sind A und B als Funktionen der Zeit vorgegeben (vier Kurven in `ab1d.rfd`); H, O und
die inerte Komponente sind Konstanten aus `ab1d.bc`.
""")

nb.code(r"""
points, cells, _, _ = read_msh(OGS / 'ab1d.msh')
mesh = OGSMesh(points[:, :1], cells['line'], 'interval')
x = mesh.points[:, 0]
left, right = int(np.argmin(x)), int(np.argmax(x))

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

t = np.linspace(0, 1e4, 200)
fig, ax = plt.subplots(figsize=(6, 3))
for k, (lab, ls) in enumerate([('A, x = 0', '-'), ('B, x = 0', '--'), ('A, x = 2 mm', '-'), ('B, x = 2 mm', '--')]):
    ax.plot(t, np.interp(t, *curves[k].T), ls, color='C0' if k < 2 else 'C3', label=lab)
ax.set_xlabel('time [s]'); ax.set_ylabel('mol / m³ pore water'); ax.set_title('Boundary values (ab1d.rfd)')
ax.legend(fontsize=8); plt.show()
print(f'{mesh.n_nodes} nodes, h = {x[1] - x[0]:.1e} m')
""")

nb.md(en="""
## Chemistry: starting from the OGS restart state

The benchmark starts from OGS restart files: for every node the porosity, the fluid volume, the
element amounts in the solids (`b_fix`), the species amounts and their **kinetic limits** `dll`/`dul`.
`init_from_restart` loads them and runs GEMS once at every interior node.

Two OGS options matter here:

- `hydrology='hayekit'` (`$FLAG_HAYEKIT 1`): after GEMS only the solvent water is scaled to the pore
  volume, the solutes are not;
- `Kinetic('AB(s)', area_model=4, area=1e4)`: surface area $A_s = 10^4\\,\\phi$.

The two end nodes are Dirichlet nodes and are not reacted (OGS default `$CALCULATE_BOUNDARY_NODES 0`).
""", zh="""
## 化学：从 OGS 重启状态开始

这个基准从 OGS 重启文件开始：每个节点的孔隙率、流体体积、固相里的元素量（`b_fix`）、物种量和它们的
**动力学上下限** `dll`/`dul`。`init_from_restart` 读入这些，并在每个内部节点算一次 GEMS。

这里有两个 OGS 选项要注意：

- `hydrology='hayekit'`（`$FLAG_HAYEKIT 1`）：GEMS 之后只把溶剂水缩放到孔隙体积，溶质不缩放；
- `Kinetic('AB(s)', area_model=4, area=1e4)`：表面积 $A_s = 10^4\\,\\phi$。

两端节点是 Dirichlet 节点，不算化学（OGS 默认 `$CALCULATE_BOUNDARY_NODES 0`）。
""", de="""
## Chemie: Start aus dem OGS-Restartzustand

Der Benchmark startet aus OGS-Restartdateien: für jeden Knoten Porosität, Fluidvolumen, die
Elementmengen in den Feststoffen (`b_fix`), die Speziesmengen und ihre **kinetischen Schranken** `dll`/`dul`.
`init_from_restart` liest sie ein und rechnet GEMS einmal an jedem inneren Knoten.

Zwei OGS-Optionen sind hier wichtig:

- `hydrology='hayekit'` (`$FLAG_HAYEKIT 1`): nach GEMS wird nur das Lösungsmittel Wasser auf das
  Porenvolumen skaliert, die gelösten Stoffe nicht;
- `Kinetic('AB(s)', area_model=4, area=1e4)`: Oberfläche $A_s = 10^4\\,\\phi$.

Die beiden Endknoten sind Dirichlet-Knoten und werden nicht reagiert (OGS-Vorgabe `$CALCULATE_BOUNDARY_NODES 0`).
""")

nb.code(r"""
def make_chemistry():
    chem = OGSGEMS(CASE / 'gems' / 'TestSolub-dat.lst', mesh.n_nodes, hydrology='hayekit', min_porosity=1e-15,
                   kinetics=[Kinetic('AB(s)', logk=(-7.69897,), area_model=4, area=1.0e4)],
                   boundary_nodes=[left, right])
    restart = read_restart(OGS / 'ab1d', mesh.n_nodes, chem.nIC, chem.nDC)
    c0 = read_primary_values(OGS / 'ab1d', 'MASS_TRANSPORT', comps)
    chem.init_from_restart(restart, c0, nodes=np.flatnonzero(~chem.boundary), update_porosity=True)
    return chem

chem = make_chemistry()
print('elements:', chem.elements)
print('species :', chem.species)
o = np.argsort(x)
fig, ax = plt.subplots(1, 2, figsize=(9, 3))
ax[0].semilogy(x[o] * 1e3, chem.phi[o]); ax[0].set_title('initial porosity (inert mineral I(s))')
ax[1].plot(x[o] * 1e3, chem.c[o, 0], label='A'); ax[1].plot(x[o] * 1e3, chem.c[o, 1], label='B')
ax[1].set_title('initial concentration [mol/m³]'); ax[1].legend()
for a in ax: a.set_xlabel('x [mm]')
plt.tight_layout(); plt.show()
""")

nb.md(en="""
## Transport and the time loop

`Transport` solves $\\phi\\,\\partial_t c - \\nabla\\cdot(D_e\\nabla c) = 0$ with linear elements and
backward Euler. Before every step the `prepare` callback updates the element coefficients from the
current node porosity, exactly as OGS does:

- element porosity = mean of its node porosities;
- element $D_e$ = **harmonic** mean of the node values $D_0\\,\\phi_i$.

`run` then performs, for every time step: transport of all components → GEMS at every interior node
(concentration → mass, kinetic limits, equilibrium, porosity, rate, mass → concentration).
""", zh="""
## 输运和时间循环

`Transport` 用线性单元和向后 Euler 解 $\\phi\\,\\partial_t c - \\nabla\\cdot(D_e\\nabla c) = 0$。
每一步之前 `prepare` 回调根据当前节点孔隙率更新单元系数，和 OGS 完全一样：

- 单元孔隙率 = 节点孔隙率的平均；
- 单元 $D_e$ = 节点值 $D_0\\,\\phi_i$ 的**调和**平均。

然后 `run` 对每个时间步：输运所有组分 → 每个内部节点算 GEMS
（浓度 → 质量、动力学上下限、平衡、孔隙率、速率、质量 → 浓度）。
""", de="""
## Transport und Zeitschleife

`Transport` löst $\\phi\\,\\partial_t c - \\nabla\\cdot(D_e\\nabla c) = 0$ mit linearen Elementen und
implizitem Euler. Vor jedem Schritt aktualisiert der Callback `prepare` die Elementkoeffizienten aus der
aktuellen Knotenporosität, genau wie OGS:

- Elementporosität = Mittelwert der Knotenporositäten;
- Element-$D_e$ = **harmonisches** Mittel der Knotenwerte $D_0\\,\\phi_i$.

`run` führt dann in jedem Zeitschritt aus: Transport aller Komponenten → GEMS an jedem inneren Knoten
(Konzentration → Masse, kinetische Schranken, Gleichgewicht, Porosität, Rate, Masse → Konzentration).
""")

nb.code(r"""
D0 = 1.0e-10
t_end = 1.0e4

def simulate(dt):
    chem = make_chemistry()
    tr = Transport(mesh, fixed_nodes=[left, right])
    snaps = {}

    def prepare(step, t, dt):
        tr.phi_cell = chem.phi[mesh.cells].mean(1)
        tr.De_cell = harmonic_mean(D0 * chem.phi, mesh.cells)
        tr.fixed_values = boundary_values(t)

    def record(step, t, dt):
        if abs(t - 1000.0) < 1e-9 or abs(t - t_end) < 1e-9:
            snaps[t] = dict(A=chem.c[:, 0].copy(), B=chem.c[:, 1].copy(), phi=chem.phi.copy(),
                            AB=chem.amounts('AB(s)').copy())

    log = run(chem, tr, [dt] * int(round(t_end / dt)), prepare=prepare, record=record, print_every=0)
    print(f'dt = {dt:5g} s: {len(log)} steps in {log.wall_s.iloc[-1]:.1f} s, failed GEMS nodes: {log.failed.sum()}')
    return snaps

runs = {dt: simulate(dt) for dt in (100.0, 10.0, 1.0)}
""")

nb.md(en="""
## Comparison with OGS (same time step, 100 s)

With the OGS time step the result agrees with the OGS output to a few $10^{-5}$ (porosity $3\\times10^{-4}$).
""", zh="""
## 和 OGS 比较（同样的时间步 100 s）

用 OGS 的时间步，结果和 OGS 输出一致到几个 $10^{-5}$（孔隙率 $3\\times10^{-4}$）。
""", de="""
## Vergleich mit OGS (gleicher Zeitschritt, 100 s)

Mit dem OGS-Zeitschritt stimmt das Ergebnis mit der OGS-Ausgabe auf einige $10^{-5}$ überein (Porosität $3\\times10^{-4}$).
""")

nb.code(r"""
ogs = read_vtk(CASE / 'reference' / 'ab1d0100.vtk')
ro = np.argsort(ogs['points'][:, 0])
sel = o[1:-1]
r = runs[100.0][t_end]
table = error_table({'A': r['A'][sel], 'B': r['B'][sel], 'AB(s)': r['AB'][sel], 'porosity': r['phi'][sel]},
                    {'A': ogs['node__1-Ael'][ro][1:-1], 'B': ogs['node__2-Bel'][ro][1:-1],
                     'AB(s)': ogs['node__AB(s)'][ro][1:-1], 'porosity': ogs['node__NodePorosity'][ro][1:-1]})
display(table.style.hide(axis='index').format({'ref_max': '{:.3g}', 'max_abs_diff': '{:.2e}', 'max_rel_diff': '{:.2e}'}))
""")

nb.md(en="""
## Comparison with the analytical solution — the time step matters

OGS itself is **24 % off** the analytical porosity at $t = 10^4$ s. The reason is the explicit
kinetics: in each step the precipitation rate is computed from the *old* $\\Omega$ and $\\phi$.
Reducing the time step converges to first order (100 s → 10 s → 1 s).
""", zh="""
## 和解析解比较——时间步很关键

在 $t = 10^4$ s，OGS 自己的孔隙率就和解析解**差 24 %**。原因是动力学是显式的：每步的沉淀速率用的是
*上一步*的 $\\Omega$ 和 $\\phi$。时间步缩小（100 s → 10 s → 1 s）按一阶收敛。
""", de="""
## Vergleich mit der analytischen Lösung — der Zeitschritt zählt

OGS selbst liegt bei $t = 10^4$ s **24 % neben** der analytischen Porosität. Grund ist die explizite
Kinetik: in jedem Schritt wird die Fällungsrate aus dem *alten* $\\Omega$ und $\\phi$ berechnet.
Kleinere Zeitschritte (100 s → 10 s → 1 s) konvergieren mit erster Ordnung.
""")

nb.code(r"""
tab = np.load(CASE / 'reference' / 'hayekit_tables.npz')
xa = tab['analytical10ks__x'] * 1e3
colors = {100.0: 'C3', 10.0: 'C1', 1.0: 'C0'}
fig, axes = plt.subplots(2, 2, figsize=(10, 6.5))
for row, (tt, key) in enumerate([(1000.0, 'analytical1000s'), (t_end, 'analytical10ks')]):
    ax = axes[row, 0]
    ax.plot(xa, tab[key + '__C1x0'], 'k-', lw=4, alpha=0.25, label='A analytical')
    ax.plot(xa, tab[key + '__C2x0'], 'k--', lw=4, alpha=0.25, label='B analytical')
    for dt, s in runs.items():
        ax.plot(x[o] * 1e3, s[tt]['A'][o], '-', color=colors[dt], lw=1, label=f'A, dt = {dt:g} s')
        ax.plot(x[o] * 1e3, s[tt]['B'][o], '--', color=colors[dt], lw=1)
    ax.set_title(f'A and B, t = {tt:.0f} s'); ax.set_ylabel('mol / m³')
    ax = axes[row, 1]
    ax.semilogy(xa, tab[key + '__Porox0'], 'k-', lw=4, alpha=0.25, label='analytical')
    for dt, s in runs.items():
        ax.semilogy(x[o] * 1e3, s[tt]['phi'][o], color=colors[dt], lw=1, label=f'dt = {dt:g} s')
    if tt == t_end:
        ax.semilogy(ogs['points'][ro, 0][::4] * 1e3, ogs['node__NodePorosity'][ro][::4], 'ko', ms=3, mfc='none', label='OGS')
    ax.set_title(f'porosity, t = {tt:.0f} s')
for a in axes.flat:
    a.set_xlabel('x [mm]'); a.legend(fontsize=7)
plt.tight_layout(); plt.show()

rows = []
for tt, key in [(1000.0, 'analytical1000s'), (t_end, 'analytical10ks')]:
    for dt, s in runs.items():
        ana = tab[key + '__Porox0'][1:-1]
        rows.append({'time': f't = {tt:g} s', 'dt': f'dt = {dt:g} s', 'err': np.max(np.abs(s[tt]['phi'][sel] - ana) / ana)})
err = pd.DataFrame(rows).pivot(index='time', columns='dt', values='err')[[f'dt = {d:g} s' for d in runs]]
err.columns.name, err.index.name = 'max. relative error of porosity', None
display(err.style.format('{:.1%}'))
""")

nb.md(en="""
## Pitfalls found while reproducing this case

1. **A misspelled keyword.** `ab1d.gem` contains `$FLAG_CALCULATE_BOUNDARY_NODE`, but OGS reads
   `$CALCULATE_BOUNDARY_NODES`. The typo is ignored, so the boundary nodes are *not* reacted. The OGS
   output confirms it: the porosity at both ends never changes.
2. **Only the water is scaled** (`$FLAG_HAYEKIT`). Scaling the whole aqueous phase, as in the other
   cases, gives a clearly different result.
3. **Surface area model 4** ($A_s = 10^4\\phi$) — not model 1 (specific area × mineral volume).
4. **Harmonic mean of $D_e$, arithmetic mean of $\\phi$, consistent mass matrix.** Changing any of
   them moves the difference to OGS from $10^{-5}$ to above $10^{-3}$.
5. **Seeding.** An absent but supersaturated phase gets 1e-6 mol; without it AB(s) would never start
   to grow from zero.
6. **Cold start every time.** With GEMS warm starts the kinetic phase sometimes stays stuck at its old
   limits.
7. **Open question:** for $\\Delta t \\to 0$ the porosity still differs by about 3 % from the analytical
   solution (spatial resolution? non-reacting boundary nodes? assumptions of the analytical solution?).
""", zh="""
## 复现时遇到的坑

1. **关键字拼错。** `ab1d.gem` 写的是 `$FLAG_CALCULATE_BOUNDARY_NODE`，OGS 识别的是
   `$CALCULATE_BOUNDARY_NODES`。拼错的关键字被忽略，所以边界节点**不**算化学。OGS 输出可以证实：两端孔隙率始终不变。
2. **只缩放水**（`$FLAG_HAYEKIT`）。像其它算例那样缩放整个水相，结果明显不同。
3. **表面积模型 4**（$A_s = 10^4\\phi$），不是模型 1（比表面积 × 矿物体积）。
4. **$D_e$ 调和平均、$\\phi$ 算术平均、一致质量矩阵。** 换掉任何一个，和 OGS 的差就从 $10^{-5}$ 升到 $10^{-3}$ 以上。
5. **成核种子。** 不存在但过饱和的相给 1e-6 mol；没有它 AB(s) 永远不会从零开始长。
6. **每次冷启动。** GEMS 热启动时动力学相有时卡在旧的上下限不动。
7. **没解决的问题：** $\\Delta t \\to 0$ 时孔隙率和解析解仍差约 3 %（空间分辨率？边界节点不反应？解析解的假设？）。
""", de="""
## Stolpersteine bei der Reproduktion

1. **Ein falsch geschriebenes Schlüsselwort.** `ab1d.gem` enthält `$FLAG_CALCULATE_BOUNDARY_NODE`, OGS liest aber
   `$CALCULATE_BOUNDARY_NODES`. Der Tippfehler wird ignoriert, die Randknoten werden also *nicht* reagiert.
   Die OGS-Ausgabe bestätigt das: die Porosität an beiden Enden ändert sich nie.
2. **Nur das Wasser wird skaliert** (`$FLAG_HAYEKIT`). Skaliert man die ganze wässrige Phase wie in den
   anderen Fällen, ergibt sich ein deutlich anderes Ergebnis.
3. **Oberflächenmodell 4** ($A_s = 10^4\\phi$) — nicht Modell 1 (spezifische Oberfläche × Mineralvolumen).
4. **Harmonisches Mittel von $D_e$, arithmetisches Mittel von $\\phi$, konsistente Massenmatrix.** Ändert man
   eines davon, steigt die Abweichung zu OGS von $10^{-5}$ auf über $10^{-3}$.
5. **Keimbildung.** Eine nicht vorhandene, aber übersättigte Phase erhält 1e-6 mol; ohne das würde AB(s) nie
   aus null zu wachsen beginnen.
6. **Jedes Mal Kaltstart.** Mit GEMS-Warmstarts bleibt die kinetische Phase manchmal an ihren alten Schranken hängen.
7. **Offene Frage:** für $\\Delta t \\to 0$ weicht die Porosität noch um etwa 3 % von der analytischen Lösung ab
   (räumliche Auflösung? nicht reagierende Randknoten? Annahmen der analytischen Lösung?).
""")

nb.md(en="""
## Exercises

1. Run with `dt = 30` s and `dt = 3` s and plot the porosity error at $t=10^4$ s against $\\Delta t$
   on log axes. Is the convergence first order?
2. Let the boundary nodes react: create the chemistry with `boundary_nodes=[]` (keep the Dirichlet
   transport nodes). How do the end porosities and the 3 % limit change?
3. Replace the harmonic mean of $D_e$ by the arithmetic mean (`element_mean`). Where in the column does
   the result change most, and why there?
""", zh="""
## 练习

1. 用 `dt = 30` s 和 `dt = 3` s 再算，把 $t=10^4$ s 的孔隙率误差对 $\\Delta t$ 画在对数坐标上。是一阶收敛吗？
2. 让边界节点也反应：建化学对象时用 `boundary_nodes=[]`（输运的 Dirichlet 节点保持不变）。两端孔隙率和 3 % 的极限误差怎么变？
3. 把 $D_e$ 的调和平均换成算术平均（`element_mean`）。柱子哪里变化最大？为什么是那里？
""", de="""
## Übungen

1. Rechnen Sie mit `dt = 30` s und `dt = 3` s und tragen Sie den Porositätsfehler bei $t=10^4$ s doppelt-logarithmisch
   über $\\Delta t$ auf. Ist die Konvergenz von erster Ordnung?
2. Lassen Sie die Randknoten reagieren: Chemie mit `boundary_nodes=[]` erzeugen (die Dirichlet-Knoten des
   Transports bleiben). Wie ändern sich die Porositäten an den Enden und die 3-%-Grenze?
3. Ersetzen Sie das harmonische Mittel von $D_e$ durch das arithmetische (`element_mean`). Wo in der Säule
   ändert sich das Ergebnis am stärksten, und warum gerade dort?
""")

nb.save('01_hayekit')
