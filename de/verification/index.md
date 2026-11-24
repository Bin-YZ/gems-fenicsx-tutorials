# Verifikation mit OpenGeoSys-GEM

## Was diese Fälle sind und was sie zeigen können

Die fünf Fälle dieses Kapitels vergleichen eine Nachrechnung mit den Originalergebnissen von **OpenGeoSys-GEM** (OGS5GEMDEV, hauptsächlich von
G. Kosakowski am PSI entwickelt). Zwei Dinge sind vor dem Lesen wichtig:

- **Sie verwenden einen anderen Code.** Die Fälle laufen mit `GEMS_FEniCSx_OGS5_Template`, einer Python-Vorlage, die die Regeln von OGS Schritt für Schritt
  übernimmt (Netz in OGS-Knotenreihenfolge, OGS-Umrechnung Konzentration ↔ Masse, kinetische Grenzen, FEM-FCT, Kluftelemente, 2D-Strömung). Sie verwenden
  **weder** `case.yaml` noch den 1D-Code der Tutorials.
- **Die meisten prüfen die Reproduktion, nicht die physikalische Richtigkeit.** Die Referenz ist meist die Ausgabe eines anderen Codes, mit dessen Einstellungen
  und für eine begrenzte Zeitspanne oder Auswahl von Größen. Übereinstimmung zeigt, dass dasselbe Modell mit denselben Regeln umgesetzt wurde; sie zeigt nicht, dass
  das Modell die Wirklichkeit beschreibt. Nur V1 hat zusätzlich eine analytische Lösung.

Was das Kapitel für den Tutorial-Code belegt: Beide Codes teilen das Operator-Splitting, den Transport von Elementmengen und die Kopplung an GEMS. Die Übereinstimmung
mit OGS ist ein Hinweis darauf, dass sich diese gemeinsamen Bestandteile wie in einem etablierten Code verhalten. Sie ist keine vollständige Verifikation von
`FEniCSx_GEMS`; dieser hat seine eigenen Prüfungen in den Tutorials.

## Ergebnisse auf einen Blick

| Fall | Referenz und Bedingungen | verglichene Größen | Ergebnis | Grenzen |
|---|---|---|---|---|
| [V1 · HAYEKIT](01_hayekit.ipynb) | OGS-Ausgabe bei 10 000 s, gleiches Netz und dt; analytische Lösung | gelöste Stoffe, Niederschlag, Porosität an allen Knoten | gegen OGS ≤ 3·10⁻⁵ (Porosität 3·10⁻⁴); gegen analytisch 24 % bei dt = 100 s, 0,3 % bei 10 s, 2,7 % bei 1 s (nur Vorlage) | deutlich zeitschrittabhängig; die vorhandenen Tests zeigen keine Konvergenz gegen die analytische Lösung; mit OGS nur bei 100 s verglichen |
| [V2 · Calcitsäule](02_calcite.ipynb) | OGS-Ausgabe bei 21 000 s, gleiches Netz | pH, Porosität, Elemente, Ionen, Calcit, Dolomit | Elemente/Ionen ≤ 1,1 %; Minerale 5 % nur am Frontknoten | keine analytische Lösung, keine Gitterstudie; Ursache am Frontknoten nicht getrennt |
| [V3 · OPC + Quarz](03_opc_quartz.ipynb) | OGS-Zeitreihen an 4 Knoten, 0–919 Jahre | 14 Mineral- und Lösungsgrößen | nRMSE ≤ 0,12 %, Zeolithe ≤ 0,28 % | kein Transport über die Ränder, aber mit der Wassernachlieferung von OGS (H, O, Cl, Na, K nehmen zu); Transport nicht geprüft; 919–10 000 Jahre ohne Referenz |
| [V4 · comedy2d](04_comedy2d.ipynb) | OGS-Ausgabe 68 s nach einem Restart bei ~7,5 Tagen | Elemente, pH, Druckhöhe, zwei kinetische Phasen, Geschwindigkeiten | Zustand nach 68 s ≤ 1,4·10⁻⁴ mit lockeren kinetischen Grenzen (streng 56 % daneben); räumliches Muster der Änderung über 68 s stimmt | kein Fehlermaß für die Änderung selbst; nur 68 s; 5 Knoten scheitern im Restart-Lauf, wie in OGS |
| [V5 · ConcreteCrack](05_concretecrack.ipynb) | OGS-Ausgabe bei 10 s | 11 Elemente, Porosität, pH, Portlandit, Druckhöhe | Chemie ≤ 1,3·10⁻³; Druckhöhe − 10 m: 0,5–0,6, **nicht** reproduziert | nur 10 s; der Vergleich der Druckhöhe kann die Implementierungsvarianten nicht unterscheiden und bestätigt nicht, dass der Strömungsteil verifiziert ist |

