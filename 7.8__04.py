"""
练习4：综合应用
"""

import numpy as np

print("="*50)
print("练习4：综合应用")
print("="*50)

# 任务1：生成随机浮点数组并归一化
np.random.seed(123)  # 设置随机种子，使结果可重复
random_arr = np.random.random(10)  # 生成10个0~1之间的随机数
print(f"\n任务1 - 原始随机数组（10个0~1之间）：")
print(random_arr)
print(f"最小值：{random_arr.min():.4f}")
print(f"最大值：{random_arr.max():.4f}")

# 归一化到 [0, 100]
min_val = random_arr.min()
max_val = random_arr.max()
normalized = (random_arr - min_val) / (max_val - min_val) * 100
print(f"\n归一化到 [0, 100]：")
print(normalized)
print(f"归一化后最小值：{normalized.min():.2f}")
print(f"归一化后最大值：{normalized.max():.2f}")

# 归一化公式详解
print("\n【归一化公式】")
print(f"(arr - {min_val:.4f}) / ({max_val:.4f} - {min_val:.4f}) * 100")

# 任务2：累计和与累计最大值
print(f"\n任务2 - 累计运算：")
print(f"原始数组：{random_arr}")

cumsum_result = np.cumsum(random_arr)  # 累计和
cummax_result = np.maximum.accumulate(random_arr)  # 累计最大值
print(f"\n累计和 (cumsum)：")
print(cumsum_result)
print(f"累计和说明：每个位置是前面所有元素的和")

print(f"\n累计最大值 (cummax)：")
print(cummax_result)
print(f"累计最大值说明：每个位置是前面所有元素的最大值")

# 额外演示：累计运算的可视化理解
print("\n【累计运算详细理解】")
print("位置  值  累计和  累计最大值")
print("-" * 35)
for i in range(len(random_arr)):
    print(f"{i+1:2d}   {random_arr[i]:.4f}   {cumsum_result[i]:.4f}   {cummax_result[i]:.4f}")

# 额外演示：其他实用操作
print("\n【额外演示】")
# 排序
sorted_arr = np.sort(random_arr)
print(f"排序后：{sorted_arr}")

# 索引位置
max_index = np.argmax(random_arr)
min_index = np.argmin(random_arr)
print(f"最大值位置：{max_index}，值：{random_arr[max_index]:.4f}")
print(f"最小值位置：{min_index}，值：{random_arr[min_index]:.4f}")