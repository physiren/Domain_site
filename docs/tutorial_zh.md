# 教程：如何先跑通 toy model 并做第一轮调参

## 1. 安装依赖

```bash
python3 -m pip install numpy scipy matplotlib
```

## 2. 首次运行（推荐）

先用 CIPSe 方案跑温度+扫场：

```bash
python3 run_toy.py \
  --material CIPSe_toy \
  --lx 24 --ly 24 \
  --n-therm 150 --n-sample 12 --sweep-between 8 \
  --field-protocol
```

再画汇总图：

```bash
python3 plot_results.py --result-dir results/CIPSe_toy
```

## 3. 结果怎么读

在 `results/<material>/cooling/observables.csv` 里重点看：

- `m`：越接近 ±1 常对应更均匀极化；
- `q_peak` 与 `S_peak`：有限 `q_peak` + 大 `S_peak` 表示更明显的有限尺度纹理；
- `L_dom = 2π/q_peak`：粗略畴尺度估计。

对比 CIPS/CIPSe 时可重点观察：

1. CIPSe 是否更容易出现更大的 `S_peak`（非均匀通道更强）；
2. CIPS 是否在降温下更快进入大畴/近均匀态（`|m|` 更快增大）。

## 4. 第一轮调参建议

按以下顺序：

1. 固定 `d_eff=0`，扫 `j2/j1`（看纯短程竞争）；
2. 逐步增大 `d_eff`（看纹理尺度是否被稳定到有限 `q`）；
3. 开启扫场（看纹理能否在强场被压制）。

## 5. 常见问题

- **运行慢**：先把 `lx,ly` 调小到 `16x16`，并降低 `n_therm` / `n_sample`。
- **几乎全随机**：提高 `n_therm`，或把降温最低温度降到 `0.15`。
- **接受率太低**：调小 `--delta-max`（例如 `0.2`）。

## 6. 下一步（接入 DFT）

- 用 frozen phonon 曲线替换 `alpha,beta,gamma`；
- 用超胞能量差拟合 `j1,j2`；
- 用极化和介电参数估算并校正 `d_eff`。
