# Case Builder

`case_builder.html` 是一个填写 `case.yaml` 四节内容的表单。编辑时它实时显示 YAML 预览，检查基本数值和化学名称，并可 **Copy**（复制）或 **Download**（下载）结果。全部在浏览器中运行，不上传任何数据。

<p><a href="../_static/tools/case_builder.html" target="_blank" rel="noopener">在新标签页打开 Case Builder ↗</a></p>

<iframe src="../_static/tools/case_builder.html" title="Case Builder" style="width:100%;height:900px;border:1px solid #d9dfdb;border-radius:6px"></iframe>

## 使用方法

1. 从内置示例开始，或用 **Import case.yaml** 载入已有算例。
2. 在 *Chemistry* 下点击 **Choose GEMS folder**，选择包含导出的 `.lst` 和 DCH 文件（`.json` 或文本 `.dat`）的文件夹。元素、相和物种名称随后来自你的项目。注意 `chemistry.project` 要相对于你保存 `case.yaml` 的位置。
3. 填写配方、温度、压力、相和可选的 Gibbs 能；再填写几何、孔隙率、扩散系数、边界、求解器、模式、时间和反馈。表单中选的时间单位会换算成秒。
4. 检查验证信息后点 **Download**，把 `case.yaml` 放在化学数据旁边，运行 `python coupling.py case.yaml`。

## 限制

表单只覆盖基本的单一材料扩散算例。它 **不** 支持分区、`darcy_flux`、`outflow` 边界、两侧不同的 `inlet` 以及 `start`/`on_failure`；导入再导出含这些设置的文件时，它们也不一定能保留。这些请参照 [`case.yaml` 参考](../yaml/index.md) 手动编辑。页面只准备输入，不运行 GEMS，也不检查配方是否收敛；检查收敛请用 `mode: chemistry`（[教程 2](../tutorials/02_single_equilibrium.ipynb)）。
