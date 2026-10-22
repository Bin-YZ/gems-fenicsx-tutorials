from nb import NB

nb = NB()
nb.md(en=r"""
# 3 · OPC concrete with quartz aggregate: 10 000 years of slow kinetics

**What you learn here**

- long-term chemistry driven by one slow kinetic mineral (the alkali–silica reaction of quartz)
- initial **constraints** on species and the two-pass OGS initialisation
- `hydrology='none'` and a **lumped** mass matrix
- how to compare time series when the reference was written at irregular times

## The problem

A 10 m column of ordinary Portland cement (OPC) concrete with quartz aggregate (OGS5GEMDEV
`LookUp-Table/Case1`, files `bench.*`). Quartz dissolves very slowly (Palandri rate law), its silica reacts
with portlandite and C-S-H, the pH drops from 12.9 to about 10, zeolites form.

The input looks like a leaching problem, but **all boundary conditions are written after `#STOP`** — OGS
never reads them. The column is closed and homogeneous: every node is the same batch reactor, and the
four OGS monitoring nodes give identical results. Transport is still solved (and must not change anything).

$$\frac{dn_\text{Qtz}}{dt} = -A_s\left[10^{-13.99} + 10^{-16.29}\,a_{H^+}^{-0.5}\right](1-\Omega),
\qquad A_s = 4000\ \mathrm{m^{-1}}\times V_\text{Qtz}$$

| quantity | value | OGS file |
|---|---|---|
| column | 10 m, 100 line elements | `bench.msh` |
| pore diffusion | $2\times10^{-10}$ m²/s, lumped mass | `bench.mcp`, `bench.num` |
| initial concrete | total b vector per m³ | `bench.ic` |
| quartz constraint | Qtz ≥ 31 999.95 mol if Al ∈ [160, 180]; Amor-Sl = 0 | `bench.gem` `$CONSTRAINT_GEMS` |
| kinetics | quartz (surface model 1, 4000 m²/m³); amorphous silica with zero surface | `bench.gem` |
| reference | node1/10/50/100.dat, 0 – 919 years | `reference/` |
""", zh=r"""
# 3 · OPC 混凝土 + 石英骨料：1 万年的慢动力学

**这一篇学什么**

- 由一个慢动力学矿物（石英的碱–硅反应）驱动的长期化学
- 物种的初始**约束**和 OGS 两遍初始化
- `hydrology='none'` 和**集中**质量矩阵
- 参考结果输出时刻不规则时，怎样比较时间序列

## 问题

10 m 长的普通硅酸盐水泥（OPC）混凝土柱，骨料是石英（OGS5GEMDEV `LookUp-Table/Case1`，文件 `bench.*`）。
石英按 Palandri 速率很慢地溶解，溶出的硅和 portlandite、C-S-H 反应，pH 从 12.9 降到约 10，生成沸石。

输入看起来像淋滤问题，但**所有边界条件都写在 `#STOP` 之后**——OGS 根本不读。柱子是封闭、均匀的：每个节点都是同样的
批反应器，OGS 的 4 个监测节点结果完全相同。输运照样要算（而且不应改变任何东西）。

$$\frac{dn_\text{Qtz}}{dt} = -A_s\left[10^{-13.99} + 10^{-16.29}\,a_{H^+}^{-0.5}\right](1-\Omega),
\qquad A_s = 4000\ \mathrm{m^{-1}}\times V_\text{Qtz}$$

| 量 | 值 | OGS 文件 |
|---|---|---|
| 柱子 | 10 m，100 个线单元 | `bench.msh` |
| 孔隙扩散 | $2\times10^{-10}$ m²/s，集中质量 | `bench.mcp`、`bench.num` |
| 初始混凝土 | 每 m³ 的总 b 向量 | `bench.ic` |
| 石英约束 | Al ∈ [160, 180] 时 Qtz ≥ 31 999.95 mol；Amor-Sl = 0 | `bench.gem` `$CONSTRAINT_GEMS` |
| 动力学 | 石英（表面积模型 1，4000 m²/m³）；无定形硅表面积为 0 | `bench.gem` |
| 参考 | node1/10/50/100.dat，0 – 919 年 | `reference/` |
""", de=r"""
# 3 · OPC-Beton mit Quarzzuschlag: 10 000 Jahre langsame Kinetik

**Was Sie hier lernen**

- Langzeitchemie, angetrieben von einem langsamen kinetischen Mineral (Alkali-Kieselsäure-Reaktion des Quarzes)
- anfängliche **Nebenbedingungen** für Spezies und die zweistufige OGS-Initialisierung
- `hydrology='none'` und eine **konzentrierte** Massenmatrix
- Vergleich von Zeitreihen, wenn die Referenz zu unregelmäßigen Zeiten geschrieben wurde

## Das Problem

Eine 10 m lange Säule aus Portlandzementbeton (OPC) mit Quarzzuschlag (OGS5GEMDEV `LookUp-Table/Case1`,
Dateien `bench.*`). Quarz löst sich sehr langsam (Ratengesetz nach Palandri), das Silikat reagiert mit
Portlandit und C-S-H, der pH sinkt von 12,9 auf etwa 10, Zeolithe bilden sich.

Die Eingabe sieht wie ein Auslaugungsproblem aus, aber **alle Randbedingungen stehen nach `#STOP`** — OGS liest
sie nie. Die Säule ist geschlossen und homogen: jeder Knoten ist derselbe Batch-Reaktor, und die vier
OGS-Beobachtungsknoten liefern identische Ergebnisse. Der Transport wird trotzdem gelöst (und darf nichts ändern).

$$\frac{dn_\text{Qtz}}{dt} = -A_s\left[10^{-13.99} + 10^{-16.29}\,a_{H^+}^{-0.5}\right](1-\Omega),
\qquad A_s = 4000\ \mathrm{m^{-1}}\times V_\text{Qtz}$$

| Größe | Wert | OGS-Datei |
|---|---|---|
| Säule | 10 m, 100 Linienelemente | `bench.msh` |
| Porendiffusion | $2\times10^{-10}$ m²/s, konzentrierte Masse | `bench.mcp`, `bench.num` |
| Anfangsbeton | b-Gesamtvektor pro m³ | `bench.ic` |
| Quarz-Nebenbedingung | Qtz ≥ 31 999,95 mol falls Al ∈ [160, 180]; Amor-Sl = 0 | `bench.gem` `$CONSTRAINT_GEMS` |
| Kinetik | Quarz (Oberflächenmodell 1, 4000 m²/m³); amorphes SiO₂ mit Oberfläche null | `bench.gem` |
| Referenz | node1/10/50/100.dat, 0 – 919 Jahre | `reference/` |
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
from ogs_io import read_msh, read_constant_blocks
from fe_mesh import OGSMesh
from transport import Transport
from gems_ogs import OGSGEMS, Kinetic
from reactive_transport import run

CASE = ROOT / 'cases' / '3_opc_quartz'
OGS = CASE / 'ogs_input'
YR = 3.156e7                                   # one year as used in the OGS input
plt.rcParams.update({'figure.dpi': 110, 'font.size': 9, 'axes.grid': True, 'grid.alpha': 0.3})
""")

