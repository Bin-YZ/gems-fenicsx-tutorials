# Überblick über die Tutorials

Fünf Fälle, jeder etwas mehr als der vorige. Jedes Tutorial ist ein ausgeführtes Notebook: Es zeigt die vollständige `case.yaml`, startet
`coupling.py` damit und stellt die Ergebnisse dar, meist im Vergleich mit einer analytischen Lösung oder einem veröffentlichten Benchmark.

| # | was simuliert wird | Modus | was man lernt | Laufzeit |
|---|---|---|---|---|
| [1](01_tracer_diffusion.ipynb) | Ein nicht reaktiver Tracer diffundiert von einem Rand mit c = 1 in eine 10 mm lange wassergesättigte Säule (φ = 0,4); das andere Ende wird auf 0 gehalten, später geschlossen. | `diffusion` | die vier Abschnitte von `case.yaml`, den Lauf, die Ergebnisdateien, die Massenbilanz; Vergleich mit der analytischen Reihenlösung | 2 s |
| [2](02_single_equilibrium.ipynb) | Ein GEMS-Gleichgewicht einer hydratisierten Zementpaste (Ca, Si, Wasser, Spuren Cl): welche Minerale und welches Porenwasser sie enthält. Ein Scan des Ca/Si von 3,7 bis 0,5 zeigt, wie Portlandit verschwindet, C-S-H Ca verliert und amorphes SiO₂ erscheint. | `chemistry` | Element- und Phasennamen eines GEMS-Projekts, Einheiten der Rezepte (mol pro dm³ Gesamtmaterial), `gibbs`-Anpassungen | 15 s |
| [3](03_nacl_diffusion.ipynb) | Eine 1-M- und eine 0,5-M-NaCl-Lösung berühren sich in der Mitte einer 20-mm-Säule; das Salz diffundiert 100 s lang von der starken zur schwachen Seite. Keine Feststoffe. | `coupled` | der erste gekoppelte Lauf, zwei Zonen mit eigenen Rezepten, seitenweise Randlösungen; Vergleich mit der erf-Lösung | 5 s |
| [4](04_cement_leaching.ipynb) | Eine 4 mm dicke hydratisierte Zementpaste steht 1000 Jahre in Kontakt mit 14,6-mM-CaCl₂-Wasser. Ca wird ausgelaugt, Portlandit löst sich von der Oberfläche nach innen, und C-S-H entkalkt hinter der Front. | `coupled` | Minerale und `solid_phases`, lange Zeiten, Rückkopplung von Porosität und Diffusivität; Vergleich mit einem HYDRUS-Benchmarkprofil | 2 × 3–5 min |
| [5](05_calcite_dolomite.ipynb) | Eine 0,5 m lange Calcitsäule wird 21 000 s lang mit MgCl₂-Lösung durchströmt (Darcy-Fluss 3·10⁻⁶ m/s). Calcit löst sich, Dolomit fällt in einem Band aus, das mit der Strömung wandert und sich dahinter wieder löst. | `coupled` | Advektion (`darcy_flux`), `outflow`-Rand, ein GEMS-Projekt ohne O, numerische Dispersion; Vergleich mit der veröffentlichten Benchmarkabbildung | 25 s |

Die Tutorials 1 und 2 legen ihre Fälle in `tutorial_runs/` neben `FEniCSx_GEMS` ab, die Tutorials 3 bis 5 laufen im passenden Ordner
`FEniCSx_GEMS/example/<Fall>/`. Die erste Codezelle jedes Notebooks findet diese Ordner selbst.
