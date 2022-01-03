import pytest
from datetime import datetime


@pytest.fixture
def clubs_fixture():
    """ Simulation of clubs data """
    clubs = \
        [{
            "name": "Fake club",
            "email": "fake@mail.com",
            "points": "4"
        },
            {
                "name": "Another Fake club",
                "email": "anotherfake@mail.com",
                "points": "12"
            }
        ]
    return clubs


@pytest.fixture
def competitions_fixture():
    """ Simulation of competitions data """
    competitions = \
        [{
            "name": "Fake competition",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "5"
        },
            {
                "name": "Another Fake competition",
                "date": "2022-10-22 13:30:00",
                "numberOfPlaces": "25"
            }
        ]
    return competitions


def test_valid_email_showSummary(clubs_fixture):
    """ Check a valid email return the expected data"""

    email = clubs_fixture[0]['email']
    club = [club for club in clubs_fixture if club['email'] == email][0]
    assert club == clubs_fixture[0]


def test_invalid_email_showSummary(clubs_fixture):
    """ Check that an invalid email return an index error"""

    email = "invalid@mail.com"
    with pytest.raises(IndexError):
        club = [club for club in clubs_fixture if club['email'] == email][0]
        raise (IndexError, 'list index out of range')


def test_competitions_information_purchasePlaces(competitions_fixture):
    """ Check the selection of a competition in the dictionary based on the
    competition' name """

    competition = {"name": "Fake competition",
                   "date": "2020-10-22 13:30:00",
                   "numberOfPlaces": "5"}
    selected_competition = [c for c in competitions_fixture if c['name'] ==
                            competition["name"]][0]
    assert selected_competition == competition


def test_clubs_information_purchasePlaces(clubs_fixture):
    """ Check the selection of a club in the dictionary based on the
    club's name """

    club = {"name": "Another Fake club",
            "email": "anotherfake@mail.com",
            "points": "12"}
    selected_club = [c for c in clubs_fixture if c['name'] == club["name"]][0]
    assert selected_club == club


@pytest.mark.parametrize('places', ['2', '4'])
def test_places_required_inferior_or_equal_to_club_points(clubs_fixture,
                                                          places):
    """ Check the places required is inferior to the club' points """

    club = clubs_fixture[0]
    placesRequired = places
    assert int(placesRequired) <= int(club["points"])


def test_places_required_superior_to_club_points(clubs_fixture):
    """ Check the places required is superior to the club' points """

    club = clubs_fixture[0]
    placesRequired = 7
    assert placesRequired > int(club["points"])


@pytest.mark.parametrize('places', ['2', '5'])
def test_places_required_inferior_or_equal_to_competition_places(
        competitions_fixture, places):
    """ Check the places required is inferior or equal to the competitions'
    places """

    competition = competitions_fixture[0]
    placesRequired = int(places)
    assert placesRequired <= int(competition["numberOfPlaces"])


def test_places_required_superior_to_competition_places(competitions_fixture):
    """ Check the places required is superior to the competitions' places """

    competition = competitions_fixture[0]
    placesRequired = 7
    assert placesRequired > int(competition["numberOfPlaces"])


@pytest.mark.parametrize('places', ['7', '12'])
def test_places_required_inferior_or_equal_to_twelve(places):
    """ Check the places required is superior to the club' points """

    maximumPlaces = 12
    assert int(places) <= maximumPlaces


def test_places_required_superior_to_twelve():
    """ Check the places required is superior to the club' points """

    placesRequired = 19
    maximumPlaces = 12
    assert placesRequired > maximumPlaces


def test_transform_string_date_in_date(competitions_fixture):
    """ Check the transformation of a date in string to an actual date """

    competition = competitions_fixture[0]
    date = competition['date'][0:10]
    expected_value = "2020-10-22"
    date_transform = datetime.strptime(date, "%Y-%m-%d").date()
    expected_value_transform = datetime.strptime(expected_value,
                                                 "%Y-%m-%d").date()
    assert date == expected_value
    assert date_transform == expected_value_transform


def test_future_competition(competitions_fixture):
    """ Check the competition's date is after the actual date """

    result = datetime.strptime(competitions_fixture[0]['date'][0:10],
                               "%Y-%m-%d").date() > datetime.strptime(
        "2019-10-22", "%Y-%m-%d").date()
    assert result


def test_past_competition(competitions_fixture):
    """ Check the competition's date is already passed """

    result = datetime.strptime(competitions_fixture[0]['date'][0:10],
                               "%Y-%m-%d").date() > datetime.strptime(
        "2021-10-22", "%Y-%m-%d").date()
    assert not result


def test_remaining_points_available_after_booking(clubs_fixture):
    """ Check the club's points are updated after booking """

    club_point = int(clubs_fixture[0]["points"])
    placesRequired = 3
    remaining_points = club_point - placesRequired
    expected_value = 1
    assert remaining_points == expected_value
