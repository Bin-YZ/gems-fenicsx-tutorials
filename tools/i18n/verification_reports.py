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

A and B **diffuse into a column from opposite ends**. Where they meet, **AB(s) precipitates at a kinetic rate**. The precipitate
fills the pores, so **porosity and diffusivity decrease**.

| | |
|---|---|
| **Tested** | Kinetic mineral, porosity–diffusivity feedback, OGS-GEM coupling rules (kinetic limits, restart initialisation, `hayekit` water scaling) |
| **References** | OGS5GEMDEV output `ab1d0100.vtk` (t = 10 000 s, dt = 100 s); analytical solution of Hayek et al. (2011) |
| **Compared** | A, B, AB(s) and porosity at all 101 nodes |
| **Error** | max\|template − reference\| / max\|reference\| |
| **Code** | `GEMS_FEniCSx_OGS5_Template/cases/2_hayekit`: run `python run_case.py` (Windows: `Run.cmd`) |

## Results

- [x] **Agrees with OGS** (dt = 100 s): A, B, AB(s) ≤ 3·10⁻⁵, porosity 3·10⁻⁴.
- [ ] **Convergence to the analytical solution not shown.** The result depends on the time step:

| dt | porosity error at 10 000 s | computed with |
|---|---|---|
| 100 s | 24 % | OGS and template |
| 10 s | 0.3 % | template only |
| 1 s | 2.7 % | template only |

This chapter uses the OGS template, not the `case.yaml` code of the tutorials.

""",
'zh': r"""# V1 · HAYEKIT：扩散、沉淀与孔隙率反馈

A 和 B **从柱子两端相向扩散**，相遇处 **AB(s) 按动力学速率沉淀**。沉淀堵塞孔隙，**孔隙率和扩散系数随之下降**。

| | |
|---|---|
| **检验内容** | 动力学矿物、孔隙率–扩散系数反馈、OGS-GEM 耦合规则（动力学上下限、重启初始化、`hayekit` 水量缩放） |
| **参考** | OGS5GEMDEV 输出 `ab1d0100.vtk`（t = 10 000 s，dt = 100 s）；Hayek 等（2011）的解析解 |
| **比较的量** | 全部 101 个节点上的 A、B、AB(s) 和孔隙率 |
| **误差** | max\|模板 − 参考\| / max\|参考\| |
| **代码** | `GEMS_FEniCSx_OGS5_Template/cases/2_hayekit`：运行 `python run_case.py`（Windows：`Run.cmd`） |

## 结果

- [x] **与 OGS 一致**（dt = 100 s）：A、B、AB(s) ≤ 3·10⁻⁵，孔隙率 3·10⁻⁴。
- [ ] **未证明收敛到解析解。** 结果随时间步变化：

| dt | 10 000 s 时孔隙率误差 | 计算者 |
|---|---|---|
| 100 s | 24 % | OGS 和模板 |
| 10 s | 0.3 % | 只有模板 |
| 1 s | 2.7 % | 只有模板 |

本章使用 OGS 模板，不是教程中的 `case.yaml` 代码。

""",
'de': r"""# V1 · HAYEKIT: Diffusion, Fällung und Porositätsrückkopplung

| | |
|---|---|
| **Was geprüft wird** | Kinetische Fällung eines Minerals aus zwei gegeneinander diffundierenden gelösten Stoffen, mit Rückkopplung von Porosität und Diffusivität, nach den Kopplungsregeln von OGS-GEM (kinetische Grenzen, Restart-Initialisierung, `hayekit`-Wasserskalierung). |
| **Referenzen** | (1) OGS5GEMDEV-Ausgabe `ab1d0100.vtk`: gleiches Netz, gleicher Zeitschritt (100 s), t = 10 000 s. (2) Die analytische Lösung von Hayek, Kosakowski & Churakov (2011) bei t = 1000 s und 10 000 s. |
| **Verglichene Größen** | A, B (mol/m³ Wasser), AB(s) und Porosität an allen 101 Knoten. Fehler = max\|Vorlage − Referenz\| / max\|Referenz\|. |
| **Ergebnis** | Gegenüber OGS (dt = 100 s): ≤ 3·10⁻⁵ für A, B und AB(s), 3·10⁻⁴ für die Porosität. Gegenüber der analytischen Lösung (Porosität bei 10 000 s): 24 % mit dt = 100 s (OGS und Vorlage), 0,3 % mit 10 s und 2,7 % mit 1 s (nur die Vorlage; OGS wurde mit diesen Schritten nicht neu gerechnet). |
| **Schluss** | Die Vorlage reproduziert OGS in diesem Fall beim OGS-Zeitschritt. Die Ergebnisse der Vorlage hängen deutlich vom Zeitschritt ab, die vorhandenen Tests zeigen aber nicht, dass sie gegen die analytische Lösung konvergieren. |
| **Code und Lauf** | `GEMS_FEniCSx_OGS5_Template/cases/2_hayekit`: `python run_case.py` (oder `Run.cmd`). Das ist die OGS-Vorlage, nicht der `case.yaml`-Code der Tutorials. |

