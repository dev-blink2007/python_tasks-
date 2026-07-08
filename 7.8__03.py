"""
练习3：矢量化运算与聚合函数
"""

import numpy as np

print("="*50)
print("练习3：矢量化运算与聚合函数")
print("="*50)

# 任务1：逐元素乘法和矩阵乘法
np.random.seed(42)  # 设置随机种子，使结果可重复
A = np.random.randint(1, 10, size=(2, 3))
B = np.random.randint(1, 10, size=(2, 3))
print(f"\n数组 A (2×3):")
print(A)
print(f"\n数组 B (2×3):")
print(B)

# 逐元素乘法（*）
element_wise = A * B
print(f"\n任务1 - 逐元素乘法 (A * B):")
print(element_wise)
print("说明：对应位置元素相乘")

# 矩阵乘法（@）
# A是2×3，需要B的转置(3×2)才能相乘，结果为2×2
matrix_product = A @ B.T
print(f"\n矩阵乘法 (A @ B.T):")
print(matrix_product)
print("说明：A(2×3) × B.T(3×2) = 2×2矩阵")

# 如果B是3×2的话可以直接相乘
print("\n【矩阵乘法补充】")
C = np.random.randint(1, 10, size=(3, 2))
print(f"A (2×3):\n{A}")
print(f"C (3×2):\n{C}")
print(f"A @ C = \n{A @ C}")

# 任务2：按行和列求和
arr_sum = np.array([[1, 2], [3, 4]])
print(f"\n任务2 - 测试数组:")
print(arr_sum)

row_sum = np.sum(arr_sum, axis=1)  # 按行求和（水平方向）
col_sum = np.sum(arr_sum, axis=0)  # 按列求和（垂直方向）
print(f"按行求和 (axis=1)：{row_sum}")
print(f"按列求和 (axis=0)：{col_sum}")

# 详细说明axis参数
print("\n【axis参数说明】")
print(f"axis=0（垂直）：{np.sum(arr_sum, axis=0)}  # 每列求和")
print(f"axis=1（水平）：{np.sum(arr_sum, axis=1)}  # 每行求和")

# 任务3：均值、标准差、四舍五入
arr_float = np.array([1.2, 3.5, 2.8])
print(f"\n任务3 - 数组：{arr_float}")

mean_val = np.mean(arr_float)
std_val = np.std(arr_float)
round_val = np.round(arr_float)
print(f"均值：{mean_val:.2f}")
print(f"标准差：{std_val:.2f}")
print(f"四舍五入：{round_val}")

# 额外演示：其他聚合函数
print("\n【其他聚合函数】")
print(f"最大值：{np.max(arr_float)}")
print(f"最小值：{np.min(arr_float)}")
print(f"总和：{np.sum(arr_float)}")
print(f"中位数：{np.median(arr_float)}")