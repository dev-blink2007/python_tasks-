"""
课程资料整理器 - 主程序

用法：
    python main.py --source sample_materials --target organized_materials --dry-run
    python main.py --source sample_materials --target organized_materials
    python main.py --source sample_materials --target organized_materials --mode move
"""

import sys
from pathlib import Path
from course_organizer import generate_plan, print_plan, execute_plan, generate_report


def parse_args():
    """简单解析命令行参数"""
    args = {
        'source': 'sample_materials',
        'target': 'organized_materials',
        'mode': 'copy',
        'dry_run': False
    }

    i = 0
    while i < len(sys.argv):
        if sys.argv[i] == '--source' and i + 1 < len(sys.argv):
            args['source'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--target' and i + 1 < len(sys.argv):
            args['target'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--mode' and i + 1 < len(sys.argv):
            args['mode'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--dry-run':
            args['dry_run'] = True
            i += 1
        else:
            i += 1

    return args


def main():
    args = parse_args()

    # 检查源目录
    source_dir = Path(args['source'])
    if not source_dir.exists():
        print(f"错误：源目录不存在 - {source_dir}")
        sys.exit(1)

    # 生成计划
    plan, stats = generate_plan(args['source'], args['target'])

    if not plan:
        print("没有文件需要整理")
        return

    # 显示计划
    print_plan(plan, stats, args['source'], args['target'], args['dry_run'])

    # 预览模式退出
    if args['dry_run']:
        return

    # 确认执行
    confirm = input("\n确认执行？(y/n)：")
    if confirm.lower() != 'y':
        print("已取消")
        return

    # 执行
    results = execute_plan(plan, args['target'], args['mode'])

    # 生成报告
    generate_report(results, stats, args['source'], args['target'], args['mode'])


if __name__ == "__main__":
    main()