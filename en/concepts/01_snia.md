# Operator splitting (SNIA)

OGS-GEM does not solve transport and chemistry together. Every time step is split into separate
solves, executed once each — the *sequential non-iterative approach* (SNIA):

```{image} ../figures/snia.png
:width: 100%
```

1. **prepare** — the new porosity of every node is turned into element coefficients (porosity,
   diffusion coefficient, permeability) and boundary values for this time.
2. **flow** (if present) — a steady Darcy problem, with the excess water of the last GEMS step as a source.
3. **transport** — every mobile chemical element is advected and dispersed as a passive solute.
4. **chemistry** — GEMS re-equilibrates every node with the transported amounts.

In the template this is `reactive_transport.run`:

```{literalinclude} ../../GEMS_FEniCSx_OGS5_Template/reactive_transport.py
:language: python
:pyobject: run
```

**Consequences you will meet in the tutorials**

- The splitting error is first order in $\Delta t$. With explicit kinetics this can be large:
  in [HAYEKIT](../tutorials/01_hayekit) OGS's own result is 24 % off the analytical porosity at
  $\Delta t = 100$ s.
- Coefficients lag one step behind: transport in step $n$ uses the porosity from step $n-1$.
- Nothing is iterated, so a node where GEMS fails keeps its old state for the whole step.
