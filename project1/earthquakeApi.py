import requests
from dotenv import load_dotenv
import os


load_dotenv()
authorization = os.getenv('AUTHORIZATION')

url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={}'.format(authorization)
data = requests.get(url)
data_json = data.json()
eq = data_json['records']['Earthquake']    # 轉換成 json 格式
for i in eq:
    loc = i['EarthquakeInfo']['Epicenter']['Location']        # 地震地點
    val = i['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue']  # 芮氏規模
    dep = i['EarthquakeInfo']['FocalDepth']               # 地震深度
    eq_time = i['EarthquakeInfo']['OriginTime']               # 地震時間
    print(f'地震發生於{loc}，芮氏規模 {val} 級，深度 {dep} 公里，發生時間 {eq_time}')