nb.md(en="""
## Initial state: constraints and the two-pass start

`init_from_bulk(normalize=True, ...)` follows OGS: the first GEMS run uses the constrained limits; the
kinetic species (`pin`) are then fixed to the amounts just found, the b vector and the limits are divided
by the system volume so that the node holds 1 m³, and GEMS runs again.
""", zh="""
## 初始状态：约束和两遍启动

`init_from_bulk(normalize=True, ...)` 照 OGS 做：第一遍 GEMS 用约束后的上下限；然后把动力学物种（`pin`）钉在刚算出的量上，
b 向量和上下限除以体系体积，使节点正好是 1 m³，再算一遍 GEMS。
""", de="""
## Anfangszustand: Nebenbedingungen und zweistufiger Start

`init_from_bulk(normalize=True, ...)` folgt OGS: der erste GEMS-Lauf verwendet die beschränkten Schranken; danach
werden die kinetischen Spezies (`pin`) auf die gefundenen Mengen festgelegt, b-Vektor und Schranken durch das
Systemvolumen geteilt, damit der Knoten genau 1 m³ enthält, und GEMS erneut gerechnet.
""")

nb.code(r"""
points, cells, _, _ = read_msh(OGS / 'bench.msh')
mesh = OGSMesh(points[:, :1], cells['line'], 'interval')
x = mesh.points[:, 0]
monitor_x = [0.1, 1.0, 5.0, 10.0]
monitor = [int(np.argmin(np.abs(x - xm))) for xm in monitor_x]

quartz = Kinetic('Qtz', logk=(-13.99, -16.29), n_H=(0.0, -0.5), area_model=1, area=4000.0)
amorph = Kinetic('Amor-Sl', area_model=1, area=0.0)
chem = OGSGEMS(CASE / 'gems' / 'OPC-norm-gas-dat.lst', mesh.n_nodes, hydrology='none', min_porosity=1e-4,
               kinetics=[quartz, amorph], retry=True)
comps = [f'{i + 1}-{e}' for i, e in enumerate(chem.elements)]
b_ic = np.zeros(chem.nIC)
for pcs, var, geo, val in read_constant_blocks(OGS / 'bench.ic', '#INITIAL_CONDITION'):
    if var in comps:
        b_ic[comps.index(var)] = val
lower = np.zeros((mesh.n_nodes, chem.nDC))
upper = np.full((mesh.n_nodes, chem.nDC), 1.0e6)
iQ, iA = chem.species.index('Qtz'), chem.species.index('Amor-Sl')
if 160.0 <= b_ic[chem.elements.index('Al')] <= 180.0:
    lower[:, iQ], upper[:, iQ] = 3.19999541657500e+04, 1.0e6
lower[:, iA] = upper[:, iA] = 0.0
chem.init_from_bulk(b_ic, normalize=True, lower=lower, upper=upper, pin=['Qtz', 'Amor-Sl'])

key_solids = ['Qtz', 'Portlandite', 'ECSH2-JenCa', 'ECSH2-TobCa', 'ECSH2-KSH', 'ECSH2-NaSH', 'ettringite',
              'Cal', 'hydrotalcite', 'Gp', 'Chabazite', 'Scolecite', 'Inert_Qtz']
i = monitor[2]
print(f'{chem.nIC} elements, {chem.nDC} species, {chem.nPH} phases; porosity {chem.phi[i]:.4f}, pH {chem.pH[i]:.3f}, '
      f'quartz rate {chem.dmdt[i, 0] * YR:.2f} mol/m³/yr')
display(pd.Series({s: chem.amounts(s)[i] for s in key_solids}, name='mol per m³ at t = 0').to_frame().T.round(2))
""")

