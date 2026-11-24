"""New front matter and conclusions of the five verification notebooks (en/zh/de).

Applied by tools/restructure_verification.py: the part of the first markdown cell before the
"problem" heading is replaced by HEAD, the exercise cell is removed, the pitfalls heading is renamed,
a few cells get corrected text (FIX), and CONCL is appended as the last cell.
The notebooks are not re-executed; their code and outputs stay as they are.
"""

PITFALLS = {
    'en': ('## Pitfalls found while reproducing this case', '## Implementation notes: pitfalls found while reproducing'),
    'zh': ('## 复现时遇到的坑', '## 实现备注：复现时遇到的坑'),
    'de': ('## Stolpersteine bei der Reproduktion', '## Implementierungshinweise: Stolpersteine bei der Reproduktion'),
}
PROBLEM = {'en': '## The problem', 'zh': '## 问题', 'de': '## Das Problem'}
EXERCISES = {'en': '## Exercises', 'zh': '## 练习', 'de': '## Übungen'}

HEAD, CONCL, FIX = {}, {}, {}

# ---------------------------------------------------------------- V1 HAYEKIT
HEAD['01_hayekit'] = {
'en': r"""# V1 · HAYEKIT: diffusion, precipitation and porosity feedback

| | |
|---|---|
| **What is tested** | Kinetic precipitation of a mineral from two counter-diffusing solutes, with porosity and diffusivity feedback, using the OGS-GEM coupling rules (kinetic limits, restart initialisation, `hayekit` water scaling). |
| **References** | (1) OGS5GEMDEV output `ab1d0100.vtk`: same mesh, same time step (100 s), t = 10 000 s. (2) The analytical solution of Hayek, Kosakowski & Churakov (2011) at t = 1000 s and 10 000 s. |
| **Compared variables** | A, B (mol/m³ water), AB(s) and porosity at all 101 nodes. Error = max\|template − reference\| / max\|reference\|. |
| **Result** | Against OGS: ≤ 3·10⁻⁵ for A, B and AB(s), 3·10⁻⁴ for porosity. Against the analytical solution (porosity at 10 000 s): 24 % with dt = 100 s (OGS has the same error), 0.3 % with 10 s, 2.7 % with 1 s. |
| **Conclusion** | The template reproduces OGS for this case. Neither code converges cleanly to the analytical solution as dt → 0; a difference of a few percent remains unexplained. |
| **Code and run** | `GEMS_FEniCSx_OGS5_Template/cases/2_hayekit`: `python run_case.py` (or `Run.cmd`). This is the OGS template, not the `case.yaml` code of the tutorials. |

""",
'zh': r"""# V1 · HAYEKIT：扩散、沉淀与孔隙率反馈

| | |
|---|---|
| **检验什么** | 两种相向扩散的溶质按动力学速率沉淀为矿物，并带孔隙率和扩散系数反馈；使用 OGS-GEM 的耦合规则（动力学上下限、重启初始化、`hayekit` 水量缩放）。 |
| **参考** | (1) OGS5GEMDEV 的输出 `ab1d0100.vtk`：相同网格、相同时间步（100 s），t = 10 000 s。(2) Hayek、Kosakowski 和 Churakov（2011）的解析解，t = 1000 s 和 10 000 s。 |
| **比较的量** | 全部 101 个节点上的 A、B（mol/m³ 水）、AB(s) 和孔隙率。误差 = max\|模板 − 参考\| / max\|参考\|。 |
| **结果** | 与 OGS 比：A、B、AB(s) ≤ 3·10⁻⁵，孔隙率 3·10⁻⁴。与解析解比（10 000 s 时的孔隙率）：dt = 100 s 时差 24 %（OGS 也一样），10 s 时 0.3 %，1 s 时 2.7 %。 |
| **结论** | 在这个算例中模板复现了 OGS。dt → 0 时两个代码都没有干净地收敛到解析解，还剩几个百分点的差异没有得到解释。 |
| **代码与运行** | `GEMS_FEniCSx_OGS5_Template/cases/2_hayekit`：`python run_case.py`（或 `Run.cmd`）。这是 OGS 模板，不是教程里的 `case.yaml` 代码。 |

""",
'de': r"""# V1 · HAYEKIT: Diffusion, Fällung und Porositätsrückkopplung

| | |
|---|---|
| **Was geprüft wird** | Kinetische Fällung eines Minerals aus zwei gegeneinander diffundierenden gelösten Stoffen, mit Rückkopplung von Porosität und Diffusivität, nach den Kopplungsregeln von OGS-GEM (kinetische Grenzen, Restart-Initialisierung, `hayekit`-Wasserskalierung). |
| **Referenzen** | (1) OGS5GEMDEV-Ausgabe `ab1d0100.vtk`: gleiches Netz, gleicher Zeitschritt (100 s), t = 10 000 s. (2) Die analytische Lösung von Hayek, Kosakowski & Churakov (2011) bei t = 1000 s und 10 000 s. |
| **Verglichene Größen** | A, B (mol/m³ Wasser), AB(s) und Porosität an allen 101 Knoten. Fehler = max\|Vorlage − Referenz\| / max\|Referenz\|. |
| **Ergebnis** | Gegenüber OGS: ≤ 3·10⁻⁵ für A, B und AB(s), 3·10⁻⁴ für die Porosität. Gegenüber der analytischen Lösung (Porosität bei 10 000 s): 24 % mit dt = 100 s (OGS hat denselben Fehler), 0,3 % mit 10 s, 2,7 % mit 1 s. |
| **Schluss** | Die Vorlage reproduziert OGS in diesem Fall. Keiner der beiden Codes konvergiert für dt → 0 sauber gegen die analytische Lösung; eine Abweichung von einigen Prozent bleibt ungeklärt. |
| **Code und Lauf** | `GEMS_FEniCSx_OGS5_Template/cases/2_hayekit`: `python run_case.py` (oder `Run.cmd`). Das ist die OGS-Vorlage, nicht der `case.yaml`-Code der Tutorials. |

""",
}
FIX['01_hayekit'] = {
'en': (r"## Comparison with the analytical solution — the time step matters", r"""## Comparison with the analytical solution — the time step matters

With the OGS time step (100 s), OGS and the template are both 24 % off the analytical porosity at $t = 10^4$ s. A likely reason
is the explicit treatment of the kinetics: the precipitation rate of each step is computed from the *previous* $\Omega$ and $\phi$.
With 10 s the error drops to 0.3 %, but with 1 s it rises again to 2.7 %. The result therefore does not converge cleanly as
$\Delta t \to 0$, and the remaining difference of a few percent is not explained (see the conclusions)."""),
'zh': (r"## 和解析解比较——时间步很关键", r"""## 和解析解比较——时间步很关键

用 OGS 的时间步（100 s）时，OGS 和模板在 $t = 10^4$ s 的孔隙率都与解析解差 24 %。一个可能的原因是动力学按显式处理：每一步的沉淀速率用的是 *上一步* 的 $\Omega$ 和 $\phi$。时间步取 10 s 时误差降到 0.3 %，但取 1 s 时又升到 2.7 %。因此 $\Delta t \to 0$ 时结果没有干净地收敛，剩下几个百分点的差异没有得到解释（见结论）。"""),
'de': (r"## Vergleich mit der analytischen Lösung — der Zeitschritt zählt", r"""## Vergleich mit der analytischen Lösung — der Zeitschritt zählt

Mit dem OGS-Zeitschritt (100 s) liegen OGS und die Vorlage bei $t = 10^4$ s beide 24 % neben der analytischen Porosität. Ein
wahrscheinlicher Grund ist die explizite Behandlung der Kinetik: Die Fällungsrate jedes Schritts wird aus dem *vorherigen* $\Omega$ und $\phi$
berechnet. Mit 10 s sinkt der Fehler auf 0,3 %, mit 1 s steigt er aber wieder auf 2,7 %. Das Ergebnis konvergiert für $\Delta t \to 0$
also nicht sauber, und die verbleibende Abweichung von einigen Prozent ist ungeklärt (siehe Schlussfolgerungen)."""),
}
CONCL['01_hayekit'] = {
'en': r"""## Conclusions

**Supported by this case**

- The template implements the OGS-GEM rules for a kinetic mineral (moving lower/upper limits, seeding, cold starts), the restart
  initialisation, the `hayekit` water scaling and the porosity–diffusivity feedback as OGS does: the two codes agree to 10⁻⁵–10⁻⁴.
- The large error of both codes against the analytical solution at 100 s is a time-step effect, not a difference between the codes.

**Not shown, or open**

- Convergence to the analytical solution: with dt = 1 s a difference of about 3 % remains. Possible causes are the spatial resolution,
  the non-reacting boundary nodes, or assumptions of the analytical solution; none of them has been tested separately.
- The case is 1D and has no flow.
""",
'zh': r"""## 结论

**这个算例支持的结论**

- 模板对动力学矿物（移动的上下限、成核种子、冷启动）、重启初始化、`hayekit` 水量缩放以及孔隙率–扩散系数反馈的处理与 OGS 一致：两个代码的结果吻合到 10⁻⁵–10⁻⁴。
- 100 s 时两个代码相对解析解的大误差是时间步造成的，不是两个代码之间的差别。

**没有说明的、或仍未解决的问题**

- 是否收敛到解析解：dt = 1 s 时仍差约 3 %。可能的原因有空间分辨率、不参与反应的边界节点，或解析解本身的假设，这些都没有单独检验。
- 算例是一维的，没有水流。
""",
'de': r"""## Schlussfolgerungen

**Was dieser Fall belegt**

- Die Vorlage setzt die OGS-GEM-Regeln für ein kinetisches Mineral (wandernde untere/obere Grenzen, Keimbildung, Kaltstarts), die
  Restart-Initialisierung, die `hayekit`-Wasserskalierung und die Rückkopplung Porosität–Diffusivität so um wie OGS: Beide Codes stimmen auf 10⁻⁵–10⁻⁴ überein.
- Der große Fehler beider Codes gegenüber der analytischen Lösung bei 100 s ist ein Zeitschritteffekt, kein Unterschied zwischen den Codes.

**Nicht gezeigt oder offen**

- Konvergenz gegen die analytische Lösung: Mit dt = 1 s bleiben etwa 3 %. Mögliche Ursachen sind die räumliche Auflösung, die nicht
  reagierenden Randknoten oder Annahmen der analytischen Lösung; keine davon wurde einzeln geprüft.
- Der Fall ist eindimensional und ohne Strömung.
""",
}

