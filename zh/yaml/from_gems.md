# 从 GEMS-Selektor 到配方

化学体系在 **GEMS-Selektor** 中定义，数据库、相和溶液模型都在那里。代码只读取导出的 **GEMS3K 文件**。准备一个新算例需要：

1. 在 GEMS-Selektor 中建立体系，计算一次试验平衡；
2. 导出为 GEMS3K 输入文件；
3. 把它的总组成转换为 `case.yaml` 中的 `initial`（和 `inlet`）配方。

## 1–2. 导出 GEMS3K 文件

在 GEMS-Selektor 中计算材料的平衡，然后把体系导出为 **JSON** 或 **文本** 格式的 GEMS3K 输入文件（浏览器检查工具不支持二进制格式）。导出得到四个文件，把它们放在 `case.yaml` 旁边：

```text
my_case/
├── case.yaml
└── chemistry_data/
    ├── mysys-dat.lst          ← chemistry.project 指向这里
    ├── mysys-dch.json         化学数据
    ├── mysys-ipm.json         求解器设置
    └── mysys-dbr-0-0000.json  导出的状态
```

`.lst` 文件只列出另外三个文件，例如 `-j "mysys-dch.json" "mysys-ipm.json" "mysys-dbr-0-0000.json"`。四个文件要放在一起；改名时要同时修改 `.lst`。

写 YAML 之前先检查导出的名称：用 [GEMS Chemistry Inspector](../tools/inspector.md) 打开文件夹，或运行 [教程 2](../tutorials/02_single_equilibrium.ipynb) 的第一个代码单元。

把运行中可能生成的所有相（例如次生矿物）都包含进去。若希望某元素以后从边界进入，它必须存在于体系中，在配方里给一个痕量即可。

## 3. 总组成 → 配方

导出的 DBR 文件保存了所算体系的元素总量（`bIC`），单位是 **该体系** 的 mol。配方则要按 **每 1 dm³ 体相材料** 给出，并含正确的孔隙水量。若导出的体系含 $V_w$ dm³ 溶液、你想要孔隙率 φ，把所有量乘以

$$
f = \frac{\phi}{V_w}
$$

然后检查缩放后的固相体积加 φ 不超过 1 dm³，剩下的部分是惰性物质。

下面的脚本完成缩放，并打印可直接粘贴的 YAML：

```{literalinclude} ../../tools/recipe_from_dbr.py
:language: python
```

默认项目、φ = 0.5 时：

```text
$ python recipe_from_dbr.py chemistry_data/b_time0-dat.lst 0.5
# stored system: 0.5012 dm3 solution, 0.0482 dm3 other phases, pH 12.47
# scaled by 0.99752: solids take 0.048 of 1 dm3 bulk (phi + solids must be <= 1)
initial:
  Ca: 1.11644400166
  Cl: 1e-15
  H: 58.3771472977
  O: 30.9235097918
  Si: 0.309345822605
```

教程 5 的方解石柱也是这样得到的：1 L 方解石饱和溶液乘以 0.31906，使 1 dm³ 体相含 0.32 dm³ 孔隙水。

两点说明：

- **水泥** 配方中固相可能占 1 dm³ 的很大一部分（水化产物 + 未反应熟料 + 骨料）。只有 `solid_phases` 中的相计入孔隙率更新，其余都是惰性的。
- 有些项目的独立组分不是元素，例如用 `H2` 表示水而没有 `O`。使用项目列出的名称即可，方解石示例中就没有 `O`。

## 入口溶液

`inlet` 的边界水可以单独作为一个 GEMS 体系导出或计算，通常是约 1 kg 水加上溶解的盐，直接复制它的 `bIC`，不必缩放。程序会平衡它并除以溶液体积。例如 14.6 mM 的 CaCl₂ 溶液：

```yaml
inlet:
  Ca: 0.01460
  Cl: 0.02919801532501
  H: 111.0167489181          # 55.5 mol H2O
  O: 55.508741415148
  Si: 0.000183
```

若入口水应与某种材料平衡（例如进入水泥的黏土孔隙水），改用分区名写法 `inlet: clay`，程序会平衡该分区的配方并使用其孔隙水。

## 浏览器方式

[Case Builder](../tools/case_builder.md) 可以加载导出的文件夹，输入时提示元素和相名，并生成 YAML。它适用于单一材料的扩散算例；分区、流动和两侧不同的入口溶液需要手动编辑。
