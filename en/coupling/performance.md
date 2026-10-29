# Speeding up a run

## Where the time goes

The code runs as **one process with one thread**. `transport.py` stops if it is started with more than one MPI process, and
nothing in the code starts threads or worker processes. Each time step therefore runs in order:

1. transport: one direct PETSc solve per element;
2. chemistry: a Python loop that calls GEMS once per cell;
3. feedback, mass balance, output.

In 1D almost all of the time is chemistry. The cement case of [Tutorial 4](../tutorials/04_cement_leaching.ipynb) makes
40 cells × 10 000 steps = 400 000 GEMS calls in 4.8 minutes, about 0.7 ms per call. The transport solves of a 40-cell mesh are
negligible next to that.

So the place to gain time is the chemistry step. It parallelises well, because **each cell is equilibrated on its own**: the
result for one cell does not depend on any other cell in the same step.

## Processes, not threads

Measured on the cement recipe, 4000 equilibria on 2 CPU cores, one GEMS engine per worker:

| run | time | speed-up | result |
|---|---|---|---|
| serial (one engine) | 2.4 s | 1.0 | reference |
| 2 processes (`multiprocessing.Pool`) | 1.1 s | **2.1** | identical (max. difference 0) |
| 2 threads (`ThreadPoolExecutor`) | 2.0 s | 0.9 | identical, but no faster |

**Threads do not help.** The `xgems` calls hold Python's global interpreter lock (GIL), so two threads take turns instead of
running at the same time. A single GEMS engine must not be shared between threads anyway.

**Processes scale with the number of cores.** Each process has its own interpreter and its own GEMS engine. The work per cell is
about 0.5 ms, much more than the cost of sending a row of element amounts to a worker. The speed-up is therefore close to the number of cores.

## How to parallelise the chemistry step

The current code has no parallel option. This is the pattern to add one. Every worker loads the GEMS project once, and the cells of a step
are split into blocks:

```python
from multiprocessing import Pool
import numpy as np

_chem = None                                  # one Chemistry (one GEMS engine) per worker process

def _init(config):
    global _chem
    from chemistry import Chemistry
    _chem = Chemistry(config)

def _solve_block(rows):                       # rows: (cell index, total element amounts)
    return [(i, _chem.equilibrate(total)) for i, total in rows]

pool = Pool(processes=4, initializer=_init, initargs=(config['chemistry'],))
blocks = np.array_split(np.arange(n_cells), 4)            # the same split in every step
for block in pool.map(_solve_block, [[(i, state['total'][i]) for i in b] for b in blocks]):
    for i, result in block:
        state['aqueous'][i] = result['aqueous']           # ... and the other fields, as in coupling.py
```

Points to watch:

- **Keep the split fixed.** With `chemistry.start: warm` each cell starts from its own previous equilibrium, which lives in the engine of
  the worker that solved it. The same cell must therefore go to the same worker in every step. With `cold` (the default) the split
  does not matter, and results are identical to the serial run.
- **Limit library threads.** Set `OMP_NUM_THREADS=1` (and `OPENBLAS_NUM_THREADS=1`) before starting, so that numpy or PETSc do not
  start extra threads in every worker and compete for the same cores.
- **Use at most one worker per physical core.** More workers than cores makes the run slower.
- **Mind start-up cost.** Create the pool once, before the time loop, not in every step. Loading the GEMS project takes a fraction of a second.
- **Error handling stays the same.** A worker returns the same result dictionary or raises the same `RuntimeError`, and `coupling.py`
  handles it as before (`on_failure: stop` or `skip`).

For large 2D or 3D meshes the transport also becomes expensive. Then the usual route is MPI (`mpirun -n 4`), where every process owns part of the
mesh and the GEMS calls of its own nodes. This is how OpenGeoSys-GEM runs its PETSc benchmarks. It needs a distributed mesh and a parallel
linear solver, so it is a larger change than the process pool above. The 1D code does not support it.

## Arrays, not dictionaries

Numerical solvers keep their data in arrays. GEMS3K stores element amounts, species amounts and phase volumes as C++ arrays in a fixed
order, and FEniCSx/PETSc vectors are arrays as well. Every value that passes between them through a **dictionary** keyed by name has to be
looked up by name, boxed as a Python object, and copied back into an array. That adds work on every call, in a loop that runs once per cell and step.

`xgems` offers both interfaces:

| | array interface `xgems.ChemicalEngine` | dictionary interface `xgems.ChemicalEngineDicts` |
|---|---|---|
| input | `equilibrate(T, P, b)` with `b` a numpy array in element order | `add_multiple_elements_amt({'Ca': …, 'Si': …})` |
| output | `elementAmountsInPhase(i)`, `phaseVolumes()`, `phaseAmounts()` → arrays | `aq_elements_moles`, `phase_volumes`, `phase_amounts` → dicts |

Measured for the data exchange around one equilibrium of the cement recipe (setting the composition, reading the aqueous elements, phase
volumes, mineral amounts and pH):

| | array | dictionary |
|---|---|---|
| set the composition | 0.5 µs | 2.8 µs |
| read the results | 4.5 µs | 6.3 µs |
| total per call | **5 µs** | **9 µs** |

For this small system the equilibrium itself takes about 500 µs, so the dictionary overhead is about 1 % of the run time. It grows when GEMS is
fast (small systems, warm starts) or when many values are exchanged, for example all species amounts of a large database. In both cases the
array path stays cheaper.

`FEniCSx_GEMS` follows this rule:

- Recipes are dictionaries only in `case.yaml`. `Chemistry.amounts()` turns each recipe into an array in GEMS element order **once**, at start-up.
- The state is kept in arrays with one row per cell and one column per element (`state['total']`, `state['aqueous']`). Transport works on
  whole columns of these arrays.
- `Chemistry.equilibrate()` passes an array to `g.equilibrate(T, P, b)` and reads arrays back.

Rules for your own extensions:

- Translate names to indices **before** the time loop (`g.indexPhase(name)`, `names.index(element)`) and use the indices inside it. In
  `chemistry.py` the phase indices are still looked up by name in every call. Caching them in `__init__` is an easy saving.
- Do not build dictionaries, pandas tables or YAML inside the loop over cells. Collect results in preallocated numpy arrays and write output in
  `output.py` every `output.every` steps.
- Use the dictionary interface for exploration in a notebook, where readability matters more than microseconds.

The measurements can be repeated with the scripts in `tools/benchmarks/` (run from `FEniCSx_GEMS/`).
