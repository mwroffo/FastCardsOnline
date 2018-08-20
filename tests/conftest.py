import pytest
from app import create_app, db
from config import TestingConfig, DevelopmentConfig
from app.models import User, Card, Deck

@pytest.fixture(scope='module')
def loggedin_client(test_client):
    response = test_client.post('/login',
                                data=dict(
                                    username='mroffo', password='password', remember_me=False),
                                follow_redirects=True)
    # quickly confirm that login worked and we are at /index:
    assert b"Welcome, mroffo, to FastCards" in response.data
    assert b'New user?' not in response.data

@pytest.fixture(scope='module')
def test_client():
    """
    Initializes a client for a suite of functional tests for FastCards.
    """
    app = create_app(TestingConfig)  # init the flask instance

    # init werkzeug test client from flask instance. this will be used in functional tests.
    client = app.test_client()

    # an application context enables the flask instance to respond to GET and POST requests.
    app_context = app.app_context()
    app_context.push()  # binds the current app to this app_context

    yield client
    # in pytest, everything after the yield statement serves as teardown:
    app_context.pop()  # pop the context after each test.


@pytest.fixture(scope='module')
def init_db():
    db.create_all()
    u = User(username='mroffo', email='mroffo@umass.edu')
    u.set_password('password')
    d1 = Deck(deckname='Fall Out Boy songs', user=u)
    Card(term='This is side one.', definition='Flip me over.', deck=d1)
    Card(term='I know I am not your favorite record.',
         definition='But the songs you grow to like.', deck=d1)
    d2 = Deck(deckname='Feels Like This songs', user=u)
    Card(term='No more stuttering.', definition='Two hearts fluttering.', deck=d2)
    Card(term='This Narrow Gate.',
         definition='But by this grace, there is room for two.', deck=d2)
    db.session.add(u)
    db.session.commit()
    # TODO must admit I don't understand how yield is applicable, pytest.
    yield db
    # what does this fixture have in common with generators?
    db.drop_all()
