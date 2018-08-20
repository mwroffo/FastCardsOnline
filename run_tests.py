"""
Test suite for FastCardsOnline.
mwroffo August 2018
"""
import unittest
import os
import tempfile
from app import db, migrate, login, create_app
import app
from config import TestingConfig
from app.models import User, Card
import flask_login

class DatabaseCase(unittest.TestCase):
    """
    Instantiates a user and calls essential methods to the card database, etc.
    """
    def setUp(self):
        self.app = create_app(TestingConfig) # db is :memory:
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.init_app(self.app)
        db.create_all() # init tables
        # commit a user:
        u = User(username='joey', email='joey@gmail.com')
        u.set_password('real_password')
        db.session.add(u)
        db.session.commit()
        # TODO implement a request context to fix RuntimeError.
        # TODO also, UNIQUE constraint is failing. tearDown must
        # not be running properly.

        flask_login.login_user(u, remember=False)

    def tearDown(self):
        # TODO somehow this must not be deleting the user.
        db.drop_all()
        db.session.remove()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User.query.filter_by(username='mwroffo').first()
        self.assertFalse(u.check_password('incorrect_password'))
        self.assertTrue(u.check_password('real_password'))

    def test_database(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        tester = os.path.exists(os.path.join(basedir, 'app.db'))
        self.assertTrue(tester, "db connection should exist")

    def test_addCard(self):
        userID = flask_login.current_user
        card1 = Card(term='What is Pip\'s real name?',
            definition='Purity Tyler',
            user_id = flask_login.current_user.id)
        card2 = Card(term='Who is Andreas\'s only love?',
            definition='Annagret',
            user_id = flask_login.current_user.id)
        db.session.add_all([card1, card2])
        db.session.commit()

        

    def test_resetDB(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
