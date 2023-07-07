import requests
import json

from linebot import  LineBotApi, WebhookHandler

from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

headers = {'Authorization':'Bearer {}'.format(access_token),'Content-Type':'application/json'}

body = {
    'size': {'width': 2500, 'height': 640},    # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'bbb',                             # 選單名稱
    'chatBarText': 'b',                        # 選單在 LINE 顯示的標題
    'areas':[                                  # 選單內容
        {
          'bounds': {'x': 0, 'y': 0, 'width': 1250, 'height': 640},           # 選單位置與大小
          'action': {'type': 'uri', 'uri': 'https://line.me/R/nv/location/'}  # 點擊後開啟地圖定位，傳送位置資訊
        },
        {
          'bounds': {'x': 1251, 'y': 0, 'width':625, 'height': 640},     # 選單位置與大小
          'action': {'type': 'message', 'text':'雷達回波圖'}               # 點擊後傳送文字
        },
        {
          'bounds': {'x': 1879, 'y': 0, 'width':625, 'height': 640},     # 選單位置與大小
          'action': {'type': 'message', 'text':'地震資訊'}               # 點擊後傳送文字
        }
    ]
  }
# 向指定網址發送 request
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                      headers=headers,data=json.dumps(body).encode('utf-8'))
# 印出得到的結果
print(req.text)
req_data = req.json()
richMenuId = req_data.get('richMenuId')
print(richMenuId)


# step2

line_bot_api = LineBotApi(access_token)

# 開啟對應的圖片

with open('../images/line-bot-weather-demo.jpg', 'rb') as f:
    line_bot_api.set_rich_menu_image(richMenuId, 'image/jpeg', f)


# step 3

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/{}'.format(richMenuId), headers=headers)

print(req.text)


