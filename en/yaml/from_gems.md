# From GEMS-Selektor to a recipe

The chemical system is defined in **GEMS-Selektor**, which holds the database, phases and solution models. The code only reads
the exported **GEMS3K files**. Preparing a new case means:

1. set up the system in GEMS-Selektor and calculate a test equilibrium;
2. export it as GEMS3K input files;
3. turn its bulk composition into an `initial` (and `inlet`) recipe for `case.yaml`.

## 1–2. Export the GEMS3K files

In GEMS-Selektor, calculate the equilibrium of your material, then export the system as GEMS3K input files in **JSON** or
**text** format (binary is not supported by the browser inspector). The export gives four files. Put them in a folder next to `case.yaml`:

```text
my_case/
├── case.yaml
└── chemistry_data/
    ├── mysys-dat.lst          ← chemistry.project points here
    ├── mysys-dch.json         chemical data
    ├── mysys-ipm.json         solver settings
    └── mysys-dbr-0-0000.json  the exported state
```

The `.lst` file only lists the three others, for example `-j "mysys-dch.json" "mysys-ipm.json" "mysys-dbr-0-0000.json"`.
Keep the four files together and do not rename one without editing the `.lst`.

Check the names in the export before writing YAML: open the folder in the [GEMS Chemistry Inspector](../tools/inspector.md)
or run the first cell of [Tutorial 2](../tutorials/02_single_equilibrium.ipynb).

Include every phase that may form during the run, such as secondary minerals. If you want an element to arrive later
through the boundary, it must exist in the system. Give it a trace amount in the recipe.

## 3. Bulk composition → recipe

The exported DBR file stores the bulk element amounts (`bIC`) of the system you calculated, in mol for **that** system. A recipe
must be per **1 dm³ of bulk material** with the right amount of pore water. If the exported system has $V_w$ dm³ of solution and you
want porosity φ, scale all amounts by

$$
f = \frac{\phi}{V_w}
$$

then check that the scaled solid volume plus φ is at most 1 dm³. The rest of the dm³ is inert material.

This script does the scaling and prints YAML you can paste:

```{literalinclude} ../../tools/recipe_from_dbr.py
:language: python
```

For the default project and φ = 0.5:

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

The calcite column of Tutorial 5 was built the same way: a 1 L calcite-saturated solution scaled by 0.31906, so that 1 dm³ bulk
holds 0.32 dm³ pore water.

Two remarks:

- In a **cement** recipe the solids can fill a large part of the dm³ (hydrates + unreacted clinker + aggregate). Only the phases in
  `solid_phases` count for the porosity update. Everything else is inert.
- Some projects use **independent components** other than elements, e.g. water as `H2` without `O`. Use whatever names the project
  lists as elements. The calcite example has no `O`.

## The inlet solution

For `inlet`, export or calculate the boundary water as its own GEMS system, typically about 1 kg of water with the dissolved salts,
and copy its `bIC` without scaling. The code equilibrates it and divides by the solution volume. For example, a 14.6 mM CaCl₂
solution:

```yaml
inlet:
  Ca: 0.01460
  Cl: 0.02919801532501
  H: 111.0167489181          # 55.5 mol H2O
  O: 55.508741415148
  Si: 0.000183
```

If the inlet water should be in equilibrium with a material, for example clay pore water entering cement, use the zone-name form
`inlet: clay` instead. The code then equilibrates that zone's recipe and uses its pore water.

## Browser alternative

[Case Builder](../tools/case_builder.md) loads the exported folder, offers the element and phase names as you type, and writes the
YAML. Use it for single-material diffusion cases. Zones, flow and per-side inlets are edited by hand.
