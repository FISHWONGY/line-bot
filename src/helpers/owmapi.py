import re
from typing import Tuple
from helpers.utils import mgr, owm_temp_metrics, owm_rep_dict, owm_status_replace_dict


def clean_data(str_obj: str, replace_dict: dict) -> str:
    rep = dict((re.escape(k), v) for k, v in replace_dict.items())
    pattern = re.compile("|".join(rep.keys()))
    clean_str = pattern.sub(lambda m: rep[re.escape(m.group(0))], str_obj)

    return clean_str


def get_weather_details(location: str) -> Tuple[str, str]:
    obs = mgr.weather_at_place(location)
    temp = {key: value for key, value in obs.weather.temperature("celsius").items() if key not in owm_temp_metrics}
    temp_str = clean_data(str(temp), owm_rep_dict)

    status = clean_data(obs.weather.detailed_status, owm_status_replace_dict)

    return temp_str, status
