# Wie die Kopplung funktioniert

Der Code teilt jeden Zeitschritt in einen **Transportschritt** und einen **Chemieschritt**. Das ist sequentielles, nicht-iteratives Operator-Splitting (SNIA).
Jedes der vier Module hat eine Aufgabe, und nur `coupling.py` spricht mit den anderen dreien:

| Modul | Abschnitt in `case.yaml` | macht | macht **nicht** |
|---|---|---|---|
| `coupling.py` | `coupling` | liest die Eingabe, hält die Arrays, Zeitschleife, aktualisiert φ und De, prüft die Erhaltung | GEMS aufrufen oder FE-Formen assemblieren |
| `transport.py` | `transport` | 1D-Gitter, Randbedingungen, ein Transportschritt pro Element | irgendetwas über Chemie wissen |
| `chemistry.py` | `chemistry` | lädt GEMS, rechnet Rezepte um, berechnet ein lokales Gleichgewicht | das Gitter kennen |
| `output.py` | `output` | schreibt CSV, XDMF, Abbildungen, Logs, Zusammenfassung und Fehlerberichte | etwas berechnen |

```{image} ../figures/coupling_loop.png
:alt: coupling.py in der Mitte, transport.py und chemistry.py rechts, case.yaml und output.py links
:width: 100%
```

## Was gespeichert wird und in welcher Einheit

Alles liegt in Arrays mit **einer Zeile pro Zelle und einer Spalte pro Element**. Die Spaltenreihenfolge ist die Elementreihenfolge des GEMS-Projekts,
z. B. `Ca, Cl, H, O, Si, Zz`.

| Array | Bedeutung | Einheit |
|---|---|---|
| `state['total']` | gesamte Menge eines Elements in der Zelle (gelöst + fest) | mol/m³ Gesamtvolumen |
| `state['aqueous']` | der gelöste Teil | mol/m³ Gesamtvolumen |
| `c = aqueous / phi` | Konzentration in Lösung | mol/m³ Porenwasser |
| `state['phi']` | Porosität | – |
| `state['De']` | effektiver Diffusionskoeffizient | m²/s |
| `state['minerals']` | Mengen der Phasen aus `chemistry.solid_phases` | mol/m³ Gesamtvolumen |

Rezepte in `case.yaml` werden in **mol pro dm³ Gesamtmaterial** angegeben, der Größe eines GEMS-Referenzsystems.
`chemistry.py` multipliziert beim Einlesen mit 1000 und teilt vor dem GEMS-Aufruf wieder durch 1000.

```{image} ../figures/cell_volume.png
:alt: Eine Zelle von 1 m³ Gesamtvolumen, aufgeteilt in Porenwasser, reaktive Minerale und inertes Material
:width: 90%
```

## Ein Zeitschritt

```python
# coupling.py, in der Zeitschleife (vereinfacht)
immobile = state['total'] - state['aqueous']           # 1. was liegen bleibt
state['aqueous'], incoming = transport.step(            # 2. den gelösten Teil bewegen
    state['aqueous'], state['phi'], state['De'], dt, boundary_c, mobile)
state['total'] = immobile + state['aqueous']            # 3. neue Gesamtmengen
for i in cells:                                         # 4. lokales Gleichgewicht
    result = chemistry.equilibrate(state['total'][i])
    state['aqueous'][i] = result['aqueous']             #    GEMS verteilt die Gesamtmenge neu
    solid[i] = result['solid']                          #    Volumenanteil der solid_phases
phi = phi0 + initial_solid - solid                      # 5. Rückkopplung (falls aktiv)
De = De0 * (phi / phi0) ** exponent
balance = inventory - initial_inventory - exchange      # 6. Erhaltungsprüfung
output.write(state, diagnostics)                        # 7. Ausgabe
```

