from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from pymongo.mongo_client import MongoClient

import web_driver
import time
import dotenv
import os

### load ENV File
dotenv.load_dotenv()

### URL
url = 'https://kr.investing.com/dividends-calendar/'
MONGODB_URI = os.getenv("MONGODB_URI")

def scroll_down(driver):

    ## 현재 스크롤 높이
    last_scroll_height = driver.execute_script('return document.body.scrollHeight')

    while True:

        ## 끝까지 스크롤 내리기
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(5)

        new_scroll_height = driver.execute_script('return document.body.scrollHeight')

        if new_scroll_height == last_scroll_height:
            break

        last_scroll_height = new_scroll_height


### 매수할 배당주 나라 선택
def select_usa(driver):

    ### 팝업창 뜰 때까지 대기
    time.sleep(120)

    ### ESC 입력
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(5)

    ### scroll down
    driver.execute_script('window.scrollBy(0, 300);')
    time.sleep(5)

    ### 필터 오픈
    driver.find_element(By.XPATH,
                    '//*[@id="filterStateAnchor"]').click()
    time.sleep(5)

    ### 나라 모두 지우기
    driver.find_element(By.XPATH,
                    '//*[@id="calendarFilterBox_country"]/div[1]/a[2]').click()
    time.sleep(5)

    ### 미국 선택
    driver.find_element(By.XPATH,
                    '//*[@id="country5"]').click()
    time.sleep(5)

    # print('한국 선택')
    # driver.find_element(By.XPATH,
    #                 '//*[@id="country11"]').click()

    ### 적용하기
    driver.find_element(By.XPATH,
                    '//*[@id="ecSubmitButton"]').click()
    time.sleep(5)

    ### scroll up
    driver.execute_script('window.scrollTo(0, 0)')
    time.sleep(5)

    ### scroll down
    driver.execute_script('window.scrollBy(0, 300);')
    time.sleep(5)


def click_this_week(driver):

    driver.find_element(By.XPATH,
            '//*[@id="timeFrame_thisWeek"]').click()  ## 이번 주
    
    scroll_down(driver)

    time.sleep(5)


def click_next_week(driver):

    # ### 팝업창 뜰 때까지 대기
    # time.sleep(120)

    # ### ESC 입력
    # ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # time.sleep(5)

    # driver.execute_script('window.scrollTo(0, 0)')
    # time.sleep(5)

    # driver.execute_script('window.scrollBy(0, 300);')
    # time.sleep(5)

    driver.find_element(By.XPATH,
            '//*[@id="timeFrame_nextWeek"]').click()  ## 다음 주
    time.sleep(5)

    scroll_down(driver)

    time.sleep(5)


def dividend_calendar_crawling(driver, uri):

    table = driver.find_elements(By.XPATH, '//*[@id="dividendsCalendarData"]/tbody/tr')
    time.sleep(5)

    total_list = []

    client = MongoClient(uri)
    db = client['dividendscalendar']
    collection = db['2023']

    for value in table:

        tag_list = value.find_elements(By.TAG_NAME, 'td')

        try:

            if len(tag_list) == 1:  ## 날짜 구분란
                continue
            else:

                ## no.2 주식 이름 및 코드
                stock_name = tag_list[1].find_element(By.TAG_NAME, 'span').text
                stock_code = tag_list[1].find_element(By.TAG_NAME, 'a').text
                # print(stock_name, stock_code)

                ## no.3 배당락일
                ex_dividend_year = int(tag_list[2].text[:4])
                ex_dividend_month = int(tag_list[2].text[6:8])
                ex_dividend_date = int(tag_list[2].text[10:12])
                # print(ex_dividend_year + '/' + ex_dividend_month + '/' + ex_dividend_date)

                ## no.4 배당
                dividend_rate = float(tag_list[3].text)
                # print(dividend_rate)

                ## no.6 배당 지불일
                dividend_pay_year = int(tag_list[5].text[:4])
                dividend_pay_month = int(tag_list[5].text[6:8])
                dividend_pay_date = int(tag_list[5].text[10:12])
                # print(dividend_pay_year + '/' + dividend_pay_month + '/' + dividend_pay_date)

                # ## no.7 수익률
                # print(tag_list[6].text[:-1])

                total_list.append([stock_name, stock_code,
                                    ex_dividend_year, ex_dividend_month, ex_dividend_date,
                                    dividend_rate,
                                    dividend_pay_year, dividend_pay_month, dividend_pay_date])

                query = {'stock_code': stock_code}

                ## $set은 MongoDB에서 사용하는 Update 연산자
                new_data = {'$set': {
                'stock_name': stock_name,
                'stock_code': stock_code,
                'dividend_rate': dividend_rate,
                'ex_date': {'year': ex_dividend_year, 'month': ex_dividend_month, 'day': ex_dividend_date},
                'pay_date': {'year': dividend_pay_year, 'month': dividend_pay_month, 'day': dividend_pay_date}
                }}

                collection.update_one(query, new_data, upsert=True)

                time.sleep(3)
        except:
            pass

    client.close()

    return total_list


if __name__ == "__main__":

    start_time = time.time()

    driver = web_driver.driver_start()

    driver.get(url)

    ### Start!
    select_usa(driver)

    # click_this_week(driver)
    # this_week_stock_list = dividend_calendar_crawling(driver, MONGODB_URI)

    time.sleep(5)

    click_next_week(driver)
    next_week_stock_list = dividend_calendar_crawling(driver, MONGODB_URI)

    web_driver.quit(driver)

    # print(this_week_stock_list)
    print()
    print(next_week_stock_list)

    end_time = time.time()

    print(f"소요 시간 : {end_time - start_time}초")

    # print(datetime.datetime.today())
    # print(datetime.datetime.strptime('2023-11-12', '%Y-%m-%d'))

    # test = dict()

