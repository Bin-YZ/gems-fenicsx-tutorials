# GEMS–FEniCSx 模板（OGS5-GEM 算例版）

在 `GEMS_ADE_1D_Template` 的基础上扩展的模板：仍然是 “输运对象 + 化学对象 + SNIA 时间循环 + 每个算例一个短脚本” 的结构，
补上了 OGS5-GEM 基准算例需要、而原模板没有的部分（对流、FEM-FCT、水流、OGS 的浓度/质量换算、动力学限值、重启文件、线单元裂缝）。
前面单独复现过的 5 个算例全部改写成基于这个模板的脚本，结果和原来各自的 notebook 一致（见下面的核对表）。

| 编号 | 算例 | 文件夹 | 原来的单独复现 |
|---|---|---|---|
| 1 | calcite_gems | `cases/1_calcite` | `OGS5_calcite_GEMS_FEniCSx` |
| 2 | HAYEKIT | `cases/2_hayekit` | `HAYEKIT_GEMS_FEniCSx` |
| 3 | OPC + 石英（LookUp-Table Case1） | `cases/3_opc_quartz` | `OPC_quartz_GEMS_FEniCSx` |
| 4 | comedy2d | `cases/4_comedy2d` | `COMEDY2D_GEMS_FEniCSx` |
| 5 | ConcreteCrack | `cases/5_concretecrack` | `ConcreteCrack_GEMS_FEniCSx` |

## 运行

每个算例文件夹里双击 `Run.cmd`（用 Ubuntu 的 fenicsx 环境），或在 Ubuntu 里：

```bash
cd cases/1_calcite
/home/xi_b/miniforge3/envs/fenicsx/bin/python run_case.py
```

结果写到各自的 `results/`：`error_vs_ogs.csv`（和 OGS 参考比）、剖面/时间序列、`run_log.txt`。
脚本最后还会自动和旁边原来那个 notebook 文件夹的结果比较（找不到就跳过）。

| 算例 | 用时（2 核云端） | 说明 |
|---|---|---|
| 1 calcite | 15 s | |
| 2 HAYEKIT | 3 min | 默认算 dt = 100、10、1 s 三遍；`python run_case.py 100` 只算 OGS 的步长 |
| 3 OPC 石英 | 18 min | 1 万年；`python run_case.py 1000` 只算 1000 年 |
| 4 comedy2d | 25 s | loose / strict 两遍 |
| 5 ConcreteCrack | 3.5 min | 主结果 + 3 个对照变体 |

## 文件

```text
fe_mesh.py             OGSMesh：用 OGS 的节点和单元建 dolfinx 网格（线 / 三角形 / 四边形），节点 <-> 自由度、单元映射，节点体积
transport.py           Transport：CG1 对流-弥散，Backward Euler；集中质量、FEM-FCT（OGS 符号）、线单元附加矩阵
flow.py                Darcy：饱和稳态水流，节点源项，Darcy 通量 q 直接给 Transport
gems_ogs.py            OGSGEMS：每节点一个 GEMS 体系 + OGS-GEM 的耦合规则；Kinetic：动力学相
reactive_transport.py  run()：prepare -> 水流 -> after_flow -> 输运 -> 化学 -> record 的 SNIA 循环
ogs_models.py          节点值 -> 单元值（算术 / 调和平均）、扩散模型 8、Kozeny–Carman 模型 4、裂缝线单元 LineElements
ogs_io.py              读 OGS 的 .msh / .ic / .bc / .st / .gli、重启文件（*_gem.asc、*_primary_value.asc）、vtk
compare.py             误差表、和原来 notebook 结果的比较
cases/<算例>/          run_case.py、Run.cmd、gems/（OGS 原版 GEMS 文件）、ogs_input/、reference/、results/
复现问题记录.md         做模板时遇到的问题和没解决的疑点
```

## 和 GEMS_ADE_1D_Template 的对应

| 原模板 | 本模板 | 变化 |
|---|---|---|
| `ADE.py`（DG1/SWIP 扩散） | `transport.py` | 改成 CG1（和 OGS 一样，结果才能逐点对上）；加对流、弥散张量、集中质量、FCT、线单元；系数每步重组装（孔隙率反馈） |
| `gems.py`（局部平衡） | `gems_ogs.py` | 每节点保存 OGS 的状态量（b_fix、溶剂水、V_f、孔隙率、dll/dul、速率）；照 `rf_REACT_GEM.cpp` 做 ConcentrationToMass / MassToConcentration / CalcLimits |
| `reactive_transport.run` | `reactive_transport.run` | 仍只通过小接口调用输运和化学；加了水流和多余水源项；算例相关的系数在 `prepare` 回调里设 |
| `example.py` + `cement.py` | `cases/*/run_case.py` | 每个算例一个脚本，参数和初边值从 OGS 输入文件读 |
| 无 | `flow.py`、`ogs_io.py`、`fe_mesh.py`、`ogs_models.py` | 新增 |

