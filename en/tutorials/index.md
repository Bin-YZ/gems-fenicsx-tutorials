# Tutorials overview

The five tutorials use the 1D code in `FEniCSx_GEMS`. Every case is set up **only by editing `case.yaml`**; the Python modules are not
changed. Each tutorial follows the same order: the physical problem → the model assumptions → how `case.yaml` expresses them → the run →
how to read the result → what the case does and does not show.

They build on each other: diffusion without chemistry, then chemistry without transport, then both together, then minerals, then flow.

## 1 · [Tracer diffusion](01_tracer_diffusion.ipynb)

- **Simulates:** a non-reactive tracer diffusing into a 10 mm water-saturated column from a boundary held at c = 1. Mode `diffusion`, about 2 s.
- **You learn:** the four sections of `case.yaml`, how to run a case, the result files and the mass balance.
- **Compared with:** the exact analytical solution.
- **Result:** maximum difference 9·10⁻⁴ mol/m³ (0.1 % of the boundary value); mass balance closes to 10⁻¹⁷ mol/m².

## 2 · [One chemical equilibrium](02_single_equilibrium.ipynb)

- **Simulates:** one GEMS equilibrium of a hydrated cement paste, then a scan of its Ca/Si from 3.7 to 0.5. Mode `chemistry`, about 15 s.
- **You learn:** element and phase names of a GEMS project, recipe units (mol per dm³ of bulk material), how to check a recipe, the `gibbs` adjustments.
- **Compared with:** nothing external; the phase assemblage is checked for consistency (portlandite + C-S-H at pH 12.45).
- **Result:** portlandite disappears below Ca/Si ≈ 1.5, amorphous silica appears below ≈ 0.65.

## 3 · [NaCl diffusion](03_nacl_diffusion.ipynb)

- **Simulates:** 1 M and 0.5 M NaCl solutions meeting in a 20 mm column, 100 s, no solids. Mode `coupled`, about 5 s.
- **You learn:** the first coupled run, zones with their own recipes, per-side boundary solutions.
- **Compared with:** the erf solution with the binary salt diffusion coefficient.
- **Result:** maximum difference 0.43 % of the 1 M concentration. Tests the coupled loop, not the single-coefficient assumption.

## 4 · [Cement leaching](04_cement_leaching.ipynb)

- **Simulates:** a 4 mm cement paste in contact with 14.6 mM CaCl₂ water for 1000 years. Mode `coupled`, two runs of 3–5 min.
- **You learn:** reacting minerals, long time scales, and what changes when porosity and diffusivity feedback is switched on.
- **Compared with:** HYDRUS profiles of the same benchmark (constant φ and De).
- **Result:** the portlandite front lies within about one cell (0.1 mm) of HYDRUS. With feedback the front moves slightly *less*.

## 5 · [Calcite → dolomite](05_calcite_dolomite.ipynb)

- **Simulates:** a 0.5 m calcite column flushed with MgCl₂ solution for 21 000 s; a dolomite band forms and migrates. Mode `coupled`, about 25 s.
- **You learn:** advection (`darcy_flux`), an `outflow` boundary, a GEMS project without O, numerical dispersion and mesh size.
- **Compared with:** the published benchmark figure (visual comparison only; the reference curves are an image).
- **Result:** front and band positions agree by eye; refining from 100 to 1000 cells sharpens the band edges but does not move the band.

## Where the cases run

Tutorials 1 and 2 write their cases to `tutorial_runs/` next to `FEniCSx_GEMS`. Tutorials 3 to 5 run inside the matching folder
`FEniCSx_GEMS/example/<case>/`. The first code cell of each notebook finds these folders by itself.
