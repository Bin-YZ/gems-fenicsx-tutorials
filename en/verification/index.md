# Verification against OpenGeoSys-GEM

Before the beginner code above existed, the coupling rules were worked out by reproducing five benchmarks of
**OpenGeoSys-GEM** (OGS5GEMDEV, mainly developed by G. Kosakowski at PSI) with FEniCSx and GEMS, and comparing against the original
OGS output. These cases go beyond the 1D code: 2D Darcy flow, kinetics, fracture elements and flux-corrected transport. They use a
separate Python template, `GEMS_FEniCSx_OGS5_Template` in this repository, which follows OGS's own rules step by step.

Read them as evidence that the operator-splitting approach reproduces an established code, and as worked examples for advanced
features.

| # | benchmark | what it adds |
|---|---|---|
| 1 | [HAYEKIT](01_hayekit.ipynb) | kinetic limits, porosity feedback, analytical solution |
| 2 | [Calcite column](02_calcite.ipynb) | advection, equilibrium fronts, OGS concentration ↔ mass rules |
| 3 | [OPC concrete + quartz](03_opc_quartz.ipynb) | 10 000 years of slow kinetics, closed system |
| 4 | [comedy2d](04_comedy2d.ipynb) | 2D Darcy flow, two kinetic phases, sub-steps |
| 5 | [ConcreteCrack](05_concretecrack.ipynb) | fracture elements, FEM-FCT, Kozeny–Carman |

Each notebook ends with an error table against the OGS reference. The OGS input files and reference results in
`GEMS_FEniCSx_OGS5_Template/cases/*/ogs_input` and `…/reference` are taken unchanged from OGS5GEMDEV.
