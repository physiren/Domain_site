from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from src.toymodel.init_states import init_gamma, init_k_three_sublattice, init_random, init_stripe_m
from src.toymodel.io_utils import ensure_dirs, save_array, write_observables_csv
from src.toymodel.lattice import TriangularLattice
from src.toymodel.observables import radial_average_spectrum, structure_factor
from src.toymodel.params import get_preset
from src.toymodel.protocols import run_field_protocol, run_temperature_protocol


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run CIPS/CIPSe triangular-lattice toy model")
    p.add_argument("--material", choices=["CIPS_toy", "CIPSe_toy"], default="CIPSe_toy")
    p.add_argument("--lx", type=int, default=24)
    p.add_argument("--ly", type=int, default=24)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--n-therm", type=int, default=200)
    p.add_argument("--n-sample", type=int, default=20)
    p.add_argument("--sweep-between", type=int, default=10)
    p.add_argument("--delta-max", type=float, default=0.35)
    p.add_argument("--dipolar-cutoff", type=float, default=6.0)
    p.add_argument("--init", choices=["random", "gamma", "stripe_m", "k3"], default="random")
    p.add_argument("--field-protocol", action="store_true", help="run fixed-T hysteresis sweep")
    p.add_argument("--outdir", default="results")
    return p.parse_args()


def build_initial_state(args: argparse.Namespace) -> np.ndarray:
    if args.init == "random":
        return init_random(args.lx, args.ly, seed=args.seed)
    if args.init == "gamma":
        return init_gamma(args.lx, args.ly)
    if args.init == "stripe_m":
        return init_stripe_m(args.lx, args.ly, direction=0)
    return init_k_three_sublattice(args.lx, args.ly)


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(args.seed)
    lattice = TriangularLattice(args.lx, args.ly)
    params = get_preset(args.material)
    s = build_initial_state(args)

    base = Path(args.outdir) / args.material

    cooling_dir = ensure_dirs(base / "cooling")
    temperatures = np.linspace(1.8, 0.2, 9)
    cooling_rows = run_temperature_protocol(
        s=s,
        base_params=params,
        lattice=lattice,
        temperatures=temperatures,
        rng=rng,
        n_therm=args.n_therm,
        n_sample=args.n_sample,
        sweep_between_samples=args.sweep_between,
        delta_max=args.delta_max,
        dipolar_cutoff=args.dipolar_cutoff,
    )
    write_observables_csv(cooling_dir["base"] / "observables.csv", cooling_rows)
    save_array(cooling_dir["snapshots"] / "final_state.npy", s)
    sq = structure_factor(s)
    q, srad = radial_average_spectrum(sq)
    save_array(cooling_dir["spectra"] / "Sq.npy", sq)
    save_array(cooling_dir["spectra"] / "q.npy", q)
    save_array(cooling_dir["spectra"] / "Srad.npy", srad)

    if args.field_protocol:
        hysteresis_dir = ensure_dirs(base / "hysteresis")
        fields = np.concatenate([np.linspace(-10, 10, 11), np.linspace(10, -10, 11)[1:]])
        field_rows = run_field_protocol(
            s=s,
            base_params=params,
            lattice=lattice,
            field_schedule=fields,
            temperature=0.4,
            rng=rng,
            n_therm=args.n_therm,
            n_sample=max(5, args.n_sample // 2),
            sweep_between_samples=args.sweep_between,
            delta_max=args.delta_max,
            dipolar_cutoff=args.dipolar_cutoff,
        )
        write_observables_csv(hysteresis_dir["base"] / "observables.csv", field_rows)
        save_array(hysteresis_dir["snapshots"] / "final_state.npy", s)

    print(f"Done. Results saved to: {base}")


if __name__ == "__main__":
    main()
