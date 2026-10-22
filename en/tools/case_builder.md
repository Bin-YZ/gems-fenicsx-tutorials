# Case Builder

`case_builder.html` is a form for the four sections of `case.yaml`. As you edit it shows a live YAML preview, checks basic values
and the chemical names, and lets you **Copy** or **Download** the result. It runs entirely in your browser, and nothing is uploaded.

<p><a href="../_static/tools/case_builder.html" target="_blank" rel="noopener">Open Case Builder in its own tab ↗</a></p>

<iframe src="../_static/tools/case_builder.html" title="Case Builder" style="width:100%;height:900px;border:1px solid #d9dfdb;border-radius:6px"></iframe>

## How to use it

1. Start from the built-in example or use **Import case.yaml** to load an existing case.
2. Under *Chemistry*, click **Choose GEMS folder** and select the folder with the exported `.lst` and its DCH file (`.json` or text `.dat`).
   The element, phase and species names then come from your project. Check that `chemistry.project` is relative to where you will save `case.yaml`.
3. Fill in recipes, temperature, pressure, phases and optional Gibbs energies. Then fill in geometry, porosity, diffusivity, boundaries,
   solver, mode, time and feedback. Time units chosen in the form are converted to seconds.
4. Read the validation messages, **Download**, put `case.yaml` next to your chemistry data and run `python coupling.py case.yaml`.

## Limits

The form covers the basic single-material diffusion case. It does **not** handle zones, `darcy_flux`, `outflow` boundaries,
per-side `inlet` or `start`/`on_failure`, and does not reliably keep them when you import and export a file that has them. Edit those
by hand using the [`case.yaml` reference](../yaml/index.md). The page prepares input. It does not run GEMS or check that a recipe converges.
Use `mode: chemistry` for that ([Tutorial 2](../tutorials/02_single_equilibrium.ipynb)).
