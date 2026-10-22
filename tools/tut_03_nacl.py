from nb import NB

nb = NB()
nb.md(en=r"""
# 3. NaCl diffusion: first coupled run

**Goal.** Run `mode: coupled` for the first time, on the simplest chemistry there is: a solution without any solids.
Two NaCl solutions, 1 M and 0.5 M, meet in the middle of a 20 mm column and diffuse into each other.

New in `case.yaml`:

- **`transport.zones`**: two zones, `high` and `low`. Each gets its own recipe in `chemistry.initial`.
- **`chemistry.inlet: {left: high, right: low}`**: each end is held at the equilibrated pore water of its own zone.
- **`solid_phases: []`**: solution only. GEMS only speciates the water, and porosity stays constant.

| | |
|---|---|
| Mode | `coupled` |
| Case folder | `FEniCSx_GEMS/example/demo_NaCl_diffusion` (this notebook runs there) |
| Domain | 20 mm, 200 cells, 100 s with `dt` = 1 s |
| Runtime | about 5 s |
""")

nb.md(en=r"""
## The input file
""")
nb.code(r"""
print(open('case.yaml').read())
""")
nb.md(en=r"""
Compared with [Tutorial 2](02_single_equilibrium.ipynb), three things change:

```yaml
chemistry:
  initial:                 # one recipe per zone instead of one recipe
    high: {Cl: 0.981, H: 108.9, Na: 0.981, O: 54.47}
    low:  {Cl: 0.495, H: 109.8, Na: 0.495, O: 54.90}
  inlet: {left: high, right: low}
transport:
  zones:
    - {name: high, from: 0.0,  to: 0.01}
    - {name: low,  from: 0.01, to: 0.02}
coupling:
  mode: coupled
```

The zones give no `phi` or `De` of their own, so both use `material`. Here that is free solution with φ = 1.

### Why one diffusion coefficient is enough here

Na⁺ and Cl⁻ diffuse at different rates on their own ($D_\text{Na} = 1.334\times10^{-9}$, $D_\text{Cl} = 2.032\times10^{-9}$ m²/s).
In solution, electroneutrality makes the two ions move together. For a 1:1 salt, Nernst–Planck then reduces to Fick's law with the salt
coefficient

$$
D_\text{salt} = \frac{2 D_\text{Na} D_\text{Cl}}{D_\text{Na} + D_\text{Cl}} = 1.611\times10^{-9}\ \text{m}^2/\text{s},
$$

which is the `De` in the file. The code transports every element with the same coefficient, so it is exact for this case.
It would not be exact for mixtures of salts with different ions.
""")

nb.md(en=r"""
## Run
""")
nb.code(r"""
!python ../../coupling.py case.yaml 2>&1 | grep -v gems3k | tail -n 4
""")

nb.md(en=r"""
## Compare with the analytical solution

Two half-spaces at $c_H$ and $c_L$ give $c(x,t) = \tfrac{c_H+c_L}{2} - \tfrac{c_H-c_L}{2}\,\mathrm{erf}\!\big((x-x_0)/2\sqrt{Dt}\big)$.
In 100 s the front spreads less than 1 mm, so the fixed ends 10 mm away do not matter.
""")
nb.code(r"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, yaml
from scipy.special import erf

case = yaml.safe_load(open('case.yaml'))
p = pd.read_csv('results/profiles.csv')
D, x0 = case['transport']['material']['De'], 0.01
p0 = p[p.time_s == 0].sort_values('x_m')

fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
worst = 0.0
for ax, e in zip(axes, ('Na', 'Cl')):
    col = f'{e}_c_mol_m3_water'
    cH, cL = p0[col].iloc[0], p0[col].iloc[-1]
    for k, (t, g) in enumerate(p[p.time_s > 0].groupby('time_s')):
        x = g.sort_values('x_m').x_m.to_numpy()
        exact = (cH + cL) / 2 - (cH - cL) / 2 * erf((x - x0) / (2 * np.sqrt(D * t)))
        ax.plot((x - x0) * 1e3, g.sort_values('x_m')[col], '.', ms=3, color=f'C{k}', label=f'{t:g} s')
        ax.plot((x - x0) * 1e3, exact, '-', lw=1, color=f'C{k}')
        worst = max(worst, np.max(np.abs(g.sort_values('x_m')[col].to_numpy() - exact)) / cH)
    ax.set(xlim=(-2, 2), xlabel='x − 10 mm (mm)', ylabel=f'{e} (mol/m³ water)', title=f'{e}: dots model, lines analytical')
axes[0].legend(fontsize=8); plt.tight_layout(); plt.show()
print(f'largest |model − analytical| / c_high: {100 * worst:.2f} %')
""")
nb.md(en=r"""
The model follows the erf solution closely. The small differences come from the 0.1 mm cells and the first-order time step.
The chemistry step does almost nothing here: it only speciates the solution again. That is the point of this case. The coupled loop
runs end to end on a problem whose answer is known.

## What GEMS adds: pH and the water

Every element is transported, including the H and O of the water. GEMS recomputes the solution in every cell, so pH and the
amount of water follow from the transported totals.
""")
nb.code(r"""
last = p[p.time_s == p.time_s.max()].sort_values('x_m')
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.2))
a1.plot((last.x_m - x0) * 1e3, last.pH); a1.set(xlim=(-3, 3), xlabel='x − 10 mm (mm)', ylabel='pH', title='pH at 100 s')
a2.plot((last.x_m - x0) * 1e3, last.H_c_mol_m3_water / 2 / 1000 * 0.018015, color='C2')
a2.set(xlim=(-3, 3), xlabel='x − 10 mm (mm)', ylabel='kg H₂O per dm³ (from H)', title='water content of the solution')
plt.tight_layout(); plt.show()
""")
nb.md(en=r"""
The 1 M solution holds slightly less water per litre than the 0.5 M solution, because the salt takes up volume. The transport of H and O carries this
difference along with the salt.

## Try it yourself

1. Give the `low` zone a different porosity, e.g. `{name: low, from: 0.01, to: 0.02, phi: 0.3, De: 3.0e-10}`, and look at the jump in the profile.
2. Use the same solution on both sides: `inlet: high`. What happens at the right end?
3. Close the right end (`type: no_flux`) and run to `end: 100000`. Where does the profile end up?

**Next:** [Tutorial 4](04_cement_leaching.ipynb) adds minerals, which dissolve as the solution changes.
""")
nb.save('03_nacl_diffusion')
