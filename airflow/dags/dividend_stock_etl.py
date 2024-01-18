from airflow.decorators import dag, task
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.postgres.hooks.postgres import PostgresHook

import datetime, time

today = datetime.datetime.today()

MONGO_DB_CONN_ID = 'mongo_default'
POSTGRES_DB_CONN_ID = 'dividend_stock_db'

default_args = {
    'owner': 'airflow',
    'start_date': datetime.datetime(2024, 1, 18)
}

@dag(
    'test_dividend_stock_etl',
    default_args = default_args,
    catchup = False,
    schedule_interval = '0 1 * * 1-5',  # MON ~ FRI / 01:00
    tags = ['test']
)
def dividend_stock_etl():

    @task()
    def mongo_db_to_extract_data():

        hook = MongoHook(mongo_conn_id = MONGO_DB_CONN_ID)
        query = {
            'ex_date': {
                'year': today.year,
                'month': today.month,
                'day': today.day + 7
            }
        }

        today_stock_list = hook.find(
            query = query,
            mongo_collection = '2023'
        )

        ## Extract to Mongo DB Stock Data List
        mongo_db_stock_list = []

        for stock_info in today_stock_list:
            mongo_db_stock_list.append(
                [
                    stock_info['stock_code'],
                    stock_info['dividend_rate'],
                    stock_info['ex_date'],
                    stock_info['pay_date']
                ]
            )

        return mongo_db_stock_list


    @task()
    def transform_stock_data(mongo_db_stock_list):

        import yfinance as yf

        today_dividend_stock_list = []

        for stock_info in mongo_db_stock_list:

            try:

                stock_code = yf.Ticker(stock_info[0])
                previous_day_close = round(stock_code.history(period="1d")['Close'].values[0], 4)  ## 전일 해당 주식의 종가

                ## Transform EX-Date & Pay-Date
                ex_date = stock_info[2]
                pay_date = stock_info[3]

                stock_info = stock_info[:-2]

                ## Add Stock Previous Close
                stock_info.insert(1, previous_day_close)

                stock_info.append(datetime.datetime(
                    ex_date['year'], ex_date['month'], ex_date['day']))

                stock_info.append(datetime.datetime(
                    pay_date['year'], pay_date['month'], pay_date['day']
                ))

                today_dividend_stock_list.append(stock_info)

                time.sleep(2)
            except:

                pass

        return today_dividend_stock_list


    @task()
    def load_to_postgres(today_dividend_stock_list):
        
        hook = PostgresHook(postgres_conn_id = POSTGRES_DB_CONN_ID)
        conn = hook.get_conn()
        cursor = conn.cursor()

        try:

            cursor.executemany(
                "INSERT INTO stock_info (code, cost, dividend_rate, ex_date, pay_date) VALUES (%s, %s, %s, %s, %s)",
                today_dividend_stock_list
            )
            conn.commit()

        except:

            pass

        finally:
        
            cursor.close()
            conn.close()


    extract_dividend_stock_data = mongo_db_to_extract_data()
    transforms_dividend_stock_data = transform_stock_data(extract_dividend_stock_data)
    load_to_postgres(transforms_dividend_stock_data)


ETL_DAG = dividend_stock_etl()