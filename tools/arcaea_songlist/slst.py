# -*- encoding: utf-8 -*-
"""Arcaea Songlist提取工具"""

import json
from pathlib import Path

P = Path(__file__).resolve().parent

# 打开songlist
with open(P / "songlist", "rb") as f:
    s = json.load(f)

# 提取数据
l = [song["title_localized"]["en"] for song in s["songs"]]

# 写入曲库
with open(P / "dict", "w", encoding="utf-8") as output:
    for line in l:
        output.write(line + "\n")
