ZH = [
r"""
# 5. 方解石 → 白云石（含对流）

**问题。** 代码怎样处理水流？它能否复现一个已发表的反应运移基准，其中矿物在移动的锋面上溶解和沉淀？

## 物理问题

一根 0.5 m 的多孔材料柱，含少量方解石，孔隙水与方解石平衡。从 $t = 0$ 起，从左端以恒定流量泵入 1 mM 的 MgCl₂ 溶液（孔隙流速约 0.8 m/天），水从右端流出。随着 MgCl₂ 水推进：

- 方解石溶解，释放出 Ca 和碳酸根；
- 碳酸根与 Mg 相遇，**白云石** 在一个条带中沉淀；
- 条带后方流入的水对白云石不饱和，白云石再次溶解，于是条带沿柱向下移动。

这是反应运移代码的标准基准（[doi:10.1007/s10596-019-09919-3](https://doi.org/10.1007/s10596-019-09919-3)，4.4 节，图 6）。

## 模型假设

- 恒定 Darcy 通量的饱和流；φ 和弥散系数不变（没有反馈）；
- 弥散和扩散合并成一个系数，所有元素相同；
- 每个单元、每一步都达到局部平衡（没有动力学）；
- 流入的水始终不变；出口处水以最后一个单元的组成流出（出口没有扩散通量）。

## 从假设到 `case.yaml`

| 假设 | `case.yaml` 中的键 |
|---|---|
| 沿 +x 的恒定 Darcy 通量 | `material.darcy_flux: 3.0e-06` |
| 弥散 + 扩散 | `material.De: 6.432e-09`（= φ × 基准的 $D$） |
| 流入的 MgCl₂ 水 | `chemistry.inlet`，左边界 `dirichlet` |
| 右端流出 | 右边界 `outflow` |
| φ = 0.32 的方解石柱 | `chemistry.initial`（缩放到 φ = 0.32 的 GEMS 状态，[方法](../yaml/from_gems.md)）、`material.phi: 0.32` |
| φ 和 De 不变 | `update_porosity: false`、`update_diffusivity: false` |

| | |
|---|---|
| 算例文件夹 | `FEniCSx_GEMS/example/demo_calcite_dolomite`（本 notebook 在其中运行） |
| 区域 | 0.5 m，1000 个单元，105 步 × 200 s（21 000 s） |
| 运行时间 | 约 25 s |
""",
r"""
### `case.yaml` 中的流动

基准给出孔隙流速 $v = 9.375\times10^{-6}$ m/s 和弥散系数 $D = 2.01\times10^{-8}$ m²/s。代码使用通量形式，两者都要乘以 φ：

$$
q = \phi v = 0.32 \times 9.375\times10^{-6} = 3.0\times10^{-6}\ \text{m/s},\qquad D_e = \phi D = 6.432\times10^{-9}\ \text{m}^2/\text{s}
$$

```yaml
transport:
  material: {phi: 0.32, De: 6.432e-09, darcy_flux: 3.0e-06}
  boundary:
    left:  {type: dirichlet}   # chemistry.inlet 流入
    right: {type: outflow}     # 水流出；扩散梯度为零
```

有流动时左边界必须是 `dirichlet`，右边界为 `outflow` 或 `dirichlet`；其他组合在启动时就会停止。Courant 数为 $q\,\Delta t/(\phi h) = 9.375\times10^{-6}\cdot 200 / 5\times10^{-4} = 3.75$，向后欧拉在此仍然稳定。

### 化学体系中没有 O

项目列出的独立组分是 `C, Ca, Cl, H, Mg, Zz`。水只由 `H` 构成，每个物种的 O 由其他组分决定，再加一行 O 会使化学计量矩阵奇异。因此配方中没有 `O`：项目列出什么名称就写什么。入口水中 C 和 Ca 保持在 1e-9 mol，使 GEMS 始终拥有每种组分的少量。
""",
r"""
## 运行
""",
r"""
## 与论文比较（t = 21 000 s）

左：本模型，按图 6 的版式绘制。右：已发表的图。矿物量按论文的做法从 mol/m³ 体相换算为每 m³ 水的 mol（÷ φ）。
""",
r"""
**怎样读这个结果。** Mg 和 Cl 锋面、方解石溶解锋面以及白云石条带的位置，目视比较时与已发表的图一致；已发表的曲线只有图片，所以没有计算误差。自己运行时检查：Cl 不反应，它的锋面标志着流入的水走了多远（$v t \approx 0.2$ m）；锋面前方的方解石平台应保持初始值（这里为 0.206 mol/m³ 水）；`summary.txt` 中的质量守恒应闭合。

## 条带如何移动
""",
r"""
白云石在 Mg 与正在溶解的方解石相遇处生成。条带后方流入的 MgCl₂ 水对白云石不饱和，白云石再次溶解，于是条带随方解石锋面一起移动。

## 为什么用 1000 个单元？数值弥散

迎风格式在物理 $D_e$ 之外还会增加约 $q h/2$ 的数值弥散。1000 个单元（$h$ = 0.5 mm）时为 $0.75\times10^{-9}$ m²/s，约为 $D_e$ 的 12 %；100 个单元时则是 $D_e$ 的 1.2 倍。改一行就能看到效果：
""",
r"""
**怎样读这个结果。** 用 100 个单元时条带位置不变，只有边缘分布在几个粗单元上。一个可能的原因是平衡化学使矿物锋面保持陡峭，所以这里网格的影响比弥散估计的要小。这只是本例中的观察；其他问题中网格的影响可能很大，要加密网格，直到结果不再变化。

## 这篇教程说明了什么

- 用 `darcy_flux`、`outflow` 边界和平衡化学，复现了基准中移动的溶解锋面和白云石条带（与已发表的图目视比较）。
- GEMS 项目可以用非元素的独立组分（这里没有 O）；配方使用项目列出的名称。
- 迎风输运会带来约 $qh/2$ 的数值弥散；它的影响有多大，要通过加密网格来检查。

现在你已经了解 `case.yaml` 的每一节。[参考页](../yaml/index.md) 列出了其余选项，例如用于难收敛化学的 `start: warm` 和 `on_failure: skip`。
"""]

