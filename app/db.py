from flask_sqlalchemy import SQLAlchemy, SQLAlchemy.create_engine, SQLAlchemy.sessionmaker
import flask_migrate
from config import Config
from contextlib import contextmanager
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_SQLAlchemy():
    """ loads sqlalchemy(app) into g.sql_alchemy """
    g.sql_alchemy = SQLAlchemy(current_app)

@contextmanager
def get_db():
    """ yields a SQLAlchemy session instance, associated with current_app """
    if 'db' not in g:
        init_SQLAlchemy()
        # .session is Flask-SQLAlchemy's preconfigured session factory:
        Session = g.sql_alchemy.session
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
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """ uses Migrate to init database. gets a session from get_db() """
    db = get_db()
    g.migrate = get_migrate()
    flask_migrate.init() # informed by models.py
    flask_migrate.migrate()
    flask_migrate.upgrade()

def init_migrate():
    """ puts a Migrate(current_app, g.sql_alchemy) object into g.migrate """
    if 'sql_alchemy' not in g:
        init_SQLAlchemy() # ensures that db was initialized first
    g.migrate = flask_migrate.Migrate(current_app, g.sql_alchemy)

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
