# `case.yaml` im Überblick

Eine Datei beschreibt die ganze Simulation. Sie hat **genau vier Abschnitte auf oberster Ebene**, einen pro Modul. Ein fünfter oder ein fehlender
Abschnitt beendet den Lauf mit *Use exactly four sections*.

```yaml
chemistry:   # chemistry.py  GEMS-Projekt, Bedingungen, Phasen, Rezepte
transport:   # transport.py  Geometrie, Material, Zonen, Ränder, Löser
coupling:    # coupling.py   Modus, Zeitschritte, Rückkopplung von Porosität/Diffusivität
output:      # output.py     Ergebnisordner, wie oft Profile geschrieben werden
```

| Seite | Schlüssel |
|---|---|
| [chemistry](chemistry.md) | `project`, `temperature`, `pressure`, `aqueous_phase`, `solid_phases`, `gibbs`, `initial`, `inlet`, `start`, `on_failure` |
| [transport](transport.md) | `geometry`, `material` (`phi`, `De`, `darcy_flux`), `zones`, `components`, `initial`, `boundary`, `solver` |
| [coupling und output](coupling_output.md) | `mode`, `time`, `update_porosity`, `update_diffusivity`, `exponent`; `folder`, `every` |
| [Von GEMS-Selektor zum Rezept](from_gems.md) | woher die Zahlen für `initial` und `inlet` kommen |

## Der Standardfall

Das ist `FEniCSx_GEMS/case.yaml`: eine Zementpaste in Kontakt mit einer CaCl₂-Lösung, mit Rückkopplung von Porosität und Diffusivität.

```{literalinclude} ../../FEniCSx_GEMS/case.yaml
:language: yaml
```

## Regeln, die Zeit sparen

- **Pfade sind relativ zur Datei `case.yaml`**, nicht zum Ort, an dem Python gestartet wird. Das gilt für `chemistry.project` und
  `output.folder`.
- **Einheiten sind SI** (m, s, K, Pa, m²/s, m/s). Einzige Ausnahme sind chemische Rezepte: mol pro **dm³ Gesamtmaterial**.
- **Gleitkommazahlen mit Dezimalpunkt schreiben:** `1.0e-15`, nicht `1e-15`. PyYAML liest `1e-15` als Zeichenkette. Die meisten Schlüssel werden
  danach umgewandelt, aber ein Dezimalpunkt vermeidet Überraschungen.
- **Ganzzahlen müssen Ganzzahlen sein:** `cells: 40` und `every: 5`, nicht `40.0`.
- **`true`/`false`** für die Rückkopplungsschalter, nicht `yes`/`1`.
- **Namen unterscheiden Groß- und Kleinschreibung** und müssen zum GEMS-Projekt passen: `Ca`, `Portlandite`, `aq_gen`.
- `{a: 1, b: 2}` ist dasselbe wie `a: 1` und `b: 2` auf eigenen, eingerückten Zeilen, und `[A, B]` ist eine Liste. Kommentare beginnen mit `#`.
- **Schlüssel, die vorhanden, aber nicht benötigt sind, werden ignoriert**, z. B. `transport.components` im Modus coupled. Die Beispieldateien
  behalten sie, damit ein Moduswechsel nur eine Zeile kostet.

## Vorgehen für einen neuen Fall

1. Einen Beispielordner kopieren, der Ihrem Problem nahekommt (siehe [Tutorials](../tutorials/01_tracer_diffusion.ipynb)).
2. Ihre GEMS-Projektdateien hineinlegen und `chemistry.project` auf die `.lst`-Datei zeigen lassen.
3. Einmal mit `mode: chemistry` rechnen, um Rezept und Phasennamen zu prüfen.
4. Mit `mode: diffusion` Gitter, Zeitschritt und Ränder ohne GEMS prüfen.
5. Auf `mode: coupled` umstellen. Mit kurzem `end` beginnen, `summary.txt` und `profiles.png` ansehen, dann die volle Zeit rechnen.
6. Vor jeder neuen Variante `output.folder` ändern, damit frühere Ergebnisse erhalten bleiben. `case_used.json` in jedem Ordner hält die genauen
   Einstellungen dieses Laufs fest.
