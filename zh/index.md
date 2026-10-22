# FEniCSx + GEMS 反应运移

本站介绍一套把两个程序耦合起来的 Python 小代码：

- **[FEniCSx](https://fenicsproject.org)**：在一维多孔介质柱中，通过扩散和对流移动溶解的元素；
- **[GEMS3K](https://gems.web.psi.ch)**（通过 `xgems` 调用）：计算每个网格单元的局部化学平衡。

一次模拟完全由 **一个输入文件 `case.yaml`** 描述。建立新问题时只改这个文件，Python 模块保持不变。

```{image} figures/coupling_loop.png
:alt: 一个时间步：coupling.py 读取 case.yaml，把水相量交给 transport.py，把总量交给 chemistry.py，再用 output.py 输出
:width: 100%
```

## 快速上手

```bash
# 1. 准备含 FEniCSx、PETSc、GEMS3K、PyYAML 的环境（见“安装”）
conda activate fenicsx

# 2. 修改输入
cd FEniCSx_GEMS
nano case.yaml                  # 或使用浏览器里的 Case Builder

# 3. 运行；结果写入 output.folder
python coupling.py case.yaml
```

在 Windows + WSL 上，双击 `Run.cmd` 即完成第 3 步。

## 网站结构

| 部分 | 内容 |
|---|---|
| [安装](install.md) | 配置 Python 环境并检查 |
| [耦合原理](coupling/overview.md) | 每个时间步四个模块交换什么、单位、守恒检查 |
| [方程与数值方法](coupling/numerics.md) | 输运方程、离散方法、孔隙率和扩散系数反馈 |
| [`case.yaml` 参考](yaml/index.md) | 四节中每个参数的含义、单位、默认值和示例 |
| [浏览器工具](tools/case_builder.md) | 用表单生成 `case.yaml`；在浏览器中查看 GEMS 项目 |
| [教程](tutorials/01_tracer_diffusion.ipynb) | 五个算例：从不含化学的示踪剂到带流动的方解石–白云石转化 |
| [结果与排错](outputs.md) | 每个输出文件的内容；GEMS 不收敛时怎么办 |
| [与 OGS-GEM 的验证](verification/index.md) | 用 FEniCSx 和 GEMS 复现的五个 OpenGeoSys-GEM 基准算例 |

## 学习路线

1. [示踪剂扩散](tutorials/01_tracer_diffusion.ipynb)：`diffusion` 模式、解析解、质量守恒
2. [单点化学平衡](tutorials/02_single_equilibrium.ipynb)：`chemistry` 模式、配方、相名称、Gibbs 能
3. [NaCl 扩散](tutorials/03_nacl_diffusion.ipynb)：第一次 `coupled` 运行、两个分区
4. [水泥溶蚀](tutorials/04_cement_leaching.ipynb)：孔隙率和扩散系数反馈
5. [方解石 → 白云石](tutorials/05_calcite_dolomite.ipynb)：对流、入流和出流边界

每篇教程都给出完整的 `case.yaml`、与上一篇相比改了哪些行、运行方法和结果。
