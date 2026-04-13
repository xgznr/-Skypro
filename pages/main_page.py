import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 120)
        # Список возможных имен поля поиска для гибкости
        self._search_locators = [(By.NAME, "q"), (By.NAME, "kp_query")]

    @allure.step("Открыть главную страницу: {url}")
    def open(self, url):
        self.driver.get(url)

    @allure.step("Найти поле поиска и ввести")
    def _find_search_field(self):
        """Внутренний метод для перебора локаторов поля поиска."""
        for locator in self._search_locators:
            try:
                return self.wait.until(EC.element_to_be_clickable(locator))
            except Exception:
                continue
        raise Exception(
            "Поле поиска не найдено ни по одному из локаторов (q, kp_query)")

    @allure.step("Выполнить поиск фильма: {name}")
    def search_film(self, name: str):
        search_field = self._find_search_field()
        search_field.clear()
        search_field.send_keys(name)
        search_field.send_keys(Keys.ENTER)

    @allure.step("Проверить наличие текста '{text}' на странице")
    def check_page_contains_text(self, text: str):
        locator = (By.TAG_NAME, "body")
        body_text = self.wait.until(
            EC.presence_of_element_located(locator)).text
        assert text.lower() in body_text.lower(
        ), f"Текст '{text}' не найден на странице"
