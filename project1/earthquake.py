import requests
from dotenv import load_dotenv
import os

load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')
channel_secret = os.getenv('SECRET')
authorization = os.getenv('AUTHORIZATION')

# 地震資訊函式
def earth_quake():
    # 預設回傳的訊息
    msg = ['找不到地震資訊','https://example.com/demo.jpg']
    try:
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={}'.format(authorization)
        # 爬取地震資訊網址
        e_data = requests.get(url)
        # json 格式化訊息內容
        e_data_json = e_data.json()
        # 取出地震資訊
        eq = e_data_json['records']['Earthquake']
        for i in eq:
            loc = i['EarthquakeInfo']['Epicenter']['Location']        # 地震地點
            val = i['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue']  # 芮氏規模
            dep = i['EarthquakeInfo']['FocalDepth']               # 地震深度
            eq_time = i['EarthquakeInfo']['OriginTime']               # 地震時間
            img = i['ReportImageURI']                                # 地震圖
            msg = [f'{loc}，芮氏規模 {val} 級，深度 {dep} 公里，發生時間 {eq_time}。', img]
            break     # 取出第一筆資料後就 break
        return msg    # 回傳 msg
    except:
        return msg    # 如果取資料有發生錯誤，直接回傳 msg