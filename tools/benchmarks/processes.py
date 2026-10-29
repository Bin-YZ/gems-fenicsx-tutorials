"""Run from FEniCSx_GEMS/:  OMP_NUM_THREADS=1 python ../tools/benchmarks/processes.py"""
import os, time, numpy as np
from multiprocessing import Pool
LST = 'chemistry_data/b_time0-dat.lst'
_g = None
def init():
    global _g
    import xgems
    _g = xgems.ChemicalEngine(LST)
def solve(block):
    out = []
    for b in block:
        _g.setColdStart(); _g.equilibrate(298.15, 1e5, b)
        out.append(np.asarray(_g.elementAmountsInPhase(0)))
    return np.array(out)
if __name__ == '__main__':
    import xgems
    g = xgems.ChemicalEngine(LST); names = [g.elementName(k) for k in range(g.numElements())]
    r = {'Ca': 1.119218076064, 'Si': 0.31000148638994, 'H': 58.52226105076, 'O': 31.00037832923, 'Cl': 1e-15}
    b0 = np.array([r.get(n, 0.0) for n in names]); n = 4000
    B = np.tile(b0, (n, 1)); B[:, names.index('Ca')] *= np.linspace(0.2, 1, n)
    init(); t = time.perf_counter(); s = solve(B); t1 = time.perf_counter() - t
    with Pool(2, initializer=init) as p:
        t = time.perf_counter(); res = np.vstack(p.map(solve, np.array_split(B, 2))); t2 = time.perf_counter() - t
    print(f'serial {t1:.2f} s, 2 processes {t2:.2f} s, speed-up {t1/t2:.2f}, max diff {np.abs(res-s).max():.1e}')
