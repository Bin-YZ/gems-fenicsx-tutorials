# FEniCSx + GEMS reactive transport tutorials

Website: <https://bin-yz.github.io/gems-fenicsx-tutorials/> (English / 中文 / Deutsch)

How a 1D FEniCSx transport solver and GEMS3K chemical equilibrium are coupled, how to write the `case.yaml` input file,
five tutorials from tracer diffusion to calcite–dolomite conversion with advection, and five OpenGeoSys-GEM benchmarks
reproduced as verification.

## Repository layout

```text
FEniCSx_GEMS/                 the coupling code (coupling / transport / chemistry / output), case.yaml and examples
GEMS_FEniCSx_OGS5_Template/   template used for the OGS-GEM verification cases
en/  zh/  de/                 page sources per language (Markdown + executed notebooks)
figures/                      figures used on the pages
tools/                        scripts that generate the tutorials and build the site
  tut_0*.py                   tutorial notebook sources (English text + code)
  i18n/*.py                   Chinese and German text of the tutorials
  execute.sh                  generate -> execute -> copy into the three languages
  make_pages.py, build.py     write _config.yml/_toc.yml and build _site/
.github/workflows/deploy.yml  builds and publishes to GitHub Pages on every push to main
```

## Running the code

Requirements (tested versions; see the Installation page for details): Python 3.12, fenics-dolfinx 0.10 with PETSc,
xgems 2.1, pyyaml.

```bash
conda create -n fenicsx -c conda-forge python=3.12 fenics-dolfinx=0.10 petsc4py mpich xgems=2.1 pyyaml pandas matplotlib scipy
conda activate fenicsx
cd FEniCSx_GEMS
python coupling.py case.yaml
```

## Editing and publishing the site

- **Text:** edit the `.md` files in `en/`, `zh/`, `de/`. Tutorial text lives in `tools/tut_0*.py` (English) and
  `tools/i18n/` (Chinese, German); after editing run
  `cd tools && python3 tut_0X_name.py && python3 -c "from nb import localize; localize('0X_name')"`.
- **Re-run a tutorial** (needs the environment above, registered as Jupyter kernel `fx`):
  `tools/execute.sh 03_nacl_diffusion tut_03_nacl demo_NaCl_diffusion`.
- **Local preview:** `pip install "jupyter-book<2"`, then `python tools/make_pages.py && python tools/build.py` and open `_site/index.html`.
- **Publish:** push to `main` (Settings → Pages → Source: GitHub Actions). The workflow only renders the stored notebook
  outputs; it does not re-run the simulations.

## Credits

The OGS input files and reference results come from OGS5GEMDEV. Please cite the original work when you use them
(see the Sources page of the website).
