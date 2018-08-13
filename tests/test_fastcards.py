import os
import tempfile
import flask
from app.forms import DeckForm

import pytest

from app import app

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
    app = flask.Flask(__name__)
    deck_form = DeckForm()
    # with app.test_request_context('/browse_edit', data=data)
