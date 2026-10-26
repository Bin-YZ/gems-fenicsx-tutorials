ZH = [r"""
# 4. 水泥溶蚀

**目标。** 在柱中放入矿物并让它们反应。4 mm 的水化水泥浆体与 CaCl₂ 水接触 1000 年：Ca 向外扩散，portlandite 从表面向内溶解，锋面后方的 C-S-H 脱钙。这正是 [教程 2 中 Ca/Si 扫描](02_single_equilibrium.ipynb) 的顺序，只是现在随深度变化。

`case.yaml` 中的新内容：

- 含真实矿物的 **`solid_phases`**，以及取自基准算例的 `gibbs` 修正；
- **一个 `inlet` 配方**，用于左侧 `dirichlet` 边界；右侧边界为 `no_flux`；
- **长时间尺度**：`dt` = 0.1 年，`end` = 1000 年，都以秒为单位；
- **反馈开关**：基准算例保持 φ 和 De 不变，最后我们把它们打开。

| | |
|---|---|
| 模式 | `coupled` |
| 算例文件夹 | `FEniCSx_GEMS/example/demo_Cement_1D_benchmark`（本 notebook 在其中运行） |
| 区域 | 4 mm，40 个单元，10 000 步 |
| 运行时间 | 每次约 5 min；400 000 次 GEMS 平衡 |
| 参考 | 同一基准算例的 HYDRUS 剖面 `Profile_HYDRUS.out` |
""", r"""
关于这些数字：

- `project: ../../chemistry_data/b_time0-dat.lst`：本例使用主文件夹中的 GEMS 项目，与教程 2 相同。
- `De: 5.0e-15` 是 $\phi D_p$，其中基准算例的孔隙扩散系数 $D_p = 10^{-14}$ m²/s。
- `dt: 3155760` s 即 0.1 年。$D_p\,\Delta t/h^2 \approx 3$，显式格式会不稳定，向后欧拉则不会。
- `every: 1000` 表示每 100 年写一次剖面。

## 运行

每 1000 步打印一次进度。
""", r"""
## 溶蚀后的剖面

矿物量的单位是每 m³ 体相的 mol；除以 1000 即为 mol/dm³。
""", r"""
portlandite 在表面附近一个不断扩大的区域内消失，锋面很陡；锋面后方 pH 从约 12.5 降到 12 以下，C-S-H 失去 Ca。

## 与 HYDRUS 基准比较

`Profile_HYDRUS.out` 中所有量都按每 dm³ 体相给出，因此需要换算模型输出：

$$
X_\text{aq} = \frac{\phi\,c_X}{1000},\qquad X_\text{s} = \frac{\text{total}_X - \phi\,c_X}{1000},\qquad
\text{Ca}_\text{ss} = \text{Ca}_\text{s} - \text{Portlandite}
$$
""", r"""
粗线是 HYDRUS，虚线是本模型。两个代码给出的 portlandite 锋面位置相差约一个单元（0.1 mm）以内。表中是浆体内部参考节点上、按各列单位计的均方根差；x = 0 处的节点不计入，因为参考结果在那里存的是边界水本身（pH 7.6），而本模型的第一个值位于第一个单元中心。剩余差异来自不同的网格（参考结果在节点上存值，包括边界节点；这里边界距第一个单元中心半个单元）、时间步进和 GEMS 舍入误差。

在扩散控制下，锋面按 $\sqrt{t}$ 推进：
""", r"""
## 打开孔隙率和扩散系数反馈

基准算例中 φ 和 De 保持不变。实际上 portlandite 溶解会使孔隙变大，溶蚀区内扩散变快。在 `case.yaml` 中改两行即可打开反馈。我们另存一份，并使用新的输出文件夹：

```yaml
coupling:
  update_porosity: true      # phi = phi0 + V_solid0 - V_solid
  update_diffusivity: true   # De = De0 (phi/phi0)^2
output:
  folder: results_feedback
```
""", r"""
溶解使表面附近的 φ 从 0.50 升到约 0.55，De 按 $(\phi/\phi_0)^2$ 增大约 20 %。这里对锋面的影响很小，而且与直觉相反：portlandite 锋面比性质不变时 *落后* 约 0.1 mm。portlandite 只占体积的百分之几，所以 φ 变化不大，而溶蚀区现在也容纳了更多孔隙水。这类效应应该通过计算来检查，而不是想当然。指数是模型选择，不是浆体本身的性质。

**下一篇：** [教程 5](05_calcite_dolomite.ipynb) 加入流动。
"""]

