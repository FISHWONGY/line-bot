from flask import Flask
import emoji
from pyowm import OWM
from linebot import LineBotApi, WebhookHandler

app = Flask(__name__)

line_bot_api = LineBotApi("YOUR_TOKEN")
handler = WebhookHandler("YOUR_TOKEN")

owm = OWM("YOUR_TOKEN")
mgr = owm.weather_manager()
owm_temp_metrics = ["temp_kf", "temp_max", "temp_min"]
owm_rep_dict = {
    "{": "",
    "}": "",
    "'": "",
    ", ": " \n",
    "temp": "溫度",
    "feels_like": "體感",
}
owm_status_replace_dict = {
    "light rain": emoji.emojize(":umbrella:", use_aliases=True) + "小雨",
    "rain": emoji.emojize(":umbrella:", use_aliases=True) + "驟雨",
    "mist": emoji.emojize(":foggy:", use_aliases=True) + "霧",
    "clouds": emoji.emojize(":cloud:", use_aliases=True) + "有雲",
    "few clouds": emoji.emojize(":cloud:", use_aliases=True) + "少雲",
    "broken clouds": emoji.emojize(":cloud:", use_aliases=True) + "碎雲",
    "scattered clouds": emoji.emojize(":cloud:", use_aliases=True) + "散雲",
    "overcast clouds": emoji.emojize(":cloud:", use_aliases=True) + "陰雲",
    "clear sky": emoji.emojize(":milky_way:", use_aliases=True) + "天清",
}


wiki_url = "https://zh.wikipedia.org/wiki/%E5%90%84%E5%9B%BD%E5%AE%B6%E5%92%8C%E5%9C%B0%E5%8C%BA%E4%BA%BA%E5%8F%A3%E5%88%97%E8%A1%A8"
