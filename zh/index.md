# GEMS + FEniCSx：反应运移教程

这些页面用 **GEMS**（吉布斯自由能最小化算化学）和 **FEniCSx**（有限元算水流和输运）讲反应运移建模，
以 **OpenGeoSys-GEM**（OGS5GEMDEV）的基准算例为例题。每篇教程用一个小的 Python 模板重建一个 OGS-GEM 算例，
并和 OGS 原始输出比较。

目标不只是把算例跑通，而是把耦合里的**每一条**规则弄明白——包括只写在 OGS 源代码里的那些——
直到能自己搭模型。

## 学习路线

| # | 教程 | 新内容 | 用时 |
|---|---|---|---|
| 1 | [HAYEKIT](tutorials/01_hayekit) | SNIA、动力学上下限、孔隙率反馈、解析解 | 3 分钟 |
| 2 | [方解石柱](tutorials/02_calcite) | 对流、平衡前锋、OGS 的浓度 ↔ 质量换算 | 15 秒 |
| 3 | [OPC 混凝土 + 石英](tutorials/03_opc_quartz) | 1 万年的慢动力学、约束、封闭体系 | 18 分钟 |
| 4 | [comedy2d](tutorials/04_comedy2d) | 二维 Darcy 流、两个动力学相、子步、多余水源项 | 25 秒 |
| 5 | [ConcreteCrack](tutorials/05_concretecrack) | 裂缝单元、FEM-FCT、Kozeny–Carman、复现到哪里为止 | 4 分钟 |

建议配合[概念篇](concepts/01_snia)一起读；每篇教程都链接到它用到的概念。

## 需要什么

- 模板文件夹 `GEMS_FEniCSx_OGS5_Template`（模块 + 所有算例数据）；
- 装有 dolfinx 和 xgems 的 Python 环境，见[安装](setup)。

## 致谢

基准算例、输入文件和参考结果来自 **OGS5GEMDEV**（OpenGeoSys 5 与 GEMS3K 的耦合，主要由 PSI 的
Georg Kosakowski 开发）。GEMS3K 和 xGEMS 由 GEMS 团队（Kulik 等）开发，FEniCSx 由 FEniCS 项目开发。见[参考文献](sources)。
