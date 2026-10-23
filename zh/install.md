# 安装

代码需要以下 Python 包：

| 包 | 使用者 | 用途 |
|---|---|---|
| `fenics-dolfinx`（**带 PETSc**） | `transport.py`、`output.py` | 网格、有限元形式、线性求解器、XDMF 输出 |
| `petsc4py`、`mpi4py` | `transport.py` | PETSc 求解器对象 |
| `xgems` | `chemistry.py` | GEMS3K 化学平衡 |
| `pyyaml` | `coupling.py` | 读取 `case.yaml` |
| `numpy` | 全部 | 数组 |

`pandas` 和 `matplotlib` 只在教程 notebook 中使用。

## Linux、macOS 或 Windows（WSL）

所有包都在 conda-forge 上。用 [Miniforge](https://github.com/conda-forge/miniforge) 建一个环境：

```bash
conda create -n fenicsx -c conda-forge python=3.12 fenics-dolfinx=0.10 petsc4py mpich xgems=2.1 pyyaml pandas matplotlib scipy jupyterlab
conda activate fenicsx
```

FEniCSx 不能在 Windows 上原生运行。先安装 WSL（以管理员身份在 PowerShell 中运行 `wsl --install`），打开 Ubuntu 终端，再在其中执行上面两条命令。

## 测试过的版本

本站教程是用下面这些 conda-forge 包运行的（Linux，2026 年 10 月）。其他版本也可能可用，但 dolfinx 的 Python 接口在小版本之间会变化（0.9 → 0.10），因此除非你准备修改 `transport.py`，请使用 **dolfinx 0.10.x**。

| 包 | 版本 |
|---|---|
| Python | 3.12.13 |
| fenics-dolfinx | 0.10.0 (basix 0.10.0, ffcx 0.10.0, ufl 2025.2.1) |
| PETSc / petsc4py | 3.25.6 |
| mpi4py / mpich | 4.1.2 / 5.0.1 |
| xgems (GEMS3K) | 2.1.2 |
| pyyaml | 6.0.3 |
| numpy | 2.5.4 |
| pandas / matplotlib / scipy | 3.0.6 / 3.11.2 / 1.18.1 （仅教程使用） |
| jupyter-book | 1.0.4 （仅用于构建本网站；不兼容 2.x） |

查看已安装的版本：

```bash
conda list -n fenicsx | grep -E "dolfinx|petsc|xgems|pyyaml|numpy"
```

## 获取代码

代码是本站仓库中的 `FEniCSx_GEMS` 文件夹：

```text
FEniCSx_GEMS/
├── coupling.py        读取 case.yaml、时间循环、数据交换、反馈
├── transport.py       FEniCSx 网格、边界条件、求解器
├── chemistry.py       GEMS 引擎、配方、局部平衡
├── output.py          CSV / XDMF / PNG / 摘要文件
├── case.yaml          输入文件
├── chemistry_data/    case.yaml 使用的 GEMS 项目
├── example/           教程 3–5 的算例
├── case_builder.html  生成 case.yaml 的浏览器表单
└── gems_inspector.html 查看 GEMS 项目的浏览器工具
```

## 检查环境

```bash
cd FEniCSx_GEMS
python -c "import dolfinx, xgems, yaml; print(dolfinx.__version__, dolfinx.has_petsc)"
```

输出最后应为 `True`。不带 PETSc 的 FEniCSx 也能 import，但 `transport.py` 会报错 `No module named 'petsc4py'`。

然后运行 [教程 1](tutorials/01_tracer_diffusion.ipynb)（需要 FEniCSx，不需要 GEMS）和 [教程 2](tutorials/02_single_equilibrium.ipynb)（需要 GEMS，不需要 FEniCSx），两部分就都检查到了。

## Windows：`Run.cmd`

`Run.cmd` 直接调用环境中的 WSL Python，所以双击即可运行同一文件夹里的 `case.yaml`：

```bat
wsl /home/<user>/miniforge3/envs/fenicsx/bin/python ../../coupling.py "%CASE_FILE%"
```

把 `/home/<user>/miniforge3/envs/fenicsx` 改成你的环境路径（`conda env list` 可以查看）。`Run.cmd other.yaml` 运行另一个输入文件。

## 多进程

当前版本只支持单个 MPI 进程（`transport.py` 会提示 *This version supports one MPI process*）。一维网格很小，运行时间几乎都花在 GEMS 上：每个单元、每个时间步各算一次平衡。