nb.md(en="""
## The 10 000-year run

Lumped mass (`ELE_MASS_LUMPING`), diffusion $\\phi_e\\,D_p$, no boundary conditions, and only the components
marked mobile in `bench.mcp` (all but `Inrt` and `Zz`). Time step 1 year up to 1000 years, then 10 years.
**This cell takes about 18 minutes.**
""", zh="""
## 1 万年的计算

集中质量（`ELE_MASS_LUMPING`）、扩散 $\\phi_e\\,D_p$、没有边界条件，只输运 `bench.mcp` 里标为可动的组分（除 `Inrt` 和 `Zz`）。
时间步前 1000 年 1 年，之后 10 年。**这个单元格大约要算 18 分钟。**
""", de="""
## Der 10 000-Jahre-Lauf

Konzentrierte Masse (`ELE_MASS_LUMPING`), Diffusion $\\phi_e\\,D_p$, keine Randbedingungen und nur die in
`bench.mcp` als mobil markierten Komponenten (alle außer `Inrt` und `Zz`). Zeitschritt 1 Jahr bis 1000 Jahre,
danach 10 Jahre. **Diese Zelle rechnet etwa 18 Minuten.**
""")

nb.code(r"""
steps, t = [], 0.0
while t < 10000 * YR - 1.0:
    steps.append(1.0 * YR if t < 1000 * YR - 1.0 else 10.0 * YR)
    t += steps[-1]
mobile = [k for k, e in enumerate(chem.elements) if e not in ('Inrt', 'Zz')]
tr = Transport(mesh, lumped=True)
history, spread = [], []

def prepare(step, t, dt):
    tr.phi_cell = chem.phi[mesh.cells].mean(1)
    tr.De_cell = tr.phi_cell * 2.0e-10

def record(step, t, dt):
    for xm, i in zip(monitor_x, monitor):
        row = {'time_yr': t / YR, 'x_m': xm, 'porosity': chem.phi[i], 'pH': chem.pH[i],
               'rate_qtz_mol_m3_yr': chem.dmdt[i, 0] * YR}
        row.update({f'c_{e}': chem.c[i, k] for k, e in enumerate(chem.elements)})
        row.update({f'b_{e}': chem.b_fix[i, k] + chem.c[i, k] * chem.phi[i] for k, e in enumerate(chem.elements)})
        row.update({s: chem.amounts(s)[i] for s in key_solids})
        history.append(row)
    spread.append(np.ptp(chem.amounts('Qtz')))

record(0, 0.0, 0.0)
log = run(chem, tr, steps, mobile=mobile, prepare=prepare, record=record, print_every=500)
history = pd.DataFrame(history)
print(f'{len(log)} steps, {log.wall_s.iloc[-1] / 60:.1f} min, failed GEMS nodes {log.failed.sum()}; '
      f'largest spread of quartz along the column: {max(spread):.2e} mol/m³')
""")

