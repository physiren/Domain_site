from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class ModelParams:
    name: str
    alpha: float
    beta: float
    gamma: float
    j1: float
    j2: float
    d_eff: float
    h: float = 0.0
    k_b: float = 1.0

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


TOY_PRESETS: Dict[str, ModelParams] = {
    "CIPS_toy": ModelParams(
        name="CIPS_toy",
        alpha=1.3,
        beta=3.3,
        gamma=1.0,
        j1=12.0,
        j2=1.0,
        d_eff=10.0,
        h=0.0,
    ),
    "CIPSe_toy": ModelParams(
        name="CIPSe_toy",
        alpha=0.9,
        beta=2.5,
        gamma=1.0,
        j1=8.0,
        j2=3.0,
        d_eff=6.0,
        h=0.0,
    ),
}


def get_preset(material: str) -> ModelParams:
    try:
        return TOY_PRESETS[material]
    except KeyError as exc:
        raise KeyError(f"Unknown preset '{material}'. Choices: {list(TOY_PRESETS)}") from exc
