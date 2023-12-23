import re
from helpers.utils import mgr, owm_temp_metrics, owm_rep_dict, owm_status_replace_dict


def get_weather_deatils(location: str):
    obs = mgr.weather_at_place(f"{location}")
    w = obs.weather
    temp = w.temperature("celsius")
    for e in owm_temp_metrics:
        temp.pop(e)
    temp2 = str(temp)

    rep = dict((re.escape(k), v) for k, v in owm_rep_dict.items())
    pattern = re.compile("|".join(rep.keys()))
    temp2 = pattern.sub(lambda m: rep[re.escape(m.group(0))], temp2)

    status = w.detailed_status
    status_replace = dict((re.escape(k), v) for k, v in owm_status_replace_dict.items())
    status_pattern = re.compile("|".join(status_replace.keys()))
    status = status_pattern.sub(lambda m: status_replace[re.escape(m.group(0))], status)

    return temp2, status
