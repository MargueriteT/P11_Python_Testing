import unittest
from unittest.mock import patch, mock_open
import json

from server import loadClubs, loadCompetitions


class TestLoadJson(unittest.TestCase):
    def test_open_clubs(self):
        expected_value = {"clubs": [{"name": "fake_club",
                                     "email": "fake@mail.com",
                                     "points": "12"}]}

        read_data = json.dumps(expected_value)
        mock_clubs = mock_open(read_data=read_data)

        with patch('builtins.open', mock_clubs):
            result = loadClubs()

        self.assertEqual(expected_value['clubs'], result)

    def test_open_competitions(self):
        expected_value = {"competitions": [{"name": "FakeFest",
                                            "date": "2020-03-27 10:00:00",
                                            "numberOfPlaces": "25"}]}
        read_data = json.dumps(expected_value)
        mock_competitions = mock_open(read_data=read_data)
        with patch('builtins.open', mock_competitions):
            result = loadCompetitions()
        self.assertEqual(expected_value['competitions'], result)