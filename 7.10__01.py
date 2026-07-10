"""
Pandas 课堂作业：电商订单经营分析挑战
"""

import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

# ========== 数据准备 ==========
orders = pd.DataFrame({
    'order_id': [f'O{number}' for number in range(1001, 1019)],
    'region': ['华东','华北','华南','华东','西南','华北','华南','华东','西南','华北','华东','华南','西南','华东','华北','华南','华东','西南'],
    'product': ['机械键盘','无线鼠标','显示器','扩展坞','机械键盘','显示器','无线鼠标','显示器','扩展坞','机械键盘','无线鼠标','扩展坞','显示器','机械键盘','扩展坞','显示器','无线鼠标','机械键盘'],
    'category': ['外设','外设','显示设备','配件','外设','显示设备','外设','显示设备','配件','外设','外设','配件','显示设备','外设','配件','显示设备','外设','外设'],
    'quantity': [2,3,1,4,5,2,6,1,3,2,8,2,1,3,5,2,4,6],
    'unit_price': [289,129,1299,399,289,1299,129,1299,399,289,129,399,1299,289,399,1299,129,289],
    'member_level': ['金卡','普通','银卡','金卡','银卡','普通','金卡','银卡','普通','金卡','银卡','金卡','普通','银卡','金卡','金卡','普通','银卡'],
    'coupon_rate': [0.05,0.00,0.08,0.10,0.05,0.00,0.12,0.05,0.00,0.08,0.10,0.05,0.00,0.12,0.05,0.08,0.00,0.10],
    'salesperson': ['小林','小周','小陈','小林','小赵','小周','小陈','小林','小赵','小周','小林','小陈','小赵','小林','小周','小陈','小林','小赵']
})

print("="*60)
print("原始数据：")
print(orders)
print("\n")


# ========== 任务1：快速理解数据 ==========
print("="*60)
print("任务1：快速理解数据")
print("="*60)

# 1. 行数、列数、列名
print(f"\n行数：{orders.shape[0]}")
print(f"列数：{orders.shape[1]}")
print(f"列名：{list(orders.columns)}")

# 2. 取出单列和多列
region_col = orders['region']
multi_cols = orders[['order_id', 'product', 'quantity']]
print(f"\nregion列类型：{type(region_col)}")
print(f"多列类型：{type(multi_cols)}")

# 3. iloc取第4~8行、前4列（索引从0开始，4:9取第5~9行）
print(f"\niloc取第4~8行、前4列：")
print(orders.iloc[4:9, :4])

# 4. loc找出华东订单
print(f"\n华东订单的order_id、product、member_level：")
print(orders.loc[orders['region'] == '华东', ['order_id', 'product', 'member_level']])

# 5. 回答
print("\n【回答】为什么长期维护的业务代码通常更推荐loc？")
print("因为loc使用标签索引，代码可读性更强，当列的顺序发生变化时，")
print("loc仍然能正确工作，而iloc依赖位置，列顺序变动会导致错误。")


# ========== 任务2：构造订单结算指标 ==========
print("\n" + "="*60)
print("任务2：构造订单结算指标")
print("="*60)

# 创建analysis表
analysis = orders.copy()

# 计算各列
analysis['gross_amount'] = analysis['quantity'] * analysis['unit_price']

# 会员折扣：金卡10%，银卡5%，普通0%
analysis['member_discount'] = np.where(
    analysis['member_level'] == '金卡', 0.10,
    np.where(analysis['member_level'] == '银卡', 0.05, 0.00)
)

analysis['payable_amount'] = (
    analysis['gross_amount'] *
    (1 - analysis['member_discount']) *
    (1 - analysis['coupon_rate'])
)

analysis['shipping_fee'] = np.where(
    analysis['payable_amount'] >= 1000, 0, 20
)

analysis['final_amount'] = analysis['payable_amount'] + analysis['shipping_fee']

# 保留两位小数
analysis['gross_amount'] = analysis['gross_amount'].round(2)
analysis['payable_amount'] = analysis['payable_amount'].round(2)
analysis['final_amount'] = analysis['final_amount'].round(2)

