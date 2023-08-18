# 音游猜曲名刮刮乐

**C++ 版本：<https://github.com/SkyEye-FAST/rhythm_scratch_cpp>**

此脚本适用于即时通讯的群组/聊天室/服务器等处，**需要主持人来操作**，而非自主进行游戏。

执行与题目相关的命令后会自动将输出内容复制到剪贴板，无需手动复制。

题目和答案会在执行过程中以文件形式出现在**输出文件夹**（默认为`output`）内。

刮开的字符如果为字母（包括拉丁、希腊、西里尔），则会同时刮开大小写。

## 需求

由于使用了标准库`tomllib`，所以需要**Python >= 3.11**

需要库`pyperclip`，请使用下面的命令安装：

``` shell
pip install pyperclip
```

## 命令列表

- help | ? - 显示帮助
- exit | e - 退出
- version | ver | v - 列出曲库使用音游版本号
- (heart | h) add [amount] - 增加可用刮开次数
- (heart | h) remove [amount] - 减少可用刮开次数
- (open | o) [character] - 刮开指定字符
- openspace | os - 刮开空格
- (check | c) [index] - 将某题全部刮开
- (show | s) - 显示题目

## 曲库

目前提供的音游：Arcaea、Phigros、Orzmic。

- 曲库使用的Arcaea版本：v4.6.1
- 曲库使用的Phiros版本：3.1.1.1
- 曲库使用的Orzmic版本：2.18.21

### 自定义曲库

在曲库文件夹（默认为`song_dict`）下，请按照以下结构存放曲库：

- 曲库文件夹
  - 曲库1
    - `dict`
      - 曲库文件1
      - 曲库文件2
    - `dict.toml`
  - 曲库2
  - 曲库3

`dict.toml`的格式如下：

``` toml
name = "游戏名称"
version = "游戏版本"
dicts = ["曲库文件1", "曲库文件2"]
```

曲库文件为纯文本，一行一个曲名。

## 配置文件

配置文件名为`configuration.toml`，位置与脚本同级。

| 键名              | 默认值 | 说明         |
|-------------------|--------|--------------|
| `generate_amount` | `10`   | 生成曲目数量 |
| `guess_chancess`  | `10`   | 可用刮开次数 |

| 键名            | 默认值      | 说明       |
|-----------------|-------------|------------|
| `output_folder` | `output`    | 输出文件夹 |
| `dict_folder`   | `song_dict` | 曲库文件夹 |
