from linebot import LineBotApi, WebhookHandler
from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
richMenuId = os.getenv('RICHMENUID')

line_bot_api = LineBotApi(access_token)
rich_menu_list = line_bot_api.get_rich_menu_list()
for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)