print("\n前8行相关字段：")
print(analysis[['order_id', 'gross_amount', 'member_discount',
                'payable_amount', 'shipping_fee', 'final_amount']].head(8))


# ========== 任务3：复杂条件筛选 ==========
print("\n" + "="*60)
print("任务3：复杂条件筛选 - 重点跟进订单")
print("="*60)

# 定义三个布尔条件
cond1 = analysis['region'].isin(['华东', '华南'])
cond2 = analysis['final_amount'] >= 700
cond3 = (analysis['quantity'] >= 2) | (analysis['member_level'] == '金卡')

# 组合条件
mask = cond1 & cond2 & cond3

result = analysis.loc[mask, ['order_id', 'region', 'product',
                             'quantity', 'member_level', 'final_amount']]
result = result.sort_values('final_amount', ascending=False)

print("\n重点跟进订单：")
print(result)

print("\n【回答】& 和 | 两侧为什么要加括号？")
print("因为&和|的优先级低于比较运算符（如>=、==），")
print("不加括号会导致运算顺序错误，例如 cond1 & cond2 会先执行 cond1 & cond2，")
print("但 cond1 & cond2 会先按位运算再比较，结果不符合预期。")


# ========== 任务4：封装可复用处理函数 ==========
print("\n" + "="*60)
print("任务4：封装可复用处理函数")
print("="*60)

def add_order_level(df):
    """根据final_amount添加订单等级"""
    result = df.copy()
    result['order_level'] = np.where(
        result['final_amount'] >= 2000, '战略订单',
        np.where(result['final_amount'] >= 1000, '重点订单', '普通订单')
    )
    return result

leveled_orders = analysis.pipe(add_order_level)

print("\n各等级订单数：")
print(leveled_orders['order_level'].value_counts())


# ========== 任务5：一条链完成经营汇总 ==========
print("\n" + "="*60)
print("任务5：一条链完成经营汇总")
print("="*60)

region_report = (
    analysis
    .pipe(add_order_level)
    .query('final_amount >= 500')
    .groupby(['region', 'order_level'])
    .agg(
        order_count=('order_id', 'count'),
        quantity_sum=('quantity', 'sum'),
        revenue_sum=('final_amount', 'sum'),
        revenue_mean=('final_amount', 'mean')
    )
    .sort_values('revenue_sum', ascending=False)
)

print("\n地区经营汇总报告：")
print(region_report)


# ========== 任务6：经营诊断与表达 ==========
print("\n" + "="*60)
print("任务6：经营诊断与表达")
print("="*60)

# 1. 哪位销售人员成交金额最高？
sales_summary = analysis.groupby('salesperson')['final_amount'].sum().sort_values(ascending=False)
top_salesperson = sales_summary.index[0]
top_sales_amount = sales_summary.iloc[0]

print(f"\n1. 成交金额最高的销售人员：{top_salesperson}")
print(f"   总成交金额：{top_sales_amount:.2f}")

# 2. 该销售人员成交金额最高的地区
sales_region = (
    analysis[analysis['salesperson'] == top_salesperson]
    .groupby('region')['final_amount']
    .sum()
    .sort_values(ascending=False)
)
top_region = sales_region.index[0]
top_region_amount = sales_region.iloc[0]

print(f"\n2. 该销售人员成交金额最高的地区：{top_region}")
print(f"   地区成交金额：{top_region_amount:.2f}")

# 3. 地区贡献率
contribution_rate = top_region_amount / top_sales_amount

print(f"\n3. 地区贡献率：{contribution_rate:.2%}")

# 业务结论
print("\n【业务结论】")
print(f"{top_salesperson}的{top_region}地区成交金额为{top_region_amount:.2f}元，")
print(f"占其总成交金额{top_sales_amount:.2f}元的{contribution_rate:.2%}，")
print(f"建议重点关注{top_region}市场，巩固{top_salesperson}在该地区的优势。")