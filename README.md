# line-bot
Line messenger bot

This project is a Line Chatbot that provides automated responses. It was developed in Python and uses the Line Python SDK, web scrapping and OpenWeather API for chat operations.

## ✨ Demo
![linebot_sample](https://github.com/FISHWONGY/line-bot/assets/59711659/20cd6f7c-0b5c-4c77-9b13-d0863bcf76e0)


## 📁 Folder Structure
```
├── README.md
├── requirements.txt
└── src
    ├── helpers
    │   ├── f1.py
    │   ├── functions.py
    │   └── owmapi.py
    ├── linebot_message.py
    ├── main.py
    └── utils.py
```

## 🚀 Installation

```git clone https://github.com/FISHWONGY/line-bot/```

```pip install -r requirements.txt```

## ✨ Hosting
1. Create an account on [LINE Developer](https://developers.line.biz/en/)
2. Register an Messanging API
3. Use [ngrok](https://dashboard.ngrok.com/) for webhook
4. Run ```ngrok http 5000```
5. Change webhook URL in Messaging API

## ✨ Current usages
- Auto Reply
    - Auto reply when text messeges/ command is received
- Open Weather API
    - Grab weather data from different city
- Web scrapper
    - Scrape https://www.f1.com to get F1 weekly race calender 
    - Scrpae the F1 website to get current driver/ constructor championship stnading
    - Scrape table from wiki
- Count down
    - Count down function to certain date/ events
- Random Drawing
    - Automatically choose restaurant

