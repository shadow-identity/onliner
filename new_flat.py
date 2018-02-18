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
from dataclasses import dataclass, asdict
from typing import List
from urllib.parse import parse_qs, urlparse, urlencode, urlunparse

import requests
from os.path import isfile

from constants import BASE_API_URL, URL_PARAMETERS, URL_PARAMS_FILE


def get_new_flats():
    response = requests.get(BASE_API_URL, params=URL_PARAMETERS)
    flats = json.loads(response.text)
    filter_new_flats(flats)


def filter_new_flats(flats: List) -> List:
    """ Compare flats from params with flats from DB, save new flats and make an alert """

    return []


@dataclass
class QueryParams:
    rent_type: List[str]
    price_min: int
    price_max: int
    currency: str
    bounds_lb_lat: str
    bounds_lb_long: str
    bounds_rt_lat: str
    bounds_rt_long: str
    page: int = 1


@dataclass()
class QueryUrl:
    url_base: str
    params: dict

@dataclass
class Flats:
    price: int
    coordinate_lat: float
    coordinate_long: float


class ConfigHandler:
    @staticmethod
    def update_url_params(query_params: QueryParams) -> None:
        file_params = 'w' if isfile(URL_PARAMS_FILE) else 'x'
        with open(URL_PARAMS_FILE, file_params) as f:
            json.dump(asdict(query_params), f)


    @staticmethod
    def read_url_params() -> QueryParams:
        with open(URL_PARAMS_FILE) as f:
            params = json.load(f)
        return QueryParams(**params)


class Onliner:
    """ Send proper request to Onliner, return list of flats"""
    url_base = BASE_API_URL

    def send_search_request(self, url_params: QueryParams) -> List[Flats]:
        pass

    def parse_url_params_from_site(self, public_url: str) -> None:
        """
        :type public_url: str URL which user can see in browser window
        """
        parsed_url = urlparse(public_url)
        query = parse_qs(parsed_url.query)
        coordinates = parse_qs(parsed_url.fragment)
        ConfigHandler.update_url_params(QueryParams(
            rent_type=query['rent_type[]'],
            price_min=int(query['price[min]'][0]),
            price_max=int(query['price[max]'][0]),
            currency=query['currency'][0],
            bounds_lb_lat=coordinates['bounds[lb][lat]'][0],
            bounds_lb_long=coordinates['bounds[lb][long]'][0],
            bounds_rt_lat=coordinates['bounds[rt][lat]'][0],
            bounds_rt_long=coordinates['bounds[rt][long]'][0],
            page=1
        ))

    def make_search_url(self, url_params: QueryParams) -> QueryUrl:
        return QueryUrl(url_base=BASE_API_URL,
                        params=asdict(url_params))

    # todo: open notification with osascript -e 'display notification "Lorem ipsum dolor sit amet" with title "Title"'
