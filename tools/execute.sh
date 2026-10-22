#!/bin/bash
# Generate, execute and localize one tutorial:
#   tools/execute.sh 01_tracer_diffusion tut_01_tracer            (runs in _build_src/)
#   tools/execute.sh 03_nacl_diffusion tut_03_nacl demo_NaCl_diffusion
#        (runs inside a scratch copy of FEniCSx_GEMS/example/demo_NaCl_diffusion)
# Needs a Python with dolfinx (+PETSc), xgems and pyyaml (FX_BIN, registered as Jupyter kernel "fx").
set -e
BOOK=$(cd "$(dirname "$0")/.." && pwd)
FX_BIN=${FX_BIN:-/home/claude/mm/root/envs/fx/bin}
cd "$BOOK/tools" && python3 "$2.py"
RUN="$BOOK/_build_src"
if [ -n "$3" ]; then
  mkdir -p "$BOOK/_build_src/work"
  cp -r "$BOOK/FEniCSx_GEMS" "$BOOK/_build_src/work/"
  RUN="$BOOK/_build_src/work/FEniCSx_GEMS/example/$3"
  cp "$BOOK/_build_src/$1.ipynb" "$RUN/"
fi
cd "$RUN"
PATH="$FX_BIN:$PATH" jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=fx \
     --ExecutePreprocessor.timeout=7200 "$1.ipynb" --output "$1.executed.ipynb"
[ -n "$3" ] && cp "$RUN/$1.executed.ipynb" "$BOOK/_build_src/"
cd "$BOOK/tools" && python3 -c "from nb import localize; localize('$1', ${LANGS:-('en',)})"
