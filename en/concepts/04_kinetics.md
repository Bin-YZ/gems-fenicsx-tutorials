# Kinetics with an equilibrium solver

GEMS only computes equilibria. OGS-GEM makes a mineral kinetic by giving GEMS a **window**
$[\text{dll}, \text{dul}]$ for its amount: GEMS finds the equilibrium *within* that window.

## Rate

After each GEMS run the rate of every kinetic phase is computed (OGS `CalcReactionRate`):

$$\frac{dm}{dt} = -A_s \sum_m 10^{\log k_m}\, a_{H^+}^{\,n_m}\,(1-\Omega)$$

with the saturation $\Omega$ from GEMS and the reactive surface $A_s$ from one of the surface models
(`Kinetic.area_model`): 1 — $A\,V_\text{mineral}$; 3 — $A\,V_\text{mineral}/\phi$; 4 — $A\,\phi$.

## Moving the window

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/gems_ogs.py
:language: python
:pyobject: OGSGEMS.calc_limits
```

In the next step the window is moved by $\frac{dm}{dt}\,\Delta t$ (OGS `CalcLimits`):

```{image} ../figures/kinetics_window.png
:width: 90%
```

- `limits='loose'` (`$LOOSE_KINETICS 1`): one end of the window stays at the current amount, so GEMS may
  also choose *less* reaction than the rate allows. `'strict'` pins the amount to the kinetic target.
- **Seeding:** an absent phase that is supersaturated gets $10^{-6}$ mol, otherwise it could never start.
- **Sub-steps** (`substep_kinetics`, OGS 2017): if a phase would change an element by more than 10 % in one
  step, the chemistry step is split.

The rate is explicit — computed from the state at the end of the previous step. This is the main source
of time-step dependence (see [HAYEKIT](../tutorials/01_hayekit)).
