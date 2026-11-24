ZH = [
r"""
# 2. 单点化学平衡

**问题。** 对给定的材料 GEMS 算出什么？怎样在 `case.yaml` 中描述这种材料？在长时间的耦合计算之前怎样检查一个配方？

## 物理问题

一小块水化水泥浆体：每 dm³ 含 1.12 mol Ca、0.31 mol Si、半升水和痕量 Cl。平衡时它含哪些矿物？孔隙水是什么成分、pH 是多少？接着问：如果浆体含更多二氧化硅，矿物和 pH 怎样变化？

## 模型假设

- 封闭样品：没有物质进出，没有输运，也没有时间；
- 25 °C、1 bar 下的完全热力学平衡（没有动力学）；
- 相、物种和溶液模型取自 GEMS 项目；只报告 CSHQ、portlandite 和无定形硅；
- 两个标准 Gibbs 能修正为该体系所来自的基准算例中的值。

## 从假设到 `case.yaml`

| 假设 | `case.yaml` 中的键 |
|---|---|
| 一次平衡，没有网格和时间 | `coupling.mode: chemistry` |
| 化学体系 | `chemistry.project`（GEMS 文件） |
| 25 °C、1 bar | `chemistry.temperature: 298.15`、`pressure: 100000` |
| 样品组成 | `chemistry.initial`（每 dm³ 体相材料的 mol） |
| 要报告的矿物 | `chemistry.solid_phases` |
| 修正的 Gibbs 能 | `chemistry.gibbs` |

`transport` 和 `coupling` 仍必须存在；这种模式下只用到 `transport.material.phi`，用来把溶解量换算成孔隙水浓度。
""",
r"""
## GEMS 项目里有什么？

GEMS-Selektor 把一个化学体系导出为四个文件：

| 文件 | 内容 |
|---|---|
| `*-dat.lst` | 另外三个文件的列表，`chemistry.project` 指向它 |
| `*-dch.json` / `.dat` | 化学数据：元素、物种、相、热力学数据 |
| `*-ipm.json` / `.dat` | 求解器的数值设置 |
| `*-dbr-0-0000.json` / `.dat` | 一个示例状态（温度、压力、总组成） |

`case.yaml` 中的名称必须与这些文件中的名称完全一致，包括大小写。浏览器页面 [GEMS Chemistry Inspector](../tools/inspector.md) 不用 Python 就能显示它们；在 Python 中用 `xgems` 可以直接列出：
""",
r"""
- **元素** 是参与输运的量，也是配方中要写的名称。`Zz` 是电荷，从不输运，也不需要赋值。
- **相**：`aq_gen` 是水溶液，填入 `chemistry.aqueous_phase`。你想跟踪的固相写进 `chemistry.solid_phases`：它们的量会写入输出，在后面的教程中它们的体积还会参与孔隙率更新。
""",
r"""
## 写输入文件

这个配方是一种水化水泥浆体：每 dm³ **体相**（孔隙水 + 固相）含 1.119 mol Ca 和 0.310 mol Si，以及 0.5 dm³ 水。量是元素总量，不是氧化物；H 和 O 包含水。
""",
r"""
这里的 `transport` 和 `coupling` 用 YAML 的紧凑写法 `{key: value}`，与教程 1 中的缩进写法含义完全相同。
""",
r"""
## 读取结果

chemistry 模式下 `profiles.csv` 只有一行。单位：

- `*_total_mol_m3_bulk`：配方 ×1000（mol/dm³ → mol/m³），代码内部用 mol/m³ 计算。
- `*_c_mol_m3_water`：溶解浓度，每 m³ **孔隙水** 的 mol，使用 `transport.material.phi`。
- `<phase>_mol_m3_bulk`：`solid_phases` 中每个相的 mol 数。
""",
r"""
**怎样读这个结果。** pH 12.45，portlandite 约 605 mol/m³：浆体被 portlandite 饱和，由它缓冲 pH。大部分 Si 结合在 C-S-H 中，无定形硅不稳定。这是水化波特兰水泥浆体的常见矿物组合，说明配方和相名是自洽的。

在耦合计算中使用配方之前，检查两项：

- `summary.txt` 中的 **化学元素重建误差**（GEMS 重现配方的精度，这里约 10⁻¹¹ mol/m³）应在舍入误差水平；
- **水相体积/孔隙率不匹配**：GEMS 用自己的数据计算溶液体积，并与 `phi` 比较。所附算例中约为零点几个百分点，这是观察值，不是可接受阈值；若数值很大，说明配方的含水量与 `transport.material` 中设置的孔隙率不一致。
""",
r"""
## 扫描配方：更多二氧化硅，更低的 Ca/Si

配方很容易修改，所以也很容易探索。这里保持 Ca 和水不变，加入 SiO₂（每 mol Si 同时加 2 mol O），体相 Ca/Si 从 3.7 降到 0.5。每个取值都是用 `mode: chemistry` 独立计算的一次平衡。

注意这个扫描是什么、不是什么：它是一系列组成不同的封闭样品。真实的溶蚀中是 Ca *离开* 浆体，路径不同；但体相 Ca/Si 同样在下降，所以这里的矿物组合顺序是有用的参考。
""",
r"""
**怎样读这个结果。** 随着 Ca/Si 降低出现三个区：

- Ca/Si 高于约 1.5：有 portlandite，pH 固定在 12.45；
- 约 1.5 到 0.65 之间：portlandite 消失，C-S-H 吸收加入的 Si，pH 从 12.3 降到约 10；
- 低于约 0.65：C-S-H 无法再吸收 Si，无定形硅沉淀，pH 保持在 9.8 左右。

在教程 4 的耦合溶蚀中，前两个阶段表现为 portlandite 溶解锋面以及锋面后方的脱钙区。

## `gibbs` 修正有什么作用？

`chemistry.gibbs` 只在 **内存中** 覆盖指定物种的标准摩尔 Gibbs 能 $G^\circ$（J/mol），不修改 GEMS 文件。本例使用的是其来源基准算例中的值。去掉这些修正后，同一配方给出的溶液不同：
""",
r"""
去掉修正后，pH 变化 0.015，溶解 Ca 变化约 5 %。所以在与基准算例做定量比较时，$G^\circ$ 的微小变化也很重要。除非有这样的理由需要改动数据库，否则用 `gibbs: {}`。

## 这篇教程说明了什么

- `mode: chemistry` 约一秒就算出一个配方的平衡；在耦合计算之前用它检查名称、单位和矿物组合。
- 配方是每 dm³ 体相材料中的元素量，包括水；GEMS 返回矿物、孔隙水和 pH。
- 随 Ca/Si 降低的相序（portlandite → 只有 C-S-H → C-S-H + 二氧化硅）是水泥溶蚀背后的化学。

**下一篇：** [教程 3](03_nacl_diffusion.ipynb) 用 `mode: coupled` 让两种 NaCl 溶液相互扩散：每一步都有输运和化学。
"""]

