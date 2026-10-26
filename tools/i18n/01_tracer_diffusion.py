ZH = [r"""
# 1. 第一次运行：示踪剂扩散

**目标。** 在不涉及化学的情况下完整运行一次代码。你将：

- 写出含四节的完整 `case.yaml`，
- 用 `coupling.py` 运行它，
- 找到结果文件，
- 用解析解检查结果。

`coupling.mode: diffusion` 会关闭 GEMS，只运行 `transport.py` 和 `output.py`。所以这个算例也能检查 FEniCSx 是否装好了。

| | |
|---|---|
| 模式 | `diffusion` |
| 区域 | 一维，10 mm，50 个单元 |
| 物理 | $\phi\,\partial c/\partial t = \partial_x (D_e\,\partial_x c)$ |
| 运行时间 | 约 2 s |

## 文件夹结构

本 notebook 放在 `FEniCSx_GEMS` 文件夹旁边，每篇教程的算例放在自己的文件夹中：

```text
FEniCSx_GEMS/          四个模块 + chemistry_data/
t01_tracer/case.yaml   下面写出
t01_tracer/results/    运行时创建
```
""", r"""
## 写输入文件

`case.yaml` 始终是同样的四节，每节对应一个 Python 模块。diffusion 模式只读取 `transport`、`coupling` 和 `output`；`chemistry` 必须存在，但不使用。

下面单元格中的 `%%writefile` 会把内容写进文件。在 notebook 之外，直接用文本编辑器修改 `case.yaml` 即可。
""", r"""
## 运行

在终端中就是 `python FEniCSx_GEMS/coupling.py t01_tracer/case.yaml`（Windows 上双击 `Run.cmd`，它调用 WSL 中的 Python）。`!` 在 notebook 中运行同一条命令。
""", r"""
## 运行写出了什么

所有文件都写入 `output.folder`。`summary.txt` 说明运行是 COMPLETED 还是 FAILED，并列出最大的守恒误差。
""", r"""
## 与解析解比较

当 $\phi$ 和 $D_e$ 不变时，方程就是普通扩散，孔隙扩散系数 $D = D_e/\phi = 10^{-9}$ m²/s。对 $c(0,t)=1$、$c(L,t)=0$、$c(x,0)=0$：

$$
c(x,t) = 1-\frac{x}{L}-\frac{2}{\pi}\sum_{n=1}^{\infty}\frac{1}{n}\sin\frac{n\pi x}{L}\,
\exp\!\left(-\frac{n^2\pi^2 D t}{L^2}\right)
$$

`profiles.csv` 中每个单元、每个保存时刻一行。示踪剂浓度在 `tracer_c_mol_m3_water` 列（mol/m³ 孔隙水）；`tracer_total_mol_m3_bulk` 是同一量按体相体积计。
""", r"""
误差约为 $10^{-3}$，来自时间上一阶的向后欧拉和以单元中心存值的网格。把 `dt` 减半或把 `cells` 加倍，误差就会下降。

## 质量守恒

代码每一步都检查：柱中的量只因穿过边界的量而变化。`mass_balance.csv` 中有存量（每 m² 截面的 mol）、累计边界输入以及两者之差。
""", r"""
## 改一处：封闭右端

输入只在 `case.yaml` 中修改。这里载入文件，把右边界改为封闭（`no_flux`），把结果写到另一个文件夹，再运行一次。在文本编辑器中只需改两行：

```yaml
    right:
      type: no_flux
...
output:
  folder: results_noflux
```
""", r"""
**下一篇：** [教程 2](02_single_equilibrium.ipynb) 打开 GEMS，计算一次化学平衡。
"""]

