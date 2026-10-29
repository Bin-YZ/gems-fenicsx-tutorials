# Rechnungen beschleunigen

## Wo die Zeit bleibt

Der Code läuft als **ein Prozess mit einem Thread**. `transport.py` bricht ab, wenn er mit mehr als einem MPI-Prozess gestartet wird, und nirgends
im Code werden Threads oder Arbeitsprozesse gestartet. Jeder Zeitschritt läuft daher der Reihe nach ab:

1. Transport: eine direkte PETSc-Lösung pro Element;
2. Chemie: eine Python-Schleife, die GEMS einmal pro Zelle aufruft;
3. Rückkopplung, Massenbilanz, Ausgabe.

In 1D entfällt fast die ganze Zeit auf die Chemie. Der Zementfall aus [Tutorial 4](../tutorials/04_cement_leaching.ipynb) braucht
40 Zellen × 10 000 Schritte = 400 000 GEMS-Aufrufe in 4,8 Minuten, etwa 0,7 ms pro Aufruf. Die Transportlösungen auf einem Gitter mit 40 Zellen
fallen dagegen nicht ins Gewicht.

Zeit gewinnt man also im Chemieschritt. Er lässt sich gut parallelisieren, denn **jede Zelle wird für sich ins Gleichgewicht gebracht**: Das
Ergebnis einer Zelle hängt im selben Schritt von keiner anderen Zelle ab.

## Prozesse, nicht Threads

Gemessen am Zementrezept, 4000 Gleichgewichte auf 2 CPU-Kernen, eine GEMS-Engine pro Arbeiter:

| Lauf | Zeit | Beschleunigung | Ergebnis |
|---|---|---|---|
| seriell (eine Engine) | 2,4 s | 1,0 | Referenz |
| 2 Prozesse (`multiprocessing.Pool`) | 1,1 s | **2,1** | identisch (max. Differenz 0) |
| 2 Threads (`ThreadPoolExecutor`) | 2,0 s | 0,9 | identisch, aber nicht schneller |

**Threads helfen nicht.** Die `xgems`-Aufrufe halten Pythons globale Interpretersperre (GIL), sodass zwei Threads abwechselnd statt gleichzeitig
rechnen. Eine GEMS-Engine darf ohnehin nicht zwischen Threads geteilt werden.

**Prozesse skalieren mit der Zahl der Kerne.** Jeder Prozess hat seinen eigenen Interpreter und seine eigene GEMS-Engine. Die Arbeit pro Zelle
(etwa 0,5 ms) ist viel größer als die Kosten, eine Zeile Elementmengen an einen Arbeiter zu schicken, daher liegt die Beschleunigung nahe an der Kernzahl.

## Den Chemieschritt parallelisieren

Der aktuelle Code hat keine Parallel-Option. So lässt sie sich ergänzen: Jeder Arbeiter lädt das GEMS-Projekt einmal, und die Zellen eines
Schritts werden in Blöcke geteilt:

```python
from multiprocessing import Pool
import numpy as np

_chem = None                                  # eine Chemistry (eine GEMS-Engine) pro Arbeitsprozess

def _init(config):
    global _chem
    from chemistry import Chemistry
    _chem = Chemistry(config)

def _solve_block(rows):                       # rows: (Zellindex, Elementmengen)
    return [(i, _chem.equilibrate(total)) for i, total in rows]

pool = Pool(processes=4, initializer=_init, initargs=(config['chemistry'],))
blocks = np.array_split(np.arange(n_cells), 4)            # in jedem Schritt dieselbe Aufteilung
for block in pool.map(_solve_block, [[(i, state['total'][i]) for i in b] for b in blocks]):
    for i, result in block:
        state['aqueous'][i] = result['aqueous']           # ... und die übrigen Felder wie in coupling.py
```

Worauf zu achten ist:

- **Aufteilung festhalten.** Mit `chemistry.start: warm` startet jede Zelle von ihrem eigenen vorherigen Gleichgewicht, und das liegt in der Engine des
  Arbeiters, der sie gerechnet hat. Dieselbe Zelle muss daher in jedem Schritt zum selben Arbeiter. Mit `cold` (Standard) spielt die Aufteilung keine Rolle,
  und die Ergebnisse sind identisch mit dem seriellen Lauf.
- **Bibliotheks-Threads begrenzen.** Vor dem Start `OMP_NUM_THREADS=1` (und `OPENBLAS_NUM_THREADS=1`) setzen, damit numpy oder PETSc nicht in jedem
  Arbeiter zusätzliche Threads starten und um dieselben Kerne konkurrieren.
