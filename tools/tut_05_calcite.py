from nb import NB

nb = NB()
nb.md(en=r"""
# 5. Calcite → dolomite with advection

**Goal.** Add flow. An MgCl₂ solution is pumped into a 0.5 m column of calcite. Calcite dissolves, the released carbonate meets Mg, and
**dolomite** precipitates in a band that travels down the column and dissolves again behind it. This benchmark is used to compare
reactive transport codes ([doi:10.1007/s10596-019-09919-3](https://doi.org/10.1007/s10596-019-09919-3), section 4.4, Fig. 6).

New in `case.yaml`:

- **`transport.material.darcy_flux`**: advection towards $+x$;
- **an `outflow` boundary** on the right, where water leaves with the composition of the last cell;
- **a fine mesh**, because the upwind scheme smears fronts;
- **a GEMS project whose independent components are not all elements** (no `O`);
- a recipe obtained by scaling a GEMS state to φ = 0.32 ([how](../yaml/from_gems.md)).

| | |
|---|---|
| Mode | `coupled` |
| Case folder | `FEniCSx_GEMS/example/demo_calcite_dolomite` (this notebook runs there) |
| Domain | 0.5 m, 1000 cells, 105 steps of 200 s |
| Runtime | about 25 s |
""")
nb.code(r"""
print(open('case.yaml').read())
""")
nb.md(en=r"""
### Flow in `case.yaml`

The benchmark gives a pore velocity $v = 9.375\times10^{-6}$ m/s and a dispersion coefficient $D = 2.01\times10^{-8}$ m²/s. In the
flux form used by the code both are multiplied by φ:

$$
q = \phi v = 0.32 \times 9.375\times10^{-6} = 3.0\times10^{-6}\ \text{m/s},\qquad D_e = \phi D = 6.432\times10^{-9}\ \text{m}^2/\text{s}
$$

```yaml
transport:
  material: {phi: 0.32, De: 6.432e-09, darcy_flux: 3.0e-06}
  boundary:
    left:  {type: dirichlet}   # inflow of chemistry.inlet
    right: {type: outflow}     # water leaves; zero diffusive gradient
```

With flow the left boundary must be `dirichlet` and the right boundary `outflow` or `dirichlet`. Any other combination stops the run at start-up.
The Courant number is $q\,\Delta t/(\phi h) = 9.375\times10^{-6}\cdot 200 / 5\times10^{-4} = 3.75$. Backward Euler is stable at that value.

### The chemical system has no O

The project lists the independent components `C, Ca, Cl, H, Mg, Zz`. Water is built from `H` alone, and every species' O follows from the others.
An extra O row would make the stoichiometry matrix singular. The recipe therefore has no `O`: write the names the project lists, whatever they are.
The inlet holds C and Ca at 1e-9 mol, so that GEMS always has a little of every component.
""")

nb.md(en=r"""
## Run
""")
nb.code(r"""
!python ../../coupling.py case.yaml 2>&1 | grep -v gems3k | tail -n 2
""")

nb.md(en=r"""
## Compare with the paper (t = 21 000 s)

Left: this model in the layout of Fig. 6. Right: the published figure. Minerals are converted from mol/m³ bulk to mol per m³ of water
(÷ φ), as in the paper.
""")
nb.code(r"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
phi = 0.32
p = pd.read_csv('results/profiles.csv')
s = p[p.time_s == p.time_s.max()].sort_values('x_m')

fig, (ax1, axi) = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw={'width_ratios': [1.1, 1]})
ax2 = ax1.twinx()
ax1.plot(s.x_m, s.Cl_c_mol_m3_water, color='tab:green', label='Cl')
ax1.plot(s.x_m, s.Mg_c_mol_m3_water, color='tab:red', label='Mg')
ax1.plot(s.x_m, s.Ca_c_mol_m3_water, color='tab:blue', label='Ca')
ax2.plot(s.x_m, s.Calcite_mol_m3_bulk / phi, color='tab:purple', label='Calcite')
ax2.plot(s.x_m, s['Dolomite-dis_mol_m3_bulk'] / phi, color='tab:orange', label='Dolomite')
ax1.set(xlim=(0, 0.5), ylim=(0, 2.1), xlabel='distance (m)', ylabel='concentration (mol/m³)')
ax2.set(ylim=(0, 0.5), ylabel='mineral (mol/m³ water)')
ax1.legend(loc='upper center'); ax2.legend(loc='center right')
ax1.set_title(f'this model, t = {s.time_s.iloc[0]:.0f} s')
axi.imshow(plt.imread('reference/paper_fig6_bench5.png')); axi.axis('off'); axi.set_title('paper, Fig. 6')
plt.tight_layout(); plt.show()

