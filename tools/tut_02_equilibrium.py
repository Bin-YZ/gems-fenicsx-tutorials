from nb import NB

nb = NB()
nb.md(en=r"""
# 2. One chemical equilibrium

**Goal.** Switch GEMS on and learn the `chemistry` section of `case.yaml`:

- which names you may write (elements, phases),
- what the recipe numbers mean and their units,
- what GEMS returns, and
- what the `gibbs` adjustments do.

`coupling.mode: chemistry` runs exactly one equilibrium with the `initial` recipe. No mesh is built and
no time steps are taken. It is the quickest way to check a recipe before you start a long coupled run.

| | |
|---|---|
| Mode | `chemistry` |
| System | CaO–SiO₂–H₂O (+Cl), phases CSHQ, Portlandite, amorphous silica |
| Runtime | about 1 s per equilibrium |
""")

nb.md(en=r"""
## What is in a GEMS project?

GEMS-Selektor exports a chemical system as four files:

| file | content |
|---|---|
| `*-dat.lst` | list of the other three files; this is what `chemistry.project` points to |
| `*-dch.json` / `.dat` | chemical data: elements, species, phases, thermodynamic data |
| `*-ipm.json` / `.dat` | numerical settings of the solver |
| `*-dbr-0-0000.json` / `.dat` | one example state (temperature, pressure, bulk composition) |

Names in `case.yaml` must match the names in these files exactly, including case. The browser page
[GEMS Chemistry Inspector](../tools/inspector.md) shows them without Python. From Python, `xgems` lists them directly:
""")
nb.code(r"""
import xgems
g = xgems.ChemicalEngine('../FEniCSx_GEMS/chemistry_data/b_time0-dat.lst')
print('elements:', [g.elementName(k) for k in range(g.numElements())])
print('phases:  ', [g.phaseName(k) for k in range(g.numPhases())])
""")
nb.md(en=r"""
- **Elements** are what is transported and what you write in recipes. `Zz` is charge; it is never transported
  and never needs a value.
- **Phases**: `aq_gen` is the aqueous solution and becomes `chemistry.aqueous_phase`. The solids you want
  to follow go into `chemistry.solid_phases`. Their amounts are written to the output, and their volumes
  enter the porosity update in later tutorials.
""")

nb.md(en=r"""
## Write the input file

The recipe is a hydrated cement paste: 1.119 mol Ca and 0.310 mol Si per dm³ of **bulk** material
(pore water + solids), with 0.5 dm³ of water. The amounts are whole elements, not oxides. H and O include the water.
""")
nb.code(r"""
import os
os.makedirs('t02_equilibrium', exist_ok=True)
""")
nb.code(r"""
%%writefile t02_equilibrium/case.yaml
# Tutorial 2: one GEMS equilibrium of a cement paste.

chemistry:
  project: ../../FEniCSx_GEMS/chemistry_data/b_time0-dat.lst   # relative to this file
  temperature: 298.15            # K
  pressure: 100000               # Pa
  aqueous_phase: aq_gen
  solid_phases: [CSHQ, Portlandite, Silica-amorph]
  gibbs: {H2O@: -237183.0, Ca+2: -552400.0}    # J/mol, applied in memory only
  initial:                       # mol per 1 dm3 of bulk sample
    Ca: 1.119218076064
    Si: 0.31000148638994
    H: 58.52226105076
    O: 31.00037832923
    Cl: 1.0e-15

transport:                       # only geometry.length is used in chemistry mode
  geometry: {length: 0.004, cells: 40}
  material: {phi: 0.5, De: 5.0e-15}
  components: [tracer]
  initial: {tracer: 0.0}
  boundary:
    left: {type: no_flux, concentrations: {tracer: 0.0}}
    right: {type: no_flux, concentrations: {tracer: 0.0}}
  solver: {ksp_type: preonly, pc_type: lu, rtol: 1.0e-10, max_iterations: 1000}

coupling:
  mode: chemistry
  time: {dt: 1, end: 1}          # not used in chemistry mode
  update_porosity: false
  update_diffusivity: false
  exponent: 1.0

output:
  folder: results
  every: 1
""")
nb.md(en=r"""
The `transport` and `coupling` blocks are written here in YAML's compact `{key: value}` form. It means
exactly the same as the indented form in Tutorial 1.
""")
nb.code(r"""
!python ../FEniCSx_GEMS/coupling.py t02_equilibrium/case.yaml 2>&1 | grep -v gems3k
""")

