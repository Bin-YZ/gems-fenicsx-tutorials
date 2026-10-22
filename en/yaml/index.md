# `case.yaml` at a glance

One file describes the whole simulation. It has **exactly four top-level sections**, one per module. A fifth section, or a
missing one, stops the run with *Use exactly four sections*.

```yaml
chemistry:   # chemistry.py  GEMS project, conditions, phases, recipes
transport:   # transport.py  geometry, material, zones, boundaries, solver
coupling:    # coupling.py   mode, time stepping, porosity/diffusivity feedback
output:      # output.py     result folder, how often profiles are written
```

| page | keys |
|---|---|
| [chemistry](chemistry.md) | `project`, `temperature`, `pressure`, `aqueous_phase`, `solid_phases`, `gibbs`, `initial`, `inlet`, `start`, `on_failure` |
| [transport](transport.md) | `geometry`, `material` (`phi`, `De`, `darcy_flux`), `zones`, `components`, `initial`, `boundary`, `solver` |
| [coupling and output](coupling_output.md) | `mode`, `time`, `update_porosity`, `update_diffusivity`, `exponent`; `folder`, `every` |
| [From GEMS-Selektor to a recipe](from_gems.md) | how to get the numbers for `initial` and `inlet` |

## The default case

This is `FEniCSx_GEMS/case.yaml`: a cement paste in contact with a CaCl₂ solution, with porosity and diffusivity feedback.

```{literalinclude} ../../FEniCSx_GEMS/case.yaml
:language: yaml
```

## Rules that save time

- **Paths are relative to the `case.yaml` file**, not to where you start Python. This applies to `chemistry.project` and
  `output.folder`.
- **Units are SI** (m, s, K, Pa, m²/s, m/s). The one exception is chemical recipes: mol per **dm³ of bulk** material.
- **Write floats with a decimal point:** `1.0e-15`, not `1e-15`. PyYAML reads `1e-15` as a string. Most keys are
  converted afterwards, but a decimal point avoids surprises.
- **Integers must be integers:** `cells: 40` and `every: 5`, not `40.0`.
- **`true`/`false`** for the feedback switches, not `yes`/`1`.
- **Names are case-sensitive** and must match the GEMS project: `Ca`, `Portlandite`, `aq_gen`.
- `{a: 1, b: 2}` is the same as writing `a: 1` and `b: 2` on separate indented lines, and `[A, B]` is a list. Comments start with `#`.
- **Keys you leave in but do not need are ignored.** For example, `transport.components` is ignored in coupled mode. Example files
  keep them so that switching modes needs only one line.

## Workflow for a new case

1. Copy an example folder that is close to your problem (see the [tutorials](../tutorials/01_tracer_diffusion.ipynb)).
2. Put your GEMS project files in it and point `chemistry.project` to the `.lst` file.
3. Run once with `mode: chemistry` to check the recipe and the phase names.
4. Run with `mode: diffusion` to check mesh, time step and boundaries without GEMS.
5. Switch to `mode: coupled`. Start with a short `end`, look at `summary.txt` and `profiles.png`, then run the full time.
6. Change `output.folder` before each new variant so earlier results are kept. `case_used.json` in each folder records the
   exact settings of that run.