原模板的约定保留：主要数据是 NumPy 数组（这里按 OGS 节点编号）；运移的是溶解元素总量（b 向量，`$TRANSPORT_B 1`），电荷 Zz 不动；
没有插件框架和继承，换输运或化学对象不用改时间循环。

## 写一个新算例：五步

```python
mesh = OGSMesh(points, cells, 'quadrilateral')                    # 1. 网格（OGS .msh 或自己生成的节点/单元）
flow = Darcy(mesh, fixed_nodes=outlet)                            # 2. 水流（没有就不建，输运用常数 q 或 q=None）
tr = Transport(mesh, fixed_nodes=inlet, q=flow.q, alpha_L=0.02)   # 3. 输运
chem = OGSGEMS('gems/xxx-dat.lst', mesh.n_nodes, hydrology='full',
               kinetics=[Kinetic('Portlandite', logk=(-5,), area_model=3, area=1000)],
               boundary_nodes=inlet)                              # 4. 化学 + 初值
chem.init_from_bulk(b_init)          # 或 chem.init_from_restart(read_restart(...), c0)

def prepare(step, t, dt):                                          # 5. 每步的系数，然后 run
    tr.phi_cell = chem.phi[mesh.cells].mean(1)
    tr.De_cell = tr.phi_cell * D
log = run(chem, tr, [dt] * n, flow=flow, prepare=prepare)
```

## 每个算例用到的模板功能

| | 1 calcite | 2 HAYEKIT | 3 OPC | 4 comedy2d | 5 ConcreteCrack |
|---|---|---|---|---|---|
| 维度 / 单元 | 1D 线 | 1D 线 | 1D 线 | 2D 四边形 | 2D 四边形 + 1D 裂缝 |
| 水流 | 常数 q | 无 | 无 | Darcy + 节点源 | Darcy，K 随孔隙率 |
| 输运 | 对流+弥散 | 扩散，D 随孔隙率 | 扩散，集中质量 | 对流+弥散 | 弥散张量 + FCT |
| 边界 | 入口 Dirichlet | 两端随时间变化 | 封闭 | 两个入口 | 顶部 |
| 初值 | .ic 一遍平衡 | 重启文件 | .ic 两遍 + 约束 | 重启文件 | .ic 两遍 |
| hydrology | full | hayekit | none | full | full |
| 动力学 | 无 | AB(s)，表面积模型 4 | 石英，模型 1 | 2 相，模型 3 + 子步 | 无 |
| 多余水源项 | – | – | – | 有 | 有 |

## 和 OGS / 原 notebook 的核对（最终版代码重新跑一遍的结果）

| 算例 | 和 OGS 参考（最大相对差） | 和原 notebook 的最大相对差 |
|---|---|---|
| 1 calcite | 浓度 0.2–1 %（前锋处）、孔隙率 3e-7，和原 notebook 的误差表相同 | 7e-4（白云石），pH 5e-7 |
| 2 HAYEKIT | A 2e-5、B 3e-5、AB(s) 2e-5、孔隙率 3e-4 | 8e-8 |
| 3 OPC 石英 | nRMSE：石英 0.035 %、Portlandite 0.037 %、孔隙率 0.07 % | 矿物 ≤ 4e-4；Ca 浓度 8e-3（低值时） |
| 4 comedy2d | Ca 1.4e-4、孔隙率 6e-8、水头 1e-9、速度 7e-6 / 1e-5 | 1e-4（速度）；水头和速度比原来更接近 OGS |
| 5 ConcreteCrack | 浓度 ≤ 1.3e-3、Cl/N/Na 2e-4、孔隙率 2.7e-6、pH 3e-5；水头对不上（同原 notebook） | 浓度 1.3e-3、水头 2.5e-3 |

和原 notebook 不是逐位相同：GEMS 对输入第 15 位有效数字的变化就会给出 1e-6 量级不同的解（单节点测过），
组装顺序、求和顺序一变，结果就在 GEMS 的收敛容差内漂动。和 OGS 参考的误差水平没有变。详见 `复现问题记录.md`。
