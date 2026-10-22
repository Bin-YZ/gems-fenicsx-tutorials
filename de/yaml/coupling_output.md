# `coupling` und `output`

## `coupling`

Wird von `coupling.py` gelesen.

```yaml
coupling:
  mode: coupled
  time:
    dt: 3155760          # s (0,1 Jahr)
    end: 63115200        # s (2 Jahre)
  update_porosity: true
  update_diffusivity: true
  exponent: 2.0
```

| Schlüssel | Wert | Bedeutung |
|---|---|---|
| `mode` | `diffusion` / `chemistry` / `coupled` | was läuft, siehe [die drei Modi](../coupling/overview.md) |
| `time.dt` | s, > 0 | Zeitschritt für Transport und Chemie; der letzte Schritt wird gekürzt, um `end` genau zu treffen |
| `time.end` | s, > 0 | Endzeit; im Modus `chemistry` ignoriert |
| `update_porosity` | `true` / `false` | $\phi = \phi_0 + V_\text{solid,0} - V_\text{solid}$ nach jedem Chemieschritt |
| `update_diffusivity` | `true` / `false` | $D_e = D_{e,0}(\phi/\phi_0)^m$; braucht `update_porosity: true` |
| `exponent` | > 0 | $m$ im Gesetz oben; auch nötig, wenn ungenutzt |

Prüfungen beim Start:

- `update_porosity` braucht Chemie und muss im Modus `diffusion` daher `false` sein;
- `update_diffusivity: true` mit `update_porosity: false` wird abgelehnt;
- mit `update_porosity` dürfen Anfangsfeststoffe plus φ das Gesamtvolumen um höchstens 0,1 % überschreiten. Sonst ist φ oder der Feststoffanteil
  des Rezepts zu groß.

Nützliche Umrechnungen: 1 Tag = 86 400 s, 1 Jahr (365,25 d) = 31 557 600 s.

## `output`

Wird von `output.py` gelesen.

```yaml
output:
  folder: results/current     # relativ zu case.yaml; wird bei Bedarf angelegt
  every: 5                    # Profile alle 5 Schritte (und immer am Ende)
```

| Schlüssel | Wert | Bedeutung |
|---|---|---|
| `folder` | Pfad | Ort aller Ergebnisdateien; ein bestehender Ordner wird **überschrieben** |
| `every` | Ganzzahl ≥ 1 | Profile und Felder alle `every` Schritte schreiben; die Massenbilanz in jedem Schritt |

Für jede Variante, die erhalten bleiben soll, einen neuen `folder` verwenden. Der Inhalt des Ordners ist unter
[Ergebnisse und Fehlersuche](../outputs.md) beschrieben.
