"""Concept pages, three languages. Code listings are pulled from the template with literalinclude."""

T = '../../GEMS_FEniCSx_OGS5_Template'


def code(module, obj):
    return f"""
```{{literalinclude}} {T}/{module}
:language: python
:pyobject: {obj}
```
"""


CONCEPTS = []

# ---------------------------------------------------------------- 1 SNIA
CONCEPTS.append(('01_snia', {
'en': r"""
# Operator splitting (SNIA)

OGS-GEM does not solve transport and chemistry together. Every time step is split into separate
solves, executed once each — the *sequential non-iterative approach* (SNIA):

```{image} ../figures/snia.png
:width: 100%
```

1. **prepare** — the new porosity of every node is turned into element coefficients (porosity,
   diffusion coefficient, permeability) and boundary values for this time.
2. **flow** (if present) — a steady Darcy problem, with the excess water of the last GEMS step as a source.
3. **transport** — every mobile chemical element is advected and dispersed as a passive solute.
4. **chemistry** — GEMS re-equilibrates every node with the transported amounts.

In the template this is `reactive_transport.run`:
""" + code('reactive_transport.py', 'run') + r"""
**Consequences you will meet in the tutorials**

- The splitting error is first order in $\Delta t$. With explicit kinetics this can be large:
  in [HAYEKIT](../tutorials/01_hayekit) OGS's own result is 24 % off the analytical porosity at
  $\Delta t = 100$ s.
- Coefficients lag one step behind: transport in step $n$ uses the porosity from step $n-1$.
- Nothing is iterated, so a node where GEMS fails keeps its old state for the whole step.
""",
'zh': r"""
# 算子分裂（SNIA）

OGS-GEM 不把输运和化学放在一起解。每个时间步拆成几个独立的求解，每个只做一次——
即*顺序非迭代方法*（SNIA）：

```{image} ../figures/snia.png
:width: 100%
```

1. **prepare**——把每个节点的新孔隙率换成单元系数（孔隙率、扩散系数、渗透率），并给出当前时刻的边界值。
2. **flow**（如果有）——稳态 Darcy 问题，上一步 GEMS 的多余水作为源项。
3. **transport**——每个可动化学元素当作被动溶质做对流和弥散。
4. **chemistry**——用输运后的量在每个节点重新做 GEMS 平衡。

模板里对应的是 `reactive_transport.run`：
""" + code('reactive_transport.py', 'run') + r"""
**在教程里会遇到的后果**

- 分裂误差对 $\Delta t$ 是一阶的。动力学是显式的，误差可能很大：在 [HAYEKIT](../tutorials/01_hayekit)
  里，$\Delta t = 100$ s 时 OGS 自己的孔隙率就和解析解差 24 %。
- 系数滞后一步：第 $n$ 步的输运用的是第 $n-1$ 步的孔隙率。
- 不迭代，所以 GEMS 失败的节点整步保持旧状态。
""",
'de': r"""
# Operator-Splitting (SNIA)

OGS-GEM löst Transport und Chemie nicht gemeinsam. Jeder Zeitschritt wird in getrennte Lösungsschritte
aufgeteilt, die jeweils einmal ausgeführt werden — der *sequentielle nicht-iterative Ansatz* (SNIA):

```{image} ../figures/snia.png
:width: 100%
```

1. **prepare** — die neue Porosität jedes Knotens wird in Elementkoeffizienten (Porosität,
   Diffusionskoeffizient, Permeabilität) und Randwerte für diesen Zeitpunkt umgerechnet.
2. **flow** (falls vorhanden) — ein stationäres Darcy-Problem, mit dem Überschusswasser des letzten GEMS-Schritts als Quelle.
3. **transport** — jedes mobile chemische Element wird als passiver Stoff advektiert und dispergiert.
4. **chemistry** — GEMS bringt jeden Knoten mit den transportierten Mengen neu ins Gleichgewicht.

In der Vorlage ist das `reactive_transport.run`:
""" + code('reactive_transport.py', 'run') + r"""
**Folgen, denen Sie in den Tutorials begegnen**

- Der Splitting-Fehler ist von erster Ordnung in $\Delta t$. Mit expliziter Kinetik kann er groß sein:
  in [HAYEKIT](../tutorials/01_hayekit) liegt das OGS-Ergebnis bei $\Delta t = 100$ s 24 % neben der
  analytischen Porosität.
- Koeffizienten hinken einen Schritt hinterher: der Transport in Schritt $n$ verwendet die Porosität aus Schritt $n-1$.
- Es wird nicht iteriert; ein Knoten, an dem GEMS versagt, behält für den ganzen Schritt seinen alten Zustand.
"""}))

