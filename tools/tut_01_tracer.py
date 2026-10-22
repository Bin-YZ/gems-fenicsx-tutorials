from nb import NB

nb = NB()
nb.md(en=r"""
# 1. First run: tracer diffusion

**Goal.** Run the code once, end to end, without any chemistry. You will

- write a complete `case.yaml` with its four sections,
- run `coupling.py` on it,
- find the result files, and
- check the numbers against an analytical solution.

`coupling.mode: diffusion` switches GEMS off. Only `transport.py` and `output.py` run, so this
case also tells you whether FEniCSx is installed correctly.

| | |
|---|---|
| Mode | `diffusion` |
| Domain | 1D, 10 mm, 50 cells |
| Physics | $\phi\,\partial c/\partial t = \partial_x (D_e\,\partial_x c)$ |
| Runtime | about 2 s |

## Folder layout

This notebook sits next to the `FEniCSx_GEMS` folder. Each tutorial keeps its case in its own folder:

```text
FEniCSx_GEMS/          the four modules + chemistry_data/
t01_tracer/case.yaml   written below
t01_tracer/results/    created by the run
```
""")

nb.md(en=r"""
## Write the input file

`case.yaml` always has the same four sections, one per Python module. In diffusion mode only
`transport`, `coupling` and `output` are read; `chemistry` must still be present but is not used.

The `%%writefile` line below writes the cell into a file. Outside a notebook you would simply
edit `case.yaml` in a text editor.
""")
nb.code(r"""
import os
os.makedirs('t01_tracer', exist_ok=True)
""")
nb.code(r"""
%%writefile t01_tracer/case.yaml
# Tutorial 1: one tracer diffusing through a porous column, no chemistry.

chemistry:                       # not used in diffusion mode, but the section must exist
  project: ../../FEniCSx_GEMS/chemistry_data/b_time0-dat.lst
  temperature: 298.15
  pressure: 100000
  aqueous_phase: aq_gen
  solid_phases: []
  gibbs: {}
  initial: {}

transport:
  geometry:
    length: 0.01                 # m
    cells: 50                    # uniform 1D mesh, dx = 0.2 mm
  material:
    phi: 0.4                     # porosity
    De: 4.0e-10                  # effective diffusion coefficient, m2/s
  components: [tracer]           # names of the transported tracers
  initial: {tracer: 0.0}         # mol/m3 pore water
  boundary:
    left:
      type: dirichlet
      concentrations: {tracer: 1.0}
    right:
      type: dirichlet
      concentrations: {tracer: 0.0}
  solver:
    ksp_type: preonly
    pc_type: lu
    rtol: 1.0e-10
    max_iterations: 1000

coupling:
  mode: diffusion                # diffusion | chemistry | coupled
  time:
    dt: 100                      # s
    end: 20000                   # s
  update_porosity: false         # must be false without chemistry
  update_diffusivity: false
  exponent: 1.0                  # unused here

output:
  folder: results                # relative to this case.yaml
  every: 50                      # write profiles every 50 steps (5000 s)
""")

nb.md(en=r"""
## Run it

From a terminal this is `python FEniCSx_GEMS/coupling.py t01_tracer/case.yaml`
(on Windows: double-click `Run.cmd`, which calls the WSL Python). The `!` runs the same command
from the notebook.
""")
nb.code(r"""
!python ../FEniCSx_GEMS/coupling.py t01_tracer/case.yaml
""")

nb.md(en=r"""
## What the run wrote

Everything goes into `output.folder`. `summary.txt` says whether the run COMPLETED or FAILED and lists the
largest conservation errors.
""")
nb.code(r"""
print(sorted(os.listdir('t01_tracer/results')))
print(open('t01_tracer/results/summary.txt').read())
""")

