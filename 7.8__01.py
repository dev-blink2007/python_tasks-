"""
练习1：数组创建与形状操作
"""

import numpy as np

print("="*50)
print("练习1：数组创建与形状操作")
print("="*50)

# 任务1：创建形状为(3,4)的随机整数数组（范围0~9）
arr = np.random.randint(0, 10, size=(3, 4))
print(f"\n任务1 - 原始数组 (3×4):")
print(arr)
print(f"形状：{arr.shape}")
print(f"数据类型：{arr.dtype}")

# 任务2：重塑为(4,3)并转置
# 先reshape成(4,3)，再转置
reshaped_arr = arr.reshape(4, 3)  # 重塑
transposed_arr = reshaped_arr.T   # 转置
print(f"\n任务2 - 重塑为(4×3)后转置:")
print(transposed_arr)
print(f"形状：{transposed_arr.shape}")

# 也可以用一行代码实现
# transposed_arr = arr.reshape(4, 3).T

# 任务3：提取所有大于5的元素
filtered_arr = arr[arr > 5]
print(f"\n任务3 - 大于5的元素:")
print(filtered_arr)
print(f"元素个数：{len(filtered_arr)}")
print(f"大于5的元素值：{filtered_arr}")

# 额外演示：布尔索引
print("\n【布尔索引演示】")
print(f"原始数组：\n{arr}")
print(f"布尔掩码（>5）：\n{arr > 5}")
print(f"提取结果：{arr[arr > 5]}")