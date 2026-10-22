# `chemistry`: GEMS-Projekt und Rezepte

Wird von `chemistry.py` gelesen. Im Modus `diffusion` muss der Abschnitt vorhanden sein, wird aber nicht verwendet.

```yaml
chemistry:
  project: chemistry_data/b_time0-dat.lst
  temperature: 298.15
  pressure: 100000
  aqueous_phase: aq_gen
  solid_phases: [CSHQ, Portlandite, Silica-amorph]
  gibbs: {H2O@: -237183.0, Ca+2: -552400.0}
  initial: {Ca: 1.119, Si: 0.310, H: 58.52, O: 31.00, Cl: 1.0e-15}
  inlet:   {Ca: 0.0146, Cl: 0.0292, H: 111.0, O: 55.51, Si: 0.000183}
  start: cold          # optional
  on_failure: stop     # optional
```

## Schlüssel

| Schlüssel | nötig | Wert | Bedeutung |
|---|---|---|---|
| `project` | ja | Pfad | die GEMS-Datei `*-dat.lst`, relativ zu `case.yaml`. JSON- (`-j`) und Text-Exporte (`-t`) funktionieren |
| `temperature` | ja | K, > 0 | Temperatur jedes Gleichgewichts |
| `pressure` | ja | Pa, > 0 | Druck jedes Gleichgewichts |
| `aqueous_phase` | ja | Phasenname | die Phase, deren Elemente transportiert werden, meist `aq_gen` |
| `solid_phases` | ja | Liste von Phasennamen, darf `[]` sein | Phasen in der Ausgabe; **ihre Volumina bestimmen die Porositätsänderung** |
| `gibbs` | ja | `{Spezies: J/mol}`, darf `{}` sein | überschreibt molare Standard-Gibbs-Energien, nur im Speicher |
| `initial` | ja* | Rezept oder `{Zone: Rezept}` | das Material bei t = 0 |
| `inlet` | wenn ein Rand `dirichlet` ist | Rezept, Zonenname oder `{left: …, right: …}` | die Lösung an Dirichlet-Rändern |
| `start` | nein, Standard `cold` | `cold` / `warm` | wie GEMS bei jedem Aufruf startet, siehe [Numerik](../coupling/numerics.md) |
| `on_failure` | nein, Standard `stop` | `stop` / `skip` | was geschieht, wenn eine Zelle nicht konvergiert |

\* `initial` darf im Modus diffusion `{}` sein.

## Rezepte

Ein Rezept gibt **Elementmengen in mol pro 1 dm³ Gesamtmaterial** an: Porenwasser plus Feststoffe plus inertes Material.

```yaml
initial:
  Ca: 1.119218076064     # mol/dm3 Gesamtvolumen
  Si: 0.31000148638994
  H: 58.52226105076      # enthält das Wasser: 0,5 dm3 Wasser = 27,75 mol H2O -> 55,5 mol H ...
  O: 31.00037832923
  Cl: 1.0e-15            # Spur, damit das Element vorhanden ist
```

- **Element**namen des GEMS-Projekts verwenden (`Ca`, `Si`, …), keine Oxide oder Spezies.
- `Zz` (Ladung) weglassen. Nicht genannte Elemente sind 0.
- **Das Wasser mitzählen.** H und O im Rezept sind die des Wassers plus die in Feststoffen und gelösten Spezies.
- Soll ein Element später verfügbar sein, etwa Cl, das vom Rand kommt, eine winzige Menge wie `1.0e-15` angeben. Das hält das GEMS-Problem
  wohldefiniert.
- Das Porenwasser des Rezepts sollte zu `transport.material.phi` passen: ein Rezept mit 0,5 dm³ Wasser pro dm³ gehört zu `phi: 0.5`.
  **water mismatch** in der Zusammenfassung meldet die Abweichung.

[Von GEMS-Selektor zum Rezept](from_gems.md) zeigt, wie man diese Zahlen aus einem exportierten GEMS-Zustand erhält.