DE = [r"""
# 4. Zementauslaugung

**Ziel.** Minerale in die Säule bringen und reagieren lassen. Eine 4 mm dicke hydratisierte Zementpaste steht 1000 Jahre in Kontakt mit CaCl₂-Wasser: Ca diffundiert
hinaus, Portlandit löst sich von der Oberfläche nach innen, und hinter der Front entkalkt C-S-H. Das ist die Abfolge des
[Ca/Si-Scans aus Tutorial 2](02_single_equilibrium.ipynb), jetzt als Funktion der Tiefe.

Neu in `case.yaml`:

- **`solid_phases`** mit echten Mineralen und `gibbs`-Anpassungen aus dem Benchmark;
- **ein `inlet`-Rezept** am linken `dirichlet`-Rand und ein `no_flux`-Rand rechts;
- **lange Zeiten**: `dt` = 0,1 Jahr und `end` = 1000 Jahre, beide in Sekunden;
- **Rückkopplungsschalter**: Der Benchmark hält φ und De konstant; am Ende schalten wir sie ein.

| | |
|---|---|
| Modus | `coupled` |
| Fallordner | `FEniCSx_GEMS/example/demo_Cement_1D_benchmark` (dieses Notebook läuft dort) |
| Gebiet | 4 mm, 40 Zellen, 10 000 Schritte |
| Laufzeit | etwa 5 min pro Lauf; 400 000 GEMS-Gleichgewichte |
| Referenz | HYDRUS-Profile desselben Benchmarks, `Profile_HYDRUS.out` |
""", r"""
Zu den Zahlen:

- `project: ../../chemistry_data/b_time0-dat.lst`: Dieser Fall verwendet das GEMS-Projekt im Hauptordner, dasselbe wie Tutorial 2.
- `De: 5.0e-15` ist $\phi D_p$ mit dem Porendiffusionskoeffizienten des Benchmarks $D_p = 10^{-14}$ m²/s.
- `dt: 3155760` s sind 0,1 Jahre. Mit $D_p\,\Delta t/h^2 \approx 3$ wäre ein explizites Verfahren instabil, das implizite Euler-Verfahren nicht.
- `every: 1000` schreibt alle 100 Jahre ein Profil.

## Rechnen

Der Fortschritt wird alle 1000 Schritte ausgegeben.
""", r"""
## Das ausgelaugte Profil

Mineralmengen sind in mol pro m³ Gesamtvolumen; durch 1000 geteilt ergibt mol/dm³.
""", r"""
Portlandit verschwindet in einer wachsenden Zone an der Oberfläche, mit scharfer Front. Dahinter fällt der pH von etwa 12,5 auf unter 12, und C-S-H verliert Ca.

## Vergleich mit dem HYDRUS-Benchmark

`Profile_HYDRUS.out` gibt alles pro dm³ Gesamtmaterial an, deshalb wird die Modellausgabe umgerechnet:

$$
X_\text{aq} = \frac{\phi\,c_X}{1000},\qquad X_\text{s} = \frac{\text{total}_X - \phi\,c_X}{1000},\qquad
\text{Ca}_\text{ss} = \text{Ca}_\text{s} - \text{Portlandit}
$$
""", r"""
Dicke Linien sind HYDRUS, gestrichelte dieses Modell. Beide Codes setzen die Portlanditfront bis auf etwa eine Zelle (0,1 mm) an dieselbe Stelle. Die Tabelle gibt die
RMS-Abweichung an den Referenzknoten innerhalb der Paste, in den Einheiten jeder Spalte. Der Knoten bei x = 0 fehlt, weil die Referenz dort das Randwasser selbst speichert (pH 7,6),
während der erste Wert dieses Modells im Mittelpunkt der ersten Zelle liegt.
Die verbleibenden Unterschiede kommen von den verschiedenen Gittern (die Referenz speichert Werte an Knoten, einschließlich des Randknotens; hier liegt der Rand eine halbe Zelle vom ersten
Zellmittelpunkt entfernt), der Zeitschrittweite und Rundung in GEMS.

Unter Diffusionskontrolle wandert die Front mit $\sqrt{t}$:
""", r"""
## Rückkopplung von Porosität und Diffusivität einschalten

Der Benchmark hält φ und De fest. In Wirklichkeit öffnet sich lösender Portlandit die Poren, und in der ausgelaugten Zone wird die Diffusion schneller. Zwei Zeilen in
`case.yaml` schalten das ein. Wir schreiben eine Kopie mit neuem Ausgabeordner:

```yaml
coupling:
  update_porosity: true      # phi = phi0 + V_solid0 - V_solid
  update_diffusivity: true   # De = De0 (phi/phi0)^2
output:
  folder: results_feedback
```
""", r"""
Die Lösung erhöht φ nahe der Oberfläche von 0,50 auf etwa 0,55, und De steigt mit $(\phi/\phi_0)^2$ um etwa 20 %. Die Wirkung auf die Front ist hier klein und geht in die
unerwartete Richtung: Die Portlanditfront liegt etwa 0,1 mm *hinter* dem Lauf mit konstanten Eigenschaften. Portlandit füllt nur wenige Prozent des Volumens, φ ändert sich also wenig,
und die ausgelaugte Zone enthält nun auch mehr Porenwasser. Solche Effekte mit einem Lauf prüfen, statt sie anzunehmen. Der Exponent ist eine Modellannahme, keine Eigenschaft der Paste.

**Weiter:** [Tutorial 5](05_calcite_dolomite.ipynb) fügt Strömung hinzu.
"""]
