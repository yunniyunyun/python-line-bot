import requests
from dotenv import load_dotenv
import os, statistics


load_dotenv()
authorization = os.getenv('AUTHORIZATION')

# 目前天氣函式
def current_weather(address):
    # 定義好待會要用的變數
    city_list, area_list, area_list2 = {}, {}, {}
    # 預設回傳訊息
    msg = '找不到氣象資訊。'

    # 定義取得資料的函式
    def get_data(url):
        # 爬取目前天氣網址的資料
        w_data = requests.get(url)
        # json 格式化訊息內容
        w_data_json = w_data.json()
        # 取出對應地點的內容
        location = w_data_json['cwbopendata']['location']  
        for i in location:
            name = i['locationName']                       # 測站地點
            city = i['parameter'][0]['parameterValue']     # 縣市名稱
            area = i['parameter'][2]['parameterValue']     # 鄉鎮行政區
            temp = check_data(i['weatherElement'][3]['elementValue']['value'])                       # 氣溫
            humd = check_data(round(float(i['weatherElement'][4]['elementValue']['value'] )*100 ,1)) # 相對濕度
            r24 = check_data(i['weatherElement'][6]['elementValue']['value'])                        # 累積雨量
            if area not in area_list:
                # 以鄉鎮區域為 key，儲存需要的資訊
                area_list[area] = {'temp':temp, 'humd':humd, 'r24':r24}
            if city not in city_list:
                # 以主要縣市名稱為 key，準備紀錄裡面所有鄉鎮的數值
                city_list[city] = {'temp':[], 'humd':[], 'r24':[]}
            city_list[city]['temp'].append(temp)   # 記錄主要縣市裡鄉鎮區域的溫度 ( 串列格式 )
            city_list[city]['humd'].append(humd)   # 記錄主要縣市裡鄉鎮區域的濕度 ( 串列格式 )
            city_list[city]['r24'].append(r24)     # 記錄主要縣市裡鄉鎮區域的雨量 ( 串列格式 )

    # 定義如果數值小於 0，回傳 False 的函式
    def check_data(e):
        return False if float(e)<0 else float(e)

    # 定義產生回傳訊息的函式
    def msg_content(loc, msg):
        a = msg
        for i in loc:
            if i in address: # 如果地址裡存在 key 的名稱
                temp = f"氣溫 {loc[i]['temp']} 度，" if loc[i]['temp'] != False else ''
                humd = f"相對濕度 {loc[i]['humd']}%，" if loc[i]['humd'] != False else ''
                r24 = f"累積雨量 {loc[i]['r24']}mm" if loc[i]['r24'] != False else ''
                description = f'{temp}{humd}{r24}'.strip('，')
                a = f'{description}。' # 取出 key 的內容作為回傳訊息使用
                break
        return a

    try:
        # 因為目前天氣有兩組網址，兩組都爬取
        get_data('https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization={}&downloadType=WEB&format=JSON'.format(authorization))
        get_data('https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0003-001?Authorization={}&downloadType=WEB&format=JSON'.format(authorization))

        for i in city_list:
            if i not in area_list2: 
                # 將主要縣市裡的數值平均後，以主要縣市名稱為 key，再度儲存一次，如果找不到鄉鎮區域，就使用平均數值
                area_list2[i] = {'temp':round(statistics.mean(city_list[i]['temp']),1),
                                'humd':round(statistics.mean(city_list[i]['humd']),1),
                                'r24':round(statistics.mean(city_list[i]['r24']),1)
                                }
        msg = msg_content(area_list2, msg)  # 將訊息改為「大縣市」
        msg = msg_content(area_list, msg)   # 將訊息改為「鄉鎮區域」
        return msg    # 回傳 msg
    except Exception as e:
        print('error', e)
        return msg    # 如果取資料有發生錯誤，直接回傳 msg

