from __future__ import annotations

import numpy as np

from .model import ToyModel


def metropolis_sweep(
    s: np.ndarray,
    model: ToyModel,
    temperature: float,
    delta_max: float,
    rng: np.random.Generator,
) -> float:
    accepted = 0
    total = s.size
    beta = 1.0 / max(temperature * model.params.k_b, 1e-12)

    lx, ly = s.shape
    for _ in range(total):
        i = int(rng.integers(0, lx))
        j = int(rng.integers(0, ly))
        proposal = s[i, j] + rng.uniform(-delta_max, delta_max)
        dE = model.delta_energy_local(s, i, j, proposal)
        if dE <= 0 or rng.random() < np.exp(-beta * dE):
            s[i, j] = proposal
            accepted += 1
    return accepted / total


def run_mc(
    s: np.ndarray,
    model: ToyModel,
    temperature: float,
    n_therm: int,
    n_sample: int,
    sweep_between_samples: int,
    delta_max: float,
    rng: np.random.Generator,
):
    for _ in range(n_therm):
        metropolis_sweep(s, model, temperature, delta_max, rng)

    accepts = []
    snapshots = []
    for _ in range(n_sample):
        for _ in range(sweep_between_samples):
            acc = metropolis_sweep(s, model, temperature, delta_max, rng)
            accepts.append(acc)
        snapshots.append(s.copy())
    return snapshots, float(np.mean(accepts)) if accepts else 0.0
