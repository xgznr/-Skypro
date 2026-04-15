import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # Скрываем автоматизацию, чтобы куки работали лучше
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()

    yield driver
    driver.quit()


@pytest.fixture
def auth_driver(driver):
    driver.get("https://www.kinopoisk.ru")

    cookies = [
        {
            "name": "Session_id",
            "value": "3:1775721768.5.0.1775721768334:OekrwQ:4476.1.2:1|"
            "54056513.-1.20002.3:1775721768|"
            "3:11829094.826881._fuGHeew1_1lXGvfDSGIt9sj4bM",
            "domain": ".kinopoisk.ru"
        },
        {
            "name": "sessionid2",
            "value": "3:1775721768.5.0.1775721768334:OekrwQ:4476.1.2:1|"
            "54056513.-1.20002.3:1775721768|"
            "3:11829094.826881.fakesign0000000000000000000",
            "domain": ".kinopoisk.ru"
        }
    ]

    for cookie in cookies:
        driver.add_cookie(cookie)

    # Обновляем страницу, чтобы применить куки
    driver.refresh()
    import time
    time.sleep(3)  # Даем время на прогрузку хедера с аватаркой
    return driver
