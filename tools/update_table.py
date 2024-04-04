# -*- encoding: utf-8 -*-
"""曲库内容更新器"""

from pathlib import Path
import requests
from bs4 import BeautifulSoup

P = Path(__file__).resolve().parent.parent


def get_data(url: str, song_row: int, folder: str, file: str):
    """获取数据函数"""
    soup = BeautifulSoup(requests.get(url, timeout=30).text, "html.parser")
    tables = soup.find_all("table")

    file_path = P / "song_dict" / folder / "dict" / file
    with open(file_path, "w", encoding="utf-8") as dict_file:
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                if len(cells) > 1:
                    data = cells[song_row].text
                    dict_file.write(data + "\n")


get_data("https://phigros.fandom.com/wiki/Songs", 0, "phigros", "pgr")
get_data("https://musedash.fandom.com/wiki/Songs", 1, "muse_dash", "muse_dash")
get_data("https://orzmic.fandom.com/wiki/Songs", 0, "orzmic", "orz")


def fix_dict(folder: str, file: str):
    """修复曲库函数"""
    file_path = P / "song_dict" / folder / "dict" / file

    with open(file_path, "r", encoding="utf-8") as dict_file:
        dict_content = sorted({line.strip() for line in dict_file})

    dict_content = list(filter(None, dict_content))
    if folder == "muse_dash":
        dict_content.remove("HARD")
    if folder == "orzmic":
        dict_content.remove("-")
        dict_content = list(filter(lambda x: not str(x).isdigit(), dict_content))

    with open(file_path, "w", encoding="utf-8") as dict_file:
        dict_file.writelines(f"{element}\n" for element in dict_content)


fix_dict("phigros", "pgr")
fix_dict("muse_dash", "muse_dash")
fix_dict("orzmic", "orz")
