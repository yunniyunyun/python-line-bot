import requests, json
from dotenv import load_dotenv
import os


load_dotenv()

# 設定 request 的 headers，注意前方要有 Bearer
access_token = os.getenv('ACCESS_TOKEN')
user_ID = os.getenv('USER_ID')
headers = {'Authorization':'Bearer {}'.format(access_token),'Content-Type':'application/json'}

# 設定 request 的 body，必須包含 to 和 messages
body = {
    'to':user_ID,
    'messages':[{
            'type': 'text',
            'text': 'hello'
        }]
    }
# 向指定網址用 POST 方法發送 request
req = requests.request('POST', 'https://api.line.me/v2/bot/message/push',headers=headers,data=json.dumps(body).encode('utf-8'))
# 印出得到的結果
print(req.text)