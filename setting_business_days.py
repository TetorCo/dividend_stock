from pymongo.mongo_client import MongoClient

import pandas_market_calendars as mcal
import datetime
import dotenv
import os

### load ENV File
dotenv.load_dotenv()

### MongoDB Stock Load
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)

# Send a ping to confirm a successful connection
try:
    
    nyse = mcal.get_calendar('NYSE')

    business_days_list = nyse.valid_days(start_date='2023-11-14', end_date='2023-12-31').strftime('%Y-%m-%d')

    temp = dict()

    for day in business_days_list:
        # year = day.split('-')[0]
        month = day.split('-')[1]
        date = day.split('-')[2]

        # if year not in temp:
        #     temp[year] = {}

        if month not in temp:
            temp[month] = {}

        if date not in temp[month]:
            temp[month][date] = {}

    db = client['dividendscalendar']
    collection = db['2023']
    collection.insert_one(temp)

except Exception as e:
    print(e)


client.close()