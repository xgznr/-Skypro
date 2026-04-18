import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage:
    # Локаторы элементов
    SEARCH_LOCATORS = [(By.NAME, "kp_query"), (By.NAME, "q"), (By.CSS_SELECTOR, "input[name='kp_query']")]
    FIRST_RESULT_ITEM = (By.XPATH, '//div[contains(@class, "element") and contains(@class, "most_wanted")]')
    TRAILER_BUTTON = (By.XPATH, "//button[contains(@aria-label, 'трейлер')] | //button[contains(., 'Трейлер')]")
    PLAYER_CLOSE_BTN = (By.XPATH, "//button[@aria-label='Закрыть плеер трейлеров']")
    PAGE_TITLE = (By.TAG_NAME, "h1")
    BODY = (By.TAG_NAME, "body")

    def __init__(self, driver):
        self.driver = driver
        # Увеличенный таймаут для работы в условиях капчи
        self.wait = WebDriverWait(self.driver, 60)

    @allure.step("Открыть страницу: {url}")
    def open(self, url):
        self.driver.get(url)

    def _find_search_field(self):
        """Внутренний метод для перебора возможных локаторов поля поиска"""
        for locator in self.SEARCH_LOCATORS:
            try:
                return self.wait.until(EC.element_to_be_clickable(locator))
            except:
                continue
        raise Exception("Поле поиска не найдено ни по одному из локаторов")

    @allure.step("Ввести название фильма '{name}' в поиск")
    def type_search_query(self, name: str):
        search_field = self._find_search_field()
        search_field.click()
        search_field.clear()
        search_field.send_keys(name)


    @allure.step("Получить текст первого результата из списка подсказок")
    def get_text_first_result(self) -> str:
        """Ожидает появления подсказки и возвращает её полный текст"""

        FIRST_RESULT_ITEM = (By.XPATH, "//*[contains(@class, 'suggest-item')] | //*[contains(@class, 'most_wanted')]")
        element = self.wait.until(EC.visibility_of_element_located(FIRST_RESULT_ITEM))
        return element.text

    @allure.step("Нажать на кнопку воспроизведения трейлера")
    def open_trailer(self):
        def click_retry(d):
            try:
                btn = d.find_element(*self.TRAILER_BUTTON)
                d.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                btn.click()
                return True
            except:
                return False
        self.wait.until(click_retry)

    @allure.step("Проверить видимость плеера")
    def is_player_visible(self) -> bool:
        return self.wait.until(
            EC.visibility_of_element_located(self.PLAYER_CLOSE_BTN)
        ).is_displayed()

    @allure.step("Получить заголовок страницы (H1)")
    def get_page_title(self) -> str:
        """Возвращает текст заголовка, игнорируя страницу капчи"""
        return self.wait.until(
            lambda d: d.find_element(*self.PAGE_TITLE).text 
            if "подтвердите" not in d.find_element(*self.PAGE_TITLE).text.lower() 
            else False
        )

    @allure.step("Проверить наличие текста на странице")
    def check_page_contains_text(self, text: str):
        body_text = self.wait.until(EC.presence_of_element_located(self.BODY)).text
        assert text.lower() in body_text.lower(), f"Текст '{text}' не найден"
