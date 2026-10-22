# `chemistry`: GEMS project and recipes

Read by `chemistry.py`. In `diffusion` mode the section must be present, but it is not used.

```yaml
chemistry:
  project: chemistry_data/b_time0-dat.lst
  temperature: 298.15
  pressure: 100000
  aqueous_phase: aq_gen
  solid_phases: [CSHQ, Portlandite, Silica-amorph]
  gibbs: {H2O@: -237183.0, Ca+2: -552400.0}
  initial: {Ca: 1.119, Si: 0.310, H: 58.52, O: 31.00, Cl: 1.0e-15}
  inlet:   {Ca: 0.0146, Cl: 0.0292, H: 111.0, O: 55.51, Si: 0.000183}
  start: cold          # optional
  on_failure: stop     # optional
```

## Keys

| key | required | value | meaning |
|---|---|---|---|
| `project` | yes | path | the GEMS `*-dat.lst` file, relative to `case.yaml`. JSON (`-j`) and text (`-t`) exports work. |
| `temperature` | yes | K, > 0 | temperature of every equilibrium |
| `pressure` | yes | Pa, > 0 | pressure of every equilibrium |
| `aqueous_phase` | yes | phase name | the phase whose elements are transported, usually `aq_gen` |
| `solid_phases` | yes | list of phase names, may be `[]` | phases written to the output; their **volumes drive the porosity update** |
| `gibbs` | yes | `{species: J/mol}`, may be `{}` | overwrite standard molar Gibbs energies, in memory only |
| `initial` | yes* | recipe, or `{zone: recipe}` | the material at t = 0 |
| `inlet` | if a boundary is `dirichlet` | recipe, zone name, or `{left: …, right: …}` | the solution held at Dirichlet boundaries |
| `start` | no, default `cold` | `cold` / `warm` | how GEMS is initialised each call, see [numerics](../coupling/numerics.md#chemistry-cold-and-warm-starts) |
| `on_failure` | no, default `stop` | `stop` / `skip` | what to do when a cell does not converge |

\* `initial` may be `{}` in diffusion mode.

## Recipes

A recipe gives **element amounts in mol per 1 dm³ of bulk material**: pore water plus solids plus inert material.

```yaml
initial:
  Ca: 1.119218076064     # mol/dm3 bulk
  Si: 0.31000148638994
  H: 58.52226105076      # includes the water: 0.5 dm3 water = 27.75 mol H2O -> 55.5 mol H ...
  O: 31.00037832923
  Cl: 1.0e-15            # trace, keeps the element present
```

- Use the **element** names of the GEMS project (`Ca`, `Si`, …), not oxides or species.
- Leave out `Zz` (charge). An element you leave out is set to 0.
- **Include the water.** H and O in the recipe are the water's plus those bound in solids or dissolved species.
- If an element should be available later, for example Cl entering from the boundary, give it a tiny amount such as `1.0e-15`.
  This keeps GEMS well-posed.
- The pore water implied by the recipe should match `transport.material.phi`. A recipe with 0.5 dm³ of water per dm³ bulk belongs
  with `phi: 0.5`. The summary's **water mismatch** reports any difference.

[From GEMS-Selektor to a recipe](from_gems.md) shows how to get these numbers from an exported GEMS state.

### Several materials: one recipe per zone

With [`transport.zones`](transport.md#zones), `initial` can map zone names to recipes:

```yaml
chemistry:
  initial:                 # illustrative numbers; the elements must exist in your project
    clay:   {Ca: 0.01, Si: 0.6, H: 57.0, O: 30.0, Na: 0.2, Cl: 0.2}
    cement: {Ca: 1.12, Si: 0.31, H: 58.5, O: 31.0, Cl: 1.0e-15}
```

Every zone needs a recipe. In `chemistry` mode, which has no mesh, the first recipe is used.

## Boundary solution: `inlet`

`inlet` is equilibrated once at the start. Its pore-water concentrations are then held at every `dirichlet` boundary.
There are three forms:

```yaml
inlet: {Ca: 0.0146, Cl: 0.0292, H: 111.0, O: 55.5}   # 1. a recipe (about 1 dm3 of solution), used on both sides
inlet: clay                                          # 2. the equilibrated pore water of a zone
inlet:                                               # 3. per side, each side either form
  left: {Na: 0.1, Cl: 0.1, H: 111.0, O: 55.5}
  right: cement
```

For an inlet recipe the amounts are per GEMS system, normally about 1 dm³ of water. The code divides by the aqueous-phase volume
GEMS returns, so the exact water amount does not matter as long as the ratio of solutes to water is right.
Omit `inlet` when no boundary is `dirichlet`.

## Phase names and `solid_phases`

`aqueous_phase` and every entry of `solid_phases` must be phase names of the project; otherwise the run stops with
*Unknown GEMS phase*. Phases that are not listed still take part in the equilibrium, but

- their amounts are not written to `profiles.csv`, and
- their volume does **not** count in the porosity update.

So list every solid that can form or dissolve when `update_porosity` is on.

## `gibbs`

```yaml
gibbs: {H2O@: -237183.0, Ca+2: -552400.0}    # J/mol at the run temperature
```

Overwrites $G^\circ$ of the named **species** after loading the project. The files are not changed. Use it to reproduce a
benchmark that used slightly different data. Otherwise keep `gibbs: {}`.
[Tutorial 2](../tutorials/02_single_equilibrium.ipynb) shows the effect.

## When GEMS does not converge

A cell is accepted when GEMS returns status 2 or 6 **and** reproduces the given element totals to 1e-8. Otherwise:

1. with `start: warm`: retry from the cell's last state and approach the new composition in four steps;
2. cold starts at scaled sizes (×1, ×1, ×10, ×100, ×0.1, ×0.01);
3. still failing: `on_failure: stop` ends the run and writes `failure.txt` with the step, cell, position and composition.
   `on_failure: skip` leaves that cell unreacted for this step. Its totals are unchanged, so mass is still conserved. Every skip
   is logged and counted.

The initial equilibrium (step 0) always stops on failure.
