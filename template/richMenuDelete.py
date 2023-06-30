from linebot import LineBotApi, WebhookHandler
from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
deleteRichMenuId = 'richmenu-fa234808bf90be5c7eb65aa518dae77c'

line_bot_api = LineBotApi(access_token)
line_bot_api.delete_rich_menu(deleteRichMenuId)
