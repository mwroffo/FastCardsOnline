from flask_sqlalchemy import SQLAlchemy, SQLAlchemy.create_engine, SQLAlchemy.sessionmaker
from flask_migrate import Migrate
from config import Config
from contextlib import contextmanager
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_SQLAlchemy():
    return SQLAlchemy(current_app)

@contextmanager
def get_db():
    """ Returns a SQLAlchemy session instance """
    if 'db' not in g:
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=engine)
        g.db = Session()
    try:
        yield g.db
        g.db.commit()
    except:
        g.db.rollback()
        raise
    finally:
        close_db()

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    g.migrate = get_migrate()
    # TODO use migrate to init tables in models.py

def get_migrate():
    g.migrate = Migrate(current_app, get_SQLAlchemy())

@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear existing data and create new tables. """
    init_db()
    click.echo('Database init: data cleared. tables reset.')

def init_app(app):
    """
    Performs essential setup tasks.
    """
    app.teardown_appcontext(close_db)    # now flask will run close_db() after returning responses.
    app.cli.add_command(init_db_command) # now you can say: flask init-db