nb.md(en=r"""
## Compare with the analytical solution

With constant $\phi$ and $D_e$ the equation is ordinary diffusion with the pore diffusion coefficient
$D = D_e/\phi = 10^{-9}$ m²/s. For $c(0,t)=1$, $c(L,t)=0$ and $c(x,0)=0$:

$$
c(x,t) = 1-\frac{x}{L}-\frac{2}{\pi}\sum_{n=1}^{\infty}\frac{1}{n}\sin\frac{n\pi x}{L}\,
\exp\!\left(-\frac{n^2\pi^2 D t}{L^2}\right)
$$

`profiles.csv` has one row per cell and saved time. The tracer concentration is in the column
`tracer_c_mol_m3_water` (mol/m³ pore water); `tracer_total_mol_m3_bulk` is the same amount per bulk volume.
""")
nb.code(r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

p = pd.read_csv('t01_tracer/results/profiles.csv')
L, D = 0.01, 4.0e-10 / 0.4

def exact(x, t, terms=400):
    n = np.arange(1, terms + 1)[:, None]
    return 1 - x / L - 2 / np.pi * np.sum(np.sin(n * np.pi * x / L) / n * np.exp(-(n * np.pi) ** 2 * D * t / L ** 2), axis=0)

fig, ax = plt.subplots(figsize=(6.5, 3.6))
xf = np.linspace(0, L, 400)
for t, g in p[p.time_s > 0].groupby('time_s'):
    line, = ax.plot(g.x_m * 1e3, g.tracer_c_mol_m3_water, 'o', ms=3)
    ax.plot(xf * 1e3, exact(xf, t), '-', color=line.get_color(), lw=1, label=f'{t:.0f} s')
ax.set_xlabel('x (mm)'); ax.set_ylabel('c (mol/m³ pore water)')
ax.set_title('dots: FEniCSx (DG0 cells), lines: analytical')
ax.legend(); plt.tight_layout(); plt.show()

last = p[p.time_s == p.time_s.max()]
err = np.max(np.abs(last.tracer_c_mol_m3_water - exact(last.x_m.values, last.time_s.values[0])))
print(f'max |error| at t = {last.time_s.values[0]:.0f} s: {err:.2e} mol/m3')
""")

nb.md(en=r"""
The error is about $10^{-3}$: first-order backward Euler in time plus the cell-centred mesh.
Halve `dt` or double `cells` and it drops.

## Mass balance

The code checks every step that the amount in the column changes only by what crossed the boundaries.
`mass_balance.csv` has the inventory (mol per m² of cross-section), the cumulative boundary input and
their difference.
""")
nb.code(r"""
m = pd.read_csv('t01_tracer/results/mass_balance.csv')
fig, ax = plt.subplots(figsize=(6.5, 3))
ax.plot(m.time_s, m.inventory_mol_m2, label='inventory in the column')
ax.plot(m.time_s, m.cumulative_net_in_mol_m2, '--', label='net input through the boundaries')
ax.set_xlabel('t (s)'); ax.set_ylabel('mol/m²'); ax.legend(); plt.tight_layout(); plt.show()
print('largest balance error:', abs(m.balance_error_mol_m2).max(), 'mol/m2')
""")

nb.md(en=r"""
## Change one thing: a closed right end

Inputs are only ever changed in `case.yaml`. Here we load the file, close the right boundary
(`no_flux`), send results to another folder and run again. In a text editor this is a two-line change:

```yaml
    right:
      type: no_flux
...
output:
  folder: results_noflux
```
""")
nb.code(r"""
import yaml
case = yaml.safe_load(open('t01_tracer/case.yaml'))
case['transport']['boundary']['right']['type'] = 'no_flux'
case['coupling']['time']['end'] = 100000
case['output']['folder'] = 'results_noflux'
yaml.safe_dump(case, open('t01_tracer/case_noflux.yaml', 'w'), sort_keys=False)
!python ../FEniCSx_GEMS/coupling.py t01_tracer/case_noflux.yaml > /dev/null && tail -n 1 t01_tracer/results_noflux/simulation.log
""")
nb.code(r"""
q = pd.read_csv('t01_tracer/results_noflux/profiles.csv')
fig, ax = plt.subplots(figsize=(6.5, 3.4))
for t, g in q[q.time_s > 0].groupby('time_s'):
    ax.plot(g.x_m * 1e3, g.tracer_c_mol_m3_water, label=f'{t:.0f} s')
ax.set_xlabel('x (mm)'); ax.set_ylabel('c (mol/m³ pore water)')
ax.set_title('right boundary closed: the column fills up to c = 1')
ax.legend(); plt.tight_layout(); plt.show()
""")

nb.md(en=r"""
## Try it yourself

1. Set `cells: 10` and compare the error with the 50-cell run.
2. Set `dt: 1000`. Backward Euler stays stable, but how large is the error now?
3. Add a second tracer: `components: [tracer, salt]`, and give `salt` a value in `initial` and in
   both boundary `concentrations`.
4. Try an invalid input, for example `update_porosity: true` in diffusion mode, and read the error message.

**Next:** [Tutorial 2](02_single_equilibrium.ipynb) switches on GEMS and computes one chemical equilibrium.
""")
nb.save('01_tracer_diffusion')