nb.md(en=r"""
## Read the result

`profiles.csv` has a single row in chemistry mode. Units:

- `*_total_mol_m3_bulk`: the recipe ×1000 (mol/dm³ → mol/m³). The code works in mol/m³ internally.
- `*_c_mol_m3_water`: dissolved concentration, mol per m³ of **pore water**, using `transport.material.phi`.
- `<phase>_mol_m3_bulk`: moles of each phase listed in `solid_phases`.
""")
nb.code(r"""
import pandas as pd
r = pd.read_csv('t02_equilibrium/results/profiles.csv').iloc[0]
print(f"pH = {r.pH:.3f}")
print('dissolved (mol/m3 pore water):', {e: f"{r[e + '_c_mol_m3_water']:.3g}" for e in ['Ca', 'Si', 'Cl']})
print('solids (mol/m3 bulk):         ', {p: round(float(r[p + '_mol_m3_bulk']), 1) for p in ['CSHQ', 'Portlandite', 'Silica-amorph']})
""")
nb.md(en=r"""
The paste is saturated with portlandite (pH ≈ 12.5). Most of the Si sits in C-S-H. Amorphous silica is not stable here.

`summary.txt` also reports the **aqueous-volume/porosity mismatch**. GEMS computes the volume of the solution
from its own data and compares it with `phi`. A few tenths of a percent is normal. A large value means the recipe's
water content does not match the porosity you set in `transport.material`.
""")
nb.code(r"""
print([l for l in open('t02_equilibrium/results/summary.txt') if 'mismatch' in l][0])
""")

nb.md(en=r"""
## Scan the recipe: from portlandite to silica

A recipe is easy to change, so it is easy to explore. Here we keep Ca and the water fixed and add SiO₂: per mol of Si
we also add 2 mol of O. Each value is one run of the same code with `mode: chemistry`.
""")
nb.code(r"""
import yaml, subprocess
import numpy as np
base = yaml.safe_load(open('t02_equilibrium/case.yaml'))
O_without_Si = base['chemistry']['initial']['O'] - 2 * base['chemistry']['initial']['Si']

rows = []
for Si in np.linspace(0.3, 2.4, 15):
    case = yaml.safe_load(open('t02_equilibrium/case.yaml'))
    case['chemistry']['initial']['Si'] = float(Si)
    case['chemistry']['initial']['O'] = float(O_without_Si + 2 * Si)
    case['output']['folder'] = f'scan/Si_{Si:.2f}'
    yaml.safe_dump(case, open('t02_equilibrium/scan.yaml', 'w'), sort_keys=False)
    subprocess.run(['python', '../FEniCSx_GEMS/coupling.py', 't02_equilibrium/scan.yaml'],
                   check=True, capture_output=True)
    r = pd.read_csv(f't02_equilibrium/scan/Si_{Si:.2f}/profiles.csv').iloc[0]
    rows.append(dict(Ca_Si=1.119218076064 / Si, pH=r.pH, CSHQ=r.CSHQ_mol_m3_bulk,
                     Portlandite=r.Portlandite_mol_m3_bulk, Silica=r['Silica-amorph_mol_m3_bulk']))
scan = pd.DataFrame(rows)
scan.round(2)
""")
nb.code(r"""
import matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
for name in ['CSHQ', 'Portlandite', 'Silica']:
    a1.plot(scan.Ca_Si, scan[name], 'o-', ms=3, label=name)
a1.set_xlabel('Ca/Si of the recipe'); a1.set_ylabel('mol/m³ bulk'); a1.invert_xaxis(); a1.legend()
a2.plot(scan.Ca_Si, scan.pH, 'o-', ms=3, color='k')
a2.set_xlabel('Ca/Si of the recipe'); a2.set_ylabel('pH'); a2.invert_xaxis()
plt.tight_layout(); plt.show()
""")
nb.md(en=r"""
From left to right the bulk Ca/Si falls, as it does in a paste that loses Ca by leaching. Portlandite runs out first. The C-S-H then
loses Ca and pH drops. At the lowest Ca/Si amorphous silica appears. A coupled run (Tutorial 4) goes through the same sequence,
cell by cell, as Ca diffuses out.

## What do the `gibbs` adjustments do?

`chemistry.gibbs` overwrites the standard molar Gibbs energy $G^\circ$ (J/mol) of named species **in memory only**; the
GEMS files are not changed. This example uses the values of the benchmark it was taken from. Without them the
same recipe gives a different solution:
""")
nb.code(r"""
case = yaml.safe_load(open('t02_equilibrium/case.yaml'))
case['chemistry']['gibbs'] = {}
case['output']['folder'] = 'results_no_gibbs'
yaml.safe_dump(case, open('t02_equilibrium/no_gibbs.yaml', 'w'), sort_keys=False)
subprocess.run(['python', '../FEniCSx_GEMS/coupling.py', 't02_equilibrium/no_gibbs.yaml'], check=True, capture_output=True)
for folder in ['results', 'results_no_gibbs']:
    r = pd.read_csv(f't02_equilibrium/{folder}/profiles.csv').iloc[0]
    print(f"{folder:17s} pH = {r.pH:.3f}   Ca = {r.Ca_c_mol_m3_water:.2f} mol/m3 water")
""")
nb.md(en=r"""
Use `gibbs: {}` unless you have a reason, such as matching a published benchmark, to change the database.

## Try it yourself

1. Remove `Silica-amorph` from `solid_phases`. What changes in the output columns?
2. Write an element that is not in the project, e.g. `Mg: 0.1`, and read the error message.
3. Set `temperature: 323.15` (50 °C) and compare pH and portlandite.
4. Try a recipe in [Case Builder](../tools/case_builder.md): it builds the same YAML from a form.

**Next:** [Tutorial 3](03_nacl_diffusion.ipynb) lets two NaCl solutions diffuse into each other with `mode: coupled`: transport and chemistry in every step.
""")
nb.save('02_single_equilibrium')
