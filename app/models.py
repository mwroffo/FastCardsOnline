from datetime import datetime
from app import db

class User(db.Model):
    """
    Declares the SQL schema for a `User`s table.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    cards = db.relationship('Card', backref='owner', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Card(db.Model):
    """
    Declares SQL schema for a cards table.
    Foreign key associates a card with a user.

    """
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(), nullable=False, unique=True, index=True)
    definition = db.Column(db.String(), nullable=False, index=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    deck_id = db.Column(db.Integer())
    def __repr__(self):
        return '<Card {} ; {} ; user_id={} ; deck_id={}>'.format(
            self.term, self.definition, self.user_id, self.deck_id)
