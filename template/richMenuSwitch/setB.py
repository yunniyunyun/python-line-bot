import requests, json
from linebot import LineBotApi, WebhookHandler
import requests
import json

from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

# step 1
headers = {'Authorization':'Bearer {}'.format(access_token),'Content-Type':'application/json'}
print("B")

body = {
    'size': {'width': 2500, 'height': 1200},   # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'bbb',                             # 選單名稱 ( 別名 Alias Id )
    'chatBarText': '選單 B',                    # 選單在 LINE 顯示的標題
    'areas':[                                  # 選單內容
        {
          'bounds': {'x': 0, 'y': 0, 'width': 830, 'height': 280},
          'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'aaa', 'data':'change-to-aaa'} # 按鈕 A 使用 richmenuswitch
        },
        {
          'bounds': {'x': 835, 'y': 0, 'width':830, 'height': 640},
          'action': {'type': 'postback', 'data':'no-data'}          # 按鈕 B 使用 postback
        },
        {
          'bounds': {'x': 1670, 'y': 0, 'width':830, 'height': 640},
          'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'ccc', 'data':'change-to-ccc'} # 按鈕 C 使用 richmenuswitch
        }
    ]
  }
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                      headers=headers,data=json.dumps(body).encode('utf-8'))
print(req.text)
req_data = req.json()
richMenuId = req_data.get('richMenuId')
print(richMenuId)

# step 2

line_bot_api = LineBotApi(access_token)

# import os
# os.chdir('/content/drive/MyDrive/Colab Notebooks')  # Colab 換路徑使用

# 開啟對應的圖片
with open('../../images/line-rich-menu-switch-demo-b.jpg', 'rb') as f:
    line_bot_api.set_rich_menu_image(richMenuId, 'image/jpeg', f)

# step 3
body = {
    "richMenuAliasId":"bbb",
    "richMenuId":richMenuId
}
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias',
                      headers=headers,data=json.dumps(body).encode('utf-8'))
print(req.text)

# step 4
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/{}'.format(richMenuId), headers=headers)
print(req.text)