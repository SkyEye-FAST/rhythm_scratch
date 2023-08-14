# -*- encoding: utf-8 -*-

import re, os, sys, pyperclip, tomllib
from random import sample

# 加载配置
with open("configuration.toml", "rb") as f:
    config = tomllib.load(f)

# 常量
NUM = config["const"]["generate_amount"]  # 生成曲目数量
GUESS_CHANCES = config["const"]["guess_chances"]  # 最初刮开可用次数

# 路径
P = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "."
)  # 当前绝对路径
DICT_FOLDER = os.path.join(P, config["path"]["dict_folder"])  # 曲库路径
OUTPUT_FOLDER = os.path.join(P, config["path"]["output_folder"])  # 输出路径

# 创建输出文件夹（若不存在）
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# 加载曲库列表
games, versions, all_dicts_folder = [], [], []
for i in os.listdir(DICT_FOLDER):
    dict_config = os.path.join(DICT_FOLDER, i, "dict.toml")
    if os.path.exists(dict_config):
        all_dicts_folder.append(i)
        with open(dict_config, "rb") as f:
            toml = tomllib.load(f)
            games.append(toml["name"])
            versions.append(toml["version"])


# 定义加载曲库为列表函数
def load_dict(file_path):
    dict_content = []
    with open(os.path.join(DICT_FOLDER, file_path), "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip()
            dict_content.append(word)
    return dict_content


# 定义复制文件内容到剪贴板函数
def copy(file):
    with open(os.path.join(OUTPUT_FOLDER, file), "r", encoding="utf-8") as f:
        pyperclip.copy(f.read())


# 定义已开字符函数
def known_char(name):
    if name != []:
        s = "已开字符：" + name[0]
        for i in range(1, len(name)):
            s += "、" + name[i]
        return s + "。"
    else:
        return ""


class output:
    # 定义输出文件函数
    def to_file(name, file):
        with open(os.path.join(OUTPUT_FOLDER, file), "w", encoding="utf-8") as f:
            for i, element in enumerate(name):
                f.write(f"{i + 1}. {element}\n")

    # 定义输出暂存到文件函数
    def to_temp(known, name, file):
        with open(os.path.join(OUTPUT_FOLDER, file), "w", encoding="utf-8") as f:
            if known != "":
                f.write(known + "\n")
            for i, element in enumerate(name):
                f.write(f"{i + 1}. {element}\n")

    # 定义循环输出函数
    def loop_print(name):
        for i, element in enumerate(name):
            print(f"{i + 1}. {element}")

    # 定义输出帮助函数
    def h():
        print("可用命令：")
        print("  help | ? - 显示帮助")
        print("  exit - 退出")
        print("  version | ver | v - 列出曲库使用音游版本号")
        print("  (heart | h) add [amount] - 增加可用刮开次数")
        print("  (heart | h) remove [amount] - 减少可用刮开次数")
        print("  (open | o) [character] - 刮开指定字符")
        print("  (check | c) [index] - 将某题全部刮开")
        print("  (show | s) - 显示题目")


def main():
    print("音游猜曲名刮刮乐\n作者：SkyEye_FAST\n\n可用的曲库：")
    # 输出曲库列表
    i = 0
    while i < len(games):
        print(f"{i + 1}. {games[i]}（游戏版本：{versions[i]}）")
        i += 1
    # 选择曲库
    selected_dicts = input("请选择曲库编号，以逗号分隔：\n\n>> ").split(",")
    selected_dicts = [
        int(index.strip()) for index in selected_dicts if index.strip().isdigit()
    ]
    if len(selected_dicts) == 0:
        print("未选择任何曲库。")
        sys.exit()
    # 加载曲库
    selected_dict_content = []
    for index in selected_dicts:
        if index > 0 and index <= len(all_dicts_folder):
            dict_config = os.path.join(
                DICT_FOLDER, all_dicts_folder[index - 1], "dict.toml"
            )
            with open(dict_config, "rb") as f:
                toml = tomllib.load(f)
                for element in toml["dicts"]:
                    selected_dict_content += load_dict(
                        os.path.join(
                            DICT_FOLDER, all_dicts_folder[index - 1], "dict", element
                        )
                    )
            print(f"已加载曲库“{games[index - 1]}”。")
        else:
            print(f"编号为“{index}”的曲库不存在，忽略。")
    selected_dict_content = list(set(selected_dict_content))  # 去除重复曲目
    print(f"选择曲目总数：{len(selected_dict_content)}\n")

    # 生成答案
    answer_list = sample(selected_dict_content, 10)
    output.to_file(answer_list, "Answer")

    # 生成初始问题
    question_list = []
    for element in answer_list:
        question_list.append("*" * len(element))
    output.to_file(question_list, "Question")
    copy("Question")
    print("输入“?”来查看帮助。\n\n题目：")
    output.loop_print(question_list)

    # 刮卡
    heart = GUESS_CHANCES  # 刮开可用次数
    t = question_list  # 题目暂存
    tt = question_list  # 题目暂存的暂存
    opened_char = []  # 刮开的字符，拉丁字母大小写
    opened_char_lowercase = []  # 刮开的字符，拉丁字母全部小写

    while heart > 0 and t != answer_list:
        command = input("\n>> ")  # 输入命令

        # 替换命令别名
        command_aliases = {
            "heart": "h",
            "open": "o",
            "check": "c",
            "exit": "e",
            "show": "s",
            "ver": "v",
            "version": "v",
            "help": "?",
            "？": "?",
        }
        parts = command.split()
        action = parts[0]
        if action in command_aliases:
            action = command_aliases[action]

        if action == "?":
            output.h()
        elif action == "e":
            sys.exit()
        elif action == "v":
            i = 0
            while i < len(games):
                print(f"曲库使用的{games[i]}版本：{versions[i]}\n")
                i += 1
        elif action == "o":
            if len(parts[1]) != 1:
                print("无效的参数，应为单个字符。")
            else:
                input_char = parts[1]
                if input_char in "-$( )*+.[]{{}}?\\^|/":
                    input_char = "\\" + input_char  # 转义字符

                if input_char in opened_char:
                    print(f"这个字符已经刮开了！剩余次数：{heart}。")
                else:
                    opened_char_lowercase.append(str.lower(parts[1]))
                    if re.match(r"^[A-Za-z]$", input_char):  # 判断是否为拉丁字母
                        opened_char.append(str.lower(input_char))  # 加入小写
                        opened_char.append(str.upper(input_char))  # 加入大写
                    else:
                        opened_char.append(input_char)  # 加入非拉丁字母字符
                    heart -= 1  # 扣除1点可用刮开次数
                    print(f"刮开的字符：{parts[1]}。\n剩余次数：{heart}。")
                    # 为正则替换而合并opened_char为字符串
                    used_char = ""
                    for i in range(len(opened_char)):
                        used_char += opened_char[i]
                    # 使用正则替换刮开字符
                    t = []
                    for element in answer_list:
                        t.append(re.sub("[^" + used_char + "\\s]", "*", element))
                    # 将回答正确的全部刮开
                    for i in range(NUM):
                        if tt[i] == answer_list[i]:
                            t[i] = answer_list[i]
                    output.to_temp(known_char(opened_char_lowercase), t, "Temp")
                    copy("Temp")
                    if known_char(opened_char_lowercase) != "":
                        print(known_char(opened_char_lowercase))
                    output.loop_print(t)
                    tt = t  # 暂存
                    t = []  # 清空

        elif action == "c":
            if not str.isdigit(parts[1]):
                print("无效的参数，应为数字。")
            else:
                n = int(parts[1])
                if n > NUM or n < 1:
                    print("题目不存在。")
                elif tt[n - 1] != answer_list[n - 1]:
                    print("编号为“%d”的题目回答正确，全部刮开。" % n)
                    tt[n - 1] = answer_list[n - 1]
                    output.to_temp(known_char(opened_char_lowercase), tt, "Temp")
                    copy("Temp")
                    if known_char(opened_char_lowercase) != "":
                        print(known_char(opened_char_lowercase))
                    output.loop_print(tt)
                    t = tt
                else:
                    print("编号为“%d”的题目已经回答正确。" % n)

        elif action == "h":
            if len(parts) >= 2:
                if parts[1] == "add":
                    amount = int(parts[2]) if len(parts) > 2 else 1
                    heart += amount
                    print(f"已增加{amount}次可用刮开次数。\n剩余次数：{heart}。")
                elif parts[1] == "remove":
                    amount = int(parts[2]) if len(parts) > 2 else 1
                    heart -= amount
                    print(f"已减少{amount}次可用刮开次数。\n剩余次数：{heart}。")
                else:
                    print("无效的命令，请重试。")
            else:
                print("无效的命令，请重试。")

        elif action == "s":
            if t == []:
                output.loop_print(tt)
            else:
                output.loop_print(t)
            copy("Temp")
        else:
            print("无效的命令，请重试。")

    if action != "e":
        if t == answer_list:
            print("\n回答正确，答案为：")
        else:
            print("\n次数已耗尽，答案为：")
        output.loop_print(answer_list)
        copy("Answer")


if __name__ == "__main__":
    main()