Fehlerdefinitionen: V1, V2, V4, V5 verwenden max\|Vorlage − Referenz\| / max\|Referenz\| über alle Knoten, angewandt auf den Zustand zum Vergleichszeitpunkt
(in V4 nicht auf die Änderung während der 68 s). Ausnahme: Die Druckhöhe in V5 wird als Druckhöhe − 10 m verglichen, weil sie selbst überall ≈ 10 m ist
und eine Normierung damit die Unterschiede verdecken würde. V3 verwendet die RMS-Abweichung über die OGS-Ausgabezeiten,
geteilt durch die Spannweite der OGS-Reihe (nRMSE).

## Was jeder Fall simuliert

**V1 · HAYEKIT.** Eine 2 mm lange Säule in 1D. Zwei gelöste Spezies diffundieren von beiden Enden hinein und fallen nach einem kinetischen Ratengesetz als Feststoff
aus; der Niederschlag füllt die Poren und verlangsamt die Diffusion.

**V2 · Calcitsäule.** Der Engesgaard–Kipp-Benchmark: eine 0,5 m lange Calcitsäule, mit konstantem Darcy-Fluss von MgCl₂-Lösung durchströmt. Dieselbe Chemie wie
Tutorial 5, aber mit dem CG1-Transport und der Dispersivität von OGS.

**V3 · OPC-Beton + Quarz.** Eine 10 m lange Säule aus Portlandzementbeton mit Quarzzuschlag. Quarz löst sich sehr langsam (Alkali-Kieselsäure-Reaktion), der pH fällt
von 12,9 auf etwa 10, und Zeolithe bilden sich. OGS liest die Randbedingungen nie, über die Ränder gelangt also nichts, und jeder Knoten ist derselbe Batchreaktor; ein geschlossenes System ist es
aber nicht, weil OGS das von Reaktionen verbrauchte Wasser durch Porenwasser der aktuellen Zusammensetzung ersetzt.

**V4 · comedy2d.** Ein gesättigtes Quadrat von 14 × 14 cm in 2D: ein Zementstreifen zwischen zwei Sandbereichen, mit zuströmender NaCl- und Oxalatlösung. Oxalat
reagiert am Streifen mit Portlandit zu Calciumoxalat.

**V5 · ConcreteCrack.** Ein Betonschnitt von 2,5 × 10,5 cm mit Randschicht und einem 0,5 mm breiten Riss; oben eine Nitratlösung, die Strömung läuft hauptsächlich durch den Riss.

## Einen Fall rechnen

Jeder Fall hat einen eigenen Ordner mit den OGS-Eingabedateien, den GEMS-Dateien und den Referenzergebnissen:

```bash
cd GEMS_FEniCSx_OGS5_Template/cases/2_hayekit      # 1_calcite, 2_hayekit, 3_opc_quartz, 4_comedy2d, 5_concretecrack
python run_case.py                                   # Windows: Run.cmd
```

Das Skript gibt dieselben Fehlertabellen aus wie die Notebooks. Die Notebooks dieser Seiten sind mit ihren Ausgaben gespeichert; die Seiten rechnen sie nicht neu.
Die OGS-Eingabedateien und Referenzergebnisse in `cases/*/ogs_input` und `cases/*/reference` stammen unverändert aus OGS5GEMDEV.