1. **Nur Gelöstes bewegt sich.** Minerale und andere immobile Anteile werden vor dem Transport abgezogen und danach wieder addiert.
2. **Jedes Element wird transportiert**, auch H und O des Wassers. Nur die Ladung `Zz` nicht. Jedes Element ist ein eigenes lineares System mit derselben Matrix.
3. **φ und De sind während eines Transportschritts fest.** Sie werden nach der Chemie aktualisiert; der nächste Schritt verwendet die neuen Werte.
4. **Chemie ist lokal.** Jede Zelle wird für sich mit ihren Elementmengen ins Gleichgewicht gebracht. Das Gleichgewicht erhält die Gesamtmengen,
   der Chemieschritt ändert also die Massenbilanz nicht.
5. **Rückkopplung ist optional.** Ohne `update_porosity` bleibt φ auf dem Anfangswert, egal wie viel Mineral sich löst.

Im Schritt 0 gibt es keinen Transport. Das Anfangsrezept wird einmal ins Gleichgewicht gebracht, und das dabei gefundene Feststoffvolumen wird zum
Bezugswert `initial_solid` für die Porositätsänderung.

## Randlösungen

Ein `dirichlet`-Rand hält das Porenwasser auf einer festen Zusammensetzung. Im Modus `coupled` stammt sie aus `chemistry.inlet`.
Das Rezept wird zu Beginn einmal ins Gleichgewicht gebracht, und die Randkonzentration jedes Elements ist

$$
c_\text{Rand} = \frac{\text{Menge des Elements in der wässrigen Phase}}{\text{Volumen der wässrigen Phase}}
\qquad \text{(mol/m³ Wasser)}
$$

Das Randwasser bringt also neben den gelösten Stoffen auch sein eigenes H und O mit. `no_flux`-Ränder tauschen nichts aus.
`outflow` lässt Wasser nur advektiv ausströmen (siehe [transport](../yaml/transport.md)).

## Erhaltung wird geprüft, nicht angenommen

Nach jedem Schritt vergleicht `coupling.py` für jedes Element

$$
\underbrace{\textstyle\sum_\text{Zellen} \text{total}\cdot h}_\text{Inventar jetzt}
-\underbrace{\textstyle\sum_\text{Zellen} \text{total}_0\cdot h}_\text{Anfangsinventar}
-\underbrace{\textstyle\sum_\text{Schritte} \text{Randeintrag}}_\text{Austausch}
$$

in mol pro m² Querschnitt. Der Randeintrag wird getrennt aus den Randflüssen berechnet. Übersteigt die Differenz
$10^{-9} + 10^{-8}\,(|\text{Anfang}| + |\text{Austausch}|)$, **bricht** der Lauf mit `Mass balance failed` ab. Negative Konzentrationen oder
Porositäten werden ebenfalls nicht stillschweigend abgeschnitten. Jeder solche Wert beendet den Lauf und schreibt `failure.txt`.

Zwei weitere Diagnosen werden in jedem Schritt geschrieben, beenden den Lauf aber nicht:

- **chemistry error**: wie genau GEMS die vorgegebenen Elementmengen reproduziert (mol/m³);
- **water mismatch**: relative Differenz zwischen dem Volumen der wässrigen Phase in GEMS und φ. Der Transport nimmt gesättigte Poren mit dem
  Volumen φ an. GEMS berechnet das Lösungsvolumen mit seinem eigenen Dichtemodell. Einige Zehntelprozent sind normal.

## Drei Modi

`coupling.mode` bestimmt, welcher Teil der Schleife läuft:

| Modus | Transport | Chemie | typischer Zweck |
|---|---|---|---|
| `diffusion` | ja, Tracer aus `transport.components` | nein (GEMS wird nicht geladen) | Gitter, Zeitschritt und Ränder prüfen |
| `chemistry` | nein (kein Gitter) | ein Gleichgewicht von `chemistry.initial` | Rezept und Phasennamen prüfen |
| `coupled` | ja, alle Elemente außer `Zz` | jede Zelle, jeder Schritt | die eigentliche Simulation |
