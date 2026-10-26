from nb import NB

nb = NB()
nb.md(en=r"""
# 4. Cement leaching

**Goal.** Put minerals into the column and let them react. A 4 mm hydrated cement paste is in contact with a CaCl₂ water for
1000 years. Ca diffuses out, portlandite dissolves from the surface inwards, and C-S-H decalcifies behind the front. This is the sequence
of the [Ca/Si scan in Tutorial 2](02_single_equilibrium.ipynb), now as a function of depth.

New in `case.yaml`:

- **`solid_phases`** with real minerals, and `gibbs` adjustments taken from the benchmark;
- **one `inlet` recipe** on a `dirichlet` left boundary, and a `no_flux` right boundary;
- **long times**: `dt` = 0.1 year and `end` = 1000 years, both in seconds;
- **feedback switches**: the benchmark keeps φ and De constant; at the end we switch them on.

| | |
|---|---|
| Mode | `coupled` |
| Case folder | `FEniCSx_GEMS/example/demo_Cement_1D_benchmark` (this notebook runs there) |
| Domain | 4 mm, 40 cells, 10 000 steps |
| Runtime | about 5 min per run; 400 000 GEMS equilibria |
| Reference | HYDRUS profiles of the same benchmark, `Profile_HYDRUS.out` |
""")
nb.code(r"""
print(open('case.yaml').read())
""")
nb.md(en=r"""
Notes on the numbers:

- `project: ../../chemistry_data/b_time0-dat.lst`: this case uses the GEMS project in the main folder, the same one as Tutorial 2.
- `De: 5.0e-15` is $\phi D_p$ with the benchmark's pore diffusion coefficient $D_p = 10^{-14}$ m²/s.
- `dt: 3155760` s is 0.1 year. With $D_p\,\Delta t/h^2 \approx 3$, an explicit scheme would be unstable. Backward Euler is not.
- `every: 1000` writes a profile every 100 years.

## Run

Progress is printed every 1000 steps.
""")
nb.code(r"""
import time
t0 = time.time()
!python ../../coupling.py case.yaml 2>&1 | grep -v gems3k | grep -E "step=.*000,|Saved"
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
Portlandite disappears from a growing zone at the surface, with a sharp front. Behind it pH drops from about 12.5 to below 12
and the C-S-H loses Ca.

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
stores the boundary water itself (pH 7.6), while this model's first value is the centre of the first cell. The remaining differences come from the different grids (the reference stores values at nodes, including the boundary node;
here the boundary sits half a cell from the first cell centre), the time stepping and GEMS round-off.

Under diffusion control the front moves as $\sqrt{t}$:
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
## Switch on porosity and diffusivity feedback

The benchmark keeps φ and De fixed. In reality, dissolving portlandite opens pores, and diffusion becomes faster in the leached zone.
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
!python ../../coupling.py case_feedback.yaml 2>&1 | grep -v gems3k | grep -E "Saved"
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
Dissolution raises φ near the surface from 0.50 to about 0.55, and De rises with $(\phi/\phi_0)^2$ by about 20 %. The effect on the front is small here and
goes the other way from what one might guess: the portlandite front ends up about 0.1 mm *behind* the constant-property run. Portlandite fills only a few percent
of the volume, so φ changes little, and the leached zone now also holds more pore water. Check effects like this with a run rather than assuming them.
The exponent is a model choice, not a property of the paste.

**Next:** [Tutorial 5](05_calcite_dolomite.ipynb) adds flow.
""")
nb.save('04_cement_leaching')
