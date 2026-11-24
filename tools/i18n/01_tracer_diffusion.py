ZH = [
r"""
# 1. 第一次运行：示踪剂扩散

**问题。** 代码的输运部分能否正确求解扩散？怎样运行一个算例、怎样读它的输出？

## 物理问题

一根 10 mm 长的多孔材料柱完全被水饱和。开始时孔隙水中没有示踪剂。从 $t = 0$ 起，左端接触浓度 $c = 1$ mol/m³ 的溶液，右端接触 $c = 0$ 的溶液。示踪剂只通过扩散进入柱子：没有反应、没有水流，材料本身也不变化。

## 模型假设

- 一种不反应的示踪剂，没有化学（不调用 GEMS）；
- 孔隙饱和，孔隙率 φ = 0.4 和有效扩散系数 $D_e = 4\times10^{-10}$ m²/s 都不变；
- 没有水流，输运只有扩散：$\phi\,\partial c/\partial t = \partial_x (D_e\,\partial_x c)$；
- 两端浓度固定（Dirichlet 边界）。

在这些假设下问题有精确解，所以它可以用来做检验。

## 从假设到 `case.yaml`

| 假设 | `case.yaml` 中的键 |
|---|---|
| 没有化学，一种示踪剂 | `coupling.mode: diffusion`、`transport.components: [tracer]` |
| 初始孔隙水不含示踪剂 | `transport.initial: {tracer: 0.0}` |
| φ 和 $D_e$ 不变 | `transport.material`、`update_porosity: false`、`update_diffusivity: false` |
| 两端浓度固定 | `boundary.left/right.type: dirichlet` 加 `concentrations` |
| 10 mm、50 个单元、20 000 s、步长 100 s | `geometry`、`coupling.time` |

第一个代码单元会自动找到 `FEniCSx_GEMS` 文件夹（无论 notebook 在仓库中的哪个位置打开），并在它旁边的 `tutorial_runs/` 文件夹中工作：

```text
FEniCSx_GEMS/                       四个模块 + chemistry_data/
tutorial_runs/t01_tracer/case.yaml  下面写出
tutorial_runs/t01_tracer/results/   运行时创建
```
""",
r"""
## 写输入文件

`case.yaml` 始终是同样的四节，每节对应一个 Python 模块。diffusion 模式只读取 `transport`、`coupling` 和 `output`；`chemistry` 必须存在，但不使用。

下面单元格中的 `%%writefile` 会把内容写进文件。在 notebook 之外，直接用文本编辑器修改 `case.yaml` 即可。
""",
r"""
## 运行

在 `tutorial_runs/` 目录的终端中就是 `python ../FEniCSx_GEMS/coupling.py t01_tracer/case.yaml`。`!{PY}` 这一行用 notebook 自己的 Python 运行同一条命令。
""",
r"""
## 运行写出了什么

所有文件都写入 `output.folder`。`summary.txt` 说明运行是 COMPLETED 还是 FAILED，并列出最大的守恒误差。
""",
r"""
## 与解析解比较

当 $\phi$ 和 $D_e$ 不变时，方程就是普通扩散，孔隙扩散系数 $D = D_e/\phi = 10^{-9}$ m²/s。对 $c(0,t)=1$、$c(L,t)=0$、$c(x,0)=0$：

$$
c(x,t) = 1-\frac{x}{L}-\frac{2}{\pi}\sum_{n=1}^{\infty}\frac{1}{n}\sin\frac{n\pi x}{L}\,
\exp\!\left(-\frac{n^2\pi^2 D t}{L^2}\right)
$$

`profiles.csv` 中每个单元、每个保存时刻一行。示踪剂浓度在 `tracer_c_mol_m3_water` 列（mol/m³ 孔隙水）；`tracer_total_mol_m3_bulk` 是同一量按体相体积计。
""",
r"""
**怎样读这个结果。** 与精确解的最大差约 $10^{-3}$ mol/m³，即边界值的 0.1 %。两种近似都有贡献：时间上一阶的向后欧拉，以及空间上每个单元一个值。要知道哪一种占主导，就一次只改一样：先固定网格把 `dt` 减半，再固定 `dt` 把 `cells` 加倍。

## 质量守恒

代码每一步都检查：柱中的量只因穿过边界的量而变化。`mass_balance.csv` 中有存量（每 m² 截面的 mol）、累计边界输入以及两者之差。运行正常时，这个差保持在舍入误差水平（这里约 $10^{-17}$ mol/m²），两条曲线重合。
""",
r"""
## 改一个假设：封闭右端

现在右端改为封闭，而不是固定在 $c = 0$。物理上，示踪剂再也不能离开柱子，所以柱子会慢慢被充满，直到全部孔隙水都达到 $c = 1$。在 `case.yaml` 中只需改两行：

```yaml
    right:
      type: no_flux
...
output:
  folder: results_noflux
```

notebook 用 `yaml` 完成修改，并计算到 100 000 s；此时封闭端已达到约 0.9 mol/m³。图中只画出保存的 20 条剖面中的 4 条。
""",
r"""
## 这篇教程说明了什么

- 在这套网格和时间步下，输运求解器复现精确扩散解的精度约为 0.1 %，质量守恒闭合到舍入误差。
- 边界类型按预期改变物理行为：用 `no_flux` 时柱子被充满，而不是形成线性剖面。
- 它没有检验化学、水流或孔隙率变化，这些在后面的教程中出现。

**下一篇：** [教程 2](02_single_equilibrium.ipynb) 打开 GEMS，计算一次化学平衡。
"""]

