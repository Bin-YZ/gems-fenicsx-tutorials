from nb import NB

nb = NB()
nb.md(en=r"""
# 2. One chemical equilibrium

**Question.** What does GEMS compute for a given material, how do you describe that material in `case.yaml`, and how do you
check a recipe before a long coupled run?

## The physical problem

A small sample of hydrated cement paste: per dm³ it contains 1.12 mol Ca, 0.31 mol Si, half a litre of water and a trace of Cl. Which
minerals does it contain at equilibrium, what is the composition of its pore water, and what is the pH? Then: how do minerals and pH
change if the paste contains more silica?

## Model assumptions

- a closed sample: nothing enters or leaves, there is no transport and no time;
- full thermodynamic equilibrium at 25 °C and 1 bar (no kinetics);
- the phases, species and solution models are those of the GEMS project; only CSHQ, portlandite and amorphous silica are reported;
- two standard Gibbs energies are adjusted to the values of the benchmark this system comes from.

## From assumptions to `case.yaml`

| assumption | key in `case.yaml` |
|---|---|
| one equilibrium, no mesh, no time | `coupling.mode: chemistry` |
| the chemical system | `chemistry.project` (the GEMS files) |
| 25 °C, 1 bar | `chemistry.temperature: 298.15`, `pressure: 100000` |
| composition of the sample | `chemistry.initial` (mol per dm³ of bulk material) |
| minerals to report | `chemistry.solid_phases` |
| adjusted Gibbs energies | `chemistry.gibbs` |

`transport` and `coupling` must still be present; in this mode only `transport.material.phi` is used, to turn dissolved amounts
into pore-water concentrations.
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
import os, sys
from pathlib import Path
# Find the FEniCSx_GEMS folder, wherever this notebook is opened inside the repository
here = Path.cwd()
code = next(p / 'FEniCSx_GEMS' for p in [here, *here.parents] if (p / 'FEniCSx_GEMS' / 'coupling.py').exists())
PY = sys.executable                         # the Python of this kernel runs coupling.py
work = code.parent / 'tutorial_runs'       # tutorial cases go here, next to FEniCSx_GEMS
work.mkdir(exist_ok=True)
os.chdir(work)
os.makedirs('t02_equilibrium', exist_ok=True)
print('working in', work.name, 'next to', code.name)
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
!{PY} ../FEniCSx_GEMS/coupling.py t02_equilibrium/case.yaml 2>&1 | grep -v gems3k
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
**How to read this.** pH 12.45 with about 605 mol/m³ portlandite: the paste is saturated with portlandite, which buffers the pH.
Most of the Si is bound in C-S-H, and amorphous silica is not stable. This is the usual assemblage of a hydrated Portland cement
paste, so the recipe and the phase names are consistent.

Two checks before using a recipe in a coupled run:

- the **chemical element reconstruction error** in `summary.txt` (how well GEMS reproduces the recipe; here about 10⁻¹¹ mol/m³)
  should be at round-off level;
- the **aqueous-volume/porosity mismatch**: GEMS computes the volume of the solution from its own data and compares it with `phi`.
  In the supplied examples it is a few tenths of a percent; that is an observation, not an acceptance threshold. A large value means the
  recipe's water content does not match the porosity you set in `transport.material`.
""")
nb.code(r"""
print([l for l in open('t02_equilibrium/results/summary.txt') if 'mismatch' in l][0])
""")

nb.md(en=r"""
## Scan the recipe: more silica, lower Ca/Si

A recipe is easy to change, so it is easy to explore. Here Ca and the water stay fixed and SiO₂ is added (per mol of Si also 2 mol of O),
so the bulk Ca/Si falls from 3.7 to 0.5. Each value is one independent equilibrium with `mode: chemistry`.

Note what this scan is and is not: it is a series of closed samples with different compositions. In real leaching Ca *leaves* the paste;
the path is different, but the bulk Ca/Si also falls, so the sequence of phase assemblages is a useful guide.
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
    subprocess.run([PY, '../FEniCSx_GEMS/coupling.py', 't02_equilibrium/scan.yaml'],
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
**How to read this.** Three regions appear as Ca/Si falls:

- Ca/Si above about 1.5: portlandite is present and fixes the pH at 12.45;
- between about 1.5 and 0.65: portlandite is gone, C-S-H takes up the added Si, and the pH drops from 12.3 to about 10;
- below about 0.65: the C-S-H cannot take up more Si, and amorphous silica precipitates; the pH stays near 9.8.

In the coupled leaching of Tutorial 4 the first two stages appear as a portlandite dissolution front and a decalcifying zone behind it.

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
subprocess.run([PY, '../FEniCSx_GEMS/coupling.py', 't02_equilibrium/no_gibbs.yaml'], check=True, capture_output=True)
for folder in ['results', 'results_no_gibbs']:
    r = pd.read_csv(f't02_equilibrium/{folder}/profiles.csv').iloc[0]
    print(f"{folder:17s} pH = {r.pH:.3f}   Ca = {r.Ca_c_mol_m3_water:.2f} mol/m3 water")
""")
nb.md(en=r"""
Without the adjustments the pH changes by 0.015 and dissolved Ca by about 5 %. Small changes of $G^\circ$ therefore matter for a
quantitative comparison with a benchmark. Use `gibbs: {}` unless you have such a reason to change the database.

## What this tutorial shows

- `mode: chemistry` computes one equilibrium of a recipe in about a second; use it to check names, units and the mineral assemblage
  before a coupled run.
- Recipes are element amounts per dm³ of bulk material, including the water; GEMS returns the minerals, the pore water and pH.
- The phase sequence with falling Ca/Si (portlandite → C-S-H only → C-S-H + silica) is the chemistry behind cement leaching.

**Next:** [Tutorial 3](03_nacl_diffusion.ipynb) lets two NaCl solutions diffuse into each other with `mode: coupled`: transport and chemistry in every step.
""")
nb.save('02_single_equilibrium')
