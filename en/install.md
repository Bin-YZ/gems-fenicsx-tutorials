# Installation

The code needs five Python packages:

| package | used by | for |
|---|---|---|
| `fenics-dolfinx` **with PETSc** | `transport.py`, `output.py` | mesh, finite-element forms, linear solver, XDMF output |
| `petsc4py`, `mpi4py` | `transport.py` | PETSc solver objects |
| `xgems` | `chemistry.py` | GEMS3K chemical equilibrium |
| `pyyaml` | `coupling.py` | reading `case.yaml` |
| `numpy` | all | arrays |

`pandas` and `matplotlib` are only used by the tutorial notebooks.

## Linux, macOS or Windows with WSL

All packages are on conda-forge. Use [Miniforge](https://github.com/conda-forge/miniforge) and create one environment:

```bash
conda create -n fenicsx -c conda-forge python=3.12 fenics-dolfinx=0.10 petsc4py mpich xgems=2.1 pyyaml pandas matplotlib scipy jupyterlab
conda activate fenicsx
```

FEniCSx does not run natively on Windows. Install WSL (`wsl --install` in an administrator PowerShell),
open the Ubuntu terminal and run the two commands above there.

## Tested versions

The tutorials on this site were run with the conda-forge packages below (Linux, October 2026). Other versions may work, but
dolfinx changes its Python API between minor releases (0.9 → 0.10), so keep **dolfinx 0.10.x** unless you are ready to adapt `transport.py`.

| package | version |
|---|---|
| Python | 3.12.13 |
| fenics-dolfinx | 0.10.0 (basix 0.10.0, ffcx 0.10.0, ufl 2025.2.1) |
| PETSc / petsc4py | 3.25.6 |
| mpi4py / mpich | 4.1.2 / 5.0.1 |
| xgems (GEMS3K) | 2.1.2 |
| pyyaml | 6.0.3 |
| numpy | 2.5.4 |
| pandas / matplotlib / scipy | 3.0.6 / 3.11.2 / 1.18.1 (tutorials only) |
| jupyter-book | 1.0.4 (building this site only; version 2 is not compatible) |

To check what you have:

```bash
conda list -n fenicsx | grep -E "dolfinx|petsc|xgems|pyyaml|numpy"
```

## Get the code

The code is the folder `FEniCSx_GEMS` in this site's repository:

```text
FEniCSx_GEMS/
├── coupling.py        reads case.yaml, time loop, data exchange, feedback
├── transport.py       FEniCSx mesh, boundary conditions, solver
├── chemistry.py       GEMS engine, recipes, local equilibrium
├── output.py          CSV / XDMF / PNG / summary files
├── case.yaml          the input
├── chemistry_data/    the GEMS project used by case.yaml
├── example/           the cases of Tutorials 3 to 5
├── case_builder.html  browser form that writes case.yaml
└── gems_inspector.html browser viewer for GEMS projects
```

## Check the environment

```bash
cd FEniCSx_GEMS
python -c "import dolfinx, xgems, yaml; print(dolfinx.__version__, dolfinx.has_petsc)"
```

The output should end with `True`. A FEniCSx build without PETSc imports fine, but `transport.py` then stops with
`No module named 'petsc4py'`.

Then run [Tutorial 1](tutorials/01_tracer_diffusion.ipynb). It needs FEniCSx but not GEMS. [Tutorial 2](tutorials/02_single_equilibrium.ipynb) needs GEMS but not FEniCSx.
Together they test both halves.

## Windows: `Run.cmd`

`Run.cmd` calls the WSL Python of the environment directly, so a double-click runs `case.yaml`
in the same folder:

```bat
wsl /home/<user>/miniforge3/envs/fenicsx/bin/python ../../coupling.py "%CASE_FILE%"
```

Change `/home/<user>/miniforge3/envs/fenicsx` to the path of your environment (`conda env list` shows it).
`Run.cmd other.yaml` runs a different input file.

## Running more than one process

This version runs on one MPI process only (`transport.py` stops with *This version supports one MPI process*).
In 1D the mesh is small. Almost all of the run time is spent in GEMS, one equilibrium per cell and step.
