import requests, json
from linebot import LineBotApi, WebhookHandler
from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

headers = {'Authorization':'Bearer {}'.format(access_token),'Content-Type':'application/json'}

print("A")
# step 1
body = {
    'size': {'width': 2500, 'height': 1200},   # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'aaa',                             # 選單名稱 ( 別名 Alias Id )
    'chatBarText': '選單 A',                    # 選單在 LINE 顯示的標題
    'areas':[                                  # 選單內容
        {
          'bounds': {'x': 0, 'y': 0, 'width': 830, 'height': 280},
          'action': {'type': 'postback', 'data':'no-data'}  # 按鈕 A 使用 postback
        },
        {
          'bounds': {'x': 835, 'y': 0, 'width':830, 'height': 640},
          'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'bbb', 'data':'change-to-bbb'} # 按鈕 B 使用 richmenuswitch
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

with open('../../images/line-rich-menu-switch-demo-a.jpg', 'rb') as f:
    line_bot_api.set_rich_menu_image(richMenuId, 'image/jpeg', f)


# step 3

body = {
    "richMenuAliasId":"aaa",
    "richMenuId":richMenuId
}
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias',
                      headers=headers,data=json.dumps(body).encode('utf-8'))
print(req.text)

# step 4
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/{}'.format(richMenuId), headers=headers)
print(req.text)