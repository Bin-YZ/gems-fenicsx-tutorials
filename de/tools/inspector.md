# GEMS Chemistry Inspector

`gems_inspector.html` macht ein exportiertes GEMS3K-System lesbar, bevor Sie einen Fall schreiben. Es läuft im Browser; nichts wird hochgeladen.

<p><a href="../_static/tools/gems_inspector.html" target="_blank" rel="noopener">Inspector in eigenem Tab öffnen ↗</a></p>

<iframe src="../_static/tools/gems_inspector.html" title="GEMS Chemistry Inspector" style="width:100%;height:900px;border:1px solid #d9dfdb;border-radius:6px"></iframe>

## Was er zeigt

Auf **Open folder…** oder **Open files…** klicken oder die Dateien auf die Seite ziehen. Die `.lst` und die darin genannten DCH/IPM-Dateien
mitnehmen. JSON- (`-j`) und Text-Exporte (`-t`) funktionieren, binäre (`-b`) nicht.

| Reiter | Inhalt | wofür |
|---|---|---|
| Elements | Elemente und Ladung | erlaubte Namen in `initial` / `inlet` |
| Phases | Phasen und ihre Spezies | `aqueous_phase`, `solid_phases` |
| Species & thermo | durchsuchbare Eigenschaften: Zusammensetzung, Ladung, Molmasse, Standarddaten | Namen für `gibbs` |
| Stoichiometry | die Formelmatrix | Rezepte prüfen |
| Reactions | Bilanzprüfung, ΔrG°, ΔrH°, ΔrS°, ΔrCp°, ΔrV°, log K | z. B. `Calcite = Ca+2 + CO3-2` |

In **Reactions** exakte Speziesnamen mit Groß-/Kleinschreibung verwenden, Leerzeichen um `+` setzen und Koeffizienten vor die Namen schreiben (`2 H2O@`).
`log10 K = −ΔrG° / (R T ln 10)` verwendet die gespeicherten DCH-Daten am gewählten Temperatur-Druck-Punkt, ohne Interpolation und ohne die
`chemistry.gibbs`-Überschreibungen eines Falls.

Der Inspector liest nur: Er lädt keine DBR-Zustandsdateien und startet GEMS nicht.
