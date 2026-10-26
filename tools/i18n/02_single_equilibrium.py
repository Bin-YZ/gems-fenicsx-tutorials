ZH = [r"""
# 2. 单点化学平衡

**目标。** 打开 GEMS，学习 `case.yaml` 中的 `chemistry` 节：

- 可以写哪些名称（元素、相），
- 配方中的数字是什么意思、用什么单位，
- GEMS 返回什么，
- `gibbs` 修正有什么作用。

`coupling.mode: chemistry` 只用 `initial` 配方算一次平衡：不建网格，不走时间步。在开始长时间耦合计算之前，这是检查配方最快的方法。

| | |
|---|---|
| 模式 | `chemistry` |
| 体系 | CaO–SiO₂–H₂O（+Cl），相为 CSHQ、Portlandite、无定形硅 |
| 运行时间 | 每次平衡约 1 s |
""", r"""
## GEMS 项目里有什么？

GEMS-Selektor 把一个化学体系导出为四个文件：

| 文件 | 内容 |
|---|---|
| `*-dat.lst` | 另外三个文件的列表，`chemistry.project` 指向它 |
| `*-dch.json` / `.dat` | 化学数据：元素、物种、相、热力学数据 |
| `*-ipm.json` / `.dat` | 求解器的数值设置 |
| `*-dbr-0-0000.json` / `.dat` | 一个示例状态（温度、压力、总组成） |

`case.yaml` 中的名称必须与这些文件中的名称完全一致，包括大小写。浏览器页面 [GEMS Chemistry Inspector](../tools/inspector.md) 不用 Python 就能显示它们；在 Python 中用 `xgems` 可以直接列出：
""", r"""
- **元素** 是参与输运的量，也是配方中要写的名称。`Zz` 是电荷，从不输运，也不需要赋值。
- **相**：`aq_gen` 是水溶液，填入 `chemistry.aqueous_phase`。你想跟踪的固相写进 `chemistry.solid_phases`：它们的量会写入输出，在后面的教程中它们的体积还会参与孔隙率更新。
""", r"""
## 写输入文件

这个配方是一种水化水泥浆体：每 dm³ **体相**（孔隙水 + 固相）含 1.119 mol Ca 和 0.310 mol Si，以及 0.5 dm³ 水。量是元素总量，不是氧化物；H 和 O 包含水。
""", r"""
这里的 `transport` 和 `coupling` 用 YAML 的紧凑写法 `{key: value}`，与教程 1 中的缩进写法含义完全相同。
""", r"""
## 读取结果

chemistry 模式下 `profiles.csv` 只有一行。单位：

- `*_total_mol_m3_bulk`：配方 ×1000（mol/dm³ → mol/m³），代码内部用 mol/m³ 计算。
- `*_c_mol_m3_water`：溶解浓度，每 m³ **孔隙水** 的 mol，使用 `transport.material.phi`。
- `<phase>_mol_m3_bulk`：`solid_phases` 中每个相的 mol 数。
""", r"""
浆体被 portlandite 饱和（pH ≈ 12.5）；大部分 Si 在 C-S-H 中，无定形硅在这里不稳定。

`summary.txt` 还报告 **水相体积/孔隙率不匹配**：GEMS 用自己的数据计算溶液体积，并与 `phi` 比较。零点几个百分点属于正常；若数值很大，说明配方的含水量与 `transport.material` 中设置的孔隙率不一致。
""", r"""
## 扫描配方：从 portlandite 到二氧化硅

配方很容易修改，所以也很容易探索。这里保持 Ca 和水不变，逐步加入 SiO₂：每加 1 mol Si 同时加 2 mol O。每个取值都是用 `mode: chemistry` 运行同一代码一次。
""", r"""
从左到右，体相的 Ca/Si 逐渐降低，就像浆体因溶蚀失去 Ca 一样。portlandite 最先耗尽，随后 C-S-H 失去 Ca、pH 下降，在 Ca/Si 最低处出现无定形硅。耦合计算（教程 4）会逐个单元经历同样的顺序，因为 Ca 会向外扩散。

## `gibbs` 修正有什么作用？

`chemistry.gibbs` 只在 **内存中** 覆盖指定物种的标准摩尔 Gibbs 能 $G^\circ$（J/mol），不修改 GEMS 文件。本例使用的是其来源基准算例中的值。去掉这些修正后，同一配方给出的溶液不同：
""", r"""
除非有理由（例如复现已发表的基准算例）需要改动数据库，否则用 `gibbs: {}`。

**下一篇：** [教程 3](03_nacl_diffusion.ipynb) 用 `mode: coupled` 让两种 NaCl 溶液相互扩散：每一步都有输运和化学。
"""]

