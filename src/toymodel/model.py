from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from .lattice import TriangularLattice
from .params import ModelParams


@dataclass
class ToyModel:
    lattice: TriangularLattice
    params: ModelParams
    dipolar_cutoff: float = 6.0

    def __post_init__(self) -> None:
        self.dipolar_pairs = self.lattice.all_pairs_within_cutoff(self.dipolar_cutoff)

    def onsite_energy_density(self, s: np.ndarray) -> np.ndarray:
        p = self.params
        return 0.5 * p.alpha * s**2 - 0.25 * p.beta * s**4 + (p.gamma / 6.0) * s**6

    def total_energy(self, s: np.ndarray) -> float:
        e = float(np.sum(self.onsite_energy_density(s)))
        e += self._pair_energy(s, shell="nn", coef=-self.params.j1)
        e += self._pair_energy(s, shell="nnn", coef=+self.params.j2)
        e += self._dipolar_energy(s)
        e -= self.params.h * float(np.sum(s))
        return e

    def _pair_energy(self, s: np.ndarray, shell: str, coef: float) -> float:
        e = 0.0
        for i in range(self.lattice.lx):
            for j in range(self.lattice.ly):
                for ii, jj in self.lattice.neighbor_indices(i, j, shell=shell):
                    if (ii, jj) <= (i, j):
                        continue
                    e += coef * s[i, j] * s[ii, jj]
        return float(e)

    def _dipolar_energy(self, s: np.ndarray) -> float:
        e = 0.0
        for (i, j), (ii, jj), d in self.dipolar_pairs:
            e += self.params.d_eff * s[i, j] * s[ii, jj] / (d**3)
        return float(e)

    def local_energy(self, s: np.ndarray, i: int, j: int) -> float:
        p = self.params
        x = s[i, j]
        e = 0.5 * p.alpha * x**2 - 0.25 * p.beta * x**4 + (p.gamma / 6.0) * x**6 - p.h * x
        for ii, jj in self.lattice.neighbor_indices(i, j, shell="nn"):
            e += -p.j1 * x * s[ii, jj]
        for ii, jj in self.lattice.neighbor_indices(i, j, shell="nnn"):
            e += +p.j2 * x * s[ii, jj]
        for (a, b), (c, d), dist in self.dipolar_pairs:
            if (a, b) == (i, j):
                e += p.d_eff * x * s[c, d] / (dist**3)
            elif (c, d) == (i, j):
                e += p.d_eff * x * s[a, b] / (dist**3)
        return float(e)

    def delta_energy_local(self, s: np.ndarray, i: int, j: int, new_value: float) -> float:
        old_value = s[i, j]
        if new_value == old_value:
            return 0.0
        old_e = self.local_energy(s, i, j)
        s[i, j] = new_value
        new_e = self.local_energy(s, i, j)
        s[i, j] = old_value
        return float(new_e - old_e)
