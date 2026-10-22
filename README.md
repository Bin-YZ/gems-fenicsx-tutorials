# GEMS + FEniCSx tutorials (book source)

Three-language website (English default, 中文, Deutsch) built with Jupyter Book from the five OGS5-GEM
benchmark reproductions in `GEMS_FEniCSx_OGS5_Template`.

## 结构 / Layout

```text
GEMS_FEniCSx_OGS5_Template/   模板模块 + 5 个算例的数据（notebook 从这里 import）
en/  zh/  de/                 三种语言的书：_config.yml、_toc.yml、页面、tutorials/*.ipynb（已带输出）
figures/                      概念篇的图（tools/make_figures.py 生成）
tools/
  pages_intro.py              首页、安装、API、参考文献的三语文字
  pages_concepts.py           6 篇概念页的三语文字（代码片段直接从模板 literalinclude）
  tut_0X_*.py                 每篇教程：三语说明 + 共用代码
  nb.py                       生成 notebook、执行后换语言
  execute.sh                  python tools/tut_X.py -> 执行 -> 复制到 en/zh/de
  make_pages.py               写 _config.yml、_toc.yml 和 markdown 页面
  make_figures.py             概念篇的图（用模板真算）
  build.py                    构建三种语言 -> _site/{en,zh,de}，_site/index.html 跳到英文
  static/                     语言切换按钮（lang-switch.js/css）和本地 MathJax
.github/workflows/deploy.yml  推到 GitHub 后自动构建并发布到 GitHub Pages
```

## 修改内容后

```bash
# 改了概念页、首页等文字
python tools/make_pages.py && python tools/build.py

# 改了某篇教程（需要 dolfinx + xgems 环境，会重新计算）
bash tools/execute.sh 02_calcite && python tools/build.py

# 本地预览
python -m http.server -d _site 8000     # 打开 http://localhost:8000
```

教程的代码在三种语言里完全相同，只算一次；`nb.py` 把执行好的 notebook 复制三份，只换说明文字。

## 发布到 GitHub Pages

1. 新建仓库，把这个文件夹推上去（`main` 分支）。
2. 仓库 Settings → Pages → Source 选 **GitHub Actions**。
3. 每次推送，`deploy.yml` 构建三种语言并发布；GitHub 上不重新计算 notebook，直接用存好的输出。
