# Case Builder

`case_builder.html` ist ein Formular für die vier Abschnitte von `case.yaml`. Beim Bearbeiten zeigt es eine laufende YAML-Vorschau, prüft
Grundwerte und chemische Namen und erlaubt **Copy** (Kopieren) oder **Download** (Herunterladen) des Ergebnisses. Es läuft vollständig im Browser;
nichts wird hochgeladen.

<p><a href="../_static/tools/case_builder.html" target="_blank" rel="noopener">Case Builder in eigenem Tab öffnen ↗</a></p>

<iframe src="../_static/tools/case_builder.html" title="Case Builder" style="width:100%;height:900px;border:1px solid #d9dfdb;border-radius:6px"></iframe>

## So geht's

1. Mit dem eingebauten Beispiel beginnen oder mit **Import case.yaml** einen bestehenden Fall laden.
2. Unter *Chemistry* auf **Choose GEMS folder** klicken und den Ordner mit der exportierten `.lst` und ihrer DCH-Datei (`.json` oder Text-`.dat`) wählen.
   Element-, Phasen- und Speziesnamen kommen dann aus Ihrem Projekt. Darauf achten, dass `chemistry.project` relativ zum späteren Speicherort von `case.yaml` ist.
3. Rezepte, Temperatur, Druck, Phasen und optionale Gibbs-Energien ausfüllen; dann Geometrie, Porosität, Diffusivität, Ränder, Löser, Modus, Zeit und
   Rückkopplung. Im Formular gewählte Zeiteinheiten werden in Sekunden umgerechnet.
4. Die Prüfmeldungen lesen, **Download**, `case.yaml` neben die Chemiedaten legen und `python coupling.py case.yaml` ausführen.

## Grenzen

Das Formular deckt den einfachen Diffusionsfall mit einem Material ab. Zonen, `darcy_flux`, `outflow`-Ränder, seitenweises `inlet` sowie
`start`/`on_failure` unterstützt es **nicht** und erhält sie beim Import und Export nicht zuverlässig. Diese von Hand nach der
[`case.yaml`-Referenz](../yaml/index.md) bearbeiten. Die Seite bereitet nur die Eingabe vor; sie startet GEMS nicht und prüft nicht, ob ein Rezept konvergiert.
Dafür `mode: chemistry` verwenden ([Tutorial 2](../tutorials/02_single_equilibrium.ipynb)).
