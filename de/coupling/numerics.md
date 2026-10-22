# Gleichungen und Numerik

## Transportgleichung

Für jedes transportierte Element, mit $c$ in mol/m³ Porenwasser:

$$
\frac{\partial(\phi c)}{\partial t} + \frac{\partial}{\partial x}\!\left(q\,c - D_e \frac{\partial c}{\partial x}\right) = 0,
\qquad 0 < x < L
$$

| Symbol | Schlüssel in `case.yaml` | Einheit |
|---|---|---|
| $\phi$ | `transport.material.phi` (oder je Zone), dann durch die Rückkopplung aktualisiert | – |
| $D_e$ | `transport.material.De` (oder je Zone), dann durch die Rückkopplung aktualisiert | m²/s |
| $q$ | `transport.material.darcy_flux` (Darcy-Fluss $=\phi\times$ Porengeschwindigkeit, in $+x$-Richtung) | m/s |
| $L$ | `transport.geometry.length` | m |

$D_e$ ist der **effektive** Koeffizient im Fluss; der Porendiffusionskoeffizient ist $D_p = D_e/\phi$. Alle Elemente verwenden dasselbe $D_e$.
Elektromigration ist nicht enthalten.

## Diskretisierung

- **Ort: DG0-Finite-Volumen auf einem gleichmäßigen Gitter.** `transport.geometry.cells` Zellen der Breite $h = L/n$ mit je einem Wert. Der
  Diffusionsfluss zwischen zwei Zellen verwendet das harmonische Mittel ihrer $D_e$, $D_\text{face} = 2D_e^+D_e^-/(D_e^+ + D_e^-)$. Ein
  Dirichlet-Rand liegt $h/2$ vom Mittelpunkt der ersten Zelle entfernt.
- **Advektion: Upwind erster Ordnung.** Jede Zelle gibt $q\,c$ über ihre stromabwärtige Seite ab. Upwind ist stabil und erzeugt nie negative Werte,
  verschmiert aber Fronten mit einer numerischen Dispersion von etwa $q h / 2$. Für advektive Probleme feine Gitter verwenden.
- **Zeit: implizites Euler-Verfahren.** Unbedingt stabil, erster Ordnung genau. `coupling.time.dt` ist der einzige Zeitschritt; Transport und Chemie
  verwenden denselben.
- **Linearer Löser: PETSc**, eingestellt über `transport.solver`. Der Standard `preonly` + `lu` ist ein direkter Löser und für 1D die richtige Wahl.

Die schwache Form in `transport.py` mit DG0-Testfunktionen $v$ lautet

$$
\int \phi\,\frac{c^{n+1}-c^n}{\Delta t}\,v\,dx
+ \sum_\text{Flächen} D_\text{face}\,\frac{[c^{n+1}]\,[v]}{h}
+ \text{Upwind- und Randterme} = 0 .
$$

## Rückkopplung von Porosität und Diffusivität

Mit `coupling.update_porosity: true` folgt die Porosität dem Volumen der Minerale aus `chemistry.solid_phases`:

$$
\phi = \phi_0 + V_\text{solid,0} - V_\text{solid}
$$

$V_\text{solid}$ ist ihr Volumenanteil aus GEMS, $V_\text{solid,0}$ der Wert nach dem Anfangsgleichgewicht. Lösung öffnet Poren, Fällung schließt sie.
Material, das keine GEMS-Phase ist, ist inert und ändert sich nie. Eine Porosität außerhalb von $(0, 1]$ beendet den Lauf.

Mit zusätzlich `coupling.update_diffusivity: true`:

$$
D_e = D_{e,0}\left(\frac{\phi}{\phi_0}\right)^{m}, \qquad m = \texttt{coupling.exponent}
$$

Das ist ein Archie-artiges Gesetz; der Exponent wird vorgegeben, nicht angepasst. Wenn sich φ ändert, bleiben die gelösten **Mengen** pro Gesamtvolumen
erhalten; die Konzentrationen werden als $c = \text{aqueous}/\phi$ neu berechnet.

## Wahl des Zeitschritts

Operator-Splitting fügt zum Fehler des Euler-Verfahrens einen weiteren hinzu, der mit $\Delta t$ wächst.

- **Diffusionsdominiert:** Die Front wandert pro Schritt etwa $\sqrt{D_p\,\Delta t}$. Für scharfe Mineralfronten sollte das deutlich kleiner als die
  Zellbreite $h$ sein.
- **Advektionsdominiert:** Die Courant-Zahl $q\,\Delta t / (\phi h)$ um 1 oder darunter halten. Das Euler-Verfahren bleibt auch darüber stabil,
  aber die Fronten werden breiter.
- **Durch Halbieren prüfen.** Mit halbem `dt` (und doppelten `cells`) noch einmal rechnen und die Profile vergleichen.

## Chemie: Kalt- und Warmstart

GEMS minimiert die Gibbs-Energie des Systems jeder Zelle. Standardmäßig (`chemistry.start: cold`) beginnt jeder Aufruf von vorn; das Ergebnis hängt
also weder vom vorherigen Schritt noch von Nachbarzellen ab. Meldet GEMS eine schlechte Elementbilanz, wird dasselbe System in skalierter Größe neu
gelöst (×1, ×10, ×100, ×0,1, ×0,01) und zurückskaliert, denn das Gleichgewicht hängt nicht von der Systemgröße ab.

`start: warm` gibt jeder Zelle eine eigene GEMS-Engine und startet vom vorherigen Gleichgewicht dieser Zelle. Das ist für große Systeme schneller und
robuster. Scheitert ein Warmstart, wird die Zelle zuerst bei ihrer vorherigen Zusammensetzung neu gelöst und in vier Warmstart-Schritten zur neuen
geführt, bevor auf Kaltstarts zurückgegriffen wird.

GEMS-Ergebnisse hängen auf einem Niveau von etwa 1e-5 relativ von Rundungsfehlern ab. Zwei Läufe mit Eingaben, die sich in der letzten Stelle
unterscheiden, können so weit voneinander abweichen. Das ist Löser-Genauigkeit, kein Fehler.
