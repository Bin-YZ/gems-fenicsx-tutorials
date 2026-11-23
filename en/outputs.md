# Results and troubleshooting

## Files in `output.folder`

| file | written | content |
|---|---|---|
| `summary.txt` | start (RUNNING), end | **COMPLETED**, **COMPLETED WITH SKIPPED CELLS** or **FAILED**, mode, mesh, GEMS start mode, number of skipped cell-steps, final time, largest balance / chemistry / water errors, φ and De ranges |
| `profiles.csv` | every `output.every` steps and at the end | one row per cell and time (see below) |
| `mass_balance.csv` | every step | per element: inventory, cumulative boundary input, balance error, chemistry error, water mismatch |
| `profiles.png` | end | quick-look plot of the profiles |
| `fields.xdmf` + `fields.h5` | with the profiles (not in chemistry mode) | dissolved concentrations, φ, De and pH for ParaView (element totals and mineral amounts are only in `profiles.csv`) |
| `simulation.log` | during the run | one progress line per saved step, warnings |
| `case_used.json` | start | the settings actually used, with absolute paths |
| `failure.txt` | only on failure | the Python traceback and the message |
| `xGEMS.log`, `ipmlog.txt` | by GEMS | GEMS's own messages |

### Columns of `profiles.csv`

```text
time_s, x_m, phi, De_m2_s, pH,
<E>_c_mol_m3_water, <E>_total_mol_m3_bulk     for every element E (or tracer)
<P>_mol_m3_bulk                               for every phase P in solid_phases
```

Reading it with pandas:

```python
import pandas as pd
p = pd.read_csv('results/profiles.csv')
last = p[p.time_s == p.time_s.max()]
last.plot(x='x_m', y=['Portlandite_mol_m3_bulk', 'CSHQ_mol_m3_bulk'])
```

Inventories in `mass_balance.csv` are in mol per m² of cross-section (amount × cell length, summed).

## When something goes wrong

Every failure stops the run. Where the message appears depends on when it happens:

- **Input checks** (`read_case`: the four sections, paths, numbers, mode and feedback switches) run before the output folder is created. These errors
  appear only in the terminal; no `failure.txt` is written.
- **Everything after start-up** (loading GEMS and the names in it, the initial equilibrium, every time step) writes `failure.txt` and marks `summary.txt`
  **FAILED**.

The message names the cause:

| message | cause | what to do |
|---|---|---|
| `Use exactly four sections` | missing, misspelt or extra top-level key | check `chemistry`, `transport`, `coupling`, `output` |
| `GEMS project file does not exist` | `chemistry.project` path | the path is relative to `case.yaml` |
| `Unknown GEMS element: …` / `Unknown GEMS phase: …` | name not in the project | copy names from the [Inspector](tools/inspector.md); names are case-sensitive |
| `Initial solids plus porosity exceed the bulk volume` | recipe has more solid than 1 − φ | lower φ or rescale the recipe ([from GEMS](yaml/from_gems.md)) |
| `Chemistry failed: step=…, cell=…, x=…` | GEMS did not converge for that cell | see below |
| `Porosity outside (0,1]; no clipping` | so much precipitation that the pores close (or the reverse) | smaller `dt`; check `solid_phases`; the model reaches its physical limit |
| `Invalid concentration … no clipping` | negative value from transport | finer mesh / smaller `dt`; with advection, check the boundary types |
| `Mass balance failed at step …` | inventory ≠ initial + boundary input | should not happen; report it with `case_used.json` |
| `With flow, the left (inflow) boundary must be dirichlet` | advection set-up | left `dirichlet`, right `outflow` or `dirichlet` |

### GEMS does not converge

In this order:

1. Run the failing composition alone. `failure.txt` prints `total_mol_dm3`; put it into a recipe and use `mode: chemistry`.
2. Make sure every element has at least a trace amount (`1.0e-15`) in `initial` **and** `inlet`. An element that is exactly 0 in one
   and positive in the other is a common cause.
3. Try `chemistry.start: warm`: each cell starts from its own previous equilibrium.
4. Reduce `dt`, so that the composition changes less per step.
5. As a last resort, use `chemistry.on_failure: skip`. Failing cells stay unreacted for that step and every skip is logged in `simulation.log`.
   The first line of `summary.txt` then reads **COMPLETED WITH SKIPPED CELLS** and gives the number of skipped cell-steps.

### Small differences between runs

Two runs with nearly identical inputs can give slightly different results. In the tested examples, inputs that differed only in the last digit changed
concentrations by up to about 1e-5 relative. This is not a general bound, and a difference of that size is not automatically harmless. Before you attribute a
difference to round-off, check:

- **convergence**: no GEMS failures or skipped cells in `simulation.log`, and the same phases present in both runs;
- **element-balance residuals**: the *chemistry error* column of `mass_balance.csv` and the maximum in `summary.txt`;
- **sensitivity**: whether the difference shrinks when `dt` or the mesh is refined, or grows near fronts where phases appear or disappear.

Report pH differences as absolute values (pH units), not as relative errors.
