"""Text of the landing, setup, API and sources pages, in three languages."""

INDEX = {}
INDEX['en'] = r"""
# GEMS + FEniCSx: reactive transport tutorials

These pages teach reactive transport modelling with **GEMS** (Gibbs energy minimisation for the
chemistry) and **FEniCSx** (finite elements for flow and transport), using benchmarks of
**OpenGeoSys-GEM** (OGS5GEMDEV) as worked examples. Every tutorial rebuilds an OGS-GEM benchmark with a
small Python template and compares the result with the original OGS output.

The goal is not only to run the cases, but to understand *every* rule in the coupling — including the
ones that are only written in the OGS source code — well enough to build your own models.

## Learning path

| # | tutorial | new ideas | runtime |
|---|---|---|---|
| 1 | [HAYEKIT](tutorials/01_hayekit) | SNIA, kinetic limits, porosity feedback, analytical solution | 3 min |
| 2 | [Calcite column](tutorials/02_calcite) | advection, equilibrium fronts, OGS concentration ↔ mass rules | 15 s |
| 3 | [OPC concrete + quartz](tutorials/03_opc_quartz) | 10 000 years of slow kinetics, constraints, closed system | 18 min |
| 4 | [comedy2d](tutorials/04_comedy2d) | 2D Darcy flow, two kinetic phases, sub-steps, excess-water source | 25 s |
| 5 | [ConcreteCrack](tutorials/05_concretecrack) | fracture elements, FEM-FCT, Kozeny–Carman, where reproduction stops | 4 min |

Read the [concept pages](concepts/01_snia) alongside; each tutorial links to the concepts it uses.

## What you need

- the template folder `GEMS_FEniCSx_OGS5_Template` (modules + all case data),
- a Python environment with dolfinx and xgems — see [Setup](setup).

## Credits

The benchmarks, their input files and reference results come from **OGS5GEMDEV** (OpenGeoSys 5 coupled
with GEMS3K, developed mainly by Georg Kosakowski at PSI). GEMS3K and xGEMS are developed by the GEMS
team (Kulik et al.), FEniCSx by the FEniCS project. See [Sources](sources).
"""
INDEX['zh'] = r"""
# GEMS + FEniCSx：反应运移教程

这些页面用 **GEMS**（吉布斯自由能最小化算化学）和 **FEniCSx**（有限元算水流和输运）讲反应运移建模，
以 **OpenGeoSys-GEM**（OGS5GEMDEV）的基准算例为例题。每篇教程用一个小的 Python 模板重建一个 OGS-GEM 算例，
并和 OGS 原始输出比较。

目标不只是把算例跑通，而是把耦合里的**每一条**规则弄明白——包括只写在 OGS 源代码里的那些——
直到能自己搭模型。

## 学习路线

| # | 教程 | 新内容 | 用时 |
|---|---|---|---|
| 1 | [HAYEKIT](tutorials/01_hayekit) | SNIA、动力学上下限、孔隙率反馈、解析解 | 3 分钟 |
| 2 | [方解石柱](tutorials/02_calcite) | 对流、平衡前锋、OGS 的浓度 ↔ 质量换算 | 15 秒 |
| 3 | [OPC 混凝土 + 石英](tutorials/03_opc_quartz) | 1 万年的慢动力学、约束、封闭体系 | 18 分钟 |
| 4 | [comedy2d](tutorials/04_comedy2d) | 二维 Darcy 流、两个动力学相、子步、多余水源项 | 25 秒 |
| 5 | [ConcreteCrack](tutorials/05_concretecrack) | 裂缝单元、FEM-FCT、Kozeny–Carman、复现到哪里为止 | 4 分钟 |

建议配合[概念篇](concepts/01_snia)一起读；每篇教程都链接到它用到的概念。

## 需要什么

- 模板文件夹 `GEMS_FEniCSx_OGS5_Template`（模块 + 所有算例数据）；
- 装有 dolfinx 和 xgems 的 Python 环境，见[安装](setup)。

## 致谢

基准算例、输入文件和参考结果来自 **OGS5GEMDEV**（OpenGeoSys 5 与 GEMS3K 的耦合，主要由 PSI 的
Georg Kosakowski 开发）。GEMS3K 和 xGEMS 由 GEMS 团队（Kulik 等）开发，FEniCSx 由 FEniCS 项目开发。见[参考文献](sources)。
"""
INDEX['de'] = r"""
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
"""

