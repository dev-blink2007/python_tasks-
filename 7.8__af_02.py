"""
练习2：金融数据分析实战
"""

import numpy as np

print("="*50)
print("练习2：金融数据分析实战")
print("="*50)

# ========== 1. 股票收益率计算 ==========
print("\n【1. 股票收益率计算】")

prices = np.array([100, 102, 105, 103, 107])
returns = np.log(prices[1:] / prices[:-1])
print(f"股价：{prices}")
print(f"每日对数收益率：{returns}")
print(f"总收益率：{np.sum(returns):.4f}")


# ========== 2. 移动平均线 ==========
print("\n【2. 移动平均线】")

np.random.seed(42)
prices_daily = 100 + np.cumsum(np.random.randn(100) * 0.5)

# 5日移动平均
w5 = np.ones(5) / 5
ma5 = np.convolve(prices_daily, w5, mode='valid')

# 20日移动平均
w20 = np.ones(20) / 20
ma20 = np.convolve(prices_daily, w20, mode='valid')

print(f"股价前5个：{prices_daily[:5]}")
print(f"5日MA前5个：{ma5[:5]}")
print(f"20日MA前5个：{ma20[:5]}")


# ========== 3. 风险分析 ==========
print("\n【3. 风险分析】")

np.random.seed(123)
returns_data = np.random.randn(1000, 252) * 0.02

# 年化波动率
annual_vol = np.std(returns_data, axis=1) * np.sqrt(252)
print(f"前5支股票年化波动率：{annual_vol[:5]}")
print(f"平均波动率：{annual_vol.mean():.2%}")

# 相关系数矩阵（前10支）
corr = np.corrcoef(returns_data[:10, :])
print(f"相关系数矩阵（前5行前5列）：\n{corr[:5, :5]}")

# 平均相关系数
triu = np.triu_indices_from(corr, k=1)
print(f"平均相关系数：{np.mean(corr[triu]):.4f}")