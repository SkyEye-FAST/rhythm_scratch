# -*- encoding: utf-8 -*-
"""Arcaea Songlist提取工具"""

import json
import os

P = (
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")
    + os.path.sep
)

# 打开songlist
with open(os.path.join(P + "songlist"), "rb") as f:
    s = json.load(f)

# 提取数据
l = []
for element in s["songs"]:
    title = element["title_localized"]["en"]
    l.append(title)

# 写入曲库
with open(os.path.join(P + "dict"), "w", encoding="utf-8") as output:
    for line in l:
        output.write(line + "\n")
