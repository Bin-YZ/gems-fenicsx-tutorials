# `transport`：网格、材料、边界

由 `transport.py` 读取。`chemistry` 模式下不使用，只把 `geometry.length` 当作参考长度。

```yaml
transport:
  geometry: {length: 0.004, cells: 40}
  material: {phi: 0.5, De: 5.0e-15}          # 加 darcy_flux 即有对流
  zones: [...]                               # 可选
  components: [tracer]                       # 仅 diffusion 模式
  initial: {tracer: 0.0}                     # 仅 diffusion 模式
  boundary:
    left:  {type: dirichlet, concentrations: {tracer: 1.0}}
    right: {type: no_flux,   concentrations: {tracer: 0.0}}
  solver: {ksp_type: preonly, pc_type: lu, rtol: 1.0e-10, max_iterations: 1000}
```

## `geometry`

| 键 | 取值 | 含义 |
|---|---|---|
| `length` | m，> 0 | 柱长；x 从 0（左）到 `length`（右） |
| `cells` | 整数 ≥ 1 | 等宽单元数；$h$ = length / cells |

运行时间随 `cells` 线性增长，因为每个单元每一步都要调用一次 GEMS。

## `material`

| 键 | 取值 | 含义 |
|---|---|---|
| `phi` | 0 < φ ≤ 1 | 初始孔隙率 |
| `De` | m²/s，> 0 | 初始有效扩散系数（通量 $= -D_e\,\partial_x c$） |
| `darcy_flux` | m/s，≥ 0，可选 | 指向 $+x$ 的 Darcy 通量 $q = \phi v$；省略或为 0 即纯扩散 |

`darcy_flux > 0` 时，左边界必须是 `dirichlet`（入流），右边界为 `outflow` 或 `dirichlet`。

## 分区（zones）

分区把柱子分成几种材料，各有自己的 φ、De，并通过 `chemistry.initial` 各有自己的配方：

```yaml
transport:
  zones:
    - {name: clay,   from: 0.0,  to: 0.25, phi: 0.51, De: 5.1e-10}
    - {name: cement, from: 0.25, to: 0.5,  phi: 0.52, De: 5.2e-10}
```

| 键 | 含义 |
|---|---|
| `name` | 唯一的分区名，供 `chemistry.initial` 和 `chemistry.inlet` 使用 |
| `from`、`to` | m；单元 **中心** 落在 `[from, to)` 内即属于该分区；默认 0 和 `length` |
| `phi`、`De` | 可选；否则用 `material.phi` / `material.De` |

每个分区至少要包含一个单元中心。不在任何分区内的单元使用 `material` 的值。两个分区之间的扩散系数取两侧单元的调和平均。

## `boundary`

`left`（x = 0）和 `right`（x = length）各有一个 `type`：

| 类型 | 条件 | `coupled` 模式下 |
|---|---|---|
| `dirichlet` | 边界孔隙水组成固定；扩散交换（有流动时还有对流交换） | 组成来自 `chemistry.inlet` |
| `no_flux` | 无物质通过 | – |
| `outflow` | 水以单元的组成随对流流出；扩散梯度为零 | 配合 `darcy_flux` 用于下游端 |

`concentrations`（mol/m³ 孔隙水，每个示踪剂一个值）**只在 diffusion 模式下**用于 `dirichlet` 边界。coupled 模式下所有 Dirichlet 边界都使用 `chemistry.inlet`，这些值被忽略。

## 示踪剂：`components` 和 `initial`（diffusion 模式）

```yaml
components: [tracer, salt]           # 任意名称，Zz 除外
initial: {tracer: 0.0, salt: 0.5}    # mol/m3 孔隙水，每个组分都要给
```

在 `coupled` 和 `chemistry` 模式下，输运的名称就是 GEMS 元素，这两个键被忽略。

## `solver`

| 键 | 示例中的值 | 含义 |
|---|---|---|
| `ksp_type` | `preonly` | PETSc Krylov 方法；`preonly` 表示只应用一次预条件子 |
| `pc_type` | `lu` | PETSc 预条件子；`lu` 为直接分解 |
| `rtol` | `1.0e-10` | 相对容差（迭代法） |
| `max_iterations` | `1000` | 迭代次数上限（迭代法） |

一维网格保持 `preonly` + `lu` 即可。输运求解不收敛，或出现低于 −1e-12 mol/m³ 的浓度时，运行停止。
