# Verification against OpenGeoSys-GEM

## What these cases are, and what they can show

The five cases in this chapter compare a reproduction with the original **OpenGeoSys-GEM** results (OGS5GEMDEV, mainly developed by
G. Kosakowski at PSI). Two things are important before reading them:

- **They use a different code.** The cases run with `GEMS_FEniCSx_OGS5_Template`, a Python template that copies OGS's rules step by step
  (mesh in OGS node order, OGS's concentration ↔ mass conversion, its kinetic limits, FEM-FCT, fracture elements, 2D flow). They do **not**
  use `case.yaml` or the 1D code of the tutorials.
- **Most of them test reproduction, not physical correctness.** The reference is usually another code's output, under that code's settings
  and for a limited time span or set of variables. Agreement shows that the same model and the same rules were implemented; it does not show that the
  model describes reality. Only V1 also has an analytical solution.

What the chapter supports for the tutorial code: both codes share the operator-splitting scheme, the transport of element totals and the GEMS
coupling. Agreement with OGS here is evidence that these shared ingredients behave as in an established code. It is not a full verification of
`FEniCSx_GEMS`, which has its own checks in the tutorials.

## Results at a glance

| case | reference and conditions | compared variables | result | limits |
|---|---|---|---|---|
| [V1 · HAYEKIT](01_hayekit.ipynb) | OGS output at 10 000 s, same mesh and dt; analytical solution | solutes, precipitate, porosity at all nodes | vs OGS ≤ 3·10⁻⁵ (porosity 3·10⁻⁴); vs analytical 24 % (dt = 100 s) down to 0.3–2.7 % | no clean convergence to the analytical solution; ~3 % unexplained |
| [V2 · Calcite column](02_calcite.ipynb) | OGS output at 21 000 s, same mesh | pH, porosity, elements, ions, calcite, dolomite | elements/ions ≤ 1.1 %; minerals 5 % at the front node only | no analytical solution, no mesh study; front-node cause not separated |
| [V3 · OPC + quartz](03_opc_quartz.ipynb) | OGS time series at 4 nodes, 0–919 years | 14 minerals and solution variables | nRMSE ≤ 0.12 %, zeolites ≤ 0.28 % | closed system (transport not tested); 919–10 000 years without reference |
| [V4 · comedy2d](04_comedy2d.ipynb) | OGS output 68 s after a restart at ~7.5 days | elements, pH, head, two kinetic phases, velocities | ≤ 1.4·10⁻⁴ with loose kinetic limits; strict limits 56 % off | only 68 s; 5 nodes fail in the restart run, as in OGS |
| [V5 · ConcreteCrack](05_concretecrack.ipynb) | OGS output at 10 s | 11 elements, porosity, pH, portlandite, head | chemistry ≤ 1.3·10⁻³; head **not** reproduced | only 10 s; head ill-conditioned; FCT variants indistinguishable |

Error definitions: V1, V2, V4, V5 use max\|template − reference\| / max\|reference\| over all nodes; V3 uses the RMS difference over the OGS
output times divided by the range of the OGS series (nRMSE).

## What each case simulates

**V1 · HAYEKIT.** A 2 mm column in 1D. Two dissolved species diffuse in from opposite ends and precipitate as a solid with a kinetic rate law; the
precipitate fills the pores and slows diffusion.

**V2 · Calcite column.** The Engesgaard–Kipp benchmark: a 0.5 m calcite column flushed with MgCl₂ solution at constant Darcy flux. The same chemistry as
Tutorial 5, but with OGS's CG1 transport and dispersivity.

**V3 · OPC concrete + quartz.** A 10 m column of Portland cement concrete with quartz aggregate. Quartz dissolves very slowly (alkali–silica reaction),
pH falls from 12.9 to about 10 and zeolites form. OGS never reads the boundary conditions, so the column is a closed batch system.

**V4 · comedy2d.** A 14 × 14 cm saturated square in 2D: a cement strip between two sand regions, with NaCl and oxalate solutions flowing in. Oxalate
reacts with portlandite to calcium oxalate at the strip.

**V5 · ConcreteCrack.** A 2.5 × 10.5 cm concrete section with a surface layer and a 0.5 mm crack; a nitrate solution on top, flow mainly through the crack.

## How to run a case

Each case has its own folder with the OGS input files, the GEMS files and the reference results:

```bash
cd GEMS_FEniCSx_OGS5_Template/cases/2_hayekit      # 1_calcite, 2_hayekit, 3_opc_quartz, 4_comedy2d, 5_concretecrack
python run_case.py                                   # Windows: Run.cmd
```

The script prints the same error tables as the notebooks. The notebooks on this site are stored with their outputs; the site does not re-run them.
The OGS input files and reference results in `cases/*/ogs_input` and `cases/*/reference` are taken unchanged from OGS5GEMDEV.