- **Höchstens ein Arbeiter pro physischem Kern.** Mehr Arbeiter als Kerne machen den Lauf langsamer.
- **Startkosten beachten.** Den Pool einmal vor der Zeitschleife anlegen, nicht in jedem Schritt. Das Laden des GEMS-Projekts dauert Bruchteile einer Sekunde.
- **Fehlerbehandlung bleibt gleich.** Ein Arbeiter liefert dasselbe Ergebnis-Dictionary oder wirft denselben `RuntimeError`, und `coupling.py`
  behandelt ihn wie bisher (`on_failure: stop` oder `skip`).

Bei großen 2D- oder 3D-Gittern wird auch der Transport teuer. Dann ist MPI (`mpirun -n 4`) der übliche Weg: Jeder Prozess besitzt einen Teil des Gitters
und die GEMS-Aufrufe seiner Knoten. So rechnet OpenGeoSys-GEM seine PETSc-Benchmarks. Das erfordert ein verteiltes Gitter und einen parallelen linearen Löser
und ist ein größerer Umbau als der Prozess-Pool oben; der 1D-Code unterstützt es nicht.

## Arrays, nicht Dictionaries

Numerische Löser halten ihre Daten in Arrays. GEMS3K speichert Elementmengen, Speziesmengen und Phasenvolumina als C++-Arrays in fester Reihenfolge,
und FEniCSx/PETSc-Vektoren sind ebenfalls Arrays. Jeder Wert, der über ein **Dictionary** mit Namen als Schlüssel zwischen ihnen wandert, muss per Namen
nachgeschlagen, als Python-Objekt verpackt und wieder in ein Array kopiert werden. Diese Arbeit fällt bei jedem Aufruf an, in einer Schleife, die einmal pro Zelle und Schritt läuft.

`xgems` bietet beide Schnittstellen:

| | Array-Schnittstelle `xgems.ChemicalEngine` | Dictionary-Schnittstelle `xgems.ChemicalEngineDicts` |
|---|---|---|
| Eingabe | `equilibrate(T, P, b)` mit `b` als numpy-Array in Elementreihenfolge | `add_multiple_elements_amt({'Ca': …, 'Si': …})` |
| Ausgabe | `elementAmountsInPhase(i)`, `phaseVolumes()`, `phaseAmounts()` → Arrays | `aq_elements_moles`, `phase_volumes`, `phase_amounts` → Dictionaries |

Gemessen für den Datenaustausch um ein Gleichgewicht des Zementrezepts (Zusammensetzung setzen, gelöste Elemente, Phasenvolumina, Mineralmengen und pH lesen):

| | Array | Dictionary |
|---|---|---|
| Zusammensetzung setzen | 0,5 µs | 2,8 µs |
| Ergebnisse lesen | 4,5 µs | 6,3 µs |
| gesamt pro Aufruf | **5 µs** | **9 µs** |

Für dieses kleine System dauert das Gleichgewicht selbst etwa 500 µs; der Mehraufwand des Dictionaries macht also etwa 1 % der Rechenzeit aus. Er wächst,
wenn GEMS schnell ist (kleine Systeme, Warmstarts) oder viele Werte ausgetauscht werden, etwa alle Speziesmengen einer großen Datenbank. In beiden Fällen
bleibt der Array-Weg günstiger.

`FEniCSx_GEMS` folgt dieser Regel:

- Rezepte sind nur in `case.yaml` Dictionaries. `Chemistry.amounts()` wandelt jedes Rezept beim Start **einmal** in ein Array in GEMS-Elementreihenfolge um.
- Der Zustand liegt in Arrays mit einer Zeile pro Zelle und einer Spalte pro Element (`state['total']`, `state['aqueous']`). Der Transport arbeitet auf ganzen
  Spalten dieser Arrays.
- `Chemistry.equilibrate()` übergibt ein Array an `g.equilibrate(T, P, b)` und liest Arrays zurück.

Regeln für eigene Erweiterungen:

- Namen **vor** der Zeitschleife in Indizes übersetzen (`g.indexPhase(name)`, `names.index(element)`) und in der Schleife nur Indizes verwenden. In
  `chemistry.py` werden die Phasenindizes noch bei jedem Aufruf über den Namen gesucht; sie in `__init__` zwischenzuspeichern ist eine einfache Einsparung.
- In der Schleife über die Zellen keine Dictionaries, pandas-Tabellen oder YAML aufbauen. Ergebnisse in vorab angelegten numpy-Arrays sammeln und die Ausgabe
  alle `output.every` Schritte in `output.py` schreiben.
- Die Dictionary-Schnittstelle eignet sich zum Erkunden im Notebook, wo Lesbarkeit wichtiger ist als Mikrosekunden.

Die Messungen lassen sich mit den Skripten in `tools/benchmarks/` wiederholen (aus `FEniCSx_GEMS/` starten).
