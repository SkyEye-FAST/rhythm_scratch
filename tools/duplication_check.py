from collections import Counter  # 引入Counter

load_dict = lambda file_path: [
    line.strip() for line in open(file_path, "r", encoding="utf-8")
]

dict_path = input("需要查重的曲库路径：")
dict_content = load_dict(dict_path)
dict_content_counter = dict(Counter(dict_content))

# 输出重复元素和重复次数
print({key: value for key, value in dict_content_counter.items() if value > 1})
