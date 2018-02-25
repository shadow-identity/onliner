from dataclasses import asdict
from unittest import TestCase
from unittest.mock import patch

from tinydb import Query
from tinydb.database import Document

from constants import FLATS_DB_NAME
from new_flat import Flats, Flat


class TestFlats(TestCase):
    def setUp(self):
        self.flat = Flat(id=1, price=2, url='ex.com')
        self.db_patcher = patch('new_flat.TinyDB')
        self.db_mock = self.db_patcher.start()

    def tearDown(self):
        self.db_patcher.stop()

    @patch.object(Flats, '_get_flat')
    @patch.object(Flats, '_is_flats_identical', return_value=True)
    def test_flat_exists(self, _is_flats_identical_mock, _get_flat_mock):
        self.assertFalse(Flats().is_new(self.flat))
        _is_flats_identical_mock.assert_called_once()
        _get_flat_mock.assert_called_once()

    @patch.object(Flats, '_get_flat', return_value=None)
    @patch.object(Flats, '_upsert_flat')
    def test_new_flat(self, _upsert_flat_mock, _get_flat_mock):
        self.assertTrue(Flats().is_new(self.flat))
        _upsert_flat_mock.assert_called_once()
        _get_flat_mock.assert_called_once()

    @patch.object(Flats, '_get_flat')
    @patch.object(Flats, '_is_flats_identical', return_value=False)
    @patch.object(Flats, '_upsert_flat')
    def test_flat_updated(self, _upsert_flat_mock, _is_flats_identical_mock, _get_flat_mock):
        self.assertTrue(Flats().is_new(self.flat))
        _upsert_flat_mock.assert_called_once()
        _get_flat_mock.assert_called_once()
        _is_flats_identical_mock.assert_called_once()

    def test_get_flat(self):
        self.db_mock.return_value.get.return_value = Document(
            asdict(self.flat), 'foo',
        )
        Flats()._get_flat(self.flat.id)
        self.db_mock.return_value.get.assert_called_once_with(Query().id == self.flat.id)

    def test_is_flats_identical(self):
        self.assertTrue(Flats()._is_flats_identical(self.flat, Flat(id=1, price=2, url='ex.com')))
        self.assertFalse(Flats()._is_flats_identical(self.flat, Flat(id=1, price=3, url='sldk')))

    def test_upsert_flat(self):
        Flats()._upsert_flat(self.flat)
        self.db_mock.return_value.upsert.assert_called_once_with(
            asdict(self.flat),
            Query().id == self.flat.id
        )

    def test_init(self):
        Flats()
        self.db_mock.assert_called_once_with(FLATS_DB_NAME)

    # todo: cover creating of a new db
