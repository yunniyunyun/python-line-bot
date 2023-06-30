from linebot import LineBotApi, WebhookHandler

from dotenv import load_dotenv
import os


load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
richMenuId = os.getenv('RICHMENUID')

line_bot_api = LineBotApi(access_token)

# import os
# os.chdir('/content/drive/MyDrive/Colab Notebooks')  # Colab 換路徑使用

# 開啟對應的圖片
with open('../images/line-rich-menu-demo.jpg', 'rb') as f:
    line_bot_api.set_rich_menu_image(richMenuId, 'image/jpeg', f)