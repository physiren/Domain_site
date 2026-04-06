from __future__ import annotations

from typing import Tuple

import numpy as np


def polarization(s: np.ndarray) -> float:
    return float(np.mean(s))


def structure_factor(s: np.ndarray) -> np.ndarray:
    fluc = s - np.mean(s)
    sq = np.abs(np.fft.fftshift(np.fft.fft2(fluc))) ** 2
    return sq / s.size


def radial_average_spectrum(sq: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    lx, ly = sq.shape
    qx = np.fft.fftshift(np.fft.fftfreq(lx)) * 2 * np.pi
    qy = np.fft.fftshift(np.fft.fftfreq(ly)) * 2 * np.pi
    qxx, qyy = np.meshgrid(qx, qy, indexing="ij")
    qr = np.sqrt(qxx**2 + qyy**2)

    qmax = float(np.max(qr))
    nbins = min(lx, ly) // 2
    bins = np.linspace(0, qmax, nbins + 1)
    idx = np.digitize(qr.ravel(), bins) - 1

    ssum = np.zeros(nbins)
    cnt = np.zeros(nbins)
    vals = sq.ravel()
    for k, v in zip(idx, vals):
        if 0 <= k < nbins:
            ssum[k] += v
            cnt[k] += 1

    cnt[cnt == 0] = 1
    srad = ssum / cnt
    qmid = 0.5 * (bins[:-1] + bins[1:])
    return qmid, srad


def q_peak_and_domain(q: np.ndarray, srad: np.ndarray) -> Tuple[float, float, float]:
    if len(q) < 2:
        return 0.0, 0.0, np.inf
    idx = int(np.argmax(srad[1:]) + 1)
    q_peak = float(q[idx])
    s_peak = float(srad[idx])
    l_dom = float(2 * np.pi / q_peak) if q_peak > 1e-12 else np.inf
    return q_peak, s_peak, l_dom
