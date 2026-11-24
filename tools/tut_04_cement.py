from nb import NB

nb = NB()
nb.md(en=r"""
# 4. Cement leaching

**Question.** How does a hydrated cement paste degrade when its surface is in contact with a low-Ca water for a long time, and does
the coupled code reproduce a published benchmark of this process?

## The physical problem

A slab of hydrated cement paste, 4 mm thick, the same material as in [Tutorial 2](02_single_equilibrium.ipynb): portlandite and C-S-H,
pore water at pH 12.45. Its left face is in permanent contact with a large volume of groundwater containing 14.6 mM CaCl₂ (pH about 7.6);
the right face is sealed. Over 1000 years:

- Ca diffuses out of the paste into the low-Ca water, and Cl diffuses in;
- portlandite dissolves first, from the surface inwards, leaving a front that moves into the paste;
- behind that front C-S-H loses Ca, and the pH falls.

## Model assumptions

- saturated pores, transport by diffusion only, one effective diffusion coefficient for all elements;
- local equilibrium in every cell at every step (no kinetics); phases and data from the GEMS project of Tutorial 2, with the benchmark's Gibbs-energy adjustments;
- the contact water never changes (a Dirichlet boundary): the reservoir is assumed large and well mixed;
- **in the benchmark run φ and De stay constant** even though minerals dissolve; this is the benchmark's simplification. In the second run the feedback is switched on.

## From assumptions to `case.yaml`

| assumption | key in `case.yaml` |
|---|---|
| the paste | `chemistry.initial` (same recipe as Tutorial 2), `material.phi: 0.5` |
| minerals that react and are reported | `chemistry.solid_phases: [CSHQ, Portlandite, Silica-amorph]` |
| contact water, fixed for 1000 years | `chemistry.inlet` (14.6 mM CaCl₂), left boundary `dirichlet` |
| sealed back face | right boundary `no_flux` |
| benchmark diffusion coefficient | `material.De: 5.0e-15` = $\phi D_p$ with $D_p = 10^{-14}$ m²/s |
| constant φ and De (benchmark) | `update_porosity: false`, `update_diffusivity: false` |
| 1000 years in steps of 0.1 year | `coupling.time` (in seconds) |

| | |
|---|---|
| Case folder | `FEniCSx_GEMS/example/demo_Cement_1D_benchmark` (this notebook runs there) |
| Domain | 4 mm, 40 cells, 10 000 steps |
| Runtime | 3–5 min per run; 400 000 GEMS equilibria |
| Reference | HYDRUS profiles of the same benchmark, `Profile_HYDRUS.out` |
""")
nb.code(r"""
import os, sys
from pathlib import Path
# Find the FEniCSx_GEMS folder, wherever this notebook is opened inside the repository
here = Path.cwd()
code = next(p / 'FEniCSx_GEMS' for p in [here, *here.parents] if (p / 'FEniCSx_GEMS' / 'coupling.py').exists())
PY = sys.executable                         # the Python of this kernel runs coupling.py
os.chdir(code / 'example' / 'demo_Cement_1D_benchmark')          # the case folder
print(open('case.yaml').read())
""")
nb.md(en=r"""
Notes on the numbers:

- `project: ../../chemistry_data/b_time0-dat.lst`: this case uses the GEMS project in the main folder, the same one as Tutorial 2.
- `dt: 3155760` s is 0.1 year. With $D_p\,\Delta t/h^2 \approx 3$, an explicit scheme would be unstable. Backward Euler is not, but stability
  says nothing about accuracy; the time step is the benchmark's choice and is not checked here.
- `every: 1000` writes a profile every 100 years.

## Run

Progress is printed every 1000 steps.
""")
nb.code(r"""
import time
t0 = time.time()
!{PY} ../../coupling.py case.yaml 2>&1 | grep -v gems3k | grep -E "step=.*000,|Saved"
print(f'{(time.time() - t0) / 60:.1f} min')
""")
nb.code(r"""
print(open('results_benchmark/summary.txt').read())
""")

