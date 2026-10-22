# Kinetik mit einem Gleichgewichtslöser

GEMS berechnet nur Gleichgewichte. OGS-GEM macht ein Mineral kinetisch, indem es GEMS ein **Fenster**
$[\text{dll}, \text{dul}]$ für dessen Menge vorgibt: GEMS sucht das Gleichgewicht *innerhalb* dieses Fensters.

## Rate

Nach jeder GEMS-Rechnung wird die Rate jeder kinetischen Phase berechnet (OGS `CalcReactionRate`):

$$\frac{dm}{dt} = -A_s \sum_m 10^{\log k_m}\, a_{H^+}^{\,n_m}\,(1-\Omega)$$

mit der Sättigung $\Omega$ aus GEMS und der reaktiven Oberfläche $A_s$ aus einem der Oberflächenmodelle
(`Kinetic.area_model`): 1 — $A\,V_\text{Mineral}$; 3 — $A\,V_\text{Mineral}/\phi$; 4 — $A\,\phi$.

## Verschieben des Fensters

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/gems_ogs.py
:language: python
:pyobject: OGSGEMS.calc_limits
```

Im nächsten Schritt wird das Fenster um $\frac{dm}{dt}\,\Delta t$ verschoben (OGS `CalcLimits`):

```{image} ../figures/kinetics_window.png
:width: 90%
```

- `limits='loose'` (`$LOOSE_KINETICS 1`): ein Ende des Fensters bleibt bei der aktuellen Menge, GEMS darf
  also auch *weniger* Reaktion wählen als die Rate erlaubt. `'strict'` legt die Menge auf das kinetische Ziel fest.
- **Keimbildung:** eine nicht vorhandene, übersättigte Phase erhält $10^{-6}$ mol, sonst könnte sie nie entstehen.
- **Teilschritte** (`substep_kinetics`, OGS 2017): würde eine Phase ein Element in einem Schritt um mehr als
  10 % ändern, wird der Chemieschritt unterteilt.

Die Rate ist explizit — aus dem Zustand am Ende des vorigen Schritts. Das ist die Hauptursache der
Zeitschrittabhängigkeit (siehe [HAYEKIT](../tutorials/01_hayekit)).
