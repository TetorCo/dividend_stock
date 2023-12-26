import yfinance as yf
import time

def transfom_data(stock_list):
    stock_buy_list = []

    for stock_info in stock_list:
        try:
            stock_code = yf.Ticker(stock_info[0])
            previous_day_close = round(stock_code.history(period="1d")['Close'].values[0], 4)  ## 전일 해당 주식의 종가

            stock_info.append(previous_day_close)

            stock_buy_list.append(stock_info)

            time.sleep(2)
        except:
            pass

    return stock_buy_list