""",
}
FIX['01_hayekit'] = {
'en': (r"## Comparison with the analytical solution — the time step matters", r"""## Comparison with the analytical solution

The porosity error **depends on the time step**: 24 % at 100 s, 0.3 % at 10 s, and 2.7 % again at 1 s.
The error does not decrease steadily with dt, so **these runs do not show convergence** to the analytical solution.

- The 10 s and 1 s runs use the template only. OGS was not rerun.
- Possible cause: explicit kinetics (the rate uses $\Omega$ and $\phi$ of the previous step). Not tested."""),
'zh': (r"## 和解析解比较——时间步很关键", r"""## 与解析解比较

孔隙率误差 **取决于时间步**：100 s 时 24 %，10 s 时 0.3 %，1 s 时又升到 2.7 %。
误差不随 dt 单调减小，所以 **这些计算不能说明结果收敛到解析解**。

- 10 s 和 1 s 只用模板算过，OGS 没有重算。
- 可能的原因：动力学按显式处理（速率用上一步的 $\Omega$ 和 $\phi$）。未检验。"""),
'de': (r"## Vergleich mit der analytischen Lösung — der Zeitschritt zählt", r"""## Vergleich mit der analytischen Lösung — der Zeitschritt zählt

Mit dem OGS-Zeitschritt (100 s) liegen OGS und die Vorlage bei $t = 10^4$ s beide 24 % neben der analytischen Porosität. Die kleineren
Schritte wurden nur mit der Vorlage gerechnet (OGS nicht): Der Fehler beträgt 0,3 % mit 10 s und 2,7 % mit 1 s. Die Ergebnisse der Vorlage
hängen also deutlich vom Zeitschritt ab, der Fehler nimmt aber nicht stetig ab, und diese drei Läufe zeigen keine Konvergenz gegen die
analytische Lösung. Eine mögliche Ursache der Zeitschrittabhängigkeit ist die explizite Behandlung der Kinetik (die Fällungsrate jedes Schritts
wird aus dem *vorherigen* $\Omega$ und $\phi$ berechnet); das wurde nicht geprüft (siehe Schlussfolgerungen)."""),
}
CONCL['01_hayekit'] = {
'en': r"""## Conclusions

**Verified**

- [x] Kinetic mineral (moving limits, seeding, cold starts), restart initialisation, `hayekit` water scaling and
  porosity–diffusivity feedback behave as in OGS: agreement 10⁻⁵–10⁻⁴.
- [x] At dt = 100 s both codes have the same 24 % error against the analytical solution. The error is not a code difference.

**Not verified**

- [ ] Convergence to the analytical solution.
- [ ] Agreement with OGS at smaller time steps.
- [ ] 2D geometry and flow.
""",
'zh': r"""## 结论

**已验证**

- [x] 动力学矿物（移动的上下限、成核种子、冷启动）、重启初始化、`hayekit` 水量缩放和孔隙率–扩散系数反馈与 OGS 一致，误差 10⁻⁵–10⁻⁴。
- [x] dt = 100 s 时两个代码与解析解的误差相同（24 %）。这个误差不是代码之间的差别。

**未验证**

- [ ] 收敛到解析解。
- [ ] 更小时间步下与 OGS 的一致性。
- [ ] 二维几何和水流。
""",
'de': r"""## Schlussfolgerungen

**Was dieser Fall belegt**

- Die Vorlage setzt die OGS-GEM-Regeln für ein kinetisches Mineral (wandernde untere/obere Grenzen, Keimbildung, Kaltstarts), die
  Restart-Initialisierung, die `hayekit`-Wasserskalierung und die Rückkopplung Porosität–Diffusivität so um wie OGS: Beide Codes stimmen auf 10⁻⁵–10⁻⁴ überein.
- Beim OGS-Zeitschritt (100 s) haben beide Codes denselben Fehler von 24 % gegenüber der analytischen Lösung; dieser Fehler ist also kein Unterschied zwischen den Codes.

**Nicht gezeigt oder offen**

- Konvergenz gegen die analytische Lösung: Die Ergebnisse der Vorlage hängen deutlich vom Zeitschritt ab (24 %, 0,3 %, 2,7 % mit 100, 10, 1 s),
  die vorhandenen Tests zeigen aber nicht, dass sie gegen die analytische Lösung konvergieren. Explizite Kinetik, räumliche Auflösung, die nicht
  reagierenden Randknoten und Annahmen der analytischen Lösung sind mögliche Ursachen; keine wurde einzeln geprüft.