dol = (s['Dolomite-dis_mol_m3_bulk'] / phi).to_numpy(); band = s.x_m.to_numpy()[dol > 0.01]
print(f'calcite plateau {(s.Calcite_mol_m3_bulk / phi).max():.4f} mol/m3 water')
print(f'dolomite peak   {dol.max():.4f} mol/m3 water, band {band.min():.3f}-{band.max():.3f} m')
""")
nb.md(en=r"""
The positions of the Mg and Cl fronts, the calcite dissolution front and the dolomite band match the published figure.

## How the band moves
""")
nb.code(r"""
fig, axes = plt.subplots(1, 3, figsize=(13, 3.5))
for k, (t, g) in enumerate(p.groupby('time_s')):
    g = g.sort_values('x_m')
    axes[0].plot(g.x_m, g.Calcite_mol_m3_bulk / phi, color=f'C{k}', label=f'{t:.0f} s')
    axes[1].plot(g.x_m, g['Dolomite-dis_mol_m3_bulk'] / phi, color=f'C{k}')
    axes[2].plot(g.x_m, g.pH, color=f'C{k}')
for ax, title in zip(axes, ['Calcite (mol/m³ water)', 'Dolomite (mol/m³ water)', 'pH']):
    ax.set(title=title, xlabel='distance (m)')
axes[0].legend(fontsize=7); plt.tight_layout(); plt.show()
""")
nb.md(en=r"""
Dolomite forms where Mg meets dissolving calcite. Behind the band the inflowing MgCl₂ water is undersaturated with dolomite, which dissolves again,
so the band moves with the calcite front.

## Why 1000 cells? Numerical dispersion

The upwind scheme adds a numerical dispersion of about $q h/2$ to the physical $D_e$. With 1000 cells ($h$ = 0.5 mm) this is
$0.75\times10^{-9}$ m²/s, about 12 % of $D_e$. With 100 cells it would be 1.2 times $D_e$. One changed line shows the effect:
""")
nb.code(r"""
import yaml
case = yaml.safe_load(open('case.yaml'))
case['transport']['geometry']['cells'] = 100
case['output']['folder'] = 'results_100cells'
yaml.safe_dump(case, open('case_100cells.yaml', 'w'), sort_keys=False)
!python ../../coupling.py case_100cells.yaml 2>&1 | grep -v gems3k | tail -n 1

c = pd.read_csv('results_100cells/profiles.csv'); c = c[c.time_s == c.time_s.max()].sort_values('x_m')
fig, ax = plt.subplots(figsize=(6.5, 3.4))
for d, lab, st in ((s, '1000 cells', '-'), (c, '100 cells', '--')):
    ax.plot(d.x_m, d['Dolomite-dis_mol_m3_bulk'] / phi, st, color='tab:orange', label=f'dolomite, {lab}')
    ax.plot(d.x_m, d.Calcite_mol_m3_bulk / phi, st, color='tab:purple', label=f'calcite, {lab}')
ax.set(xlabel='distance (m)', ylabel='mol/m³ water', title='t = 21 000 s'); ax.legend(fontsize=8)
plt.tight_layout(); plt.show()
""")
nb.md(en=r"""
With 100 cells the band sits in the same place; only its edges are spread over a few coarse cells. Equilibrium chemistry keeps the mineral fronts sharp, so here the mesh
matters less than the dispersion estimate suggests. For other problems it can matter a lot: refine until the result stops changing.

## Try it yourself

1. Double `darcy_flux` (and keep `De`). How far does the band get in 21 000 s?
2. Switch on `update_porosity: true`. Dolomite has a smaller molar volume per Ca+Mg than calcite. Does φ go up or down?
3. Set `dt: 100` and compare with `dt: 200`.

You now know every section of `case.yaml`. The [reference pages](../yaml/index.md) list the remaining options, such as `start: warm`
and `on_failure: skip` for difficult chemistry.
""")
nb.save('05_calcite_dolomite')
