import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.main_page import MainPage
from data.config import BASE_URL_UI
from selenium.common.exceptions import StaleElementReferenceException


def wait_for_target_page(driver, timeout=80):
    """Ожидает появления основного контента страницы (тега body или h1)"""
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )


@pytest.mark.ui
@allure.feature("UI: Взаимодействие с сайтом")
class TestKinopoiskUi:

    @allure.story("Поиск фильма через хедер")
    def test_search_functional(self, driver):
        main_page = MainPage(driver)
        with allure.step("Открыть главную страницу"):
            driver.get(BASE_URL_UI)

        with allure.step("РУЧНОЕ ДЕЙСТВИЕ: Решите капчу"):
            wait_for_target_page(driver)

        with allure.step("Выполнить ввод названия 'Зеленая миля'"):
            main_page.search_film("Зеленая миля")

        with allure.step("Кликнуть по первому результату в поиске"):
            # Используем селектор, который вы нашли (ссылка на фильм 435)
            first_result = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "a[data-id='435']"))
            )
            driver.execute_script("arguments[0].click();", first_result)

        with allure.step("Проверить, что открылась страница фильма"):
            # Проверяем тот самый параграф с названием, который вы нашли ранее
            title_locator = (By.TAG_NAME, "h1")
            element = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(title_locator)
            )

            # Дополнительно проверяем и хлебные крошки, раз вы их нашли
            breadcrumb_locator = (By.CLASS_NAME, "breadcrumbs__link")
            breadcrumb = driver.find_element(*breadcrumb_locator)

            assert "Зеленая миля" \
                in element.text or "Зеленая миля" in breadcrumb.text

    @allure.story("Переход на страницу актера")
    def test_go_to_actor_page(self, driver):
        with allure.step("Открыть страницу фильма"):
            driver.get(f"{BASE_URL_UI}/film/327/")
        with allure.step("РУЧНОЕ ДЕЙСТВИЕ: Решите капчу"):
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.TAG_NAME, "h1"))
            )
        with allure.step("Кликнуть на первого актера в списке"):
            actor_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Пачино"))
            )
            # ВАЖНО: Вместо actor_link.click() используем JavaScript клик:
            driver.execute_script("arguments[0].click();", actor_link)

        with allure.step("Проверить, что открылся профиль актера"):
            WebDriverWait(driver, 20).until(EC.title_contains("Аль Пачино"))
        assert "Пачино" in driver.page_source

    @allure.story("Раздел ТОП-250")
    def test_top_250_open(self, driver):
        url = f"{BASE_URL_UI}/lists/movies/top250/"

        with allure.step(f"Перейти по прямой ссылке {url}"):
            driver.get(url)

        with allure.step("РУЧНОЕ ДЕЙСТВИЕ: Решите капчу"):
            wait_for_target_page(driver)

        with allure.step("Проверить заголовок страницы"):

            title = WebDriverWait(driver, 30).until(
                lambda d: d.find_element(By.TAG_NAME, "h1").text
                if "Подтвердите" not in d.find_element(By.TAG_NAME, "h1").text
                else False
            )

            allure.attach(title, name="Заголовок раздела")
            assert "250" in title

    @allure.story("Воспроизведение трейлера")
    def test_trailer_playback(self, driver):
        url = f"{BASE_URL_UI}/lists/movies/popular/"
        with allure.step(f"Открыть список популярных фильмов: {url}"):
            driver.get(url)

        with allure.step("РУЧНОЕ ДЕЙСТВИЕ: Решите капчу"):
            wait_for_target_page(driver)

        with allure.step("Нажать на кнопку 'Трейлер'"):
            xpath = (
                "//button[contains(@aria-label, 'трейлер')] | "
                "//button[contains(., 'Трейлер')]"
                )

            def click_with_retry(d):
                try:
                    btn = d.find_element(By.XPATH, xpath)
                    d.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", btn)
                    btn.click()
                    return True
                except (StaleElementReferenceException, Exception):
                    return False

            WebDriverWait(driver, 30).until(click_with_retry)

        with allure.step("Проверить наличие видеоплеера"):
            close_btn_visible = WebDriverWait(driver, 40).until(
                lambda d: d.find_element(
                    By.XPATH, "//button[@aria-label='Закрыть плеер трейлеров']"
                ).is_displayed()
            )

            assert close_btn_visible is True

    @allure.story("Раздел 'График кинопроката'")
    def test_open_premiere_schedule(self, driver):
        url = f"{BASE_URL_UI}/premiere/"

        with allure.step(f"Перейти на страницу графика проката: {url}"):
            driver.get(url)

        with allure.step("РУЧНОЕ ДЕЙСТВИЕ: Решите капчу"):

            wait_for_target_page(driver)

        with allure.step("Проверить наличие заголовка"):
            title = WebDriverWait(driver, 40).until(
                lambda d: d.find_element(By.TAG_NAME, "h1").text.lower()
                if "подтвердите" not in d.find_element(
                    By.TAG_NAME, "h1").text.lower()
                else False
            )

            assert "премьер" in title or "график" in title
