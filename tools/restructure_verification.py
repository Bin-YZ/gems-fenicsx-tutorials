"""Turn the five verification notebooks into verification reports (see i18n/verification_reports.py).

    python tools/restructure_verification.py      (idempotent: skips notebooks already restructured)
"""
import json
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
ns = {}
exec((BOOK / 'tools' / 'i18n' / 'verification_reports.py').read_text(encoding='utf-8'), ns)


def md(text):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': text.strip('\n').splitlines(keepends=True)}


for lang in ('en', 'zh', 'de'):
    for name in ns['HEAD']:
        path = BOOK / lang / 'verification' / f'{name}.ipynb'
        nb = json.loads(path.read_text(encoding='utf-8'))
        first = ''.join(nb['cells'][0]['source'])
        if first.startswith('# V'):
            print('already done:', path.relative_to(BOOK)); continue
        # 1. front matter: replace title + "what you learn" by the report table, keep "the problem"
        i = first.index(ns['PROBLEM'][lang])
        nb['cells'][0] = md(ns['HEAD'][name][lang] + first[i:])
        cells = []
        for c in nb['cells']:
            src = ''.join(c['source'])
            if c['cell_type'] == 'markdown' and src.startswith(ns['EXERCISES'][lang]):
                continue                                                    # 2. no exercises
            if c['cell_type'] == 'markdown' and src.startswith(ns['PITFALLS'][lang][0]):
                c = md(src.replace(ns['PITFALLS'][lang][0], ns['PITFALLS'][lang][1], 1))   # 3. notes last
            fix = ns['FIX'].get(name, {}).get(lang)
            if fix and c['cell_type'] == 'markdown' and src.startswith(fix[0]):
                c = md(fix[1])                                              # 4. corrected text
            cells.append(c)
        # 5. conclusions after the implementation notes
        cells.append(md(ns['CONCL'][name][lang]))
        nb['cells'] = cells
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print('restructured:', path.relative_to(BOOK))
