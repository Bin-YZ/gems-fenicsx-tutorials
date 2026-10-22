# 与 OpenGeoSys-GEM 的验证

在上述入门代码出现之前，耦合规则是通过用 FEniCSx 和 GEMS 复现 **OpenGeoSys-GEM**（OGS5GEMDEV，主要由 PSI 的 G. Kosakowski 开发）的五个基准算例、并与 OGS 原始结果对比而确定的。这些算例超出了一维代码的范围：二维 Darcy 流、动力学、裂隙单元和通量修正输运。它们使用本仓库中单独的 Python 模板 `GEMS_FEniCSx_OGS5_Template`，逐条遵循 OGS 自身的规则。

可以把它们看作算子分裂方法能够复现成熟代码的证据，也可以作为高级功能的完整示例。

| # | 基准算例 | 新增内容 |
|---|---|---|
| 1 | [HAYEKIT](01_hayekit.ipynb) | 动力学限制、孔隙率反馈、解析解 |
| 2 | [方解石柱](02_calcite.ipynb) | 对流、平衡锋面、OGS 浓度 ↔ 质量规则 |
| 3 | [OPC 混凝土 + 石英](03_opc_quartz.ipynb) | 10 000 年慢动力学、封闭体系 |
| 4 | [comedy2d](04_comedy2d.ipynb) | 二维 Darcy 流、两个动力学相、子步 |
| 5 | [ConcreteCrack](05_concretecrack.ipynb) | 裂隙单元、FEM-FCT、Kozeny–Carman |

每个 notebook 末尾都有与 OGS 参考结果的误差表。`GEMS_FEniCSx_OGS5_Template/cases/*/ogs_input` 和 `…/reference` 中的 OGS 输入文件和参考结果原样取自 OGS5GEMDEV。
