"""
分类规则模块
"""

# 关键字规则：文件名包含这些关键字就归入 homework
KEYWORD_RULES = {
    'homework': ['作业', '练习', '实验', '任务']
}

# 后缀规则
EXTENSION_RULES = {
    'slides': ['.ppt', '.pptx', '.key'],
    'code': ['.py', '.ipynb', '.c', '.cpp', '.java'],
    'data': ['.csv', '.xlsx', '.json'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.md'],
    'images': ['.png', '.jpg', '.jpeg', '.gif']
}

DEFAULT = 'others'


def get_category(filename):
    """根据文件名返回分类目录"""
    import os

    # 1. 先检查关键字
    for category, keywords in KEYWORD_RULES.items():
        for kw in keywords:
            if kw in filename:
                return category

    # 2. 再检查后缀
    ext = os.path.splitext(filename)[1].lower()
    for category, exts in EXTENSION_RULES.items():
        if ext in exts:
            return category

    # 3. 默认
    return DEFAULT


def get_all_categories():
    """返回所有分类"""
    cats = set(EXTENSION_RULES.keys())
    cats.add(DEFAULT)
    cats.update(KEYWORD_RULES.keys())
    return sorted(cats)