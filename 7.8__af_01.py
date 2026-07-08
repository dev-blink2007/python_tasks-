"""
练习1：矩阵运算与性能优化
"""

import numpy as np
import time

print("="*50)
print("练习1：矩阵运算与性能优化")
print("="*50)

# ========== 1. 矩阵乘法性能对比 ==========
print("\n【1. 矩阵乘法性能对比】")

np.random.seed(42)
A = np.random.rand(1000, 2000)
B = np.random.rand(2000, 3000)

start = time.time()
r1 = np.dot(A, B)
t1 = time.time() - start

start = time.time()
r2 = A @ B
t2 = time.time() - start

start = time.time()
r3 = np.matmul(A, B)
t3 = time.time() - start

print(f"np.dot：{t1:.4f}秒")
print(f"@ 运算符：{t2:.4f}秒")
print(f"np.matmul：{t3:.4f}秒")
print(f"结果一致：{np.allclose(r1, r2) and np.allclose(r2, r3)}")


# ========== 2. 内存布局影响 ==========
print("\n【2. 内存布局对性能的影响】")

arr_c = np.random.rand(1000, 1000)
arr_f = np.asfortranarray(np.random.rand(1000, 1000))

# 按行求和
start = time.time()
np.sum(arr_c, axis=1)
t_c_row = time.time() - start

start = time.time()
np.sum(arr_f, axis=1)
t_f_row = time.time() - start

print(f"C顺序按行求和：{t_c_row:.4f}秒")
print(f"F顺序按行求和：{t_f_row:.4f}秒")

# 按列求和
start = time.time()
np.sum(arr_c, axis=0)
t_c_col = time.time() - start

start = time.time()
np.sum(arr_f, axis=0)
t_f_col = time.time() - start

print(f"C顺序按列求和：{t_c_col:.4f}秒")
print(f"F顺序按列求和：{t_f_col:.4f}秒")


# ========== 3. 避免临时内存分配 ==========
print("\n【3. 避免临时内存分配】")

x = np.random.rand(1000, 1000)

start = time.time()
res1 = x*x + 2*x + 1
t1 = time.time() - start

start = time.time()
res2 = np.empty_like(x)
tmp = np.multiply(x, x, out=res2)
tmp = np.multiply(2, x, out=tmp)
tmp = np.add(tmp, 1, out=tmp)
t2 = time.time() - start

print(f"直接计算：{t1:.4f}秒")
print(f"优化计算：{t2:.4f}秒")
print(f"结果一致：{np.allclose(res1, res2)}")