"""
Уведомляем, когда появляются новые квартиры в аренду на onliner.by

Параметры: URL из окна браузера

Первый запуск или запуск с URL:
✓ Сохранение параметров поиска в конфиг
- Парсинг параметра с url
✓ Поиск квартир

Запуск без параметров:
✓ Поиск квартир

Поиск квартир:
✓ Получаем url и query из конфига
✓ Отправляем запрос, парсим из ответа список квартир
✓ Сравниваем список с тем, что есть в базе
- Если есть новое:
  ✓ сохраняем это в базу
  - показываем уведомление


✓ Параметры поиска в конфиге в json
✓ База квартир в json
"""
import argparse
import json
import math
from dataclasses import dataclass, asdict
from os.path import isfile
from typing import List, Optional, NewType, Dict
from urllib.parse import parse_qs, urlparse

import requests
from tinydb import TinyDB, Query

from constants import BASE_API_URL, URL_PARAMS_FILE, FLATS_DB_NAME


def get_new_flats(new_search_url: str = None):
    """
    Doing all stuff. As result returns alert if new flats was added
    # Save search config if new_search_url is given
    # Prepare URL
    # Request
    # Parse response
    # Check if new flats in response
    # Make alert if any
    """
    if new_search_url:
        search_config = Onliner.parse_url(new_search_url)
        SearchConfig().write(search_config)
    else:
        search_config = SearchConfig().read()
    query_url = Onliner().make_search_url(search_config)
    response = requests.get(query_url.url_base, params=query_url.params).json()
    flats = Onliner().parse_response(response)
    for flat in flats:
        if Flats().is_new(flat):
            do_alert(flat)


@dataclass
class QueryUrl:
    url_base: str
    params: dict


FlatId = NewType('FlatId', int)


@dataclass
class Flat:
    id: FlatId
    price: int
    url: str


class Flats:
    """
    Interface to operate with Flats data base
    """

    def __init__(self):
        """ connect to a db """
        self.db = TinyDB(FLATS_DB_NAME)

    def is_new(self, flat: Flat) -> bool:
        old_record = self._get_flat(flat.id)
        if old_record:
            if self._is_flats_identical(old_record, flat):
                return False
        self._upsert_flat(flat)
        return True

    def _get_flat(self, flat_id: FlatId) -> Optional[Flat]:
        """ db get query """
        flat_q = Query()
        return Flat(**self.db.get(flat_q.id == flat_id))

    def _is_flats_identical(self, old_record: Flat, flat: Flat) -> bool:
        """ db compare instances """
        return old_record == flat

    def _upsert_flat(self, flat: Flat) -> None:
        """ db upsert given flat """
        flat_q = Query()
        self.db.upsert(asdict(flat), flat_q.id == flat.id)


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
    def parse_url(public_url: str) -> Dict:
        """
        :type public_url: str URL which user can see in browser window
        """
        parsed_url = urlparse(public_url)
        query = parse_qs(parsed_url.query)
        coordinates = parse_qs(parsed_url.fragment)
        query.update(coordinates)
        return query

    @staticmethod
    def make_search_url(url_params: dict) -> QueryUrl:
        return QueryUrl(url_base=BASE_API_URL,
                        params=url_params)

    @staticmethod
    def parse_apartment(apartment: Dict) -> Flat:
        return Flat(
            id=apartment['id'],
            price=math.floor(float(apartment['price']['converted']['USD']['amount'])),
            url=apartment['url']
        )

    def parse_response(self, response: Dict) -> List[Flat]:
        return [self.parse_apartment(apartment) for apartment in response['apartments']]

    # todo: open notification with osascript -e 'display notification "Lorem ipsum dolor sit amet" with title "Title"'


def do_alert(flat: Flat) -> None:
    print(f'New flat for ${flat.price}! {flat.url}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check new flats at Onliner.by')
    parser.add_argument('--url', '-u', type=str,
                        help='Onliner.by url you want to use')

    args = parser.parse_args()

    get_new_flats(args.url)
