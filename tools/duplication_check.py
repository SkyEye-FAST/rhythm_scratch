# -*- encoding: utf-8 -*-
"""曲库重复内容检查器"""

from collections import Counter  # 引入Counter


def load_dict(file_path: str):
    """加载曲库为列表函数"""
    with open(file_path, "r", encoding="utf-8") as dict_file:
        return [line.strip() for line in dict_file]


dict_path = input("需要查重的曲库路径：")
dict_content_counter = dict(Counter(load_dict(dict_path)))

# 输出重复元素和重复次数
print({key: value for key, value in dict_content_counter.items() if value > 1})
