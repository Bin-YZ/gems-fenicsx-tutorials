# Verifikation mit OpenGeoSys-GEM

Bevor es den Einsteigercode oben gab, wurden die Kopplungsregeln erarbeitet, indem fünf Benchmarks von **OpenGeoSys-GEM** (OGS5GEMDEV, hauptsächlich
von G. Kosakowski am PSI entwickelt) mit FEniCSx und GEMS nachgerechnet und mit der Original-Ausgabe von OGS verglichen wurden. Diese Fälle gehen über den
1D-Code hinaus: 2D-Darcy-Strömung, Kinetik, Kluftelemente und flusskorrigierter Transport. Sie verwenden eine eigene Python-Vorlage,
`GEMS_FEniCSx_OGS5_Template` in diesem Repository, die den Regeln von OGS Schritt für Schritt folgt.

Lesen Sie sie als Beleg dafür, dass der Operator-Splitting-Ansatz einen etablierten Code reproduziert, und als ausgearbeitete Beispiele für fortgeschrittene Funktionen.

| # | Benchmark | was er hinzufügt |
|---|---|---|
| 1 | [HAYEKIT](01_hayekit.ipynb) | kinetische Grenzen, Porositätsrückkopplung, analytische Lösung |
| 2 | [Calcitsäule](02_calcite.ipynb) | Advektion, Gleichgewichtsfronten, OGS-Regeln Konzentration ↔ Masse |
| 3 | [OPC-Beton + Quarz](03_opc_quartz.ipynb) | 10 000 Jahre langsame Kinetik, geschlossenes System |
| 4 | [comedy2d](04_comedy2d.ipynb) | 2D-Darcy-Strömung, zwei kinetische Phasen, Unterschritte |
| 5 | [ConcreteCrack](05_concretecrack.ipynb) | Kluftelemente, FEM-FCT, Kozeny–Carman |

Jedes Notebook endet mit einer Fehlertabelle gegenüber der OGS-Referenz. Die OGS-Eingabedateien und Referenzergebnisse in
`GEMS_FEniCSx_OGS5_Template/cases/*/ogs_input` und `…/reference` stammen unverändert aus OGS5GEMDEV.
