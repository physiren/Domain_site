from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

import csv
import numpy as np


def ensure_dirs(base: Path) -> Dict[str, Path]:
    paths = {
        "base": base,
        "snapshots": base / "snapshots",
        "spectra": base / "spectra",
    }
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    return paths


def write_observables_csv(path: Path, rows: Iterable[dict]) -> None:
    rows = list(rows)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_array(path: Path, arr: np.ndarray) -> None:
    np.save(path, arr)