# ---------------------------------------------------------------- 2 element totals
CONCEPTS.append(('02_components', {
'en': r"""
# What is transported: element totals of the pore water

GEMS describes a system by the total amounts of its **independent components** — chemical elements plus
charge (`Zz`) — the *b vector*. OGS-GEM transports exactly these totals, but only the part dissolved in
the pore water (`$TRANSPORT_B 1`):

```{image} ../figures/bvector.png
:width: 100%
```

After each GEMS calculation a node's b vector is split into

- `b_fix` — everything in solids (and gas): stays at the node,
- the pore water — solutes **plus the solvent water**: the H and O of H₂O are removed before transport
  and added back afterwards, so the transported concentration of H and O is only the part in solutes.

Why element totals and not species? There are far fewer elements than species (16 vs 157 in
TransLay2d), the totals are conserved by transport, and the solution stays electroneutral without
transporting charge. The price: all species of an element move with the same diffusion coefficient.

The charge `Zz` is never transported and is set to zero before GEMS. Inert components (e.g. `Inrt`, `Sn`)
can be excluded from transport with the `mobile` argument of `run`.
""",
'zh': r"""
# 输运的是什么：孔隙水里的元素总量

GEMS 用**独立组分**——化学元素加电荷（`Zz`）——的总量描述一个体系，即 *b 向量*。OGS-GEM 输运的正是这些总量，
但只输运溶在孔隙水里的那部分（`$TRANSPORT_B 1`）：

```{image} ../figures/bvector.png
:width: 100%
```

每次 GEMS 计算之后，一个节点的 b 向量分成

- `b_fix`——固相（和气相）里的全部量：留在节点上；
- 孔隙水——溶质**加溶剂水**：H₂O 里的 H、O 在输运前扣掉、输运后再加回来，所以输运的 H、O 浓度只是溶质里的那部分。

为什么输运元素总量而不是物种？元素比物种少得多（TransLay2d 里 16 个对 157 个），总量在输运中守恒，
而且不输运电荷溶液也保持电中性。代价是同一元素的所有物种用同一个扩散系数。

电荷 `Zz` 从不输运，进 GEMS 前设为零。惰性组分（例如 `Inrt`、`Sn`）可以用 `run` 的 `mobile` 参数排除在输运之外。
""",
'de': r"""
# Was transportiert wird: Elementsummen des Porenwassers

GEMS beschreibt ein System durch die Gesamtmengen seiner **unabhängigen Komponenten** — chemische Elemente
plus Ladung (`Zz`) — den *b-Vektor*. OGS-GEM transportiert genau diese Summen, aber nur den im Porenwasser
gelösten Anteil (`$TRANSPORT_B 1`):

```{image} ../figures/bvector.png
:width: 100%
```

Nach jeder GEMS-Rechnung wird der b-Vektor eines Knotens aufgeteilt in

- `b_fix` — alles in Feststoffen (und Gas): bleibt am Knoten,
- das Porenwasser — gelöste Stoffe **plus das Lösungsmittel Wasser**: H und O des H₂O werden vor dem
  Transport abgezogen und danach wieder addiert; die transportierte Konzentration von H und O ist also nur
  der Anteil in gelösten Stoffen.

Warum Elementsummen und nicht Spezies? Es gibt viel weniger Elemente als Spezies (16 gegenüber 157 in
TransLay2d), die Summen bleiben beim Transport erhalten, und die Lösung bleibt elektroneutral, ohne Ladung
zu transportieren. Der Preis: alle Spezies eines Elements bewegen sich mit demselben Diffusionskoeffizienten.

Die Ladung `Zz` wird nie transportiert und vor GEMS auf null gesetzt. Inerte Komponenten (z. B. `Inrt`, `Sn`)
können mit dem Argument `mobile` von `run` vom Transport ausgenommen werden.
"""}))

