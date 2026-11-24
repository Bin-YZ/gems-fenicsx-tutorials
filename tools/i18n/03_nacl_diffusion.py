ZH = [
r"""
# 3. NaCl 扩散：第一次耦合运行

**问题。** 在最简单的化学条件下，完整的耦合循环（输运 → 每个单元的 GEMS → 质量守恒检查）能否复现已知结果？

## 物理问题

一根 20 mm 的自由溶液柱。左半部分是 1 M NaCl，右半部分是 0.5 M NaCl，两者在 x = 10 mm 处接触。两端各自与装有本侧溶液的储液接触。盐从浓侧向稀侧扩散。没有固相，因此没有沉淀或溶解，观察时间也很短（100 s）。

## 模型假设

- 饱和的自由溶液：φ = 1，没有固相（`solid_phases: []`），孔隙率不变；
- 所有元素（Na、Cl、H、O）用 **同一个** 扩散系数输运，即二元盐扩散系数 $D_\text{salt}$（见下文）；
- 输运中不含电迁移项和活度梯度；每一步之后 GEMS 在每个单元计算物种分布和 pH；
- 两端分别固定为本侧半段的平衡溶液。

## 从假设到 `case.yaml`

| 假设 | `case.yaml` 中的键 |
|---|---|
| 两种溶液并排 | `transport.zones`（`high`、`low`），`chemistry.initial` 中每个分区一个配方 |
| 两端各自固定为本侧溶液 | `chemistry.inlet: {left: high, right: low}`，边界为 `dirichlet` |
| 没有固相，φ 不变 | `solid_phases: []`、`material.phi: 1.0`、反馈关闭 |
| 一个扩散系数 | `material.De: 1.611e-09` |
| 每一步都有输运和化学 | `coupling.mode: coupled`、`dt: 1`、`end: 100` |

| | |
|---|---|
| 算例文件夹 | `FEniCSx_GEMS/example/demo_NaCl_diffusion`（本 notebook 在其中运行） |
| 区域 | 20 mm，200 个单元，100 s，`dt` = 1 s |
| 运行时间 | 约 5 s |
""",
r"""
## 输入文件
""",
r"""
与 [教程 2](02_single_equilibrium.ipynb) 相比有三处变化：

```yaml
chemistry:
  initial:                 # 每个分区一个配方，而不是一个配方
    high: {Cl: 0.981, H: 108.9, Na: 0.981, O: 54.47}
    low:  {Cl: 0.495, H: 109.8, Na: 0.495, O: 54.90}
  inlet: {left: high, right: low}
transport:
  zones:
    - {name: high, from: 0.0,  to: 0.01}
    - {name: low,  from: 0.01, to: 0.02}
coupling:
  mode: coupled
```

分区没有给出自己的 `phi` 或 `De`，所以都使用 `material` 中的值，这里是 φ = 1 的自由溶液。

### 为什么这里用一个扩散系数

Na⁺ 和 Cl⁻ 单独扩散的速度不同（$D_\text{Na} = 1.334\times10^{-9}$，$D_\text{Cl} = 2.032\times10^{-9}$ m²/s）。在溶液中，电中性使两种离子一起移动。对单一的 1:1 盐，在没有电流、按理想稀溶液处理（通量中忽略活度系数）的条件下，Nernst–Planck 方程化为以盐扩散系数表示的 Fick 定律：

$$
D_\text{salt} = \frac{2 D_\text{Na} D_\text{Cl}}{D_\text{Na} + D_\text{Cl}} = 1.611\times10^{-9}\ \text{m}^2/\text{s},
$$

这就是文件中的 `De`。在这些假设下，用这一个系数输运所有元素，得到的盐通量与 Nernst–Planck 相同。对于含不同离子的混合盐，这并不精确；1 M 时 $D_\text{salt}$ 随浓度的变化也被忽略了。
""",
r"""
## 运行
""",
r"""
## 与解析解比较

两个分别为 $c_H$ 和 $c_L$ 的半无限区域给出 $c(x,t) = \tfrac{c_H+c_L}{2} - \tfrac{c_H-c_L}{2}\,\mathrm{erf}\!\big((x-x_0)/2\sqrt{Dt}\big)$。100 s 内锋面展宽不到 1 mm，所以 10 mm 外的固定端没有影响。
""",
r"""
**怎样读这个结果。** 与 erf 解的最大差为 1 M 浓度的 0.43 %。因为解析解和代码用的是同一个 $D_\text{salt}$，这个数衡量的是耦合循环的数值误差（0.1 mm 的单元、一阶时间步），而不是 Na–Cl 扩散的物理。Na 和 Cl 处处相等，这正是电中性所要求的；如果两者出现差异，就说明有问题。

这里化学步几乎什么也没改变，只是重新计算溶液的物种分布。这正是本例的目的：在一个答案已知的问题上，把包括每个单元的 GEMS 计算和质量守恒检查在内的耦合循环完整跑通一遍。

## GEMS 带来了什么：pH 和水

每个元素都参与输运，包括水中的 H 和 O。GEMS 在每个单元重新计算溶液，因此 pH 和水量都由输运后的总量决定。
""",
r"""
1 M 溶液每升含水略少于 0.5 M 溶液，因为盐占据了体积。H 和 O 的输运把这一差异连同盐一起带走。

## 这篇教程说明了什么

- 在化学不会改变答案的情况下，耦合循环以 0.4 % 的精度复现 erf 解，Na 和 Cl 保持平衡。
- 用分区和两侧不同的边界溶液，可以让柱子从两种不同的水开始。
- 它没有检验与固相的反应，也没有检验单一扩散系数这个假设本身（解析解和代码用的是同一个 $D_\text{salt}$）。

**下一篇：** [教程 4](04_cement_leaching.ipynb) 加入矿物，它们会随溶液变化而溶解。
"""]