- Die kleineren Zeitschritte wurden nur mit der Vorlage gerechnet; mit OGS wurde nur bei 100 s verglichen.
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
| **What is tested** | Long-term chemistry driven by one slow kinetic mineral (quartz, alkali–silica reaction) with no transport across the boundaries, but with OGS's water replenishment: initial species constraints, the two-pass OGS initialisation, `hydrology='none'` and a lumped mass matrix. |
| **Reference** | OGS5GEMDEV time series at the four monitoring nodes (`node1/10/50/100.dat`), 351 output times from 0 to **919 years**. No analytical solution. |
| **Compared variables** | Quartz, portlandite, C-S-H end members, ettringite, zeolites, gypsum, pH, porosity, dissolved Si, Ca, Na, Cl. Error = nRMSE: RMS difference over the OGS output times divided by the range of the OGS series. |
| **Result** | nRMSE ≤ 0.12 % for all variables except the zeolites (chabazite 0.28 %, scolecite 0.18 %). Portlandite is exhausted after 88 years (OGS 88.7), ettringite after 858 years (OGS 887). |
| **Conclusion** | The first 919 years of OGS are reproduced. The template is run to 10 000 years, but everything after 919 years is a prediction without a reference. |
| **Code and run** | `GEMS_FEniCSx_OGS5_Template/cases/3_opc_quartz`: `python run_case.py` (or `Run.cmd`), about 18 minutes. This is the OGS template, not the `case.yaml` code of the tutorials. |

""",
'zh': r"""# V3 · 含石英骨料的 OPC 混凝土：长时间的慢动力学

| | |
|---|---|
| **检验什么** | 无边界输运、但包含 OGS 补水处理的体系中，由一种慢动力学矿物（石英，碱–硅反应）驱动的长期化学演化：初始物种约束、OGS 的两遍初始化、`hydrology='none'` 和集中质量矩阵。 |
| **参考** | OGS5GEMDEV 在四个监测节点（`node1/10/50/100.dat`）的时间序列，0 到 **919 年**共 351 个输出时刻。没有解析解。 |
| **比较的量** | 石英、portlandite、C-S-H 端元、钙矾石、沸石、石膏、pH、孔隙率、溶解的 Si、Ca、Na、Cl。误差 = nRMSE：在 OGS 输出时刻上的均方根差除以 OGS 序列的变化范围。 |
| **结果** | 除沸石外（菱沸石 0.28 %、钙沸石 0.18 %），所有量的 nRMSE ≤ 0.12 %。portlandite 在 88 年时耗尽（OGS 88.7 年），钙矾石在 858 年时耗尽（OGS 887 年）。 |
| **结论** | OGS 的前 919 年得到了复现。模板一直算到 10 000 年，但 919 年以后都是没有参考的预测。 |
| **代码与运行** | `GEMS_FEniCSx_OGS5_Template/cases/3_opc_quartz`：`python run_case.py`（或 `Run.cmd`），约 18 分钟。这是 OGS 模板，不是教程里的 `case.yaml` 代码。 |

""",
'de': r"""# V3 · OPC-Beton mit Quarzzuschlag: langsame Kinetik über lange Zeiten

| | |
|---|---|
| **Was geprüft wird** | Langzeitchemie, angetrieben von einem langsamen kinetischen Mineral (Quarz, Alkali-Kieselsäure-Reaktion) ohne Transport über die Ränder, aber mit der Wassernachlieferung von OGS: Anfangsbedingungen für Spezies, die zweistufige OGS-Initialisierung, `hydrology='none'` und eine konzentrierte Massenmatrix. |
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
- Transport is not tested. OGS ignores the boundary conditions (they are written after `#STOP`), so nothing crosses the boundaries and every node is the same batch reactor.
- The system is not closed in the strict sense: with `$FLAG_COUPLING_HYDROLOGY 0` the water consumed by reactions is replaced by pore water of the
  current composition (the template does the same with `hydrology='none'`), so the totals of H, O, Cl, Na and K increase. The comparison
  tests this OGS rule, not a mass-conserving batch reactor.
- The time step differs (1–10 years here, adaptive steps ≤ 10⁵ s in OGS). The 30-year later exhaustion of ettringite in OGS is probably a
  time-step effect, but this has not been tested.
- Gas diffusion (`$FLAG_GAS_DIFFUSION 1`) is not modelled.
""",
'zh': r"""## 结论

**这个算例支持的结论**

- 约束、固定动力学相后的两遍初始化、带冷启动的石英速率方程以及 `hydrology='none'` 的实现与 OGS 一致：在 919 年内，矿物组合和孔隙水与 OGS 的偏差 ≤ 0.3 %（nRMSE）。

**没有说明的、或仍未解决的问题**

