import os
import tempfile
import flask
import sys
sys.path.insert(0 '/Users/_mexus/Documents/code/FastCardsOnline/app')
import app.forms

import pytest, os, flask, tempfile
from flask import current_app, g

@pytest.fixture
def client():
    """ Called by each individual test """
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])

def test_request(client):
    current_app = flask.Flask(__name__)
    deck_form = DeckForm()
    # with app.test_request_context('/browse_edit', data=data)
