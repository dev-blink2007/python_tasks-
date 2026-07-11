"""
任务1：数据清洗与预处理
使用Titanic数据集（seaborn内置）
"""

import numpy as np
import pandas as pd
import seaborn as sns

print("="*60)
print("任务1：数据清洗与预处理")
print("="*60)

# ========== 1. 加载数据 ==========
print("\n【1. 加载数据】")

# 使用seaborn内置的Titanic数据集
titanic = sns.load_dataset('titanic')
print(f"原始数据形状：{titanic.shape}")
print(f"列名：{list(titanic.columns)}")
print(f"\n前5行数据：")
print(titanic.head())


# ========== 2. 查看数据概况 ==========
print("\n【2. 数据概况】")

print("\n数据类型：")
print(titanic.dtypes)

print("\n缺失值统计：")
print(titanic.isnull().sum())

print("\n描述性统计：")
print(titanic.describe())


# ========== 3. 处理缺失值 ==========
print("\n【3. 处理缺失值】")

df = titanic.copy()

# 3.1 查看缺失值比例
missing_ratio = df.isnull().sum() / len(df) * 100
print("\n缺失值比例（%）：")
print(missing_ratio)

# 3.2 删除缺失率过高的列（这里没有，跳过）

# 3.3 填充缺失值
print("\n【3.3 填充缺失值】")

# Age：用中位数填充
age_median = df['age'].median()
df['age_filled'] = df['age'].fillna(age_median)
print(f"Age中位数：{age_median}")

# Embarked：用众数填充
embarked_mode = df['embarked'].mode()[0]
df['embarked_filled'] = df['embarked'].fillna(embarked_mode)
print(f"Embarked众数：{embarked_mode}")

# 3.4 插值填充（线性插值）
df['age_interp'] = df['age'].interpolate(method='linear')
print(f"\n插值填充后的age前10个值：")
print(df[['age', 'age_filled', 'age_interp']].head(10))

# 3.5 删除缺失值（dropna）
df_clean = df.dropna(subset=['age', 'embarked', 'fare'])
print(f"\n删除缺失值后形状：{df_clean.shape}")


# ========== 4. 处理重复记录 ==========
print("\n【4. 处理重复记录】")

# 添加一些重复行用于演示
df_demo = df.copy()
df_demo = pd.concat([df_demo, df_demo.iloc[:3]], ignore_index=True)
print(f"添加重复行后形状：{df_demo.shape}")

# 检测重复
duplicates = df_demo.duplicated()
print(f"重复行数：{duplicates.sum()}")

# 删除重复
df_demo = df_demo.drop_duplicates()
print(f"删除重复后形状：{df_demo.shape}")

# 基于指定列检测重复
df_demo2 = df.copy()
# 假设有重复的乘客
df_demo2 = pd.concat([df_demo2, df_demo2.iloc[:5].copy()], ignore_index=True)
duplicates_subset = df_demo2.duplicated(subset=['sex', 'age', 'fare'])
print(f"\n基于[sex, age, fare]的重复行数：{duplicates_subset.sum()}")


# ========== 5. 数据类型转换 ==========
print("\n【5. 数据类型转换】")

# 查看当前类型
print("\n转换前类型：")
print(df[['survived', 'pclass', 'age', 'fare']].dtypes)

# 转换为分类类型
df['survived_cat'] = df['survived'].astype('category')
df['pclass_cat'] = df['pclass'].astype('category')

# 转换为字符串
df['sex_str'] = df['sex'].astype('str')

# 转换为整数
df['age_int'] = df['age_filled'].astype('int')

print("\n转换后类型：")
print(df[['survived_cat', 'pclass_cat', 'sex_str', 'age_int']].dtypes)


# ========== 6. 格式标准化 ==========
print("\n【6. 格式标准化】")

# 6.1 字符串标准化
df['sex_std'] = df['sex'].str.lower().str.strip()
df['embarked_std'] = df['embarked'].str.upper().str.strip()
print(f"\n标准化后的性别值：{df['sex_std'].unique()}")
print(f"标准化后的港口值：{df['embarked_std'].unique()}")

# 6.2 日期时间处理（演示）
dates = pd.date_range('2020-01-01', periods=10)
df_dates = pd.DataFrame({'date': dates})
df_dates['year'] = df_dates['date'].dt.year
df_dates['month'] = df_dates['date'].dt.month
df_dates['day'] = df_dates['date'].dt.day
df_dates['weekday'] = df_dates['date'].dt.day_name()
print(f"\n日期处理演示：")
print(df_dates)

# 6.3 数值标准化
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Z-score标准化
scaler = StandardScaler()
df['age_standardized'] = scaler.fit_transform(df[['age_filled']])
print(f"\nAge标准化后均值和标准差：")
print(f"均值：{df['age_standardized'].mean():.4f}")
print(f"标准差：{df['age_standardized'].std():.4f}")

# Min-Max归一化
scaler = MinMaxScaler()
df['fare_normalized'] = scaler.fit_transform(df[['fare']])
print(f"\nFare归一化后范围：")
print(f"最小值：{df['fare_normalized'].min():.4f}")
print(f"最大值：{df['fare_normalized'].max():.4f}")


# ========== 7. 异常值处理 ==========
print("\n【7. 异常值处理】")

# 7.1 使用IQR检测异常值
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower) | (data[column] > upper)]
    return outliers, lower, upper

# 检测age和fare的异常值
age_outliers, age_lower, age_upper = detect_outliers_iqr(df, 'age')
fare_outliers, fare_lower, fare_upper = detect_outliers_iqr(df, 'fare')

print(f"\nAge异常值检测：")
print(f"  正常范围：{age_lower:.2f} ~ {age_upper:.2f}")
print(f"  异常值数量：{len(age_outliers)}")
print(f"  异常值比例：{len(age_outliers)/len(df)*100:.2f}%")

print(f"\nFare异常值检测：")
print(f"  正常范围：{fare_lower:.2f} ~ {fare_upper:.2f}")
print(f"  异常值数量：{len(fare_outliers)}")
print(f"  异常值比例：{len(fare_outliers)/len(df)*100:.2f}%")

# 7.2 处理异常值（截断）
df['age_capped'] = df['age'].clip(lower=age_lower, upper=age_upper)
print(f"\nAge截断后范围：{df['age_capped'].min():.2f} ~ {df['age_capped'].max():.2f}")


# ========== 8. 导出清洗后的数据 ==========
print("\n【8. 导出清洗后的数据】")

# 选择需要保存的列
df_final = df[['survived', 'pclass', 'sex_std', 'age_filled', 'fare',
               'embarked_std', 'age_standardized', 'fare_normalized']]
df_final = df_final.rename(columns={
    'sex_std': 'sex',
    'age_filled': 'age',
    'embarked_std': 'embarked'
})

print(f"清洗后数据形状：{df_final.shape}")
print("\n清洗后前5行：")
print(df_final.head())

# 保存到CSV（可选）
# df_final.to_csv('titanic_cleaned.csv', index=False)
# print("\n数据已保存到 titanic_cleaned.csv")