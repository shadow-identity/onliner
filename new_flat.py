"""
Уведомляем, когда появляются новые квартиры в аренду на onliner.by

Параметры: URL из окна браузера

Первый запуск или запуск с URL:
- Сохранение параметров поиска в конфиг
- Поиск квартир

Запуск без параметров:
- Поиск квартир

Поиск квартир:
- Получаем url и query из конфига
- Отправляем запрос, парсим из ответа список квартир
- Сравниваем список с тем, что есть в базе
- Если есть новое:
  + сохраняем это в базу
  + показываем уведомление


- Параметры поиска в конфиге в yaml
- База квартир в yaml
"""

import json
from dataclasses import dataclass
from os.path import isfile
from typing import List
from urllib.parse import parse_qs, urlparse

import requests

from constants import BASE_API_URL, URL_PARAMETERS, URL_PARAMS_FILE


def get_new_flats():
    response = requests.get(BASE_API_URL, params=URL_PARAMETERS)
    flats = json.loads(response.text)
    filter_new_flats(flats)


def filter_new_flats(flats: List) -> List:
    """ Compare flats from params with flats from DB, save new flats and make an alert """

    return []


@dataclass()
class QueryUrl:
    url_base: str
    params: dict

@dataclass
class Flats:
    price: int
    coordinate_lat: float
    coordinate_long: float


class SearchConfig:
    @staticmethod
    def write(query_params: dict) -> None:
        file_params = 'w' if isfile(URL_PARAMS_FILE) else 'x'
        with open(URL_PARAMS_FILE, file_params) as f:
            json.dump(query_params, f)


    @staticmethod
    def read() -> dict:
        with open(URL_PARAMS_FILE) as f:
            params = json.load(f)
        return params


class Onliner:
    """ Send proper request to Onliner, return list of flats"""
    url_base = BASE_API_URL

    @staticmethod
    def parse_url(public_url: str) -> None:
        """
        :type public_url: str URL which user can see in browser window
        """
        parsed_url = urlparse(public_url)
        query = parse_qs(parsed_url.query)
        coordinates = parse_qs(parsed_url.fragment)
        query.update(coordinates)
        SearchConfig.write(query)

    @staticmethod
    def make_search_url(url_params: dict) -> QueryUrl:
        return QueryUrl(url_base=BASE_API_URL,
                        params=url_params)

    # todo: open notification with osascript -e 'display notification "Lorem ipsum dolor sit amet" with title "Title"'
