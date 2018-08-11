from datetime import datetime
from app import db

class User(db.Model):
    """
    Declares the SQL schema for a `User`s table.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # you can declare columns as indexed to increase Search compatibility
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    # db.relationship connects "one" (User) to "many" ('Post'[s])
    decks = db.relationship('Deck', backref='owner', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)