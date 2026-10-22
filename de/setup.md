# Einrichtung

## Umgebung

Die Vorlage benötigt Python ≥ 3.10 mit **dolfinx** (0.8 – 0.10), **xgems**, NumPy, SciPy, pandas und
matplotlib. PETSc wird *nicht* benötigt: die Matrizen werden mit dolfinx assembliert und mit SciPy gelöst.
Alles läuft in einem einzigen Prozess.

Unter Windows WSL2 (Ubuntu) mit miniforge verwenden:

```bash
mamba create -n fenicsx -c conda-forge python=3.12 fenics-dolfinx xgems scipy pandas matplotlib jupyterlab
mamba activate fenicsx
python -c "import dolfinx, xgems; print(dolfinx.__version__)"
```

Falls für Ihre Plattform kein xgems-Paket verfügbar ist, aus dem Quellcode bauen
(<https://github.com/gemshub/xgems>, benötigt GEMS3K und pybind11).

## Material

```text
GEMS_FEniCSx_OGS5_Template/
  fe_mesh.py  transport.py  flow.py  gems_ogs.py  reactive_transport.py  ogs_models.py  ogs_io.py  compare.py
  cases/1_calcite  2_hayekit  3_opc_quartz  4_comedy2d  5_concretecrack
        run_case.py  gems/  ogs_input/  reference/
```

Jeder Fall lässt sich auch ohne Notebook ausführen:

```bash
cd GEMS_FEniCSx_OGS5_Template/cases/1_calcite
python run_case.py          # schreibt results/ und gibt den Vergleich mit OGS aus
```

Die Tutorial-Notebooks enthalten denselben Code, in Schritte zerlegt und erklärt. Sie finden den
Vorlagenordner automatisch, wenn er im Notebook-Ordner oder einem übergeordneten Ordner liegt.

## Überall gültige Konventionen

- **Einheiten:** SI; Stoffmengen pro Knoten-Kontrollvolumen (in OGS 1 m³ poröses Medium), Konzentrationen
  in mol pro m³ Porenwasser.
- **Reihenfolge:** alle Arrays in der Knoten- und Elementreihenfolge der OGS-Netzdatei, Spalten in GEMS-Reihenfolge.
- **Chemie an Knoten:** ein GEMS-System pro Netzknoten, wie in OGS.