nb.md(en=r"""
## The leached profile

Mineral amounts are in mol per m³ of bulk. Divide by 1000 for mol/dm³.
""")
nb.code(r"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
YEAR = 365.25 * 86400
p = pd.read_csv('results_benchmark/profiles.csv')
p['t_yr'] = (p.time_s / YEAR).round(3)

fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
for t, g in p.groupby('t_yr'):
    if t in (0, 100, 300, 600, 1000):
        g = g.sort_values('x_m')
        axes[0].plot(g.x_m * 1e3, g.Portlandite_mol_m3_bulk / 1000, label=f'{t:g} yr')
        axes[1].plot(g.x_m * 1e3, g.CSHQ_mol_m3_bulk / 1000)
        axes[2].plot(g.x_m * 1e3, g.pH)
axes[0].set(title='Portlandite (mol/dm³ bulk)', xlabel='x (mm)'); axes[0].legend(fontsize=8)
axes[1].set(title='C-S-H (CSHQ, mol/dm³ bulk)', xlabel='x (mm)')
axes[2].set(title='pH', xlabel='x (mm)')
plt.tight_layout(); plt.show()
""")
nb.md(en=r"""
**How to read this.** Portlandite disappears from a zone at the surface that grows with time, and the edge of that zone is sharp: a
dissolution front. Behind it the pH drops from about 12.5 to below 12 and C-S-H loses Ca, as in the Ca/Si scan of Tutorial 2. Two
things to check in your own run: the mass balance in `summary.txt` stays at round-off level, and no GEMS failures or skipped cells are reported.

## Comparison with the HYDRUS benchmark

`Profile_HYDRUS.out` reports everything per dm³ of bulk, so the model output is converted:

$$
X_\text{aq} = \frac{\phi\,c_X}{1000},\qquad X_\text{s} = \frac{\text{total}_X - \phi\,c_X}{1000},\qquad
\text{Ca}_\text{ss} = \text{Ca}_\text{s} - \text{Portlandite}
$$
""")
nb.code(r"""
sim = pd.DataFrame({'Time': p.t_yr, 'Distance': p.x_m, 'pH': p.pH})
for n in ('Ca', 'Si'):
    aq = p[f'{n}_c_mol_m3_water'] * p.phi
    sim[f'{n}_aq'] = aq / 1000
    sim[f'{n}_s'] = (p[f'{n}_total_mol_m3_bulk'] - aq) / 1000
sim['Portlandite'] = p.Portlandite_mol_m3_bulk / 1000
sim['Ca_ss'] = sim.Ca_s - sim.Portlandite
bench = pd.read_csv('Profile_HYDRUS.out', sep=r'\s+')
bench = bench.loc[:, ~bench.columns.str.startswith('Unnamed')]

cols = ['pH', 'Ca_aq', 'Portlandite', 'Ca_ss']
fig, axes = plt.subplots(1, 4, figsize=(14, 3.4))
for k, t in enumerate((200, 600, 1000)):
    b = bench[np.isclose(bench.Time, t)].sort_values('Distance')
    s = sim[np.isclose(sim.Time, t)].sort_values('Distance')
    for ax, c in zip(axes, cols):
        ax.plot(b.Distance * 1e3, b[c], '-', lw=2.4, alpha=0.4, color=f'C{k}', label=f'HYDRUS {t} yr')
        ax.plot(s.Distance * 1e3, s[c], '--', lw=1.2, color=f'C{k}', label=f'FEniCSx+GEMS {t} yr')
for ax, c in zip(axes, cols):
    ax.set(title=c, xlabel='x (mm)')
axes[0].legend(fontsize=7); plt.tight_layout(); plt.show()

rows = []   # RMS over the reference nodes inside the paste (x > 0; x = 0 is the boundary water in the reference)
for t in (200, 600, 1000):
    b = bench[np.isclose(bench.Time, t) & (bench.Distance > 0)].sort_values('Distance')
    s = sim[np.isclose(sim.Time, t)].sort_values('Distance')
    rows.append({'t (yr)': t, **{c: np.sqrt(np.mean((np.interp(b.Distance, s.Distance, s[c]) - b[c]) ** 2)) for c in cols}})
pd.DataFrame(rows).set_index('t (yr)').style.format('{:.2e}')
""")
nb.md(en=r"""
Thick lines are HYDRUS and dashed lines are this model. The two codes put the portlandite front within about one cell (0.1 mm) of each other. The table
gives the RMS difference over the reference nodes inside the paste, in the units of each column. The node at x = 0 is left out, because there the reference
stores the boundary water itself (pH 7.6), while this model's first value is the centre of the first cell.

Where do the remaining differences come from? Possible causes are the different grids (the reference stores values at nodes, including the boundary
node; here the boundary sits half a cell from the first cell centre), the different transport schemes and time stepping, and GEMS round-off. These
causes have not been separated here; a mesh and time-step refinement of both codes would be needed for that.

If the leaching is controlled by diffusion, the front position should grow as $\sqrt{t}$, i.e. lie on a straight line in the plot below:
""")
nb.code(r"""
def front(df, t, frac=0.5):
    d = df[np.isclose(df.Time, t)].sort_values('Distance')
    f = d.Portlandite.to_numpy() / df[np.isclose(df.Time, 0)].Portlandite.max()
    i = np.argmax(f >= frac)
    if i == 0:
        return 0.0
    x = d.Distance.to_numpy()
    return (x[i - 1] + (frac - f[i - 1]) / (f[i] - f[i - 1]) * (x[i] - x[i - 1])) * 1e3

times = np.array(sorted(set(sim.Time) & set(bench.Time)))
fig, ax = plt.subplots(figsize=(5, 3.4))
ax.plot(np.sqrt(times), [front(bench, t) for t in times], 'o-', alpha=0.5, lw=2.2, label='HYDRUS')
ax.plot(np.sqrt(times), [front(sim, t) for t in times], 's--', ms=4, label='FEniCSx + GEMS')
ax.set(xlabel='√t (√yr)', ylabel='portlandite front (mm)'); ax.legend(); plt.tight_layout(); plt.show()
""")

nb.md(en=r"""
## Change one assumption: porosity and diffusivity feedback

The benchmark keeps φ and De fixed. Physically, dissolving portlandite frees pore space, and a more open pore structure lets solutes diffuse
faster. Switching the feedback on changes two model assumptions:

- φ now follows the volume of the minerals in `solid_phases`: $\phi = \phi_0 + V_\text{solid,0} - V_\text{solid}$;
- De follows φ through an assumed law, $D_e = D_{e,0}(\phi/\phi_0)^m$ with $m = 2$. The exponent is a model choice, not a measured property of this paste.

Two lines in `case.yaml` switch this on. We write a copy with a new output folder:

```yaml
coupling:
  update_porosity: true      # phi = phi0 + V_solid0 - V_solid
  update_diffusivity: true   # De = De0 (phi/phi0)^2
output:
  folder: results_feedback
```
""")
nb.code(r"""
import yaml
case = yaml.safe_load(open('case.yaml'))
case['coupling']['update_porosity'] = True
case['coupling']['update_diffusivity'] = True
case['output']['folder'] = 'results_feedback'
yaml.safe_dump(case, open('case_feedback.yaml', 'w'), sort_keys=False)
!{PY} ../../coupling.py case_feedback.yaml 2>&1 | grep -v gems3k | grep -E "Saved"
""")
nb.code(r"""
q = pd.read_csv('results_feedback/profiles.csv'); q['t_yr'] = (q.time_s / YEAR).round(3)
fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
for k, t in enumerate((300, 1000)):
    a = p[np.isclose(p.t_yr, t)].sort_values('x_m'); b = q[np.isclose(q.t_yr, t)].sort_values('x_m')
    axes[0].plot(a.x_m * 1e3, a.Portlandite_mol_m3_bulk / 1000, '--', color=f'C{k}', label=f'constant φ, {t} yr')
    axes[0].plot(b.x_m * 1e3, b.Portlandite_mol_m3_bulk / 1000, '-', color=f'C{k}', label=f'feedback, {t} yr')
    axes[1].plot(b.x_m * 1e3, b.phi, color=f'C{k}', label=f'{t} yr')
    axes[2].plot(b.x_m * 1e3, b.De_m2_s, color=f'C{k}')
axes[0].set(title='Portlandite (mol/dm³ bulk)', xlabel='x (mm)'); axes[0].legend(fontsize=7)
axes[1].set(title='porosity φ', xlabel='x (mm)'); axes[1].legend(fontsize=8)
axes[2].set(title='De (m²/s)', xlabel='x (mm)')
plt.tight_layout(); plt.show()
print(open('results_feedback/summary.txt').read().split('Final porosity')[1][:120])
""")
nb.md(en=r"""
**How to read this.** Dissolution raises φ near the surface from 0.50 to about 0.55, and De rises with $(\phi/\phi_0)^2$ by about 20 %. The effect on
the front is small here and goes the other way from what one might expect: the portlandite front ends up about 0.1 mm *behind* the
constant-property run. One possible reason is that portlandite fills only a few percent of the volume, so φ changes little, while the
leached zone now holds more pore water; this has not been tested further. The result shows why such feedback should be checked with a run
rather than assumed.

## What this tutorial shows

- The coupled code produces the expected leaching sequence (portlandite front, C-S-H decalcification, pH drop) and puts the front within
  about one cell of the HYDRUS benchmark over 1000 years.
- Switching on the porosity–diffusivity feedback changes the assumptions of the model, and its effect has to be evaluated, not guessed.
- It does not show which numerical choices cause the remaining differences to HYDRUS, nor whether the feedback law fits a real paste.

**Next:** [Tutorial 5](05_calcite_dolomite.ipynb) adds flow.
""")
nb.save('04_cement_leaching')
