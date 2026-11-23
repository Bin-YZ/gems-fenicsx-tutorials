# Verifikation mit OpenGeoSys-GEM

Bevor es den Einsteigercode oben gab, wurden die Kopplungsregeln erarbeitet, indem fünf Benchmarks von **OpenGeoSys-GEM** (OGS5GEMDEV, hauptsächlich
von G. Kosakowski am PSI entwickelt) mit FEniCSx und GEMS nachgerechnet und mit der Original-Ausgabe von OGS verglichen wurden. Diese Fälle gehen über den
1D-Code hinaus: 2D-Darcy-Strömung, Kinetik, Kluftelemente und flusskorrigierter Transport. Sie verwenden eine eigene Python-Vorlage,
`GEMS_FEniCSx_OGS5_Template` in diesem Repository, die den Regeln von OGS Schritt für Schritt folgt.

Lesen Sie sie als Beleg dafür, dass der Operator-Splitting-Ansatz einen etablierten Code reproduziert, und als ausgearbeitete Beispiele für fortgeschrittene Funktionen.

## Was jeder Fall simuliert

**[V1 · HAYEKIT](01_hayekit.ipynb).** Eine 2 mm lange Säule in 1D. Zwei gelöste Spezies A und B diffundieren von beiden Enden hinein und fallen nach einem
kinetischen Ratengesetz als Feststoff AB(s) aus. Der Niederschlag füllt die Poren, die Porosität sinkt und mit ihr der Diffusionskoeffizient $D_e = D_0\phi$.
Es gibt eine analytische Lösung (Hayek, Kosakowski & Churakov 2011). *Neu:* kinetische Grenzen in GEMS, Porositätsrückkopplung, OGS-Restartdateien.

**[V2 · Calcitsäule](02_calcite.ipynb).** Der klassische Engesgaard–Kipp-Benchmark: eine 0,5 m lange Calcitsäule, 21 000 s lang mit konstantem Darcy-Fluss
von MgCl₂-Lösung durchströmt. Calcit löst sich, Dolomit fällt in einem Band hinter der Lösungsfront aus. Dieselbe Chemie wie in Tutorial 5, aber mit dem
CG1-Transport und der Dispersivität von OGS. *Neu:* Advektion–Dispersion der Elementmengen, reine Gleichgewichtsfronten, die OGS-Regeln zur Umrechnung
zwischen Konzentrationen und Knotenmengen.

**[V3 · OPC-Beton + Quarz](03_opc_quartz.ipynb).** Eine 10 m lange Säule aus Portlandzementbeton mit Quarzzuschlag über 10 000 Jahre. Quarz löst sich sehr
langsam (Alkali-Kieselsäure-Reaktion); seine Kieselsäure reagiert mit Portlandit und C-S-H, der pH fällt von 12,9 auf etwa 10, und Zeolithe bilden sich.
Die Randbedingungen in der OGS-Eingabe werden nie gelesen, die Säule ist also ein geschlossenes Batchsystem. *Neu:* ein langsames kinetisches Mineral über
lange Zeiten, Anfangsbedingungen für Spezies, zweistufige Initialisierung.

**[V4 · comedy2d](04_comedy2d.ipynb).** Ein gesättigtes Quadrat von 14 × 14 cm in 2D: ein senkrechter Zementstreifen zwischen zwei Sandbereichen, mit
zuströmender NaCl- und Natriumoxalatlösung und Wasser, das rechts austritt. Oxalat reagiert am Streifen mit Portlandit zu Calciumoxalat. Der Benchmark startet
von einem OGS-Zustand und rechnet 6 Schritte (68 s). *Neu:* ein 2D-Darcy-Strömungsfeld, zwei kinetische Phasen mit Unterschritten, die
Überschusswasserquelle aus GEMS-Volumenänderungen.

**[V5 · ConcreteCrack](05_concretecrack.ipynb).** Ein senkrechter Betonschnitt von 2,5 × 10,5 cm mit Randschicht und einem 0,5 mm breiten, 5 cm tiefen
Riss. Oben steht eine Nitratlösung an; die Strömung läuft hauptsächlich durch den Riss. Der Benchmark rechnet 10 Schritte zu 1 s und prüft die
Initialisierung und die Kopplung von Riss und Matrix. *Neu:* Kluft-Linienelemente in einem 2D-Gitter, Kozeny–Carman-Permeabilität, porositätsabhängige
Diffusion, FEM-FCT und die Grenzen der Reproduzierbarkeit bei einem schlecht konditionierten Strömungsproblem.

Jedes Notebook endet mit einer Fehlertabelle gegenüber der OGS-Referenz. Die OGS-Eingabedateien und Referenzergebnisse in
`GEMS_FEniCSx_OGS5_Template/cases/*/ogs_input` und `…/reference` stammen unverändert aus OGS5GEMDEV.
