import os
import random
import requests
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
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    worldtable = soup.find("table", {"class": "wikitable"})

    countries = [
        row.select_one("td:nth-of-type(1)").get_text(strip=True)
        for row in worldtable.select("tr")[1:]
    ]
    percentages = [
        float(
            row.select_one("td:nth-of-type(2)")
            .get_text(strip=True)
            .replace("%", "")
            .replace("‰", "")
            .strip()
        )
        for row in worldtable.select("tr")[1:]
    ]

    percentages = [percent / sum(percentages) for percent in percentages]

    selected_country = random.choices(countries, weights=percentages)[0]

    return f"你下世做{selected_country}人啦^_^"


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
