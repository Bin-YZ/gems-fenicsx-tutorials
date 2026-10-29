"""Run from FEniCSx_GEMS/:  OMP_NUM_THREADS=1 python ../tools/benchmarks/array_vs_dict.py"""
import time, numpy as np, xgems
lst = 'chemistry_data/b_time0-dat.lst'
recipe = {'Ca': 1.119218076064, 'Si': 0.31000148638994, 'H': 58.52226105076, 'O': 31.00037832923, 'Cl': 1e-15}
g = xgems.ChemicalEngine(lst); names = [g.elementName(k) for k in range(g.numElements())]
b0 = np.array([recipe.get(n, 0.0) for n in names])
g.setColdStart(); g.equilibrate(298.15, 1e5, b0); print('array pH', g.pH(), 'iters', g.numIterations())
d = xgems.ChemicalEngineDicts(lst); d.clear(); d.add_multiple_elements_amt(recipe); d.cold_start(); d.equilibrate()
print('dict  pH', d.pH, 'iters', d.num_iterations, 'T', d.T, 'P', d.P)
aq = g.indexPhase('aq_gen'); ph = [g.indexPhase(p) for p in ('CSHQ', 'Portlandite', 'Silica-amorph')]
N = 20000
t = time.perf_counter()
for k in range(N):
    a = np.asarray(g.elementAmountsInPhase(aq)); v = np.asarray(g.phaseVolumes()); m = np.asarray(g.phaseAmounts())[ph]; p = g.pH()
ta = (time.perf_counter() - t) / N
t = time.perf_counter()
for k in range(N):
    a = d.aq_elements_moles; v = d.phase_volumes; pa = d.phase_amounts; m = [pa[x] for x in ('CSHQ', 'Portlandite', 'Silica-amorph')]; p = d.pH
    a = np.array([a[n] for n in names if n in a])     # back to an array for the transport step
td = (time.perf_counter() - t) / N
print(f'reading results: array {ta*1e6:.1f} us   dict {td*1e6:.1f} us   ratio {td/ta:.1f}')
t = time.perf_counter()
for k in range(N):
    b = b0.copy()
ta = (time.perf_counter() - t) / N
t = time.perf_counter()
for k in range(N):
    d.clear(); d.add_multiple_elements_amt({n: float(x) for n, x in zip(names, b0) if n != 'Zz'})
td = (time.perf_counter() - t) / N
print(f'setting input:   array {ta*1e6:.1f} us   dict {td*1e6:.1f} us')
