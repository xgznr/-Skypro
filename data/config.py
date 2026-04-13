import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL_API = "https://kinopoiskapiunofficial.tech"
X_API_KEY = os.getenv("API_KEY")
HEADERS = {
    "X-API-KEY": X_API_KEY,
    "Content-Type": "application/json"
}

BASE_URL_UI = "https://www.kinopoisk.ru"
