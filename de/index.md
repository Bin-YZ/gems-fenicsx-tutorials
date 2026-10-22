# GEMS + FEniCSx: Tutorials zum reaktiven Transport

Diese Seiten vermitteln die Modellierung des reaktiven Transports mit **GEMS** (Minimierung der Gibbs-Energie
für die Chemie) und **FEniCSx** (Finite Elemente für Strömung und Transport). Als Beispiele dienen Benchmarks
von **OpenGeoSys-GEM** (OGS5GEMDEV). Jedes Tutorial baut einen OGS-GEM-Benchmark mit einer kleinen
Python-Vorlage nach und vergleicht das Ergebnis mit der originalen OGS-Ausgabe.

Ziel ist nicht nur, die Fälle laufen zu lassen, sondern *jede* Regel der Kopplung zu verstehen — auch
diejenigen, die nur im OGS-Quellcode stehen — so gut, dass Sie eigene Modelle aufbauen können.

## Lernpfad

| # | Tutorial | neue Konzepte | Laufzeit |
|---|---|---|---|
| 1 | [HAYEKIT](tutorials/01_hayekit) | SNIA, kinetische Schranken, Porositätsrückkopplung, analytische Lösung | 3 min |
| 2 | [Calcitsäule](tutorials/02_calcite) | Advektion, Gleichgewichtsfronten, OGS-Regeln Konzentration ↔ Masse | 15 s |
| 3 | [OPC-Beton + Quarz](tutorials/03_opc_quartz) | 10 000 Jahre langsame Kinetik, Nebenbedingungen, geschlossenes System | 18 min |
| 4 | [comedy2d](tutorials/04_comedy2d) | 2D-Darcy-Strömung, zwei kinetische Phasen, Teilschritte, Überschusswasser-Quelle | 25 s |
| 5 | [ConcreteCrack](tutorials/05_concretecrack) | Risselemente, FEM-FCT, Kozeny–Carman, Grenzen der Reproduktion | 4 min |

Lesen Sie die [Konzeptseiten](concepts/01_snia) parallel; jedes Tutorial verweist auf die verwendeten Konzepte.

## Was Sie brauchen

- den Vorlagenordner `GEMS_FEniCSx_OGS5_Template` (Module + alle Falldaten),
- eine Python-Umgebung mit dolfinx und xgems — siehe [Einrichtung](setup).

## Danksagung

Die Benchmarks, ihre Eingabedateien und Referenzergebnisse stammen aus **OGS5GEMDEV** (OpenGeoSys 5 gekoppelt
mit GEMS3K, hauptsächlich entwickelt von Georg Kosakowski am PSI). GEMS3K und xGEMS werden vom GEMS-Team
(Kulik et al.) entwickelt, FEniCSx vom FEniCS-Projekt. Siehe [Quellen](sources).
