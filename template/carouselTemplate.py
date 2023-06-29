from linebot import LineBotApi, WebhookHandler
# 需要額外載入對應的函示庫
from linebot.models import PostbackAction,URIAction, MessageAction, TemplateSendMessage
from linebot.models import MessageAction, TemplateSendMessage, CarouselTemplate,  CarouselColumn

from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
user_ID = os.getenv('USER_ID')

line_bot_api = LineBotApi(access_token)
line_bot_api.push_message(user_ID, TemplateSendMessage(
    alt_text='CarouselTemplate',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                title='選單 1',
                text='說明文字 1',
                actions=[
                    PostbackAction(
                        label='postback',
                        data='data1'
                    ),
                    MessageAction(
                        label='hello',
                        text='hello'
                    ),
                    URIAction(
                        label='oxxo.studio',
                        uri='http://oxxo.studio'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                title='選單 2',
                text='說明文字 2',
                actions=[
                    PostbackAction(
                        label='postback',
                        data='data1'
                    ),
                    MessageAction(
                        label='hi',
                        text='hi'
                    ),
                    URIAction(
                        label='STEAM 教育學習網',
                        uri='https://steam.oxxostudio.tw'
                    )
                ]
            )
        ]
    )
))