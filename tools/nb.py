"""Tiny helper: one notebook source with markdown in three languages, code shared.

    nb = NB()
    nb.md(en='...', zh='...', de='...')
    nb.code('...')
    nb.save('xx')            -> _build_src/xx.ipynb (English markdown, to be executed)
    localize('xx')           -> en|zh|de/tutorials/xx.ipynb from the executed notebook
"""
import json
from pathlib import Path
import nbformat as nbf

BOOK = Path(__file__).resolve().parents[1]
LANGS = ('en', 'zh', 'de')
SRC = BOOK / '_build_src'


class NB:
    def __init__(self):
        self.cells = []

    def md(self, en, zh, de):
        self.cells.append(('md', {'en': en.strip('\n'), 'zh': zh.strip('\n'), 'de': de.strip('\n')}))

    def code(self, src):
        self.cells.append(('code', src.strip('\n')))

    def save(self, name):
        SRC.mkdir(exist_ok=True)
        nb = nbf.v4.new_notebook()
        nb.cells = [nbf.v4.new_markdown_cell(c['en']) if k == 'md' else nbf.v4.new_code_cell(c) for k, c in self.cells]
        nb.metadata['kernelspec'] = {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}
        nbf.write(nb, SRC / f'{name}.ipynb')
        (SRC / f'{name}.texts.json').write_text(json.dumps([c for k, c in self.cells if k == 'md'], ensure_ascii=False))


def localize(name):
    """Copy the executed notebook into the three books, swapping the markdown text."""
    executed = nbf.read(SRC / f'{name}.executed.ipynb', as_version=4)
    texts = json.loads((SRC / f'{name}.texts.json').read_text())
    for lang in LANGS:
        nb = nbf.from_dict(json.loads(json.dumps(executed)))
        k = 0
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                cell.source = texts[k][lang]
                k += 1
        assert k == len(texts)
        out = BOOK / lang / 'tutorials' / f'{name}.ipynb'
        out.parent.mkdir(parents=True, exist_ok=True)
        nbf.write(nb, out)
