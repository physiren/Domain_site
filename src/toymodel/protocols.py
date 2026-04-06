from __future__ import annotations

from dataclasses import replace
from typing import Dict, Iterable, List

import numpy as np

from .mc import run_mc
from .model import ToyModel
from .observables import polarization, q_peak_and_domain, radial_average_spectrum, structure_factor
from .params import ModelParams


def run_temperature_protocol(
    s: np.ndarray,
    base_params: ModelParams,
    lattice,
    temperatures: Iterable[float],
    rng: np.random.Generator,
    n_therm: int,
    n_sample: int,
    sweep_between_samples: int,
    delta_max: float,
    dipolar_cutoff: float,
) -> List[Dict[str, float]]:
    records: List[Dict[str, float]] = []
    for T in temperatures:
        model = ToyModel(lattice=lattice, params=base_params, dipolar_cutoff=dipolar_cutoff)
        snapshots, acc = run_mc(
            s=s,
            model=model,
            temperature=float(T),
            n_therm=n_therm,
            n_sample=n_sample,
            sweep_between_samples=sweep_between_samples,
            delta_max=delta_max,
            rng=rng,
        )
        s[:, :] = snapshots[-1]
        sq = structure_factor(s)
        q, srad = radial_average_spectrum(sq)
        q_peak, s_peak, l_dom = q_peak_and_domain(q, srad)
        records.append(
            {
                "T": float(T),
                "h": base_params.h,
                "m": polarization(s),
                "energy": model.total_energy(s) / s.size,
                "q_peak": q_peak,
                "S_peak": s_peak,
                "L_dom": l_dom,
                "acceptance": acc,
            }
        )
    return records


def run_field_protocol(
    s: np.ndarray,
    base_params: ModelParams,
    lattice,
    field_schedule: Iterable[float],
    temperature: float,
    rng: np.random.Generator,
    n_therm: int,
    n_sample: int,
    sweep_between_samples: int,
    delta_max: float,
    dipolar_cutoff: float,
) -> List[Dict[str, float]]:
    records: List[Dict[str, float]] = []
    for h in field_schedule:
        params_h = replace(base_params, h=float(h))
        model = ToyModel(lattice=lattice, params=params_h, dipolar_cutoff=dipolar_cutoff)
        snapshots, acc = run_mc(
            s=s,
            model=model,
            temperature=temperature,
            n_therm=n_therm,
            n_sample=n_sample,
            sweep_between_samples=sweep_between_samples,
            delta_max=delta_max,
            rng=rng,
        )
        s[:, :] = snapshots[-1]
        sq = structure_factor(s)
        q, srad = radial_average_spectrum(sq)
        q_peak, s_peak, l_dom = q_peak_and_domain(q, srad)
        records.append(
            {
                "T": temperature,
                "h": float(h),
                "m": polarization(s),
                "energy": model.total_energy(s) / s.size,
                "q_peak": q_peak,
                "S_peak": s_peak,
                "L_dom": l_dom,
                "acceptance": acc,
            }
        )
    return records
