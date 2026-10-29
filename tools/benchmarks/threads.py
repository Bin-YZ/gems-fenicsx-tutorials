"""Run from FEniCSx_GEMS/:  OMP_NUM_THREADS=1 python ../tools/benchmarks/threads.py"""
import time, numpy as np, xgems
from concurrent.futures import ThreadPoolExecutor
LST = 'chemistry_data/b_time0-dat.lst'
g0 = xgems.ChemicalEngine(LST); names = [g0.elementName(k) for k in range(g0.numElements())]
r = {'Ca': 1.119218076064, 'Si': 0.31000148638994, 'H': 58.52226105076, 'O': 31.00037832923, 'Cl': 1e-15}
b0 = np.array([r.get(n, 0.0) for n in names]); n = 4000
B = np.tile(b0, (n, 1)); B[:, names.index('Ca')] *= np.linspace(0.2, 1, n)
def solve(args):
    g, block = args
    out = []
    for b in block:
        g.setColdStart(); g.equilibrate(298.15, 1e5, b); out.append(np.asarray(g.elementAmountsInPhase(0)))
    return np.array(out)
t = time.perf_counter(); s = solve((g0, B)); t1 = time.perf_counter() - t
engines = [xgems.ChemicalEngine(LST) for _ in range(2)]
t = time.perf_counter()
with ThreadPoolExecutor(2) as ex: res = np.vstack(list(ex.map(solve, zip(engines, np.array_split(B, 2)))))
t2 = time.perf_counter() - t
print(f'serial {t1:.2f} s, 2 threads {t2:.2f} s, speed-up {t1/t2:.2f}, max diff {np.abs(res-s).max():.1e}')
