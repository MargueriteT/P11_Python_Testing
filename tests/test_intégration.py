import pytest
import tempfile
from server import app
import os
import json
from flask import template_rendered
from contextlib import contextmanager


@contextmanager
def captured_templates(app):
    """ Context manager is used to check template's name """

    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def client():
    """ This fixture is used to simulate a client """

    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            with open('clubs.json') as c:
                json.load(c)['clubs']
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_index(client):
    """ Check the status code and the template's name for the index page """

    with captured_templates(app) as templates:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to the GUDLFT Registration Portal!' in response.data
        template, context = templates[0]
        assert template.name == 'index.html'


def test_showSummary_success(client):
    """ Check the status code and the template's name for the showSummary
    page if the email provide is valid """

    mock_request_data = {'email': 'john@simplylift.co'}
    with captured_templates(app) as templates:
        response = client.post('/showSummary', data=mock_request_data)
        assert response.status_code == 200
        assert 'john@simplylift.co' in response.data.decode('utf-8')
        template, context = templates[0]
        assert template.name == 'welcome.html'


def test_showSummary_failure(client):
    """ Check the status code and the template's name for the showSummary
    page if the email provide is invalid """

    mock_request_data = {'email': 'john@simplylift.com'}
    with captured_templates(app) as templates:
        response = client.post('/showSummary', data=mock_request_data)
        assert response.status_code == 200
        assert 'john@simplylift.com' not in response.data.decode('utf-8')
        template, context = templates[0]
        assert template.name == 'index.html'


def test_book_success(client):
    """ Check the status code and the template's name for the book page if
    the club's name and the competition's name are valid """

    with captured_templates(app) as templates:
        response = client.get('/book/Full Classic/Simply Lift')
        assert response.status_code == 200
        assert 'Full Classic' in response.data.decode('utf-8')
        assert 'Simply Lift' in response.data.decode('utf-8')
        assert 'Booking for Full Classic' in response.data.decode('utf-8')
        template, context = templates[0]
        assert template.name == 'booking.html'


def test_book_past_competition_failure(client):
    """ Check the status code and the template's name for the book page if
    the competition is already passed """

    with captured_templates(app) as templates:
        response = client.get('/book/Fall Classic/Simply Lift')
        assert response.status_code == 200
        assert 'This is a past competition, reservation is not available' in \
               response.data.decode('utf-8')
        assert 'john@simplylift.co' in response.data.decode('utf-8')
        template, context = templates[0]
        assert template.name == 'welcome.html'


def test_book_something_wrong_failure(client):
    """ Check the status code and the template's name for the book page if
    the club's name and the competition's name are somehow invalid """

    with captured_templates(app) as templates:
        response = client.get('/book/Simply Lift/Full Classic')
        assert response.status_code == 200
        assert 'Something went wrong-please try again' in \
               response.data.decode('utf-8')
        template, context = templates[0]
        assert template.name == 'index.html'


@pytest.mark.parametrize('places', ['7', '10'])
def test_purchasePlaces_failure(client, places):
    """ Check the status code and the template's name for the purchasePlaces
    page if the number of places required is superior to the points'
    club """

    mock_request_data = {'competition': 'Full Classic',
                         'club': 'Iron Temple',
                         'places': places}
    with captured_templates(app) as templates:
        response = client.post('/purchasePlaces', data=mock_request_data)
        print(response.data.decode('utf-8'))
        assert 'Not enough points to book' in response.data.decode('utf-8')
        assert response.status_code == 200
        template, context = templates[0]
        assert template.name == 'welcome.html'


def test_purchasePlaces_success(client):
    """ Check the status code and the template's name for the purchasePlaces
    page if the number of places required is inferior or equal to the points'
    club """

    mock_request_data = {'competition': 'Full Classic',
                         'club': 'Simply Lift',
                         'places': '2'}
    with captured_templates(app) as templates:
        response = client.post('/purchasePlaces', data=mock_request_data)
        assert '2 places reserved' in response.data.decode('utf-8')
        assert response.status_code == 200
        template, context = templates[0]
        assert template.name == 'welcome.html'


def test_purchasePlaces_failure_more_than_twelve(client):
    """ Check the status code and the template's name for the purchasePlaces
    page if the number of places required is snot superior to twelve"""

    mock_request_data = {'competition': 'Fully Classic',
                         'club': 'Iron Temple',
                         'places': 14}
    with captured_templates(app) as templates:
        response = client.post('/purchasePlaces', data=mock_request_data)
        assert response.status_code == 200
        template, context = templates[0]
        assert "Not possible to book more than twelve places." in \
               response.data.decode('utf-8')
        assert template.name == 'booking.html'


def test_purchasePlaces_failure_more_than_competition_places(client):
    """ Check the status code and the template's name for the purchasePlaces
    page if the number of places required is snot superior to twelve"""

    mock_request_data = {'competition': 'Full Classic',
                         'club': 'Iron Temple',
                         'places': 19}
    with captured_templates(app) as templates:
        response = client.post('/purchasePlaces', data=mock_request_data)
        assert response.status_code == 200
        template, context = templates[0]
        assert template.name == 'booking.html'


def test_board_success(client):
    """ Check the status code and the template's name for the board
    page """

    with captured_templates(app) as templates:
        response = client.get('/board/Simply Lift')
        assert response.status_code == 200
        assert 'Points board' in response.data.decode('utf-8')
        template, context = templates[0]
        assert template.name == 'board.html'


def test_logout(client):
    """ Check the status code and the template's name for logout and the
    redirection to index page """
    response = client.get('/logout')
    assert response.status_code == 302
    with captured_templates(app) as templates:
        response = client.get('/', follow_redirects=True)
        assert response.status_code == 200
        template, context = templates[0]
        assert template.name == 'index.html'