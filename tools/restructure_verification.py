"""Turn the five verification notebooks into verification reports (see i18n/verification_reports.py).

    python tools/restructure_verification.py      (idempotent)

A notebook that is already a report is refreshed: the report table, the corrected sections, the
conclusions and the sentence EDITS are rewritten from i18n/verification_reports.py.
"""
import json
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
ns = {}
exec((BOOK / 'tools' / 'i18n' / 'verification_reports.py').read_text(encoding='utf-8'), ns)


def md(text):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': text.strip('\n').splitlines(keepends=True)}


def refresh(nb, name, lang, first):
    i = first.index(ns['PROBLEM'][lang])
    nb['cells'][0] = md(ns['HEAD'][name][lang] + first[i:])
    fix = ns['FIX'].get(name, {}).get(lang)
    for k, c in enumerate(nb['cells']):
        if c['cell_type'] != 'markdown':
            continue
        src = ''.join(c['source'])
        if fix and src.startswith(fix[0]):
            src = fix[1]
        for old, new in ns['EDITS'].get(name, {}).get(lang, []):
            src = src.replace(old, new)
        if src != ''.join(c['source']):
            nb['cells'][k] = md(src)
    nb['cells'][-1] = md(ns['CONCL'][name][lang])
    for old, new in ns['EDITS'].get(name, {}).get(lang, []):
        if not any(new in ''.join(c['source']) for c in nb['cells']):
            raise SystemExit(f'edit not applied: {lang}/{name}: {old[:60]}')


for lang in ('en', 'zh', 'de'):
    for name in ns['HEAD']:
        path = BOOK / lang / 'verification' / f'{name}.ipynb'
        nb = json.loads(path.read_text(encoding='utf-8'))
        first = ''.join(nb['cells'][0]['source'])
        if first.startswith('# V'):
            refresh(nb, name, lang, first)
            path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
            print('refreshed:', path.relative_to(BOOK)); continue
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
