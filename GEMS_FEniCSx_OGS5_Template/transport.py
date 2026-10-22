"""Advection-dispersion of dissolved components with CG1 finite elements (OGS5 MASS_TRANSPORT).

    phi dc/dt + q . grad c - div((De I + D_disp(q)) grad c) = 0,   backward Euler (OGS theta = 1)

    c        mol / m3 pore water, one column per transported component
    phi      element porosity (storage), OGS uses the mean of the node porosities
    De       element effective diffusion coefficient, m2/s (whatever the case's
             diffusion model gives; it multiplies grad c directly)
    q        Darcy flux, a UFL vector (a constant, or -K grad(head) from flow.Darcy)
    D_disp   alpha_T |q| I + (alpha_L - alpha_T) q q^T / |q|

Discretisation options, matching what the OGS cases use:
    lumped=True           row-sum (lumped) mass matrix
    fct=True              FEM-FCT (Kuzmin linearised, Zalesak limiter) as OGS $FEM_FCT;
                          fct_ogs_sign=True adds +f_ij to row j like OGS's AddFCT_CorrectionVector
                          (the textbook scheme uses -f_ij)
    quadrature_degree     e.g. 5 for OGS's 3x3 Gauss points on quadrilaterals

Interface used by reactive_transport.run():
    transport.phi_cell, transport.De_cell   (n_cells,) arrays, set by the case before each step
    transport.fixed_values                  (n_fixed, n_components) Dirichlet values
    transport.M_extra, transport.K_extra    optional sparse matrices in OGS node order (line elements)
    transport.step(c, dt) -> c_new          c in OGS node order, shape (n_nodes, n_components)
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import ufl
from dolfinx import fem


class Transport:
    def __init__(self, mesh, fixed_nodes=(), q=None, alpha_L=0.0, alpha_T=None, lumped=False,
                 fct=False, fct_ogs_sign=True, quadrature_degree=None):
        self.mesh = mesh
        self.fixed = mesh.node2dof[np.asarray(fixed_nodes, int)]        # dof numbers of Dirichlet nodes
        self.free = np.setdiff1d(np.arange(mesh.n_nodes), self.fixed)
        self.lumped, self.fct, self.fct_ogs_sign = lumped, fct, fct_ogs_sign
        self.phi_cell = np.ones(mesh.n_cells)
        self.De_cell = np.zeros(mesh.n_cells)
        self.fixed_values = None
        self.M_extra = self.K_extra = None
        self._phi, self._De = mesh.cell_function(), mesh.cell_function()
        u, v = ufl.TrialFunction(mesh.V), ufl.TestFunction(mesh.V)
        dx = ufl.dx(domain=mesh.domain) if quadrature_degree is None else \
            ufl.Measure('dx', domain=mesh.domain, metadata={'quadrature_degree': quadrature_degree})
        stiff = self._De * ufl.inner(ufl.grad(u), ufl.grad(v)) * dx
        if q is not None:
            stiff += ufl.dot(q, ufl.grad(u)) * v * dx
            alpha_T = alpha_L if alpha_T is None else alpha_T
            if alpha_L or alpha_T:
                qn = ufl.sqrt(ufl.dot(q, q) + 1e-60)
                if alpha_T == alpha_L:
                    stiff += alpha_L * qn * ufl.inner(ufl.grad(u), ufl.grad(v)) * dx
                else:
                    D = alpha_T * qn * ufl.Identity(mesh.dim) + (alpha_L - alpha_T) * ufl.outer(q, q) / qn
                    stiff += ufl.inner(D * ufl.grad(u), ufl.grad(v)) * dx
        self._m_form = fem.form(self._phi * u * v * dx)
        self._k_form = fem.form(stiff)

    def _to_dof(self, A):
        """Sparse matrix in OGS node order -> dof order."""
        p = self.mesh.dof2node
        return A.tocsr()[p][:, p]

    def matrices(self):
        """Assemble M and K (dof order) for the current phi_cell, De_cell and q."""
        self.mesh.set_cells(self._phi, self.phi_cell)
        self.mesh.set_cells(self._De, self.De_cell)
        M = fem.assemble_matrix(self._m_form).to_scipy().tocsr()
        K = fem.assemble_matrix(self._k_form).to_scipy().tocsr()
        if self.M_extra is not None:
            M = M + self._to_dof(self.M_extra)
        if self.K_extra is not None:
            K = K + self._to_dof(self.K_extra)
        if self.lumped:
            M = sp.diags(np.asarray(M.sum(axis=1)).ravel()).tocsr()
        return M, K

    def step(self, c, dt):
        """Advance all columns of c (OGS node order) by one backward-Euler step of size dt."""
        n2d = self.mesh.node2dof
        u0 = np.asarray(c, float)[self.mesh.dof2node]                   # dof order
        u_fix = None
        if len(self.fixed):
            u_fix = np.broadcast_to(self.fixed_values, (len(self.fixed), u0.shape[1]))
        M, K = self.matrices()
        if self.fct:
            u = self._fct(M, K, u0, u_fix, dt)
        else:
            u = self._solve(M / dt + K, M / dt @ u0, u0, u_fix)
        return u[n2d]

    def _solve(self, A, rhs, u0, u_fix):
        A = A.tocsr()
        u = u0.copy()
        if u_fix is not None:
            u[self.fixed] = u_fix
            rhs = rhs[self.free] - A[self.free][:, self.fixed] @ u_fix
        else:
            rhs = rhs[self.free]
        u[self.free] = spla.splu(A[self.free][:, self.free].tocsc()).solve(rhs)
        return u

    def _fct(self, M, K, u0, u_fix, dt):
        """FEM-FCT: high-order Galerkin, low-order with discrete diffusion D, Zalesak-limited antidiffusion."""
        n, fixed = len(u0), self.fixed
        u_high = self._solve(M / dt + K, M / dt @ u0, u0, u_fix)
        pair = sp.triu(abs(M) + abs(K), k=1).tocoo()
        ii, jj = pair.row, pair.col
        d = np.minimum(np.minimum(0.0, -np.asarray(K[ii, jj]).ravel()), -np.asarray(K[jj, ii]).ravel())
        D = sp.csr_matrix((np.r_[d, d, -d, -d], (np.r_[ii, jj, ii, jj], np.r_[jj, ii, ii, jj])), shape=(n, n))
        ML = np.asarray(M.sum(1)).ravel()
        A_low = (sp.diags(ML / dt) + K + D).tocsr()
        lu = spla.splu(A_low[self.free][:, self.free].tocsc())
        du = u_high[ii] - u_high[jj]
        flux = np.asarray(M[ii, jj]).ravel()[:, None] / dt * (du - (u0[ii] - u0[jj])) - d[:, None] * du
        flux[flux * (-du) > 0] = 0.0                                     # prelimiting
        u = u0.copy()
        if u_fix is not None:
            u[fixed] = u_fix
        for col in range(u0.shape[1]):
            f_i = flux[:, col]
            f_j = f_i if self.fct_ogs_sign else -f_i
            Pp, Pm, Qp, Qm = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)
            np.add.at(Pp, ii, np.maximum(f_i, 0)); np.add.at(Pm, ii, np.minimum(f_i, 0))
            np.add.at(Pp, jj, np.maximum(f_j, 0)); np.add.at(Pm, jj, np.minimum(f_j, 0))
            diff = u_high[jj, col] - u_high[ii, col]
            np.maximum.at(Qp, ii, diff); np.minimum.at(Qm, ii, diff)
            np.maximum.at(Qp, jj, -diff); np.minimum.at(Qm, jj, -diff)
            with np.errstate(divide='ignore', invalid='ignore'):
                Rp = np.where(Pp == 0, 0.0, np.minimum(1.0, ML * Qp / (dt * Pp)))
                Rm = np.where(Pm == 0, 0.0, np.minimum(1.0, ML * Qm / (dt * Pm)))
            Rp[fixed] = 1.0
            Rm[fixed] = 1.0
            a_i = np.where(f_i > 0, np.minimum(Rp[ii], Rm[jj]), np.minimum(Rp[jj], Rm[ii]))
            a_j = np.where(f_j > 0, np.minimum(Rp[jj], Rm[ii]), np.minimum(Rp[ii], Rm[jj]))
            corr = np.zeros(n)
            np.add.at(corr, ii, a_i * f_i)
            np.add.at(corr, jj, a_j * f_j)
            rhs = ML / dt * u0[:, col] + corr
            if u_fix is not None:
                rhs = rhs[self.free] - A_low[self.free][:, fixed] @ u[fixed, col]
            else:
                rhs = rhs[self.free]
            u[self.free, col] = lu.solve(rhs)
        return u
