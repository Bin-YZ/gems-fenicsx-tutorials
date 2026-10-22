"""GEMS chemistry at every mesh node with the OGS5-GEM coupling rules (sources/FEM/rf_REACT_GEM.cpp).

One chemical system per OGS node. All state is kept in NumPy arrays in OGS
node order (rows) and GEMS order (columns):

    c       (n, nIC)  transport concentration, mol / m3 fluid; solvent water H, O removed
                      (hydrology='none': total aqueous amounts incl. water)
    b_fix   (n, nIC)  element amounts of all non-aqueous phases, mol per m3 node volume
    water   (n,)      solvent H2O@ amount in the (scaled) fluid, mol
    Vf      (n,)      fluid volume the concentrations refer to, m3
    phi     (n,)      porosity  (OGS CalcPorosity: 1 - sum of solid phase volumes)
    x, dll, dul (n, nDC)  species amounts and the kinetic lower / upper limits passed to GEMS
    omega, dmdt (n, nkin) saturation and rate of each kinetic phase (mol/s, > 0 precipitation)
    excess  (n,)      GEMS aqueous volume - porosity, m3: OGS turns it into a flow source
    pH      (n,)

One time step at a node (react):
    ConcentrationToMass -> [CalcLimits -> GEMS -> CalcPorosity -> CalcReactionRate] (sub-steps)
    -> MassToConcentration;  a failed node keeps its old state (OGS RestoreOldSolution)

Where OGS versions / cases differ, the behaviour is an option of the constructor;
the case scripts say which setting their OGS input implies.

    hydrology   'full'    $FLAG_COUPLING_HYDROLOGY 1: whole aqueous phase scaled to the pore volume
                'hayekit' only the solvent water scaled ($FLAG_HAYEKIT)
                'none'    no scaling, c = aqueous amounts / aqueous volume, b = b_fix + c * phi
    kinetics    list of Kinetic(...) (OGS $KINETIC_GEM, single-species phases)
"""
from dataclasses import dataclass
import re
from pathlib import Path
import numpy as np
import xgems


@dataclass
class Kinetic:
    """One kinetically controlled single-species phase (OGS $KINETIC_GEM).

    rate dm/dt = -A * sum_m 10**logk[m] * a_H+**n_H[m] * (1 - Omega)     (mol/s, > 0 precipitation)

    area_model  1: A = area * V_phase          (m2/m3 of mineral)
                3: A = area * V_phase / phi
                4: A = area * phi              (HAYEKIT)
    """
    species: str
    logk: tuple = (0.0,)
    n_H: tuple = (0.0,)
    area_model: int = 1
    area: float = 0.0


