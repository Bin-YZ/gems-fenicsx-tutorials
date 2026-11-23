# Verification against OpenGeoSys-GEM

Before the beginner code above existed, the coupling rules were worked out by reproducing five benchmarks of
**OpenGeoSys-GEM** (OGS5GEMDEV, mainly developed by G. Kosakowski at PSI) with FEniCSx and GEMS, and comparing against the original
OGS output. These cases go beyond the 1D code: 2D Darcy flow, kinetics, fracture elements and flux-corrected transport. They use a
separate Python template, `GEMS_FEniCSx_OGS5_Template` in this repository, which follows OGS's own rules step by step.

Read them as evidence that the operator-splitting approach reproduces an established code, and as worked examples for advanced
features.

## What each case simulates

**[V1 · HAYEKIT](01_hayekit.ipynb).** A 2 mm column in 1D. Two dissolved species A and B diffuse in from opposite ends and
precipitate as a solid AB(s) with a kinetic rate law. The precipitate fills the pores, porosity drops, and with it the diffusion
coefficient $D_e = D_0\phi$. An analytical solution exists (Hayek, Kosakowski & Churakov 2011). *Adds:* kinetic limits in GEMS, porosity feedback,
OGS restart files.

**[V2 · Calcite column](02_calcite.ipynb).** The classic Engesgaard–Kipp benchmark: a 0.5 m column with calcite, flushed with MgCl₂
solution at a constant Darcy flux for 21 000 s. Calcite dissolves and dolomite precipitates in a band behind the dissolution front.
The same chemistry as Tutorial 5, but with OGS's CG1 transport and dispersivity. *Adds:* advection–dispersion of element totals, pure
equilibrium fronts, OGS's rules for converting between concentrations and node amounts.

**[V3 · OPC concrete + quartz](03_opc_quartz.ipynb).** A 10 m column of Portland cement concrete with quartz aggregate over
10 000 years. Quartz dissolves very slowly (alkali–silica reaction); its silica reacts with portlandite and C-S-H, pH falls from 12.9
to about 10 and zeolites form. The boundary conditions in the OGS input are never read, so the column is a closed batch system.
*Adds:* one slow kinetic mineral over long times, initial species constraints, two-pass initialisation.

**[V4 · comedy2d](04_comedy2d.ipynb).** A 14 × 14 cm saturated square in 2D: a vertical cement strip between two sand regions, with
NaCl and sodium oxalate solutions flowing in and water leaving on the right. Oxalate reacts with portlandite to calcium oxalate at the
strip. The benchmark restarts from an OGS state and runs 6 steps (68 s). *Adds:* a 2D Darcy flow field, two kinetic phases with
sub-steps, the excess-water source from GEMS volume changes.

**[V5 · ConcreteCrack](05_concretecrack.ipynb).** A vertical 2.5 × 10.5 cm section of concrete with a surface layer and a 0.5 mm
crack reaching 5 cm deep. A nitrate solution sits on top; flow goes mainly through the crack. The benchmark runs 10 steps of 1 s and tests
the initialisation and the crack–matrix coupling. *Adds:* fracture line elements in a 2D mesh, Kozeny–Carman permeability,
porosity-dependent diffusion, FEM-FCT, and the limits of reproduction in an ill-conditioned flow problem.

Each notebook ends with an error table against the OGS reference. The OGS input files and reference results in
`GEMS_FEniCSx_OGS5_Template/cases/*/ogs_input` and `…/reference` are taken unchanged from OGS5GEMDEV.
