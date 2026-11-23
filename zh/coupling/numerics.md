# 方程与数值方法

## 输运方程

下面的方程是算子分裂中的 **输运子步**：这一子步内不考虑反应，孔隙率保持不变。溶解元素的完整方程还包含反应源项 $R$（溶解减去沉淀），
即 $\partial(\phi c)/\partial t + \partial_x(qc - D_e\partial_x c) = R$。代码不直接离散 $R$，而是由随后的化学子步在每个单元中用局部平衡代替它（见 [耦合原理](overview.md)）。

在输运子步中，对每个参与输运的元素（$c$ 单位为 mol/m³ 孔隙水）：

$$
\frac{\partial(\phi c)}{\partial t} + \frac{\partial}{\partial x}\!\left(q\,c - D_e \frac{\partial c}{\partial x}\right) = 0,
\qquad 0 < x < L
$$

| 符号 | `case.yaml` 中的键 | 单位 |
|---|---|---|
| $\phi$ | `transport.material.phi`（或分区值），随后由反馈更新 | – |
| $D_e$ | `transport.material.De`（或分区值），随后由反馈更新 | m²/s |
| $q$ | `transport.material.darcy_flux`（Darcy 通量 $=\phi\times$ 孔隙流速，指向 $+x$） | m/s |
| $L$ | `transport.geometry.length` | m |

$D_e$ 是通量中的 **有效** 扩散系数，孔隙扩散系数为 $D_p = D_e/\phi$。所有元素用同一个 $D_e$，不考虑电迁移。

## 离散

- **空间：均匀网格上的 DG0 有限体积。** `transport.geometry.cells` 个宽 $h = L/n$ 的单元，每个单元一个值。相邻两单元之间的扩散通量用两者 $D_e$ 的调和平均 $D_\text{face} = 2D_e^+D_e^-/(D_e^+ + D_e^-)$。Dirichlet 边界距第一个单元中心 $h/2$。
- **对流：一阶迎风。** 每个单元从下游面流出 $q\,c$。迎风格式稳定且不会产生负值，但会让锋面变平，数值弥散约为 $q h / 2$。对流问题要用细网格。
- **时间：向后欧拉。** 无条件稳定、一阶精度。`coupling.time.dt` 是唯一的时间步，输运和化学共用。
- **线性求解器：PETSc**，由 `transport.solver` 设置。默认的 `preonly` + `lu` 是直接法，一维问题用它最合适。

`transport.py` 中以 DG0 测试函数 $v$ 写出的弱形式为

$$
\int \phi\,\frac{c^{n+1}-c^n}{\Delta t}\,v\,dx
+ \sum_\text{单元面} D_\text{face}\,\frac{[c^{n+1}]\,[v]}{h}
+ \text{迎风项和边界项} = 0 .
$$

## 孔隙率与扩散系数反馈

当 `coupling.update_porosity: true` 时，孔隙率随 `chemistry.solid_phases` 中矿物的体积变化：

$$
\phi = \phi_0 + V_\text{solid,0} - V_\text{solid}
$$

$V_\text{solid}$ 是 GEMS 给出的这些相的体积分数，$V_\text{solid,0}$ 是初始平衡后的值。溶解使孔隙变大，沉淀使孔隙变小。不由 GEMS 相表示的物质是惰性的，始终不变。孔隙率超出 $(0, 1]$ 时运行停止。

再开启 `coupling.update_diffusivity: true` 时：

$$
D_e = D_{e,0}\left(\frac{\phi}{\phi_0}\right)^{m}, \qquad m = \texttt{coupling.exponent}
$$

这是 Archie 型关系，指数是给定的，不是拟合的。φ 变化时保持每体相体积的溶解 **量** 不变，因此浓度重新按 $c = \text{aqueous}/\phi$ 计算。

## 时间步的选择

除向后欧拉的误差外，算子分裂还会引入随 $\Delta t$ 增大的误差。

- **扩散主导：** $\sqrt{D_p\,\Delta t}$ 是一个时间步的扩散长度。它是长度尺度，并不是矿物锋面每步移动的距离；锋面移动还取决于需要溶解或沉淀多少矿物。若 $\sqrt{D_p\,\Delta t}$ 远大于单元宽度 $h$，浓度梯度在一步之内变化很大，分裂误差就会增大。
- **对流主导：** Courant 数 $q\,\Delta t / (\phi h)$ 保持在 1 左右或更小。向后欧拉在更大值下仍稳定，但锋面会更平。
- **时间和空间分开检查。** 先在细网格上依次用 `dt`、`dt/2`、`dt/4` 计算，直到剖面不再变化；再用这个时间步加密 `cells`，直到剖面不再变化。同时减半 `dt` 并加倍 `cells` 只能看到二者的综合效果，无法区分哪种误差占主导。

## 化学：冷启动与热启动

GEMS 对每个单元的体系做 Gibbs 能最小化。默认（`chemistry.start: cold`）每次调用都从头开始，因此结果不依赖上一步或相邻单元。若 GEMS 的元素平衡不好，就把同一体系按比例缩放后再解（×1、×10、×100、×0.1、×0.01），再缩放回来，因为平衡与体系大小无关。

`start: warm` 给每个单元一个独立的 GEMS 引擎，从该单元上一次的平衡出发，对大体系更快、更稳健。热启动失败时，先在原组成上重新求解，再分四个热启动小步过渡到新组成，最后才回到冷启动。

GEMS 的结果在舍入误差层面不能完全复现。在已测试的算例中，输入只差最后一位的两次运行，浓度的相对差异最大约 1e-5。这是这些算例中的观察值，不是普遍上限：差异大小取决于体系、求解器容差以及是否有相出现或消失。如何判断这类差异见 [两次运行的微小差异](../outputs.md)。