DE = [
r"""
# 5. Calcit → Dolomit mit Advektion

**Frage.** Wie behandelt der Code Strömung, und reproduziert er einen veröffentlichten Benchmark für reaktiven Transport, in dem Minerale an wandernden Fronten
gelöst und gefällt werden?

## Das physikalische Problem

Eine 0,5 m lange Säule aus porösem Material mit einer kleinen Menge Calcit; ihr Porenwasser steht mit dem Calcit im Gleichgewicht. Ab $t = 0$ wird links mit
konstanter Rate eine 1-mM-MgCl₂-Lösung eingepumpt (Porengeschwindigkeit etwa 0,8 m/Tag), und rechts tritt Wasser aus. Während das MgCl₂-Wasser vordringt:

- löst sich Calcit und setzt Ca und Carbonat frei;
- trifft das Carbonat auf Mg, und **Dolomit** fällt in einem Band aus;
- ist das nachströmende Wasser hinter dem Band an Dolomit untersättigt, der sich wieder löst; so wandert das Band die Säule hinab.

Das ist ein Standard-Benchmark für Codes des reaktiven Transports ([doi:10.1007/s10596-019-09919-3](https://doi.org/10.1007/s10596-019-09919-3), Abschnitt 4.4, Abb. 6).

## Modellannahmen

- gesättigte Strömung mit konstantem Darcy-Fluss; φ und Dispersionskoeffizient bleiben konstant (keine Rückkopplung);
- Dispersion und Diffusion in einem Koeffizienten zusammengefasst, für alle Elemente gleich;
- lokales Gleichgewicht in jeder Zelle und jedem Schritt (keine Kinetik);
- das zuströmende Wasser ändert sich nie; am Auslass tritt Wasser mit der Zusammensetzung der letzten Zelle aus (kein diffusiver Fluss darüber).

## Von den Annahmen zu `case.yaml`

| Annahme | Schlüssel in `case.yaml` |
|---|---|
| konstanter Darcy-Fluss in +x-Richtung | `material.darcy_flux: 3.0e-06` |
| Dispersion + Diffusion | `material.De: 6.432e-09` (= φ × $D$ des Benchmarks) |
| zuströmendes MgCl₂-Wasser | `chemistry.inlet`, linker Rand `dirichlet` |
| Ausstrom am rechten Ende | rechter Rand `outflow` |
| Calcitsäule bei φ = 0,32 | `chemistry.initial` (ein auf φ = 0,32 skalierter GEMS-Zustand, [wie](../yaml/from_gems.md)), `material.phi: 0.32` |
| φ und De konstant | `update_porosity: false`, `update_diffusivity: false` |

| | |
|---|---|
| Fallordner | `FEniCSx_GEMS/example/demo_calcite_dolomite` (dieses Notebook läuft dort) |
| Gebiet | 0,5 m, 1000 Zellen, 105 Schritte zu 200 s (21 000 s) |
| Laufzeit | etwa 25 s |
""",
r"""
### Strömung in `case.yaml`

Der Benchmark gibt eine Porengeschwindigkeit $v = 9{,}375\times10^{-6}$ m/s und einen Dispersionskoeffizienten $D = 2{,}01\times10^{-8}$ m²/s vor. In der Flussform des Codes werden
beide mit φ multipliziert:

$$
q = \phi v = 0{,}32 \times 9{,}375\times10^{-6} = 3{,}0\times10^{-6}\ \text{m/s},\qquad D_e = \phi D = 6{,}432\times10^{-9}\ \text{m}^2/\text{s}
$$

```yaml
transport:
  material: {phi: 0.32, De: 6.432e-09, darcy_flux: 3.0e-06}
  boundary:
    left:  {type: dirichlet}   # Zustrom von chemistry.inlet
    right: {type: outflow}     # Wasser tritt aus; diffusiver Gradient null
```

Mit Strömung muss der linke Rand `dirichlet` und der rechte `outflow` oder `dirichlet` sein; jede andere Kombination bricht beim Start ab. Die Courant-Zahl ist
$q\,\Delta t/(\phi h) = 9{,}375\times10^{-6}\cdot 200 / 5\times10^{-4} = 3{,}75$; das implizite Euler-Verfahren ist dort stabil.

### Das chemische System hat kein O

Das Projekt listet die unabhängigen Komponenten `C, Ca, Cl, H, Mg, Zz`. Wasser wird allein aus `H` gebildet, und der O-Gehalt jeder Spezies folgt aus den übrigen; eine
zusätzliche O-Zeile machte die Stöchiometriematrix singulär. Das Rezept enthält daher kein `O`: Verwenden Sie die Namen, die das Projekt auflistet, welche es auch sind.
Das Zustromwasser hält C und Ca bei 1e-9 mol, damit GEMS immer etwas von jeder Komponente hat.
""",
r"""
## Rechnen
""",
r"""
## Vergleich mit der Veröffentlichung (t = 21 000 s)

Links: dieses Modell im Layout von Abb. 6. Rechts: die veröffentlichte Abbildung. Minerale sind wie in der Veröffentlichung von mol/m³ Gesamtvolumen in mol pro m³ Wasser (÷ φ) umgerechnet.
""",
r"""
**So liest man das.** Die Lage der Mg- und Cl-Fronten, der Calcit-Lösungsfront und des Dolomitbands stimmt beim Vergleich mit dem Auge mit der veröffentlichten Abbildung
überein; die veröffentlichten Kurven liegen nur als Bild vor, daher wird kein Fehler berechnet. Im eigenen Lauf zu prüfen: Cl reagiert nicht, seine Front zeigt also, wie weit das
zuströmende Wasser gekommen ist ($v t \approx 0{,}2$ m); das Calcitplateau vor der Front sollte auf seinem Anfangswert bleiben (hier 0,206 mol/m³ Wasser); und die Massenbilanz in
`summary.txt` sollte schließen.

## Wie das Band wandert
""",
r"""
Dolomit bildet sich dort, wo Mg auf sich lösenden Calcit trifft. Hinter dem Band ist das zuströmende MgCl₂-Wasser an Dolomit untersättigt, der sich wieder löst. So wandert das
Band mit der Calcitfront.

## Warum 1000 Zellen? Numerische Dispersion

Das Upwind-Verfahren fügt zum physikalischen $D_e$ eine numerische Dispersion von etwa $q h/2$ hinzu. Mit 1000 Zellen ($h$ = 0,5 mm) sind das
$0{,}75\times10^{-9}$ m²/s, etwa 12 % von $D_e$; mit 100 Zellen wären es das 1,2-Fache von $D_e$. Eine geänderte Zeile zeigt den Effekt:
""",
r"""
**So liest man das.** Mit 100 Zellen liegt das Band an derselben Stelle; nur seine Ränder verteilen sich über einige grobe Zellen. Ein wahrscheinlicher Grund ist, dass
Gleichgewichtschemie die Mineralfronten scharf hält, sodass das Gitter hier weniger ausmacht, als die Dispersionsabschätzung vermuten lässt. Das ist eine Beobachtung nur für
diesen Fall; bei anderen Problemen kann das Gitter viel ausmachen, daher verfeinern, bis sich das Ergebnis nicht mehr ändert.

## Was dieses Tutorial zeigt

- Advektion mit `darcy_flux`, ein `outflow`-Rand und Gleichgewichtschemie reproduzieren die wandernde Lösungsfront und das Dolomitband des Benchmarks, verglichen mit dem Auge
  an der veröffentlichten Abbildung.
- Ein GEMS-Projekt kann unabhängige Komponenten verwenden, die keine Elemente sind (hier kein O); Rezepte verwenden die Namen, die das Projekt auflistet.
- Upwind-Transport fügt eine numerische Dispersion von etwa $qh/2$ hinzu; wie viel sie ausmacht, muss durch Gitterverfeinerung geprüft werden.

Sie kennen jetzt jeden Abschnitt von `case.yaml`. Die [Referenzseiten](../yaml/index.md) nennen die übrigen Optionen, etwa `start: warm` und `on_failure: skip`
für schwierige Chemie.
"""]
