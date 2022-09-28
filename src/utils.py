from flask import Flask, request, abort
import os
import requests
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, Sender,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_TOKEN')
handler = WebhookHandler('YOUR_TOKEN')
