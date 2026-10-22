# `transport`: mesh, material, boundaries

Read by `transport.py`. Not used in `chemistry` mode, where only `geometry.length` serves as the reference length.

```yaml
transport:
  geometry: {length: 0.004, cells: 40}
  material: {phi: 0.5, De: 5.0e-15}          # + darcy_flux for advection
  zones: [...]                               # optional
  components: [tracer]                       # diffusion mode only
  initial: {tracer: 0.0}                     # diffusion mode only
  boundary:
    left:  {type: dirichlet, concentrations: {tracer: 1.0}}
    right: {type: no_flux,   concentrations: {tracer: 0.0}}
  solver: {ksp_type: preonly, pc_type: lu, rtol: 1.0e-10, max_iterations: 1000}
```

## `geometry`

| key | value | meaning |
|---|---|---|
| `length` | m, > 0 | column length; x runs from 0 (left) to `length` (right) |
| `cells` | integer ≥ 1 | number of equal cells; $h$ = length / cells |

The run time grows linearly with `cells`, because GEMS is called once per cell and step.

## `material`

| key | value | meaning |
|---|---|---|
| `phi` | 0 < φ ≤ 1 | initial porosity |
| `De` | m²/s, > 0 | initial effective diffusion coefficient (flux $= -D_e\,\partial_x c$) |
| `darcy_flux` | m/s, ≥ 0, optional | Darcy flux $q = \phi v$ towards $+x$; omit or 0 for pure diffusion |

With `darcy_flux > 0` the left boundary must be `dirichlet` (the inflow) and the right boundary `outflow` or `dirichlet`.

## Zones

Zones split the column into materials with their own φ and De and, through `chemistry.initial`, their own recipe:

```yaml
transport:
  zones:
    - {name: clay,   from: 0.0,  to: 0.25, phi: 0.51, De: 5.1e-10}
    - {name: cement, from: 0.25, to: 0.5,  phi: 0.52, De: 5.2e-10}
```

| key | meaning |
|---|---|
| `name` | unique zone name, used by `chemistry.initial` and `chemistry.inlet` |
| `from`, `to` | m; a cell belongs to the zone if its **centre** lies in `[from, to)`; default 0 and `length` |
| `phi`, `De` | optional; otherwise `material.phi` / `material.De` |

Every zone must contain at least one cell centre. Cells outside all zones keep `material` values. The diffusion coefficient
between two zones is the harmonic mean of the two cells.

## `boundary`

`left` (x = 0) and `right` (x = length) each have a `type`:

| type | condition | in `coupled` mode |
|---|---|---|
| `dirichlet` | pore water at the boundary has a fixed composition; diffusive (and, with flow, advective) exchange | composition from `chemistry.inlet` |
| `no_flux` | nothing crosses | – |
| `outflow` | water leaves by advection with the cell's composition; zero diffusive gradient | for the downstream end with `darcy_flux` |

`concentrations` (mol/m³ pore water, one value per tracer) is used **only in diffusion mode** at `dirichlet` boundaries. In coupled
mode every Dirichlet boundary uses `chemistry.inlet` and these values are ignored.

## Tracers: `components` and `initial` (diffusion mode)

```yaml
components: [tracer, salt]           # any names except Zz
initial: {tracer: 0.0, salt: 0.5}    # mol/m3 pore water, every component
```

In `coupled` and `chemistry` mode the transported names are the GEMS elements, and both keys are ignored.

## `solver`

| key | default in examples | meaning |
|---|---|---|
| `ksp_type` | `preonly` | PETSc Krylov method; `preonly` = apply the preconditioner once |
| `pc_type` | `lu` | PETSc preconditioner; `lu` = direct factorisation |
| `rtol` | `1.0e-10` | relative tolerance (iterative methods) |
| `max_iterations` | `1000` | iteration limit (iterative methods) |

For 1D meshes keep `preonly` + `lu`. A transport solve that does not converge, or produces a concentration below −1e-12 mol/m³, stops the run.