DE = [r"""
# 2. Ein chemisches Gleichgewicht

**Ziel.** GEMS einschalten und den Abschnitt `chemistry` von `case.yaml` kennenlernen:

- welche Namen Sie schreiben dürfen (Elemente, Phasen),
- was die Zahlen eines Rezepts bedeuten und in welcher Einheit sie stehen,
- was GEMS zurückgibt und
- was die `gibbs`-Anpassungen bewirken.

`coupling.mode: chemistry` berechnet genau ein Gleichgewicht mit dem Rezept `initial`: kein Gitter, keine Zeitschritte. Das ist der schnellste Weg,
ein Rezept zu prüfen, bevor ein langer gekoppelter Lauf beginnt.

| | |
|---|---|
| Modus | `chemistry` |
| System | CaO–SiO₂–H₂O (+Cl), Phasen CSHQ, Portlandit, amorphes SiO₂ |
| Laufzeit | etwa 1 s pro Gleichgewicht |
""", r"""
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
""", r"""
- **Elemente** werden transportiert und in Rezepten angegeben. `Zz` ist die Ladung; sie wird nie transportiert und braucht keinen Wert.
- **Phasen**: `aq_gen` ist die wässrige Lösung und wird `chemistry.aqueous_phase`. Die Feststoffe, die Sie verfolgen wollen, kommen in
  `chemistry.solid_phases`: Ihre Mengen werden ausgegeben, und ihre Volumina gehen in späteren Tutorials in die Porositätsänderung ein.
""", r"""
## Die Eingabedatei schreiben

Das Rezept ist eine hydratisierte Zementpaste: 1,119 mol Ca und 0,310 mol Si pro dm³ **Gesamtmaterial** (Porenwasser + Feststoffe), mit 0,5 dm³ Wasser.
Die Mengen sind ganze Elemente, keine Oxide; H und O enthalten das Wasser.
""", r"""
Die Blöcke `transport` und `coupling` stehen hier in der kompakten YAML-Form `{key: value}`. Sie bedeutet genau dasselbe wie die eingerückte Form in Tutorial 1.
""", r"""
## Das Ergebnis lesen

Im Modus chemistry hat `profiles.csv` genau eine Zeile. Einheiten:

- `*_total_mol_m3_bulk`: das Rezept ×1000 (mol/dm³ → mol/m³); intern rechnet der Code in mol/m³.
- `*_c_mol_m3_water`: gelöste Konzentration, mol pro m³ **Porenwasser**, mit `transport.material.phi`.
- `<phase>_mol_m3_bulk`: Mol jeder Phase aus `solid_phases`.
""", r"""
Die Paste ist mit Portlandit gesättigt (pH ≈ 12,5); der größte Teil des Si steckt in C-S-H, amorphes SiO₂ ist hier nicht stabil.

`summary.txt` meldet auch die **Abweichung zwischen Lösungsvolumen und Porosität**: GEMS berechnet das Volumen der Lösung aus seinen eigenen Daten und vergleicht
es mit `phi`. Einige Zehntelprozent sind normal; ein großer Wert bedeutet, dass der Wassergehalt des Rezepts nicht zur Porosität in `transport.material` passt.
""", r"""
## Das Rezept variieren: von Portlandit zu SiO₂

Ein Rezept ist leicht zu ändern und damit leicht zu erkunden. Hier halten wir Ca und das Wasser fest und geben SiO₂ hinzu: pro mol Si auch 2 mol O.
Jeder Wert ist ein Lauf desselben Codes mit `mode: chemistry`.
""", r"""
Von links nach rechts sinkt das Ca/Si des Materials, wie in einer Paste, die durch Auslaugung Ca verliert. Zuerst ist Portlandit aufgebraucht, dann verliert C-S-H Ca und
der pH fällt, und beim niedrigsten Ca/Si erscheint amorphes SiO₂. Ein gekoppelter Lauf (Tutorial 4) durchläuft dieselbe Abfolge Zelle für Zelle, während Ca hinausdiffundiert.

## Was bewirken die `gibbs`-Anpassungen?

`chemistry.gibbs` überschreibt die molare Standard-Gibbs-Energie $G^\circ$ (J/mol) der genannten Spezies **nur im Speicher**; die GEMS-Dateien bleiben unverändert.
Dieses Beispiel verwendet die Werte des Benchmarks, aus dem es stammt. Ohne sie ergibt dasselbe Rezept eine andere Lösung:
""", r"""
Verwenden Sie `gibbs: {}`, außer Sie haben einen Grund, die Datenbank zu ändern, etwa einen veröffentlichten Benchmark nachzurechnen.

**Weiter:** [Tutorial 3](03_nacl_diffusion.ipynb) lässt mit `mode: coupled` zwei NaCl-Lösungen ineinander diffundieren: Transport und Chemie in jedem Schritt.
"""]
