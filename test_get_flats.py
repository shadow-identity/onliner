from unittest import TestCase
from unittest.mock import patch

from constants import URL_PARAMETERS, BASE_API_URL
from new_flat import get_new_flats


class TestNewFlat(TestCase):
    @patch('new_flat.requests.get')
    @patch('new_flat.filter_new_flats')
    @patch('new_flat.json.loads')
    def test_get_flats(self, mock_json_loads, mock_get_new_flats, mock_requests_get):
        result = get_new_flats()
        mock_requests_get.assert_called_once_with(BASE_API_URL, params=URL_PARAMETERS)
        mock_json_loads.assert_called_once_with(mock_requests_get.return_value.text)
        mock_get_new_flats.assert_called_once_with(mock_json_loads.return_value)


class TestGetNewFlats(TestCase):
    def test_filter_new_flats(self):
        self.fail()

