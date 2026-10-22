# 耦合原理

代码把每个时间步拆成一个 **输运步** 和一个 **化学步**，即顺序非迭代算子分裂（SNIA）。四个模块各管一件事，只有 `coupling.py` 与另外三个模块通信：

| 模块 | `case.yaml` 中的节 | 负责 | **不**负责 |
|---|---|---|---|
| `coupling.py` | `coupling` | 读输入、管理数组、时间循环、更新 φ 和 De、检查守恒 | 直接调用 GEMS 或组装有限元形式 |
| `transport.py` | `transport` | 建一维网格、施加边界条件、对每个元素求解一次输运 | 任何化学 |
| `chemistry.py` | `chemistry` | 加载 GEMS、转换配方、计算一次局部平衡 | 网格 |
| `output.py` | `output` | 写 CSV、XDMF、图、日志、摘要和失败报告 | 任何计算 |

```{image} ../figures/coupling_loop.png
:alt: coupling.py 居中，右侧为 transport.py 和 chemistry.py，左侧为 case.yaml 和 output.py
:width: 100%
```

## 存什么、用什么单位

所有量都存在 **每行一个单元、每列一个元素** 的数组里。列的顺序就是 GEMS 项目中元素的顺序，例如 `Ca, Cl, H, O, Si, Zz`。

| 数组 | 含义 | 单位 |
|---|---|---|
| `state['total']` | 单元内某元素的全部量（溶解 + 固相） | mol/m³ 体相 |
| `state['aqueous']` | 溶解部分 | mol/m³ 体相 |
| `c = aqueous / phi` | 溶解浓度 | mol/m³ 孔隙水 |
| `state['phi']` | 孔隙率 | – |
| `state['De']` | 有效扩散系数 | m²/s |
| `state['minerals']` | `chemistry.solid_phases` 中各相的量 | mol/m³ 体相 |

`case.yaml` 中的化学配方以 **每 dm³ 体相材料的 mol 数** 书写，这是 GEMS 参考体系的大小。`chemistry.py` 读入时乘以 1000，调用 GEMS 之前再除以 1000。

```{image} ../figures/cell_volume.png
:alt: 1 m³ 体相单元分为孔隙水、反应矿物和惰性物质
:width: 90%
```

## 一个时间步

```python
# coupling.py 时间循环内部（简化）
immobile = state['total'] - state['aqueous']           # 1. 不动的部分
state['aqueous'], incoming = transport.step(            # 2. 移动溶解部分
    state['aqueous'], state['phi'], state['De'], dt, boundary_c, mobile)
state['total'] = immobile + state['aqueous']            # 3. 新的总量
for i in cells:                                         # 4. 局部平衡
    result = chemistry.equilibrate(state['total'][i])
    state['aqueous'][i] = result['aqueous']             #    GEMS 重新分配总量
    solid[i] = result['solid']                          #    solid_phases 的体积分数
phi = phi0 + initial_solid - solid                      # 5. 反馈（若开启）
De = De0 * (phi / phi0) ** exponent
balance = inventory - initial_inventory - exchange      # 6. 守恒检查
output.write(state, diagnostics)                        # 7. 输出
```

1. **只有溶解的量会移动。** 矿物等不动部分在输运前取出，输运后加回。
2. **每个元素都参与输运**，包括水中的 H 和 O，只有电荷 `Zz` 不输运。每个元素各自求解一个线性方程组，矩阵相同。
3. **一个输运步内 φ 和 De 固定。** 它们在化学步之后更新，下一步才使用新值。
4. **化学是局部的。** 每个单元按自己的元素总量单独平衡。平衡守恒总量，因此化学步不影响质量守恒。
5. **反馈可选。** 不开 `update_porosity` 时，无论矿物溶解多少，φ 都保持初始值。

第 0 步没有输运：初始配方只平衡一次，此时得到的固相体积作为孔隙率更新的参考值 `initial_solid`。

## 边界溶液

`dirichlet` 边界把孔隙水固定为某个组成。在 `coupled` 模式下，这个组成来自 `chemistry.inlet`。程序在开始时平衡一次该配方，每个元素的边界浓度为

$$
c_\text{boundary} = \frac{\text{水相中该元素的量}}{\text{水相体积}}
\qquad \text{（mol/m³ 水）}
$$

因此边界水除溶质外也带着自身的 H 和 O。`no_flux` 边界不交换任何物质；`outflow` 只让水随对流流出（见 [transport](../yaml/transport.md)）。

## 守恒是检查出来的，不是假设的

每一步之后，`coupling.py` 对每个元素比较

$$
\underbrace{\textstyle\sum_\text{单元} \text{total}\cdot h}_\text{当前存量}
-\underbrace{\textstyle\sum_\text{单元} \text{total}_0\cdot h}_\text{初始存量}
-\underbrace{\textstyle\sum_\text{时间步} \text{边界输入}}_\text{交换量}
$$

单位为每 m² 截面的 mol。边界输入单独由边界通量计算。若差值超过 $10^{-9} + 10^{-8}\,(|\text{初始}| + |\text{交换}|)$，运行会 **停止** 并报 `Mass balance failed`。负浓度或负孔隙率也不会被悄悄截断，一出现就停止运行并写出 `failure.txt`。

另外每一步还会写两个不终止运行的诊断量：

- **chemistry error**：GEMS 重现给定元素总量的精度（mol/m³）；
- **water mismatch**：GEMS 水相体积与 φ 的相对差。输运假设孔隙饱和、体积为 φ，而 GEMS 用自己的密度模型算溶液体积，零点几个百分点属于正常。

## 三种模式

`coupling.mode` 决定循环中运行哪些部分：

| 模式 | 输运 | 化学 | 典型用途 |
|---|---|---|---|
| `diffusion` | 是，输运 `transport.components` 中的示踪剂 | 否（不加载 GEMS） | 检查网格、时间步和边界 |
| `chemistry` | 否（不建网格） | 对 `chemistry.initial` 算一次平衡 | 检查配方和相名称 |
| `coupled` | 是，除 `Zz` 外所有元素 | 每个单元、每个时间步 | 正式模拟 |