- 919 年以后没有任何对比：剩下的 9000 年是没有参考的预测。
- 没有检验输运。OGS 忽略了边界条件（它们写在 `#STOP` 之后），所以没有物质穿过边界，每个节点都是同样的批式反应器。
- 这不是严格意义上的封闭体系：在 `$FLAG_COUPLING_HYDROLOGY 0` 下，反应消耗的水由当前组成的孔隙水补充（模板用 `hydrology='none'` 做同样的处理），因此 H、O、Cl、Na 和 K 的总量会增加。比较检验的是 OGS 的这一规则，而不是质量守恒的批式反应器。
- 时间步不同（这里 1–10 年，OGS 为 ≤ 10⁵ s 的自适应步长）。OGS 中钙矾石晚 30 年耗尽，可能是时间步的影响，但没有检验。
- 没有模拟气体扩散（`$FLAG_GAS_DIFFUSION 1`）。
""",
'de': r"""## Schlussfolgerungen

**Was dieser Fall belegt**

- Nebenbedingungen, die zweistufige Initialisierung mit festgehaltenen kinetischen Phasen, das Quarz-Ratengesetz mit Kaltstarts und
  `hydrology='none'` sind wie in OGS umgesetzt: Mineralbestand und Porenwasser folgen OGS über 919 Jahre auf ≤ 0,3 % (nRMSE).

**Nicht gezeigt oder offen**

- Nichts nach 919 Jahren: Die übrigen 9000 Jahre sind eine Vorhersage ohne Referenz.
- Der Transport wird nicht geprüft. OGS ignoriert die Randbedingungen (sie stehen nach `#STOP`), über die Ränder gelangt also nichts, und jeder Knoten ist derselbe Batchreaktor.
- Das System ist nicht im strengen Sinn geschlossen: Mit `$FLAG_COUPLING_HYDROLOGY 0` wird das von Reaktionen verbrauchte Wasser durch Porenwasser der
  aktuellen Zusammensetzung ersetzt (die Vorlage macht dasselbe mit `hydrology='none'`), daher nehmen die Gesamtmengen von H, O, Cl, Na und K zu. Der
  Vergleich prüft diese OGS-Regel, nicht einen massenerhaltenden Batchreaktor.
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
| **Compared variables** | Element concentrations, porosity, pH, head, portlandite and calcium oxalate at all nodes, plus element velocities. Error = max\|template − OGS\| / max\|OGS\| of the **state after 68 s**. The *change* during the 68 s is compared only as a spatial pattern (figure), without an error measure. |
| **Result** | With loose kinetic limits, state after 68 s: ≤ 1.4·10⁻⁴ for all variables (Ca), head 10⁻⁹, velocities ~10⁻⁵. With strict limits Ca is 56 % off — the reference corresponds to loose limits. |
| **Conclusion** | The state after 68 s agrees with OGS to ≤ 1.4·10⁻⁴, and the spatial pattern of the change near the reaction front matches the OGS pattern. Because the change is small compared with the state, the state error does not measure how accurately the change itself is reproduced. The comparison also identifies how the 2017 OGS code treated kinetic limits. Longer times are not compared. |
| **Code and run** | `GEMS_FEniCSx_OGS5_Template/cases/4_comedy2d`: `python run_case.py` (or `Run.cmd`). This is the OGS template, not the `case.yaml` code of the tutorials. |

""",
'zh': r"""# V4 · comedy2d：带两个动力学相的二维水流（短时重启计算）

| | |
|---|---|
| **检验什么** | 二维 Darcy 流场驱动的对流–弥散，按 OGS 2017 规则处理的两个动力学相（子步、下限检查），以及 GEMS 体积变化产生的多余水源项。 |
| **参考** | OGS5GEMDEV 从约 7.5 天时的 OGS 状态重启、计算 **6 步（68 s）** 后的输出；相同网格（1849 个节点）。 |
| **比较的量** | 所有节点上的元素浓度、孔隙率、pH、水头、portlandite 和草酸钙，以及单元流速。误差 = **68 s 后状态** 的 max\|模板 − OGS\| / max\|OGS\|。68 s 内的 *变化量* 只按空间分布（图）比较，没有误差指标。 |
| **结果** | 用宽松（loose）的动力学上下限时，68 s 后的状态：所有量 ≤ 1.4·10⁻⁴（Ca），水头 10⁻⁹，流速约 10⁻⁵。用严格（strict）上下限时 Ca 差 56 %，说明参考结果对应的是宽松上下限。 |
| **结论** | 68 s 后的状态与 OGS 吻合到 ≤ 1.4·10⁻⁴，反应锋面附近变化量的空间分布与 OGS 一致。由于变化量相对状态本身很小，状态误差不能衡量变化量本身复现得有多准。比较还确定了 2017 版 OGS 代码处理动力学上下限的方式。更长时间的演化没有对比。 |
| **代码与运行** | `GEMS_FEniCSx_OGS5_Template/cases/4_comedy2d`：`python run_case.py`（或 `Run.cmd`）。这是 OGS 模板，不是教程里的 `case.yaml` 代码。 |

