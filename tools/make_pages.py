"""Write _config.yml and _toc.yml for each language folder that exists (en first; zh, de follow)."""
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
META = {
    'en': dict(title='FEniCSx + GEMS reactive transport', sphinx_lang='en',
               parts=['Getting started', 'How the coupling works', 'case.yaml reference', 'Browser tools',
                      'Tutorials', 'Results', 'Verification', 'Reference']),
    'zh': dict(title='FEniCSx + GEMS 反应运移', sphinx_lang='zh_CN',
               parts=['入门', '耦合原理', 'case.yaml 参考', '浏览器工具', '教程', '结果', '验证', '参考']),
    'de': dict(title='FEniCSx + GEMS reaktiver Transport', sphinx_lang='de',
               parts=['Einstieg', 'Wie die Kopplung funktioniert', 'case.yaml-Referenz', 'Browser-Werkzeuge',
                      'Tutorials', 'Ergebnisse', 'Verifikation', 'Referenz']),
}
CHAPTERS = [
    ['install'],
    ['coupling/overview', 'coupling/numerics', 'coupling/performance'],
    ['yaml/index', 'yaml/chemistry', 'yaml/transport', 'yaml/coupling_output', 'yaml/from_gems'],
    ['tools/case_builder', 'tools/inspector'],
    ['tutorials/01_tracer_diffusion', 'tutorials/02_single_equilibrium', 'tutorials/03_nacl_diffusion',
     'tutorials/04_cement_leaching', 'tutorials/05_calcite_dolomite'],
    ['outputs'],
    ['verification/index', 'verification/01_hayekit', 'verification/02_calcite', 'verification/03_opc_quartz',
     'verification/04_comedy2d', 'verification/05_concretecrack'],
    ['sources'],
]
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
    for caption, files in zip(m['parts'], CHAPTERS):
        toc += [f'  - caption: "{caption}"', '    chapters:'] + [f'      - file: {f}' for f in files]
    (BOOK / lang / '_toc.yml').write_text('\n'.join(toc) + '\n')
print('pages:', LANGS)
