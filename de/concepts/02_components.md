# Was transportiert wird: Elementsummen des Porenwassers

GEMS beschreibt ein System durch die Gesamtmengen seiner **unabhängigen Komponenten** — chemische Elemente
plus Ladung (`Zz`) — den *b-Vektor*. OGS-GEM transportiert genau diese Summen, aber nur den im Porenwasser
gelösten Anteil (`$TRANSPORT_B 1`):

```{image} ../figures/bvector.png
:width: 100%
```

Nach jeder GEMS-Rechnung wird der b-Vektor eines Knotens aufgeteilt in

- `b_fix` — alles in Feststoffen (und Gas): bleibt am Knoten,
- das Porenwasser — gelöste Stoffe **plus das Lösungsmittel Wasser**: H und O des H₂O werden vor dem
  Transport abgezogen und danach wieder addiert; die transportierte Konzentration von H und O ist also nur
  der Anteil in gelösten Stoffen.

Warum Elementsummen und nicht Spezies? Es gibt viel weniger Elemente als Spezies (16 gegenüber 157 in
TransLay2d), die Summen bleiben beim Transport erhalten, und die Lösung bleibt elektroneutral, ohne Ladung
zu transportieren. Der Preis: alle Spezies eines Elements bewegen sich mit demselben Diffusionskoeffizienten.

Die Ladung `Zz` wird nie transportiert und vor GEMS auf null gesetzt. Inerte Komponenten (z. B. `Inrt`, `Sn`)
können mit dem Argument `mobile` von `run` vom Transport ausgenommen werden.
