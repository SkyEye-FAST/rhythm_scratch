# -*- encoding: utf-8 -*-
"""音游猜曲名刮刮乐"""

from random import sample
import re
import sys
import tomllib
from pathlib import Path
import pyperclip

# 当前绝对路径
P = Path(__file__).resolve().parent

# 加载配置
with open(P / "configuration.toml", "rb") as f:
    config = tomllib.load(f)

# 常量
NUM = config["const"]["generate_amount"]  # 生成曲目数量
GUESS_CHANCES = config["const"]["guess_chances"]  # 最初刮开可用次数
DICT_FOLDER = P / config["path"]["dict_folder"]  # 曲库路径
OUTPUT_FOLDER = P / config["path"]["output_folder"]  # 输出路径
ENABLE_COPY = config["other"]["enable_clipboard"]  # 是否启用剪贴板

# 创建输出文件夹（若不存在）
OUTPUT_FOLDER.mkdir(exist_ok=True)

# 加载曲库列表
all_dicts_folder = [
    i for i in DICT_FOLDER.iterdir() if (DICT_FOLDER / i / "dict.toml").exists()
]
games = []
versions = []

for folder in all_dicts_folder:
    with open(DICT_FOLDER / folder / "dict.toml", "rb") as f:
        dict_config = tomllib.load(f)
        games.append(dict_config["name"])
        versions.append(dict_config["version"])


def load_dict(file_path):
    """加载曲库为列表函数"""
    with open(file_path, "r", encoding="utf-8") as dict_file:
        return [line.strip() for line in dict_file]


def copy_to_clipboard(file):
    """复制文件内容到剪贴板函数"""
    if ENABLE_COPY:
        with open(OUTPUT_FOLDER / file, "r", encoding="utf-8") as text:
            pyperclip.copy(text.read())


def known_char(name):
    """已开字符函数"""
    return f"已开字符：{'、'.join(name)}。" if name else ""


class Output:
    """输出类"""

    @staticmethod
    def to_file(name, file):
        """输出文件函数"""
        with open(OUTPUT_FOLDER / file, "w", encoding="utf-8") as text:
            text.writelines(f"{i + 1}. {element}\n" for i, element in enumerate(name))

    @staticmethod
    def to_temp(known, name, file):
        """输出暂存到文件函数"""
        with open(OUTPUT_FOLDER / file, "w", encoding="utf-8") as text:
            if known:
                text.write(known + "\n")
            text.writelines(f"{i + 1}. {element}\n" for i, element in enumerate(name))

    @staticmethod
    def loop_print(name):
        """循环输出函数"""
        for i, ele in enumerate(name):
            print(f"{i + 1}. {ele}")

    @staticmethod
    def show_help():
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

    @staticmethod
    def show_dicts():
        """显示曲库"""
        for i, game in enumerate(games):
            print(f"{i + 1}. {game}（游戏版本：{versions[i]}）")


print("音游猜曲名刮刮乐\n作者：SkyEye_FAST\n\n可用的曲库：")
# 输出曲库列表
Output.show_dicts()

# 选择曲库
selected_dicts = input("请选择曲库编号，以逗号分隔：\n\n>> ").split(",")
selected_dicts_int = [
    int(index.strip()) for index in selected_dicts if index.strip().isdigit()
]
if not selected_dicts_int:
    print("未按格式输入，请重试。")
    sys.exit()

# 加载曲库
selected_dict_content = []
for index in selected_dicts_int:
    if 1 <= index <= len(all_dicts_folder):
        get_folder = all_dicts_folder[index - 1]
        with open(DICT_FOLDER / get_folder / "dict.toml", "rb") as dict_config:
            dict_config_content = tomllib.load(dict_config)
            for element in dict_config_content["dicts"]:
                selected_dict_content.extend(
                    load_dict(DICT_FOLDER / get_folder / "dict" / element)
                )
        print(f"已加载曲库“{games[index - 1]}”。")
    else:
        print(f"编号为“{index}”的曲库不存在，忽略。")
selected_dict_content = list(set(selected_dict_content))  # 去除重复曲目
TOTAL_SELECTED = len(selected_dict_content)
print(f"选择曲目总数：{TOTAL_SELECTED}\n")

# 生成答案
answer_list = sample(selected_dict_content, NUM)
Output.to_file(answer_list, "Answer.txt")

# 生成初始问题
question_list = ["*" * len(element) for element in answer_list]
Output.to_file(question_list, "Question.txt")
copy_to_clipboard("Question.txt")
print("输入“?”来查看帮助。\n\n题目：")
Output.loop_print(question_list)