# ---------------------------------------------------------------- V2 calcite
HEAD['02_calcite'] = {
'en': r"""# V2 · Calcite column: an equilibrium front moving with the flow

| | |
|---|---|
| **What is tested** | Advection–dispersion of all element totals with equilibrium chemistry (calcite dissolution, dolomite precipitation), and the OGS rules for converting between transported concentrations and node amounts (`hydrology='full'`). |
| **Reference** | OGS5GEMDEV output `calcite0210.vtk` at t = 21 000 s (210 steps of 100 s), same mesh (101 nodes). No analytical solution. |
| **Compared variables** | pH, porosity, element concentrations (mol/m³ water), calcite, dolomite, Ca²⁺, Mg²⁺, Cl⁻ at all nodes. Error = max\|template − OGS\| / max\|OGS\|. |
| **Result** | Dissolved elements and ions ≤ 1.1 %, pH 2·10⁻³ (absolute), porosity 3·10⁻⁷. Calcite and dolomite 5 % — at one node, the one at the dissolution front (x = 0.19 m); elsewhere they differ by less than 10⁻⁴ mol/m³. |
| **Conclusion** | Front positions and plateaus are reproduced. The remaining difference is concentrated at the front node, which reacts most to small input changes; its cause (GEMS version or round-off) has not been separated. |
| **Code and run** | `GEMS_FEniCSx_OGS5_Template/cases/1_calcite`: `python run_case.py` (or `Run.cmd`). This is the OGS template, not the `case.yaml` code of the tutorials. |

""",
'zh': r"""# V2 · 方解石柱：随水流移动的平衡锋面

| | |
|---|---|
| **检验什么** | 全部元素总量的对流–弥散加平衡化学（方解石溶解、白云石沉淀），以及 OGS 在输运浓度和节点量之间换算的规则（`hydrology='full'`）。 |
| **参考** | OGS5GEMDEV 在 t = 21 000 s（210 步 × 100 s）的输出 `calcite0210.vtk`，相同网格（101 个节点）。没有解析解。 |
| **比较的量** | 所有节点上的 pH、孔隙率、元素浓度（mol/m³ 水）、方解石、白云石、Ca²⁺、Mg²⁺、Cl⁻。误差 = max\|模板 − OGS\| / max\|OGS\|。 |
| **结果** | 溶解元素和离子 ≤ 1.1 %，pH 差 2·10⁻³（绝对值），孔隙率 3·10⁻⁷。方解石和白云石差 5 %，但只在溶解锋面处的一个节点（x = 0.19 m）；其他位置相差不到 10⁻⁴ mol/m³。 |
| **结论** | 锋面位置和平台值都复现了。剩余差异集中在锋面节点，该节点对输入的微小变化最敏感；差异来自 GEMS 版本还是舍入误差，没有分开检验。 |
| **代码与运行** | `GEMS_FEniCSx_OGS5_Template/cases/1_calcite`：`python run_case.py`（或 `Run.cmd`）。这是 OGS 模板，不是教程里的 `case.yaml` 代码。 |

""",
'de': r"""# V2 · Calcitsäule: eine Gleichgewichtsfront, die mit der Strömung wandert

| | |
|---|---|
| **Was geprüft wird** | Advektion–Dispersion aller Elementmengen mit Gleichgewichtschemie (Calcitlösung, Dolomitfällung) und die OGS-Regeln zur Umrechnung zwischen transportierten Konzentrationen und Knotenmengen (`hydrology='full'`). |
| **Referenz** | OGS5GEMDEV-Ausgabe `calcite0210.vtk` bei t = 21 000 s (210 Schritte zu 100 s), gleiches Netz (101 Knoten). Keine analytische Lösung. |
| **Verglichene Größen** | pH, Porosität, Elementkonzentrationen (mol/m³ Wasser), Calcit, Dolomit, Ca²⁺, Mg²⁺, Cl⁻ an allen Knoten. Fehler = max\|Vorlage − OGS\| / max\|OGS\|. |
| **Ergebnis** | Gelöste Elemente und Ionen ≤ 1,1 %, pH 2·10⁻³ (absolut), Porosität 3·10⁻⁷. Calcit und Dolomit 5 % — an einem Knoten, dem an der Lösungsfront (x = 0,19 m); sonst unter 10⁻⁴ mol/m³. |
| **Schluss** | Frontlagen und Plateaus werden reproduziert. Die verbleibende Abweichung sitzt am Frontknoten, der am stärksten auf kleine Änderungen der Eingabe reagiert; ihre Ursache (GEMS-Version oder Rundung) wurde nicht getrennt. |
| **Code und Lauf** | `GEMS_FEniCSx_OGS5_Template/cases/1_calcite`: `python run_case.py` (oder `Run.cmd`). Das ist die OGS-Vorlage, nicht der `case.yaml`-Code der Tutorials. |

""",
}
CONCL['02_calcite'] = {
'en': r"""## Conclusions

**Supported by this case**

- Advection–dispersion of element totals with OGS's dispersivity and its concentration ↔ node-amount rules give the same fronts and
  plateaus as OGS at t = 21 000 s.
- Away from the dissolution front the two codes agree to better than 10⁻⁴ mol/m³.

**Not shown, or open**

- The 5 % mineral difference at the front node is attributed to the sensitivity of that node; whether it comes from the GEMS version
  or from round-off has not been tested.
- There is no comparison with an analytical solution and no mesh-convergence study here (Tutorial 5 looks at the mesh effect in the 1D code).
- The excess-water flow source of OGS is not modelled; with ~0.1 mol/m³ of minerals the volume change is estimated at ~10⁻⁶ m³, but this was not checked by a run.
""",
'zh': r"""## 结论

**这个算例支持的结论**

- 采用 OGS 的弥散度以及浓度 ↔ 节点量换算规则，对元素总量做对流–弥散，在 t = 21 000 s 得到与 OGS 相同的锋面和平台值。
- 离开溶解锋面后，两个代码的差异小于 10⁻⁴ mol/m³。

**没有说明的、或仍未解决的问题**

- 锋面节点处 5 % 的矿物差异被归因于该节点的敏感性；它来自 GEMS 版本还是舍入误差，没有检验。
- 这里没有与解析解对比，也没有做网格收敛研究（教程 5 在一维代码中考察了网格的影响）。
- 没有模拟 OGS 的多余水流源项；矿物量约 0.1 mol/m³，估计体积变化约 10⁻⁶ m³，但没有通过计算验证。
""",
'de': r"""## Schlussfolgerungen

**Was dieser Fall belegt**

- Advektion–Dispersion der Elementmengen mit der Dispersivität von OGS und seinen Regeln für Konzentration ↔ Knotenmenge ergibt bei
  t = 21 000 s dieselben Fronten und Plateaus wie OGS.
- Abseits der Lösungsfront stimmen beide Codes besser als 10⁻⁴ mol/m³ überein.

**Nicht gezeigt oder offen**

- Die Mineralabweichung von 5 % am Frontknoten wird der Empfindlichkeit dieses Knotens zugeschrieben; ob sie von der GEMS-Version oder von Rundung
  kommt, wurde nicht geprüft.
- Es gibt hier keinen Vergleich mit einer analytischen Lösung und keine Gitterkonvergenzstudie (Tutorial 5 betrachtet den Gittereffekt im 1D-Code).
- Die Überschusswasserquelle von OGS wird nicht modelliert; bei ~0,1 mol/m³ Mineral wird die Volumenänderung auf ~10⁻⁶ m³ geschätzt, aber nicht durch einen Lauf geprüft.
""",
}

