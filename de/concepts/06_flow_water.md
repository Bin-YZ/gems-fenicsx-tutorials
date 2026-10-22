# Strömung, Permeabilität und die Überschusswasser-Quelle

Für gesättigte Fälle löst OGS-GEM in jedem Schritt ein stationäres Grundwasserströmungsproblem:

$$-\nabla\cdot(K\nabla h) = Q, \qquad q = -K\nabla h,$$

mit $K$ pro Element. Hängt $K$ von der Porosität ab (Kozeny–Carman, `$PERMEABILITY_FUNCTION_POROSITY 4`)

$$K = K_0\,\frac{(1-\phi_0)^2}{(1-\phi)^2}\,\frac{\phi^3}{\phi_0^3},$$

werden die Knotenwerte pro Element harmonisch gemittelt.

## Die Überschusswasser-Quelle

Mit `hydrology='full'` wird das GEMS-Volumen der wässrigen Phase auf die Porosität skaliert. Die Differenz
$V_{aq} - \phi$ geht nicht verloren: im nächsten Schritt wird sie als Knotenquelle
$Q_i = (V_{aq,i} - \phi_i)/\Delta t \cdot V_i$ in das Strömungsproblem eingespeist (OGS `SetSourceSink`):

```{image} ../figures/excess_water.png
:width: 100%
```

Wo Minerale reagieren, ist diese Volumenänderung physikalisch (comedy2d: bis $10^{-5}$ m³/m³ entlang des
Zementstreifens). Wo nichts reagiert, ist sie Rundungsrauschen von GEMS ($10^{-10}$–$10^{-7}$). In gering
durchlässigem Material verschiebt selbst dieses Rauschen die Druckhöhe um Zentimeter — die Druckhöhe in
[ConcreteCrack](../tutorials/05_concretecrack) lässt sich daher nicht knotengenau reproduzieren.