### Mehrere Materialien: ein Rezept pro Zone

Mit [`transport.zones`](transport.md) kann `initial` Zonennamen auf Rezepte abbilden:

```yaml
chemistry:
  initial:                 # Zahlen nur zur Illustration; die Elemente müssen im Projekt vorkommen
    clay:   {Ca: 0.01, Si: 0.6, H: 57.0, O: 30.0, Na: 0.2, Cl: 0.2}
    cement: {Ca: 1.12, Si: 0.31, H: 58.5, O: 31.0, Cl: 1.0e-15}
```

Jede Zone braucht ein Rezept. Im Modus `chemistry`, der kein Gitter hat, wird das erste Rezept verwendet.

## Randlösung: `inlet`

`inlet` wird zu Beginn einmal ins Gleichgewicht gebracht. Seine Porenwasserkonzentrationen werden dann an jedem `dirichlet`-Rand festgehalten.
Es gibt drei Formen:

```yaml
inlet: {Ca: 0.0146, Cl: 0.0292, H: 111.0, O: 55.5}   # 1. ein Rezept (ca. 1 dm3 Lösung), auf beiden Seiten
inlet: clay                                          # 2. das Gleichgewichts-Porenwasser einer Zone
inlet:                                               # 3. je Seite, jeweils eine der beiden Formen
  left: {Na: 0.1, Cl: 0.1, H: 111.0, O: 55.5}
  right: cement
```

Bei einem inlet-Rezept gelten die Mengen pro GEMS-System, normalerweise etwa 1 dm³ Wasser. Der Code teilt durch das Volumen der wässrigen Phase aus
GEMS; die genaue Wassermenge spielt also keine Rolle, solange das Verhältnis von gelösten Stoffen zu Wasser stimmt. Ohne `dirichlet`-Rand `inlet` weglassen.

## Phasennamen und `solid_phases`

`aqueous_phase` und jeder Eintrag in `solid_phases` müssen Phasennamen des Projekts sein, sonst bricht der Lauf mit *Unknown GEMS phase* ab.
Nicht aufgeführte Phasen nehmen weiter am Gleichgewicht teil, aber

- ihre Mengen erscheinen nicht in `profiles.csv`, und
- ihr Volumen zählt **nicht** zur Porositätsänderung.

Mit `update_porosity` also jeden Feststoff aufführen, der sich bilden oder lösen kann.

## `gibbs`

```yaml
gibbs: {H2O@: -237183.0, Ca+2: -552400.0}    # J/mol bei der Rechentemperatur
```

Überschreibt $G^\circ$ der genannten **Spezies** nach dem Laden des Projekts; die Dateien bleiben unverändert. Damit lässt sich ein Benchmark nachrechnen,
der leicht andere Daten verwendet hat. Sonst `gibbs: {}` lassen. [Tutorial 2](../tutorials/02_single_equilibrium.ipynb) zeigt die Wirkung.

## Wenn GEMS nicht konvergiert

Eine Zelle gilt als gelöst, wenn GEMS Status 2 oder 6 meldet **und** die vorgegebenen Elementmengen auf 1e-8 reproduziert. Sonst:

1. mit `start: warm`: neuer Versuch vom letzten Zustand der Zelle, Annäherung an die neue Zusammensetzung in vier Schritten;
2. Kaltstarts mit skalierter Größe (×1, ×1, ×10, ×100, ×0,1, ×0,01);
3. weiter erfolglos: `on_failure: stop` beendet den Lauf und schreibt `failure.txt` mit Schritt, Zelle, Position und Zusammensetzung.
   `on_failure: skip` lässt diese Zelle in diesem Schritt unreagiert. Ihre Gesamtmengen bleiben unverändert, die Masse ist also weiter erhalten.
   Jedes Überspringen wird protokolliert und gezählt.

Das Anfangsgleichgewicht (Schritt 0) bricht bei Misserfolg immer ab.
