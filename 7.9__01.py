"""
成绩分析命令行工具（简化版）
"""

import numpy as np

# 存储数据
names = []
scores = []


# ========== 功能1：录入成绩 ==========
def input_scores():
    global names, scores
    print("\n" + "-" * 30)
    print("【录入成绩】")

    n = int(input("学生人数："))
    names = []
    scores = []

    for i in range(n):
        name = input(f"第{i + 1}个学生姓名：")
        score = float(input(f"{name}的成绩："))
        names.append(name)
        scores.append(score)

    print(f"✓ 录入{n}名学生成功！")


# ========== 功能2：成绩统计 ==========
def show_stats():
    if not scores:
        print("请先录入成绩！")
        return

    arr = np.array(scores)
    print("\n" + "-" * 30)
    print("【成绩统计】")
    print(f"人数：{len(scores)}")
    print(f"最高分：{arr.max():.1f}")
    print(f"最低分：{arr.min():.1f}")
    print(f"平均分：{arr.mean():.2f}")
    print(f"标准差：{arr.std():.2f}")

    # 及格人数
    passed = np.sum(arr >= 60)
    print(f"及格：{passed}人（{passed / len(scores) * 100:.1f}%）")


# ========== 功能3：成绩排名 ==========
def show_ranking():
    if not scores:
        print("请先录入成绩！")
        return

    arr = np.array(scores)
    idx = np.argsort(arr)[::-1]  # 从高到低排序

    print("\n" + "-" * 30)
    print("【成绩排名】")
    print("名次\t姓名\t成绩")
    for rank, i in enumerate(idx, 1):
        print(f"{rank}\t{names[i]}\t{arr[i]:.1f}")


# ========== 功能4：成绩分布 ==========
def show_distribution():
    if not scores:
        print("请先录入成绩！")
        return

    arr = np.array(scores)

    # 等级区间
    levels = {
        '优秀(90+)': 90,
        '良好(80-89)': 80,
        '中等(70-79)': 70,
        '及格(60-69)': 60,
        '不及格(<60)': 0
    }

    print("\n" + "-" * 30)
    print("【成绩分布】")
    for level, threshold in levels.items():
        if level == '不及格(<60)':
            count = np.sum(arr < 60)
        else:
            # 计算在各区间的人数
            if level == '优秀(90+)':
                count = np.sum(arr >= 90)
            elif level == '良好(80-89)':
                count = np.sum((arr >= 80) & (arr < 90))
            elif level == '中等(70-79)':
                count = np.sum((arr >= 70) & (arr < 80))
            elif level == '及格(60-69)':
                count = np.sum((arr >= 60) & (arr < 70))
            else:
                count = 0

        percent = count / len(arr) * 100
        bar = '█' * int(percent)
        print(f"{level}：{count}人（{percent:.1f}%）{bar}")


# ========== 功能5：查询学生 ==========
def query_student():
    if not scores:
        print("请先录入成绩！")
        return

    name = input("请输入要查询的学生姓名：")

    for i, n in enumerate(names):
        if n == name:
            print(f"{name}的成绩：{scores[i]:.1f}分")
            return

    print(f"未找到学生：{name}")


# ========== 主程序 ==========
def main():
    while True:
        print("\n" + "=" * 30)
        print("  成绩分析系统")
        print("=" * 30)
        print("1. 录入成绩")
        print("2. 成绩统计")
        print("3. 成绩排名")
        print("4. 成绩分布")
        print("5. 查询学生")
        print("6. 退出")
        print("=" * 30)

        choice = input("请选择（1-6）：")

        if choice == '1':
            input_scores()
        elif choice == '2':
            show_stats()
        elif choice == '3':
            show_ranking()
        elif choice == '4':
            show_distribution()
        elif choice == '5':
            query_student()
        elif choice == '6':
            print("再见！")
            break
        else:
            print("无效选择！")

        input("\n按回车继续...")


# 运行
if __name__ == "__main__":
    main()