SETUP = {}
SETUP['en'] = r"""
# Setup

## Environment

The template needs Python ≥ 3.10 with **dolfinx** (0.8 – 0.10), **xgems**, NumPy, SciPy, pandas and
matplotlib. PETSc is *not* needed: matrices are assembled with dolfinx and solved with SciPy. Everything
runs in a single process.

On Windows use WSL2 (Ubuntu) with miniforge:

```bash
mamba create -n fenicsx -c conda-forge python=3.12 fenics-dolfinx xgems scipy pandas matplotlib jupyterlab
mamba activate fenicsx
python -c "import dolfinx, xgems; print(dolfinx.__version__)"
```

If no xgems package is available for your platform, build it from source
(<https://github.com/gemshub/xgems>, it needs GEMS3K and pybind11).

## Material

```text
GEMS_FEniCSx_OGS5_Template/
  fe_mesh.py  transport.py  flow.py  gems_ogs.py  reactive_transport.py  ogs_models.py  ogs_io.py  compare.py
  cases/1_calcite  2_hayekit  3_opc_quartz  4_comedy2d  5_concretecrack
        run_case.py  gems/  ogs_input/  reference/
```

Each case can be run without the notebooks:

```bash
cd GEMS_FEniCSx_OGS5_Template/cases/1_calcite
python run_case.py          # writes results/ and prints the comparison with OGS
```

The tutorial notebooks contain the same code, cut into steps and explained. They find the template
folder automatically if it lies in the notebook folder or in one of its parents.

## Conventions used everywhere

- **Units:** SI; amounts in mol per node control volume (1 m³ of porous medium in OGS), concentrations in
  mol per m³ of pore water.
- **Ordering:** all arrays are in the node and element order of the OGS mesh file, columns in GEMS order.
- **Chemistry at nodes:** one GEMS system per mesh node, as in OGS.
"""
SETUP['zh'] = r"""
# 安装

## 环境

模板需要 Python ≥ 3.10，以及 **dolfinx**（0.8 – 0.10）、**xgems**、NumPy、SciPy、pandas、matplotlib。
**不需要** PETSc：矩阵用 dolfinx 组装，用 SciPy 求解。全部单进程运行。

Windows 上用 WSL2（Ubuntu）+ miniforge：

```bash
mamba create -n fenicsx -c conda-forge python=3.12 fenics-dolfinx xgems scipy pandas matplotlib jupyterlab
mamba activate fenicsx
python -c "import dolfinx, xgems; print(dolfinx.__version__)"
```

如果你的平台没有 xgems 的安装包，就从源码编译（<https://github.com/gemshub/xgems>，需要 GEMS3K 和 pybind11）。

## 材料

```text
GEMS_FEniCSx_OGS5_Template/
  fe_mesh.py  transport.py  flow.py  gems_ogs.py  reactive_transport.py  ogs_models.py  ogs_io.py  compare.py
  cases/1_calcite  2_hayekit  3_opc_quartz  4_comedy2d  5_concretecrack
        run_case.py  gems/  ogs_input/  reference/
```

每个算例也可以不用 notebook 直接运行：

```bash
cd GEMS_FEniCSx_OGS5_Template/cases/1_calcite
python run_case.py          # 写 results/，并打印和 OGS 的比较
```

教程 notebook 里是同样的代码，拆成步骤并加了讲解。模板文件夹放在 notebook 所在目录或它的任一上级目录里，notebook 会自动找到。

## 全书统一的约定

- **单位：** 国际单位；物质的量按节点控制体积计（OGS 里是 1 m³ 多孔介质），浓度是每 m³ 孔隙水的 mol。
- **编号：** 所有数组按 OGS 网格文件里的节点和单元顺序，列按 GEMS 的顺序。
- **化学在节点上：** 每个网格节点一个 GEMS 体系，和 OGS 一样。
"""
SETUP['de'] = r"""
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
"""

