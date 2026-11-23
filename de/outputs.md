# Ergebnisse und Fehlersuche

## Dateien in `output.folder`

| Datei | geschrieben | Inhalt |
|---|---|---|
| `summary.txt` | Start (RUNNING), Ende | **COMPLETED**, **COMPLETED WITH SKIPPED CELLS** oder **FAILED**, Modus, Gitter, GEMS-Startmodus, Zahl übersprungener Zellschritte, Endzeit, größte Bilanz-/Chemie-/Wasserfehler, Bereiche von φ und De |
| `profiles.csv` | alle `output.every` Schritte und am Ende | eine Zeile pro Zelle und Zeit (siehe unten) |
| `mass_balance.csv` | jeder Schritt | je Element: Inventar, kumulierter Randeintrag, Bilanzfehler, Chemiefehler, Wasserabweichung |
| `profiles.png` | Ende | Übersichtsbild der Profile |
| `fields.xdmf` + `fields.h5` | mit den Profilen (nicht im Modus chemistry) | gelöste Konzentrationen, φ, De und pH für ParaView (Elementmengen und Mineralmengen nur in `profiles.csv`) |
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

Jeder Fehler beendet den Lauf. Wo die Meldung erscheint, hängt vom Zeitpunkt ab:

- **Eingabeprüfungen** (`read_case`: die vier Abschnitte, Pfade, Zahlen, Modus und Rückkopplungsschalter) laufen, bevor der Ausgabeordner angelegt wird.
  Diese Fehler erscheinen nur im Terminal; es wird kein `failure.txt` geschrieben.
- **Alles nach dem Start** (Laden von GEMS und seiner Namen, Anfangsgleichgewicht, jeder Zeitschritt) schreibt `failure.txt` und markiert `summary.txt`
  als **FAILED**.

Die Meldung nennt die Ursache:

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
5. Als letztes Mittel `chemistry.on_failure: skip`. Fehlschlagende Zellen bleiben in diesem Schritt unreagiert, und jedes Überspringen wird in `simulation.log` protokolliert;
   die erste Zeile von `summary.txt` lautet dann **COMPLETED WITH SKIPPED CELLS** und nennt die Zahl übersprungener Zellschritte.

### Kleine Unterschiede zwischen Läufen

Zwei Läufe mit fast identischen Eingaben können leicht unterschiedliche Ergebnisse liefern. In den getesteten Beispielen änderten Eingaben, die sich nur in der
letzten Stelle unterschieden, die Konzentrationen um bis zu etwa 1e-5 relativ. Das ist keine allgemeine Schranke, und eine Abweichung dieser Größe ist nicht
automatisch harmlos. Bevor Sie eine Abweichung der Rundung zuschreiben, prüfen Sie:

- **Konvergenz**: keine GEMS-Fehler oder übersprungenen Zellen in `simulation.log`, und in beiden Läufen dieselben Phasen;
- **Elementbilanz-Residuen**: die Spalte *chemistry error* in `mass_balance.csv` und das Maximum in `summary.txt`;
- **Sensitivität**: ob die Abweichung bei feinerem `dt` oder Gitter kleiner wird oder an Fronten, an denen Phasen erscheinen oder verschwinden, größer.

pH-Unterschiede als absolute Werte (pH-Einheiten) angeben, nicht als relative Fehler.
