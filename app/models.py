from datetime import datetime
from flask import current_app, g

class User(g.db.Model):
    """
    Declares the SQL schema for a `User`s table.
    """
    __tablename__ = 'users'
    id = g.db.Column(g.db.Integer, primary_key=True)
    username = g.db.Column(g.db.String(64), nullable=False, index=True, unique=True)
    email = g.db.Column(g.db.String(120), nullable=False, index=True, unique=True)
    cards = g.db.relationship('Card', backref='owner', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Card(g.db.Model):
    """
    Declares SQL schema for a cards table.
    Foreign key associates a card with a user.
    """
    __tablename__ = 'cards'
    id = g.db.Column(g.db.Integer, primary_key=True)
    term = g.db.Column(g.db.String(), nullable=False, unique=True, index=True)
    definition = g.db.Column(g.db.String(), nullable=False, index=True)
    user_id = g.db.Column(g.db.Integer(), g.db.ForeignKey('user.id'))
    deck_id = g.db.Column(g.db.Integer())
    def __repr__(self):
        return '<Card {} ; {} ; user_id={} ; deck_id={}>'.format(
            self.term, self.definition, self.user_id, self.deck_id)
