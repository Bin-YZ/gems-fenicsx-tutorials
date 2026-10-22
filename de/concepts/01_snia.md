# Operator-Splitting (SNIA)

OGS-GEM löst Transport und Chemie nicht gemeinsam. Jeder Zeitschritt wird in getrennte Lösungsschritte
aufgeteilt, die jeweils einmal ausgeführt werden — der *sequentielle nicht-iterative Ansatz* (SNIA):

```{image} ../figures/snia.png
:width: 100%
```

1. **prepare** — die neue Porosität jedes Knotens wird in Elementkoeffizienten (Porosität,
   Diffusionskoeffizient, Permeabilität) und Randwerte für diesen Zeitpunkt umgerechnet.
2. **flow** (falls vorhanden) — ein stationäres Darcy-Problem, mit dem Überschusswasser des letzten GEMS-Schritts als Quelle.
3. **transport** — jedes mobile chemische Element wird als passiver Stoff advektiert und dispergiert.
4. **chemistry** — GEMS bringt jeden Knoten mit den transportierten Mengen neu ins Gleichgewicht.

In der Vorlage ist das `reactive_transport.run`:

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/reactive_transport.py
:language: python
:pyobject: run
```

**Folgen, denen Sie in den Tutorials begegnen**

- Der Splitting-Fehler ist von erster Ordnung in $\Delta t$. Mit expliziter Kinetik kann er groß sein:
  in [HAYEKIT](../tutorials/01_hayekit) liegt das OGS-Ergebnis bei $\Delta t = 100$ s 24 % neben der
  analytischen Porosität.
- Koeffizienten hinken einen Schritt hinterher: der Transport in Schritt $n$ verwendet die Porosität aus Schritt $n-1$.
- Es wird nicht iteriert; ein Knoten, an dem GEMS versagt, behält für den ganzen Schritt seinen alten Zustand.
