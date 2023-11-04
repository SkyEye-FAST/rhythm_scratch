# -*- encoding: utf-8 -*-
"""音游猜曲名刮刮乐"""

from random import sample
import os
import re
import sys
import tomllib
import pyperclip

# 当前绝对路径
P = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")

# 加载配置
with open(os.path.join(P, "configuration.toml"), "rb") as f:
    config = tomllib.load(f)

# 常量
NUM = config["const"]["generate_amount"]  # 生成曲目数量
GUESS_CHANCES = config["const"]["guess_chances"]  # 最初刮开可用次数
DICT_FOLDER = os.path.join(P, config["path"]["dict_folder"])  # 曲库路径
OUTPUT_FOLDER = os.path.join(P, config["path"]["output_folder"])  # 输出路径

# 创建输出文件夹（若不存在）
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 加载曲库列表
all_dicts_folder = [
    i
    for i in os.listdir(DICT_FOLDER)
    if os.path.exists(os.path.join(DICT_FOLDER, i, "dict.toml"))
]
games = []
versions = []
for folder in all_dicts_folder:
    dict_config = os.path.join(DICT_FOLDER, folder, "dict.toml")
    with open(dict_config, "rb") as f:
        dict_config = tomllib.load(f)
        games.append(dict_config["name"])
        versions.append(dict_config["version"])


def load_dict(file_path: str):
    """加载曲库为列表函数"""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def copy(file: str):
    """复制文件内容到剪贴板函数"""
    with open(os.path.join(OUTPUT_FOLDER, file), "r", encoding="utf-8") as text:
        pyperclip.copy(text.read())


def known_char(name: list):
    """已开字符函数"""
    return f"已开字符：{'、'.join(name)}。" if name else ""


class Output:
    """输出类"""

    @staticmethod
    def to_file(name: list, file: str):
        """输出文件函数"""
        with open(os.path.join(OUTPUT_FOLDER, file), "w", encoding="utf-8") as text:
            text.writelines(f"{i + 1}. {element}\n" for i, element in enumerate(name))

    @staticmethod
    def to_temp(known: str, name: list, file: str):
        """输出暂存到文件函数"""
        with open(os.path.join(OUTPUT_FOLDER, file), "w", encoding="utf-8") as text:
            if known:
                text.write(known + "\n")
            lines = [f"{i + 1}. {element}\n" for i, element in enumerate(name)]
            text.writelines(lines)

    @staticmethod
    def loop_print(name: list):
        """循环输出函数"""
        return [print(f"{i + 1}. {element}") for i, element in enumerate(name)]

    @staticmethod
    def h():
        """输出帮助函数"""
        print("可用命令：")
        print("  help | ? - 显示帮助")
        print("  exit | e - 退出")
        print("  version | ver | v - 列出曲库使用音游版本号")
        print("  (heart | h) add [amount] - 增加可用刮开次数")
        print("  (heart | h) remove [amount] - 减少可用刮开次数")
        print("  (open | o) [character] - 刮开指定字符")
        print("  openspace | os - 刮开空格")
        print("  (check | c) [index] - 将某题全部刮开")
        print("  (show | s) - 显示题目")