# ---------------------------------------------------------------- 3 coupling rules
_c2m = code('gems_ogs.py', 'OGSGEMS.concentration_to_mass')
_m2c = code('gems_ogs.py', 'OGSGEMS.mass_to_concentration')
CONCEPTS.append(('03_coupling', {
'en': r"""
# Concentration ↔ mass, porosity and initialisation

Transport works with concentrations (mol per m³ of fluid), GEMS with amounts (mol per node). OGS converts
between them with two functions; the template copies them line by line.

## Concentration → mass (before GEMS)
""" + _c2m + r"""
The transported concentration is multiplied by the fluid volume $V_f$ the node had *before* transport,
negative values are replaced by their absolute value, the solvent water is added back, and very small
totals are set to $10^{-16}$ (GEMS cannot handle zeros).

## Mass → concentration (after GEMS)
""" + _m2c + r"""
- **Porosity** is $\phi = 1 - \sum V_\text{solid}$ (OGS `CalcPorosity`; the node volume is 1 m³), clipped to
  `[MIN_POROSITY, MAX_POROSITY]`.
- GEMS returns its own aqueous volume $V_{aq}$, which is never exactly $\phi$. What happens next is the
  `hydrology` option:

| `hydrology` | OGS input | rule |
|---|---|---|
| `'full'` | `$FLAG_COUPLING_HYDROLOGY 1` | the whole aqueous phase is scaled by $\phi/V_{aq}$; $V_f = \phi$; the difference $V_{aq}-\phi$ becomes a flow source |
| `'hayekit'` | `$FLAG_HAYEKIT 1` | only the solvent water is scaled |
| `'none'` | `$FLAG_COUPLING_HYDROLOGY 0` | no scaling; $c = b_{aq}/V_{aq}$ and later $b = b_\text{fix} + c\,\phi$ |

## Initialisation

There are two ways an OGS-GEM run starts:

- **from total b vectors** (`.ic` file) — `init_from_bulk`. OGS runs GEMS, divides the b vector by the
  resulting system volume $V_s$ so that every node holds exactly 1 m³, and runs GEMS again (two passes);
- **from restart files** (`$RELOAD`) — `init_from_restart`. The stored porosity, fluid volume, `b_fix`,
  species amounts and kinetic limits are loaded and GEMS is run once with them. Several benchmarks
  (HAYEKIT, comedy2d, TransLay2d) only make sense from their restart state.
""",
'zh': r"""
# 浓度 ↔ 质量、孔隙率和初始化

输运用浓度（每 m³ 流体的 mol），GEMS 用物质的量（每个节点的 mol）。OGS 用两个函数在二者之间换算；模板逐行照抄。

## 浓度 → 质量（GEMS 之前）
""" + _c2m + r"""
输运后的浓度乘以节点在输运*之前*的流体体积 $V_f$，负值取绝对值，加回溶剂水，很小的总量设成 $10^{-16}$（GEMS 处理不了零）。

## 质量 → 浓度（GEMS 之后）
""" + _m2c + r"""
- **孔隙率** $\phi = 1 - \sum V_\text{固相}$（OGS `CalcPorosity`；节点体积是 1 m³），限制在 `[MIN_POROSITY, MAX_POROSITY]` 之间。
- GEMS 给出自己的水相体积 $V_{aq}$，它从来不正好等于 $\phi$。接下来怎么处理由 `hydrology` 选项决定：

| `hydrology` | OGS 输入 | 规则 |
|---|---|---|
| `'full'` | `$FLAG_COUPLING_HYDROLOGY 1` | 整个水相乘 $\phi/V_{aq}$；$V_f = \phi$；差值 $V_{aq}-\phi$ 作为水流源项 |
| `'hayekit'` | `$FLAG_HAYEKIT 1` | 只缩放溶剂水 |
| `'none'` | `$FLAG_COUPLING_HYDROLOGY 0` | 不缩放；$c = b_{aq}/V_{aq}$，之后 $b = b_\text{fix} + c\,\phi$ |

## 初始化

OGS-GEM 有两种开始方式：

- **从总 b 向量开始**（`.ic` 文件）——`init_from_bulk`。OGS 先算一次 GEMS，把 b 向量除以得到的体系体积 $V_s$，
  让每个节点正好是 1 m³，再算一次（两遍）；
- **从重启文件开始**（`$RELOAD`）——`init_from_restart`。读入保存的孔隙率、流体体积、`b_fix`、物种量和动力学上下限，
  用它们算一次 GEMS。好几个基准（HAYEKIT、comedy2d、TransLay2d）只有从重启状态开始才有意义。
""",
'de': r"""
# Konzentration ↔ Masse, Porosität und Initialisierung

Der Transport arbeitet mit Konzentrationen (mol pro m³ Fluid), GEMS mit Stoffmengen (mol pro Knoten). OGS
rechnet mit zwei Funktionen zwischen beiden um; die Vorlage übernimmt sie Zeile für Zeile.

## Konzentration → Masse (vor GEMS)
""" + _c2m + r"""
Die transportierte Konzentration wird mit dem Fluidvolumen $V_f$ multipliziert, das der Knoten *vor* dem
Transport hatte, negative Werte werden durch ihren Betrag ersetzt, das Lösungsmittel Wasser wird wieder
addiert, und sehr kleine Summen werden auf $10^{-16}$ gesetzt (GEMS kann mit Nullen nicht umgehen).

## Masse → Konzentration (nach GEMS)
""" + _m2c + r"""
- Die **Porosität** ist $\phi = 1 - \sum V_\text{fest}$ (OGS `CalcPorosity`; das Knotenvolumen ist 1 m³),
  begrenzt auf `[MIN_POROSITY, MAX_POROSITY]`.
- GEMS liefert ein eigenes Volumen der wässrigen Phase $V_{aq}$, das nie genau $\phi$ ist. Was dann passiert,
  bestimmt die Option `hydrology`:

| `hydrology` | OGS-Eingabe | Regel |
|---|---|---|
| `'full'` | `$FLAG_COUPLING_HYDROLOGY 1` | die ganze wässrige Phase wird mit $\phi/V_{aq}$ skaliert; $V_f = \phi$; die Differenz $V_{aq}-\phi$ wird zur Strömungsquelle |
| `'hayekit'` | `$FLAG_HAYEKIT 1` | nur das Lösungsmittel Wasser wird skaliert |
| `'none'` | `$FLAG_COUPLING_HYDROLOGY 0` | keine Skalierung; $c = b_{aq}/V_{aq}$ und später $b = b_\text{fix} + c\,\phi$ |

## Initialisierung

Ein OGS-GEM-Lauf kann auf zwei Arten beginnen:

- **aus b-Gesamtvektoren** (`.ic`-Datei) — `init_from_bulk`. OGS rechnet GEMS, teilt den b-Vektor durch das
  resultierende Systemvolumen $V_s$, damit jeder Knoten genau 1 m³ enthält, und rechnet GEMS erneut (zwei Durchläufe);
- **aus Restartdateien** (`$RELOAD`) — `init_from_restart`. Gespeicherte Porosität, Fluidvolumen, `b_fix`,
  Speziesmengen und kinetische Schranken werden geladen und GEMS einmal damit gerechnet. Mehrere Benchmarks
  (HAYEKIT, comedy2d, TransLay2d) ergeben nur ab ihrem Restartzustand Sinn.
"""}))

