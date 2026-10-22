# Transportnumerik: Elementkoeffizienten, Massenmatrix und FCT

Die Vorlage verwendet lineare (CG1) finite Elemente und impliziten Euler, wie OGS. Um OGS Knoten für Knoten
zu reproduzieren, müssen auch die Details gleich gewählt werden:

| Detail | OGS-Regel | Vorlage |
|---|---|---|
| Elementporosität | Mittel der Knotenporositäten | `element_mean(phi, cells)` |
| Elementdiffusion | harmonisches Mittel der Knotenwerte (`$DIFFUSION 8/9`) | `harmonic_mean(...)` |
| Massenmatrix | konsistent, oder konzentriert mit `ELE_MASS_LUMPING` | `Transport(lumped=...)` |
| Dispersion | $\alpha_T|q|I + (\alpha_L-\alpha_T)\,qq^T/|q|$ | `alpha_L`, `alpha_T` |
| Quadratur | 3×3 Gauß auf Vierecken | `quadrature_degree=5` |

## FEM-FCT

Bei starker Advektion erzeugt das Galerkin-Verfahren Oszillationen und negative Konzentrationen; GEMS
erhält dann negative Elementmengen. OGS bietet flusskorrigierten Transport (`$FEM_FCT 1`, linearisiertes
Verfahren nach Kuzmin): eine Lösung niedriger Ordnung mit zusätzlicher diskreter Diffusion, plus so viel
„antidiffusive“ Korrektur, wie der Zalesak-Limiter ohne neue Extrema erlaubt.

```{image} ../figures/fct.png
:width: 90%
```

OGS addiert den begrenzten Fluss $+f_{ij}$ in Zeile $j$; das Lehrbuchverfahren verwendet $-f_{ij}$
(massenerhaltend). `Transport(fct_ogs_sign=True)` übernimmt OGS. In [ConcreteCrack](../tutorials/05_concretecrack)
lassen sich beide Varianten gegenüber der OGS-Referenz nicht unterscheiden.
