# Tutorials overview

Five cases, each a little more than the one before. Every tutorial is an executed notebook: it shows the complete `case.yaml`,
runs `coupling.py` on it and plots the results, mostly against an analytical solution or a published benchmark.

| # | what is simulated | mode | you learn | runtime |
|---|---|---|---|---|
| [1](01_tracer_diffusion.ipynb) | A non-reactive tracer diffuses into a 10 mm water-saturated column (φ = 0.4) from a boundary held at c = 1; the other end is held at 0, later closed. | `diffusion` | the four sections of `case.yaml`, running the code, result files, the mass balance; comparison with the analytical series solution | 2 s |
| [2](02_single_equilibrium.ipynb) | One GEMS equilibrium of a hydrated cement paste (Ca, Si, water, trace Cl): which minerals and which pore water it contains. A scan of the bulk Ca/Si from 3.7 to 0.5 shows portlandite disappearing, C-S-H losing Ca and amorphous silica appearing. | `chemistry` | element and phase names of a GEMS project, recipe units (mol per dm³ bulk), the `gibbs` adjustments | 15 s |
| [3](03_nacl_diffusion.ipynb) | A 1 M and a 0.5 M NaCl solution in contact in the middle of a 20 mm column; salt diffuses from the strong to the weak side for 100 s. No solids. | `coupled` | the first coupled run, two zones with their own recipes, per-side boundary solutions; comparison with the erf solution | 5 s |
| [4](04_cement_leaching.ipynb) | A 4 mm hydrated cement paste in contact with 14.6 mM CaCl₂ water for 1000 years. Ca leaches out, portlandite dissolves from the surface inwards and C-S-H decalcifies behind the front. | `coupled` | minerals and `solid_phases`, long time scales, porosity and diffusivity feedback; comparison with a HYDRUS benchmark profile | 2 × 3–5 min |
| [5](05_calcite_dolomite.ipynb) | A 0.5 m calcite column flushed with MgCl₂ solution (Darcy flux 3·10⁻⁶ m/s) for 21 000 s. Calcite dissolves, dolomite precipitates in a band that moves with the flow and dissolves again behind it. | `coupled` | advection (`darcy_flux`), `outflow` boundary, a GEMS project without O, numerical dispersion; comparison with the published benchmark figure | 25 s |

Tutorials 1 and 2 write their cases to `tutorial_runs/` next to `FEniCSx_GEMS`. Tutorials 3 to 5 run inside the matching folder
`FEniCSx_GEMS/example/<case>/`. The first code cell of each notebook finds these folders by itself.
