import re
from helpers.utils import mgr, owm_temp_metrics, owm_rep_dict, owm_status_replace_dict


def clean_data(str_obj: str, replace_dict: dict) -> str:
    rep = dict((re.escape(k), v) for k, v in replace_dict.items())
    pattern = re.compile("|".join(rep.keys()))
    str_obj = pattern.sub(lambda m: rep[re.escape(m.group(0))], str_obj)

    return str_obj


def get_weather_deatils(location: str):
    obs = mgr.weather_at_place(f"{location}")
    w = obs.weather
    temp = w.temperature("celsius")
    for e in owm_temp_metrics:
        temp.pop(e)
    temp2 = str(temp)
    temp2 = clean_data(temp2, owm_rep_dict)

    status = w.detailed_status
    status = clean_data(status, owm_status_replace_dict)

    return temp2, status
