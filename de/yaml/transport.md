# `transport`: Gitter, Material, Ränder

Wird von `transport.py` gelesen. Im Modus `chemistry` nicht verwendet; dort dient nur `geometry.length` als Bezugslänge.

```yaml
transport:
  geometry: {length: 0.004, cells: 40}
  material: {phi: 0.5, De: 5.0e-15}          # + darcy_flux für Advektion
  zones: [...]                               # optional
  components: [tracer]                       # nur Modus diffusion
  initial: {tracer: 0.0}                     # nur Modus diffusion
  boundary:
    left:  {type: dirichlet, concentrations: {tracer: 1.0}}
    right: {type: no_flux,   concentrations: {tracer: 0.0}}
  solver: {ksp_type: preonly, pc_type: lu, rtol: 1.0e-10, max_iterations: 1000}
```

## `geometry`

| Schlüssel | Wert | Bedeutung |
|---|---|---|
| `length` | m, > 0 | Säulenlänge; x läuft von 0 (links) bis `length` (rechts) |
| `cells` | Ganzzahl ≥ 1 | Anzahl gleich großer Zellen; $h$ = length / cells |

Die Rechenzeit wächst linear mit `cells`, weil GEMS einmal pro Zelle und Schritt aufgerufen wird.

## `material`

| Schlüssel | Wert | Bedeutung |
|---|---|---|
| `phi` | 0 < φ ≤ 1 | Anfangsporosität |
| `De` | m²/s, > 0 | effektiver Anfangsdiffusionskoeffizient (Fluss $= -D_e\,\partial_x c$) |
| `darcy_flux` | m/s, ≥ 0, optional | Darcy-Fluss $q = \phi v$ in $+x$-Richtung; weglassen oder 0 für reine Diffusion |

Mit `darcy_flux > 0` muss der linke Rand `dirichlet` (Zustrom) und der rechte `outflow` oder `dirichlet` sein.

## Zonen

Zonen teilen die Säule in Materialien mit eigenem φ und De und, über `chemistry.initial`, eigenem Rezept:

```yaml
transport:
  zones:
    - {name: clay,   from: 0.0,  to: 0.25, phi: 0.51, De: 5.1e-10}
    - {name: cement, from: 0.25, to: 0.5,  phi: 0.52, De: 5.2e-10}
```

| Schlüssel | Bedeutung |
|---|---|
| `name` | eindeutiger Zonenname, verwendet von `chemistry.initial` und `chemistry.inlet` |
| `from`, `to` | m; eine Zelle gehört zur Zone, wenn ihr **Mittelpunkt** in `[from, to)` liegt; Standard 0 und `length` |
| `phi`, `De` | optional; sonst `material.phi` / `material.De` |

Jede Zone muss mindestens einen Zellmittelpunkt enthalten. Zellen außerhalb aller Zonen behalten die Werte aus `material`. Der Diffusionskoeffizient
zwischen zwei Zonen ist das harmonische Mittel der beiden Zellen.

## `boundary`

`left` (x = 0) und `right` (x = length) haben je einen `type`:

| Typ | Bedingung | im Modus `coupled` |
|---|---|---|
| `dirichlet` | Porenwasser am Rand hat eine feste Zusammensetzung; diffusiver (mit Strömung auch advektiver) Austausch | Zusammensetzung aus `chemistry.inlet` |
| `no_flux` | nichts geht hindurch | – |
| `outflow` | Wasser verlässt die Säule advektiv mit der Zusammensetzung der Zelle; diffusiver Gradient null | für das stromabwärtige Ende mit `darcy_flux` |

`concentrations` (mol/m³ Porenwasser, ein Wert pro Tracer) wird **nur im Modus diffusion** an `dirichlet`-Rändern verwendet. Im Modus coupled nimmt
jeder Dirichlet-Rand `chemistry.inlet`, und diese Werte werden ignoriert.

## Tracer: `components` und `initial` (Modus diffusion)

```yaml
components: [tracer, salt]           # beliebige Namen außer Zz
initial: {tracer: 0.0, salt: 0.5}    # mol/m3 Porenwasser, für jede Komponente
```

In den Modi `coupled` und `chemistry` sind die transportierten Namen die GEMS-Elemente, und beide Schlüssel werden ignoriert.

## `solver`

| Schlüssel | Wert in den Beispielen | Bedeutung |
|---|---|---|
| `ksp_type` | `preonly` | PETSc-Krylov-Verfahren; `preonly` = Vorkonditionierer einmal anwenden |
| `pc_type` | `lu` | PETSc-Vorkonditionierer; `lu` = direkte Zerlegung |
| `rtol` | `1.0e-10` | relative Toleranz (iterative Verfahren) |
| `max_iterations` | `1000` | Iterationsgrenze (iterative Verfahren) |

Für 1D-Gitter `preonly` + `lu` beibehalten. Ein Transportschritt, der nicht konvergiert oder eine Konzentration unter −1e-12 mol/m³ liefert, beendet den Lauf.
