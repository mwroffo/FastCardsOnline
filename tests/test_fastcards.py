import os, tempfile, pytest
from app import create_app, db
from config import TestingConfig, DevelopmentConfig
from app.models import User, Card
import flask
import pytest

@pytest.fixture(scope='module')
def test_client():
    """
    Initializes a client for a suite of functional tests for FastCards.
    """
    app = create_app(DevelopmentConfig) # init the flask instance

    # init werkzeug test client from flask instance. this will be used in functional tests.
    client = app.test_client()

    # an application context enables the flask instance to respond to GET and POST requests.
    app_context = app.app_context()
    app_context.push() # binds the current app to this app_context

    yield client
    # in pytest, everything after the yield statement serves as teardown:
    app_context.pop() # pop the context after each test.

@pytest.fixture(scope='module')
def init_db():
    db.create_all()
    u = User(username='billy', email='billy-bob@gmail.com')
    u2 = User(username='andrew', email='andrew-dude@comcastsucks.net')
    u.set_password('real_password')
    u2.set_password('that-is-an-L-bro')
    db.session.add(u)
    db.session.add(u2)
    db.session.commit()
    yield db    # TODO must admit I don't understand how yield is applicable, pytest.
                # what does this fixture have in common with generators?
    db.drop_all()

def test_login_redirect(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested via GET
    THEN check that the response is a 302 redirect.
    """
    response = test_client.get('/')
    assert response.status_code == 302

def test_login_200(test_client):
    """
    GIVEN a Flask app
    WHEN the '/login' page is requested via GET
    THEN check that the response is 200
    """
    response = test_client.get('/login')
    assert response.status_code == 200