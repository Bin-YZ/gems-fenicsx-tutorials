# FEniCSx + GEMS reactive transport tutorials

网站地址：<https://bin-yz.github.io/gems-fenicsx-tutorials/>（英文 / 中文 / 德文）

内容：FEniCSx 与 GEMS 如何耦合、`case.yaml` 怎么写、五篇由浅入深的教程，以及与 OpenGeoSys-GEM 的五个验证算例。

## 仓库结构

```text
FEniCSx_GEMS/                 耦合代码（coupling / transport / chemistry / output + case.yaml + 示例）
GEMS_FEniCSx_OGS5_Template/   OGS-GEM 验证算例用的模板
en/  zh/  de/                 三种语言的网页源文件（Markdown + 已执行的 notebook）
figures/                      网页插图
tools/                        生成教程、构建网站的脚本
  tut_0*.py                   教程 notebook 的源（英文正文 + 代码）
  i18n/*.py                   教程正文的中文、德文翻译
  execute.sh                  生成 → 执行 → 分发到三种语言
  make_pages.py, build.py     写 _config/_toc，构建 _site/
.github/workflows/deploy.yml  推送到 main 后自动构建并发布到 GitHub Pages
```

## 修改与发布

- 改文字：直接编辑 `en/`、`zh/`、`de/` 下的 `.md`；教程正文改 `tools/tut_0*.py`（英文）和 `tools/i18n/`（中/德），然后
  `cd tools && python3 tut_0X_*.py && python3 -c "from nb import localize; localize('0X_name')"`。
- 重新计算教程（需要带 PETSc 的 dolfinx、xgems、pyyaml，并注册名为 `fx` 的 Jupyter kernel）：
  `tools/execute.sh 03_nacl_diffusion tut_03_nacl demo_NaCl_diffusion`。
- 本地预览：`pip install "jupyter-book<2"`，然后 `python tools/make_pages.py && python tools/build.py`，打开 `_site/index.html`。
- 发布：推送到 `main` 即可（仓库 Settings → Pages → Source 选 GitHub Actions）。GitHub 上不重新执行 notebook，只渲染已保存的结果。

OGS 输入文件和参考结果取自 OGS5GEMDEV，使用时请引用原始文献（见网站 Sources 页）。
