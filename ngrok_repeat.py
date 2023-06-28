from flask import Flask, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, 
                            StickerSendMessage, ImageSendMessage, LocationSendMessage)

from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

@app.route('/', methods=['POST'])
def linebot():
     # 取得收到的訊息內容
    body = request.get_data(as_text=True)
    try:
        # json 格式化訊息內容
        json_data = json.loads(body)
        access_token = os.getenv('ACCESS_TOKEN')
        secret = os.getenv('SECRET')
        # 確認 token 是否正確
        line_bot_api = LineBotApi(access_token)
        # 確認 secret 是否正確
        handler = WebhookHandler(secret)
        # 加入回傳的 headers
        signature = request.headers['X-Line-Signature']
        # 綁定訊息回傳的相關資訊
        handler.handle(body, signature)
        # 取得回傳訊息的 Token
        tk = json_data['events'][0]['replyToken']
        # 取得 LINe 收到的訊息類型
        type = json_data['events'][0]['message']['type']
        if type=='text':
            # 取得 LINE 收到的文字訊息
            msg = json_data['events'][0]['message']['text']
            if msg == '傳一張圖片吧':
                img_url = 'https://images.unsplash.com/photo-1687777238205-d7c572cde6cc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=688&q=80'
                reply = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
            elif msg == '美術館在哪?':
                reply = LocationSendMessage(title='美術館',
                                            address='80460高雄市鼓山區美術館路80號',
                                            latitude=22.660181,
                                            longitude=120.286149)
            else:
                reply = TextSendMessage(msg)
        elif type == 'sticker':
            # 取得 stickerId
            stickerId = json_data['events'][0]['message']['stickerId']
            # 取得 packageId
            packageId = json_data['events'][0]['message']['packageId']
            # 設定要回傳的表情貼圖
            reply = StickerSendMessage(sticker_id=stickerId, package_id=packageId)
        else:
            reply = TextSendMessage('我還不會回傳這東西')
        # 回傳訊息
        line_bot_api.reply_message(tk,reply)
    except:
        # 如果發生錯誤，印出收到的內容
        print('body', body)
    # 驗證 Webhook 使用，不能省略
    return 'OK'


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run()