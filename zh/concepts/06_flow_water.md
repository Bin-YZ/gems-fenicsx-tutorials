# 水流、渗透率和多余水源项

对饱和算例，OGS-GEM 每一步解一个稳态地下水流问题：

$$-\nabla\cdot(K\nabla h) = Q, \qquad q = -K\nabla h,$$

$K$ 按单元给。$K$ 依赖孔隙率时（Kozeny–Carman，`$PERMEABILITY_FUNCTION_POROSITY 4`）

$$K = K_0\,\frac{(1-\phi_0)^2}{(1-\phi)^2}\,\frac{\phi^3}{\phi_0^3},$$

节点值在单元内取调和平均。

## 多余水源项

`hydrology='full'` 时，GEMS 的水相体积被缩放到孔隙率。差值 $V_{aq} - \phi$ 不会丢掉：下一步它作为节点源项
$Q_i = (V_{aq,i} - \phi_i)/\Delta t \cdot V_i$ 注入水流问题（OGS `SetSourceSink`）：

```{image} ../figures/excess_water.png
:width: 100%
```

矿物在反应的地方，这个体积变化是物理的（comedy2d：沿水泥带最大 $10^{-5}$ m³/m³）。没有反应的地方，它只是
GEMS 的舍入误差（$10^{-10}$–$10^{-7}$）。在低渗透材料里，连这点噪声也会让水头变化几厘米——所以
[ConcreteCrack](../tutorials/05_concretecrack) 的水头无法逐节点复现。
