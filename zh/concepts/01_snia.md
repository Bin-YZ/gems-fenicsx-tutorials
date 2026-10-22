# 算子分裂（SNIA）

OGS-GEM 不把输运和化学放在一起解。每个时间步拆成几个独立的求解，每个只做一次——
即*顺序非迭代方法*（SNIA）：

```{image} ../figures/snia.png
:width: 100%
```

1. **prepare**——把每个节点的新孔隙率换成单元系数（孔隙率、扩散系数、渗透率），并给出当前时刻的边界值。
2. **flow**（如果有）——稳态 Darcy 问题，上一步 GEMS 的多余水作为源项。
3. **transport**——每个可动化学元素当作被动溶质做对流和弥散。
4. **chemistry**——用输运后的量在每个节点重新做 GEMS 平衡。

模板里对应的是 `reactive_transport.run`：

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/reactive_transport.py
:language: python
:pyobject: run
```

**在教程里会遇到的后果**

- 分裂误差对 $\Delta t$ 是一阶的。动力学是显式的，误差可能很大：在 [HAYEKIT](../tutorials/01_hayekit)
  里，$\Delta t = 100$ s 时 OGS 自己的孔隙率就和解析解差 24 %。
- 系数滞后一步：第 $n$ 步的输运用的是第 $n-1$ 步的孔隙率。
- 不迭代，所以 GEMS 失败的节点整步保持旧状态。
