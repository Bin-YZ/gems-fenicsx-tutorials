ZH = [
r"""
# 4. 水泥溶蚀

**问题。** 水化水泥浆体的表面长期接触低钙的水时会怎样劣化？耦合代码能否复现这一过程的已发表基准？

## 物理问题

一块 4 mm 厚的水化水泥浆体，材料与 [教程 2](02_single_equilibrium.ipynb) 相同：含 portlandite 和 C-S-H，孔隙水 pH 12.45。它的左表面一直与大量含 14.6 mM CaCl₂ 的地下水接触（pH 约 7.6），右表面密封。在 1000 年中：

- Ca 从浆体向低钙水中扩散，Cl 向浆体内扩散；
- portlandite 最先溶解，从表面向内推进，形成一个向浆体内部移动的锋面；
- 锋面后方的 C-S-H 失去 Ca，pH 下降。

## 模型假设

- 孔隙饱和，只有扩散输运，所有元素共用一个有效扩散系数；
- 每个单元、每一步都达到局部平衡（没有动力学）；相和数据取自教程 2 的 GEMS 项目，并采用基准算例的 Gibbs 能修正；
- 接触的水始终不变（Dirichlet 边界）：假设储液体积很大、混合均匀；
- **在基准计算中，即使矿物溶解，φ 和 De 也保持不变**，这是基准算例的简化。第二次计算中打开反馈。

## 从假设到 `case.yaml`

| 假设 | `case.yaml` 中的键 |
|---|---|
| 浆体 | `chemistry.initial`（与教程 2 相同的配方）、`material.phi: 0.5` |
| 参与反应并报告的矿物 | `chemistry.solid_phases: [CSHQ, Portlandite, Silica-amorph]` |
| 接触水，1000 年不变 | `chemistry.inlet`（14.6 mM CaCl₂），左边界 `dirichlet` |
| 背面密封 | 右边界 `no_flux` |
| 基准的扩散系数 | `material.De: 5.0e-15` = $\phi D_p$，其中 $D_p = 10^{-14}$ m²/s |
| φ 和 De 不变（基准） | `update_porosity: false`、`update_diffusivity: false` |
| 1000 年，步长 0.1 年 | `coupling.time`（以秒为单位） |

| | |
|---|---|
| 算例文件夹 | `FEniCSx_GEMS/example/demo_Cement_1D_benchmark`（本 notebook 在其中运行） |
| 区域 | 4 mm，40 个单元，10 000 步 |
| 运行时间 | 每次 3–5 分钟；400 000 次 GEMS 平衡 |
| 参考 | 同一基准算例的 HYDRUS 剖面 `Profile_HYDRUS.out` |
""",
r"""
关于这些数字：

- `project: ../../chemistry_data/b_time0-dat.lst`：本例使用主文件夹中的 GEMS 项目，与教程 2 相同。
- `dt: 3155760` s 即 0.1 年。$D_p\,\Delta t/h^2 \approx 3$，显式格式会不稳定，向后欧拉则不会；但稳定不等于准确，这个时间步是基准算例的选择，这里没有检验。
- `every: 1000` 表示每 100 年写一次剖面。

## 运行

每 1000 步打印一次进度。
""",
r"""
## 溶蚀后的剖面

矿物量的单位是每 m³ 体相的 mol；除以 1000 即为 mol/dm³。
""",
r"""
**怎样读这个结果。** portlandite 在表面附近一个随时间扩大的区域内消失，区域边缘很陡，这就是溶解锋面。锋面后方 pH 从约 12.5 降到 12 以下，C-S-H 失去 Ca，与教程 2 中的 Ca/Si 扫描一致。自己运行时检查两项：`summary.txt` 中的质量守恒保持在舍入误差水平，且没有报告 GEMS 失败或被跳过的单元。

## 与 HYDRUS 基准比较

`Profile_HYDRUS.out` 中所有量都按每 dm³ 体相给出，因此需要换算模型输出：

$$
X_\text{aq} = \frac{\phi\,c_X}{1000},\qquad X_\text{s} = \frac{\text{total}_X - \phi\,c_X}{1000},\qquad
\text{Ca}_\text{ss} = \text{Ca}_\text{s} - \text{Portlandite}
$$
""",
r"""
粗线是 HYDRUS，虚线是本模型。两个代码给出的 portlandite 锋面位置相差约一个单元（0.1 mm）以内。表中是浆体内部参考节点上、按各列单位计的均方根差；x = 0 处的节点不计入，因为参考结果在那里存的是边界水本身（pH 7.6），而本模型的第一个值位于第一个单元中心。

剩余差异从哪里来？可能的原因有：不同的网格（参考结果在节点上存值，包括边界节点；这里边界距第一个单元中心半个单元）、不同的输运格式和时间步进，以及 GEMS 舍入误差。这里没有把这些原因分开；要分开，需要对两个代码都做网格和时间步加密。

如果溶蚀受扩散控制，锋面位置应按 $\sqrt{t}$ 增长，即在下图中落在一条直线上：
""",
r"""
## 改一个假设：孔隙率和扩散系数反馈

基准算例中 φ 和 De 固定。物理上，portlandite 溶解会腾出孔隙空间，更开放的孔隙结构使溶质扩散更快。打开反馈改变了两个模型假设：

- φ 现在随 `solid_phases` 中矿物的体积变化：$\phi = \phi_0 + V_\text{solid,0} - V_\text{solid}$；
- De 按一个假定的关系随 φ 变化：$D_e = D_{e,0}(\phi/\phi_0)^m$，$m = 2$。指数是模型选择，不是这种浆体的实测性质。

在 `case.yaml` 中改两行即可打开反馈。我们另存一份，并使用新的输出文件夹：

```yaml
coupling:
  update_porosity: true      # phi = phi0 + V_solid0 - V_solid
  update_diffusivity: true   # De = De0 (phi/phi0)^2
output:
  folder: results_feedback
```
""",
r"""
**怎样读这个结果。** 溶解使表面附近的 φ 从 0.50 升到约 0.55，De 按 $(\phi/\phi_0)^2$ 增大约 20 %。这里对锋面的影响很小，而且与预期相反：portlandite 锋面比性质不变时 *落后* 约 0.1 mm。一个可能的原因是 portlandite 只占体积的百分之几，φ 变化不大，而溶蚀区现在容纳了更多孔隙水；这一点没有进一步检验。这个结果说明，这类反馈应该通过计算来检查，而不是想当然。

## 这篇教程说明了什么

- 耦合代码给出了预期的溶蚀顺序（portlandite 锋面、C-S-H 脱钙、pH 下降），1000 年内锋面位置与 HYDRUS 基准相差约一个单元。
- 打开孔隙率–扩散系数反馈会改变模型假设，它的影响需要计算评估，不能靠猜。
- 它没有说明是哪些数值选择造成了与 HYDRUS 的剩余差异，也没有说明反馈关系是否符合真实的浆体。

**下一篇：** [教程 5](05_calcite_dolomite.ipynb) 加入水流。
"""]