# ---------------------------------------------------------------- V3 OPC + quartz
HEAD['03_opc_quartz'] = {
'en': r"""# V3 · OPC concrete with quartz aggregate: slow kinetics over long times

| | |
|---|---|
| **What is tested** | Long-term chemistry driven by one slow kinetic mineral (quartz, alkali–silica reaction) in a closed system: initial species constraints, the two-pass OGS initialisation, `hydrology='none'` and a lumped mass matrix. |
| **Reference** | OGS5GEMDEV time series at the four monitoring nodes (`node1/10/50/100.dat`), 351 output times from 0 to **919 years**. No analytical solution. |
| **Compared variables** | Quartz, portlandite, C-S-H end members, ettringite, zeolites, gypsum, pH, porosity, dissolved Si, Ca, Na, Cl. Error = nRMSE: RMS difference over the OGS output times divided by the range of the OGS series. |
| **Result** | nRMSE ≤ 0.12 % for all variables except the zeolites (chabazite 0.28 %, scolecite 0.18 %). Portlandite is exhausted after 88 years (OGS 88.7), ettringite after 858 years (OGS 887). |
| **Conclusion** | The first 919 years of OGS are reproduced. The template is run to 10 000 years, but everything after 919 years is a prediction without a reference. |
| **Code and run** | `GEMS_FEniCSx_OGS5_Template/cases/3_opc_quartz`: `python run_case.py` (or `Run.cmd`), about 18 minutes. This is the OGS template, not the `case.yaml` code of the tutorials. |

""",
'zh': r"""# V3 · 含石英骨料的 OPC 混凝土：长时间的慢动力学

| | |
|---|---|
| **检验什么** | 封闭体系中由一种慢动力学矿物（石英，碱–硅反应）驱动的长期化学演化：初始物种约束、OGS 的两遍初始化、`hydrology='none'` 和集中质量矩阵。 |
| **参考** | OGS5GEMDEV 在四个监测节点（`node1/10/50/100.dat`）的时间序列，0 到 **919 年**共 351 个输出时刻。没有解析解。 |
| **比较的量** | 石英、portlandite、C-S-H 端元、钙矾石、沸石、石膏、pH、孔隙率、溶解的 Si、Ca、Na、Cl。误差 = nRMSE：在 OGS 输出时刻上的均方根差除以 OGS 序列的变化范围。 |
| **结果** | 除沸石外（菱沸石 0.28 %、钙沸石 0.18 %），所有量的 nRMSE ≤ 0.12 %。portlandite 在 88 年时耗尽（OGS 88.7 年），钙矾石在 858 年时耗尽（OGS 887 年）。 |
| **结论** | OGS 的前 919 年得到了复现。模板一直算到 10 000 年，但 919 年以后都是没有参考的预测。 |
| **代码与运行** | `GEMS_FEniCSx_OGS5_Template/cases/3_opc_quartz`：`python run_case.py`（或 `Run.cmd`），约 18 分钟。这是 OGS 模板，不是教程里的 `case.yaml` 代码。 |

""",
'de': r"""# V3 · OPC-Beton mit Quarzzuschlag: langsame Kinetik über lange Zeiten

| | |
|---|---|
| **Was geprüft wird** | Langzeitchemie, angetrieben von einem langsamen kinetischen Mineral (Quarz, Alkali-Kieselsäure-Reaktion) in einem geschlossenen System: Anfangsbedingungen für Spezies, die zweistufige OGS-Initialisierung, `hydrology='none'` und eine konzentrierte Massenmatrix. |
| **Referenz** | OGS5GEMDEV-Zeitreihen an den vier Beobachtungsknoten (`node1/10/50/100.dat`), 351 Ausgabezeiten von 0 bis **919 Jahren**. Keine analytische Lösung. |
| **Verglichene Größen** | Quarz, Portlandit, C-S-H-Endglieder, Ettringit, Zeolithe, Gips, pH, Porosität, gelöstes Si, Ca, Na, Cl. Fehler = nRMSE: RMS-Abweichung über die OGS-Ausgabezeiten, geteilt durch die Spannweite der OGS-Reihe. |
| **Ergebnis** | nRMSE ≤ 0,12 % für alle Größen außer den Zeolithen (Chabasit 0,28 %, Skolezit 0,18 %). Portlandit ist nach 88 Jahren aufgebraucht (OGS 88,7), Ettringit nach 858 Jahren (OGS 887). |
| **Schluss** | Die ersten 919 Jahre von OGS werden reproduziert. Die Vorlage rechnet bis 10 000 Jahre, aber alles nach 919 Jahren ist eine Vorhersage ohne Referenz. |
| **Code und Lauf** | `GEMS_FEniCSx_OGS5_Template/cases/3_opc_quartz`: `python run_case.py` (oder `Run.cmd`), etwa 18 Minuten. Das ist die OGS-Vorlage, nicht der `case.yaml`-Code der Tutorials. |

""",
}
CONCL['03_opc_quartz'] = {
'en': r"""## Conclusions

**Supported by this case**

- Constraints, the two-pass initialisation with pinned kinetic phases, the quartz rate law with cold starts and `hydrology='none'`
  are implemented as in OGS: the mineral assemblage and pore water follow OGS to ≤ 0.3 % (nRMSE) over 919 years.

**Not shown, or open**

- Nothing after 919 years: the remaining 9000 years are a prediction without a reference.
- Transport is not tested. OGS ignores the boundary conditions (they are written after `#STOP`), so the column is closed and every node is the same batch reactor.
- The time step differs (1–10 years here, adaptive steps ≤ 10⁵ s in OGS). The 30-year later exhaustion of ettringite in OGS is probably a
  time-step effect, but this has not been tested.
- Gas diffusion (`$FLAG_GAS_DIFFUSION 1`) is not modelled.
""",
'zh': r"""## 结论

**这个算例支持的结论**

- 约束、固定动力学相后的两遍初始化、带冷启动的石英速率方程以及 `hydrology='none'` 的实现与 OGS 一致：在 919 年内，矿物组合和孔隙水与 OGS 的偏差 ≤ 0.3 %（nRMSE）。

**没有说明的、或仍未解决的问题**

- 919 年以后没有任何对比：剩下的 9000 年是没有参考的预测。
- 没有检验输运。OGS 忽略了边界条件（它们写在 `#STOP` 之后），所以柱子是封闭的，每个节点都是同样的批式反应器。
- 时间步不同（这里 1–10 年，OGS 为 ≤ 10⁵ s 的自适应步长）。OGS 中钙矾石晚 30 年耗尽，可能是时间步的影响，但没有检验。
- 没有模拟气体扩散（`$FLAG_GAS_DIFFUSION 1`）。
""",
'de': r"""## Schlussfolgerungen

**Was dieser Fall belegt**

- Nebenbedingungen, die zweistufige Initialisierung mit festgehaltenen kinetischen Phasen, das Quarz-Ratengesetz mit Kaltstarts und
  `hydrology='none'` sind wie in OGS umgesetzt: Mineralbestand und Porenwasser folgen OGS über 919 Jahre auf ≤ 0,3 % (nRMSE).

**Nicht gezeigt oder offen**

- Nichts nach 919 Jahren: Die übrigen 9000 Jahre sind eine Vorhersage ohne Referenz.
- Der Transport wird nicht geprüft. OGS ignoriert die Randbedingungen (sie stehen nach `#STOP`), die Säule ist also geschlossen und jeder Knoten derselbe Batchreaktor.
- Der Zeitschritt unterscheidet sich (hier 1–10 Jahre, in OGS adaptive Schritte ≤ 10⁵ s). Das um 30 Jahre spätere Verschwinden von Ettringit in OGS ist
  wahrscheinlich ein Zeitschritteffekt, wurde aber nicht geprüft.
- Gasdiffusion (`$FLAG_GAS_DIFFUSION 1`) wird nicht modelliert.
""",
}

