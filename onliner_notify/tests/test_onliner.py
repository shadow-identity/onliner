import json
from unittest import TestCase
from unittest.mock import patch, mock_open, call

from onliner_notify.constants import BASE_API_URL, URL_PARAMS_FILE
from onliner_notify.notify import Onliner, SearchConfig
from typings import QueryUrl, Flat


class TestOnliner(TestCase):
    maxDiff = None

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

    def test_parse_url_to_dict(self):
        search_config = Onliner().parse_url(self.site_url)
        self.assertDictEqual(search_config, self.example_params_dict)

    @patch('onliner_notify.notify.open', new_callable=mock_open)
    @patch('onliner_notify.notify.json.dump')
    def test_write_url_params(self, mock_dump, mocked_open):
        SearchConfig().write(self.example_params_dict)
        mock_dump.assert_called_once_with(self.example_params_dict,
                                          mocked_open.return_value)

    def test_make_search_url(self):
        result = Onliner().make_search_url(self.example_params_dict)
        self.assertEqual(result, QueryUrl(BASE_API_URL, self.example_params_dict))

    def test_read_url_params(self):
        """ should read from file and return QS instance """
        with patch('onliner_notify.notify.open',
                   mock_open(read_data=self.example_json_params)) as m:
            result = SearchConfig.read()
        m.assert_called_once_with(URL_PARAMS_FILE)
        self.assertEqual(result, self.example_params_dict)

    @patch.object(Onliner, 'parse_apartment', side_effect=['lol', 'kek'])
    def test_parse_response(self, patched_parse_apartment):
        example_response = {'apartments': ['lol', 'kek']}
        result = Onliner().parse_response(example_response)
        patched_parse_apartment.assert_has_calls([
            call(example_response['apartments'][0]),
            call(example_response['apartments'][1])
        ])
        self.assertListEqual(['lol', 'kek'], result)

    def test_parse_apartment(self):
        example_apartment = {
            'id': 265011,
            'price': {
                'amount': '666.00',
                'currency': 'USD',
                'converted': {'BYN': {'amount': '783.72',
                                      'currency': 'BYN'},
                              'USD': {'amount': '400.00',
                                      'currency': 'USD'}}},
            'rent_type': '3_rooms',
            'location': {'address': 'Фабричная',
                         'user_address': 'Минск, Фабричная, 16',
                         'latitude': 53.864586,
                         'longitude': 27.695686},
            'photo': 'https://content.onliner.by/apartment_rentals/299654/600x400/cd992783152f3cdccb68128e11fd91c2.jpeg',
            'contact': {'owner': True},
            'created_at': '2017-10-05T17:55:10+0300',
            'last_time_up': '2018-02-24T10:17:21+0300',
            'up_available_in': 33488,
            'url': 'https://r.onliner.by/ak/apartments/265011'}
        expected = Flat(id=265011, price=400, url='https://r.onliner.by/ak/apartments/265011')
        actual = Onliner.parse_apartment(example_apartment)
        self.assertEqual(expected, actual)
