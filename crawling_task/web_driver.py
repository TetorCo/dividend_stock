from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


def driver_start():

    ## user_agent 필요하면 추가
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument('window-size=1000x813')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--mute-audio')
    # options.add_argument('disable-gpu')
    # options.add_argument(f'user_agent={user_agent}')

    ## options setting
    chrome_options= Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  ## 브라우저에서 이미지 로딩을 하지 않습니다.
    chrome_options.add_argument('--mute-audio')  ## 브라우저에 음소거 옵션을 적용합니다.
    chrome_options.add_argument('incognito')  ## 시크릿 모드의 브라우저가 실행됩니다.
    chrome_options.add_argument('window-size={1000},{813}')  ## 브라우저 사이즈 설정
    chrome_options.add_experimental_option('detach', True)  ## 브라우저를 종료하지 않고 유지

    service = ChromeService(executable_path='/Users/taebeomkim/coding/dividend_stock_automatic_trading_project/chromedriver')

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
        # options=options
    )

    return driver


def quit(driver):

    driver.quit()


if __name__ == "__main__":

    from selenium.webdriver.common.by import By
    driver = driver_start()
    driver.get('https://investing.com/dividends-calendar/')
    # driver.get('https://www.google.com/')
    # result = driver.find_elements(By.CLASS_NAME, 'tile')
    # print(result)
    quit(driver)