nb.md(en="""
## Comparison with OGS at x = 5 m

The OGS reference stops at 919 years (dashed line). Note the logarithmic-linear time axis.
""", zh="""
## 和 OGS 比较（x = 5 m）

OGS 参考只到 919 年（虚线）。注意时间轴是对数–线性混合的。
""", de="""
## Vergleich mit OGS bei x = 5 m

Die OGS-Referenz endet bei 919 Jahren (gestrichelte Linie). Beachten Sie die logarithmisch-lineare Zeitachse.
""")

nb.code(r"""
ref = {}
for xm, name in zip(monitor_x, ['node1', 'node10', 'node50', 'node100']):
    d = pd.read_csv(CASE / 'reference' / f'{name}.dat', sep=r'\s+', skiprows=1)
    d = d.sort_values('time').drop_duplicates('time').reset_index(drop=True).copy()
    d['time_yr'] = d['time'] / YR
    ref[xm] = d
ours, r = history[history.x_m == 5.0], ref[5.0]
panels = [('quartz', [('Qtz', 'Qtz', 'tab:gray')], 'mol/m³'),
          ('portlandite and C-S-H', [('Portlandite', 'Portlandite', 'tab:blue'), ('ECSH2-JenCa', 'ECSH2-JenCa', 'tab:red'),
                                     ('ECSH2-TobCa', 'ECSH2-TobCa', 'tab:green')], 'mol/m³'),
          ('minor phases', [('ettringite', 'ettringite', 'tab:purple'), ('Chabazite', 'Chabazite', 'tab:orange'),
                            ('Scolecite', 'Scolecite', 'tab:brown'), ('Gp', 'Gp', 'tab:pink')], 'mol/m³'),
          ('pH', [('pH', 'pH', 'k')], ''), ('porosity', [('porosity', 'NodePorosity', 'k')], ''),
          ('pore water', [('c_Na', '11-Na', 'tab:orange'), ('c_K', '9-K', 'tab:purple'), ('c_Ca', '4-Ca', 'tab:blue')], 'mol/m³ water')]
fig, axes = plt.subplots(2, 3, figsize=(13, 7))
for ax, (title, series, unit) in zip(axes.flat, panels):
    for ok, rk, col in series:
        ax.plot(ours.time_yr, ours[ok], '-', color=col, label=f'{rk} (template)')
        ax.plot(r.time_yr[::4], r[rk][::4], 'o', ms=3, mfc='none', color=col, label=f'{rk} (OGS)')
    ax.axvline(r.time_yr.max(), color='0.5', ls='--', lw=1)
    ax.set_xscale('symlog', linthresh=10); ax.set_xlim(0, 10000)
    ax.set_title(title); ax.set_xlabel('time [years]'); ax.set_ylabel(unit); ax.legend(fontsize=6, ncol=2)
plt.tight_layout(); plt.show()
""")

