from config import Config
from contextlib import contextmanager
import sqlite3
from app import db, migrate
import flask_migrate

import click
from flask import current_app, g
from flask.cli import with_appcontext

@contextmanager
def get_db():
    """ yields a SQLAlchemy session instance, associated with current_app """
    if 'db' not in g:
        Session = db.session
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
    """ Flask-SQLAlchemy actually closes sessions automatically
    but I am including this for personal sanity. """
    session = g.pop('db', None)
    if session is not None:
        session.close()

def init_db():
    """ uses Migrate to init database. gets a session from get_db() """
    flask_migrate.init() # informed by models.py
    flask_migrate.migrate()
    flask_migrate.upgrade()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear existing data and create new tables. """
    init_db()
    click.echo('Database init: data cleared. tables reset.')

def init_app(app):
    """
    Registers teardown_context and adds cli commands. —mwroffo
    """
    app.teardown_appcontext(close_db)    # now flask will run close_db() after returning responses.
    app.cli.add_command(init_db_command) # now you can say: flask init-db, from shell.
