# Quellen und Danksagung

**Software**

- GEMS3K und GEM-Selektor: Kulik D.A., Wagner T., Dmytrieva S.V., Kosakowski G., Hingerl F.F., Chudnenko K.V., Berner U. (2013).
  GEM-Selektor geochemical modeling package: revised algorithm and GEMS3K numerical kernel for coupled simulation codes.
  *Computational Geosciences* 17, 1–24. <https://gems.web.psi.ch>
- xGEMS: <https://github.com/gemshub/xgems>
- Baratta I.A. et al. (2023). DOLFINx: the next generation FEniCS problem solving environment. Zenodo. <https://fenicsproject.org>

**Beispiele**

- Tutorial 3: NaCl-Diffusionsdemo von fenics-reaktoro (Damiani L.H. et al.).
- Tutorial 4: Benchmark Zementauslaugung (CaO–SiO₂–H₂O-Paste in Kontakt mit CaCl₂-Wasser), verglichen mit einem HYDRUS-Profil.
- Tutorial 5: MgCl₂-Injektion in Calcit, [doi:10.1007/s10596-019-09919-3](https://doi.org/10.1007/s10596-019-09919-3), Abschnitt 4.4, Abb. 6.

**Verifikation**

- OGS5GEMDEV: OpenGeoSys 5 gekoppelt mit GEMS3K; Benchmarks `C/calcite_gems`, `C/HAYEKIT`, `PETSc/comedy2d`, `PETSc/ConcreteCrack`,
  `LookUp-Table/Case1` und ihre Referenzergebnisse.
- Kosakowski G., Watanabe N. (2014). OpenGeoSys-Gem: A numerical tool for calculating geochemical and porosity changes in saturated and
  partially saturated media. *Physics and Chemistry of the Earth* 70–71, 138–149.
- Shao H., Dmytrieva S.V., Kolditz O., Kulik D.A., Pfingsten W., Kosakowski G. (2009). Modeling reactive transport in non-ideal
  aqueous–solid solution system. *Applied Geochemistry* 24, 1287–1300.
- Hayek M., Kosakowski G., Churakov S. (2011). Exact analytical solutions for a diffusion problem coupled with precipitation–dissolution
  reaction and feedback of porosity change. *Water Resources Research* 47, W07545.
- Kuzmin D. (2009). Explicit and implicit FEM-FCT algorithms with flux linearization. *Journal of Computational Physics* 228, 2517–2534.

Bitte die Originalarbeiten zitieren, wenn Sie die Benchmark-Daten verwenden.