# ---------------------------------------------------------------- V4 comedy2d
HEAD['04_comedy2d'] = {
'en': r"""# V4 · comedy2d: 2D flow with two kinetic phases (short restart run)

| | |
|---|---|
| **What is tested** | A 2D Darcy flow field driving advection–dispersion, two kinetic phases with the OGS 2017 rules (sub-steps, lower-limit checks), and the excess-water source from GEMS volume changes. |
| **Reference** | OGS5GEMDEV output after **6 steps (68 s)**, restarted from an OGS state at about 7.5 days; same mesh (1849 nodes). |
| **Compared variables** | Element concentrations, porosity, pH, head, portlandite and calcium oxalate at all nodes, plus element velocities; also the *change* during the 68 s. Error = max\|template − OGS\| / max\|OGS\|. |
| **Result** | With loose kinetic limits: ≤ 1.4·10⁻⁴ for all variables (Ca), head 10⁻⁹, velocities ~10⁻⁵. With strict limits Ca is 56 % off — the reference corresponds to loose limits. |
| **Conclusion** | The short-term change near the reaction front is reproduced node by node, and the comparison identifies how the 2017 OGS code treated kinetic limits. Longer times are not compared. |
| **Code and run** | `GEMS_FEniCSx_OGS5_Template/cases/4_comedy2d`: `python run_case.py` (or `Run.cmd`). This is the OGS template, not the `case.yaml` code of the tutorials. |

""",
'zh': r"""# V4 · comedy2d：带两个动力学相的二维水流（短时重启计算）

| | |
|---|---|
| **检验什么** | 二维 Darcy 流场驱动的对流–弥散，按 OGS 2017 规则处理的两个动力学相（子步、下限检查），以及 GEMS 体积变化产生的多余水源项。 |
| **参考** | OGS5GEMDEV 从约 7.5 天时的 OGS 状态重启、计算 **6 步（68 s）** 后的输出；相同网格（1849 个节点）。 |
| **比较的量** | 所有节点上的元素浓度、孔隙率、pH、水头、portlandite 和草酸钙，以及单元流速；另外还比较 68 s 内的 *变化量*。误差 = max\|模板 − OGS\| / max\|OGS\|。 |
| **结果** | 用宽松（loose）的动力学上下限时：所有量 ≤ 1.4·10⁻⁴（Ca），水头 10⁻⁹，流速约 10⁻⁵。用严格（strict）上下限时 Ca 差 56 %，说明参考结果对应的是宽松上下限。 |
| **结论** | 反应锋面附近的短时变化被逐节点复现；比较还确定了 2017 版 OGS 代码处理动力学上下限的方式。更长时间的演化没有对比。 |
| **代码与运行** | `GEMS_FEniCSx_OGS5_Template/cases/4_comedy2d`：`python run_case.py`（或 `Run.cmd`）。这是 OGS 模板，不是教程里的 `case.yaml` 代码。 |

""",
'de': r"""# V4 · comedy2d: 2D-Strömung mit zwei kinetischen Phasen (kurzer Restart-Lauf)

| | |
|---|---|
| **Was geprüft wird** | Ein 2D-Darcy-Strömungsfeld, das Advektion–Dispersion antreibt, zwei kinetische Phasen nach den OGS-Regeln von 2017 (Unterschritte, Prüfung der unteren Grenzen) und die Überschusswasserquelle aus GEMS-Volumenänderungen. |
| **Referenz** | OGS5GEMDEV-Ausgabe nach **6 Schritten (68 s)**, neu gestartet von einem OGS-Zustand bei etwa 7,5 Tagen; gleiches Netz (1849 Knoten). |
| **Verglichene Größen** | Elementkonzentrationen, Porosität, pH, Druckhöhe, Portlandit und Calciumoxalat an allen Knoten sowie Elementgeschwindigkeiten; außerdem die *Änderung* während der 68 s. Fehler = max\|Vorlage − OGS\| / max\|OGS\|. |
| **Ergebnis** | Mit lockeren kinetischen Grenzen: ≤ 1,4·10⁻⁴ für alle Größen (Ca), Druckhöhe 10⁻⁹, Geschwindigkeiten ~10⁻⁵. Mit strengen Grenzen liegt Ca 56 % daneben — die Referenz entspricht den lockeren Grenzen. |
| **Schluss** | Die kurzfristige Änderung an der Reaktionsfront wird Knoten für Knoten reproduziert, und der Vergleich zeigt, wie der OGS-Code von 2017 kinetische Grenzen behandelte. Längere Zeiten werden nicht verglichen. |
| **Code und Lauf** | `GEMS_FEniCSx_OGS5_Template/cases/4_comedy2d`: `python run_case.py` (oder `Run.cmd`). Das ist die OGS-Vorlage, nicht der `case.yaml`-Code der Tutorials. |

""",
}
CONCL['04_comedy2d'] = {
'en': r"""## Conclusions

**Supported by this case**

- 2D Darcy flow, advection–dispersion driven by the flux $-K\nabla h$, two kinetic phases with sub-steps and lower-limit checks, and the
  excess-water source reproduce the OGS changes over 68 s node by node (≤ 1.4·10⁻⁴).
- The reference was produced with *loose* kinetic limits; this follows from the comparison (strict limits give 56 % in Ca), not from the OGS input.

**Not shown, or open**

- Only 68 s after a restart are compared; the evolution over days is not.
- In the restart run GEMS fails twice at five nodes (1065, 1067, 1171, 1177, 1183). OGS continues there, and so does the template
  (`on_failure='continue'`); the effect of these nodes has not been isolated.
- `retry_perturb=1e-12` is not an OGS rule; it is needed because the current GEMS3K sometimes fails at one front node.
""",
'zh': r"""## 结论

**这个算例支持的结论**

- 二维 Darcy 流、由通量 $-K\nabla h$ 驱动的对流–弥散、带子步和下限检查的两个动力学相，以及多余水源项，逐节点复现了 OGS 在 68 s 内的变化（≤ 1.4·10⁻⁴）。
- 参考结果是用 *宽松* 的动力学上下限算出的；这一点是从比较中得出的（严格上下限时 Ca 差 56 %），而不是从 OGS 输入中读出的。

**没有说明的、或仍未解决的问题**

- 只比较了重启后的 68 s，没有比较几天尺度上的演化。
- 重启计算中有 5 个节点（1065、1067、1171、1177、1183）的 GEMS 计算两次都失败。OGS 在这些节点上继续计算，模板也一样（`on_failure='continue'`）；这些节点的影响没有单独分析。
- `retry_perturb=1e-12` 不是 OGS 的规则；之所以需要它，是因为当前的 GEMS3K 有时会在一个锋面节点上失败。
""",
'de': r"""## Schlussfolgerungen

**Was dieser Fall belegt**

- 2D-Darcy-Strömung, Advektion–Dispersion mit dem Fluss $-K\nabla h$, zwei kinetische Phasen mit Unterschritten und Prüfung der unteren Grenzen sowie
  die Überschusswasserquelle reproduzieren die OGS-Änderungen über 68 s Knoten für Knoten (≤ 1,4·10⁻⁴).
- Die Referenz wurde mit *lockeren* kinetischen Grenzen erzeugt; das folgt aus dem Vergleich (strenge Grenzen ergeben 56 % bei Ca), nicht aus der OGS-Eingabe.

**Nicht gezeigt oder offen**

- Verglichen werden nur 68 s nach einem Restart, nicht die Entwicklung über Tage.
- Im Restart-Lauf scheitert GEMS an fünf Knoten (1065, 1067, 1171, 1177, 1183) zweimal. OGS rechnet dort weiter, die Vorlage ebenso
  (`on_failure='continue'`); der Einfluss dieser Knoten wurde nicht isoliert.
- `retry_perturb=1e-12` ist keine OGS-Regel; es wird gebraucht, weil das aktuelle GEMS3K an einem Frontknoten manchmal scheitert.
""",
}