class OGSGEMS:
    def __init__(self, gems_lst, n_nodes, *, T=298.15, P=1.0e5, hydrology='full',
                 min_porosity=1e-6, max_porosity=1.0, solid_phases=None, kinetics=(),
                 accept=(2,), retry=False, warm_start=False, limits='loose', seed_omega=1.0001,
                 seed_needs_rate=False, check_lower_limits=False, substep_kinetics=False,
                 retry_widen=None, retry_perturb=None, boundary_nodes=(), max_failed=None):
        """
        gems_lst            GEMS3K *-dat.lst (the OGS GEMS files, unchanged)
        n_nodes             number of OGS nodes
        hydrology           'full' | 'hayekit' | 'none' (see module docstring)
        min/max_porosity    $MIN_POROSITY / $MAX_POROSITY
        solid_phases        phases counted in CalcPorosity; default: all phases that are not
                            aqueous or gaseous according to the DCH ccPH codes
        kinetics            Kinetic(...) list
        accept              GEMS return codes accepted as converged (2 = OK_GEM_AIA, 6 = OK_GEM_SIA)
        retry               try once more with a cold start before declaring a node failed
        warm_start          one GEMS engine per node, warm-started from its own last solution
                            (otherwise one engine, cold start every call, like OGS NEED_GEM_AIA)
        limits              'loose' keeps the current amount as the second bound of the kinetic
                            window ($LOOSE_KINETICS 1), 'strict' pins both bounds to the kinetic target
        seed_omega          a phase absent (x < 1e-6) but supersaturated (Omega >= seed_omega)
                            is allowed 1e-6 mol (OGS 2013–2015: 1.0001, OGS 2017: 1.1)
        seed_needs_rate     seed only if the rate is non-zero (OGS 2017)
        check_lower_limits  shrink the lower limits if they would need more of an element than
                            the node contains (OGS 2017 CheckConstraints)
        substep_kinetics    split dt so that a kinetic phase changes an element by <= 10 %
                            per sub-step (OGS MaxDtKinetics); a failed sub-step keeps the old rates,
                            the node fails only if the last sub-step failed (OGS 2017 SolveChemistry)
        retry_widen         (f_lower, f_upper): on failure multiply dll, dul by these factors and
                            run GEMS once more (OGS 2015: 0.999999, 1.000001)
        retry_perturb       not in OGS: on failure run GEMS once more with b * (1 + retry_perturb),
                            e.g. 1e-12. Some GEMS3K failures are triggered by round-off alone (the
                            same node converges with b changed in the 12th digit); this keeps such
                            a node from being frozen for a whole step
        boundary_nodes      Dirichlet transport nodes; not reacted ($CALCULATE_BOUNDARY_NODES 0)
        max_failed          raise if more nodes fail in one step (None: never)
        """
        self.lst = str(Path(gems_lst).resolve())
        g = xgems.ChemicalEngine(self.lst)
        self.engine = g
        self.n, self.T, self.P = n_nodes, T, P
        dch = Path(self.lst).with_name(Path(self.lst).name.replace('-dat.lst', '-dch.dat'))
        dch = dch.read_text(encoding='latin-1') if dch.exists() else None
        # names are read from the DCH file as Latin-1 (some GEMS databases use e.g. 'strätlingite',
        # which xgems cannot decode); fall back to xgems for JSON-format projects
        self.elements = _dch_list(dch, 'ICNL') or [g.elementName(i) for i in range(g.numElements())]
        self.species = _dch_list(dch, 'DCNL') or [g.speciesName(i) for i in range(g.numSpecies())]
        self.phases = _dch_list(dch, 'PHNL') or [g.phaseName(i) for i in range(g.numPhases())]
        assert (len(self.elements), len(self.species), len(self.phases)) == (g.numElements(), g.numSpecies(), g.numPhases())
        self.nIC, self.nDC, self.nPH = len(self.elements), len(self.species), len(self.phases)
        self.iH, self.iO = self.elements.index('H'), self.elements.index('O')
        self.not_charge = np.array([e != 'Zz' for e in self.elements])
        self.s_water = self.species.index('H2O@')
        self.p_aq = 0
        a0 = g.indexFirstSpeciesInPhase(self.p_aq)
        self.aq_species = np.arange(a0, a0 + g.numSpeciesInPhase(self.p_aq))
        self.s_Hplus = self.species.index('H+') if 'H+' in self.species else None
        self.formula = np.asarray(g.formulaMatrix()).T                 # (species, elements)
        if solid_phases is None:
            codes = _dch_list(dch, 'ccPH')
            solid_phases = [p for p, cc in zip(self.phases, codes) if cc not in ('a', 'g', 'p', 'f')]
        self.solid = [self.phases.index(p) for p in solid_phases]
        self.hydrology, self.phi_min, self.phi_max = hydrology, min_porosity, max_porosity
        self.kin = list(kinetics)
        self.kin_species = [self.species.index(k.species) for k in self.kin]
        self.kin_phase = [g.indexPhaseWithSpecies(s) for s in self.kin_species]
        self.accept, self.retry, self.warm = tuple(accept), retry, warm_start
        self.limits, self.seed_omega, self.seed_needs_rate = limits, seed_omega, seed_needs_rate
        self.check_lower, self.substep, self.max_failed = check_lower_limits, substep_kinetics, max_failed
        self.retry_widen, self.retry_perturb = retry_widen, retry_perturb
        self.boundary = np.zeros(n_nodes, bool)
        self.boundary[np.asarray(boundary_nodes, int)] = True
        self.engines = [xgems.ChemicalEngine(self.lst) for _ in range(n_nodes)] if warm_start else None
        n, nk = n_nodes, len(self.kin)
        self.c = np.zeros((n, self.nIC)); self.b_fix = np.zeros((n, self.nIC))
        self.water, self.Vf, self.phi = np.zeros(n), np.zeros(n), np.zeros(n)
        self.x = np.zeros((n, self.nDC))
        self.dll = np.tile(np.asarray(g.speciesLowerLimits(), float), (n, 1))
        self.dul = np.tile(np.asarray(g.speciesUpperLimits(), float), (n, 1))
        self.omega, self.dmdt = np.zeros((n, nk)), np.zeros((n, nk))
        self.excess, self.pH, self.status = np.zeros(n), np.zeros(n), np.zeros(n, int)
        self.last = {}                                                  # diagnostics of the last react()
        self._good = {}                                                 # last good GEMS output per node

    # ------------------------------------------------------------------ GEMS call
    def _engine(self, i):
        return self.engines[i] if self.warm else self.engine

    def _equilibrate(self, i, b, cold=None):
        g = self._engine(i)
        g.setSpeciesLowerLimits(self.dll[i])
        g.setSpeciesUpperLimits(self.dul[i])
        if cold or not self.warm:
            g.setColdStart()
        else:
            g.setWarmStart()
        status = g.equilibrate(self.T, self.P, b)
        if status not in self.accept and self.retry:
            g.setColdStart()
            status = g.equilibrate(self.T, self.P, b)
        self.status[i] = status
        return status in self.accept

    # ------------------------------------------------------------------ OGS coupling functions
    def concentration_to_mass(self, i):
        """OGS ConcentrationToMass: total b vector of node i from c, Vf, water and b_fix."""
        solute = self.c[i] * self.Vf[i]
        solute[self.not_charge] = np.abs(solute[self.not_charge])
        solute[self.iH] += 2.0 * self.water[i]
        solute[self.iO] += self.water[i]
        b = self.b_fix[i] + solute                      # same order of the sums as OGS
        nc = self.not_charge
        b[nc] = np.where(b[nc] <= 0.0, 1e-16, b[nc])
        b[~nc] = 0.0
        return b, solute

    def after_gems(self, i, update_porosity=True):
        """OGS CalcPorosity + CalcReactionRate for node i (engine holds the new solution)."""
        g = self._engine(i)
        vol = np.asarray(g.phaseVolumes()).copy()
        # keep this GEMS solution: MassToConcentration uses the last good one (OGS GetReactInfoFromGEM)
        self._good[i] = dict(vol=vol, b_aq=np.asarray(g.elementAmountsInPhase(self.p_aq)).copy(),
                             b_tot=np.asarray(g.elementAmounts()).copy(), x=np.asarray(g.speciesAmounts()).copy())
        if update_porosity:
            self.phi[i] = np.clip(1.0 - vol[self.solid].sum(), self.phi_min, self.phi_max)
        self.x[i] = self._good[i]['x']
        if self.kin:
            lna = np.asarray(g.lnActivities())
            aH = np.exp(lna[self.s_Hplus]) if self.s_Hplus is not None else 1.0
            for k, (kin, s, p) in enumerate(zip(self.kin, self.kin_species, self.kin_phase)):
                self.omega[i, k] = np.exp(lna[s])
                area = {1: kin.area * vol[p], 3: kin.area * vol[p] / self.phi[i], 4: kin.area * self.phi[i]}[kin.area_model]
                k_sum = sum(10.0 ** lk * aH ** nh for lk, nh in zip(kin.logk, kin.n_H))
                self.dmdt[i, k] = -area * k_sum * (1.0 - self.omega[i, k])
        self.pH[i] = g.pH()

    def mass_to_concentration(self, i):
        """OGS MassToConcentration: split node i into b_fix + fluid, scale the fluid, new c."""
        r = self._good[i]
        self.x[i] = r['x']
        V_aq = r['vol'][self.p_aq]
        b_aq = r['b_aq'].copy()
        self.b_fix[i] = r['b_tot'] - b_aq
        self.excess[i] = V_aq - self.phi[i]
        s = self.phi[i] / V_aq
        if self.hydrology == 'none':
            self.c[i] = b_aq / V_aq
            self.x[i, self.aq_species] *= s                            # for output only
            self.water[i], self.Vf[i] = 0.0, self.phi[i]
            return
        if self.hydrology == 'full':
            self.x[i, self.aq_species] *= s
            b_aq *= s
        elif self.hydrology == 'hayekit':
            self.x[i, self.s_water] *= s
            b_aq[self.iH] *= s
            b_aq[self.iO] *= s
        else:
            raise ValueError(self.hydrology)
        self.water[i] = self.x[i, self.s_water]
        self.Vf[i] = V_aq * s
        b_aq[self.iH] -= 2.0 * self.water[i]
        b_aq[self.iO] -= self.water[i]
        self.c[i] = b_aq / self.Vf[i]

    def check_lower_limits(self, i, b):
        """OGS CheckConstraints: lower limits may not need more of an element than b holds."""
        need = self.dll[i] @ self.formula
        nc = self.not_charge
        bad = need[nc] > b[nc]
        if bad.any():
            self.dll[i] /= np.max(need[nc][bad] / b[nc][bad]) * 1.000000001
            self.dll[i] = np.maximum(self.dll[i], 0.0)
            fix = self.dll[i] >= self.dul[i]
            self.dul[i][fix] = self.dll[i][fix] * 1.000000001

    def calc_limits(self, i, dt):
        """OGS CalcLimits for single-species kinetic phases: move the window by dm/dt * dt."""
        for k, j in enumerate(self.kin_species):
            change = self.dmdt[i, k] * dt
            x = self.x[i, j]
            if change <= 0.0:
                self.dll[i, j] += change
                self.dul[i, j] = x if self.limits == 'loose' else self.dll[i, j]
            else:
                self.dul[i, j] += change
                self.dll[i, j] = x if self.limits == 'loose' else self.dul[i, j]
            if x < 1e-6 and self.omega[i, k] >= self.seed_omega and self.dul[i, j] < 1e-6 \
                    and (change != 0.0 or not self.seed_needs_rate):
                self.dul[i, j] = self.dll[i, j] = 1e-6
            if self.dul[i, j] <= 0.0:
                self.dul[i, j] = self.dll[i, j] = 0.0
            self.dll[i, j] = min(max(self.dll[i, j], 0.0), self.dul[i, j])
            self.x[i, j] = min(max(x, self.dll[i, j]), self.dul[i, j])

    def kinetic_dt(self, i, solute, dt):
        """OGS MaxDtKinetics (kept as written there: returns the last value computed)."""
        smallest, last = dt, dt
        for k, j in enumerate(self.kin_species):
            for e in range(self.nIC):
                change = abs(self.dmdt[i, k] * self.formula[j, e])
                if solute[e] > 0.0 or change > 0.0:
                    last = 0.1 * solute[e] / change if change > 0.0 else np.inf
                    smallest = min(smallest, last)
        return last if smallest > 1e-3 else 1e-3

    # ------------------------------------------------------------------ initialisation
    def init_from_bulk(self, b_init, normalize=True, lower=None, upper=None, pin=(), big=1.0e6):
        """Start from total b vectors per node (OGS .ic, no restart).

        b_init (n, nIC) or (nIC,); lower/upper optional species limits (n, nDC).
        normalize=True is OGS's two-pass start: equilibrate, divide b (and the
        limits below `big`) by the system volume, equilibrate again, so that each
        node holds exactly 1 m3. Species in `pin` (kinetic phases) are fixed to
        their first-pass amount (OGS SetLimitsInitial)."""
        b_init = np.broadcast_to(b_init, (self.n, self.nIC))
        if lower is not None:
            self.dll[:] = lower
        if upper is not None:
            self.dul[:] = upper
        pin = [self.species.index(s) for s in pin]
        for i in range(self.n):
            b = b_init[i].copy()
            assert self._equilibrate(i, b, cold=True), f'initial GEMS run failed at node {i}: {self.status[i]}'
            if normalize:
                g = self._engine(i)
                Vs = g.systemVolume()
                xs = np.asarray(g.speciesAmounts())
                for j in pin:
                    self.dll[i, j] = self.dul[i, j] = xs[j]
                b /= Vs
                self.dll[i] /= Vs
                self.dul[i] = np.where(self.dul[i] >= big, self.dul[i], self.dul[i] / Vs)
                assert self._equilibrate(i, b, cold=True), f'second initial GEMS run failed at node {i}'
            self.after_gems(i)
            self.mass_to_concentration(i)
        self.phi0 = self.phi.copy()

    def init_from_restart(self, restart, c, nodes=None, update_porosity=False, pin_kinetic=False):
        """Start from OGS restart files (ogs_io.read_restart) and the transport restart values c.

        For `nodes` (default all) one GEMS run with the stored limits follows
        (OGS Init with $RELOAD >= 2: no V_s normalisation; CalcPorosity only if
        update_porosity). pin_kinetic fixes the kinetic species to the new
        amounts afterwards (SetLimitsInitial of the comedy-era code)."""
        self.b_fix[:] = restart['b_fix']
        self.c[:] = c
        self.x[:] = restart['xDC']
        self.dll[:], self.dul[:] = restart['dll'], restart['dul']
        self.phi[:], self.Vf[:] = restart['porosity'], restart['fluid_volume']
        self.water[:] = restart['xDC'][:, self.s_water]
        self.phi0 = self.phi.copy()
        for i in (range(self.n) if nodes is None else nodes):
            b, _ = self.concentration_to_mass(i)
            if not self._equilibrate(i, b, cold=True):
                self._equilibrate(i, b, cold=True)        # OGS repeats a failed restart run once
            if pin_kinetic:
                xs = np.asarray(self._engine(i).speciesAmounts())
                for j in self.kin_species:
                    self.dll[i, j] = self.dul[i, j] = max(xs[j], 0.0)
            self.after_gems(i, update_porosity)
            self.mass_to_concentration(i)

    # ------------------------------------------------------------------ one time step
    def react(self, c_transport, dt):
        """Chemistry for all non-boundary nodes after transport produced c_transport (n, nIC)."""
        self.c[:] = c_transport
        n_fail = n_split = 0
        keep = ('b_fix', 'x', 'dll', 'dul', 'phi', 'Vf', 'water', 'omega', 'dmdt', 'excess')
        for i in np.flatnonzero(~self.boundary):
            saved = {k: np.copy(getattr(self, k)[i]) for k in keep}
            b, solute = self.concentration_to_mass(i)
            if self.check_lower:
                self.check_lower_limits(i, b)
            n_sub = 1
            if self.kin and self.substep:
                dt_kin = self.kinetic_dt(i, solute, dt)
                n_sub = int(min(max(dt / dt_kin, 1), 100000)) if dt_kin < dt else 1
            n_split += n_sub > 1
            dt_chem, sub_t, ok = dt / n_sub, 0.0, False
            while sub_t <= dt:
                if self.kin:
                    self.calc_limits(i, dt_chem)
                    if self.check_lower:
                        self.check_lower_limits(i, b)
                ok = self._equilibrate(i, b)
                if not ok and self.retry_perturb:
                    ok = self._equilibrate(i, b * (1.0 + self.retry_perturb))
                if not ok and self.retry_widen is not None:
                    self.dll[i] *= self.retry_widen[0]
                    self.dul[i] *= self.retry_widen[1]
                    if self.check_lower:
                        self.check_lower_limits(i, b)
                    ok = self._equilibrate(i, b)
                if ok:                                    # a failed sub-step keeps the old rates and goes on;
                    self.after_gems(i)                    # the node fails if the last sub-step failed (OGS 2017)
                sub_t += dt_chem
                if sub_t + dt_chem > dt:
                    dt_chem = dt - sub_t
                if dt_chem <= 1e-12:
                    break
            if ok:
                self.mass_to_concentration(i)
            else:                                     # OGS: keep the old solution, take transported c
                n_fail += 1
                for k, v in saved.items():
                    getattr(self, k)[i] = v
                self.c[i] = np.abs(c_transport[i])
        self.last = dict(failed=n_fail, substepped=n_split)
        if self.max_failed is not None and n_fail > self.max_failed:
            raise RuntimeError(f'{n_fail} GEMS nodes failed in one step')
        return self.c

    def water_source(self, dt, node_volume):
        """OGS SetSourceSink: excess GEMS water / dt * node volume, m3/s (0 on boundary nodes)."""
        return np.where(self.boundary, 0.0, self.excess / dt * node_volume)

    def amounts(self, name):
        """Species amount per node (mol per node volume), by species name."""
        return self.x[:, self.species.index(name)]


def _dch_list(text, tag):
    """A quoted name list (<ICNL>, <DCNL>, <PHNL>, <ccPH>) of a GEMS3K DCH text file, or None."""
    if text is None:
        return None
    m = re.search(rf'<{tag}>\s*(.*?)(?=\n\s*[#<])', text, re.S)
    return re.findall(r"'([^']*)'", m.group(1)) if m else None