DE = [
r"""
# 2. Ein chemisches Gleichgewicht

**Frage.** Was berechnet GEMS für ein gegebenes Material, wie beschreibt man dieses Material in `case.yaml`, und wie prüft man ein Rezept vor einem
langen gekoppelten Lauf?

## Das physikalische Problem

Eine kleine Probe hydratisierter Zementpaste: Pro dm³ enthält sie 1,12 mol Ca, 0,31 mol Si, einen halben Liter Wasser und eine Spur Cl. Welche Minerale
enthält sie im Gleichgewicht, wie ist ihr Porenwasser zusammengesetzt, und welcher pH stellt sich ein? Und dann: Wie ändern sich Minerale und pH, wenn die
Paste mehr Kieselsäure enthält?

## Modellannahmen

- eine geschlossene Probe: nichts tritt ein oder aus, kein Transport und keine Zeit;
- vollständiges thermodynamisches Gleichgewicht bei 25 °C und 1 bar (keine Kinetik);
- Phasen, Spezies und Lösungsmodelle sind die des GEMS-Projekts; berichtet werden nur CSHQ, Portlandit und amorphes SiO₂;
- zwei Standard-Gibbs-Energien werden auf die Werte des Benchmarks gesetzt, aus dem das System stammt.

## Von den Annahmen zu `case.yaml`

| Annahme | Schlüssel in `case.yaml` |
|---|---|
| ein Gleichgewicht, kein Gitter, keine Zeit | `coupling.mode: chemistry` |
| das chemische System | `chemistry.project` (die GEMS-Dateien) |
| 25 °C, 1 bar | `chemistry.temperature: 298.15`, `pressure: 100000` |
| Zusammensetzung der Probe | `chemistry.initial` (mol pro dm³ Gesamtmaterial) |
| zu berichtende Minerale | `chemistry.solid_phases` |
| angepasste Gibbs-Energien | `chemistry.gibbs` |

`transport` und `coupling` müssen trotzdem vorhanden sein; in diesem Modus wird nur `transport.material.phi` verwendet, um gelöste Mengen in
Porenwasserkonzentrationen umzurechnen.
""",
r"""
## Was steckt in einem GEMS-Projekt?

GEMS-Selektor exportiert ein chemisches System als vier Dateien:

| Datei | Inhalt |
|---|---|
| `*-dat.lst` | Liste der anderen drei Dateien; darauf zeigt `chemistry.project` |
| `*-dch.json` / `.dat` | chemische Daten: Elemente, Spezies, Phasen, thermodynamische Daten |
| `*-ipm.json` / `.dat` | numerische Einstellungen des Lösers |
| `*-dbr-0-0000.json` / `.dat` | ein Beispielzustand (Temperatur, Druck, Gesamtzusammensetzung) |

Namen in `case.yaml` müssen genau den Namen in diesen Dateien entsprechen, einschließlich Groß-/Kleinschreibung. Die Browserseite
[GEMS Chemistry Inspector](../tools/inspector.md) zeigt sie ohne Python; in Python listet `xgems` sie direkt auf:
""",
r"""
- **Elemente** werden transportiert und in Rezepten angegeben. `Zz` ist die Ladung; sie wird nie transportiert und braucht keinen Wert.
- **Phasen**: `aq_gen` ist die wässrige Lösung und wird `chemistry.aqueous_phase`. Die Feststoffe, die Sie verfolgen wollen, kommen in
  `chemistry.solid_phases`: Ihre Mengen werden ausgegeben, und ihre Volumina gehen in späteren Tutorials in die Porositätsänderung ein.
""",
r"""
## Die Eingabedatei schreiben

Das Rezept ist eine hydratisierte Zementpaste: 1,119 mol Ca und 0,310 mol Si pro dm³ **Gesamtmaterial** (Porenwasser + Feststoffe), mit 0,5 dm³ Wasser.
Die Mengen sind ganze Elemente, keine Oxide; H und O enthalten das Wasser.
""",
r"""
Die Blöcke `transport` und `coupling` stehen hier in der kompakten YAML-Form `{key: value}`. Sie bedeutet genau dasselbe wie die eingerückte Form in Tutorial 1.
""",
r"""
## Das Ergebnis lesen

Im Modus chemistry hat `profiles.csv` genau eine Zeile. Einheiten:

- `*_total_mol_m3_bulk`: das Rezept ×1000 (mol/dm³ → mol/m³); intern rechnet der Code in mol/m³.
- `*_c_mol_m3_water`: gelöste Konzentration, mol pro m³ **Porenwasser**, mit `transport.material.phi`.
- `<phase>_mol_m3_bulk`: Mol jeder Phase aus `solid_phases`.
""",
r"""
**So liest man das.** pH 12,45 mit etwa 605 mol/m³ Portlandit: Die Paste ist mit Portlandit gesättigt, der den pH puffert. Der größte Teil des Si ist
in C-S-H gebunden, amorphes SiO₂ ist nicht stabil. Das ist der übliche Mineralbestand einer hydratisierten Portlandzementpaste; Rezept und Phasennamen
sind also stimmig.

Zwei Prüfungen, bevor ein Rezept in einem gekoppelten Lauf verwendet wird:

- der **Rekonstruktionsfehler der Elemente** in `summary.txt` (wie genau GEMS das Rezept reproduziert; hier etwa 10⁻¹¹ mol/m³) sollte auf Rundungsniveau liegen;
- die **Abweichung zwischen Lösungsvolumen und Porosität**: GEMS berechnet das Volumen der Lösung aus seinen eigenen Daten und vergleicht es mit `phi`.
  In den mitgelieferten Beispielen sind es einige Zehntelprozent; das ist eine Beobachtung, keine Akzeptanzschwelle. Ein großer Wert bedeutet, dass der
  Wassergehalt des Rezepts nicht zur Porosität in `transport.material` passt.
""",
r"""
## Das Rezept variieren: mehr Kieselsäure, kleineres Ca/Si

Ein Rezept ist leicht zu ändern und damit leicht zu erkunden. Hier bleiben Ca und das Wasser fest, und SiO₂ wird zugegeben (pro mol Si auch 2 mol O);
das Ca/Si des Materials sinkt von 3,7 auf 0,5. Jeder Wert ist ein unabhängiges Gleichgewicht mit `mode: chemistry`.

Was dieser Scan ist und was nicht: eine Reihe geschlossener Proben unterschiedlicher Zusammensetzung. Bei echter Auslaugung *verlässt* Ca die Paste; der Weg
ist ein anderer, aber auch dort sinkt das Ca/Si, daher ist die Abfolge der Mineralbestände ein nützlicher Anhaltspunkt.
""",
r"""
**So liest man das.** Mit sinkendem Ca/Si erscheinen drei Bereiche:

- Ca/Si über etwa 1,5: Portlandit ist vorhanden und hält den pH bei 12,45;
- zwischen etwa 1,5 und 0,65: Portlandit ist verschwunden, C-S-H nimmt das zugegebene Si auf, und der pH fällt von 12,3 auf etwa 10;
- unter etwa 0,65: C-S-H kann kein Si mehr aufnehmen, amorphes SiO₂ fällt aus; der pH bleibt bei etwa 9,8.

Bei der gekoppelten Auslaugung in Tutorial 4 erscheinen die ersten beiden Stufen als Lösungsfront des Portlandits und als entkalkende Zone dahinter.

## Was bewirken die `gibbs`-Anpassungen?

`chemistry.gibbs` überschreibt die molare Standard-Gibbs-Energie $G^\circ$ (J/mol) der genannten Spezies **nur im Speicher**; die GEMS-Dateien bleiben unverändert.
Dieses Beispiel verwendet die Werte des Benchmarks, aus dem es stammt. Ohne sie ergibt dasselbe Rezept eine andere Lösung:
""",
r"""
Ohne die Anpassungen ändert sich der pH um 0,015 und gelöstes Ca um etwa 5 %. Kleine Änderungen von $G^\circ$ sind also für einen quantitativen Vergleich mit
einem Benchmark wichtig. Verwenden Sie `gibbs: {}`, außer Sie haben einen solchen Grund, die Datenbank zu ändern.

## Was dieses Tutorial zeigt

- `mode: chemistry` berechnet ein Gleichgewicht eines Rezepts in etwa einer Sekunde; damit prüft man Namen, Einheiten und Mineralbestand vor einem gekoppelten Lauf.
- Rezepte sind Elementmengen pro dm³ Gesamtmaterial, einschließlich des Wassers; GEMS liefert Minerale, Porenwasser und pH.
- Die Phasenabfolge mit sinkendem Ca/Si (Portlandit → nur C-S-H → C-S-H + SiO₂) ist die Chemie hinter der Zementauslaugung.

**Weiter:** [Tutorial 3](03_nacl_diffusion.ipynb) lässt mit `mode: coupled` zwei NaCl-Lösungen ineinander diffundieren: Transport und Chemie in jedem Schritt.
"""]