""",
'de': r"""# V4 · comedy2d: 2D-Strömung mit zwei kinetischen Phasen (kurzer Restart-Lauf)

| | |
|---|---|
| **Was geprüft wird** | Ein 2D-Darcy-Strömungsfeld, das Advektion–Dispersion antreibt, zwei kinetische Phasen nach den OGS-Regeln von 2017 (Unterschritte, Prüfung der unteren Grenzen) und die Überschusswasserquelle aus GEMS-Volumenänderungen. |
| **Referenz** | OGS5GEMDEV-Ausgabe nach **6 Schritten (68 s)**, neu gestartet von einem OGS-Zustand bei etwa 7,5 Tagen; gleiches Netz (1849 Knoten). |
| **Verglichene Größen** | Elementkonzentrationen, Porosität, pH, Druckhöhe, Portlandit und Calciumoxalat an allen Knoten sowie Elementgeschwindigkeiten. Fehler = max\|Vorlage − OGS\| / max\|OGS\| des **Zustands nach 68 s**. Die *Änderung* während der 68 s wird nur als räumliches Muster (Abbildung) verglichen, ohne Fehlermaß. |
| **Ergebnis** | Mit lockeren kinetischen Grenzen, Zustand nach 68 s: ≤ 1,4·10⁻⁴ für alle Größen (Ca), Druckhöhe 10⁻⁹, Geschwindigkeiten ~10⁻⁵. Mit strengen Grenzen liegt Ca 56 % daneben — die Referenz entspricht den lockeren Grenzen. |
| **Schluss** | Der Zustand nach 68 s stimmt auf ≤ 1,4·10⁻⁴ mit OGS überein, und das räumliche Muster der Änderung an der Reaktionsfront entspricht dem von OGS. Da die Änderung klein gegenüber dem Zustand ist, misst der Zustandsfehler nicht, wie genau die Änderung selbst reproduziert wird. Der Vergleich zeigt außerdem, wie der OGS-Code von 2017 kinetische Grenzen behandelte. Längere Zeiten werden nicht verglichen. |
| **Code und Lauf** | `GEMS_FEniCSx_OGS5_Template/cases/4_comedy2d`: `python run_case.py` (oder `Run.cmd`). Das ist die OGS-Vorlage, nicht der `case.yaml`-Code der Tutorials. |

""",
}
CONCL['04_comedy2d'] = {
'en': r"""## Conclusions

**Supported by this case**

- 2D Darcy flow, advection–dispersion driven by the flux $-K\nabla h$, two kinetic phases with sub-steps and lower-limit checks, and the
  excess-water source reproduce the OGS state after 68 s (≤ 1.4·10⁻⁴, normalised by the maximum of the reference), and the
  spatial pattern of the change over the 68 s matches OGS.
- The reference was produced with *loose* kinetic limits; this follows from the comparison (strict limits give 56 % in Ca), not from the OGS input.

**Not shown, or open**

- The accuracy of the change itself: no error measure is computed for the 68-s change; the 1.4·10⁻⁴ refers to the state.
- Only 68 s after a restart are compared; the evolution over days is not.
- In the restart run GEMS fails twice at five nodes (1065, 1067, 1171, 1177, 1183). OGS continues there, and so does the template
  (`on_failure='continue'`); the effect of these nodes has not been isolated.
- `retry_perturb=1e-12` is not an OGS rule; it is needed because the current GEMS3K sometimes fails at one front node.
""",
'zh': r"""## 结论

**这个算例支持的结论**

- 二维 Darcy 流、由通量 $-K\nabla h$ 驱动的对流–弥散、带子步和下限检查的两个动力学相，以及多余水源项，复现了 OGS 在 68 s 后的状态（≤ 1.4·10⁻⁴，以参考解最大值归一化），68 s 内变化量的空间分布也与 OGS 一致。
- 参考结果是用 *宽松* 的动力学上下限算出的；这一点是从比较中得出的（严格上下限时 Ca 差 56 %），而不是从 OGS 输入中读出的。

**没有说明的、或仍未解决的问题**

- 变化量本身的精度：没有为 68 s 内的变化量计算误差指标；1.4·10⁻⁴ 指的是状态。
- 只比较了重启后的 68 s，没有比较几天尺度上的演化。
- 重启计算中有 5 个节点（1065、1067、1171、1177、1183）的 GEMS 计算两次都失败。OGS 在这些节点上继续计算，模板也一样（`on_failure='continue'`）；这些节点的影响没有单独分析。
- `retry_perturb=1e-12` 不是 OGS 的规则；之所以需要它，是因为当前的 GEMS3K 有时会在一个锋面节点上失败。
""",
'de': r"""## Schlussfolgerungen

**Was dieser Fall belegt**

