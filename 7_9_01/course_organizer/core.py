"""
核心逻辑模块
"""

import shutil
from pathlib import Path
from datetime import datetime
from .rules import get_category


def scan_files(source_dir):
    """扫描源目录中的所有文件"""
    files = []
    for item in Path(source_dir).iterdir():
        if item.is_file():
            files.append(item)
    return files


def generate_plan(source_dir, target_dir):
    """
    生成整理计划

    返回：
        plan: 计划列表
        stats: 分类统计
    """
    plan = []
    stats = {}
    files = scan_files(source_dir)

    for file_path in files:
        filename = file_path.name
        category = get_category(filename)

        plan.append({
            'source': file_path,
            'category': category,
            'target_dir': Path(target_dir) / category,
            'target_path': Path(target_dir) / category / filename,
            'filename': filename
        })

        stats[category] = stats.get(category, 0) + 1

    return plan, stats


def print_plan(plan, stats, source_dir, target_dir, dry_run):
    """打印整理计划"""
    print("\n" + "=" * 50)
    print("【整理计划】")
    print(f"源目录：{source_dir}")
    print(f"目标目录：{target_dir}")
    print(f"模式：{'预览（不实际操作）' if dry_run else '执行'}")
    print("=" * 50)

    # 按分类分组
    grouped = {}
    for item in plan:
        cat = item['category']
        grouped.setdefault(cat, []).append(item)

    for cat, items in sorted(grouped.items()):
        print(f"\n📁 {cat}/ ({len(items)}个)")
        for item in items:
            print(f"   {item['filename']}")
            print(f"      └─> {item['target_path']}")

    print("\n" + "=" * 50)
    print(f"总计：{len(plan)} 个文件")
    for cat, count in sorted(stats.items()):
        print(f"  {cat}：{count} 个")


def get_unique_path(path):
    """如果文件已存在，生成不重复的路径"""
    if not path.exists():
        return path

    parent = path.parent
    stem = path.stem
    suffix = path.suffix
    count = 1

    while True:
        new_path = parent / f"{stem}_{count}{suffix}"
        if not new_path.exists():
            return new_path
        count += 1


def execute_plan(plan, target_dir, mode='copy'):
    """
    执行整理计划

    参数：
        plan: 整理计划
        target_dir: 目标目录
        mode: 'copy' 或 'move'
    """
    print(f"\n【开始整理】模式：{mode}")

    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)

    results = []

    for item in plan:
        source = item['source']
        target = get_unique_path(item['target_path'])

        # 创建目标目录
        target.parent.mkdir(parents=True, exist_ok=True)

        try:
            if mode == 'copy':
                shutil.copy2(source, target)
            else:
                shutil.move(str(source), str(target))

            results.append({
                'filename': item['filename'],
                'source': source,
                'target': target,
                'success': True
            })
            print(f"✓ {mode}：{item['filename']}")

        except Exception as e:
            results.append({
                'filename': item['filename'],
                'source': source,
                'target': target,
                'success': False,
                'error': str(e)
            })
            print(f"✗ 失败：{item['filename']} - {e}")

    return results


def generate_report(results, stats, source_dir, target_dir, mode):
    """生成整理报告"""
    report_path = Path(target_dir) / "整理报告.txt"

    lines = []
    lines.append("=" * 50)
    lines.append("课程资料整理报告")
    lines.append("=" * 50)
    lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"源目录：{source_dir}")
    lines.append(f"目标目录：{target_dir}")
    lines.append(f"操作模式：{mode}")
    lines.append("=" * 50)

    total = len(results)
    success = sum(1 for r in results if r['success'])

    lines.append(f"\n【总览】")
    lines.append(f"文件总数：{total}")
    lines.append(f"成功：{success}")
    lines.append(f"失败：{total - success}")

    lines.append(f"\n【分类统计】")
    for cat, count in sorted(stats.items()):
        lines.append(f"  {cat}：{count} 个")

    lines.append(f"\n【详细记录】")
    for r in results:
        status = "✓" if r['success'] else "✗"
        lines.append(f"{status} {r['filename']}")
        lines.append(f"   源：{r['source']}")
        lines.append(f"   目标：{r['target']}")

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n✅ 报告已生成：{report_path}")