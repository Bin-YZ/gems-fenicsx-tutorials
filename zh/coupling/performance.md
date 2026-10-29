# 加快计算

## 时间花在哪里

代码以 **一个进程、一个线程** 运行。用多于一个 MPI 进程启动时，`transport.py` 会直接停止；代码中也没有任何地方开启线程或子进程。因此每个时间步按顺序执行：

1. 输运：每个元素用 PETSc 直接求解一次；
2. 化学：Python 循环逐个单元调用 GEMS；
3. 反馈、质量守恒、输出。

一维问题中几乎所有时间都花在化学上。[教程 4](../tutorials/04_cement_leaching.ipynb) 的水泥算例需要 40 个单元 × 10 000 步 = 400 000 次 GEMS 调用，共 4.8 分钟，每次约 0.7 ms；40 个单元网格的输运求解与之相比可以忽略。

所以要省时间就得从化学步下手。化学步非常适合并行，因为 **每个单元各自平衡**：同一步内一个单元的结果不依赖任何其他单元。

## 用进程，不用线程

以水泥配方为例，在 2 个 CPU 核上计算 4000 次平衡，每个 worker 一个 GEMS 引擎：

| 运行方式 | 时间 | 加速比 | 结果 |
|---|---|---|---|
| 串行（一个引擎） | 2.4 s | 1.0 | 参考 |
| 2 个进程（`multiprocessing.Pool`） | 1.1 s | **2.1** | 完全相同（最大差 0） |
| 2 个线程（`ThreadPoolExecutor`） | 2.0 s | 0.9 | 相同，但没有变快 |

**线程没有帮助。** `xgems` 调用期间持有 Python 的全局解释器锁（GIL），两个线程只能轮流执行，而不是同时执行。何况一个 GEMS 引擎本来也不能在线程之间共享。

**进程随核数线性加速。** 每个进程有自己的解释器和自己的 GEMS 引擎。每个单元的计算约 0.5 ms，远大于把一行元素量发给 worker 的开销，所以加速比接近核数。

## 怎样把化学步并行化

当前代码没有并行选项，下面是加上它的做法：每个 worker 只加载一次 GEMS 项目，每一步把单元分成若干块：

```python
from multiprocessing import Pool
import numpy as np

_chem = None                                  # 每个 worker 进程一个 Chemistry（一个 GEMS 引擎）

def _init(config):
    global _chem
    from chemistry import Chemistry
    _chem = Chemistry(config)

def _solve_block(rows):                       # rows：(单元编号, 元素总量)
    return [(i, _chem.equilibrate(total)) for i, total in rows]

pool = Pool(processes=4, initializer=_init, initargs=(config['chemistry'],))
blocks = np.array_split(np.arange(n_cells), 4)            # 每一步都用同样的划分
for block in pool.map(_solve_block, [[(i, state['total'][i]) for i in b] for b in blocks]):
    for i, result in block:
        state['aqueous'][i] = result['aqueous']           # ……其余字段与 coupling.py 中相同
```

注意事项：

- **划分保持不变。** 使用 `chemistry.start: warm` 时，每个单元从自己上一次的平衡出发，而这个状态保存在当时算它的那个 worker 的引擎里，因此同一个单元每一步都必须分给同一个 worker。使用 `cold`（默认）时划分无所谓，结果与串行完全相同。
- **限制库内部线程。** 启动前设置 `OMP_NUM_THREADS=1`（以及 `OPENBLAS_NUM_THREADS=1`），以免 numpy 或 PETSc 在每个 worker 里再开线程、争抢同一批核。
- **worker 数不超过物理核数。** 超过核数反而更慢。
- **注意启动开销。** 进程池在时间循环之前创建一次，不要每一步都建。加载 GEMS 项目需要不到一秒。
- **错误处理不变。** worker 返回同样的结果字典，或抛出同样的 `RuntimeError`，`coupling.py` 照原样处理（`on_failure: stop` 或 `skip`）。

对二维或三维的大网格，输运也会变得昂贵。这时通常用 MPI（`mpirun -n 4`）：每个进程负责一部分网格以及这部分节点上的 GEMS 计算。OpenGeoSys-GEM 的 PETSc 基准算例就是这样运行的。这需要分布式网格和并行线性求解器，比上面的进程池改动大得多，一维代码不支持。

## 用数组，不用字典

数值求解器内部的数据通常是数组形式。GEMS3K 按固定顺序把元素量、物种量和相体积存在 C++ 数组中，FEniCSx/PETSc 的向量也是数组。凡是通过以名称为键的 **字典** 在两者之间传递的值，都要按名称查找、包装成 Python 对象、再拷回数组。这些开销每次调用都会发生，而这个循环每个单元、每个时间步都要执行一次。

`xgems` 提供两种接口：

| | 数组接口 `xgems.ChemicalEngine` | 字典接口 `xgems.ChemicalEngineDicts` |
|---|---|---|
| 输入 | `equilibrate(T, P, b)`，`b` 为按元素顺序排列的 numpy 数组 | `add_multiple_elements_amt({'Ca': …, 'Si': …})` |
| 输出 | `elementAmountsInPhase(i)`、`phaseVolumes()`、`phaseAmounts()` → 数组 | `aq_elements_moles`、`phase_volumes`、`phase_amounts` → 字典 |

对水泥配方的一次平衡，测量其前后的数据交换（设置组成，读取水相元素、相体积、矿物量和 pH）：

| | 数组 | 字典 |
|---|---|---|
| 设置组成 | 0.5 µs | 2.8 µs |
| 读取结果 | 4.5 µs | 6.3 µs |
| 每次调用合计 | **5 µs** | **9 µs** |

对这个小体系，平衡计算本身约需 500 µs，所以字典带来的额外开销约占运行时间的 1 %。当 GEMS 计算很快（小体系、热启动），或者需要交换很多数值（例如大数据库的全部物种量）时，这个比例会变大；两种情况下数组都更省时间。

`FEniCSx_GEMS` 遵循这一原则：

- 配方只在 `case.yaml` 中是字典。`Chemistry.amounts()` 在启动时 **一次性** 把每个配方转换成按 GEMS 元素顺序排列的数组。
- 状态保存在每行一个单元、每列一个元素的数组中（`state['total']`、`state['aqueous']`），输运直接处理这些数组的整列。
- `Chemistry.equilibrate()` 把数组传给 `g.equilibrate(T, P, b)`，并以数组形式读回结果。

扩展代码时的建议：

- 在时间循环 **之前** 把名称换成索引（`g.indexPhase(name)`、`names.index(element)`），循环内只用索引。`chemistry.py` 目前每次调用仍按名称查找相的索引，把它们在 `__init__` 中缓存起来就能省下这部分时间。
- 不要在单元循环里构建字典、pandas 表或 YAML。把结果收集到预先分配的 numpy 数组中，每 `output.every` 步在 `output.py` 里统一输出。
- 字典接口适合在 notebook 里探索，那时可读性比几微秒更重要。

以上测量可以用 `tools/benchmarks/` 中的脚本复现（在 `FEniCSx_GEMS/` 下运行）。
