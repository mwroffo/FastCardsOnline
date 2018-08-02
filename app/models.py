from app.app import db

class User(db.Model):
    """ declares the SQL schema for a users table.
    inherits from db.Model, base class for all SQLAlchemy tables. """
    id = db.Column(db.Integer, primary_key=True)
    # you can declare columns as indexed to increase Search compatibility
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
