from datetime import datetime
from app import db

class User(db.Model):
    """ declares the SQL schema for a users table.
    inherits from db.Model, base class for all SQLAlchemy tables. """
    id = db.Column(db.Integer, primary_key=True)
    # you can declare columns as indexed to increase Search compatibility
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # db.relationship connects "one" (User) to "many" ('Post'[s])
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    """
    Represents a blog post.

    Foreign key grabs id from user object
    this is how we associate a user with a post! (or a deck... :D)
    in database jargon, this is a "one-to-many" relationship
    because one user id appears in many posts,
    while one post is only written by one user.
    index=True allows entries of that column to be indexed so that 
    they can be accessed via indices aka chronilogical order.
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
