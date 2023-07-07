from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
import json, time

from earthquake import earth_quake
from message import reply_image, push_message, reply_message
from weather import current_weather, forecast, aqi

from dotenv import load_dotenv
import os

app = Flask(__name__)


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
channel_secret = os.getenv('SECRET')
authorization = os.getenv('AUTHORIZATION')

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    try:
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(channel_secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        json_data = json.loads(body)
        reply_token = json_data['events'][0]['replyToken']
        user_id = json_data['events'][0]['source']['userId']
        # print(json_data)
        if 'message' in json_data['events'][0]:
            if json_data['events'][0]['message']['type'] == 'location':
                address = json_data['events'][0]['message']['address'].replace('台','臺')
                print('address', address)
                # 回覆爬取到的相關氣象資訊
                reply_message(f'{address}\n\n{current_weather(address)}\n\n{aqi(address)}\n\n{forecast(address)}', reply_token, access_token)
            if json_data['events'][0]['message']['type'] == 'text':
                text = json_data['events'][0]['message']['text']
                if text == '雷達回波圖' or text == '雷達回波':
                    reply_image(f'https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MSC/O-A0058-003.png?{time.time_ns()}', reply_token, access_token)
                elif text == '地震資訊' or text == '地震':
                    msg = earth_quake()
                    push_message(msg[0], user_id, access_token)
                    reply_image(msg[1], reply_token, access_token)
                else:
                    reply_message(text, reply_token, access_token)
        print("OK")
    except Exception as e:
        print('main error', e)
    return 'OK'

if __name__ == "__main__":
    app.run()

