from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


Index = Tuple[int, int]


@dataclass
class TriangularLattice:
    lx: int
    ly: int

    def __post_init__(self) -> None:
        self.a1 = np.array([1.0, 0.0])
        self.a2 = np.array([0.5, np.sqrt(3.0) / 2.0])
        self.super_a = self.lx * self.a1
        self.super_b = self.ly * self.a2
        self.positions = self._build_positions()
        self.nn_offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        self.nnn_offsets = [(1, 1), (-1, -1), (2, -1), (-2, 1), (1, -2), (-1, 2)]

    @property
    def shape(self) -> Tuple[int, int]:
        return (self.lx, self.ly)

    def _pbc(self, i: int, j: int) -> Index:
        return i % self.lx, j % self.ly

    def _build_positions(self) -> np.ndarray:
        pos = np.zeros((self.lx, self.ly, 2), dtype=float)
        for i in range(self.lx):
            for j in range(self.ly):
                pos[i, j] = i * self.a1 + j * self.a2
        return pos

    def neighbor_indices(self, i: int, j: int, shell: str = "nn") -> List[Index]:
        offsets = self.nn_offsets if shell == "nn" else self.nnn_offsets
        return [self._pbc(i + di, j + dj) for di, dj in offsets]

    def minimal_image_distance(self, i: int, j: int, ii: int, jj: int) -> float:
        dr0 = self.positions[ii, jj] - self.positions[i, j]
        best = np.inf
        for m in (-1, 0, 1):
            for n in (-1, 0, 1):
                dr = dr0 + m * self.super_a + n * self.super_b
                d = np.linalg.norm(dr)
                if d < best:
                    best = d
        return float(best)

    def all_pairs_within_cutoff(self, cutoff: float) -> List[Tuple[Index, Index, float]]:
        pairs = []
        for i in range(self.lx):
            for j in range(self.ly):
                for ii in range(self.lx):
                    for jj in range(self.ly):
                        if (ii, jj) <= (i, j):
                            continue
                        d = self.minimal_image_distance(i, j, ii, jj)
                        if 1e-12 < d <= cutoff:
                            pairs.append(((i, j), (ii, jj), d))
        return pairs
