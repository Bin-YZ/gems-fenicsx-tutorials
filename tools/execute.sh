#!/bin/bash
# Generate, execute and localize one tutorial:
#   tools/execute.sh 01_tracer_diffusion tut_01_tracer
# The notebook finds FEniCSx_GEMS itself: tutorials 1-2 work in tutorial_runs/ next to it,
# tutorials 3-5 in FEniCSx_GEMS/example/<case>/.
# Needs a Python with dolfinx (+PETSc), xgems and pyyaml, registered as Jupyter kernel "fx".
set -e
BOOK=$(cd "$(dirname "$0")/.." && pwd)
cd "$BOOK/tools" && python3 "$2.py"
cd "$BOOK/_build_src"
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=fx \
     --ExecutePreprocessor.timeout=7200 "$1.ipynb" --output "$1.executed.ipynb"
cd "$BOOK/tools" && python3 -c "from nb import localize; localize('$1', ${LANGS:-('en','zh','de')})"
