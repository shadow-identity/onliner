import os

BASE_API_URL = 'https://ak.api.onliner.by/search/apartments'
FLATS_DB_NAME = 'flats_db.json'
APP_DIR = os.path.dirname(__file__)
URL_PARAMS_FILE = os.path.join(APP_DIR, 'query_params.json')