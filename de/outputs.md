# Ergebnisse und Fehlersuche

## Dateien in `output.folder`

| Datei | geschrieben | Inhalt |
|---|---|---|
| `summary.txt` | Start (RUNNING), Ende | **COMPLETED** oder **FAILED**, Modus, Gitter, Endzeit, größte Bilanz-/Chemie-/Wasserfehler, Bereiche von φ und De |
| `profiles.csv` | alle `output.every` Schritte und am Ende | eine Zeile pro Zelle und Zeit (siehe unten) |
| `mass_balance.csv` | jeder Schritt | je Element: Inventar, kumulierter Randeintrag, Bilanzfehler, Chemiefehler, Wasserabweichung |
| `profiles.png` | Ende | Übersichtsbild der Profile |
| `fields.xdmf` + `fields.h5` | mit den Profilen (nicht im Modus chemistry) | dieselben Felder für ParaView |
| `simulation.log` | während des Laufs | eine Fortschrittszeile pro gespeichertem Schritt, Warnungen |
| `case_used.json` | Start | die tatsächlich verwendeten Einstellungen, mit absoluten Pfaden |
| `failure.txt` | nur bei Abbruch | Python-Traceback und Meldung |
| `xGEMS.log`, `ipmlog.txt` | von GEMS | eigene Meldungen von GEMS |

### Spalten von `profiles.csv`

```text
time_s, x_m, phi, De_m2_s, pH,
<E>_c_mol_m3_water, <E>_total_mol_m3_bulk     für jedes Element E (oder jeden Tracer)
<P>_mol_m3_bulk                               für jede Phase P in solid_phases
```

Einlesen mit pandas:

```python
import pandas as pd
p = pd.read_csv('results/profiles.csv')
last = p[p.time_s == p.time_s.max()]
last.plot(x='x_m', y=['Portlandite_mol_m3_bulk', 'CSHQ_mol_m3_bulk'])
```

Inventare in `mass_balance.csv` sind in mol pro m² Querschnitt (Menge × Zelllänge, summiert).

## Wenn etwas schiefgeht

Jeder Fehler beendet den Lauf, schreibt `failure.txt` und markiert `summary.txt` als **FAILED**. Die Meldung nennt die Ursache:

| Meldung | Ursache | was tun |
|---|---|---|
| `Use exactly four sections` | fehlender, falsch geschriebener oder zusätzlicher Schlüssel oben | `chemistry`, `transport`, `coupling`, `output` prüfen |
| `GEMS project file does not exist` | Pfad `chemistry.project` | der Pfad ist relativ zu `case.yaml` |
| `Unknown GEMS element: …` / `Unknown GEMS phase: …` | Name nicht im Projekt | Namen aus dem [Inspector](tools/inspector.md) kopieren; Groß-/Kleinschreibung beachten |
| `Initial solids plus porosity exceed the bulk volume` | Rezept enthält mehr Feststoff als 1 − φ | φ senken oder Rezept neu skalieren ([von GEMS](yaml/from_gems.md)) |
| `Chemistry failed: step=…, cell=…, x=…` | GEMS konvergiert für diese Zelle nicht | siehe unten |
| `Porosity outside (0,1]; no clipping` | so viel Fällung, dass die Poren schließen (oder umgekehrt) | kleineres `dt`; `solid_phases` prüfen; das Modell erreicht seine physikalische Grenze |
| `Invalid concentration … no clipping` | negativer Wert aus dem Transport | feineres Gitter / kleineres `dt`; bei Advektion die Randtypen prüfen |
| `Mass balance failed at step …` | Inventar ≠ Anfang + Randeintrag | sollte nicht vorkommen; mit `case_used.json` melden |
| `With flow, the left (inflow) boundary must be dirichlet` | Advektions-Setup | links `dirichlet`, rechts `outflow` oder `dirichlet` |

### GEMS konvergiert nicht

In dieser Reihenfolge:

1. Die problematische Zusammensetzung allein rechnen. `failure.txt` gibt `total_mol_dm3` aus; daraus ein Rezept machen und `mode: chemistry` verwenden.
2. Sicherstellen, dass jedes Element in `initial` **und** `inlet` mindestens eine Spur (`1.0e-15`) hat. Ein Element, das an einer Stelle genau 0 und an der
   anderen positiv ist, ist eine häufige Ursache.
3. `chemistry.start: warm` probieren: Jede Zelle startet von ihrem eigenen vorherigen Gleichgewicht.
4. `dt` verkleinern, damit sich die Zusammensetzung pro Schritt weniger ändert.
5. Als letztes Mittel `chemistry.on_failure: skip`. Fehlschlagende Zellen bleiben in diesem Schritt unreagiert, und jedes Überspringen wird protokolliert;
   am Ende von `simulation.log` steht, wie oft.

### Kleine Unterschiede zwischen Läufen

GEMS reagiert empfindlich auf Rundung: Zwei Läufe, deren Eingaben sich in der letzten Stelle unterscheiden, können bei pH oder Konzentrationen um etwa 1e-5
relativ abweichen. Unterschiede dieser Größe sind Löser-Genauigkeit, keine Änderung des Modells.
