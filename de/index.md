# FEniCSx + GEMS reaktiver Transport

Diese Seiten erklären einen kleinen Python-Code, der zwei Programme koppelt:

- **[FEniCSx](https://fenicsproject.org)** transportiert gelöste Elemente durch Diffusion und Advektion durch eine eindimensionale poröse Säule;
- **[GEMS3K](https://gems.web.psi.ch)**, über `xgems` aufgerufen, berechnet in jeder Zelle das lokale chemische Gleichgewicht.

Eine ganze Simulation wird durch **eine Eingabedatei, `case.yaml`**, beschrieben. Für ein neues Problem ändern Sie nur diese Datei.
Die Python-Module bleiben unverändert.

```{image} figures/coupling_loop.png
:alt: Ein Zeitschritt: coupling.py liest case.yaml, gibt die gelösten Mengen an transport.py und die Gesamtmengen an chemistry.py und schreibt den Zustand mit output.py
:width: 100%
```

## Schnellstart

```bash
# 1. Umgebung mit FEniCSx, PETSc, GEMS3K und PyYAML (siehe Installation)
conda activate fenicsx

# 2. Eingabe bearbeiten
cd FEniCSx_GEMS
nano case.yaml                  # oder der Case Builder im Browser

# 3. Rechnen; die Ergebnisse landen in output.folder
python coupling.py case.yaml
```

Unter Windows mit WSL erledigt ein Doppelklick auf `Run.cmd` Schritt 3.

## Aufbau der Seiten

| Teil | Inhalt |
|---|---|
| [Installation](install.md) | Python-Umgebung einrichten und prüfen |
| [Wie die Kopplung funktioniert](coupling/overview.md) | Was die vier Module in jedem Zeitschritt austauschen, Einheiten, Erhaltung |
| [Gleichungen und Numerik](coupling/numerics.md) | Transportgleichung, Diskretisierung, Rückkopplung von Porosität und Diffusivität |
| [Rechnungen beschleunigen](coupling/performance.md) | Wo die Zeit bleibt, Prozesse vs. Threads, Arrays vs. Dictionaries |
| [`case.yaml`-Referenz](yaml/index.md) | Jeder Schlüssel der vier Abschnitte mit Einheit, Standardwert und Beispiel |
| [Browser-Werkzeuge](tools/case_builder.md) | `case.yaml` über ein Formular erstellen; ein GEMS-Projekt im Browser ansehen |
| [Tutorials](tutorials/01_tracer_diffusion.ipynb) | Fünf Fälle, vom Tracer ohne Chemie bis zur Calcit–Dolomit-Umwandlung mit Strömung |
| [Ergebnisse und Fehlersuche](outputs.md) | Inhalt jeder Ausgabedatei; was tun, wenn GEMS nicht konvergiert |
| [Verifikation mit OGS-GEM](verification/index.md) | Fünf OpenGeoSys-GEM-Benchmarks, mit FEniCSx und GEMS nachgerechnet |

## Lernpfad

1. [Tracer-Diffusion](tutorials/01_tracer_diffusion.ipynb): Modus `diffusion`, analytische Lösung, Massenbilanz
2. [Ein chemisches Gleichgewicht](tutorials/02_single_equilibrium.ipynb): Modus `chemistry`, Rezepte, Phasennamen, Gibbs-Energien
3. [NaCl-Diffusion](tutorials/03_nacl_diffusion.ipynb): erster `coupled`-Lauf, zwei Zonen
4. [Zementauslaugung](tutorials/04_cement_leaching.ipynb): Rückkopplung von Porosität und Diffusivität
5. [Calcit → Dolomit](tutorials/05_calcite_dolomite.ipynb): Advektion, Zu- und Abflussränder

Jedes Tutorial zeigt die vollständige `case.yaml`, die gegenüber dem vorherigen geänderten Zeilen, den Lauf und die Ergebnisse.
