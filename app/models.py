from datetime import datetime
from flask import current_app, g
from app import db, migrate, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    Declares the SQL schema for a `User`s table.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    decks = db.relationship('Deck', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id): # remember that Flask-Login needs a load_user function to call.
    return User.query.get(int(id)) # remember that the str id must be cast to int.

class Deck(db.Model):
    """
    A Deck associates numerous cards with each other, and itself with a user.
    """
    # rows:
    id = db.Column(db.Integer, primary_key=True)
    deckname = db.Column(db.String())
    # foreign keys and relationships:
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    cards = db.relationship('Card', backref='deck', lazy='dynamic')

    def __repr__(self):
        return '<Deck {}>'.format(self.deckname)

class Card(db.Model):
    """
    Declares SQL schema for a cards table.
    Foreign key associates a card with a user.
    """
    # rows:
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(), nullable=False, unique=True, index=True)
    definition = db.Column(db.String(), nullable=False, index=True)
    # foreign keys and relationships:
    deck_id = db.Column(db.Integer(), db.ForeignKey('deck.id'), nullable=False)

    def __repr__(self):
        return '<Card {} ; {}>'.format(
            self.term, self.definition)
