# `coupling` and `output`

## `coupling`

Read by `coupling.py`.

```yaml
coupling:
  mode: coupled
  time:
    dt: 3155760          # s (0.1 year)
    end: 63115200        # s (2 years)
  update_porosity: true
  update_diffusivity: true
  exponent: 2.0
```

| key | value | meaning |
|---|---|---|
| `mode` | `diffusion` / `chemistry` / `coupled` | what runs, see [the three modes](../coupling/overview.md#three-modes) |
| `time.dt` | s, > 0 | time step for transport and chemistry; the last step is shortened to hit `end` |
| `time.end` | s, > 0 | end time; ignored in `chemistry` mode |
| `update_porosity` | `true` / `false` | $\phi = \phi_0 + V_\text{solid,0} - V_\text{solid}$ after every chemistry step |
| `update_diffusivity` | `true` / `false` | $D_e = D_{e,0}(\phi/\phi_0)^m$; needs `update_porosity: true` |
| `exponent` | > 0 | $m$ in the law above; required even when unused |

The checks at start-up:

- `update_porosity` needs chemistry, so it must be `false` in `diffusion` mode.
- `update_diffusivity: true` with `update_porosity: false` is rejected.
- With `update_porosity`, the initial solids plus φ must not exceed the bulk volume by more than 0.1 %. If they do, either φ or the
  recipe's solid content is too large.

Handy conversions: 1 day = 86 400 s, 1 year (365.25 d) = 31 557 600 s.

## `output`

Read by `output.py`.

```yaml
output:
  folder: results/current     # relative to case.yaml; created if missing
  every: 5                    # profiles every 5 steps (and always at the end)
```

| key | value | meaning |
|---|---|---|
| `folder` | path | where all result files go; an existing folder is **overwritten** |
| `every` | integer ≥ 1 | write profiles and fields every `every` steps; the mass balance is written every step |

Use a new `folder` for each variant you want to keep. The contents of the folder are described in
[Results and troubleshooting](../outputs.md).
