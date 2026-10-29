# FEniCSx + GEMS reactive transport

This site explains a small Python code that couples two programs:

- **[FEniCSx](https://fenicsproject.org)**, which moves dissolved elements through a 1D porous column by diffusion and advection;
- **[GEMS3K](https://gems.web.psi.ch)**, used through `xgems`, which computes the local chemical equilibrium in every cell.

A whole simulation is described by **one input file, `case.yaml`**. To set up a new problem you edit that file.
The Python modules stay as they are.

```{image} figures/coupling_loop.png
:alt: One time step: coupling.py reads case.yaml, sends aqueous amounts to transport.py and total amounts to chemistry.py, and writes the state with output.py
:width: 100%
```

## Quick start

```bash
# 1. environment with FEniCSx, PETSc, GEMS3K and PyYAML (see Installation)
conda activate fenicsx

# 2. edit the input
cd FEniCSx_GEMS
nano case.yaml                  # or the browser Case Builder

# 3. run; the results go to output.folder
python coupling.py case.yaml
```

On Windows with WSL, `Run.cmd` runs step 3 with a double-click.

## How the site is organised

| Part | What you learn |
|---|---|
| [Installation](install.md) | Set up the Python environment and check it |
| [How the coupling works](coupling/overview.md) | What the four modules exchange in every time step, units, conservation |
| [Equations and numerics](coupling/numerics.md) | The transport equation, its discretisation, porosity and diffusivity feedback |
| [Speeding up a run](coupling/performance.md) | Where the time goes, processes vs threads, arrays vs dictionaries |
| [`case.yaml` reference](yaml/index.md) | Every key of the four sections, with units, defaults and examples |
| [Browser tools](tools/case_builder.md) | Build a `case.yaml` from a form; inspect a GEMS project in the browser |
| [Tutorials](tutorials/01_tracer_diffusion.ipynb) | Five cases, from a tracer without chemistry to calcite–dolomite conversion with flow |
| [Results and troubleshooting](outputs.md) | What each output file contains; what to do when GEMS does not converge |
| [Verification against OGS-GEM](verification/index.md) | Five OpenGeoSys-GEM benchmarks reproduced with FEniCSx and GEMS |

## Learning path

1. [Tracer diffusion](tutorials/01_tracer_diffusion.ipynb): `diffusion` mode, analytical solution, mass balance
2. [One chemical equilibrium](tutorials/02_single_equilibrium.ipynb): `chemistry` mode, recipes, phase names, Gibbs energies
3. [NaCl diffusion](tutorials/03_nacl_diffusion.ipynb): first `coupled` run, two zones
4. [Cement leaching](tutorials/04_cement_leaching.ipynb): porosity and diffusivity feedback
5. [Calcite → dolomite](tutorials/05_calcite_dolomite.ipynb): advection, inflow and outflow boundaries

Each tutorial shows the complete `case.yaml`, the lines that changed since the previous one, the run and the results.
