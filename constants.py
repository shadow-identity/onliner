import os

BASE_API_URL = 'https://ak.api.onliner.by/search/apartments'
URL_PARAMETERS = {
    'rent_type[]': ['3_rooms', '4_rooms', '5_rooms', '6_rooms'],
    'price[min]': ['350'],
    'price[max]': ['540'],
    'currency': ['usd'],
    'bounds[lb][lat]': ['53.805079158541254'],
    'bounds[lb][long]': ['27.65880417077024'],
    'bounds[rt][lat]': ['53.86081740555721'],
    'bounds[rt][long]': ['27.723851668989703'],
    'page': ['1']
}

FLATS_DB_NAME = 'flats_db.json'
APP_DIR = os.path.dirname(__file__)
URL_PARAMS_FILE = os.path.join(APP_DIR, 'query_params.json')