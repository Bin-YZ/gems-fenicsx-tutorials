"""Write _config.yml, _toc.yml and all markdown pages of the three books (en, zh, de)."""
from pathlib import Path
from pages_intro import INDEX, SETUP, API_HEAD, API_BODY, SOURCES
from pages_concepts import CONCEPTS

BOOK = Path(__file__).resolve().parents[1]
TUTORIALS = ['01_hayekit', '02_calcite', '03_opc_quartz', '04_comedy2d', '05_concretecrack']
META = {
    'en': dict(title='GEMS + FEniCSx: reactive transport tutorials', sphinx_lang='en',
               parts=['Getting started', 'Concepts', 'Tutorials', 'Reference']),
    'zh': dict(title='GEMS + FEniCSx：反应运移教程', sphinx_lang='zh_CN',
               parts=['入门', '概念', '教程', '参考']),
    'de': dict(title='GEMS + FEniCSx: Tutorials zum reaktiven Transport', sphinx_lang='de',
               parts=['Einstieg', 'Konzepte', 'Tutorials', 'Referenz']),
}

for lang, m in META.items():
    d = BOOK / lang
    (d / 'concepts').mkdir(parents=True, exist_ok=True)
    (d / 'tutorials').mkdir(parents=True, exist_ok=True)
    (d / '_config.yml').write_text(f"""title: "{m['title']}"
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
  extra_extensions: [sphinx.ext.autodoc, sphinx.ext.napoleon]
  config:
    language: {m['sphinx_lang']}
    mathjax_path: mathjax/tex-mml-chtml.js
    html_js_files: [lang-switch.js]
    html_css_files: [lang-switch.css]
    html_show_copyright: false
    html_last_updated_fmt: ""
    autodoc_mock_imports: [xgems, dolfinx, ufl, basix, mpi4py, petsc4py]
    autodoc_member_order: bysource
    suppress_warnings: ["myst.header", "mystnb.unknown_mime_type"]
""")
    p = m['parts']
    (d / '_toc.yml').write_text(f"""format: jb-book
root: index
parts:
  - caption: {p[0]}
    chapters:
      - file: setup
  - caption: {p[1]}
    chapters:
""" + ''.join(f"      - file: concepts/{slug}\n" for slug, _ in CONCEPTS) + f"""  - caption: {p[2]}
    chapters:
""" + ''.join(f"      - file: tutorials/{t}\n" for t in TUTORIALS) + f"""  - caption: {p[3]}
    chapters:
      - file: api
      - file: sources
""")
    (d / 'index.md').write_text(INDEX[lang].strip() + '\n')
    (d / 'setup.md').write_text(SETUP[lang].strip() + '\n')
    (d / 'api.md').write_text(API_HEAD[lang] + API_BODY)
    (d / 'sources.md').write_text(SOURCES[lang].strip() + '\n')
    for slug, text in CONCEPTS:
        (d / 'concepts' / f'{slug}.md').write_text(text[lang].strip() + '\n')
print('pages written')
