# Transport numerics: element coefficients, mass matrix and FCT

The template uses linear (CG1) finite elements and backward Euler, the same as OGS. Reproducing OGS
node by node needs the same choices in the details:

| detail | OGS rule | template |
|---|---|---|
| element porosity | mean of the node porosities | `element_mean(phi, cells)` |
| element diffusion | harmonic mean of node values (`$DIFFUSION 8/9`) | `harmonic_mean(...)` |
| mass matrix | consistent, or lumped with `ELE_MASS_LUMPING` | `Transport(lumped=...)` |
| dispersion | $\alpha_T|q|I + (\alpha_L-\alpha_T)\,qq^T/|q|$ | `alpha_L`, `alpha_T` |
| quadrature | 3×3 Gauss on quadrilaterals | `quadrature_degree=5` |

## FEM-FCT

With strong advection the Galerkin scheme produces wiggles and negative concentrations; GEMS then gets
negative element amounts. OGS offers flux-corrected transport (`$FEM_FCT 1`, Kuzmin's linearised scheme):
a low-order solution with added discrete diffusion, plus as much of the "anti-diffusive" correction as
the Zalesak limiter allows without creating new extrema.

```{image} ../figures/fct.png
:width: 90%
```

OGS adds the limited flux $+f_{ij}$ to row $j$; the textbook scheme uses $-f_{ij}$ (mass conservative).
`Transport(fct_ogs_sign=True)` copies OGS. In [ConcreteCrack](../tutorials/05_concretecrack) the two
variants cannot be told apart against the OGS reference.
