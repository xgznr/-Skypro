import pytest
import allure
from pages.main_page import MainPage
from data.config import BASE_URL_UI

@pytest.mark.ui
@allure.feature("UI: Взаимодействие с сайтом")
class TestKinopoiskUi:

    @allure.story("Поиск фильма через выпадающий список")
    def test_search_functional(self, driver):
        page = MainPage(driver)
        film_name = "Начало"

        with allure.step("Открыть главную страницу"):
            page.open(BASE_URL_UI)

        with allure.step(f"Ввести в поиск '{film_name}'"):
            page.type_search_query(film_name)

        with allure.step("Проверить, что первый результат содержит название фильма"):
            result_text = page.get_text_first_result()
            assert film_name.lower() in result_text.lower(), \
                f"Текст '{film_name}' не найден в результате: {result_text}"

    @allure.story("Раздел ТОП-250")
    def test_top_250_open(self, driver):
        page = MainPage(driver)
        url = f"{BASE_URL_UI}/lists/movies/top250/"

        with allure.step(f"Перейти в раздел ТОП-250: {url}"):
            page.open(url)

        with allure.step("Проверить заголовок страницы"):
            title = page.get_page_title()
            allure.attach(title, name="Заголовок раздела")
            assert "250" in title

    @allure.story("Воспроизведение трейлера")
    def test_trailer_playback(self, driver):
        page = MainPage(driver)
        url = f"{BASE_URL_UI}/lists/movies/popular/"

        with allure.step(f"Открыть список популярных фильмов: {url}"):
            page.open(url)

        with allure.step("Нажать на кнопку 'Трейлер'"):
            page.open_trailer()

        with allure.step("Проверить, что плеер отобразился"):
            assert page.is_player_visible() is True

    @allure.story("Раздел 'График кинопроката'")
    def test_open_premiere_schedule(self, driver):
        page = MainPage(driver)
        url = f"{BASE_URL_UI}/premiere/"

        with allure.step(f"Перейти на страницу премьер: {url}"):
            page.open(url)

        with allure.step("Проверить наличие ключевого слова в заголовке"):
            title = page.get_page_title()
            assert "премьер" in title.lower() or "график" in title.lower()

    @allure.story("Проверка наличия текста на странице")
    def test_page_content(self, driver):
        page = MainPage(driver)
        
        with allure.step("Открыть главную страницу"):
            page.open(BASE_URL_UI)
            
        with allure.step("Проверить наличие текста 'Онлайн-кинотеатр'"):
            page.check_page_contains_text("Онлайн-кинотеатр")

