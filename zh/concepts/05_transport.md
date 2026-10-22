# 输运数值方法：单元系数、质量矩阵和 FCT

模板用线性（CG1）有限元和向后 Euler，和 OGS 相同。要和 OGS 逐节点对上，细节上也得做同样的选择：

| 细节 | OGS 规则 | 模板 |
|---|---|---|
| 单元孔隙率 | 节点孔隙率的平均 | `element_mean(phi, cells)` |
| 单元扩散系数 | 节点值的调和平均（`$DIFFUSION 8/9`） | `harmonic_mean(...)` |
| 质量矩阵 | 一致质量；`ELE_MASS_LUMPING` 时集中质量 | `Transport(lumped=...)` |
| 弥散 | $\alpha_T|q|I + (\alpha_L-\alpha_T)\,qq^T/|q|$ | `alpha_L`、`alpha_T` |
| 积分 | 四边形 3×3 Gauss | `quadrature_degree=5` |

## FEM-FCT

对流很强时，Galerkin 格式会产生振荡和负浓度，GEMS 就会拿到负的元素量。OGS 提供通量校正输运
（`$FEM_FCT 1`，Kuzmin 的线性化格式）：先算加了离散扩散的低阶解，再加上 Zalesak 限制器允许的、
不产生新极值的那部分“反扩散”校正。

```{image} ../figures/fct.png
:width: 90%
```

OGS 在第 $j$ 行加的是 $+f_{ij}$；教科书格式是 $-f_{ij}$（质量守恒）。`Transport(fct_ogs_sign=True)` 照抄 OGS。
在 [ConcreteCrack](../tutorials/05_concretecrack) 里，和 OGS 参考相比这两种写法分辨不出来。
