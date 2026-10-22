"""Sequential non-iterative coupling (SNIA) as in OGS5-GEM: flow -> transport -> chemistry.

    for each time step dt:
        prepare(step, t, dt)                  the case sets coefficients / boundary values
        flow.solve(GEMS water source)         if a flow object is given (source from step 2 on)
        after_flow(step, t, dt)               the case may use the new head (e.g. fracture velocities)
        c_tr = transport.step(c[:, mobile])   one solve for all mobile components
        chemistry.react(c_tr, dt)             GEMS at every non-boundary node
        record(step, t, dt)                   the case stores what it wants

The loop knows nothing about the case: all case-specific physics sits in the
prepare() callback (porosity -> element porosity, diffusion and permeability
laws, time-dependent boundary values) and in the options of Transport,
Darcy and OGSGEMS.
"""
import time
import numpy as np
import pandas as pd


def run(chemistry, transport, time_steps, *, flow=None, mobile=None, prepare=None, after_flow=None, record=None,
        water_source=True, node_volume=None, t0=0.0, print_every=10):
    """Run the coupled time loop.

    chemistry    gems_ogs.OGSGEMS (already initialised)
    transport    transport.Transport
    time_steps   iterable of step sizes dt in s
    flow         flow.Darcy or None
    mobile       indices of the transported elements (default: all)
    prepare      prepare(step, t, dt) called first in every step
    after_flow   after_flow(step, t, dt) called after the flow solve, before transport
    record       record(step, t, dt) called last in every step
    water_source add the GEMS excess water (chemistry.water_source) to the flow
                 sources from the second step on, as OGS does ($FLAG_COUPLING_HYDROLOGY 1)
    node_volume  node control volumes for that source (default: the mesh's)

    Returns a DataFrame with one row per step (time, dt, failed / sub-stepped GEMS nodes, wall time).
    """
    mobile = np.arange(chemistry.nIC) if mobile is None else np.asarray(mobile)
    node_volume = transport.mesh.node_volume if node_volume is None else node_volume
    source = None
    t, log, start = t0, [], time.perf_counter()
    for step, dt in enumerate(time_steps, start=1):
        t += dt
        if prepare is not None:
            prepare(step, t, dt)
        if flow is not None:
            flow.solve(source if (water_source and step > 1) else None)
        if after_flow is not None:
            after_flow(step, t, dt)
        c_tr = chemistry.c.copy()
        c_tr[:, mobile] = transport.step(chemistry.c[:, mobile], dt)
        chemistry.react(c_tr, dt)            # Dirichlet nodes are not reacted and keep c_tr
        source = chemistry.water_source(dt, node_volume)
        if record is not None:
            record(step, t, dt)
        log.append(dict(step=step, t=t, dt=dt, wall_s=time.perf_counter() - start, **chemistry.last))
        if print_every and (step % print_every == 0):
            print(f'step {step}, t = {t:.6g} s, GEMS failed {chemistry.last["failed"]}, '
                  f'{time.perf_counter() - start:.0f} s', flush=True)
    return pd.DataFrame(log)