- 2D-Darcy-Strömung, Advektion–Dispersion mit dem Fluss $-K\nabla h$, zwei kinetische Phasen mit Unterschritten und Prüfung der unteren Grenzen sowie
  die Überschusswasserquelle reproduzieren den OGS-Zustand nach 68 s (≤ 1,4·10⁻⁴, normiert auf das Maximum der Referenz), und das
  räumliche Muster der Änderung über die 68 s entspricht OGS.
- Die Referenz wurde mit *lockeren* kinetischen Grenzen erzeugt; das folgt aus dem Vergleich (strenge Grenzen ergeben 56 % bei Ca), nicht aus der OGS-Eingabe.

**Nicht gezeigt oder offen**

- Die Genauigkeit der Änderung selbst: Für die Änderung über 68 s wird kein Fehlermaß berechnet; die 1,4·10⁻⁴ beziehen sich auf den Zustand.
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
| **Compared variables** | 11 element concentrations, porosity, pH, portlandite and head at all nodes, for four variants (OGS FCT sign, textbook FCT, no FCT, no excess-water source). Error = max\|template − OGS\| / max\|OGS\|; for the head it is computed on head − 10 m (the head itself is ≈ 10 m everywhere). |
| **Result** | Elements ≤ 1.3·10⁻³, porosity ~3·10⁻⁶, pH ~4·10⁻⁵, portlandite ≤ 2·10⁻⁵ — the level at which OGS itself scatters for identical compositions (~10⁻³). The **head is not reproduced** in any variant (relative error of head − 10 m is 0.5–0.6). |
| **Conclusion** | The initial chemistry and the first 10 s of crack–matrix coupling agree with OGS. The current head comparison cannot distinguish the implementation variants and does not confirm that the flow part is verified (ill-conditioned flow matrix, excess water from GEMS round-off). |
| **Code and run** | `GEMS_FEniCSx_OGS5_Template/cases/5_concretecrack`: `python run_case.py` (or `Run.cmd`). This is the OGS template, not the `case.yaml` code of the tutorials. |

""",
'zh': r"""# V5 · ConcreteCrack：混凝土中的裂缝与复现的极限

| | |
|---|---|
| **检验什么** | 嵌入二维网格的裂缝线单元、随孔隙率变化的渗透率（Kozeny–Carman）和扩散、FEM-FCT，以及四个化学分区的初始化，时间只有最初 10 s。 |
| **参考** | OGS5GEMDEV 在 t = 10 s（10 步 × 1 s）的输出 `decal0010.vtk`，由 4 个 PETSc 进程写出，按坐标映射到模板网格。没有解析解。 |
| **比较的量** | 所有节点上的 11 种元素浓度、孔隙率、pH、portlandite 和水头，共四种变体（OGS 的 FCT 符号、教科书 FCT、不用 FCT、不加多余水源项）。误差 = max\|模板 − OGS\| / max\|OGS\|；水头的误差用 水头 − 10 m 计算（水头本身处处约为 10 m）。 |
| **结果** | 元素 ≤ 1.3·10⁻³，孔隙率约 3·10⁻⁶，pH 约 4·10⁻⁵，portlandite ≤ 2·10⁻⁵，与 OGS 自身对相同组成给出的离散程度（约 10⁻³）相当。**水头在任何变体中都没有复现**（水头 − 10 m 的相对误差为 0.5–0.6）。 |
| **结论** | 初始化学和最初 10 s 的裂缝–基质耦合与 OGS 一致。当前水头比较不足以区分各实现方案，也不能确认流动部分已通过验证（流动矩阵病态，多余水来自 GEMS 的舍入误差）。 |
| **代码与运行** | `GEMS_FEniCSx_OGS5_Template/cases/5_concretecrack`：`python run_case.py`（或 `Run.cmd`）。这是 OGS 模板，不是教程里的 `case.yaml` 代码。 |

""",
'de': r"""# V5 · ConcreteCrack: ein Riss im Beton und die Grenzen der Reproduktion

