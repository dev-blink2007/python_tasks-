"""
任务2：空气质量数据分析与可视化
使用模拟的空气质量数据
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

print("="*60)
print("任务2：空气质量数据分析与可视化")
print("="*60)

# ========== 1. 生成模拟空气质量数据 ==========
print("\n【1. 生成模拟数据】")

np.random.seed(42)

# 生成时间序列（2023年全年，每小时）
dates = pd.date_range('2023-01-01', '2023-12-31 23:00:00', freq='H')

# 生成污染物数据
n = len(dates)

# 基础趋势 + 季节性 + 随机噪声
def generate_pollutant(base, seasonal_amp, noise_std):
    """生成污染物数据"""
    # 年份时间
    t = np.arange(n)
    # 日周期
    daily = seasonal_amp * 0.3 * np.sin(2 * np.pi * t / 24)
    # 年周期
    yearly = seasonal_amp * 0.7 * np.sin(2 * np.pi * t / (24*365))
    # 随机噪声
    noise = np.random.normal(0, noise_std, n)
    # 自相关性
    noise_corr = np.zeros(n)
    noise_corr[0] = noise[0]
    for i in range(1, n):
        noise_corr[i] = 0.7 * noise_corr[i-1] + 0.3 * noise[i]
    # 最终值
    values = base + daily + yearly + noise_corr
    return np.maximum(values, 0)  # 不能为负

# PM2.5
pm25 = generate_pollutant(50, 30, 15)

# PM10
pm10 = generate_pollutant(80, 40, 20)

# SO2
so2 = generate_pollutant(15, 8, 5)

# NO2
no2 = generate_pollutant(25, 12, 8)

# O3
o3 = generate_pollutant(60, 20, 10)

# 创建DataFrame
air_data = pd.DataFrame({
    'datetime': dates,
    'PM2.5': pm25,
    'PM10': pm10,
    'SO2': so2,
    'NO2': no2,
    'O3': o3
})

print(f"数据形状：{air_data.shape}")
print(f"时间范围：{air_data['datetime'].min()} ~ {air_data['datetime'].max()}")
print("\n前5行数据：")
print(air_data.head())

print("\n数据统计描述：")
print(air_data.describe())


# ========== 2. 时间序列特征分析 ==========
print("\n【2. 时间序列特征分析】")

# 添加时间特征
air_data['year'] = air_data['datetime'].dt.year
air_data['month'] = air_data['datetime'].dt.month
air_data['day'] = air_data['datetime'].dt.day
air_data['hour'] = air_data['datetime'].dt.hour
air_data['weekday'] = air_data['datetime'].dt.dayofweek
air_data['quarter'] = air_data['datetime'].dt.quarter

# 按月份聚合
monthly_avg = air_data.groupby('month')[['PM2.5', 'PM10', 'SO2', 'NO2', 'O3']].mean()
print("\n各月份平均浓度：")
print(monthly_avg.round(2))

# 按小时聚合
hourly_avg = air_data.groupby('hour')[['PM2.5', 'PM10', 'SO2', 'NO2', 'O3']].mean()
print("\n各小时平均浓度（前6小时）：")
print(hourly_avg.head(6).round(2))


# ========== 3. 污染物统计指标 ==========
print("\n【3. 污染物统计指标】")

pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3']
stats = {}

for p in pollutants:
    stats[p] = {
        'mean': air_data[p].mean(),
        'std': air_data[p].std(),
        'min': air_data[p].min(),
        'max': air_data[p].max(),
        'median': air_data[p].median(),
        'q25': air_data[p].quantile(0.25),
        'q75': air_data[p].quantile(0.75)
    }

stats_df = pd.DataFrame(stats).T
print("\n各污染物统计指标：")
print(stats_df.round(2))


# ========== 4. 相关性分析 ==========
print("\n【4. 污染物相关性分析】")

# 计算相关系数矩阵
corr_matrix = air_data[pollutants].corr()
print("\n相关系数矩阵：")
print(corr_matrix.round(3))

# 找出相关性最强的污染物对
corr_pairs = []
for i in range(len(pollutants)):
    for j in range(i+1, len(pollutants)):
        corr_pairs.append((pollutants[i], pollutants[j], corr_matrix.iloc[i, j]))

corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
print(f"\n相关性最强的污染物对：{corr_pairs[0][0]} 和 {corr_pairs[0][1]}，相关系数：{corr_pairs[0][2]:.3f}")


# ========== 5. 季节性变化规律 ==========
print("\n【5. 季节性变化规律】")

# 按季度分组
quarterly_avg = air_data.groupby('quarter')[pollutants].mean()
print("\n各季度平均浓度：")
print(quarterly_avg.round(2))

# 判断污染最严重的季节
for p in pollutants:
    max_quarter = quarterly_avg[p].idxmax()
    print(f"{p}污染最严重的季度：Q{max_quarter}")

# 按月份统计
monthly_stats = air_data.groupby('month')[pollutants].agg(['mean', 'std'])
print("\n各月份统计（PM2.5为例）：")
print(monthly_stats['PM2.5'].round(2))


# ========== 6. 数据可视化 ==========
print("\n【6. 生成可视化图表】")

# 创建大图
fig = plt.figure(figsize=(16, 14))

# 6.1 时间序列折线图（子图1）
ax1 = plt.subplot(3, 2, 1)
# 采样显示（每24小时取一点）
sample_rate = 24
dates_sample = air_data['datetime'][::sample_rate]
for p in ['PM2.5', 'PM10', 'NO2']:
    plt.plot(dates_sample, air_data[p][::sample_rate], label=p, alpha=0.7)
plt.xlabel('时间')
plt.ylabel('浓度 (μg/m³)')
plt.title('主要污染物时间序列变化')
plt.legend()
plt.grid(True, alpha=0.3)

# 6.2 月度变化柱状图（子图2）
ax2 = plt.subplot(3, 2, 2)
monthly_mean = air_data.groupby('month')[pollutants].mean()
monthly_mean.plot(kind='bar', ax=ax2, width=0.8)
plt.xlabel('月份')
plt.ylabel('平均浓度 (μg/m³)')
plt.title('各污染物月度变化趋势')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=0)

# 6.3 小时变化折线图（子图3）
ax3 = plt.subplot(3, 2, 3)
hourly_mean = air_data.groupby('hour')[pollutants].mean()
for p in pollutants:
    plt.plot(hourly_mean.index, hourly_mean[p], label=p, marker='o', markersize=3)
plt.xlabel('小时')
plt.ylabel('平均浓度 (μg/m³)')
plt.title('污染物日变化规律')
plt.legend()
plt.grid(True, alpha=0.3)

# 6.4 相关性热力图（子图4）
ax4 = plt.subplot(3, 2, 4)
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
            fmt='.3f', square=True, ax=ax4, cbar_kws={'shrink': 0.8})
plt.title('污染物相关系数热力图')
plt.xticks(rotation=45)
plt.yticks(rotation=0)

# 6.5 散点图（PM2.5 vs PM10）（子图5）
ax5 = plt.subplot(3, 2, 5)
sample_data = air_data.sample(2000)  # 抽样
plt.scatter(sample_data['PM2.5'], sample_data['PM10'], alpha=0.3, s=10)
plt.xlabel('PM2.5浓度 (μg/m³)')
plt.ylabel('PM10浓度 (μg/m³)')
plt.title('PM2.5与PM10相关性散点图')

# 添加拟合线
z = np.polyfit(sample_data['PM2.5'], sample_data['PM10'], 1)
p = np.poly1d(z)
x_line = np.linspace(sample_data['PM2.5'].min(), sample_data['PM2.5'].max(), 100)
plt.plot(x_line, p(x_line), 'r-', linewidth=2, label=f'拟合线 (斜率={z[0]:.2f})')
plt.legend()
plt.grid(True, alpha=0.3)

# 6.6 箱线图（按季节）（子图6）
ax6 = plt.subplot(3, 2, 6)
air_data['season'] = air_data['quarter'].map({1: '春', 2: '夏', 3: '秋', 4: '冬'})
sns.boxplot(data=air_data, x='season', y='PM2.5', ax=ax6, palette='Set2')
plt.xlabel('季节')
plt.ylabel('PM2.5浓度 (μg/m³)')
plt.title('PM2.5季节性分布箱线图')
plt.grid(True, alpha=0.3)

# 调整布局
plt.tight_layout()
plt.show()

print("\n可视化图表已生成！")


# ========== 7. 空气质量指数(AQI)计算 ==========
print("\n【7. 空气质量指数计算】")

# 简化的AQI计算（主要污染物PM2.5）
def calculate_aqi(pm25_value):
    """根据PM2.5计算AQI（简化版）"""
    if pm25_value <= 12:
        return pm25_value / 12 * 50
    elif pm25_value <= 35.4:
        return (pm25_value - 12.1) / (35.4 - 12.1) * 50 + 51
    elif pm25_value <= 55.4:
        return (pm25_value - 35.5) / (55.4 - 35.5) * 50 + 101
    elif pm25_value <= 150.4:
        return (pm25_value - 55.5) / (150.4 - 55.5) * 100 + 151
    elif pm25_value <= 250.4:
        return (pm25_value - 150.5) / (250.4 - 150.5) * 100 + 251
    else:
        return (pm25_value - 250.5) / (350.4 - 250.5) * 100 + 351

air_data['AQI'] = air_data['PM2.5'].apply(calculate_aqi)

# AQI等级
def aqi_level(aqi):
    if aqi <= 50:
        return '优'
    elif aqi <= 100:
        return '良'
    elif aqi <= 150:
        return '轻度污染'
    elif aqi <= 200:
        return '中度污染'
    elif aqi <= 300:
        return '重度污染'
    else:
        return '严重污染'

air_data['AQI_level'] = air_data['AQI'].apply(aqi_level)

# 统计各等级天数
print("\nAQI等级分布：")
print(air_data['AQI_level'].value_counts())

# 良好天数比例
good_days = air_data[air_data['AQI'] <= 100]['datetime'].dt.date.nunique()
total_days = air_data['datetime'].dt.date.nunique()
print(f"\n良好及以上天数：{good_days}天（{good_days/total_days*100:.1f}%）")


# ========== 8. 总结输出 ==========
print("\n" + "="*60)
print("分析总结")
print("="*60)

print(f"\n1. 数据概况：")
print(f"   - 共{len(air_data)}条记录，覆盖{total_days}天")

print(f"\n2. 主要污染物统计：")
for p in pollutants:
    print(f"   - {p}：均值{air_data[p].mean():.1f}，最大值{air_data[p].max():.1f}")

print(f"\n3. 季节性特征：")
print(f"   - 冬季（Q1）：PM2.5平均{quarterly_avg.loc[1, 'PM2.5']:.1f}")
print(f"   - 夏季（Q3）：PM2.5平均{quarterly_avg.loc[3, 'PM2.5']:.1f}")
print(f"   - PM2.5冬季比夏季高{quarterly_avg.loc[1, 'PM2.5']/quarterly_avg.loc[3, 'PM2.5']:.1f}倍")

print(f"\n4. 相关性分析：")
print(f"   - 相关性最强：{corr_pairs[0][0]}和{corr_pairs[0][1]} ({corr_pairs[0][2]:.3f})")

print(f"\n5. 空气质量：")
print(f"   - 全年优良天数占比：{good_days/total_days*100:.1f}%")
print(f"   - 主要污染等级：{air_data['AQI_level'].mode()[0]}")