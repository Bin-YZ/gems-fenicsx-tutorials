"""Small OGS5 material laws and element helpers used by the cases (NumPy only).

Node values -> element values (OGS ConvPorosityNodeValue2Elem and friends):
    element_mean(node_values, cells)          arithmetic mean of the element's nodes
    harmonic_mean(node_values, cells)         harmonic mean of the element's nodes
                                              (cells=None: values already given per element node, (m, k))

Material laws (OGS .mmp / .mcp model numbers in brackets):
    archie_diffusion(D, phi, m)               D * phi**m
    porosity_diffusion_8(D, phi, phi0, m)     $DIFFUSION 8:  D * phi**(m+1) / phi0**m
    kozeny_carman_4(k0, phi0, phi)            $PERMEABILITY_FUNCTION_POROSITY 4

1D line elements embedded in a 2D mesh (fractures, OGS GEOMETRY_AREA):
    LineElements(mesh, lines, area)           assemble mass / advection-dispersion / flow matrices
"""
import numpy as np
import scipy.sparse as sp


def element_mean(node_values, cells=None):
    """Mean over each element's nodes; with cells=None node_values is already (m, k)."""
    v = np.asarray(node_values) if cells is None else np.asarray(node_values)[cells]
    return v.mean(axis=1)


def harmonic_mean(node_values, cells=None):
    """Harmonic mean over each element's nodes; with cells=None node_values is already (m, k)."""
    v = np.asarray(node_values) if cells is None else np.asarray(node_values)[cells]
    return v.shape[1] / (1.0 / v).sum(axis=1)


def archie_diffusion(D, phi, m):
    return D * np.asarray(phi) ** m


def porosity_diffusion_8(D, phi, phi0, m):
    return D * np.asarray(phi) ** (m + 1) / np.asarray(phi0) ** m


def kozeny_carman_4(k0, phi0, phi):
    """k0 ((1-phi0)/(1-phi))^2 (phi/phi0)^3; OGS keeps k0 when phi or phi0 is outside (0, 1)."""
    k0, phi0, phi = np.broadcast_arrays(np.asarray(k0, float), np.asarray(phi0, float), np.asarray(phi, float))
    ok = (phi0 > 0) & (phi0 < 1) & (phi > 0) & (phi < 1)
    a, b = np.where(ok, phi, 0.5), np.where(ok, phi0, 0.5)
    return np.where(ok, k0 * ((1 - b) / (1 - a)) ** 2 * (a / b) ** 3, k0)


class LineElements:
    """Linear 2-node elements (e.g. a fracture) sharing nodes with the 2D mesh.

    OGS multiplies every integral over a line element by its GEOMETRY_AREA
    (aperture x unit thickness). The matrices returned here are in OGS node
    order and are added to the 2D matrices by Transport / Darcy (M_extra,
    K_extra, extra)."""

    def __init__(self, n_nodes, points, lines, area):
        self.n, self.lines, self.area = n_nodes, np.asarray(lines), area
        self.length = np.linalg.norm(points[self.lines[:, 1]] - points[self.lines[:, 0]], axis=1)
        i0, i1 = self.lines[:, 0], self.lines[:, 1]
        self._rows, self._cols = np.r_[i0, i0, i1, i1], np.r_[i0, i1, i0, i1]

    def _matrix(self, a00, a01, a10, a11):
        return sp.csr_matrix((np.r_[a00, a01, a10, a11], (self._rows, self._cols)), shape=(self.n, self.n))

    def node_volume(self):
        v = np.zeros(self.n)
        np.add.at(v, self.lines, (self.length * self.area / 2)[:, None])
        return v

    def flow_matrix(self, K):
        k = self.area * K / self.length
        return self._matrix(k, -k, -k, k)

    def velocity(self, K, head):
        """Darcy velocity along each element, positive from its node 0 to node 1."""
        return -K * (head[self.lines[:, 1]] - head[self.lines[:, 0]]) / self.length

    def transport_matrices(self, phi, De, alpha_L, v):
        """Consistent mass phi, Galerkin advection v and diffusion De + alpha_L |v|."""
        m = self.area * phi * self.length / 6
        kd = self.area * (De + alpha_L * np.abs(v)) / self.length
        adv = self.area * v / 2
        return self._matrix(2 * m, m, m, 2 * m), self._matrix(kd - adv, -kd + adv, -kd - adv, kd + adv)