DE = [
r"""
# 3. NaCl-Diffusion: der erste gekoppelte Lauf

**Frage.** Reproduziert die vollständige gekoppelte Schleife (Transport → GEMS in jeder Zelle → Massenbilanz) ein bekanntes Ergebnis, mit der
einfachsten Chemie, die es gibt?

## Das physikalische Problem

Eine 20 mm lange Säule aus freier Lösung. Die linke Hälfte enthält 1 M NaCl, die rechte 0,5 M NaCl; beide treffen bei x = 10 mm aufeinander. Jedes
Ende steht mit einem Reservoir seiner eigenen Lösung in Kontakt. Das Salz diffundiert von der starken zur schwachen Seite. Es gibt keine Feststoffe, also
wird nichts gefällt oder gelöst, und die Beobachtungszeit (100 s) ist kurz.

## Modellannahmen

- gesättigte freie Lösung: φ = 1, keine Feststoffe (`solid_phases: []`), Porosität konstant;
- jedes Element (Na, Cl, H, O) wird mit **einem** Diffusionskoeffizienten transportiert, dem binären Salzkoeffizienten $D_\text{salt}$ (siehe unten);
- kein Elektromigrationsterm und keine Aktivitätsgradienten im Transport; GEMS berechnet nach jedem Schritt Speziation und pH in jeder Zelle;
- beide Enden auf der Gleichgewichtslösung ihrer eigenen Hälfte.

## Von den Annahmen zu `case.yaml`

| Annahme | Schlüssel in `case.yaml` |
|---|---|
| zwei Lösungen nebeneinander | `transport.zones` (`high`, `low`) und ein Rezept pro Zone in `chemistry.initial` |
| jedes Ende auf seiner eigenen Lösung | `chemistry.inlet: {left: high, right: low}` mit `dirichlet`-Rändern |
| keine Feststoffe, φ konstant | `solid_phases: []`, `material.phi: 1.0`, Rückkopplung aus |
| ein Diffusionskoeffizient | `material.De: 1.611e-09` |
| Transport und Chemie in jedem Schritt | `coupling.mode: coupled`, `dt: 1`, `end: 100` |

| | |
|---|---|
| Fallordner | `FEniCSx_GEMS/example/demo_NaCl_diffusion` (dieses Notebook läuft dort) |
| Gebiet | 20 mm, 200 Zellen, 100 s mit `dt` = 1 s |
| Laufzeit | etwa 5 s |
""",
r"""
## Die Eingabedatei
""",
r"""
Gegenüber [Tutorial 2](02_single_equilibrium.ipynb) ändern sich drei Dinge:

```yaml
chemistry:
  initial:                 # ein Rezept pro Zone statt eines Rezepts
    high: {Cl: 0.981, H: 108.9, Na: 0.981, O: 54.47}
    low:  {Cl: 0.495, H: 109.8, Na: 0.495, O: 54.90}
  inlet: {left: high, right: low}
transport:
  zones:
    - {name: high, from: 0.0,  to: 0.01}
    - {name: low,  from: 0.01, to: 0.02}
coupling:
  mode: coupled
```

Die Zonen haben kein eigenes `phi` oder `De` und verwenden daher `material`, hier freie Lösung mit φ = 1.

### Warum hier ein Diffusionskoeffizient verwendet wird

Na⁺ und Cl⁻ diffundieren allein unterschiedlich schnell ($D_\text{Na} = 1{,}334\times10^{-9}$, $D_\text{Cl} = 2{,}032\times10^{-9}$ m²/s).
In Lösung zwingt die Elektroneutralität beide Ionen, sich gemeinsam zu bewegen. Für ein einzelnes 1:1-Salz, ohne elektrischen Strom und bei ideal
verdünntem Verhalten (Aktivitätskoeffizienten in den Flüssen vernachlässigt), werden die Nernst–Planck-Gleichungen zum Fickschen Gesetz mit dem Salzkoeffizienten

$$
D_\text{salt} = \frac{2 D_\text{Na} D_\text{Cl}}{D_\text{Na} + D_\text{Cl}} = 1{,}611\times10^{-9}\ \text{m}^2/\text{s},
$$

dem `De` in der Datei. Unter diesen Annahmen ergibt der Transport aller Elemente mit diesem einen Koeffizienten denselben Salzfluss wie Nernst–Planck.
Für Salzgemische mit verschiedenen Ionen ist das nicht exakt, und die Konzentrationsabhängigkeit von $D_\text{salt}$ bei 1 M wird vernachlässigt.
""",
r"""
## Rechnen
""",
r"""
## Vergleich mit der analytischen Lösung

Zwei Halbräume mit $c_H$ und $c_L$ ergeben $c(x,t) = \tfrac{c_H+c_L}{2} - \tfrac{c_H-c_L}{2}\,\mathrm{erf}\!\big((x-x_0)/2\sqrt{Dt}\big)$.
In 100 s verbreitert sich die Front um weniger als 1 mm; die festen Enden 10 mm entfernt spielen keine Rolle.
""",
r"""
**So liest man das.** Die größte Abweichung von der erf-Lösung beträgt 0,43 % der 1-M-Konzentration. Da Lösung und Code dasselbe $D_\text{salt}$
verwenden, misst das den numerischen Fehler der gekoppelten Schleife (0,1-mm-Zellen, Zeitschritt erster Ordnung), nicht die Physik der Na–Cl-Diffusion.
Na und Cl bleiben überall gleich, wie es die Elektroneutralität verlangt; ein Unterschied zwischen ihnen würde auf ein Problem hinweisen.

Der Chemieschritt ändert hier fast nichts: Er berechnet nur die Speziation der Lösung neu. Genau das ist der Zweck dieses Falls: Die gekoppelte Schleife,
einschließlich GEMS in jeder Zelle und der Prüfung der Massenbilanz, läuft einmal vollständig an einem Problem mit bekannter Lösung.

## Was GEMS beiträgt: pH und das Wasser

Jedes Element wird transportiert, auch H und O des Wassers. GEMS berechnet die Lösung in jeder Zelle neu, pH und Wassermenge folgen also aus den transportierten Gesamtmengen.
""",
r"""
Die 1-M-Lösung enthält pro Liter etwas weniger Wasser als die 0,5-M-Lösung, weil das Salz Volumen einnimmt. Der Transport von H und O trägt diesen Unterschied mit dem Salz weiter.

## Was dieses Tutorial zeigt

- Die gekoppelte Schleife reproduziert die erf-Lösung auf 0,4 %, wenn die Chemie die Antwort nicht ändern kann, und Na und Cl bleiben im Gleichgewicht.
- Zonen und seitenweise Randlösungen lassen eine Säule mit zwei verschiedenen Wässern beginnen.
- Reaktionen mit Feststoffen werden nicht geprüft, ebenso wenig die Annahme eines einzigen Koeffizienten selbst (Lösung und Code verwenden dasselbe $D_\text{salt}$).

**Weiter:** [Tutorial 4](04_cement_leaching.ipynb) fügt Minerale hinzu, die sich lösen, wenn sich die Lösung ändert.
"""]
