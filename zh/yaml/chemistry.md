# `chemistry`：GEMS 项目与配方

由 `chemistry.py` 读取。在 `diffusion` 模式下这一节必须存在，但不会被使用。

```yaml
chemistry:
  project: chemistry_data/b_time0-dat.lst
  temperature: 298.15
  pressure: 100000
  aqueous_phase: aq_gen
  solid_phases: [CSHQ, Portlandite, Silica-amorph]
  gibbs: {H2O@: -237183.0, Ca+2: -552400.0}
  initial: {Ca: 1.119, Si: 0.310, H: 58.52, O: 31.00, Cl: 1.0e-15}
  inlet:   {Ca: 0.0146, Cl: 0.0292, H: 111.0, O: 55.51, Si: 0.000183}
  start: cold          # 可选
  on_failure: stop     # 可选
```

## 参数

| 键 | 必需 | 取值 | 含义 |
|---|---|---|---|
| `project` | 是 | 路径 | GEMS 的 `*-dat.lst` 文件，相对于 `case.yaml`。JSON（`-j`）和文本（`-t`）导出均可 |
| `temperature` | 是 | K，> 0 | 每次平衡的温度 |
| `pressure` | 是 | Pa，> 0 | 每次平衡的压力 |
| `aqueous_phase` | 是 | 相名 | 其元素参与输运的相，通常为 `aq_gen` |
| `solid_phases` | 是 | 相名列表，可为 `[]` | 写入输出的相；**它们的体积决定孔隙率更新** |
| `gibbs` | 是 | `{物种: J/mol}`，可为 `{}` | 覆盖标准摩尔 Gibbs 能，只改内存中的值 |
| `initial` | 是* | 配方，或 `{分区: 配方}` | t = 0 时的材料 |
| `inlet` | 有 `dirichlet` 边界时 | 配方、分区名，或 `{left: …, right: …}` | Dirichlet 边界上固定的溶液 |
| `start` | 否，默认 `cold` | `cold` / `warm` | 每次调用 GEMS 的初始化方式，见 [数值方法](../coupling/numerics.md) |
| `on_failure` | 否，默认 `stop` | `stop` / `skip` | 某单元不收敛时怎么办 |

\* diffusion 模式下 `initial` 可以为 `{}`。

## 配方

配方给出 **每 1 dm³ 体相材料中元素的 mol 数**。体相材料包括孔隙水、固相和惰性物质。

```yaml
initial:
  Ca: 1.119218076064     # mol/dm3 体相
  Si: 0.31000148638994
  H: 58.52226105076      # 包含水：0.5 dm3 水 = 27.75 mol H2O -> 55.5 mol H ...
  O: 31.00037832923
  Cl: 1.0e-15            # 痕量，保证该元素存在
```

- 使用 GEMS 项目中的 **元素** 名（`Ca`、`Si` 等），不要用氧化物或物种。
- 不写 `Zz`（电荷）。未写的元素取 0。
- **要包含水。** 配方中的 H 和 O 是水中的量加上固相和溶解物种中的量。
- 若某元素以后才会出现（例如 Cl 从边界进入），先给一个痕量如 `1.0e-15`，这样 GEMS 的问题保持适定。
- 配方隐含的孔隙水量应与 `transport.material.phi` 一致：每 dm³ 体相含 0.5 dm³ 水的配方对应 `phi: 0.5`。摘要中的 **water mismatch** 会报告两者的差异。

[从 GEMS-Selektor 到配方](from_gems.md) 介绍如何从导出的 GEMS 状态得到这些数字。

### 多种材料：每个分区一个配方

配合 [`transport.zones`](transport.md)，`initial` 可以把分区名映射到配方：

```yaml
chemistry:
  initial:                 # 数字仅为示意；元素必须存在于你的项目中
    clay:   {Ca: 0.01, Si: 0.6, H: 57.0, O: 30.0, Na: 0.2, Cl: 0.2}
    cement: {Ca: 1.12, Si: 0.31, H: 58.5, O: 31.0, Cl: 1.0e-15}
```

每个分区都必须有配方。`chemistry` 模式没有网格，使用第一个配方。

## 边界溶液：`inlet`

`inlet` 在开始时平衡一次，其孔隙水浓度随后固定在所有 `dirichlet` 边界上。有三种写法：

```yaml
inlet: {Ca: 0.0146, Cl: 0.0292, H: 111.0, O: 55.5}   # 1. 配方（约 1 dm3 溶液），两侧共用
inlet: clay                                          # 2. 某分区平衡后的孔隙水
inlet:                                               # 3. 两侧分别指定，每侧可用以上任一写法
  left: {Na: 0.1, Cl: 0.1, H: 111.0, O: 55.5}
  right: cement
```

inlet 配方的量按一个 GEMS 体系计，通常约 1 dm³ 水。程序会除以 GEMS 给出的水相体积，所以水的确切量不重要，只要溶质与水的比例正确即可。没有 `dirichlet` 边界时省略 `inlet`。

## 相名与 `solid_phases`

`aqueous_phase` 和 `solid_phases` 中的每一项都必须是项目中的相名，否则报 *Unknown GEMS phase* 并停止。未列出的相仍参与平衡，但是：

- 它们的量不写入 `profiles.csv`；
- 它们的体积 **不** 计入孔隙率更新。

因此开启 `update_porosity` 时，要列出所有可能生成或溶解的固相。

## `gibbs`

```yaml
gibbs: {H2O@: -237183.0, Ca+2: -552400.0}    # J/mol，运行温度下
```

加载项目后覆盖指定 **物种** 的 $G^\circ$，不修改文件。用于复现使用了略有不同数据的基准算例，否则保持 `gibbs: {}`。效果见 [教程 2](../tutorials/02_single_equilibrium.ipynb)。

## GEMS 不收敛时

GEMS 返回状态 2 或 6，**并且** 以 1e-8 的精度重现给定的元素总量，单元才算成功。否则：

1. 若 `start: warm`：从该单元上一次的状态重试，并分四步逼近新组成；
2. 按比例缩放后冷启动（×1、×1、×10、×100、×0.1、×0.01）；
3. 仍失败时：`on_failure: stop` 结束运行，写出包含时间步、单元、位置和组成的 `failure.txt`；`on_failure: skip` 让该单元在本步不反应。总量不变，所以质量仍守恒。每次跳过都会记录并计数。

初始平衡（第 0 步）失败时总是停止。
