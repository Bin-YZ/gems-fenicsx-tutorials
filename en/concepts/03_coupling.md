# Concentration ↔ mass, porosity and initialisation

Transport works with concentrations (mol per m³ of fluid), GEMS with amounts (mol per node). OGS converts
between them with two functions; the template copies them line by line.

## Concentration → mass (before GEMS)

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/gems_ogs.py
:language: python
:pyobject: OGSGEMS.concentration_to_mass
```

The transported concentration is multiplied by the fluid volume $V_f$ the node had *before* transport,
negative values are replaced by their absolute value, the solvent water is added back, and very small
totals are set to $10^{-16}$ (GEMS cannot handle zeros).

## Mass → concentration (after GEMS)

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/gems_ogs.py
:language: python
:pyobject: OGSGEMS.mass_to_concentration
```

- **Porosity** is $\phi = 1 - \sum V_\text{solid}$ (OGS `CalcPorosity`; the node volume is 1 m³), clipped to
  `[MIN_POROSITY, MAX_POROSITY]`.
- GEMS returns its own aqueous volume $V_{aq}$, which is never exactly $\phi$. What happens next is the
  `hydrology` option:

| `hydrology` | OGS input | rule |
|---|---|---|
| `'full'` | `$FLAG_COUPLING_HYDROLOGY 1` | the whole aqueous phase is scaled by $\phi/V_{aq}$; $V_f = \phi$; the difference $V_{aq}-\phi$ becomes a flow source |
| `'hayekit'` | `$FLAG_HAYEKIT 1` | only the solvent water is scaled |
| `'none'` | `$FLAG_COUPLING_HYDROLOGY 0` | no scaling; $c = b_{aq}/V_{aq}$ and later $b = b_\text{fix} + c\,\phi$ |

## Initialisation

There are two ways an OGS-GEM run starts:

- **from total b vectors** (`.ic` file) — `init_from_bulk`. OGS runs GEMS, divides the b vector by the
  resulting system volume $V_s$ so that every node holds exactly 1 m³, and runs GEMS again (two passes);
- **from restart files** (`$RELOAD`) — `init_from_restart`. The stored porosity, fluid volume, `b_fix`,
  species amounts and kinetic limits are loaded and GEMS is run once with them. Several benchmarks
  (HAYEKIT, comedy2d, TransLay2d) only make sense from their restart state.