| | |
|---|---|
| **Was geprüft wird** | Kluft-Linienelemente in einem 2D-Netz, porositätsabhängige Permeabilität (Kozeny–Carman) und Diffusion, FEM-FCT und die Initialisierung von vier chemischen Zonen — über die ersten 10 s. |
| **Referenz** | OGS5GEMDEV-Ausgabe `decal0010.vtk` bei t = 10 s (10 Schritte zu 1 s), geschrieben von 4 PETSc-Prozessen; über Koordinaten auf das Netz der Vorlage abgebildet. Keine analytische Lösung. |
| **Verglichene Größen** | 11 Elementkonzentrationen, Porosität, pH, Portlandit und Druckhöhe an allen Knoten, für vier Varianten (OGS-FCT-Vorzeichen, Lehrbuch-FCT, ohne FCT, ohne Überschusswasserquelle). Fehler = max\|Vorlage − OGS\| / max\|OGS\|; für die Druckhöhe mit Druckhöhe − 10 m berechnet (die Druckhöhe selbst ist überall ≈ 10 m). |
| **Ergebnis** | Elemente ≤ 1,3·10⁻³, Porosität ~3·10⁻⁶, pH ~4·10⁻⁵, Portlandit ≤ 2·10⁻⁵ — das Niveau, auf dem OGS selbst bei identischer Zusammensetzung streut (~10⁻³). Die **Druckhöhe wird in keiner Variante reproduziert** (relativer Fehler von Druckhöhe − 10 m: 0,5–0,6). |
| **Schluss** | Die Anfangschemie und die ersten 10 s der Kopplung von Riss und Matrix stimmen mit OGS überein. Der vorliegende Vergleich der Druckhöhe kann die Implementierungsvarianten nicht unterscheiden und bestätigt nicht, dass der Strömungsteil verifiziert ist (schlecht konditionierte Strömungsmatrix, Überschusswasser aus GEMS-Rundung). |
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
  reordering the same matrix alone changes the head by 7·10⁻⁶ m). The current head comparison cannot distinguish the implementation variants
  and does not confirm that the flow part is verified.
- The FCT sign: OGS's non-conservative sign and the conservative textbook sign give differences smaller than the head noise, so this
  reference cannot decide between them. The template now uses the conservative sign by default.
- Leaching: 10 s is far too short for any degradation; longer runs are not compared.
""",
'zh': r"""## 结论

**这个算例支持的结论**

- 裂缝线单元（按开度缩放）、Kozeny–Carman 渗透率、随孔隙率变化的扩散以及分区初始化，在 10 s 后给出与 OGS 相同的化学结果，吻合到 GEMS 自身的离散水平。

**没有说明的、或仍未解决的问题**

- 水头：它主要由 GEMS 舍入误差产生的多余水和病态的流动矩阵决定（渗透系数之比 8·10⁹；仅把同一个矩阵换一种节点排序，水头就变化 7·10⁻⁶ m）。当前水头比较不足以区分各实现方案，也不能确认流动部分已通过验证。
- FCT 的符号：OGS 不守恒的符号和守恒的教科书符号带来的差异比水头噪声还小，所以这个参考无法区分两者。模板现在默认用守恒的符号。
- 溶蚀：10 s 太短，看不到任何劣化；更长时间的计算没有对比。
""",
'de': r"""## Schlussfolgerungen

**Was dieser Fall belegt**

- Die Kluft-Linienelemente (mit der Öffnungsweite skaliert), die Kozeny–Carman-Permeabilität, die porositätsabhängige Diffusion und die zonenweise
  Initialisierung ergeben nach 10 s dieselbe Chemie wie OGS, auf dem Niveau der eigenen Streuung von GEMS.

**Nicht gezeigt oder offen**

- Die Druckhöhe: Sie wird von Überschusswasser aus GEMS-Rundung und einer schlecht konditionierten Strömungsmatrix bestimmt (Leitfähigkeitskontrast 8·10⁹;
  allein das Umsortieren derselben Matrix ändert die Druckhöhe um 7·10⁻⁶ m). Der vorliegende Vergleich der Druckhöhe kann die Implementierungsvarianten nicht unterscheiden und bestätigt nicht, dass der Strömungsteil verifiziert ist.
- Das FCT-Vorzeichen: Das nicht erhaltende Vorzeichen von OGS und das erhaltende Lehrbuchvorzeichen ergeben Unterschiede, die kleiner als das Rauschen der
  Druckhöhe sind; diese Referenz kann nicht zwischen ihnen entscheiden. Die Vorlage verwendet jetzt standardmäßig das erhaltende Vorzeichen.
