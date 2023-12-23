from lxml import html
import requests


def scrape_f1_page(web_url: str) -> dict:
    page_team = requests.get(web_url)
    tree_team = html.fromstring(page_team.content)

    team_sd = tree_team.xpath("//tr")

    column_headers = [(column.text_content(), []) for column in team_sd[0]]

    for row in team_sd[1:]:
        for column_count, column in enumerate(row.iterchildren()):
            data = column.text_content()
            column_headers[column_count][1].append(data)

    return {title: column for title, column in column_headers}


def clean_and_format(data_list: list) -> list:
    return [
        item.strip().replace("\n", "").replace(" ", "").replace("  ", " ")
        for item in data_list
    ]


def team_std() -> str:
    url = "https://www.formula1.com/en/results.html/2022/team.html"
    team_dict = scrape_f1_page(url)

    team_dict["Team"] = clean_and_format(team_dict["Team"])

    team_str = "\n".join(
        f"{pos}. {name} - {pts} PTS"
        for pos, name, pts in zip(team_dict["Pos"], team_dict["Team"], team_dict["PTS"])
    )

    return f"Current Constructor Standings: \n\n{team_str}"


def driver_std() -> str:
    url = "https://www.formula1.com/en/results.html/2022/drivers.html"
    driver_dict = scrape_f1_page(url)

    driver_dict["Car"] = clean_and_format(driver_dict["Car"])
    driver_dict["Driver"] = [
        name.strip().replace(" ", "").replace("\n", " ").replace("  ", " ")
        for name in driver_dict["Driver"]
    ]

    driver_dict["Driver"] = [
        f"{first} {last}"
        for first, last, _ in [name.split(" ", 2) for name in driver_dict["Driver"]]
    ]

    dr_str = "\n".join(
        f"{pos}. {name}  -  {pts} PTS"
        for pos, name, pts in zip(
            driver_dict["Pos"], driver_dict["Driver"], driver_dict["PTS"]
        )
    )

    return f"Current F1 Driver Standings: \n\n{dr_str}"