# ---------------------------------------------------------------- 4 kinetics
_lim = code('gems_ogs.py', 'OGSGEMS.calc_limits')
CONCEPTS.append(('04_kinetics', {
'en': r"""
# Kinetics with an equilibrium solver

GEMS only computes equilibria. OGS-GEM makes a mineral kinetic by giving GEMS a **window**
$[\text{dll}, \text{dul}]$ for its amount: GEMS finds the equilibrium *within* that window.

## Rate

After each GEMS run the rate of every kinetic phase is computed (OGS `CalcReactionRate`):

$$\frac{dm}{dt} = -A_s \sum_m 10^{\log k_m}\, a_{H^+}^{\,n_m}\,(1-\Omega)$$

with the saturation $\Omega$ from GEMS and the reactive surface $A_s$ from one of the surface models
(`Kinetic.area_model`): 1 — $A\,V_\text{mineral}$; 3 — $A\,V_\text{mineral}/\phi$; 4 — $A\,\phi$.

## Moving the window
""" + _lim + r"""
In the next step the window is moved by $\frac{dm}{dt}\,\Delta t$ (OGS `CalcLimits`):

```{image} ../figures/kinetics_window.png
:width: 90%
```

- `limits='loose'` (`$LOOSE_KINETICS 1`): one end of the window stays at the current amount, so GEMS may
  also choose *less* reaction than the rate allows. `'strict'` pins the amount to the kinetic target.
- **Seeding:** an absent phase that is supersaturated gets $10^{-6}$ mol, otherwise it could never start.
- **Sub-steps** (`substep_kinetics`, OGS 2017): if a phase would change an element by more than 10 % in one
  step, the chemistry step is split.

The rate is explicit — computed from the state at the end of the previous step. This is the main source
of time-step dependence (see [HAYEKIT](../tutorials/01_hayekit)).
""",
'zh': r"""
# 用平衡求解器做动力学

GEMS 只算平衡。OGS-GEM 让某个矿物受动力学控制的办法是：给 GEMS 一个它的量的**窗口**
$[\text{dll}, \text{dul}]$，GEMS 在这个窗口*之内*找平衡。

## 速率

每次 GEMS 计算后，每个动力学相的速率（OGS `CalcReactionRate`）：

$$\frac{dm}{dt} = -A_s \sum_m 10^{\log k_m}\, a_{H^+}^{\,n_m}\,(1-\Omega)$$

饱和度 $\Omega$ 来自 GEMS，反应表面积 $A_s$ 由表面积模型给出（`Kinetic.area_model`）：
1——$A\,V_\text{矿物}$；3——$A\,V_\text{矿物}/\phi$；4——$A\,\phi$。

## 移动窗口
""" + _lim + r"""
下一步窗口移动 $\frac{dm}{dt}\,\Delta t$（OGS `CalcLimits`）：

```{image} ../figures/kinetics_window.png
:width: 90%
```

- `limits='loose'`（`$LOOSE_KINETICS 1`）：窗口一端留在当前量，所以 GEMS 也可以选择比速率允许的*更少*的反应。
  `'strict'` 把量钉在动力学目标值上。
- **成核种子：** 不存在但过饱和的相给 $10^{-6}$ mol，否则它永远不会开始生成。
- **子步**（`substep_kinetics`，OGS 2017）：如果一个相一步之内会让某元素变化超过 10 %，就把化学步拆开。

速率是显式的——用上一步结束时的状态算。这是结果依赖时间步的主要原因（见 [HAYEKIT](../tutorials/01_hayekit)）。
""",
'de': r"""
# Kinetik mit einem Gleichgewichtslöser

GEMS berechnet nur Gleichgewichte. OGS-GEM macht ein Mineral kinetisch, indem es GEMS ein **Fenster**
$[\text{dll}, \text{dul}]$ für dessen Menge vorgibt: GEMS sucht das Gleichgewicht *innerhalb* dieses Fensters.

## Rate

Nach jeder GEMS-Rechnung wird die Rate jeder kinetischen Phase berechnet (OGS `CalcReactionRate`):

$$\frac{dm}{dt} = -A_s \sum_m 10^{\log k_m}\, a_{H^+}^{\,n_m}\,(1-\Omega)$$

mit der Sättigung $\Omega$ aus GEMS und der reaktiven Oberfläche $A_s$ aus einem der Oberflächenmodelle
(`Kinetic.area_model`): 1 — $A\,V_\text{Mineral}$; 3 — $A\,V_\text{Mineral}/\phi$; 4 — $A\,\phi$.

## Verschieben des Fensters
""" + _lim + r"""
Im nächsten Schritt wird das Fenster um $\frac{dm}{dt}\,\Delta t$ verschoben (OGS `CalcLimits`):

```{image} ../figures/kinetics_window.png
:width: 90%
```

- `limits='loose'` (`$LOOSE_KINETICS 1`): ein Ende des Fensters bleibt bei der aktuellen Menge, GEMS darf
  also auch *weniger* Reaktion wählen als die Rate erlaubt. `'strict'` legt die Menge auf das kinetische Ziel fest.
- **Keimbildung:** eine nicht vorhandene, übersättigte Phase erhält $10^{-6}$ mol, sonst könnte sie nie entstehen.
- **Teilschritte** (`substep_kinetics`, OGS 2017): würde eine Phase ein Element in einem Schritt um mehr als
  10 % ändern, wird der Chemieschritt unterteilt.

Die Rate ist explizit — aus dem Zustand am Ende des vorigen Schritts. Das ist die Hauptursache der
Zeitschrittabhängigkeit (siehe [HAYEKIT](../tutorials/01_hayekit)).
"""}))

