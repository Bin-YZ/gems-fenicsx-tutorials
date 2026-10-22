# 浓度 ↔ 质量、孔隙率和初始化

输运用浓度（每 m³ 流体的 mol），GEMS 用物质的量（每个节点的 mol）。OGS 用两个函数在二者之间换算；模板逐行照抄。

## 浓度 → 质量（GEMS 之前）

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/gems_ogs.py
:language: python
:pyobject: OGSGEMS.concentration_to_mass
```

输运后的浓度乘以节点在输运*之前*的流体体积 $V_f$，负值取绝对值，加回溶剂水，很小的总量设成 $10^{-16}$（GEMS 处理不了零）。

## 质量 → 浓度（GEMS 之后）

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/gems_ogs.py
:language: python
:pyobject: OGSGEMS.mass_to_concentration
```

- **孔隙率** $\phi = 1 - \sum V_\text{固相}$（OGS `CalcPorosity`；节点体积是 1 m³），限制在 `[MIN_POROSITY, MAX_POROSITY]` 之间。
- GEMS 给出自己的水相体积 $V_{aq}$，它从来不正好等于 $\phi$。接下来怎么处理由 `hydrology` 选项决定：

| `hydrology` | OGS 输入 | 规则 |
|---|---|---|
| `'full'` | `$FLAG_COUPLING_HYDROLOGY 1` | 整个水相乘 $\phi/V_{aq}$；$V_f = \phi$；差值 $V_{aq}-\phi$ 作为水流源项 |
| `'hayekit'` | `$FLAG_HAYEKIT 1` | 只缩放溶剂水 |
| `'none'` | `$FLAG_COUPLING_HYDROLOGY 0` | 不缩放；$c = b_{aq}/V_{aq}$，之后 $b = b_\text{fix} + c\,\phi$ |

## 初始化

OGS-GEM 有两种开始方式：

- **从总 b 向量开始**（`.ic` 文件）——`init_from_bulk`。OGS 先算一次 GEMS，把 b 向量除以得到的体系体积 $V_s$，
  让每个节点正好是 1 m³，再算一次（两遍）；
- **从重启文件开始**（`$RELOAD`）——`init_from_restart`。读入保存的孔隙率、流体体积、`b_fix`、物种量和动力学上下限，
  用它们算一次 GEMS。好几个基准（HAYEKIT、comedy2d、TransLay2d）只有从重启状态开始才有意义。
