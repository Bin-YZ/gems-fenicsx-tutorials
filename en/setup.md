# Setup

## Environment

The template needs Python ≥ 3.10 with **dolfinx** (0.8 – 0.10), **xgems**, NumPy, SciPy, pandas and
matplotlib. PETSc is *not* needed: matrices are assembled with dolfinx and solved with SciPy. Everything
runs in a single process.

On Windows use WSL2 (Ubuntu) with miniforge:

```bash
mamba create -n fenicsx -c conda-forge python=3.12 fenics-dolfinx xgems scipy pandas matplotlib jupyterlab
mamba activate fenicsx
python -c "import dolfinx, xgems; print(dolfinx.__version__)"
```

If no xgems package is available for your platform, build it from source
(<https://github.com/gemshub/xgems>, it needs GEMS3K and pybind11).

## Material

```text
GEMS_FEniCSx_OGS5_Template/
  fe_mesh.py  transport.py  flow.py  gems_ogs.py  reactive_transport.py  ogs_models.py  ogs_io.py  compare.py
  cases/1_calcite  2_hayekit  3_opc_quartz  4_comedy2d  5_concretecrack
        run_case.py  gems/  ogs_input/  reference/
```

Each case can be run without the notebooks:

```bash
cd GEMS_FEniCSx_OGS5_Template/cases/1_calcite
python run_case.py          # writes results/ and prints the comparison with OGS
```

The tutorial notebooks contain the same code, cut into steps and explained. They find the template
folder automatically if it lies in the notebook folder or in one of its parents.

## Conventions used everywhere

- **Units:** SI; amounts in mol per node control volume (1 m³ of porous medium in OGS), concentrations in
  mol per m³ of pore water.
- **Ordering:** all arrays are in the node and element order of the OGS mesh file, columns in GEMS order.
- **Chemistry at nodes:** one GEMS system per mesh node, as in OGS.
