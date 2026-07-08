"""
数学计算器（简化版）
"""

import math

# 历史记录文件
HISTORY_FILE = "history.txt"


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        raise ValueError("除数不能为0！")
    return a / b


def power(a, b):
    return a ** b


def sqrt(a):
    if a < 0:
        raise ValueError("不能对负数开方！")
    return math.sqrt(a)


def save_history(text):
    """保存历史"""
    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(text + "\n")


def read_history():
    """读取历史"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            print("\n历史记录：")
            print(f.read())
    except FileNotFoundError:
        print("暂无历史记录！")


def get_num(prompt):
    """获取数字（带异常处理）"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("请输入有效数字！")


while True:
    print("\n" + "=" * 30)
    print("1. 加法  2. 减法")
    print("3. 乘法  4. 除法")
    print("5. 幂运算 6. 开方")
    print("7. 查看历史")
    print("8. 退出")
    print("=" * 30)

    choice = input("请选择：")

    if choice == '8':
        print("再见！")
        break

    try:
        if choice == '1':  # 加法
            a = get_num("第一个数：")
            b = get_num("第二个数：")
            result = add(a, b)
            text = f"{a} + {b} = {result}"
            print(text)
            save_history(text)

        elif choice == '2':  # 减法
            a = get_num("被减数：")
            b = get_num("减数：")
            result = sub(a, b)
            text = f"{a} - {b} = {result}"
            print(text)
            save_history(text)

        elif choice == '3':  # 乘法
            a = get_num("第一个数：")
            b = get_num("第二个数：")
            result = mul(a, b)
            text = f"{a} × {b} = {result}"
            print(text)
            save_history(text)

        elif choice == '4':  # 除法
            a = get_num("被除数：")
            b = get_num("除数：")
            result = div(a, b)
            text = f"{a} ÷ {b} = {result}"
            print(text)
            save_history(text)

        elif choice == '5':  # 幂运算
            a = get_num("底数：")
            b = get_num("指数：")
            result = power(a, b)
            text = f"{a} ^ {b} = {result}"
            print(text)
            save_history(text)

        elif choice == '6':  # 开方
            a = get_num("要开方的数：")
            result = sqrt(a)
            text = f"√{a} = {result}"
            print(text)
            save_history(text)

        elif choice == '7':  # 查看历史
            read_history()

        else:
            print("无效选择！")

    except ValueError as e:
        print(f"错误：{e}")
    except Exception as e:
        print(f"出错：{e}")

    input("\n按回车继续...")