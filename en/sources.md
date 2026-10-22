# Sources and credits

**Software**

- GEMS3K and GEM-Selektor: Kulik D.A., Wagner T., Dmytrieva S.V., Kosakowski G., Hingerl F.F., Chudnenko K.V., Berner U. (2013).
  GEM-Selektor geochemical modeling package: revised algorithm and GEMS3K numerical kernel for coupled simulation codes.
  *Computational Geosciences* 17, 1–24. <https://gems.web.psi.ch>
- xGEMS: <https://github.com/gemshub/xgems>
- Baratta I.A. et al. (2023). DOLFINx: the next generation FEniCS problem solving environment. Zenodo. <https://fenicsproject.org>

**Examples**

- Tutorial 3: NaCl diffusion demo of fenics-reaktoro (Damiani L.H. et al.).
- Tutorial 4: cement leaching benchmark (CaO–SiO₂–H₂O paste in contact with CaCl₂ water), compared with a HYDRUS profile.
- Tutorial 5: MgCl₂ injection into calcite, [doi:10.1007/s10596-019-09919-3](https://doi.org/10.1007/s10596-019-09919-3), section 4.4, Fig. 6.

**Verification**

- OGS5GEMDEV: OpenGeoSys 5 coupled with GEMS3K; benchmarks `C/calcite_gems`, `C/HAYEKIT`, `PETSc/comedy2d`,
  `PETSc/ConcreteCrack`, `LookUp-Table/Case1` and their reference results.
- Kosakowski G., Watanabe N. (2014). OpenGeoSys-Gem: A numerical tool for calculating geochemical and porosity changes in saturated and
  partially saturated media. *Physics and Chemistry of the Earth* 70–71, 138–149.
- Shao H., Dmytrieva S.V., Kolditz O., Kulik D.A., Pfingsten W., Kosakowski G. (2009). Modeling reactive transport in non-ideal
  aqueous–solid solution system. *Applied Geochemistry* 24, 1287–1300.
- Hayek M., Kosakowski G., Churakov S. (2011). Exact analytical solutions for a diffusion problem coupled with precipitation–dissolution
  reaction and feedback of porosity change. *Water Resources Research* 47, W07545.
- Kuzmin D. (2009). Explicit and implicit FEM-FCT algorithms with flux linearization. *Journal of Computational Physics* 228, 2517–2534.

Please cite the original work when you use the benchmark data.
