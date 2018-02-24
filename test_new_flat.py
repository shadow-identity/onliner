from unittest import TestCase
from unittest.mock import patch, call

from new_flat import get_new_flats, QueryUrl, Flat, Onliner, SearchConfig, Flats


class TestGetNewFlats(TestCase):

    def setUp(self):
        self.read_patcher = patch.object(SearchConfig, 'read')
        self.read_config_mock = self.read_patcher.start()
        self.make_search_url_patcher = patch.object(Onliner, 'make_search_url')
        self.make_search_url_mock = self.make_search_url_patcher.start()
        self.parse_response_patcher = patch.object(Onliner, 'parse_response')
        self.parse_response_mock = self.parse_response_patcher.start()
        self.requests_patcher = patch('new_flat.requests')
        self.requests_mock = self.read_patcher.start()
        self.is_new_flats_patcher = patch.object(Flats, 'is_new')
        self.is_new_flats_mock = self.is_new_flats_patcher.start()
        self.do_alert_patcher = patch('new_flat.do_alert')
        self.do_alert_mock = self.do_alert_patcher.start()

    def tearDown(self):
        self.read_patcher.stop()
        self.make_search_url_patcher.stop()
        self.parse_response_patcher.stop()
        self.requests_patcher.stop()
        self.is_new_flats_patcher.stop()
        self.do_alert_patcher.stop()

    def test_get_flats(self):
        query_url = QueryUrl('hi', 'lol')
        flat1 = Flat(id=1, price=2, url='foo')
        flat2 = Flat(id=2, price=2, url='bar')

        self.make_search_url_mock.return_value = query_url
        self.is_new_flats_mock.side_effect = [True, False]
        self.parse_response_mock.return_value = [flat1, flat2]

        get_new_flats()

        self.read_config_mock.assert_called_once()
        self.make_search_url_mock.assert_called_once_with(
            self.read_config_mock.return_value)
        self.requests_mock.get.assert_called_once_with(
            query_url.url_base, params=query_url.params)
        self.parse_response_mock.assert_called_with(
            self.requests_mock.get.return_value.json.return_value
        )
        self.is_new_flats_mock.assert_has_calls([call(flat1), call(flat2)])
        self.do_alert_mock.assert_called_once_with(flat1)

    def test_get_flats_new_url(self):
        get_new_flats('example.com')
