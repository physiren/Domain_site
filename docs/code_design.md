# 代码说明（实现与扩展）

## 模型

哈密顿量：

\[
H=\sum_i\left(\frac{\alpha}{2}s_i^2-\frac{\beta}{4}s_i^4+\frac{\gamma}{6}s_i^6\right)
-J_1\sum_{\langle ij\rangle}s_is_j
+J_2\sum_{\langle\langle ij\rangle\rangle}s_is_j
+\frac12\sum_{i\neq j}D_{\rm eff}\frac{s_is_j}{r_{ij}^3}
-h\sum_i s_i.
\]

`model.py` 里使用同一符号约定，便于与 `site_model.md` 对照。

## 三角晶格实现

- 基矢：`a1=(1,0), a2=(1/2, sqrt(3)/2)`；
- 最近邻（6个）和次近邻（6个）都按三角晶格定义；
- 偶极距离通过最小镜像（supercell 平移）近似计算。

## Monte Carlo

- 使用软自旋局域随机提案：`s' = s + U[-Δ,Δ]`；
- 接受率：Metropolis；
- 每个温度/外场点：热化 + 采样，采样末态传给下一点（协议连续）。

## 观测量

- `m = mean(s)`；
- `Sq = |FFT(s-mean)|^2`；
- 径向平均得到 `S(q)`；
- `q_peak` 是去掉 `q=0` 后的峰位；
- `L_dom = 2π/q_peak`。

## 扩展接口

1. 若要更准的偶极长程项：可在 `model.py` 中替换 `_dipolar_energy` 为 Ewald/FFT 卷积。
2. 若要更快：可将 `mc.py` 与 `model.py` 的热点循环用 `numba.njit` 包装。
3. 若要接 DFT 参数：在 `params.py` 增加 `from_json`/`from_yaml` 即可。
