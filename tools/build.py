"""Build the three language versions into _site/{en,zh,de}; _site/index.html redirects to English.

    python tools/build.py            (all languages)
    python tools/build.py en         (one language)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
SITE = BOOK / '_site'
langs = sys.argv[1:] or ['en', 'zh', 'de']
env = dict(os.environ, PYTHONPATH=str(BOOK / 'GEMS_FEniCSx_OGS5_Template'))
SITE.mkdir(exist_ok=True)
for lang in langs:
    src = BOOK / lang
    shutil.copytree(BOOK / 'tools' / 'static', src / '_static', dirs_exist_ok=True)
    shutil.copytree(BOOK / 'figures', src / 'figures', dirs_exist_ok=True)
    r = subprocess.run(['jupyter-book', 'build', '--all', str(src)], env=env, capture_output=True, text=True)
    for line in (r.stdout + r.stderr).splitlines():
        if ('WARNING' in line or 'ERROR' in line) and 'ParserConfig' not in line:
            print(f'[{lang}]', line)
    if r.returncode:
        sys.exit(f'build of {lang} failed')
    # theme translation catalogues and source maps are only used at build time
    shutil.copytree(src / '_build' / 'html', SITE / lang, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('locales', '*.map', '.buildinfo', '.doctrees'))
(SITE / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>GEMS + FEniCSx tutorials</title>\n'
                                 '<meta http-equiv="refresh" content="0; url=en/index.html">\n'
                                 '<a href="en/index.html">GEMS + FEniCSx tutorials</a>\n')
(SITE / '.nojekyll').touch()
print('built', SITE)
