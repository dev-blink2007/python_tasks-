"""
学生成绩管理系统（简化版）
"""

# 存储所有学生信息
students = {}

while True:
    print("\n" + "=" * 30)
    print("1. 录入成绩")
    print("2. 查询成绩")
    print("3. 统计成绩")
    print("4. 显示所有学生")
    print("5. 退出")
    print("=" * 30)

    choice = input("请选择：")

    if choice == '1':  # 录入
        name = input("姓名：")
        sid = input("学号：")
        if sid in students:
            print("学号已存在！")
            continue

        scores = {}
        while True:
            subject = input("科目（输入q结束）：")
            if subject == 'q':
                break
            score = float(input(f"{subject}成绩："))
            scores[subject] = score

        students[sid] = {'name': name, 'scores': scores}
        print(f"✓ {name}录入成功！")

    elif choice == '2':  # 查询
        sid = input("请输入学号：")
        if sid in students:
            s = students[sid]
            print(f"\n姓名：{s['name']}")
            for sub, sc in s['scores'].items():
                print(f"{sub}：{sc}")
            avg = sum(s['scores'].values()) / len(s['scores'])
            print(f"平均分：{avg:.2f}")
        else:
            print("未找到该学生！")

    elif choice == '3':  # 统计
        if not students:
            print("暂无学生！")
            continue

        all_avg = []
        for sid, s in students.items():
            scores = s['scores'].values()
            avg = sum(scores) / len(scores)
            all_avg.append(avg)
            print(f"{s['name']}：平均分{avg:.2f}")

        print(f"\n总平均分：{sum(all_avg) / len(all_avg):.2f}")
        print(f"最高平均分：{max(all_avg):.2f}")
        print(f"最低平均分：{min(all_avg):.2f}")

    elif choice == '4':  # 显示所有
        if not students:
            print("暂无学生！")
        else:
            print("\n学号\t姓名")
            for sid, s in students.items():
                print(f"{sid}\t{s['name']}")

    elif choice == '5':
        print("再见！")
        break

    else:
        print("无效选择！")