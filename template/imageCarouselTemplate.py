from linebot import LineBotApi, WebhookHandler
# 需要額外載入對應的函示庫
from linebot.models import MessageAction, TemplateSendMessage, ImageCarouselTemplate, ImageCarouselColumn

from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
user_ID = os.getenv('USER_ID')


line_bot_api = LineBotApi(access_token)
line_bot_api.push_message(user_ID, TemplateSendMessage(
    alt_text='ImageCarousel template',
    template=ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url='https://upload.wikimedia.org/wikipedia/en/a/a6/Pok%C3%A9mon_Pikachu_art.png',
                action=MessageAction(
                    label='皮卡丘',
                    text='皮卡丘'
                )
            ),
            ImageCarouselColumn(
                image_url='https://upload.wikimedia.org/wikipedia/en/5/59/Pok%C3%A9mon_Squirtle_art.png',
                action=MessageAction(
                    label='傑尼龜',
                    text='傑尼龜'
                )
            )
        ]
    )
))