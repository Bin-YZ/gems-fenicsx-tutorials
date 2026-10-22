# GEMS + FEniCSx: reactive transport tutorials

These pages teach reactive transport modelling with **GEMS** (Gibbs energy minimisation for the
chemistry) and **FEniCSx** (finite elements for flow and transport), using benchmarks of
**OpenGeoSys-GEM** (OGS5GEMDEV) as worked examples. Every tutorial rebuilds an OGS-GEM benchmark with a
small Python template and compares the result with the original OGS output.

The goal is not only to run the cases, but to understand *every* rule in the coupling — including the
ones that are only written in the OGS source code — well enough to build your own models.

## Learning path

| # | tutorial | new ideas | runtime |
|---|---|---|---|
| 1 | [HAYEKIT](tutorials/01_hayekit) | SNIA, kinetic limits, porosity feedback, analytical solution | 3 min |
| 2 | [Calcite column](tutorials/02_calcite) | advection, equilibrium fronts, OGS concentration ↔ mass rules | 15 s |
| 3 | [OPC concrete + quartz](tutorials/03_opc_quartz) | 10 000 years of slow kinetics, constraints, closed system | 18 min |
| 4 | [comedy2d](tutorials/04_comedy2d) | 2D Darcy flow, two kinetic phases, sub-steps, excess-water source | 25 s |
| 5 | [ConcreteCrack](tutorials/05_concretecrack) | fracture elements, FEM-FCT, Kozeny–Carman, where reproduction stops | 4 min |

Read the [concept pages](concepts/01_snia) alongside; each tutorial links to the concepts it uses.

## What you need

- the template folder `GEMS_FEniCSx_OGS5_Template` (modules + all case data),
- a Python environment with dolfinx and xgems — see [Setup](setup).

## Credits

The benchmarks, their input files and reference results come from **OGS5GEMDEV** (OpenGeoSys 5 coupled
with GEMS3K, developed mainly by Georg Kosakowski at PSI). GEMS3K and xGEMS are developed by the GEMS
team (Kulik et al.), FEniCSx by the FEniCS project. See [Sources](sources).
