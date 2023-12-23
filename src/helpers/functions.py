import os
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup


def date_diff_in_seconds(date1, date2):
    time_diff = date2 - date1
    return time_diff.days * 24 * 3600 + time_diff.seconds


def days_hrs_mins_secs_from_secs(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return days, hours, minutes, seconds


def random_sonnet(file_path: str) -> str:
    sonnet_list = []
    for root, dirs, files in os.walk(f"{file_path}"):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), "r") as f:
                    text2 = f.read()
                    sonnet_list.append(text2)

    return random.choice(sonnet_list)


def random_country(url: str) -> str:
    wikiurl = url
    response = requests.get(wikiurl)
    soup = BeautifulSoup(response.text, "html.parser")
    worldtable = soup.find("table", {"class": "wikitable"})
    df = pd.read_html(str(worldtable))
    df = pd.DataFrame(df[0])
    df = df[["國家/地區", "佔世界比"]]
    df.columns = ["country_old", "percent"]
    df = df[(df["country_old"] != "世界")]
    df["country"] = df["country_old"].str.split("[").str[0]
    df = df[["country", "percent"]]
    df["percent"] = df["percent"].str.strip()
    df["percent"] = df["percent"].str.replace("%", "")
    df["percent"] = df["percent"].str.replace("‰", "")
    df["percent"] = pd.to_numeric(df["percent"], errors="coerce")
    df["percent_new"] = df["percent"] / df["percent"].sum()

    draw = str(random.choice(df["country"].tolist(), 1, p=df.iloc[:, 2]))
    draw = draw.replace("'", "")
    draw = draw.replace("[", "")
    draw = draw.replace("]", "")

    return f""""你下世做{draw}人啦^_^"""


def readtxt(filename):
    with open(filename) as f:
        lines = f.readlines()
        return lines


def finatext(input_text: str):
    postfix_txt = readtxt("/postfix.txt")
    postfix = [x.rstrip("\n") for x in postfix_txt]

    ww = [" w", " ww", " www", " wwww ", "", "", "", ""]

    test = input_text.split("\n")
    txtoutput_list = [
        x + random.choice(ww) + " (" + random.choice(postfix) for x in test
    ]
    finaloutput = "\n".join(txtoutput_list)

    return finaloutput


def random_reply(input_text: str) -> str:
    prefix = readtxt("/prefix.txt")
    blank_list = ["", "", "", ""]
    prefix_final = blank_list + prefix
    return f"""{random.choice(prefix_final)}{finatext(input_text)}"""
