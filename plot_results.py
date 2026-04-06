from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_csv(path: Path):
    data = np.genfromtxt(path, delimiter=",", names=True)
    return data


def main() -> None:
    p = argparse.ArgumentParser(description="Plot toy-model observables")
    p.add_argument("--result-dir", required=True, help="e.g. results/CIPSe_toy")
    args = p.parse_args()

    result_dir = Path(args.result_dir)
    cooling_csv = result_dir / "cooling" / "observables.csv"
    if not cooling_csv.exists():
        raise FileNotFoundError(cooling_csv)

    d = load_csv(cooling_csv)

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    axes[0].plot(d["T"], d["m"], "o-")
    axes[0].set_xlabel("T")
    axes[0].set_ylabel("m")

    axes[1].plot(d["T"], d["q_peak"], "o-")
    axes[1].set_xlabel("T")
    axes[1].set_ylabel("q_peak")

    axes[2].plot(d["T"], d["S_peak"], "o-")
    axes[2].set_xlabel("T")
    axes[2].set_ylabel("S_peak")

    fig.tight_layout()
    out = result_dir / "cooling_summary.png"
    fig.savefig(out, dpi=150)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
