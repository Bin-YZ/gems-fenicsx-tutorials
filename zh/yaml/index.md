# `case.yaml` 概览

一个文件描述整个模拟。它 **恰好有四个顶层节**，每节对应一个模块。多一节或少一节都会停止运行，并提示 *Use exactly four sections*。

```yaml
chemistry:   # chemistry.py  GEMS 项目、条件、相、配方
transport:   # transport.py  几何、材料、分区、边界、求解器
coupling:    # coupling.py   模式、时间步、孔隙率/扩散系数反馈
output:      # output.py     结果文件夹、剖面输出频率
```

| 页面 | 键 |
|---|---|
| [chemistry](chemistry.md) | `project`、`temperature`、`pressure`、`aqueous_phase`、`solid_phases`、`gibbs`、`initial`、`inlet`、`start`、`on_failure` |
| [transport](transport.md) | `geometry`、`material`（`phi`、`De`、`darcy_flux`）、`zones`、`components`、`initial`、`boundary`、`solver` |
| [coupling 与 output](coupling_output.md) | `mode`、`time`、`update_porosity`、`update_diffusivity`、`exponent`；`folder`、`every` |
| [从 GEMS-Selektor 到配方](from_gems.md) | `initial` 和 `inlet` 中的数字从哪里来 |

## 默认算例

这是 `FEniCSx_GEMS/case.yaml`：水泥浆体与 CaCl₂ 溶液接触，开启孔隙率和扩散系数反馈。

```{literalinclude} ../../FEniCSx_GEMS/case.yaml
:language: yaml
```

## 省时间的规则

- **路径相对于 `case.yaml` 文件**，而不是启动 Python 的位置。适用于 `chemistry.project` 和 `output.folder`。
- **单位用国际单位制**（m、s、K、Pa、m²/s、m/s）。唯一的例外是化学配方：每 **dm³ 体相** 材料的 mol 数。
- **浮点数写小数点：** 写 `1.0e-15`，不要写 `1e-15`。PyYAML 会把 `1e-15` 读成字符串。大多数键之后会被转换，但写小数点可以避免意外。
- **整数必须是整数：** `cells: 40`、`every: 5`，不要写 `40.0`。
- 反馈开关用 **`true`/`false`**，不要用 `yes`/`1`。
- **名称区分大小写**，必须与 GEMS 项目一致：`Ca`、`Portlandite`、`aq_gen`。
- `{a: 1, b: 2}` 与分两行缩进写 `a: 1`、`b: 2` 相同，`[A, B]` 是列表，注释以 `#` 开头。
- **保留但用不到的键会被忽略**，例如 coupled 模式下的 `transport.components`。示例文件保留它们，这样切换模式只需改一行。

## 建立新算例的步骤

1. 复制一个与你的问题接近的示例文件夹（见 [教程](../tutorials/01_tracer_diffusion.ipynb)）。
2. 把你的 GEMS 项目文件放进去，让 `chemistry.project` 指向 `.lst` 文件。
3. 先用 `mode: chemistry` 运行一次，检查配方和相名称。
4. 用 `mode: diffusion` 在不调用 GEMS 的情况下检查网格、时间步和边界。
5. 切换到 `mode: coupled`。先用较短的 `end`，看 `summary.txt` 和 `profiles.png`，再算完整时间。
6. 每个新变体之前改一下 `output.folder`，以免覆盖旧结果。每个结果文件夹中的 `case_used.json` 记录了该次运行的完整设置。
