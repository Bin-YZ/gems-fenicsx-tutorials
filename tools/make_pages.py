"""Write _config.yml and _toc.yml for each language folder that exists (en first; zh, de follow)."""
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
# Sidebar: one part per caption, each entry (file, short title per language).
# Short titles keep the sidebar to one line per page; the page itself keeps its full heading.
NAV = [
    (('Getting started', '入门', 'Einstieg'), [
        ('install', 'Installation', '安装', 'Installation'),
        ('outputs', 'Output files and troubleshooting', '输出文件与排错', 'Ausgabe und Fehlersuche')]),
    (('Concepts', '原理', 'Grundlagen'), [
        ('coupling/overview', 'How the coupling works', '耦合原理', 'Wie die Kopplung funktioniert'),
        ('coupling/numerics', 'Equations and numerics', '方程与数值方法', 'Gleichungen und Numerik'),
        ('coupling/performance', 'Speeding up a run', '加快计算', 'Rechnungen beschleunigen')]),
    (('Input file: case.yaml', '输入文件 case.yaml', 'Eingabedatei case.yaml'), [
        ('yaml/index', 'Overview', '概览', 'Überblick'),
        ('yaml/chemistry', 'chemistry', 'chemistry', 'chemistry'),
        ('yaml/transport', 'transport', 'transport', 'transport'),
        ('yaml/coupling_output', 'coupling and output', 'coupling 与 output', 'coupling und output'),
        ('yaml/from_gems', 'From GEMS-Selektor to a recipe', '从 GEMS-Selektor 到配方', 'Von GEMS-Selektor zum Rezept')]),
    (('Tutorials', '教程', 'Tutorials'), [
        ('tutorials/01_tracer_diffusion', '1 · Tracer diffusion', '1 · 示踪剂扩散', '1 · Tracer-Diffusion'),
        ('tutorials/02_single_equilibrium', '2 · One chemical equilibrium', '2 · 单点化学平衡', '2 · Ein Gleichgewicht'),
        ('tutorials/03_nacl_diffusion', '3 · NaCl diffusion', '3 · NaCl 扩散', '3 · NaCl-Diffusion'),
        ('tutorials/04_cement_leaching', '4 · Cement leaching', '4 · 水泥溶蚀', '4 · Zementauslaugung'),
        ('tutorials/05_calcite_dolomite', '5 · Calcite → dolomite', '5 · 方解石 → 白云石', '5 · Calcit → Dolomit')]),
    (('Verification against OGS-GEM', '与 OGS-GEM 对比验证', 'Verifikation mit OGS-GEM'), [
        ('verification/index', 'Overview', '概览', 'Überblick'),
        ('verification/01_hayekit', 'V1 · HAYEKIT', 'V1 · HAYEKIT', 'V1 · HAYEKIT'),
        ('verification/02_calcite', 'V2 · Calcite column', 'V2 · 方解石柱', 'V2 · Calcitsäule'),
        ('verification/03_opc_quartz', 'V3 · OPC concrete + quartz', 'V3 · OPC 混凝土 + 石英', 'V3 · OPC-Beton + Quarz'),
        ('verification/04_comedy2d', 'V4 · comedy2d (2D flow)', 'V4 · comedy2d（二维流动）', 'V4 · comedy2d (2D-Strömung)'),
        ('verification/05_concretecrack', 'V5 · ConcreteCrack', 'V5 · ConcreteCrack', 'V5 · ConcreteCrack')]),
    (('Tools and references', '工具与参考', 'Werkzeuge und Quellen'), [
        ('tools/case_builder', 'Case Builder', 'Case Builder', 'Case Builder'),
        ('tools/inspector', 'GEMS Chemistry Inspector', 'GEMS Chemistry Inspector', 'GEMS Chemistry Inspector'),
        ('sources', 'Sources and credits', '来源与致谢', 'Quellen und Danksagung')]),
]
COL = {'en': 1, 'zh': 2, 'de': 3}
META = {
    'en': dict(title='FEniCSx + GEMS reactive transport', sphinx_lang='en'),
    'zh': dict(title='FEniCSx + GEMS 反应运移', sphinx_lang='zh_CN'),
    'de': dict(title='FEniCSx + GEMS reaktiver Transport', sphinx_lang='de'),
}
LANGS = [l for l in META if (BOOK / l / 'index.md').exists()]

for lang in LANGS:
    m = META[lang]
    switch = '[lang-switch.js]' if len(LANGS) > 1 else '[]'
    (BOOK / lang / '_config.yml').write_text(f"""title: "{m['title']}"
author: ""
copyright: ""
only_build_toc_files: true
exclude_patterns: [_build, "**.ipynb_checkpoints"]
execute:
  execute_notebooks: "off"
parse:
  myst_enable_extensions: [dollarmath, amsmath, colon_fence, deflist, html_image]
html:
  use_repository_button: false
  use_issues_button: false
  home_page_in_navbar: true
sphinx:
  config:
    language: {m['sphinx_lang']}
    myst_heading_anchors: 3
    mathjax_path: mathjax/tex-mml-chtml.js
    html_js_files: {switch}
    html_css_files: [lang-switch.css]
    html_show_copyright: false
    html_last_updated_fmt: ""
    suppress_warnings: ["myst.header", "mystnb.unknown_mime_type"]
""")
    toc = ['format: jb-book', 'root: index', 'parts:']
    k = COL[lang]
    for captions, entries in NAV:
        toc += [f'  - caption: "{captions[k - 1]}"', '    chapters:']
        toc += [f'      - file: {e[0]}\n        title: "{e[k]}"' for e in entries]
    (BOOK / lang / '_toc.yml').write_text('\n'.join(toc) + '\n')
print('pages:', LANGS)
