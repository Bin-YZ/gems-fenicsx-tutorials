# GEMS Chemistry Inspector

`gems_inspector.html` 让你在写算例之前看懂导出的 GEMS3K 体系。它在浏览器中运行，不上传任何数据。

<p><a href="../_static/tools/gems_inspector.html" target="_blank" rel="noopener">在新标签页打开 Inspector ↗</a></p>

<iframe src="../_static/tools/gems_inspector.html" title="GEMS Chemistry Inspector" style="width:100%;height:900px;border:1px solid #d9dfdb;border-radius:6px"></iframe>

## 显示内容

点击 **Open folder…** 或 **Open files…**，也可以把文件拖到页面上。需要包含 `.lst` 及其列出的 DCH/IPM 文件。支持 JSON（`-j`）和文本（`-t`）导出，不支持二进制（`-b`）。

| 标签页 | 内容 | 用途 |
|---|---|---|
| Elements | 元素和电荷 | `initial` / `inlet` 中可用的名称 |
| Phases | 相及其物种 | `aqueous_phase`、`solid_phases` |
| Species & thermo | 可搜索的性质：组成、电荷、摩尔质量、标准数据 | `gibbs` 中的物种名 |
| Stoichiometry | 化学计量矩阵 | 核对配方 |
| Reactions | 平衡检查、ΔrG°、ΔrH°、ΔrS°、ΔrCp°、ΔrV°、log K | 例如 `Calcite = Ca+2 + CO3-2` |

在 **Reactions** 中使用准确、区分大小写的物种名，`+` 两边留空格，系数写在名称前（`2 H2O@`）。`log10 K = −ΔrG° / (R T ln 10)` 使用所选温度–压力点上存储的 DCH 数据，不做插值，也不包含算例中 `chemistry.gibbs` 的覆盖值。

检查器是只读的：不加载 DBR 状态文件，也不运行 GEMS。
