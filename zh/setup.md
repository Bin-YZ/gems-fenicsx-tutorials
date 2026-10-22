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