DE = [
r"""
# 1. Erster Lauf: Tracer-Diffusion

**Frage.** Löst der Transportteil des Codes die Diffusion richtig, und wie rechnet man einen Fall und liest seine Ausgabe?

## Das physikalische Problem

Eine 10 mm lange Säule aus porösem Material ist vollständig wassergesättigt. Anfangs enthält das Porenwasser keinen Tracer.
Ab $t = 0$ berührt das linke Ende eine Lösung mit $c = 1$ mol/m³, das rechte eine Lösung mit $c = 0$. Der Tracer dringt nur
durch Diffusion in die Säule ein. Nichts reagiert, nichts strömt, und das Material ändert sich nicht.

## Modellannahmen

- ein nicht reaktiver Tracer, keine Chemie (GEMS wird nicht aufgerufen);
- gesättigte Poren, konstante Porosität φ = 0,4 und konstanter effektiver Diffusionskoeffizient $D_e = 4\times10^{-10}$ m²/s;
- keine Strömung, Transport nur durch Diffusion: $\phi\,\partial c/\partial t = \partial_x (D_e\,\partial_x c)$;
- beide Enden auf fester Konzentration (Dirichlet-Ränder).

Unter diesen Annahmen hat das Problem eine exakte Lösung; deshalb taugt es als Test.

## Von den Annahmen zu `case.yaml`

| Annahme | Schlüssel in `case.yaml` |
|---|---|
| keine Chemie, ein Tracer | `coupling.mode: diffusion`, `transport.components: [tracer]` |
| Porenwasser anfangs ohne Tracer | `transport.initial: {tracer: 0.0}` |
| φ und $D_e$ konstant | `transport.material`, `update_porosity: false`, `update_diffusivity: false` |
| feste Konzentration an beiden Enden | `boundary.left/right.type: dirichlet` mit `concentrations` |
| 10 mm, 50 Zellen, 20 000 s in Schritten von 100 s | `geometry`, `coupling.time` |

Die erste Codezelle findet den Ordner `FEniCSx_GEMS`, egal wo im Repository das Notebook geöffnet wird, und arbeitet in einem Ordner
`tutorial_runs/` daneben:

```text
FEniCSx_GEMS/                       die vier Module + chemistry_data/
tutorial_runs/t01_tracer/case.yaml  wird unten geschrieben
tutorial_runs/t01_tracer/results/   entsteht beim Lauf
```
""",
r"""
## Die Eingabedatei schreiben

`case.yaml` hat immer dieselben vier Abschnitte, einen pro Python-Modul. Im Modus diffusion werden nur `transport`, `coupling` und `output` gelesen;
`chemistry` muss vorhanden sein, wird aber nicht verwendet.

Die Zeile `%%writefile` unten schreibt die Zelle in eine Datei. Außerhalb eines Notebooks bearbeiten Sie `case.yaml` einfach im Texteditor.
""",
r"""
## Rechnen

Im Terminal in `tutorial_runs/` lautet der Befehl `python ../FEniCSx_GEMS/coupling.py t01_tracer/case.yaml`.
Die Zeile `!{PY}` führt denselben Befehl im Notebook aus, mit dem Python des Notebooks.
""",
r"""
## Was der Lauf geschrieben hat

Alles landet in `output.folder`. `summary.txt` sagt, ob der Lauf COMPLETED oder FAILED ist, und nennt die größten Erhaltungsfehler.
""",
r"""
## Vergleich mit der analytischen Lösung

Bei konstantem $\phi$ und $D_e$ ist die Gleichung gewöhnliche Diffusion mit dem Porendiffusionskoeffizienten $D = D_e/\phi = 10^{-9}$ m²/s.
Für $c(0,t)=1$, $c(L,t)=0$ und $c(x,0)=0$:

$$
c(x,t) = 1-\frac{x}{L}-\frac{2}{\pi}\sum_{n=1}^{\infty}\frac{1}{n}\sin\frac{n\pi x}{L}\,
\exp\!\left(-\frac{n^2\pi^2 D t}{L^2}\right)
$$

`profiles.csv` hat eine Zeile pro Zelle und gespeicherter Zeit. Die Tracerkonzentration steht in der Spalte `tracer_c_mol_m3_water`
(mol/m³ Porenwasser); `tracer_total_mol_m3_bulk` ist dieselbe Menge pro Gesamtvolumen.
""",
r"""
**So liest man das.** Die größte Abweichung von der exakten Lösung beträgt etwa $10^{-3}$ mol/m³, also 0,1 % des Randwerts. Zwei
Näherungen tragen bei: das implizite Euler-Verfahren erster Ordnung in der Zeit und ein Wert pro Zelle im Ort. Um herauszufinden, welche
überwiegt, ändern Sie jeweils nur eine: `dt` halbieren bei festem Gitter, dann `cells` verdoppeln bei festem `dt`.

## Massenbilanz

Der Code prüft in jedem Schritt, dass sich die Menge in der Säule nur um das ändert, was über die Ränder ging. `mass_balance.csv` enthält das Inventar
(mol pro m² Querschnitt), den kumulierten Randeintrag und ihre Differenz. In einem gesunden Lauf bleibt die Differenz auf Rundungsniveau (hier etwa
$10^{-17}$ mol/m²), und die beiden Kurven liegen übereinander.
""",
r"""
## Eine Annahme ändern: geschlossenes rechtes Ende

Jetzt wird das rechte Ende verschlossen, statt es auf $c = 0$ zu halten. Physikalisch kann kein Tracer mehr die Säule verlassen; sie sollte sich also
langsam füllen, bis das ganze Porenwasser bei $c = 1$ liegt. In `case.yaml` ist das eine Änderung von zwei Zeilen:

```yaml
    right:
      type: no_flux
...
output:
  folder: results_noflux
```

Das Notebook nimmt die Änderung mit `yaml` vor und rechnet bis 100 000 s; dann hat das geschlossene Ende etwa 0,9 mol/m³ erreicht.
Gezeigt werden nur vier der 20 gespeicherten Profile.
""",
r"""
## Was dieses Tutorial zeigt

- Der Transportlöser reproduziert die exakte Diffusionslösung mit diesem Gitter und Zeitschritt auf etwa 0,1 %, und die Massenbilanz schließt auf Rundungsniveau.
- Ein Randtyp ändert die Physik wie erwartet: Mit `no_flux` füllt sich die Säule, statt ein lineares Profil zu erreichen.
- Chemie, Strömung und Porositätsänderungen werden hier nicht geprüft; sie folgen in den nächsten Tutorials.

**Weiter:** [Tutorial 2](02_single_equilibrium.ipynb) schaltet GEMS ein und berechnet ein chemisches Gleichgewicht.
"""]
