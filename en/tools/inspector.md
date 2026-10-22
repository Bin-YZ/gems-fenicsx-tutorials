# GEMS Chemistry Inspector

`gems_inspector.html` makes an exported GEMS3K system readable before you write a case. It runs in your browser and nothing is uploaded.

<p><a href="../_static/tools/gems_inspector.html" target="_blank" rel="noopener">Open the Inspector in its own tab ↗</a></p>

<iframe src="../_static/tools/gems_inspector.html" title="GEMS Chemistry Inspector" style="width:100%;height:900px;border:1px solid #d9dfdb;border-radius:6px"></iframe>

## What it shows

Click **Open folder…** or **Open files…**, or drag the files onto the page. Include the `.lst` and the DCH/IPM files it lists. JSON (`-j`)
and text (`-t`) exports work; binary (`-b`) does not.

| tab | content | use it for |
|---|---|---|
| Elements | elements and charge | the names allowed in `initial` / `inlet` |
| Phases | phases and their species | `aqueous_phase`, `solid_phases` |
| Species & thermo | searchable properties: composition, charge, molar mass, standard data | names for `gibbs` |
| Stoichiometry | the formula matrix | checking recipes |
| Reactions | balance check, ΔrG°, ΔrH°, ΔrS°, ΔrCp°, ΔrV°, log K | e.g. `Calcite = Ca+2 + CO3-2` |

In **Reactions**, use exact, case-sensitive species names with spaces around `+`, and put coefficients before names (`2 H2O@`).
`log10 K = −ΔrG° / (R T ln 10)` uses the stored DCH data at the selected temperature–pressure point, without interpolation and without
the `chemistry.gibbs` overrides of a case.

The inspector is read-only. It does not load DBR state files and does not run GEMS.
