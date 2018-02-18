import json
from unittest import TestCase
from unittest.mock import patch, mock_open

from constants import BASE_API_URL, URL_PARAMS_FILE
from new_flat import Onliner, QueryUrl, SearchConfig


class TestOnliner(TestCase):
    def setUp(self):
        self.site_url = 'https://r.onliner.by/ak/?rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_roo' \
                        'ms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms&price%5Bmin%5D=250&' \
                        'price%5Bmax%5D=540&currency=usd#bounds%5Blb%5D%5Blat%5D=53.80876065067' \
                        '746&bounds%5Blb%5D%5Blong%5D=27.6551628112793&bounds%5Brt%5D%5Blat%5D=' \
                        '53.89240290447646&bounds%5Brt%5D%5Blong%5D=27.740993499755863'
        self.query_url = 'https://ak.api.onliner.by/search/apartments?rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms&price%5Bmin%5D=250&price%5Bmax%5D=540&currency=usd&bounds%5Blb%5D%5Blat%5D=53.80876065067746&bounds%5Blb%5D%5Blong%5D=27.6551628112793&bounds%5Brt%5D%5Blat%5D=53.89240290447646&bounds%5Brt%5D%5Blong%5D=27.740993499755863'

        example_params_dict = {
            'rent_type[]': ['3_rooms', '4_rooms', '5_rooms', '6_rooms'],
            'price[min]': ['250'],
            'price[max]': ['540'],
            'currency': ['usd'],
            'bounds[lb][lat]': ['53.80876065067746'],
            'bounds[lb][long]': ['27.6551628112793'],
            'bounds[rt][lat]': ['53.89240290447646'],
            'bounds[rt][long]': ['27.740993499755863'],

        }
        self.example_params_dict = example_params_dict
        self.example_json_params = json.dumps(example_params_dict)

    @patch('new_flat.SearchConfig.write')
    def test_parse_url_to_dict(self, write_url_params):
        Onliner().parse_url(self.site_url)
        self.assertDictEqual(write_url_params.call_args[0][0], self.example_params_dict)

    @patch('new_flat.open', new_callable=mock_open)
    @patch('new_flat.json.dump')
    def test_write_url_params(self, mock_dump, mocked_open):
        SearchConfig().write(self.example_params_dict)
        mock_dump.assert_called_once_with(self.example_params_dict,
                                          mocked_open.return_value)

    def test_make_search_url(self):
        result = Onliner().make_search_url(self.example_params_dict)
        self.assertEqual(result, QueryUrl(BASE_API_URL, self.example_params_dict))

    def test_read_url_params(self):
        """ should read from file and return QS instance """
        with patch('new_flat.open', mock_open(read_data=self.example_json_params)) as m:
            result = SearchConfig.read()
        m.assert_called_once_with(URL_PARAMS_FILE)
        self.assertEqual(result, self.example_params_dict)
