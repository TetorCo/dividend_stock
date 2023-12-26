from datetime import datetime, timedelta

import psycopg2
import os
import dotenv

dotenv.load_dotenv()

## PostgreSQL Info
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))

today = datetime.now().date()+timedelta(days=7)

## Connection Postgres DB
conn = psycopg2.connect(
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    database=POSTGRES_DB,
    host="localhost",
    port=POSTGRES_PORT
)

## Create Cursor
cursor = conn.cursor()

## Write SQL Query
sql_query = f"SELECT * FROM stock_info WHERE ex_date = '{today}' ;"
cursor.execute(sql_query)

## Result
stock_list = cursor.fetchall()

## Cursor & Connection Close
cursor.close()
conn.close()
# print(stock_list)

budget = 230.48  ## 달러
# budget = 1149.47  ## 달러
CHECK = True

buy_list = []

while CHECK:  ## 내 예산으로 아무 주식도 구매할 수 없을 때 까지 반복
    temp = []
    for stock_info in stock_list:
        buy_count = int(budget // stock_info[1])  ## 구매할 수 있는 주식 개수
        if buy_count > 0:  ## 주식을 구매할 수 있는 경우
            buy_cost = round(buy_count*stock_info[1], 2)  ## 주식 구매 비용
            # remain_cost = budget - buy_cost
            dividend_cost = buy_count*stock_info[2]  ## 배당금
            # print(f"stock_code: {stock_info[0]}, count: {buy_count}, buy_cost: {buy_cost}\ndividend_rate: {stock_info[1]}, dividend_cost: {buy_count*stock_info[1]}\n")
            if len(temp) == 0:
                temp.append([stock_info[0], dividend_cost, buy_count, buy_cost])
            else:
                if temp[0][1] < dividend_cost:  ## 기존에 저장된 배당금보다 새로운 배당금이 더 높을 때
                    del temp[0]
                    temp.append([stock_info[0], dividend_cost, buy_count, buy_cost])
                elif temp[0][1] == dividend_cost:  ## 두 주식의 배당금이 같을 때
                    ## 구매가격이 더 저렴한 주식을 선택
                    if temp[0][2] > buy_cost:
                        del temp[0]
                        temp.append([stock_info[0], dividend_cost, buy_count, buy_cost])

    if len(temp) == 0:  ## 구매할 수 있는 주식이 없는 경우
        CHECK = False
        continue

    budget -= temp[0][-1]
    buy_list.append(temp[0])
    print(buy_list)