nb.md(en="""
The table compares all four monitoring nodes at the 351 OGS output times (our series is interpolated to
them). nRMSE is the RMS error divided by the range of the OGS series.
""", zh="""
下表在 OGS 的 351 个输出时刻比较全部 4 个监测节点（我们的时间序列插值到这些时刻）。nRMSE 是均方根误差除以 OGS 序列的变化幅度。
""", de="""
Die Tabelle vergleicht alle vier Beobachtungsknoten zu den 351 OGS-Ausgabezeiten (unsere Reihe wird darauf
interpoliert). nRMSE ist der RMS-Fehler geteilt durch die Spannweite der OGS-Reihe.
""")

nb.code(r"""
compare = [('Qtz', 'Qtz'), ('Portlandite', 'Portlandite'), ('ECSH2-JenCa', 'ECSH2-JenCa'), ('ECSH2-TobCa', 'ECSH2-TobCa'),
           ('ettringite', 'ettringite'), ('Chabazite', 'Chabazite'), ('Scolecite', 'Scolecite'), ('Gp', 'Gp'),
           ('pH', 'pH'), ('porosity', 'NodePorosity'), ('c_Si', '14-Si'), ('c_Ca', '4-Ca'), ('c_Na', '11-Na'), ('b_Cl', 'Cl')]
rows = []
for ok, rk in compare:
    worst = 0.0
    for xm in monitor_x:
        o_, rr = history[history.x_m == xm], ref[xm]
        a = np.interp(rr.time_yr.values, o_.time_yr.values, o_[ok].values)
        b = rr[rk].values
        if np.ptp(b) > 1e-9:
            worst = max(worst, 100 * np.sqrt(np.mean((a - b) ** 2)) / np.ptp(b))
    rows.append({'quantity': rk, 'OGS at 919 yr': ref[5.0][rk].values[-1],
                 'template at 919 yr': np.interp(ref[5.0].time_yr.values[-1], ours.time_yr, ours[ok]), 'nRMSE %': worst})
display(pd.DataFrame(rows).style.hide(axis='index').format({'OGS at 919 yr': '{:.5g}', 'template at 919 yr': '{:.5g}', 'nRMSE %': '{:.3f}'}))
for name in ['Portlandite', 'ettringite']:
    t_ours = ours.time_yr.values[np.argmax(ours[name].values < 1e-6)]
    t_ogs = r.time_yr.values[np.argmax(r[name].values < 1e-6)]
    print(f'{name} exhausted: template {t_ours:.0f} yr, OGS {t_ogs:.1f} yr (first OGS output with zero)')
""")

