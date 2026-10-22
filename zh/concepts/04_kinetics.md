# 用平衡求解器做动力学

GEMS 只算平衡。OGS-GEM 让某个矿物受动力学控制的办法是：给 GEMS 一个它的量的**窗口**
$[\text{dll}, \text{dul}]$，GEMS 在这个窗口*之内*找平衡。

## 速率

每次 GEMS 计算后，每个动力学相的速率（OGS `CalcReactionRate`）：

$$\frac{dm}{dt} = -A_s \sum_m 10^{\log k_m}\, a_{H^+}^{\,n_m}\,(1-\Omega)$$

饱和度 $\Omega$ 来自 GEMS，反应表面积 $A_s$ 由表面积模型给出（`Kinetic.area_model`）：
1——$A\,V_\text{矿物}$；3——$A\,V_\text{矿物}/\phi$；4——$A\,\phi$。

## 移动窗口

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/gems_ogs.py
:language: python
:pyobject: OGSGEMS.calc_limits
```

下一步窗口移动 $\frac{dm}{dt}\,\Delta t$（OGS `CalcLimits`）：

```{image} ../figures/kinetics_window.png
:width: 90%
```

- `limits='loose'`（`$LOOSE_KINETICS 1`）：窗口一端留在当前量，所以 GEMS 也可以选择比速率允许的*更少*的反应。
  `'strict'` 把量钉在动力学目标值上。
- **成核种子：** 不存在但过饱和的相给 $10^{-6}$ mol，否则它永远不会开始生成。
- **子步**（`substep_kinetics`，OGS 2017）：如果一个相一步之内会让某元素变化超过 10 %，就把化学步拆开。

速率是显式的——用上一步结束时的状态算。这是结果依赖时间步的主要原因（见 [HAYEKIT](../tutorials/01_hayekit)）。