- Auslaugung: 10 s sind viel zu kurz für eine Degradation; längere Läufe werden nicht verglichen.
""",
}

# ---------------------------------------------------------------- edits in the original notebook text
EDITS = {}
EDITS['03_opc_quartz'] = {
'en': [(r"""reading at the first `#STOP`, so the column is closed.""", r"""reading at the first `#STOP`, so nothing crosses the boundaries."""),
(r"""The column is closed and homogeneous: every node is the same batch reactor, and the
four OGS monitoring nodes give identical results. Transport is still solved (and must not change anything).""",
r"""Nothing crosses the boundaries and the column is homogeneous: every node is the same batch reactor, and the
four OGS monitoring nodes give identical results. Transport is still solved (and must not change anything).
The column is not a closed system, though: with `$FLAG_COUPLING_HYDROLOGY 0` OGS replaces the water consumed by
reactions with pore water of the current composition, so the totals of H, O, Cl, Na and K increase. The template does
the same (`hydrology='none'`).""")],
'zh': [(r"""OGS 读到第一个 `#STOP` 就停，所以柱子是封闭的。""", r"""OGS 读到第一个 `#STOP` 就停，所以没有物质穿过边界。"""),
(r"""柱子是封闭、均匀的：每个节点都是同样的
批反应器，OGS 的 4 个监测节点结果完全相同。输运照样要算（而且不应改变任何东西）。""",
r"""没有物质穿过边界，柱子是均匀的：每个节点都是同样的
批反应器，OGS 的 4 个监测节点结果完全相同。输运照样要算（而且不应改变任何东西）。
但柱子并不是封闭体系：在 `$FLAG_COUPLING_HYDROLOGY 0` 下，OGS 用当前组成的孔隙水补充反应消耗的水，
因此 H、O、Cl、Na 和 K 的总量会增加。模板做同样的处理（`hydrology='none'`）。""")],
'de': [(r"""ersten `#STOP` auf zu lesen, die Säule ist also geschlossen.""", r"""ersten `#STOP` auf zu lesen, über die Ränder gelangt also nichts."""),
(r"""Die Säule ist geschlossen und homogen: jeder Knoten ist derselbe Batch-Reaktor, und die vier
OGS-Beobachtungsknoten liefern identische Ergebnisse. Der Transport wird trotzdem gelöst (und darf nichts ändern).""",
r"""Über die Ränder gelangt nichts, und die Säule ist homogen: jeder Knoten ist derselbe Batch-Reaktor, und die vier
OGS-Beobachtungsknoten liefern identische Ergebnisse. Der Transport wird trotzdem gelöst (und darf nichts ändern).
Ein geschlossenes System ist die Säule aber nicht: Mit `$FLAG_COUPLING_HYDROLOGY 0` ersetzt OGS das von Reaktionen
verbrauchte Wasser durch Porenwasser der aktuellen Zusammensetzung, daher nehmen die Gesamtmengen von H, O, Cl, Na und K
zu. Die Vorlage macht dasselbe (`hydrology='none'`).""")],
}
EDITS['04_comedy2d'] = {
'en': [(r"""With `loose` the change pattern matches OGS node by node (Ca within $1.4\times10^{-4}$, head within $10^{-9}$); with `strict`""",
r"""With `loose` the spatial pattern of the change matches OGS, and the state after 68 s agrees to $1.4\times10^{-4}$ in Ca and $10^{-9}$
in head (maximum difference of the state divided by the maximum of the reference; this is not an error of the change itself); with `strict`""")],
'zh': [(r"""用 `loose` 时变化的空间分布和 OGS 逐节点吻合（Ca 差 $1.4\times10^{-4}$ 以内，水头差 $10^{-9}$ 以内）；""",
r"""用 `loose` 时变化量的空间分布与 OGS 一致，68 s 后的状态 Ca 差在 $1.4\times10^{-4}$ 以内、水头差在 $10^{-9}$ 以内（状态的最大差除以参考解的最大值，不是变化量本身的误差）；""")],
'de': [(r"""Mit `loose` stimmt das Änderungsmuster Knoten für Knoten mit OGS überein (Ca innerhalb $1.4\times10^{-4}$, Druckhöhe innerhalb $10^{-9}$);""",
r"""Mit `loose` entspricht das räumliche Muster der Änderung dem von OGS, und der Zustand nach 68 s stimmt in Ca auf $1.4\times10^{-4}$ und in der
Druckhöhe auf $10^{-9}$ überein (größte Abweichung des Zustands, geteilt durch das Maximum der Referenz; kein Fehler der Änderung selbst);""")],
}
EDITS['05_concretecrack'] = {
'en': [(r"""— a node-by-node head comparison is meaningless here.""",
r"""— the current head comparison cannot distinguish the implementation variants and does not confirm that the flow part is verified.""")],
'zh': [(r"""——这里逐节点比较水头没有意义。""", r"""——当前水头比较不足以区分各实现方案，也不能确认流动部分已通过验证。""")],
'de': [(r"""— ein knotengenauer Vergleich der Druckhöhe ist hier sinnlos.""",
r"""— der vorliegende Vergleich der Druckhöhe kann die Implementierungsvarianten nicht unterscheiden und bestätigt nicht, dass der Strömungsteil verifiziert ist.""")],
}

EDITS['01_hayekit'] = {
'en': [(r"""7. **Open question:** for $\Delta t \to 0$ the porosity still differs by about 3 % from the analytical
   solution (spatial resolution? non-reacting boundary nodes? assumptions of the analytical solution?).""",
r"""7. **Open:** the result depends on the time step; convergence to the analytical solution is not shown (see above).""")],
'zh': [(r"""7. **没解决的问题：** $\Delta t \to 0$ 时孔隙率和解析解仍差约 3 %（空间分辨率？边界节点不反应？解析解的假设？）。""",
r"""7. **未解决：** 结果随时间步变化，未证明收敛到解析解（见上）。""")],
'de': [(r"""7. **Offene Frage:**""", r"""7. **Offene Frage:**""")],
}
