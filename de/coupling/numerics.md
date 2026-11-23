# Gleichungen und Numerik

## Transportgleichung

Die Gleichung unten ist der **Transportteilschritt** des Operator-Splittings. In diesem Teilschritt werden Reaktionen ausgeschlossen und die Porosität
festgehalten. Die vollständige Gleichung für ein gelöstes Element enthält zusätzlich einen Reaktionsquellterm $R$ (Lösung minus Fällung),
$\partial(\phi c)/\partial t + \partial_x(qc - D_e\partial_x c) = R$. Der Code diskretisiert $R$ nicht direkt: Der folgende Chemieteilschritt ersetzt ihn
durch ein lokales Gleichgewicht in jeder Zelle ([wie die Kopplung funktioniert](overview.md)).

Im Transportteilschritt gilt für jedes transportierte Element, mit $c$ in mol/m³ Porenwasser:

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

- **Diffusionsdominiert:** $\sqrt{D_p\,\Delta t}$ ist die Diffusionslänge eines Schritts. Sie ist eine Längenskala, nicht die Strecke, um die eine
  Mineralfront pro Schritt wandert; diese hängt auch davon ab, wie viel Mineral gelöst oder gefällt werden muss. Ist $\sqrt{D_p\,\Delta t}$ viel größer als
  die Zellbreite $h$, ändern sich die Gradienten innerhalb eines Schritts stark, und die Splitting-Fehler wachsen.
- **Advektionsdominiert:** Die Courant-Zahl $q\,\Delta t / (\phi h)$ um 1 oder darunter halten. Das Euler-Verfahren bleibt auch darüber stabil,
  aber die Fronten werden breiter.
- **Zeit und Ort getrennt prüfen.** Auf einem feinen Gitter mit `dt`, `dt/2` und `dt/4` rechnen, bis sich die Profile nicht mehr ändern. Dann mit diesem
  Zeitschritt `cells` verfeinern, bis sich die Profile wieder nicht mehr ändern. Gleichzeitiges Halbieren von `dt` und Verdoppeln von `cells` zeigt nur
  die kombinierte Wirkung und trennt die beiden Fehler nicht.

## Chemie: Kalt- und Warmstart

GEMS minimiert die Gibbs-Energie des Systems jeder Zelle. Standardmäßig (`chemistry.start: cold`) beginnt jeder Aufruf von vorn; das Ergebnis hängt
also weder vom vorherigen Schritt noch von Nachbarzellen ab. Meldet GEMS eine schlechte Elementbilanz, wird dasselbe System in skalierter Größe neu
gelöst (×1, ×10, ×100, ×0,1, ×0,01) und zurückskaliert, denn das Gleichgewicht hängt nicht von der Systemgröße ab.

`start: warm` gibt jeder Zelle eine eigene GEMS-Engine und startet vom vorherigen Gleichgewicht dieser Zelle. Das ist für große Systeme schneller und
robuster. Scheitert ein Warmstart, wird die Zelle zuerst bei ihrer vorherigen Zusammensetzung neu gelöst und in vier Warmstart-Schritten zur neuen
geführt, bevor auf Kaltstarts zurückgegriffen wird.

GEMS-Ergebnisse sind auf dem Niveau von Rundungsfehlern nicht exakt reproduzierbar. In den getesteten Beispielen ergaben zwei Läufe, deren Eingaben sich nur
in der letzten Stelle unterschieden, relative Abweichungen der Konzentrationen bis etwa 1e-5. Das ist eine Beobachtung für diese Beispiele, keine allgemeine
Schranke: Die Größe hängt vom System, den Lösertoleranzen und davon ab, ob Phasen erscheinen oder verschwinden. Wie man solche Unterschiede beurteilt, steht unter
[kleine Unterschiede zwischen Läufen](../outputs.md).
