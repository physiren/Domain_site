from __future__ import annotations

import numpy as np


def init_random(lx: int, ly: int, scale: float = 0.2, seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(0.0, scale, size=(lx, ly))


def init_gamma(lx: int, ly: int, amplitude: float = 1.0) -> np.ndarray:
    return np.full((lx, ly), amplitude, dtype=float)


def init_stripe_m(lx: int, ly: int, direction: int = 0, amplitude: float = 1.0) -> np.ndarray:
    s = np.zeros((lx, ly), dtype=float)
    for i in range(lx):
        for j in range(ly):
            if direction == 0:
                phase = i
            elif direction == 1:
                phase = j
            else:
                phase = i - j
            s[i, j] = amplitude if phase % 2 == 0 else -amplitude
    return s


def init_k_three_sublattice(lx: int, ly: int, mode: str = "A,A,-A", amplitude: float = 1.0) -> np.ndarray:
    s = np.zeros((lx, ly), dtype=float)
    for i in range(lx):
        for j in range(ly):
            sub = (i + 2 * j) % 3
            if mode == "A,A,-A":
                vals = [amplitude, amplitude, -amplitude]
            elif mode == "A,0,-A":
                vals = [amplitude, 0.0, -amplitude]
            else:
                raise ValueError("mode must be 'A,A,-A' or 'A,0,-A'")
            s[i, j] = vals[sub]
    return s
