import json

# 打开songlist
with open("songlist", "rb") as f:
    s = json.load(f)

# 提取数据
l = []

for everything in s["songs"]:
    title = everything["title_localized"]["en"]
    l.append(title)

# 写入曲库
output = open("dict", "w", encoding="utf-8")
for line in l:
    output.write(line + "\n")
output.close()