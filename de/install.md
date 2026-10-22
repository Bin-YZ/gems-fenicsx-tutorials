# Installation

Der Code braucht folgende Python-Pakete:

| Paket | verwendet von | für |
|---|---|---|
| `fenics-dolfinx` **mit PETSc** | `transport.py`, `output.py` | Gitter, Finite-Elemente-Formen, linearer Löser, XDMF-Ausgabe |
| `petsc4py`, `mpi4py` | `transport.py` | PETSc-Löserobjekte |
| `xgems` | `chemistry.py` | chemisches Gleichgewicht mit GEMS3K |
| `pyyaml` | `coupling.py` | Lesen von `case.yaml` |
| `numpy` | alle | Arrays |

`pandas` und `matplotlib` werden nur in den Tutorial-Notebooks verwendet.

## Linux, macOS oder Windows mit WSL

Alle Pakete gibt es auf conda-forge. Mit [Miniforge](https://github.com/conda-forge/miniforge) legen Sie eine Umgebung an:

```bash
conda create -n fenicsx -c conda-forge python=3.12 fenics-dolfinx petsc4py mpich xgems pyyaml pandas matplotlib jupyterlab
conda activate fenicsx
```

FEniCSx läuft nicht nativ unter Windows. Installieren Sie WSL (`wsl --install` in einer PowerShell mit Administratorrechten), öffnen Sie das Ubuntu-Terminal
und führen Sie dort die beiden Befehle aus.

## Den Code holen

Der Code ist der Ordner `FEniCSx_GEMS` im Repository dieser Seiten:

```text
FEniCSx_GEMS/
├── coupling.py        liest case.yaml, Zeitschleife, Datenaustausch, Rückkopplung
├── transport.py       FEniCSx-Gitter, Randbedingungen, Löser
├── chemistry.py       GEMS-Engine, Rezepte, lokales Gleichgewicht
├── output.py          CSV / XDMF / PNG / Zusammenfassungen
├── case.yaml          die Eingabe
├── chemistry_data/    das GEMS-Projekt von case.yaml
├── example/           die Fälle der Tutorials 3 bis 5
├── case_builder.html  Browser-Formular, das case.yaml schreibt
└── gems_inspector.html Browser-Ansicht für GEMS-Projekte
```

## Umgebung prüfen

```bash
cd FEniCSx_GEMS
python -c "import dolfinx, xgems, yaml; print(dolfinx.__version__, dolfinx.has_petsc)"
```

Die Ausgabe sollte mit `True` enden. Ein FEniCSx ohne PETSc lässt sich importieren, aber `transport.py` bricht dann mit
`No module named 'petsc4py'` ab.

Danach [Tutorial 1](tutorials/01_tracer_diffusion.ipynb) (braucht FEniCSx, nicht GEMS) und [Tutorial 2](tutorials/02_single_equilibrium.ipynb) (braucht GEMS, nicht FEniCSx) ausführen.
Zusammen prüfen sie beide Hälften.

## Windows: `Run.cmd`

`Run.cmd` ruft das WSL-Python der Umgebung direkt auf. Ein Doppelklick rechnet also die `case.yaml` im selben Ordner:

```bat
wsl /home/<user>/miniforge3/envs/fenicsx/bin/python ../../coupling.py "%CASE_FILE%"
```

Ersetzen Sie `/home/<user>/miniforge3/envs/fenicsx` durch den Pfad Ihrer Umgebung (`conda env list` zeigt ihn). `Run.cmd other.yaml` rechnet eine andere Eingabedatei.

## Mehrere Prozesse

Diese Version läuft nur mit einem MPI-Prozess (`transport.py` meldet sonst *This version supports one MPI process*). In 1D ist das Gitter klein.
Fast die ganze Rechenzeit entfällt auf GEMS: ein Gleichgewicht pro Zelle und Zeitschritt.
