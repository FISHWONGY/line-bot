from lxml import html
import pandas as pd
import requests


def team_std() -> str:
    page_team = requests.get("https://www.formula1.com/en/results.html/2022/team.html")
    tree_team = html.fromstring(page_team.content)
    team_sd = tree_team.xpath("//tr")
    column_headers = []

    for column in team_sd[0]:
        name = column.text_content()
        column_headers.append((name, []))

    for row in range(1, len(team_sd)):
        table_tr = team_sd[row]

        column_count = 0

        for column in table_tr.iterchildren():
            data = column.text_content()
            column_headers[column_count][1].append(data)
            column_count += 1

    dictionary = {title: column for (title, column) in column_headers}

    team_standing = pd.DataFrame(dictionary)

    # data cleaning
    team_standing = team_standing.drop("", 1)
    team_standing["Team"] = team_standing["Team"].str.strip()

    team_pos_list = team_standing["Pos"].tolist()
    team_name_list = team_standing["Team"].tolist()
    team_pts_list = team_standing["PTS"].tolist()

    teamstr = ""
    for i in range(len(team_pos_list)):
        teamstr += (
            team_pos_list[i]
            + ". "
            + team_name_list[i]
            + " - "
            + team_pts_list[i]
            + " PTS\n"
        )
    teamstr = "Current Constructor Standings: \n\n" + teamstr

    return teamstr


def driver_std() -> str:
    page_dr = requests.get("https://www.formula1.com/en/results.html/2022/drivers.html")
    tree_dr = html.fromstring(page_dr.content)
    driver_sd = tree_dr.xpath("//tr")
    column_headers = []

    for column in driver_sd[0]:
        name = column.text_content()
        column_headers.append((name, []))

    for row in range(1, len(driver_sd)):
        table_tr = driver_sd[row]

        column_count = 0

        for column in table_tr.iterchildren():
            data = column.text_content()
            column_headers[column_count][1].append(data)
            column_count += 1

    dictionary = {title: column for (title, column) in column_headers}

    driver_standing = pd.DataFrame(dictionary)
    driver_standing = driver_standing.drop("", 1)
    driver_standing["Car"] = driver_standing["Car"].str.strip()
    driver_standing["Driver"] = driver_standing["Driver"].str.strip()
    driver_standing["Driver"] = driver_standing["Driver"].str.replace(" ", "")
    driver_standing["Driver"] = driver_standing["Driver"].str.replace("\n", " ")
    driver_standing["Driver"] = driver_standing["Driver"].str.replace("  ", " ")
    driver_standing["Driver"] = driver_standing["Driver"].str.replace("  ", " ")
    # driver_standing = driver_standing.replace({'Driver': {" ": "", '\n': " "}})

    driver_standing[["First", "Last", "Int"]] = driver_standing.Driver.str.split(
        " ",
        expand=True,
    )
    driver_standing["Driver"] = driver_standing["First"] + " " + driver_standing["Last"]
    driver_standing = driver_standing.drop(["First", "Last"], axis=1)

    dr_pos_list = driver_standing["Pos"].tolist()
    dr_name_list = driver_standing["Driver"].tolist()
    dr_pts_list = driver_standing["PTS"].tolist()
    dr_str = ""
    for i in range(len(dr_pos_list)):
        dr_str += (
            dr_pos_list[i]
            + ". "
            + dr_name_list[i]
            + "  -  "
            + dr_pts_list[i]
            + " PTS\n"
        )

    dr_str = "Current F1 Driver Standings: \n\n" + dr_str

    return dr_str
