# How the coupling works

The code splits each time step into a **transport step** and a **chemistry step**. This is sequential,
non-iterative operator splitting (SNIA). Each of the four modules has one job, and only `coupling.py`
talks to the other three:

| module | `case.yaml` section | does | does **not** |
|---|---|---|---|
| `coupling.py` | `coupling` | reads the input, owns the arrays, runs the time loop, updates φ and De, checks conservation | call GEMS or assemble FE forms itself |
| `transport.py` | `transport` | builds the 1D mesh, applies boundary conditions, solves one transport step per element | know any chemistry |
| `chemistry.py` | `chemistry` | loads GEMS, converts recipes, computes one local equilibrium | know the mesh |
| `output.py` | `output` | writes CSV, XDMF, plots, logs, summary and failure reports | compute anything |

```{image} ../figures/coupling_loop.png
:alt: coupling.py in the middle, transport.py and chemistry.py on the right, case.yaml and output.py on the left
:width: 100%
```

## What is stored, and in which unit

Everything lives in arrays with **one row per cell and one column per element**. The column order is the element order of the
GEMS project, e.g. `Ca, Cl, H, O, Si, Zz`.

| array | meaning | unit |
|---|---|---|
| `state['total']` | all of an element in the cell: dissolved + solids | mol/m³ bulk |
| `state['aqueous']` | the dissolved part | mol/m³ bulk |
| `c = aqueous / phi` | dissolved concentration | mol/m³ pore water |
| `state['phi']` | porosity | – |
| `state['De']` | effective diffusion coefficient | m²/s |
| `state['minerals']` | amounts of the phases in `chemistry.solid_phases` | mol/m³ bulk |

Recipes in `case.yaml` are written in **mol per dm³ of bulk material**, which is the size of a GEMS reference system.
`chemistry.py` multiplies them by 1000 on the way in and divides by 1000 before calling GEMS.

```{image} ../figures/cell_volume.png
:alt: A cell of 1 m3 bulk split into pore water, reactive minerals and inert material
:width: 90%
```

## One time step

```python
# coupling.py, inside the time loop (simplified)
immobile = state['total'] - state['aqueous']           # 1. what stays put
state['aqueous'], incoming = transport.step(            # 2. move the dissolved part
    state['aqueous'], state['phi'], state['De'], dt, boundary_c, mobile)
state['total'] = immobile + state['aqueous']            # 3. new totals
for i in cells:                                         # 4. local equilibrium
    result = chemistry.equilibrate(state['total'][i])
    state['aqueous'][i] = result['aqueous']             #    GEMS redistributes the total
    solid[i] = result['solid']                          #    volume fraction of solid_phases
phi = phi0 + initial_solid - solid                      # 5. feedback (if switched on)
De = De0 * (phi / phi0) ** exponent
balance = inventory - initial_inventory - exchange      # 6. conservation check
output.write(state, diagnostics)                        # 7. output
```

1. **Only dissolved amounts move.** Minerals and other immobile parts are taken out before transport and put back afterwards.
2. **Every element is transported**, including the H and O of water. Only charge `Zz` is not transported. Each element is
   solved as its own linear system with the same matrix.
3. **φ and De are frozen during a transport step.** They are updated after the chemistry, so the next step uses the new values.
4. **Chemistry is local.** Each cell is equilibrated on its own, with its total element amounts. Equilibrium conserves the
   totals, so the chemistry step does not change the mass balance.
5. **Feedback is optional.** Without `update_porosity`, φ stays at its initial value however much mineral dissolves.

At step 0 there is no transport. The initial recipe is equilibrated once, and the solid volume found there becomes the reference
`initial_solid` for the porosity update.

## Boundary solutions

A `dirichlet` boundary holds the pore water at a fixed composition. In `coupled` mode this composition comes from
`chemistry.inlet`. The recipe is equilibrated once at the start, and the boundary concentration of every element is

$$
c_\text{boundary} = \frac{\text{element amount in the aqueous phase}}{\text{volume of the aqueous phase}}
\qquad \text{(mol/m³ water)}
$$

so the boundary water carries its own H and O as well as the solutes. `no_flux` boundaries exchange nothing.
`outflow` lets water leave by advection only (see [transport](../yaml/transport.md)).

## Conservation is checked, not assumed

After every step `coupling.py` compares, for each element,

$$
\underbrace{\textstyle\sum_\text{cells} \text{total}\cdot h}_\text{inventory now}
-\underbrace{\textstyle\sum_\text{cells} \text{total}_0\cdot h}_\text{initial inventory}
-\underbrace{\textstyle\sum_\text{steps} \text{boundary input}}_\text{exchange}
$$

in mol per m² of cross-section. The boundary input is computed separately, from the boundary fluxes. If this difference exceeds
$10^{-9} + 10^{-8}\,(|\text{initial}| + |\text{exchange}|)$ the run **stops** with `Mass balance failed`. There is no silent clipping
of negative concentrations or porosities either. Any such value stops the run and writes `failure.txt`.

Two further diagnostics are written every step, but they do not stop the run:

- **chemistry error**: how well GEMS reproduces the element totals it was given (mol/m³);
- **water mismatch**: relative difference between GEMS's aqueous-phase volume and φ. The transport assumes saturated pores
  with volume φ. GEMS computes the solution volume from its own density model. A few tenths of a percent is normal.

## Three modes

`coupling.mode` selects how much of this loop runs:

| mode | transport | chemistry | typical use |
|---|---|---|---|
| `diffusion` | yes, tracers from `transport.components` | no (GEMS is not loaded) | check the mesh, time step and boundaries |
| `chemistry` | no (no mesh is built) | one equilibrium of `chemistry.initial` | check a recipe and the phase names |
| `coupled` | yes, all elements except `Zz` | every cell, every step | the actual simulation |
