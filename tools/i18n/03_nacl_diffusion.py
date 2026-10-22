ZH = [r"""
# 3. NaCl 扩散：第一次耦合运行

**目标。** 第一次运行 `mode: coupled`，用最简单的化学：没有任何固相的溶液。两种 NaCl 溶液（1 M 和 0.5 M）在 20 mm 柱的中间相遇并相互扩散。

`case.yaml` 中的新内容：

- **`transport.zones`**：两个分区 `high` 和 `low`，各自在 `chemistry.initial` 中有自己的配方；
- **`chemistry.inlet: {left: high, right: low}`**：两端各自固定为本分区平衡后的孔隙水；
- **`solid_phases: []`**：只有溶液。GEMS 只计算溶液的物种分布，孔隙率保持不变。

| | |
|---|---|
| 模式 | `coupled` |
| 算例文件夹 | `FEniCSx_GEMS/example/demo_NaCl_diffusion`（本 notebook 在其中运行） |
| 区域 | 20 mm，200 个单元，100 s，`dt` = 1 s |
| 运行时间 | 约 5 s |
""", r"""
## 输入文件
""", r"""
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

### 为什么这里一个扩散系数就够了

Na⁺ 和 Cl⁻ 单独扩散的速度不同（$D_\text{Na} = 1.334\times10^{-9}$，$D_\text{Cl} = 2.032\times10^{-9}$ m²/s）。在溶液中，电中性使两种离子一起移动。对 1:1 盐，Nernst–Planck 方程化为以盐扩散系数表示的 Fick 定律：

$$
D_\text{salt} = \frac{2 D_\text{Na} D_\text{Cl}}{D_\text{Na} + D_\text{Cl}} = 1.611\times10^{-9}\ \text{m}^2/\text{s},
$$

这就是文件中的 `De`。代码对所有元素使用同一个系数，所以本例是精确的；对于离子不同的混合盐溶液则不精确。
""", r"""
## 运行
""", r"""
## 与解析解比较

两个分别为 $c_H$ 和 $c_L$ 的半无限区域给出 $c(x,t) = \tfrac{c_H+c_L}{2} - \tfrac{c_H-c_L}{2}\,\mathrm{erf}\!\big((x-x_0)/2\sqrt{Dt}\big)$。100 s 内锋面展宽不到 1 mm，所以 10 mm 外的固定端没有影响。
""", r"""
模型与 erf 解吻合得很好；微小差异来自 0.1 mm 的单元和一阶时间步。这里化学步几乎不起作用，只是重新计算溶液的物种分布。这正是本例的目的：在一个答案已知的问题上，把耦合循环完整跑通一遍。

## GEMS 带来了什么：pH 和水

每个元素都参与输运，包括水中的 H 和 O。GEMS 在每个单元重新计算溶液，因此 pH 和水量都由输运后的总量决定。
""", r"""
1 M 溶液每升含水略少于 0.5 M 溶液，因为盐占据了体积。H 和 O 的输运把这一差异连同盐一起带走。

## 自己试试

1. 给 `low` 分区不同的孔隙率，例如 `{name: low, from: 0.01, to: 0.02, phi: 0.3, De: 3.0e-10}`，观察剖面中的跳跃。
2. 两侧用同一种溶液：`inlet: high`。右端会发生什么？
3. 封闭右端（`type: no_flux`），运行到 `end: 100000`。剖面最终会变成什么样？

**下一篇：** [教程 4](04_cement_leaching.ipynb) 加入矿物，它们会随溶液变化而溶解。
"""]