# 刮卡
heart: int = GUESS_CHANCES  # 刮开可用次数
t = question_list[:]  # 题目暂存
tt = question_list[:]  # 题目暂存的暂存
opened_char_list = []  # 刮开的字符，字母大小写
opened_char_lowercase_list = []  # 刮开的字符，字母全部小写
IS_ALIVE = True

while t != answer_list:
    command = input("\n>> ").split()
    if not command:
        print("无效的命令，请重试。")
        continue

    action = command[0]
    if heart <= 0:
        IS_ALIVE = False

    match action:
        case "?" | "？" | "help":
            Output.show_help()
        case "e" | "exit":
            sys.exit()
        case "v" | "ver" | "version":
            Output.show_dicts()

        case "o" | "open":
            if not IS_ALIVE:
                print("刮开机会已用完。")
                continue

            if len(command) < 2 or len(command[1]) != 1:
                print("无效的参数，应为单个字符。")
                continue

            input_char = command[1]
            if input_char in "-$( )*+.[]{{}}?\\^|/":
                input_char = "\\" + input_char  # 转义字符

            if input_char in opened_char_list:
                print(f"这个字符已经刮开了！剩余次数：{heart}。")
            else:
                opened_char_lowercase_list.append(input_char.lower())
                if re.match(
                    r"^[\u0041-\u005a\u0061-\u007a\u0391-\u03c9\u0400-\u04ff]$",
                    input_char,
                ): # 判断是否为字母
                    opened_char_list.extend(
                        [input_char.lower(), input_char.upper()]
                    )  # 加入小写和大写
                else:
                    opened_char_list.append(input_char)  # 加入非字母字符

                heart -= 1  # 扣除1点可用刮开次数

                print(f"刮开的字符：{input_char}。\n剩余次数：{heart}。")
                # 为正则替换而合并opened_char_list为字符串
                OPENED_CHAR = "".join(opened_char_list)
                # 使用正则替换刮开字符
                t = [
                    re.sub(f"[^{OPENED_CHAR}]", "*", element) for element in answer_list
                ]
                # 将回答正确的全部刮开
                t = [
                    answer_list[i] if tt[i] == answer_list[i] else t[i]
                    for i in range(NUM)
                ]
                KC = known_char(opened_char_lowercase_list)
                Output.to_temp(KC, t, "Temp.txt")
                copy_to_clipboard("Temp.txt")
                if KC:
                    print(KC)
                Output.loop_print(t)
                tt, t = t, []  # 更新暂存

        case "os" | "openspace":
            if not IS_ALIVE:
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
                OPENED_CHAR = "".join(opened_char_list)
                # 使用正则替换刮开字符
                t = [
                    re.sub(f"[^{OPENED_CHAR}]", "*", element) for element in answer_list
                ]
                # 将回答正确的全部刮开
                t = [
                    answer_list[i] if tt[i] == answer_list[i] else t[i]
                    for i in range(NUM)
                ]
                KC = known_char(opened_char_lowercase_list)
                Output.to_temp(KC, t, "Temp.txt")
                copy_to_clipboard("Temp.txt")
                if KC:
                    print(KC)
                Output.loop_print(t)
                tt, t = t, []  # 更新暂存

        case "c" | "check":
            if len(command) < 2 or not command[1].isdigit():
                print("无效的参数，应为数字。")
                continue

            n = int(command[1])
            if not 1 <= n <= NUM:
                print("题目不存在。")
            elif tt[n - 1] != answer_list[n - 1]:
                print(f"编号为“{n}”的题目回答正确，全部刮开。")
                tt[n - 1] = answer_list[n - 1]
                KC = known_char(opened_char_lowercase_list)
                Output.to_temp(KC, tt, "Temp.txt")
                copy_to_clipboard("Temp.txt")
                if KC:
                    print(KC)
                Output.loop_print(tt)
                t = tt
            else:
                print(f"编号为“{n}”的题目已经回答正确。")

        case "h" | "heart":
            if (
                len(command) < 3
                or command[1] not in {"add", "remove"}
                or not command[2].isdigit()
            ):
                print("无效的命令，请重试。")
                continue

            amount = int(command[2])
            if command[1] == "add":
                heart += amount
                print(f"已增加{amount}次可用刮开次数。\n剩余次数：{heart}。")
            else:
                if heart == 0:
                    print("可用次数已为0，无法继续减少。")
                else:
                    reduction = min(amount, heart)
                    heart -= reduction
                    print(f"已减少{reduction}次可用刮开次数。\n剩余次数：{heart}。")


        case "s" | "show":
            Output.loop_print(t or tt)
            copy_to_clipboard("Temp.txt")

        case _:
            print("无效的命令，请重试。")

print("\n全部题目已回答正确，答案为：")
Output.loop_print(answer_list)
copy_to_clipboard("Answer.txt")