# ---------------------------------------------------------------- 5 transport numerics
CONCEPTS.append(('05_transport', {
'en': r"""
# Transport numerics: element coefficients, mass matrix and FCT

The template uses linear (CG1) finite elements and backward Euler, the same as OGS. Reproducing OGS
node by node needs the same choices in the details:

| detail | OGS rule | template |
|---|---|---|
| element porosity | mean of the node porosities | `element_mean(phi, cells)` |
| element diffusion | harmonic mean of node values (`$DIFFUSION 8/9`) | `harmonic_mean(...)` |
| mass matrix | consistent, or lumped with `ELE_MASS_LUMPING` | `Transport(lumped=...)` |
| dispersion | $\alpha_T|q|I + (\alpha_L-\alpha_T)\,qq^T/|q|$ | `alpha_L`, `alpha_T` |
| quadrature | 3×3 Gauss on quadrilaterals | `quadrature_degree=5` |

## FEM-FCT

With strong advection the Galerkin scheme produces wiggles and negative concentrations; GEMS then gets
negative element amounts. OGS offers flux-corrected transport (`$FEM_FCT 1`, Kuzmin's linearised scheme):
a low-order solution with added discrete diffusion, plus as much of the "anti-diffusive" correction as
the Zalesak limiter allows without creating new extrema.

```{image} ../figures/fct.png
:width: 90%
```

OGS adds the limited flux $+f_{ij}$ to row $j$; the textbook scheme uses $-f_{ij}$ (mass conservative).
`Transport(fct_ogs_sign=True)` copies OGS. In [ConcreteCrack](../tutorials/05_concretecrack) the two
variants cannot be told apart against the OGS reference.
""",
'zh': r"""
# 输运数值方法：单元系数、质量矩阵和 FCT

模板用线性（CG1）有限元和向后 Euler，和 OGS 相同。要和 OGS 逐节点对上，细节上也得做同样的选择：

| 细节 | OGS 规则 | 模板 |
|---|---|---|
| 单元孔隙率 | 节点孔隙率的平均 | `element_mean(phi, cells)` |
| 单元扩散系数 | 节点值的调和平均（`$DIFFUSION 8/9`） | `harmonic_mean(...)` |
| 质量矩阵 | 一致质量；`ELE_MASS_LUMPING` 时集中质量 | `Transport(lumped=...)` |
| 弥散 | $\alpha_T|q|I + (\alpha_L-\alpha_T)\,qq^T/|q|$ | `alpha_L`、`alpha_T` |
| 积分 | 四边形 3×3 Gauss | `quadrature_degree=5` |

## FEM-FCT

对流很强时，Galerkin 格式会产生振荡和负浓度，GEMS 就会拿到负的元素量。OGS 提供通量校正输运
（`$FEM_FCT 1`，Kuzmin 的线性化格式）：先算加了离散扩散的低阶解，再加上 Zalesak 限制器允许的、
不产生新极值的那部分“反扩散”校正。

```{image} ../figures/fct.png
:width: 90%
```

OGS 在第 $j$ 行加的是 $+f_{ij}$；教科书格式是 $-f_{ij}$（质量守恒）。`Transport(fct_ogs_sign=True)` 照抄 OGS。
在 [ConcreteCrack](../tutorials/05_concretecrack) 里，和 OGS 参考相比这两种写法分辨不出来。
""",
'de': r"""
# Transportnumerik: Elementkoeffizienten, Massenmatrix und FCT

Die Vorlage verwendet lineare (CG1) finite Elemente und impliziten Euler, wie OGS. Um OGS Knoten für Knoten
zu reproduzieren, müssen auch die Details gleich gewählt werden:

| Detail | OGS-Regel | Vorlage |
|---|---|---|
| Elementporosität | Mittel der Knotenporositäten | `element_mean(phi, cells)` |
| Elementdiffusion | harmonisches Mittel der Knotenwerte (`$DIFFUSION 8/9`) | `harmonic_mean(...)` |
| Massenmatrix | konsistent, oder konzentriert mit `ELE_MASS_LUMPING` | `Transport(lumped=...)` |
| Dispersion | $\alpha_T|q|I + (\alpha_L-\alpha_T)\,qq^T/|q|$ | `alpha_L`, `alpha_T` |
| Quadratur | 3×3 Gauß auf Vierecken | `quadrature_degree=5` |

## FEM-FCT

Bei starker Advektion erzeugt das Galerkin-Verfahren Oszillationen und negative Konzentrationen; GEMS
erhält dann negative Elementmengen. OGS bietet flusskorrigierten Transport (`$FEM_FCT 1`, linearisiertes
Verfahren nach Kuzmin): eine Lösung niedriger Ordnung mit zusätzlicher diskreter Diffusion, plus so viel
„antidiffusive“ Korrektur, wie der Zalesak-Limiter ohne neue Extrema erlaubt.

```{image} ../figures/fct.png
:width: 90%
```

OGS addiert den begrenzten Fluss $+f_{ij}$ in Zeile $j$; das Lehrbuchverfahren verwendet $-f_{ij}$
(massenerhaltend). `Transport(fct_ogs_sign=True)` übernimmt OGS. In [ConcreteCrack](../tutorials/05_concretecrack)
lassen sich beide Varianten gegenüber der OGS-Referenz nicht unterscheiden.
"""}))

