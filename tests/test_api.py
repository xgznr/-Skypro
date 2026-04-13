import pytest
import allure
from pages.api_client import KinopoiskAPI


@pytest.fixture(scope="module")
def api():
    return KinopoiskAPI()


@allure.epic("API Кинопоиск")
@pytest.mark.api
class TestKinopoiskAPI:

    @allure.feature("Фильмы")
    @allure.title("Получение фильма по ID")
    def test_get_film_by_id(self, api):
        film_id = 303
        response = api.get_film(film_id)

        assert response.status_code == 200
        assert response.json()["kinopoiskId"] == film_id

    @allure.feature("Премьеры")
    @allure.title("Получение списка премьер")
    def test_get_premieres(self, api):
        response = api.get_premieres(2024, "JANUARY")

        assert response.status_code == 200
        assert len(response.json().get("items", [])) > 0

    @allure.feature("Похожие фильмы")
    @allure.title("Получение списка похожих фильмов")
    def test_get_similars(self, api):
        film_id = 301
        response = api.get_similars(film_id)

        assert response.status_code == 200
        assert "items" in response.json()

    @allure.feature("Поиск")
    @allure.title("Поиск фильма по ключевому слову")
    @pytest.mark.parametrize("keyword", ["Inception", "Начало"])
    def test_search_by_keyword(self, api, keyword):
        response = api.search_by_keyword(keyword)

        assert response.status_code == 200
        films = response.json().get("films", [])
        assert any(keyword.lower() in str(f.values()).lower() for f in films)

    @allure.feature("Ошибки")
    @allure.title("Запрос несуществующего фильма (400)")
    def test_get_non_existent_film(self, api):
        response = api.get_film(99999999)

        assert response.status_code == 400