def forecast(address):
    area_list = {}
    json_api = {"宜蘭縣":"F-D0047-001","桃園市":"F-D0047-005","新竹縣":"F-D0047-009","苗栗縣":"F-D0047-013",
            "彰化縣":"F-D0047-017","南投縣":"F-D0047-021","雲林縣":"F-D0047-025","嘉義縣":"F-D0047-029",
            "屏東縣":"F-D0047-033","臺東縣":"F-D0047-037","花蓮縣":"F-D0047-041","澎湖縣":"F-D0047-045",
            "基隆市":"F-D0047-049","新竹市":"F-D0047-053","嘉義市":"F-D0047-057","臺北市":"F-D0047-061",
            "高雄市":"F-D0047-065","新北市":"F-D0047-069","臺中市":"F-D0047-073","臺南市":"F-D0047-077",
            "連江縣":"F-D0047-081","金門縣":"F-D0047-085"}
    msg = '找不到天氣預報資訊。'
    try:
        url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization={}&downloadType=WEB&format=JSON'.format(authorization)
        f_data = requests.get(url)
        f_data_json = f_data.json()
        location = f_data_json['cwbopendata']['dataset']['location']  
        for i in location:
            city = i['locationName']
            wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
            mint8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']
            maxt8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']
            ci8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']
            pop8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']
            area_list[city] = f'未來 8 小時{wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %'
        for i in area_list:
            if i in address:
                msg = area_list[i]
                url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/{json_api[i]}?Authorization={}&elementName=WeatherDescription'.format(authorization)
                f_data = requests.get(url)
                f_data_json = f_data.json()
                location = f_data_json['records']['locations'][0]['location']
                break
        for i in location:
            city = i['locationName']
            wd = i['weatherElement'][0]['time'][1]['elementValue'][0]['value']
            if city in address:
                msg = f'未來八小時天氣{wd}'
                break
        return msg
    except:
        return msg

# 空氣品質函式
def aqi(address):
    city_list, site_list ={}, {}
    msg = '找不到空氣品質資訊。'
    try:
        # 2022/12 時氣象局有修改了 API 內容，將部份大小寫混合全改成小寫，因此程式碼也跟著修正
        url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON'
        a_data = requests.get(url)             # 使用 get 方法透過空氣品質指標 API 取得內容
        a_data_json = a_data.json()            # json 格式化訊息內容
        for i in a_data_json['records']:       # 依序取出 records 內容的每個項目
            city = i['county']                 # 取出縣市名稱
            if city not in city_list:
                city_list[city]=[]             # 以縣市名稱為 key，準備存入串列資料
            site = i['sitename']               # 取出鄉鎮區域名稱
            aqi = int(i['aqi'])                # 取得 AQI 數值
            status = i['status']               # 取得空氣品質狀態
            site_list[site] = {'aqi':aqi, 'status':status}  # 記錄鄉鎮區域空氣品質
            city_list[city].append(aqi)        # 將各個縣市裡的鄉鎮區域空氣 aqi 數值，以串列方式放入縣市名稱的變數裡
        for i in city_list:
            if i in address: # 如果地址裡包含縣市名稱的 key，就直接使用對應的內容
                # 參考 https://airtw.epa.gov.tw/cht/Information/Standard/AirQualityIndicator.aspx
                aqi_val = round(statistics.mean(city_list[i]),0)  # 計算平均數值，如果找不到鄉鎮區域，就使用縣市的平均值
                aqi_status = ''  # 手動判斷對應的空氣品質說明文字
                if aqi_val<=50: aqi_status = '良好'
                elif aqi_val>50 and aqi_val<=100: aqi_status = '普通'
                elif aqi_val>100 and aqi_val<=150: aqi_status = '對敏感族群不健康'
                elif aqi_val>150 and aqi_val<=200: aqi_status = '對所有族群不健康'
                elif aqi_val>200 and aqi_val<=300: aqi_status = '非常不健康'
                else: aqi_status = '危害'
                msg = f'空氣品質{aqi_status} ( AQI {aqi_val} )。' # 定義回傳的訊息
                break
        for i in site_list:
            if i in address:  # 如果地址裡包含鄉鎮區域名稱的 key，就直接使用對應的內容
                msg = f'空氣品質{site_list[i]["status"]} ( AQI {site_list[i]["aqi"]} )。'
                break
        return msg    # 回傳 msg
    except:
        return msg    # 如果取資料有發生錯誤，直接回傳 msg