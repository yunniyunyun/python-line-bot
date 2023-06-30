import requests
from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
richMenuId = os.getenv('RICHMENUID')

headers = {'Authorization':'Bearer {}'.format(access_token)}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/{}'.format(richMenuId), headers=headers)

print(req.text)