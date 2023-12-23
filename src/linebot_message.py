from helpers.utils import *
from helpers.functions import *
import helpers.owmapi as owmapi
import helpers.f1 as f1
import emoji
import flag
import pytz
from datetime import datetime
from flask import request, abort

from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    Sender,
)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_messages(event):
    input_text = event.message.text

    if input_text == "@time":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"""{emoji.emojize(":earth_asia:", use_aliases=True)} {flag.flagize("Current time in :HK:")} :\n\n
                        {datetime.now(pytz.timezone("Asia/Hong_Kong")).strftime("%Y-%m-%d %H:%M:%S")}\n\n
                        {emoji.emojize(":earth_africa:", use_aliases=True)} {flag.flagize("Current time in :GB:")} :\n\n
                        {datetime.now(pytz.timezone("Europe/London")).strftime("%Y-%m-%d %H:%M:%S")}"""
            ),
        )

    elif input_text == "@weather":
        uk_temp, uk_status = owmapi.get_weather_deatils("London,GB")
        hk_temp, hk_status = owmapi.get_weather_deatils("Hong Kong, HK")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"""{flag.flagize(":GB:即時倫敦天氣 :")}\n {uk_temp}\n{uk_status}\n\n
                        {flag.flagize(":HK:即時香港天氣 :")}\n{hk_temp}\n{hk_status}"""
            ),
        )

    elif input_text == "@countdown":
        dest_date = datetime.strptime("2024-12-24 17:00:00", "%Y-%m-%d %H:%M:%S")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"{emoji.emojize(':calendar:')} 距離 Christmas {emoji.emojize(':christmas_tree:', use_aliases=True)} -\n"
                f"{'%d 天, %d 小時 %d 分鐘 %d 秒' % days_hrs_mins_secs_from_secs(date_diff_in_seconds(datetime.now(), dest_date))} "
                f"{emoji.emojize(':santa:', use_aliases=True)}"
            ),
        )

    elif input_text == "@sonnet":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=random_sonnet("My sonnet output/discord"),
                sender=Sender(
                    name="AI Shakespeare",
                    # name=None
                    icon_url="https://media.newyorker.com/photos/5a57ced6f686540bff451ef2/1:1/w_1200,h_1200,c_limit/180122_r31326.jpg",
                ),
            ),
        )

    elif input_text == "@f1team":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f1.team_std(),
                sender=Sender(
                    name="F1",
                    # name=None
                    icon_url="https://cdn.discordapp.com/attachments/813130040938201131/852629478923960350/dux4xq5v0zs41.png",
                ),
            ),
        )

    # Fuction that gives the current f1 driver standings
    elif input_text == "@f1driver":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f1.driver_std(),
                sender=Sender(
                    name="F1",
                    # name=None
                    icon_url="https://cdn.discordapp.com/attachments/813130040938201131/852629478923960350/dux4xq5v0zs41.png",
                ),
            ),
        )

    elif input_text == "首抽":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=random_country(wiki_url),
                sender=Sender(
                    name="刷首抽轉盤",
                    # name=None
                    icon_url="https://cdn.discordapp.com/attachments/813130040938201131/889130450180784169/unknown.png",
                ),
            ),
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=random_reply(input_text)),
        )
