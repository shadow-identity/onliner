import json
from dataclasses import asdict
from unittest import TestCase, skip
from unittest.mock import patch, mock_open

from constants import BASE_API_URL, URL_PARAMS_FILE
from new_flat import Onliner, QueryParams, QueryUrl, ConfigHandler


class TestOnliner(TestCase):
    def setUp(self):
        self.site_url = 'https://r.onliner.by/ak/?rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_roo' \
                        'ms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms&price%5Bmin%5D=250&' \
                        'price%5Bmax%5D=540&currency=usd#bounds%5Blb%5D%5Blat%5D=53.80876065067' \
                        '746&bounds%5Blb%5D%5Blong%5D=27.6551628112793&bounds%5Brt%5D%5Blat%5D=' \
                        '53.89240290447646&bounds%5Brt%5D%5Blong%5D=27.740993499755863'
        self.query_url = 'https://ak.api.onliner.by/search/apartments?rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms&price%5Bmin%5D=250&price%5Bmax%5D=540&currency=usd&bounds%5Blb%5D%5Blat%5D=53.80876065067746&bounds%5Blb%5D%5Blong%5D=27.6551628112793&bounds%5Brt%5D%5Blat%5D=53.89240290447646&bounds%5Brt%5D%5Blong%5D=27.740993499755863'

        example_params = QueryParams(
            rent_type=['3_rooms', '4_rooms', '5_rooms', '6_rooms'],
            price_min=250,
            price_max=540,
            currency='usd',
            bounds_lb_lat='53.80876065067746',
            bounds_lb_long='27.6551628112793',
            bounds_rt_lat='53.89240290447646',
            bounds_rt_long='27.740993499755863',
        )
        self.example_params = example_params
        self.example_json_params = json.dumps(asdict(example_params))


    @skip
    def test_send_search_request(self):
        self.fail()

    @patch('new_flat.ConfigHandler.update_url_params')
    def test_parse_url_params_from_site(self, update_url_params_mock):
        Onliner().parse_url_params_from_site(self.site_url)
        update_url_params_mock.assert_called_once_with(self.example_params)

    @patch('new_flat.open', new_callable=mock_open)
    @patch('new_flat.json.dump')
    def test_update_url_params(self, mock_dump, mocked_open):
        ConfigHandler().update_url_params(self.example_params)
        mock_dump.assert_called_once_with(asdict(self.example_params), mocked_open.return_value)

    def test_make_search_url(self):
        result = Onliner().make_search_url(self.example_params)
        self.assertEqual(result, QueryUrl(BASE_API_URL, asdict(self.example_params)))

    def test_read_url_params(self):
        """ should read from file and return QS instance """
        with patch('new_flat.open', mock_open(read_data=self.example_json_params)) as m:
            result = ConfigHandler.read_url_params()
        m.assert_called_once_with(URL_PARAMS_FILE)
        self.assertEqual(result, self.example_params)
