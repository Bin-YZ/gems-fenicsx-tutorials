# 教程概览

五个算例，每个都比前一个多一点内容。每篇教程都是已经运行过的 notebook：给出完整的 `case.yaml`，用 `coupling.py` 运行，并画出结果，大多与解析解或已发表的基准算例对比。

| # | 模拟的是什么 | 模式 | 学到什么 | 运行时间 |
|---|---|---|---|---|
| [1](01_tracer_diffusion.ipynb) | 一种不反应的示踪剂从浓度固定为 c = 1 的边界扩散进 10 mm 的饱水柱（φ = 0.4），另一端固定为 0，之后改为封闭。 | `diffusion` | `case.yaml` 的四节、如何运行、结果文件、质量守恒；与解析级数解对比 | 2 s |
| [2](02_single_equilibrium.ipynb) | 对一种水化水泥浆体（Ca、Si、水、痕量 Cl）做一次 GEMS 平衡计算：它含哪些矿物、孔隙水是什么成分。把体相 Ca/Si 从 3.7 扫描到 0.5，可以看到 portlandite 消失、C-S-H 失去 Ca、无定形硅出现。 | `chemistry` | GEMS 项目中的元素名和相名、配方单位（每 dm³ 体相的 mol）、`gibbs` 修正 | 15 s |
| [3](03_nacl_diffusion.ipynb) | 1 M 和 0.5 M 的 NaCl 溶液在 20 mm 柱的中间接触，盐从浓侧向稀侧扩散 100 s，没有固相。 | `coupled` | 第一次耦合运行、两个各有配方的分区、两侧不同的边界溶液；与 erf 解析解对比 | 5 s |
| [4](04_cement_leaching.ipynb) | 4 mm 的水化水泥浆体与 14.6 mM CaCl₂ 水接触 1000 年。Ca 被溶出，portlandite 从表面向内溶解，锋面后方的 C-S-H 脱钙。 | `coupled` | 矿物与 `solid_phases`、长时间尺度、孔隙率和扩散系数反馈；与 HYDRUS 基准剖面对比 | 2 × 3–5 min |
| [5](05_calcite_dolomite.ipynb) | 用 MgCl₂ 溶液冲刷 0.5 m 的方解石柱（Darcy 通量 3·10⁻⁶ m/s）21 000 s。方解石溶解，白云石在一个条带中沉淀，条带随水流移动，并在后方再次溶解。 | `coupled` | 对流（`darcy_flux`）、`outflow` 边界、没有 O 的 GEMS 项目、数值弥散；与已发表的基准图对比 | 25 s |

教程 1 和 2 把算例写到 `FEniCSx_GEMS` 旁边的 `tutorial_runs/` 中，教程 3–5 在对应的 `FEniCSx_GEMS/example/<算例>/` 文件夹中运行。每个 notebook 的第一个代码单元会自动找到这些文件夹。