DE = [
r"""
# 4. Zementauslaugung

**Frage.** Wie degradiert eine hydratisierte Zementpaste, deren Oberfläche lange mit calciumarmem Wasser in Kontakt steht, und reproduziert der
gekoppelte Code einen veröffentlichten Benchmark dieses Vorgangs?

## Das physikalische Problem

Eine 4 mm dicke Platte aus hydratisierter Zementpaste, dasselbe Material wie in [Tutorial 2](02_single_equilibrium.ipynb): Portlandit und C-S-H,
Porenwasser bei pH 12,45. Ihre linke Seite steht dauerhaft mit einem großen Volumen Grundwasser mit 14,6 mM CaCl₂ (pH etwa 7,6) in Kontakt; die rechte
Seite ist versiegelt. Über 1000 Jahre:

- Ca diffundiert aus der Paste in das calciumarme Wasser, Cl diffundiert hinein;
- zuerst löst sich Portlandit, von der Oberfläche nach innen, und hinterlässt eine Front, die in die Paste wandert;
- hinter dieser Front verliert C-S-H Ca, und der pH fällt.

## Modellannahmen

- gesättigte Poren, Transport nur durch Diffusion, ein effektiver Diffusionskoeffizient für alle Elemente;
- lokales Gleichgewicht in jeder Zelle und jedem Schritt (keine Kinetik); Phasen und Daten aus dem GEMS-Projekt von Tutorial 2, mit den Gibbs-Energie-Anpassungen des Benchmarks;
- das Kontaktwasser ändert sich nie (Dirichlet-Rand): Das Reservoir wird als groß und gut durchmischt angenommen;
- **im Benchmark-Lauf bleiben φ und De konstant**, obwohl sich Minerale lösen; das ist die Vereinfachung des Benchmarks. Im zweiten Lauf wird die Rückkopplung eingeschaltet.

## Von den Annahmen zu `case.yaml`

| Annahme | Schlüssel in `case.yaml` |
|---|---|
| die Paste | `chemistry.initial` (gleiches Rezept wie Tutorial 2), `material.phi: 0.5` |
| reagierende und berichtete Minerale | `chemistry.solid_phases: [CSHQ, Portlandite, Silica-amorph]` |
| Kontaktwasser, 1000 Jahre unverändert | `chemistry.inlet` (14,6 mM CaCl₂), linker Rand `dirichlet` |
| versiegelte Rückseite | rechter Rand `no_flux` |
| Diffusionskoeffizient des Benchmarks | `material.De: 5.0e-15` = $\phi D_p$ mit $D_p = 10^{-14}$ m²/s |
| φ und De konstant (Benchmark) | `update_porosity: false`, `update_diffusivity: false` |
| 1000 Jahre in Schritten von 0,1 Jahr | `coupling.time` (in Sekunden) |

| | |
|---|---|
| Fallordner | `FEniCSx_GEMS/example/demo_Cement_1D_benchmark` (dieses Notebook läuft dort) |
| Gebiet | 4 mm, 40 Zellen, 10 000 Schritte |
| Laufzeit | 3–5 min pro Lauf; 400 000 GEMS-Gleichgewichte |
| Referenz | HYDRUS-Profile desselben Benchmarks, `Profile_HYDRUS.out` |
""",
r"""
Zu den Zahlen:

- `project: ../../chemistry_data/b_time0-dat.lst`: Dieser Fall verwendet das GEMS-Projekt im Hauptordner, dasselbe wie Tutorial 2.
- `dt: 3155760` s sind 0,1 Jahre. Mit $D_p\,\Delta t/h^2 \approx 3$ wäre ein explizites Verfahren instabil, das implizite Euler-Verfahren nicht; Stabilität sagt
  aber nichts über Genauigkeit. Der Zeitschritt ist die Wahl des Benchmarks und wird hier nicht geprüft.
- `every: 1000` schreibt alle 100 Jahre ein Profil.

## Rechnen

Der Fortschritt wird alle 1000 Schritte ausgegeben.
""",
r"""
## Das ausgelaugte Profil

Mineralmengen sind in mol pro m³ Gesamtvolumen; durch 1000 geteilt ergibt mol/dm³.
""",
r"""
**So liest man das.** Portlandit verschwindet in einer mit der Zeit wachsenden Zone an der Oberfläche, deren Rand scharf ist: eine Lösungsfront. Dahinter
fällt der pH von etwa 12,5 auf unter 12, und C-S-H verliert Ca, wie im Ca/Si-Scan von Tutorial 2. Zwei Dinge sind im eigenen Lauf zu prüfen: Die Massenbilanz in
`summary.txt` bleibt auf Rundungsniveau, und es werden keine GEMS-Fehler oder übersprungenen Zellen gemeldet.

## Vergleich mit dem HYDRUS-Benchmark

`Profile_HYDRUS.out` gibt alles pro dm³ Gesamtmaterial an, deshalb wird die Modellausgabe umgerechnet:

$$
X_\text{aq} = \frac{\phi\,c_X}{1000},\qquad X_\text{s} = \frac{\text{total}_X - \phi\,c_X}{1000},\qquad
\text{Ca}_\text{ss} = \text{Ca}_\text{s} - \text{Portlandit}
$$
""",
r"""
Dicke Linien sind HYDRUS, gestrichelte dieses Modell. Beide Codes setzen die Portlanditfront bis auf etwa eine Zelle (0,1 mm) an dieselbe Stelle. Die Tabelle gibt die
RMS-Abweichung an den Referenzknoten innerhalb der Paste, in den Einheiten jeder Spalte. Der Knoten bei x = 0 fehlt, weil die Referenz dort das Randwasser selbst speichert (pH 7,6),
während der erste Wert dieses Modells im Mittelpunkt der ersten Zelle liegt.

Woher kommen die verbleibenden Unterschiede? Mögliche Ursachen sind die verschiedenen Gitter (die Referenz speichert Werte an Knoten, einschließlich des Randknotens; hier liegt
der Rand eine halbe Zelle vom ersten Zellmittelpunkt entfernt), die verschiedenen Transportverfahren und Zeitschritte sowie Rundung in GEMS. Diese Ursachen wurden hier nicht
getrennt; dazu wäre eine Gitter- und Zeitschrittverfeinerung beider Codes nötig.

Wird die Auslaugung durch Diffusion kontrolliert, sollte die Frontlage mit $\sqrt{t}$ wachsen, also im Bild unten auf einer Geraden liegen:
""",
r"""
## Eine Annahme ändern: Rückkopplung von Porosität und Diffusivität

Der Benchmark hält φ und De fest. Physikalisch schafft sich lösender Portlandit Porenraum, und ein offeneres Porengefüge lässt gelöste Stoffe schneller diffundieren.
Das Einschalten der Rückkopplung ändert zwei Modellannahmen:

- φ folgt nun dem Volumen der Minerale in `solid_phases`: $\phi = \phi_0 + V_\text{solid,0} - V_\text{solid}$;
- De folgt φ über ein angenommenes Gesetz, $D_e = D_{e,0}(\phi/\phi_0)^m$ mit $m = 2$. Der Exponent ist eine Modellwahl, keine gemessene Eigenschaft dieser Paste.

Zwei Zeilen in `case.yaml` schalten das ein. Wir schreiben eine Kopie mit neuem Ausgabeordner:

```yaml
coupling:
  update_porosity: true      # phi = phi0 + V_solid0 - V_solid
  update_diffusivity: true   # De = De0 (phi/phi0)^2
output:
  folder: results_feedback
```
""",
r"""
**So liest man das.** Die Lösung erhöht φ nahe der Oberfläche von 0,50 auf etwa 0,55, und De steigt mit $(\phi/\phi_0)^2$ um etwa 20 %. Die Wirkung auf die Front ist
hier klein und geht in die unerwartete Richtung: Die Portlanditfront liegt etwa 0,1 mm *hinter* dem Lauf mit konstanten Eigenschaften. Ein möglicher Grund ist, dass
Portlandit nur wenige Prozent des Volumens füllt, φ sich also wenig ändert, während die ausgelaugte Zone nun mehr Porenwasser enthält; das wurde nicht weiter geprüft. Das
Ergebnis zeigt, warum man solche Rückkopplungen mit einem Lauf prüfen und nicht annehmen sollte.

## Was dieses Tutorial zeigt

- Der gekoppelte Code liefert die erwartete Auslaugungsabfolge (Portlanditfront, Entkalkung von C-S-H, pH-Abfall) und setzt die Front über 1000 Jahre bis auf etwa eine Zelle
  an dieselbe Stelle wie der HYDRUS-Benchmark.
- Das Einschalten der Rückkopplung Porosität–Diffusivität ändert die Annahmen des Modells; ihre Wirkung muss berechnet, nicht geraten werden.
- Es zeigt nicht, welche numerischen Entscheidungen die verbleibenden Unterschiede zu HYDRUS verursachen, und nicht, ob das Rückkopplungsgesetz zu einer realen Paste passt.

**Weiter:** [Tutorial 5](05_calcite_dolomite.ipynb) fügt Strömung hinzu.
"""]