DE = [r"""
# 3. NaCl-Diffusion: der erste gekoppelte Lauf

**Ziel.** Zum ersten Mal `mode: coupled` rechnen, mit der einfachsten Chemie: einer Lösung ganz ohne Feststoffe. Zwei NaCl-Lösungen (1 M und 0,5 M)
treffen sich in der Mitte einer 20-mm-Säule und diffundieren ineinander.

Neu in `case.yaml`:

- **`transport.zones`**: zwei Zonen, `high` und `low`, jede mit eigenem Rezept in `chemistry.initial`;
- **`chemistry.inlet: {left: high, right: low}`**: Jedes Ende wird auf dem Gleichgewichts-Porenwasser seiner eigenen Zone gehalten;
- **`solid_phases: []`**: nur Lösung. GEMS berechnet nur die Speziation, die Porosität bleibt konstant.

| | |
|---|---|
| Modus | `coupled` |
| Fallordner | `FEniCSx_GEMS/example/demo_NaCl_diffusion` (dieses Notebook läuft dort) |
| Gebiet | 20 mm, 200 Zellen, 100 s mit `dt` = 1 s |
| Laufzeit | etwa 5 s |
""", r"""
## Die Eingabedatei
""", r"""
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

### Warum hier ein Diffusionskoeffizient genügt

Na⁺ und Cl⁻ diffundieren allein unterschiedlich schnell ($D_\text{Na} = 1{,}334\times10^{-9}$, $D_\text{Cl} = 2{,}032\times10^{-9}$ m²/s).
In Lösung zwingt die Elektroneutralität beide Ionen, sich gemeinsam zu bewegen. Für ein 1:1-Salz wird Nernst–Planck dann zum Fickschen Gesetz mit dem Salzkoeffizienten

$$
D_\text{salt} = \frac{2 D_\text{Na} D_\text{Cl}}{D_\text{Na} + D_\text{Cl}} = 1{,}611\times10^{-9}\ \text{m}^2/\text{s},
$$

dem `De` in der Datei. Der Code transportiert alle Elemente mit demselben Koeffizienten; für diesen Fall ist das exakt, für Salzgemische mit verschiedenen Ionen nicht.
""", r"""
## Rechnen
""", r"""
## Vergleich mit der analytischen Lösung

Zwei Halbräume mit $c_H$ und $c_L$ ergeben $c(x,t) = \tfrac{c_H+c_L}{2} - \tfrac{c_H-c_L}{2}\,\mathrm{erf}\!\big((x-x_0)/2\sqrt{Dt}\big)$.
In 100 s verbreitert sich die Front um weniger als 1 mm; die festen Enden 10 mm entfernt spielen keine Rolle.
""", r"""
Das Modell folgt der erf-Lösung eng; die kleinen Abweichungen kommen von den 0,1-mm-Zellen und dem Zeitschritt erster Ordnung. Der Chemieschritt bewirkt hier fast nichts:
Er berechnet nur die Speziation der Lösung neu. Genau das ist der Zweck dieses Falls: Die gekoppelte Schleife läuft einmal komplett durch, an einem Problem mit bekannter Lösung.

## Was GEMS beiträgt: pH und das Wasser

Jedes Element wird transportiert, auch H und O des Wassers. GEMS berechnet die Lösung in jeder Zelle neu, pH und Wassermenge folgen also aus den transportierten Gesamtmengen.
""", r"""
Die 1-M-Lösung enthält pro Liter etwas weniger Wasser als die 0,5-M-Lösung, weil das Salz Volumen einnimmt. Der Transport von H und O trägt diesen Unterschied mit dem Salz weiter.

## Selbst ausprobieren

1. Der Zone `low` eine andere Porosität geben, z. B. `{name: low, from: 0.01, to: 0.02, phi: 0.3, De: 3.0e-10}`, und den Sprung im Profil ansehen.
2. Auf beiden Seiten dieselbe Lösung verwenden: `inlet: high`. Was geschieht am rechten Ende?
3. Das rechte Ende schließen (`type: no_flux`) und bis `end: 100000` rechnen. Wo endet das Profil?

**Weiter:** [Tutorial 4](04_cement_leaching.ipynb) fügt Minerale hinzu, die sich lösen, wenn sich die Lösung ändert.
"""]
