
from linebot import LineBotApi, WebhookHandler
# 需要額外載入對應的函示庫
from linebot.models import MessageAction, TemplateSendMessage, ConfirmTemplate

from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
user_ID = os.getenv('USER_ID')


line_bot_api = LineBotApi(access_token)
line_bot_api.push_message(user_ID, TemplateSendMessage(
    alt_text='ConfirmTemplate',
    template=ConfirmTemplate(
            text='你好嗎？',
            actions=[
                MessageAction(
                    label='好',
                    text='好'
                ),
                MessageAction(
                    label='不好',
                    text='不好'
                )
            ]
        )
))