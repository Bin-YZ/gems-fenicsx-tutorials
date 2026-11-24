# Überblick über die Tutorials

Die fünf Tutorials verwenden den 1D-Code in `FEniCSx_GEMS`. Jeder Fall wird **nur durch Bearbeiten von `case.yaml`** eingerichtet; die Python-Module werden nicht
geändert. Jedes Tutorial folgt derselben Reihenfolge: das physikalische Problem → die Modellannahmen → wie `case.yaml` sie ausdrückt → der Lauf → wie man das
Ergebnis liest → was der Fall zeigt und was nicht.

Sie bauen aufeinander auf: Diffusion ohne Chemie, dann Chemie ohne Transport, dann beides zusammen, dann Minerale, dann Strömung.

## 1 · [Tracer-Diffusion](01_tracer_diffusion.ipynb)

- **Simuliert:** einen nicht reaktiven Tracer, der von einem Rand mit c = 1 in eine 10 mm lange wassergesättigte Säule diffundiert. Modus `diffusion`, etwa 2 s.
- **Man lernt:** die vier Abschnitte von `case.yaml`, wie man einen Fall rechnet, die Ergebnisdateien und die Massenbilanz.
- **Verglichen mit:** der exakten analytischen Lösung.
- **Ergebnis:** größte Abweichung 9·10⁻⁴ mol/m³ (0,1 % des Randwerts); die Massenbilanz schließt auf 10⁻¹⁷ mol/m².

## 2 · [Ein chemisches Gleichgewicht](02_single_equilibrium.ipynb)

- **Simuliert:** ein GEMS-Gleichgewicht einer hydratisierten Zementpaste, dann einen Scan ihres Ca/Si von 3,7 bis 0,5. Modus `chemistry`, etwa 15 s.
- **Man lernt:** Element- und Phasennamen eines GEMS-Projekts, Einheiten der Rezepte (mol pro dm³ Gesamtmaterial), wie man ein Rezept prüft, die `gibbs`-Anpassungen.
- **Verglichen mit:** nichts Externem; der Mineralbestand wird auf Stimmigkeit geprüft (Portlandit + C-S-H bei pH 12,45).
- **Ergebnis:** Portlandit verschwindet unter Ca/Si ≈ 1,5, amorphes SiO₂ erscheint unter ≈ 0,65.

## 3 · [NaCl-Diffusion](03_nacl_diffusion.ipynb)

- **Simuliert:** 1-M- und 0,5-M-NaCl-Lösung, die sich in einer 20-mm-Säule treffen, 100 s, keine Feststoffe. Modus `coupled`, etwa 5 s.
- **Man lernt:** den ersten gekoppelten Lauf, Zonen mit eigenen Rezepten, seitenweise Randlösungen.
- **Verglichen mit:** der erf-Lösung mit dem binären Salzdiffusionskoeffizienten.
- **Ergebnis:** größte Abweichung 0,43 % der 1-M-Konzentration. Geprüft wird die gekoppelte Schleife, nicht die Annahme eines einzigen Koeffizienten.

## 4 · [Zementauslaugung](04_cement_leaching.ipynb)

- **Simuliert:** eine 4 mm dicke Zementpaste, 1000 Jahre in Kontakt mit 14,6-mM-CaCl₂-Wasser. Modus `coupled`, zwei Läufe zu 3–5 min.
- **Man lernt:** reagierende Minerale, lange Zeiten und was sich ändert, wenn die Rückkopplung von Porosität und Diffusivität eingeschaltet wird.
- **Verglichen mit:** HYDRUS-Profilen desselben Benchmarks (φ und De konstant).
- **Ergebnis:** Die Portlanditfront liegt bis auf etwa eine Zelle (0,1 mm) bei HYDRUS. Mit Rückkopplung wandert die Front etwas *weniger* weit.

## 5 · [Calcit → Dolomit](05_calcite_dolomite.ipynb)

- **Simuliert:** eine 0,5 m lange Calcitsäule, 21 000 s mit MgCl₂-Lösung durchströmt; ein Dolomitband bildet sich und wandert. Modus `coupled`, etwa 25 s.
- **Man lernt:** Advektion (`darcy_flux`), einen `outflow`-Rand, ein GEMS-Projekt ohne O, numerische Dispersion und Gittergröße.
- **Verglichen mit:** der veröffentlichten Benchmarkabbildung (nur Vergleich mit dem Auge; die Referenzkurven liegen als Bild vor).
- **Ergebnis:** Front- und Bandlagen stimmen mit dem Auge überein; die Verfeinerung von 100 auf 1000 Zellen schärft die Bandränder, verschiebt das Band aber nicht.

## Wo die Fälle laufen

Die Tutorials 1 und 2 legen ihre Fälle in `tutorial_runs/` neben `FEniCSx_GEMS` ab, die Tutorials 3 bis 5 laufen im passenden Ordner
`FEniCSx_GEMS/example/<Fall>/`. Die erste Codezelle jedes Notebooks findet diese Ordner selbst.
