# -*- encoding: utf-8 -*-

import re, os, pyperclip
from random import sample

# 调用路径
p = (
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".")
    + os.path.sep
)

# 创建输出文件夹（若不存在）
if not os.path.exists(p + "output"):
    os.makedirs(p + "output")

NUM = 10  # 生成曲目数量
ARCVER = "v4.5.3"
PGRVER = "3.1.1.1"
ORZVER = "2.18.21"


# 定义初始化曲库函数
def ini(name, dict):
    f = open(p + "dict" + os.path.sep + name, "r", encoding="utf-8")
    line = f.readline()
    while line:
        dict.append(line[:-1])
        line = f.readline()
    f.close()


# 定义复制文件内容到剪贴板函数
def copy(file):
    f = open(p + "output" + os.path.sep + file, "r", encoding="utf-8")
    content = f.read()
    pyperclip.copy(content)


# 定义已开字符函数
def known_char(name):
    if name != []:
        s = "已开字符："
        s += name[0]
        for e in range(1, len(name)):
            s += "、" + name[e]
        return s + "。"
    else:
        return ""


# 定义输出文件函数
def output_file(name, file):
    o = open(p + "output" + os.path.sep + file, "w", encoding="utf-8")
    i = 0
    for e in name:
        i += 1
        o.write(str(i) + ". " + e + "\n")
    o.close()


# 定义输出暂存到文件函数
def output_temp(known, name, file):
    o = open(p + "output" + os.path.sep + file, "w", encoding="utf-8")
    if known != "":
        o.write(known + "\n")
    i = 0
    for e in name:
        i += 1
        o.write(str(i) + ". " + e + "\n")
    o.close()


# 定义输出函数
def output_print(name):
    i = 0
    for e in name:
        i += 1
        print(str(i) + ". " + e)


# 定义命令相关函数
def cmd_char_judge(c, s):
    if re.match("^" + c + "\\s", s):
        return True
    else:
        return False


def cmd_num_judge(c, s):
    if re.match("^" + c + "\\s", s):
        return True
    else:
        return False


def cmd_num_len(c, s):
    return len(s) - len(c) - 1


print(
    """
音游猜曲名刮刮乐
作者：SkyEye_FAST
目前支持的音游：Arcaea、Phigros、Orzmic
曲库使用的Arcaea版本：%s
曲库使用的Phiros版本：%s
曲库使用的Orzmic版本：%s
"""
    % (ARCVER, PGRVER, ORZVER)
)

# 选择游戏，初始化曲库
r = input("请选择游戏（可多选，如12）\n1. Arcaea\n2. Phigros\n3. Orzmic\n\n>> ")
d = []
if "1" in r:
    ini("arc_slst", d)
    ini("arc_other", d)
if "2" in r:
    ini("pgr", d)
if "3" in r:
    ini("orz", d)
d = list(set(d))  # 去除重复曲目
print("选择曲目总数：%d\n" % len(d))

# 生成答案
a = sample(d, NUM)
output_file(a, "Answer")

# 生成初始问题
q = []
for e in a:
    e = re.sub(r"\S", "*", e)
    q.append(e)
output_file(q, "Question")
copy("Question")
print("题目：")
output_print(q)

# 刮卡
r = ""  # 输入的内容
t = q  # 题目暂存
t1 = q  # 题目暂存的暂存
char = []  # 刮开的字符，拉丁字母大小写
char1 = []  # 刮开的字符，拉丁字母全部小写
heart = 20  # 刮开可用次数

while heart > 0 and t != a:
    r = input("\n>> ")  # 输入命令

    # 替换别名
    r = r.replace("open", "o")
    r = r.replace("correct", "c")
    r = r.replace("decrease", "d")
    r = r.replace("increase", "i")

    if cmd_char_judge("o", r):
        if len(r) != 3:
            print("无效的参数，应为单个字符。")
        else:
            input_char = r[-1]
            if input_char in "-$( )*+.[]{{}}?\\^|/":
                input_char = "\\" + input_char  # 转义字符

            if input_char in char:
                print("这个字符已经刮开了！剩余次数：%d。" % heart)
            else:
                char1.append(str.lower(r[-1]))
                if re.match(r"^[A-Za-z]$", input_char):  # 判断是否为拉丁字母
                    char.append(str.lower(input_char))  # 加入小写
                    char.append(str.upper(input_char))  # 加入大写
                else:
                    char.append(input_char)  # 加入非拉丁字母字符
                heart -= 1
                print("刮开的字符：%s。\n剩余次数：%d。" % (r[-1], heart))
                # 为正则替换而合并char为字符串
                used_char = ""
                for i in range(len(char)):
                    used_char += char[i]
                # 使用正则替换刮开字符
                t = []
                for e in a:
                    e = re.sub("[^" + used_char + "\\s]", "*", e)
                    t.append(e)
                # 将回答正确的全部刮开
                for i in range(NUM):
                    if t1[i] == a[i]:
                        t[i] = a[i]
                output_temp(known_char(char1), t, "Temp")
                copy("Temp")
                if known_char(char1) != "":
                    print(known_char(char1))
                output_print(t)
                t1 = t  # 暂存
                t = []  # 清空

    elif cmd_num_judge("c", r):
        if not str.isdigit(r[2:]):
            print("无效的参数，应为数字。")
        else:
            n = int(r[2:])
            if n > NUM or n < 1:
                print("题目不存在。")
            elif t1[n - 1] != a[n - 1]:
                print("%d.回答正确，全部刮开。" % n)
                t1[n - 1] = a[n - 1]
                output_temp(known_char(char1), t1, "Temp")
                copy("Temp")
                if known_char(char1) != "":
                    print(known_char(char1))
                output_print(t1)
                t = t1
            else:
                print("%d.已回答正确。" % n)

    elif cmd_num_judge("d", r):
        if not str.isdigit(r[2:]):
            print("无效的参数，应为数字。")
        else:
            n = int(r[2:])
            heart -= n
            print("已减少%d次可用刮开次数。\n剩余次数：%d。" % (n, heart))

    elif cmd_num_judge("i", r):
        if not str.isdigit(r[2:]):
            print("无效的参数，应为数字。")
        else:
            n = int(r[2:])
            heart += n
            print("已增加%d次可用刮开次数。\n剩余次数：%d。" % (n, heart))

    elif re.match(r"^(show|s)$", r):
        if t == []:
            output_print(t1)
        else:
            output_print(t)
        copy("Temp")

    elif re.match(r"^(version|ver|v)$", r):
        print(
            "曲库使用的Arcaea版本：%s\n曲库使用的Phiros版本：%s\n曲库使用的Orzmic版本：%s"
            % (ARCVER, PGRVER, ORZVER)
        )

    elif re.match(r"^(exit|e)$", r):
        break

    elif re.match(r"^(help|h|\?)$", r):
        print(
            " 帮助 ".center(44, "-")
            + """\nh | help | ? - 显示帮助
e | exit - 退出
v | ver | version - 显示曲库使用的Arcaea版本号
s | show - 显示题目
(o | open) <char> - 刮开某字符
(c | correct) <num> - 将某题全部刮开
(d | decrease) <num> - 减少可用刮开次数
(i | increase) <num> - 增加可用刮开次数"""
        )
    else:
        print("无效的命令。")

if not re.match(r"^(exit|e)$", r):
    if t == a:
        print("\n回答正确，答案为：")
    else:
        print("\n次数已耗尽，答案为：")
    output_print(a)
    copy("Answer")
