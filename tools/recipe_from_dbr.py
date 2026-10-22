"""Print a case.yaml recipe from the state stored in a GEMS project.

    python recipe_from_dbr.py chemistry_data/b_time0-dat.lst 0.5

scales the stored system so that 1 dm3 of bulk holds `phi` dm3 of pore water.
"""
import sys
import numpy as np
import xgems

project, phi = sys.argv[1], float(sys.argv[2])
g = xgems.ChemicalEngine(project)          # loads the DBR state of the project
T, P = g.temperature(), g.pressure()
b = np.asarray(g.elementAmounts())         # mol, in GEMS element order
g.equilibrate(T, P, b)
aq = g.indexPhase(g.aqueousPhaseName())
water = g.phaseVolume(aq) * 1000           # dm3 of solution in the stored system
solids = g.systemVolume() * 1000 - water   # dm3 of everything else (no gas assumed)
f = phi / water                            # scale factor -> phi dm3 water per dm3 bulk
print(f'# stored system: {water:.4f} dm3 solution, {solids:.4f} dm3 other phases, pH {g.pH():.2f}')
print(f'# scaled by {f:.6g}: solids take {solids * f:.3f} of 1 dm3 bulk (phi + solids must be <= 1)')
print('initial:')
for k in range(g.numElements()):
    name = g.elementName(k)
    if name != 'Zz':
        print(f'  {name}: {max(b[k] * f, 1e-15):.12g}')
