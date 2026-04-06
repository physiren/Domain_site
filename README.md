# CIPS/CIPSe 三角晶格 Toy Model（预 DFT 阶段）

本仓库实现了 `site_model.md` 中建议的第一阶段代码：

- 单层三角晶格软自旋模型（局域六次势 + J1/J2 + 有效偶极 + 外场）；
- CIPS/CIPSe 两套 toy 参数；
- 温度降温协议 + 固定温度扫场协议；
- 观测量输出：平均极化、能量、结构因子峰值、估算畴尺度。

## 快速开始

```bash
python3 run_toy.py --material CIPSe_toy --lx 24 --ly 24 --field-protocol
python3 plot_results.py --result-dir results/CIPSe_toy
```

输出目录示例：

```text
results/
  CIPSe_toy/
    cooling/
      observables.csv
      snapshots/final_state.npy
      spectra/Sq.npy
      spectra/q.npy
      spectra/Srad.npy
    hysteresis/
      observables.csv
```

## 代码结构

- `src/toymodel/params.py`：参数定义和 CIPS/CIPSe 预设。
- `src/toymodel/lattice.py`：三角晶格几何与邻居、偶极对列表。
- `src/toymodel/model.py`：哈密顿量总能和局域能差。
- `src/toymodel/mc.py`：Metropolis 更新与采样。
- `src/toymodel/protocols.py`：降温协议与扫场协议。
- `src/toymodel/observables.py`：结构因子、径向谱、`q_peak`、`L_dom`。
- `src/toymodel/init_states.py`：`Gamma/M/K` 三类初始化。
- `run_toy.py`：主程序。
- `plot_results.py`：简单结果可视化。

## 与 `site_model.md` 的对应

已按文档要求支持：

- 三角晶格（不再使用方格 checkerboard）；
- `Gamma` / `M` / `K` 初始化；
- 先运行 toy，再替换参数；
- `observables.csv` 至少包含 `T,h,m,energy,q_peak,S_peak,L_dom`。

详细教程见：`docs/tutorial_zh.md`。