DE = [r"""
# 1. Erster Lauf: Tracer-Diffusion

**Ziel.** Den Code einmal vollständig durchlaufen lassen, ganz ohne Chemie. Sie werden

- eine vollständige `case.yaml` mit ihren vier Abschnitten schreiben,
- `coupling.py` damit starten,
- die Ergebnisdateien finden und
- die Zahlen mit einer analytischen Lösung vergleichen.

`coupling.mode: diffusion` schaltet GEMS ab. Es laufen nur `transport.py` und `output.py`; der Fall zeigt also auch, ob FEniCSx richtig installiert ist.

| | |
|---|---|
| Modus | `diffusion` |
| Gebiet | 1D, 10 mm, 50 Zellen |
| Physik | $\phi\,\partial c/\partial t = \partial_x (D_e\,\partial_x c)$ |
| Laufzeit | etwa 2 s |

## Ordnerstruktur

Dieses Notebook liegt neben dem Ordner `FEniCSx_GEMS`. Jedes Tutorial hat seinen Fall in einem eigenen Ordner:

```text
FEniCSx_GEMS/          die vier Module + chemistry_data/
t01_tracer/case.yaml   wird unten geschrieben
t01_tracer/results/    entsteht beim Lauf
```
""", r"""
## Die Eingabedatei schreiben

`case.yaml` hat immer dieselben vier Abschnitte, einen pro Python-Modul. Im Modus diffusion werden nur `transport`, `coupling` und `output` gelesen;
`chemistry` muss vorhanden sein, wird aber nicht verwendet.

Die Zeile `%%writefile` unten schreibt die Zelle in eine Datei. Außerhalb eines Notebooks bearbeiten Sie `case.yaml` einfach im Texteditor.
""", r"""
## Rechnen

Im Terminal lautet der Befehl `python FEniCSx_GEMS/coupling.py t01_tracer/case.yaml` (unter Windows: Doppelklick auf `Run.cmd`, das das WSL-Python aufruft).
Das `!` führt denselben Befehl im Notebook aus.
""", r"""
## Was der Lauf geschrieben hat

Alles landet in `output.folder`. `summary.txt` sagt, ob der Lauf COMPLETED oder FAILED ist, und nennt die größten Erhaltungsfehler.
""", r"""
## Vergleich mit der analytischen Lösung

Bei konstantem $\phi$ und $D_e$ ist die Gleichung gewöhnliche Diffusion mit dem Porendiffusionskoeffizienten $D = D_e/\phi = 10^{-9}$ m²/s.
Für $c(0,t)=1$, $c(L,t)=0$ und $c(x,0)=0$:

$$
c(x,t) = 1-\frac{x}{L}-\frac{2}{\pi}\sum_{n=1}^{\infty}\frac{1}{n}\sin\frac{n\pi x}{L}\,
\exp\!\left(-\frac{n^2\pi^2 D t}{L^2}\right)
$$

`profiles.csv` hat eine Zeile pro Zelle und gespeicherter Zeit. Die Tracerkonzentration steht in der Spalte `tracer_c_mol_m3_water`
(mol/m³ Porenwasser); `tracer_total_mol_m3_bulk` ist dieselbe Menge pro Gesamtvolumen.
""", r"""
Der Fehler liegt bei etwa $10^{-3}$: implizites Euler-Verfahren erster Ordnung plus zellzentriertes Gitter. Halbieren Sie `dt` oder verdoppeln Sie `cells`, dann sinkt er.

## Massenbilanz

Der Code prüft in jedem Schritt, dass sich die Menge in der Säule nur um das ändert, was über die Ränder ging. `mass_balance.csv` enthält das Inventar
(mol pro m² Querschnitt), den kumulierten Randeintrag und ihre Differenz.
""", r"""
## Eine Sache ändern: geschlossenes rechtes Ende

Eingaben werden nur in `case.yaml` geändert. Hier laden wir die Datei, schließen den rechten Rand (`no_flux`), schreiben die Ergebnisse in einen anderen
Ordner und rechnen erneut. Im Texteditor ist das eine Änderung von zwei Zeilen:

```yaml
    right:
      type: no_flux
...
output:
  folder: results_noflux
```
""", r"""
**Weiter:** [Tutorial 2](02_single_equilibrium.ipynb) schaltet GEMS ein und berechnet ein chemisches Gleichgewicht.
"""]
