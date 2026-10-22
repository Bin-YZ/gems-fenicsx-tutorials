#!/bin/bash
# usage: tools/execute.sh 01_hayekit   (runs tools/tut_<name>.py, executes, copies into en/zh/de)
set -e
cd "$(dirname "$0")"
python3 tut_$1.py
cd ../_build_src
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=-1 $1.ipynb --output $1.executed.ipynb
cd ../tools
python3 -c "from nb import localize; localize('$1')"
echo done $1
