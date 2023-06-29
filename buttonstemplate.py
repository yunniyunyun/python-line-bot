from linebot import LineBotApi, WebhookHandler
# 需要額外載入對應的函示庫
from linebot.models import PostbackAction,URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate

from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
user_ID = os.getenv('USER_ID')


line_bot_api = LineBotApi(access_token)
line_bot_api.push_message(user_ID, TemplateSendMessage(
    alt_text='ButtonsTemplate',
    template=ButtonsTemplate(
        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
        title='BOOK.STUDIO',
        text='這是按鈕樣板',
        actions=[
            # 發送postback
            PostbackAction(
                label='postback',
                data='發送 postback'
            ),
            # 發送文字
            MessageAction(
                label='說 hello',
                text='hello'
            ),
            # 前往連結
            URIAction(
                label='前往 STEAM 教育學習網',
                uri='https://steam.oxxostudio.tw'
            )
        ]
    )
))