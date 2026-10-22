# 来源与致谢

**软件**

- GEMS3K 与 GEM-Selektor：Kulik D.A., Wagner T., Dmytrieva S.V., Kosakowski G., Hingerl F.F., Chudnenko K.V., Berner U. (2013).
  GEM-Selektor geochemical modeling package: revised algorithm and GEMS3K numerical kernel for coupled simulation codes.
  *Computational Geosciences* 17, 1–24. <https://gems.web.psi.ch>
- xGEMS：<https://github.com/gemshub/xgems>
- Baratta I.A. et al. (2023). DOLFINx: the next generation FEniCS problem solving environment. Zenodo. <https://fenicsproject.org>

**示例**

- 教程 3：fenics-reaktoro 的 NaCl 扩散示例（Damiani L.H. 等）。
- 教程 4：水泥溶蚀基准（CaO–SiO₂–H₂O 浆体与 CaCl₂ 水接触），与 HYDRUS 剖面对比。
- 教程 5：MgCl₂ 注入方解石柱，[doi:10.1007/s10596-019-09919-3](https://doi.org/10.1007/s10596-019-09919-3)，4.4 节，图 6。

**验证**

- OGS5GEMDEV：与 GEMS3K 耦合的 OpenGeoSys 5；基准 `C/calcite_gems`、`C/HAYEKIT`、`PETSc/comedy2d`、`PETSc/ConcreteCrack`、`LookUp-Table/Case1` 及其参考结果。
- Kosakowski G., Watanabe N. (2014). OpenGeoSys-Gem: A numerical tool for calculating geochemical and porosity changes in saturated and
  partially saturated media. *Physics and Chemistry of the Earth* 70–71, 138–149.
- Shao H., Dmytrieva S.V., Kolditz O., Kulik D.A., Pfingsten W., Kosakowski G. (2009). Modeling reactive transport in non-ideal
  aqueous–solid solution system. *Applied Geochemistry* 24, 1287–1300.
- Hayek M., Kosakowski G., Churakov S. (2011). Exact analytical solutions for a diffusion problem coupled with precipitation–dissolution
  reaction and feedback of porosity change. *Water Resources Research* 47, W07545.
- Kuzmin D. (2009). Explicit and implicit FEM-FCT algorithms with flux linearization. *Journal of Computational Physics* 228, 2517–2534.

使用基准数据时请引用原始文献。