def main():
    """主函数"""
    print("音游猜曲名刮刮乐\n作者：SkyEye_FAST\n\n可用的曲库：")
    # 输出曲库列表
    for i, game in enumerate(games):
        print(f"{i + 1}. {game}（游戏版本：{versions[i]}）")
    # 选择曲库
    selected_dicts = input("请选择曲库编号，以逗号分隔：\n\n>> ").split(",")
    selected_dicts = [
        int(index.strip()) for index in selected_dicts if index.strip().isdigit()
    ]
    if len(selected_dicts) == 0:
        print("未按格式输入，请重试。")
        sys.exit()
    # 加载曲库
    selected_dict_content = []

    for index in selected_dicts:
        if 1 <= index <= len(all_dicts_folder):
            get_folder = all_dicts_folder[index - 1]
            dict_config_file = os.path.join(DICT_FOLDER, get_folder, "dict.toml")
            with open(dict_config_file, "rb") as file:
                dict_config_content = tomllib.load(file)
                for element in dict_config_content["dicts"]:
                    selected_dict_content.extend(
                        load_dict(os.path.join(DICT_FOLDER, get_folder, "dict", element))
                    )
            print(f"已加载曲库“{games[index - 1]}”。")
        else:
            print(f"编号为“{index}”的曲库不存在，忽略。")

    selected_dict_content = list(set(selected_dict_content))  # 去除重复曲目
    total_selected = len(selected_dict_content)
    print(f"选择曲目总数：{total_selected}\n")

    # 生成答案
    answer_list = sample(selected_dict_content, NUM)
    Output.to_file(answer_list, "Answer.txt")

    # 生成初始问题
    question_list = []
    for element in answer_list:
        question_list.append("*" * len(element))
    Output.to_file(question_list, "Question.txt")
    copy("Question.txt")
    print("输入“?”来查看帮助。\n\n题目：")
    Output.loop_print(question_list)

    # 刮卡
    heart = GUESS_CHANCES  # 刮开可用次数
    t = question_list  # 题目暂存
    tt = question_list  # 题目暂存的暂存
    opened_char_list = []  # 刮开的字符，字母大小写
    opened_char_lowercase_list = []  # 刮开的字符，字母全部小写
    is_alive = True

    while t != answer_list:
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
            "openspace": "os",
        }
        parts = command.split()
        action = parts[0]
        action = command_aliases.get(action)

        if heart <= 0:
            is_alive = False

        if action == "?":
            Output.h()
        elif action == "e":
            sys.exit()
        elif action == "v":
            for i, game in enumerate(games):
                print(f"曲库使用的{game}版本：{versions[i]}")

        elif action == "o":
            if not is_alive:
                print("刮开机会已用完。")
                continue

            if len(parts[1]) != 1:
                print("无效的参数，应为单个字符。")
            else:
                input_char = parts[1]
                if input_char in "-$( )*+.[]{{}}?\\^|/":
                    input_char = "\\" + input_char  # 转义字符

                if input_char in opened_char_list:
                    print(f"这个字符已经刮开了！剩余次数：{heart}。")
                else:
                    opened_char_lowercase_list.append(parts[1].lower())
                    if re.match(
                        r"^[\u0041-\u005a\u0061-\u007a\u0391-\u03c9\u0400-\u04ff]$",
                        input_char,
                    ):  # 判断是否为字母
                        opened_char_list.extend(
                            [input_char.lower(), input_char.upper()]
                        )  # 加入小写和大写
                    else:
                        opened_char_list.append(input_char)  # 加入非字母字符

                    heart -= 1  # 扣除1点可用刮开次数

                    print(f"刮开的字符：{parts[1]}。\n剩余次数：{heart}。")
                    # 为正则替换而合并opened_char_list为字符串
                    opened_char = "".join(opened_char_list)
                    # 使用正则替换刮开字符
                    t = [
                        re.sub(f"[^{opened_char}]", "*", element)
                        for element in answer_list
                    ]
                    # 将回答正确的全部刮开
                    t = [
                        answer_list[i] if tt[i] == answer_list[i] else t[i]
                        for i in range(NUM)
                    ]
                    kc = known_char(opened_char_lowercase_list)
                    Output.to_temp(kc, t, "Temp.txt")
                    copy("Temp.txt")
                    if kc:
                        print(kc)
                    Output.loop_print(t)
                    tt, t = t, []  # 更新暂存
        elif action == "os":
            if not is_alive:
                print("刮开机会已用完。")
                continue

            if "空格" in opened_char_list:
                print(f"这个字符已经刮开了！剩余次数：{heart}。")
            else:
                opened_char_list.append("\\s")
                opened_char_lowercase_list.append("空格")

                heart -= 1  # 扣除1点可用刮开次数

                print(f"刮开的字符：空格。\n剩余次数：{heart}。")
                # 为正则替换而合并opened_char_list为字符串
                opened_char = "".join(opened_char_list)
                # 使用正则替换刮开字符
                t = [
                    re.sub(f"[^{opened_char}]", "*", element) for element in answer_list
                ]
                # 将回答正确的全部刮开
                t = [
                    answer_list[i] if tt[i] == answer_list[i] else t[i]
                    for i in range(NUM)
                ]
                kc = known_char(opened_char_lowercase_list)
                Output.to_temp(kc, t, "Temp.txt")
                copy("Temp.txt")
                if kc:
                    print(kc)
                Output.loop_print(t)
                tt, t = t, []  # 更新暂存

        elif action == "c":
            if not parts[1].isdigit():
                print("无效的参数，应为数字。")
            else:
                n = int(parts[1])
                if n > NUM or n < 1:
                    print("题目不存在。")
                elif tt[n - 1] != answer_list[n - 1]:
                    print(f"编号为“{n}”的题目回答正确，全部刮开。")
                    tt[n - 1] = answer_list[n - 1]
                    kc = known_char(opened_char_lowercase_list)
                    Output.to_temp(kc, tt, "Temp.txt")
                    copy("Temp.txt")
                    if kc:
                        print(kc)
                    Output.loop_print(tt)
                    t = tt
                else:
                    print(f"编号为“{n}”的题目已经回答正确。")

        elif action == "h":
            if len(parts) == 3:
                if parts[1] == "add" or parts[1] == "remove":
                    amount = int(parts[2]) if len(parts) > 2 else 1
                    if parts[1] == "add":
                        heart += amount
                        print(f"已增加{amount}次可用刮开次数。\n剩余次数：{heart}。")
                    else:
                        heart -= amount
                        print(f"已减少{amount}次可用刮开次数。\n剩余次数：{heart}。")
                else:
                    print("无效的命令，请重试。")
            else:
                print("无效的命令，请重试。")

        elif action == "s":
            if not t:
                Output.loop_print(tt)
            else:
                Output.loop_print(t)
            copy("Temp.txt")
        else:
            print("无效的命令，请重试。")

        if action != "e":
            print("\n全部题目已回答正确，答案为：")
            Output.loop_print(answer_list)
            copy("Answer.txt")


if __name__ == "__main__":
    main()
