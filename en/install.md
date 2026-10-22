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
conda create -n fenicsx -c conda-forge python=3.12 fenics-dolfinx petsc4py mpich xgems pyyaml pandas matplotlib jupyterlab
conda activate fenicsx
```

FEniCSx does not run natively on Windows. Install WSL (`wsl --install` in an administrator PowerShell),
open the Ubuntu terminal and run the two commands above there.

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