API_HEAD = {'en': '# Template API\n\nGenerated from the docstrings of the template modules.\n',
            'zh': '# 模板 API\n\n由模板模块里的说明文字自动生成（英文）。\n',
            'de': '# API der Vorlage\n\nAus den Docstrings der Vorlagenmodule erzeugt (englisch).\n'}
API_BODY = '\n'.join(f"""
## `{m}`

```{{automodule}} {m}
:members:
:undoc-members:
```
""" for m in ['reactive_transport', 'gems_ogs', 'transport', 'flow', 'fe_mesh', 'ogs_models', 'ogs_io', 'compare'])

SOURCES = {}
_refs = r"""
- **OGS5GEMDEV** — OpenGeoSys 5 coupled with GEMS3K; benchmarks `C/calcite_gems`, `C/HAYEKIT`,
  `PETSc/comedy2d`, `PETSc/ConcreteCrack`, `LookUp-Table/Case1`, `PETSc/TransLay2d` and their reference results.
- Shao H., Dmytrieva S.V., Kolditz O., Kulik D.A., Pfingsten W., Kosakowski G. (2009). Modeling reactive
  transport in non-ideal aqueous–solid solution system. *Applied Geochemistry* 24, 1287–1300.
- Kosakowski G., Watanabe N. (2014). OpenGeoSys-Gem: A numerical tool for calculating geochemical and porosity
  changes in saturated and partially saturated media. *Physics and Chemistry of the Earth* 70–71, 138–149.
- Hayek M., Kosakowski G., Churakov S. (2011). Exact analytical solutions for a diffusion problem coupled with
  precipitation–dissolution reaction and feedback of porosity change. *Water Resources Research* 47, W07545.
- Hayek M., Kosakowski G., Jakob A., Churakov S. (2012). A class of analytical solutions for multidimensional
  multispecies diffusive transport coupled with precipitation–dissolution reactions and porosity changes.
  *Water Resources Research* 48, W03525.
- Kulik D.A., Wagner T., Dmytrieva S.V., Kosakowski G., Hingerl F.F., Chudnenko K.V., Berner U. (2013).
  GEM-Selektor geochemical modeling package: revised algorithm and GEMS3K numerical kernel for coupled
  simulation codes. *Computational Geosciences* 17, 1–24.
- xGEMS: <https://github.com/gemshub/xgems>
- Baratta I.A. et al. (2023). DOLFINx: the next generation FEniCS problem solving environment. Zenodo.
- Kuzmin D. (2009). Explicit and implicit FEM-FCT algorithms with flux linearization.
  *Journal of Computational Physics* 228, 2517–2534.
"""
SOURCES['en'] = '# Sources\n\n' + _refs + """
The OGS input files and reference results in `cases/*/ogs_input` and `cases/*/reference` are taken
unchanged from OGS5GEMDEV; please cite the original work when you use them.
"""
SOURCES['zh'] = '# 参考文献\n\n' + _refs + """
`cases/*/ogs_input` 和 `cases/*/reference` 里的 OGS 输入文件和参考结果原样取自 OGS5GEMDEV；使用时请引用原始工作。
"""
SOURCES['de'] = '# Quellen\n\n' + _refs + """
Die OGS-Eingabedateien und Referenzergebnisse in `cases/*/ogs_input` und `cases/*/reference` stammen
unverändert aus OGS5GEMDEV; bitte zitieren Sie bei Verwendung die Originalarbeiten.
"""
