# 与 OpenGeoSys-GEM 的验证

在上述入门代码出现之前，耦合规则是通过用 FEniCSx 和 GEMS 复现 **OpenGeoSys-GEM**（OGS5GEMDEV，主要由 PSI 的 G. Kosakowski 开发）的五个基准算例、并与 OGS 原始结果对比而确定的。这些算例超出了一维代码的范围：二维 Darcy 流、动力学、裂隙单元和通量修正输运。它们使用本仓库中单独的 Python 模板 `GEMS_FEniCSx_OGS5_Template`，逐条遵循 OGS 自身的规则。

可以把它们看作算子分裂方法能够复现成熟代码的证据，也可以作为高级功能的完整示例。

## 每个算例模拟的是什么

**[V1 · HAYEKIT](01_hayekit.ipynb)。** 一维 2 mm 柱。两种溶解物种 A 和 B 从两端相向扩散，按动力学速率沉淀为固相 AB(s)。沉淀物填充孔隙，孔隙率下降，扩散系数 $D_e = D_0\phi$ 随之下降。这个问题有解析解（Hayek、Kosakowski 和 Churakov，2011）。*新增内容：* GEMS 中的动力学上下限、孔隙率反馈、OGS 重启文件。

**[V2 · 方解石柱](02_calcite.ipynb)。** 经典的 Engesgaard–Kipp 基准：0.5 m 的方解石柱，以恒定 Darcy 通量用 MgCl₂ 溶液冲刷 21 000 s。方解石溶解，白云石在溶解锋面后方的条带中沉淀。化学与教程 5 相同，但用的是 OGS 的 CG1 输运和弥散度。*新增内容：* 元素总量的对流–弥散、纯平衡锋面、OGS 在浓度和节点量之间换算的规则。

**[V3 · OPC 混凝土 + 石英](03_opc_quartz.ipynb)。** 含石英骨料的 10 m 波特兰水泥混凝土柱，计算 10 000 年。石英溶解得很慢（碱–硅反应），释放的硅与 portlandite 和 C-S-H 反应，pH 从 12.9 降到约 10，并生成沸石。OGS 输入中的边界条件实际上从未被读取，所以这根柱子是一个封闭的批式体系。*新增内容：* 长时间内一种慢动力学矿物、初始物种约束、两遍初始化。

**[V4 · comedy2d](04_comedy2d.ipynb)。** 二维 14 × 14 cm 的饱水方块：一条竖直的水泥带夹在两块砂区之间，NaCl 溶液和草酸钠溶液流入，水从右侧流出。草酸根在水泥带处与 portlandite 反应生成草酸钙。基准从一个 OGS 状态重启，只算 6 步（68 s）。*新增内容：* 二维 Darcy 流场、带子步的两个动力学相、GEMS 体积变化产生的多余水源项。

**[V5 · ConcreteCrack](05_concretecrack.ipynb)。** 2.5 × 10.5 cm 的竖直混凝土剖面，带表层和一条 0.5 mm 宽、深 5 cm 的裂缝。顶部是硝酸盐溶液，水流主要走裂缝。基准算 10 步、每步 1 s，检验的是初始化以及裂缝与基质的耦合。*新增内容：* 嵌入二维网格的裂缝线单元、Kozeny–Carman 渗透率、随孔隙率变化的扩散、FEM-FCT，以及病态流动问题中复现的极限。

每个 notebook 末尾都有与 OGS 参考结果的误差表。`GEMS_FEniCSx_OGS5_Template/cases/*/ogs_input` 和 `…/reference` 中的 OGS 输入文件和参考结果原样取自 OGS5GEMDEV。
