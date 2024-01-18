"""
MongoDB에 저장된 Investing.com의 배당 캘린더의 데이터를 불러와서 매일 구매할 배당주를 고르는 코드
"""

from pymongo.mongo_client import MongoClient

import datetime
import dotenv
import os

def export_data():
    ### load ENV File
    dotenv.load_dotenv()

    ### MongoDB Stock Load
    MONGODB_URI = os.getenv("MONGODB_URI")
    
    client = MongoClient(MONGODB_URI)
    db = client['dividendscalendar']
    collection = db['2023']

    today = datetime.datetime.today() + datetime.timedelta(days=7)
    ### 12/24 이후로는 str 제거하기
    stock_list = collection.find(
        {'ex_date':
            {
                'year': today.year,
                'month': today.month,
                'day': today.day
            }
        }
    )

    ## Transform Temp List / 변환 후 RDB 저장 전 임시 리스트
    transform_temp_list = []

    for stock_info in stock_list:
        transform_temp_list.append([stock_info['stock_code'], stock_info['dividend_rate'], stock_info['ex_date'], stock_info['pay_date']])

    client.close()

    ## 변환한 데이터를 반환
    return transform_temp_list


if __name__ == "__main__":

    print(export_data())