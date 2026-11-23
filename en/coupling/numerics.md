# Equations and numerics

## Transport equation

The equation below is the **transport substep** of the operator splitting. During this substep reactions are excluded and porosity
is held fixed. The full equation for a dissolved element also has a reaction source term $R$ (dissolution minus precipitation),
$\partial(\phi c)/\partial t + \partial_x(qc - D_e\partial_x c) = R$. The code does not discretise $R$: the chemistry substep that follows
replaces it by a local equilibrium in every cell ([how the coupling works](overview.md)).

In the transport substep, for each transported element, with $c$ in mol/m³ pore water,

$$
\frac{\partial(\phi c)}{\partial t} + \frac{\partial}{\partial x}\!\left(q\,c - D_e \frac{\partial c}{\partial x}\right) = 0,
\qquad 0 < x < L
$$

| symbol | `case.yaml` key | unit |
|---|---|---|
| $\phi$ | `transport.material.phi` (or per zone), then updated by the feedback | – |
| $D_e$ | `transport.material.De` (or per zone), then updated by the feedback | m²/s |
| $q$ | `transport.material.darcy_flux` (Darcy flux $=\phi \times$ pore velocity, towards $+x$) | m/s |
| $L$ | `transport.geometry.length` | m |

$D_e$ is the **effective** coefficient in the flux. The pore diffusion coefficient is $D_p = D_e/\phi$. The same $D_e$
is used for all elements. Electromigration is not included.

## Discretisation

- **Space: DG0 finite volumes on a uniform mesh.** `transport.geometry.cells` cells of width $h = L/n$ hold one value each.
  The diffusive flux between two cells uses the harmonic mean of their $D_e$,
  $D_\text{face} = 2D_e^+D_e^-/(D_e^+ + D_e^-)$. A Dirichlet boundary sits $h/2$ from the centre of the first cell.
- **Advection: first-order upwind.** Each cell sends $q\,c$ out through its downstream face. Upwinding is stable and never produces
  negative values, but it smears sharp fronts by a numerical dispersion of about $q h / 2$. Use fine meshes for advective problems.
- **Time: backward Euler.** It is unconditionally stable and first-order accurate. `coupling.time.dt` is the only time step;
  transport and chemistry use the same one.
- **Linear solver: PETSc**, configured by `transport.solver`. The default `preonly` + `lu` is a direct solve and is the right
  choice for 1D.

The weak form in `transport.py` with DG0 test functions $v$ is

$$
\int \phi\,\frac{c^{n+1}-c^n}{\Delta t}\,v\,dx
+ \sum_\text{faces} D_\text{face}\,\frac{[c^{n+1}]\,[v]}{h}
+ \text{upwind and boundary terms} = 0 .
$$

## Porosity and diffusivity feedback

With `coupling.update_porosity: true`, porosity follows the volume of the minerals in `chemistry.solid_phases`:

$$
\phi = \phi_0 + V_\text{solid,0} - V_\text{solid}
$$

$V_\text{solid}$ is the volume fraction of those phases from GEMS, and $V_\text{solid,0}$ is its value after the initial equilibrium.
Dissolution opens pores and precipitation closes them. Material not represented by a GEMS phase is inert and never changes.
A porosity outside $(0, 1]$ stops the run.

With `coupling.update_diffusivity: true` as well:

$$
D_e = D_{e,0}\left(\frac{\phi}{\phi_0}\right)^{m}, \qquad m = \texttt{coupling.exponent}
$$

This is an Archie-type law. The exponent is prescribed, not fitted. When φ changes, the dissolved **amounts** per bulk volume are kept,
so concentrations are recalculated as $c = \text{aqueous}/\phi$.

## Time-step choice

Operator splitting adds an error that grows with $\Delta t$, on top of the backward-Euler error.

- **Diffusion-dominated:** $\sqrt{D_p\,\Delta t}$ is the diffusion length of one step. It is a length scale, not the distance a mineral front moves
  per step, which also depends on how much mineral has to dissolve or precipitate. If $\sqrt{D_p\,\Delta t}$ is much larger than the cell width $h$,
  concentration gradients change a lot within one step and splitting errors grow.
- **Advection-dominated:** keep the Courant number $q\,\Delta t / (\phi h)$ around 1 or below. Backward Euler stays stable at larger values,
  but fronts are smeared further.
- **Check time and space separately.** On a fine mesh, run with `dt`, `dt/2` and `dt/4` until the profiles stop changing. Then, with that time step,
  refine `cells` until the profiles stop changing again. Halving `dt` and doubling `cells` at the same time only shows the combined effect and
  cannot tell which error dominates.

## Chemistry: cold and warm starts

GEMS minimises the Gibbs energy of each cell's system. By default (`chemistry.start: cold`) every call starts from scratch, so the
result does not depend on the previous step or on neighbouring cells. If GEMS reports a poor element balance, the same system is solved
again at a scaled size (×1, ×10, ×100, ×0.1, ×0.01) and scaled back. Equilibrium does not depend on system size.

`start: warm` gives each cell its own GEMS engine and starts from that cell's previous equilibrium. This is faster and more robust
for large systems. If a warm start fails, the cell is re-solved at its previous composition and moved to the new one in four warm
steps before falling back to cold starts.

GEMS results are not exactly reproducible at the level of round-off. In the tested examples, two runs whose inputs differed only in
the last digit gave relative differences of up to about 1e-5 in concentrations. This is an observation for these examples, not a general bound: the size
depends on the system, the solver tolerances, and whether phases appear or disappear. See
[small differences between runs](../outputs.md) for how to judge such differences.
