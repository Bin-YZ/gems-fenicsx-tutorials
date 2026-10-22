# What is transported: element totals of the pore water

GEMS describes a system by the total amounts of its **independent components** — chemical elements plus
charge (`Zz`) — the *b vector*. OGS-GEM transports exactly these totals, but only the part dissolved in
the pore water (`$TRANSPORT_B 1`):

```{image} ../figures/bvector.png
:width: 100%
```

After each GEMS calculation a node's b vector is split into

- `b_fix` — everything in solids (and gas): stays at the node,
- the pore water — solutes **plus the solvent water**: the H and O of H₂O are removed before transport
  and added back afterwards, so the transported concentration of H and O is only the part in solutes.

Why element totals and not species? There are far fewer elements than species (16 vs 157 in
TransLay2d), the totals are conserved by transport, and the solution stays electroneutral without
transporting charge. The price: all species of an element move with the same diffusion coefficient.

The charge `Zz` is never transported and is set to zero before GEMS. Inert components (e.g. `Inrt`, `Sn`)
can be excluded from transport with the `mobile` argument of `run`.
