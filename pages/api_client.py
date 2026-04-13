import requests
import allure
from data.config import BASE_URL_UI, HEADERS


class KinopoiskAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.base_url = BASE_URL_UI

    @allure.step("Отправить GET запрос на {path}")
    def _get(self, path, params=None):
        url = f"{self.base_url}{path}"
        response = self.session.get(url, params=params)
        allure.attach(
            body=str(response.status_code),
            name="Статус-код",
            attachment_type=allure.attachment_type.TEXT
        )
        return response

    def get_film(self, film_id):
        return self._get(f"/api/v2.2/films/{film_id}")

    def get_premieres(self, year, month):
        return self._get(
            "/api/v2.2/films/premieres", params={"year": year, "month": month})

    def get_similars(self, film_id):
        return self._get(f"/api/v2.2/films/{film_id}/similars")

    def search_by_keyword(self, keyword):
        return self._get(
            "/api/v2.1/films/search-by-keyword", params={"keyword": keyword})
