# `coupling` 与 `output`

## `coupling`

由 `coupling.py` 读取。

```yaml
coupling:
  mode: coupled
  time:
    dt: 3155760          # s（0.1 年）
    end: 63115200        # s（2 年）
  update_porosity: true
  update_diffusivity: true
  exponent: 2.0
```

| 键 | 取值 | 含义 |
|---|---|---|
| `mode` | `diffusion` / `chemistry` / `coupled` | 运行哪些部分，见 [三种模式](../coupling/overview.md) |
| `time.dt` | s，> 0 | 输运和化学共用的时间步；最后一步会缩短以正好到达 `end` |
| `time.end` | s，> 0 | 结束时间；`chemistry` 模式下忽略 |
| `update_porosity` | `true` / `false` | 每个化学步后 $\phi = \phi_0 + V_\text{solid,0} - V_\text{solid}$ |
| `update_diffusivity` | `true` / `false` | $D_e = D_{e,0}(\phi/\phi_0)^m$；需要 `update_porosity: true` |
| `exponent` | > 0 | 上式中的 $m$；不用时也必须给 |

启动时的检查：

- `update_porosity` 需要化学，所以在 `diffusion` 模式下必须为 `false`；
- `update_diffusivity: true` 而 `update_porosity: false` 会被拒绝；
- 开启 `update_porosity` 时，初始固相加 φ 超出体相体积不得多于 0.1 %。超出说明 φ 或配方的固相含量太大。

常用换算：1 天 = 86 400 s，1 年（365.25 天）= 31 557 600 s。

## `output`

由 `output.py` 读取。

```yaml
output:
  folder: results/current     # 相对于 case.yaml；不存在则创建
  every: 5                    # 每 5 步写一次剖面（结束时总会写）
```

| 键 | 取值 | 含义 |
|---|---|---|
| `folder` | 路径 | 所有结果文件的位置；已有文件夹会被 **覆盖** |
| `every` | 整数 ≥ 1 | 每 `every` 步写一次剖面和场；质量守恒每步都写 |

想保留的每个变体都用新的 `folder`。文件夹内容见 [结果与排错](../outputs.md)。
