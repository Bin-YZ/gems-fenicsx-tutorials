# Flow, permeability and the excess-water source

For saturated cases OGS-GEM solves a steady groundwater-flow problem every step:

$$-\nabla\cdot(K\nabla h) = Q, \qquad q = -K\nabla h,$$

with $K$ per element. When $K$ depends on porosity (Kozeny–Carman, `$PERMEABILITY_FUNCTION_POROSITY 4`)

$$K = K_0\,\frac{(1-\phi_0)^2}{(1-\phi)^2}\,\frac{\phi^3}{\phi_0^3},$$

the node values are combined with a harmonic mean per element.

## The excess-water source term

With `hydrology='full'` GEMS's aqueous volume is scaled to the porosity. The difference
$V_{aq} - \phi$ is not thrown away: in the next step it is injected into the flow problem as a nodal
source $Q_i = (V_{aq,i} - \phi_i)/\Delta t \cdot V_i$ (OGS `SetSourceSink`):

```{image} ../figures/excess_water.png
:width: 100%
```

Where minerals react this volume change is physical (comedy2d: up to $10^{-5}$ m³/m³ along the
cement strip). Where nothing reacts it is round-off of GEMS ($10^{-10}$–$10^{-7}$). In low-permeability
material even that noise moves the head by centimetres — the head in
[ConcreteCrack](../tutorials/05_concretecrack) can therefore not be reproduced node by node.