nb.md(en="""
## Pitfalls found while reproducing this case

1. **Boundary conditions after `#STOP`.** Reading the input naively suggests a leaching problem. OGS stops
   reading at the first `#STOP`, so the column is closed. Always check what OGS actually reads.
2. **H, O, Cl, Na and K slowly increase in every node.** With `$FLAG_COUPLING_HYDROLOGY 0` the consumed
   water is replaced with pore water of the current composition. This is OGS behaviour, not an error.
3. **Constraints and pinning at the start.** Without the quartz lower bound GEMS dissolves the whole
   aggregate at once; without pinning the kinetic phases after the first pass the second pass does the same.
4. **Warm starts freeze quartz.** With GEMS warm starts quartz stays at its old limit; cold starts every
   time, as OGS (`$FLAG_GEM_USE_SIA 0`).
5. **Time step.** OGS used adaptive steps ≤ 10⁵ s; here 1 year. Portlandite is exhausted after 88 years
   (OGS 88.7) — the remaining difference is probably the time step.
6. **Gas diffusion** (`$FLAG_GAS_DIFFUSION 1`) is not modelled; at this high pH GEMS finds no CO₂ gas.
7. **No reference after 919 years.** The rest of the 10 000 years is a prediction.
""", zh="""
## 复现时遇到的坑

1. **边界条件写在 `#STOP` 之后。** 直接看输入会以为是淋滤问题。OGS 读到第一个 `#STOP` 就停，所以柱子是封闭的。一定要确认 OGS 实际读了什么。
2. **每个节点的 H、O、Cl、Na、K 慢慢增加。** `$FLAG_COUPLING_HYDROLOGY 0` 时，消耗掉的水用当前成分的孔隙水补上。这是 OGS 的行为，不是误差。
3. **初始约束和钉住。** 没有石英下限，GEMS 会一下子把骨料全溶掉；第一遍之后不把动力学相钉住，第二遍也会这样。
4. **热启动会把石英卡住。** GEMS 热启动时石英停在旧上限；每次冷启动，和 OGS 一样（`$FLAG_GEM_USE_SIA 0`）。
5. **时间步。** OGS 用自适应步长 ≤ 10⁵ s；这里用 1 年。Portlandite 在 88 年耗尽（OGS 88.7 年）——剩下的差别大概来自时间步。
6. **气相扩散**（`$FLAG_GAS_DIFFUSION 1`）没做；这么高的 pH 下 GEMS 算不出 CO₂ 气体。
7. **919 年之后没有参考。** 1 万年的其余部分是预测。
""", de="""
## Stolpersteine bei der Reproduktion

1. **Randbedingungen nach `#STOP`.** Naives Lesen der Eingabe legt ein Auslaugungsproblem nahe. OGS hört beim
   ersten `#STOP` auf zu lesen, die Säule ist also geschlossen. Prüfen Sie immer, was OGS tatsächlich liest.
2. **H, O, Cl, Na und K nehmen in jedem Knoten langsam zu.** Mit `$FLAG_COUPLING_HYDROLOGY 0` wird verbrauchtes
   Wasser durch Porenwasser der aktuellen Zusammensetzung ersetzt. Das ist OGS-Verhalten, kein Fehler.
3. **Nebenbedingungen und Festlegen beim Start.** Ohne die untere Quarzschranke löst GEMS den ganzen Zuschlag
   auf einmal; ohne das Festlegen der kinetischen Phasen nach dem ersten Durchlauf tut es der zweite.
4. **Warmstarts frieren Quarz ein.** Mit GEMS-Warmstarts bleibt Quarz an seiner alten Schranke; jedes Mal
   Kaltstart wie OGS (`$FLAG_GEM_USE_SIA 0`).
5. **Zeitschritt.** OGS verwendete adaptive Schritte ≤ 10⁵ s; hier 1 Jahr. Portlandit ist nach 88 Jahren
   aufgebraucht (OGS 88,7) — der Rest der Abweichung stammt vermutlich vom Zeitschritt.
6. **Gasdiffusion** (`$FLAG_GAS_DIFFUSION 1`) wird nicht modelliert; bei diesem hohen pH findet GEMS kein CO₂-Gas.
7. **Keine Referenz nach 919 Jahren.** Der Rest der 10 000 Jahre ist eine Vorhersage.
""")

nb.md(en="""
## Exercises

1. Run 300 years with `dt = 0.1` year and with `dt = 5` years. How much does the time of portlandite
   exhaustion move?
2. Remove the quartz constraint (keep `lower = 0`). What does GEMS do with the aggregate in the first step?
3. Put back the boundary conditions that OGS ignored: fix the concentrations at x = 0 to the values in
   `bench.bc` (`Transport(mesh, fixed_nodes=[...])`, `chem` with `boundary_nodes`). How deep does the leaching
   front get in 1000 years?
""", zh="""
## 练习

1. 用 `dt = 0.1` 年和 `dt = 5` 年各算 300 年。portlandite 耗尽的时刻移动了多少？
2. 去掉石英约束（`lower = 0`）。第一步 GEMS 对骨料做了什么？
3. 把 OGS 忽略掉的边界条件加回来：x = 0 处浓度固定为 `bench.bc` 里的值（`Transport(mesh, fixed_nodes=[...])`，
   `chem` 设 `boundary_nodes`）。1000 年里淋滤前锋推进多深？
""", de="""
## Übungen

1. Rechnen Sie 300 Jahre mit `dt = 0.1` Jahr und mit `dt = 5` Jahren. Wie weit verschiebt sich der Zeitpunkt,
   an dem Portlandit aufgebraucht ist?
2. Entfernen Sie die Quarz-Nebenbedingung (`lower = 0` lassen). Was macht GEMS im ersten Schritt mit dem Zuschlag?
3. Setzen Sie die Randbedingungen wieder ein, die OGS ignoriert hat: Konzentrationen bei x = 0 auf die Werte aus
   `bench.bc` festlegen (`Transport(mesh, fixed_nodes=[...])`, `chem` mit `boundary_nodes`). Wie tief kommt
   die Auslaugungsfront in 1000 Jahren?
""")

nb.save('03_opc_quartz')
