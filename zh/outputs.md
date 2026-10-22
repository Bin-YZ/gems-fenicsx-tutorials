# 结果与排错

## `output.folder` 中的文件

| 文件 | 写入时机 | 内容 |
|---|---|---|
| `summary.txt` | 开始时（RUNNING）、结束时 | **COMPLETED** 或 **FAILED**、模式、网格、结束时间、最大守恒/化学/水量误差、φ 和 De 的范围 |
| `profiles.csv` | 每 `output.every` 步及结束时 | 每个单元、每个时间一行（见下） |
| `mass_balance.csv` | 每一步 | 每个元素的存量、累计边界输入、守恒误差、化学误差、水量差 |
| `profiles.png` | 结束时 | 剖面速览图 |
| `fields.xdmf` + `fields.h5` | 与剖面同时（chemistry 模式除外） | 同样的场，供 ParaView 使用 |
| `simulation.log` | 运行中 | 每个保存步一行进度、警告 |
| `case_used.json` | 开始时 | 实际使用的设置（绝对路径） |
| `failure.txt` | 仅失败时 | Python 回溯和错误信息 |
| `xGEMS.log`、`ipmlog.txt` | GEMS 写出 | GEMS 自己的信息 |

### `profiles.csv` 的列

```text
time_s, x_m, phi, De_m2_s, pH,
<E>_c_mol_m3_water, <E>_total_mol_m3_bulk     每个元素 E（或示踪剂）
<P>_mol_m3_bulk                               solid_phases 中的每个相 P
```

用 pandas 读取：

```python
import pandas as pd
p = pd.read_csv('results/profiles.csv')
last = p[p.time_s == p.time_s.max()]
last.plot(x='x_m', y=['Portlandite_mol_m3_bulk', 'CSHQ_mol_m3_bulk'])
```

`mass_balance.csv` 中的存量单位是每 m² 截面的 mol（量 × 单元长度，求和）。

## 出错时

任何失败都会停止运行、写出 `failure.txt`，并把 `summary.txt` 标为 **FAILED**。错误信息指明原因：

| 信息 | 原因 | 处理 |
|---|---|---|
| `Use exactly four sections` | 顶层键缺失、拼错或多余 | 检查 `chemistry`、`transport`、`coupling`、`output` |
| `GEMS project file does not exist` | `chemistry.project` 路径 | 路径相对于 `case.yaml` |
| `Unknown GEMS element: …` / `Unknown GEMS phase: …` | 项目中没有该名称 | 从 [Inspector](tools/inspector.md) 复制名称；区分大小写 |
| `Initial solids plus porosity exceed the bulk volume` | 配方中固相多于 1 − φ | 降低 φ 或重新缩放配方（[从 GEMS 到配方](yaml/from_gems.md)） |
| `Chemistry failed: step=…, cell=…, x=…` | 该单元 GEMS 不收敛 | 见下文 |
| `Porosity outside (0,1]; no clipping` | 沉淀过多使孔隙闭合（或相反） | 减小 `dt`；检查 `solid_phases`；模型已到物理极限 |
| `Invalid concentration … no clipping` | 输运产生负值 | 加密网格、减小 `dt`；有对流时检查边界类型 |
| `Mass balance failed at step …` | 存量 ≠ 初始 + 边界输入 | 不应出现；请连同 `case_used.json` 一起报告 |
| `With flow, the left (inflow) boundary must be dirichlet` | 对流设置 | 左边界 `dirichlet`，右边界 `outflow` 或 `dirichlet` |

### GEMS 不收敛

按以下顺序处理：

1. 单独计算出问题的组成：`failure.txt` 中打印了 `total_mol_dm3`，把它写成配方，用 `mode: chemistry` 计算。
2. 确保每个元素在 `initial` **和** `inlet` 中都至少有痕量（`1.0e-15`）。某元素在一处恰为 0、另一处为正，是常见原因。
3. 试试 `chemistry.start: warm`：每个单元从自己上一次的平衡出发。
4. 减小 `dt`，让每一步组成变化更小。
5. 最后手段：`chemistry.on_failure: skip`。失败的单元在该步不反应，每次跳过都会记录；结束时查看 `simulation.log` 中跳过了多少次。

### 两次运行的微小差异

GEMS 对舍入误差敏感：输入只差最后一位的两次运行，pH 或浓度可能有约 1e-5 的相对差异。这种量级的差异是求解器精度，不代表模型变化。
