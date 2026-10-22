ZH = [r"""
# 5. 方解石 → 白云石（含对流）

**目标。** 加入流动。MgCl₂ 溶液被泵入 0.5 m 的方解石柱：方解石溶解，释放出的碳酸根与 Mg 相遇，**白云石** 在一个条带中沉淀；该条带沿柱向下移动，并在其后方再次溶解。这是用于比较反应运移代码的基准算例（[doi:10.1007/s10596-019-09919-3](https://doi.org/10.1007/s10596-019-09919-3)，4.4 节，图 6）。

`case.yaml` 中的新内容：

- **`transport.material.darcy_flux`**：沿 $+x$ 的对流；
- 右侧的 **`outflow` 边界**：水以最后一个单元的组成流出；
- **细网格**，因为迎风格式会使锋面变平；
- 独立组分不全是元素的 **GEMS 项目**（没有 `O`）；
- 通过把 GEMS 状态缩放到 φ = 0.32 得到的配方（[方法](../yaml/from_gems.md)）。

| | |
|---|---|
| 模式 | `coupled` |
| 算例文件夹 | `FEniCSx_GEMS/example/demo_calcite_dolomite`（本 notebook 在其中运行） |
| 区域 | 0.5 m，1000 个单元，105 步，每步 200 s |
| 运行时间 | 约 25 s |
""", r"""
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
""", r"""
## 运行
""", r"""
## 与论文比较（t = 21 000 s）

左：本模型，按图 6 的版式绘制。右：已发表的图。矿物量按论文的做法从 mol/m³ 体相换算为每 m³ 水的 mol（÷ φ）。
""", r"""
Mg 和 Cl 锋面、方解石溶解锋面以及白云石条带的位置都与已发表的图一致。

## 条带如何移动
""", r"""
白云石在 Mg 与正在溶解的方解石相遇处生成。条带后方流入的 MgCl₂ 水对白云石不饱和，白云石再次溶解，于是条带随方解石锋面一起移动。

## 为什么用 1000 个单元？数值弥散

迎风格式在物理 $D_e$ 之外还会增加约 $q h/2$ 的数值弥散。1000 个单元（$h$ = 0.5 mm）时为 $0.75\times10^{-9}$ m²/s，约为 $D_e$ 的 12 %；100 个单元时则是 $D_e$ 的 1.2 倍。改一行就能看到效果：
""", r"""
用 100 个单元时条带位置不变，只有边缘分布在几个粗单元上。平衡化学使矿物锋面保持陡峭，所以这里网格的影响比弥散估计的要小。其他问题中影响可能很大：要加密网格，直到结果不再变化。

## 自己试试

1. 把 `darcy_flux` 加倍（`De` 不变）。21 000 s 时条带走了多远？
2. 打开 `update_porosity: true`。按每个 Ca+Mg 计，白云石的摩尔体积比方解石小。φ 会增大还是减小？
3. 设 `dt: 100`，与 `dt: 200` 比较。

现在你已经了解 `case.yaml` 的每一节。[参考页](../yaml/index.md) 列出了其余选项，例如用于难收敛化学的 `start: warm` 和 `on_failure: skip`。
"""]

DE = [r"""
# 5. Calcit → Dolomit mit Advektion

**Ziel.** Strömung hinzufügen. Eine MgCl₂-Lösung wird in eine 0,5 m lange Calcitsäule gepumpt. Calcit löst sich, das freigesetzte Carbonat trifft auf Mg, und
**Dolomit** fällt in einem Band aus, das die Säule hinabwandert und sich dahinter wieder auflöst. Mit diesem Benchmark werden Codes für reaktiven Transport verglichen
([doi:10.1007/s10596-019-09919-3](https://doi.org/10.1007/s10596-019-09919-3), Abschnitt 4.4, Abb. 6).

Neu in `case.yaml`:

- **`transport.material.darcy_flux`**: Advektion in $+x$-Richtung;
- **ein `outflow`-Rand** rechts, an dem Wasser mit der Zusammensetzung der letzten Zelle austritt;
- **ein feines Gitter**, weil das Upwind-Verfahren Fronten verschmiert;
- **ein GEMS-Projekt, dessen unabhängige Komponenten nicht alle Elemente sind** (kein `O`);
- ein Rezept, das durch Skalieren eines GEMS-Zustands auf φ = 0,32 entsteht ([wie](../yaml/from_gems.md)).

| | |
|---|---|
| Modus | `coupled` |
| Fallordner | `FEniCSx_GEMS/example/demo_calcite_dolomite` (dieses Notebook läuft dort) |
| Gebiet | 0,5 m, 1000 Zellen, 105 Schritte zu 200 s |
| Laufzeit | etwa 25 s |
""", r"""
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
""", r"""
## Rechnen
""", r"""
## Vergleich mit der Veröffentlichung (t = 21 000 s)

Links: dieses Modell im Layout von Abb. 6. Rechts: die veröffentlichte Abbildung. Minerale sind wie in der Veröffentlichung von mol/m³ Gesamtvolumen in mol pro m³ Wasser (÷ φ) umgerechnet.
""", r"""
Die Lage der Mg- und Cl-Fronten, der Calcit-Lösungsfront und des Dolomitbands stimmt mit der veröffentlichten Abbildung überein.

## Wie das Band wandert
""", r"""
Dolomit bildet sich dort, wo Mg auf sich lösenden Calcit trifft. Hinter dem Band ist das zuströmende MgCl₂-Wasser an Dolomit untersättigt, der sich wieder löst. So wandert das
Band mit der Calcitfront.

## Warum 1000 Zellen? Numerische Dispersion

Das Upwind-Verfahren fügt zum physikalischen $D_e$ eine numerische Dispersion von etwa $q h/2$ hinzu. Mit 1000 Zellen ($h$ = 0,5 mm) sind das
$0{,}75\times10^{-9}$ m²/s, etwa 12 % von $D_e$; mit 100 Zellen wären es das 1,2-Fache von $D_e$. Eine geänderte Zeile zeigt den Effekt:
""", r"""
Mit 100 Zellen liegt das Band an derselben Stelle; nur seine Ränder verteilen sich über einige grobe Zellen. Gleichgewichtschemie hält die Mineralfronten scharf, deshalb spielt das
Gitter hier eine kleinere Rolle, als die Dispersionsabschätzung vermuten lässt. Bei anderen Problemen kann es viel ausmachen: verfeinern, bis sich das Ergebnis nicht mehr ändert.

## Selbst ausprobieren

1. `darcy_flux` verdoppeln (`De` beibehalten). Wie weit kommt das Band in 21 000 s?
2. `update_porosity: true` einschalten. Dolomit hat pro Ca+Mg ein kleineres Molvolumen als Calcit. Steigt φ oder sinkt es?
3. `dt: 100` setzen und mit `dt: 200` vergleichen.

Sie kennen jetzt jeden Abschnitt von `case.yaml`. Die [Referenzseiten](../yaml/index.md) nennen die übrigen Optionen, etwa `start: warm` und `on_failure: skip`
für schwierige Chemie.
"""]