# ---------------------------------------------------------------- 6 flow and water
CONCEPTS.append(('06_flow_water', {
'en': r"""
# Flow, permeability and the excess-water source

For saturated cases OGS-GEM solves a steady groundwater-flow problem every step:

$$-\nabla\cdot(K\nabla h) = Q, \qquad q = -K\nabla h,$$

with $K$ per element. When $K$ depends on porosity (Kozeny–Carman, `$PERMEABILITY_FUNCTION_POROSITY 4`)

$$K = K_0\,\frac{(1-\phi_0)^2}{(1-\phi)^2}\,\frac{\phi^3}{\phi_0^3},$$

the node values are combined with a harmonic mean per element.

## The excess-water source term

With `hydrology='full'` GEMS's aqueous volume is scaled to the porosity. The difference
$V_{aq} - \phi$ is not thrown away: in the next step it is injected into the flow problem as a nodal
source $Q_i = (V_{aq,i} - \phi_i)/\Delta t \cdot V_i$ (OGS `SetSourceSink`):

```{image} ../figures/excess_water.png
:width: 100%
```

Where minerals react this volume change is physical (comedy2d: up to $10^{-5}$ m³/m³ along the
cement strip). Where nothing reacts it is round-off of GEMS ($10^{-10}$–$10^{-7}$). In low-permeability
material even that noise moves the head by centimetres — the head in
[ConcreteCrack](../tutorials/05_concretecrack) can therefore not be reproduced node by node.
""",
'zh': r"""
# 水流、渗透率和多余水源项

对饱和算例，OGS-GEM 每一步解一个稳态地下水流问题：

$$-\nabla\cdot(K\nabla h) = Q, \qquad q = -K\nabla h,$$

$K$ 按单元给。$K$ 依赖孔隙率时（Kozeny–Carman，`$PERMEABILITY_FUNCTION_POROSITY 4`）

$$K = K_0\,\frac{(1-\phi_0)^2}{(1-\phi)^2}\,\frac{\phi^3}{\phi_0^3},$$

节点值在单元内取调和平均。

## 多余水源项

`hydrology='full'` 时，GEMS 的水相体积被缩放到孔隙率。差值 $V_{aq} - \phi$ 不会丢掉：下一步它作为节点源项
$Q_i = (V_{aq,i} - \phi_i)/\Delta t \cdot V_i$ 注入水流问题（OGS `SetSourceSink`）：

```{image} ../figures/excess_water.png
:width: 100%
```

矿物在反应的地方，这个体积变化是物理的（comedy2d：沿水泥带最大 $10^{-5}$ m³/m³）。没有反应的地方，它只是
GEMS 的舍入误差（$10^{-10}$–$10^{-7}$）。在低渗透材料里，连这点噪声也会让水头变化几厘米——所以
[ConcreteCrack](../tutorials/05_concretecrack) 的水头无法逐节点复现。
""",
'de': r"""
# Strömung, Permeabilität und die Überschusswasser-Quelle

Für gesättigte Fälle löst OGS-GEM in jedem Schritt ein stationäres Grundwasserströmungsproblem:

$$-\nabla\cdot(K\nabla h) = Q, \qquad q = -K\nabla h,$$

mit $K$ pro Element. Hängt $K$ von der Porosität ab (Kozeny–Carman, `$PERMEABILITY_FUNCTION_POROSITY 4`)

$$K = K_0\,\frac{(1-\phi_0)^2}{(1-\phi)^2}\,\frac{\phi^3}{\phi_0^3},$$

werden die Knotenwerte pro Element harmonisch gemittelt.

## Die Überschusswasser-Quelle

Mit `hydrology='full'` wird das GEMS-Volumen der wässrigen Phase auf die Porosität skaliert. Die Differenz
$V_{aq} - \phi$ geht nicht verloren: im nächsten Schritt wird sie als Knotenquelle
$Q_i = (V_{aq,i} - \phi_i)/\Delta t \cdot V_i$ in das Strömungsproblem eingespeist (OGS `SetSourceSink`):

```{image} ../figures/excess_water.png
:width: 100%
```

Wo Minerale reagieren, ist diese Volumenänderung physikalisch (comedy2d: bis $10^{-5}$ m³/m³ entlang des
Zementstreifens). Wo nichts reagiert, ist sie Rundungsrauschen von GEMS ($10^{-10}$–$10^{-7}$). In gering
durchlässigem Material verschiebt selbst dieses Rauschen die Druckhöhe um Zentimeter — die Druckhöhe in
[ConcreteCrack](../tutorials/05_concretecrack) lässt sich daher nicht knotengenau reproduzieren.
"""}))