# ---------------------------------------------------------------- V5 ConcreteCrack
HEAD['05_concretecrack'] = {
'en': r"""# V5 · ConcreteCrack: a fracture in concrete and the limits of reproduction

| | |
|---|---|
| **What is tested** | Fracture line elements in a 2D mesh, porosity-dependent permeability (Kozeny–Carman) and diffusion, FEM-FCT, and the initialisation of four chemical zones — over the first 10 s. |
| **Reference** | OGS5GEMDEV output `decal0010.vtk` at t = 10 s (10 steps of 1 s), written by 4 PETSc processes; mapped to the template mesh by coordinates. No analytical solution. |
| **Compared variables** | 11 element concentrations, porosity, pH, portlandite and head at all nodes, for four variants (OGS FCT sign, textbook FCT, no FCT, no excess-water source). Error = max\|template − OGS\| / max\|OGS\|. |
| **Result** | Elements ≤ 1.3·10⁻³, porosity ~3·10⁻⁶, pH ~4·10⁻⁵, portlandite ≤ 2·10⁻⁵ — the level at which OGS itself scatters for identical compositions (~10⁻³). The **head is not reproduced** in any variant (relative error of head − 10 m is 0.5–0.6). |
| **Conclusion** | The initial chemistry and the first 10 s of crack–matrix coupling agree with OGS. A node-by-node head comparison is not meaningful here (ill-conditioned flow matrix, excess water from GEMS round-off), and the four variants cannot be distinguished. |
| **Code and run** | `GEMS_FEniCSx_OGS5_Template/cases/5_concretecrack`: `python run_case.py` (or `Run.cmd`). This is the OGS template, not the `case.yaml` code of the tutorials. |

""",
'zh': r"""# V5 · ConcreteCrack：混凝土中的裂缝与复现的极限

| | |
|---|---|
| **检验什么** | 嵌入二维网格的裂缝线单元、随孔隙率变化的渗透率（Kozeny–Carman）和扩散、FEM-FCT，以及四个化学分区的初始化，时间只有最初 10 s。 |
| **参考** | OGS5GEMDEV 在 t = 10 s（10 步 × 1 s）的输出 `decal0010.vtk`，由 4 个 PETSc 进程写出，按坐标映射到模板网格。没有解析解。 |
| **比较的量** | 所有节点上的 11 种元素浓度、孔隙率、pH、portlandite 和水头，共四种变体（OGS 的 FCT 符号、教科书 FCT、不用 FCT、不加多余水源项）。误差 = max\|模板 − OGS\| / max\|OGS\|。 |
| **结果** | 元素 ≤ 1.3·10⁻³，孔隙率约 3·10⁻⁶，pH 约 4·10⁻⁵，portlandite ≤ 2·10⁻⁵，与 OGS 自身对相同组成给出的离散程度（约 10⁻³）相当。**水头在任何变体中都没有复现**（水头 − 10 m 的相对误差为 0.5–0.6）。 |
| **结论** | 初始化学和最初 10 s 的裂缝–基质耦合与 OGS 一致。这里逐节点比较水头没有意义（流动矩阵病态，多余水来自 GEMS 的舍入误差），四种变体也无法区分。 |
| **代码与运行** | `GEMS_FEniCSx_OGS5_Template/cases/5_concretecrack`：`python run_case.py`（或 `Run.cmd`）。这是 OGS 模板，不是教程里的 `case.yaml` 代码。 |

""",
'de': r"""# V5 · ConcreteCrack: ein Riss im Beton und die Grenzen der Reproduktion

| | |
|---|---|
| **Was geprüft wird** | Kluft-Linienelemente in einem 2D-Netz, porositätsabhängige Permeabilität (Kozeny–Carman) und Diffusion, FEM-FCT und die Initialisierung von vier chemischen Zonen — über die ersten 10 s. |
| **Referenz** | OGS5GEMDEV-Ausgabe `decal0010.vtk` bei t = 10 s (10 Schritte zu 1 s), geschrieben von 4 PETSc-Prozessen; über Koordinaten auf das Netz der Vorlage abgebildet. Keine analytische Lösung. |
| **Verglichene Größen** | 11 Elementkonzentrationen, Porosität, pH, Portlandit und Druckhöhe an allen Knoten, für vier Varianten (OGS-FCT-Vorzeichen, Lehrbuch-FCT, ohne FCT, ohne Überschusswasserquelle). Fehler = max\|Vorlage − OGS\| / max\|OGS\|. |
| **Ergebnis** | Elemente ≤ 1,3·10⁻³, Porosität ~3·10⁻⁶, pH ~4·10⁻⁵, Portlandit ≤ 2·10⁻⁵ — das Niveau, auf dem OGS selbst bei identischer Zusammensetzung streut (~10⁻³). Die **Druckhöhe wird in keiner Variante reproduziert** (relativer Fehler von Druckhöhe − 10 m: 0,5–0,6). |
| **Schluss** | Die Anfangschemie und die ersten 10 s der Kopplung von Riss und Matrix stimmen mit OGS überein. Ein knotengenauer Vergleich der Druckhöhe ist hier nicht sinnvoll (schlecht konditionierte Strömungsmatrix, Überschusswasser aus GEMS-Rundung), und die vier Varianten lassen sich nicht unterscheiden. |
| **Code und Lauf** | `GEMS_FEniCSx_OGS5_Template/cases/5_concretecrack`: `python run_case.py` (oder `Run.cmd`). Das ist die OGS-Vorlage, nicht der `case.yaml`-Code der Tutorials. |

""",
}
CONCL['05_concretecrack'] = {
'en': r"""## Conclusions

**Supported by this case**

- The fracture line elements (scaled by the aperture), Kozeny–Carman permeability, porosity-dependent diffusion and the zone-wise
  initialisation give the same chemistry as OGS after 10 s, to the level of GEMS's own scatter.

**Not shown, or open**

- The head: it is dominated by excess water from GEMS round-off and by an ill-conditioned flow matrix (conductivity contrast 8·10⁹;
  reordering the same matrix alone changes the head by 7·10⁻⁶ m). A node-by-node comparison does not test the model here.
- The FCT sign: OGS's non-conservative sign and the conservative textbook sign give differences smaller than the head noise, so this
  reference cannot decide between them. The template now uses the conservative sign by default.
- Leaching: 10 s is far too short for any degradation; longer runs are not compared.
""",
'zh': r"""## 结论

**这个算例支持的结论**

- 裂缝线单元（按开度缩放）、Kozeny–Carman 渗透率、随孔隙率变化的扩散以及分区初始化，在 10 s 后给出与 OGS 相同的化学结果，吻合到 GEMS 自身的离散水平。

**没有说明的、或仍未解决的问题**

- 水头：它主要由 GEMS 舍入误差产生的多余水和病态的流动矩阵决定（渗透系数之比 8·10⁹；仅把同一个矩阵换一种节点排序，水头就变化 7·10⁻⁶ m）。在这里逐节点比较水头检验不了模型。
- FCT 的符号：OGS 不守恒的符号和守恒的教科书符号带来的差异比水头噪声还小，所以这个参考无法区分两者。模板现在默认用守恒的符号。
- 溶蚀：10 s 太短，看不到任何劣化；更长时间的计算没有对比。
""",
'de': r"""## Schlussfolgerungen

**Was dieser Fall belegt**

- Die Kluft-Linienelemente (mit der Öffnungsweite skaliert), die Kozeny–Carman-Permeabilität, die porositätsabhängige Diffusion und die zonenweise
  Initialisierung ergeben nach 10 s dieselbe Chemie wie OGS, auf dem Niveau der eigenen Streuung von GEMS.

**Nicht gezeigt oder offen**

- Die Druckhöhe: Sie wird von Überschusswasser aus GEMS-Rundung und einer schlecht konditionierten Strömungsmatrix bestimmt (Leitfähigkeitskontrast 8·10⁹;
  allein das Umsortieren derselben Matrix ändert die Druckhöhe um 7·10⁻⁶ m). Ein knotengenauer Vergleich prüft hier nicht das Modell.
- Das FCT-Vorzeichen: Das nicht erhaltende Vorzeichen von OGS und das erhaltende Lehrbuchvorzeichen ergeben Unterschiede, die kleiner als das Rauschen der
  Druckhöhe sind; diese Referenz kann nicht zwischen ihnen entscheiden. Die Vorlage verwendet jetzt standardmäßig das erhaltende Vorzeichen.
- Auslaugung: 10 s sind viel zu kurz für eine Degradation; längere Läufe werden nicht verglichen.
""",
}
