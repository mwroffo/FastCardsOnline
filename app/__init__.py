import shutil
import os
from flask import Flask, Blueprint
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy, Model
import sqlalchemy_utils
from flask_migrate import Migrate
import flask_migrate
import flask_login
import logging
from logging.handlers import SMTPHandler
import click
from flask.cli import with_appcontext

db = SQLAlchemy()
migrate = Migrate()
login = flask_login.LoginManager()
login.login_view = 'auth.login' # force users to login before seeing protected pages

# set up CLI:
@click.command('reset-db')
@with_appcontext
def reset_db_command():
    """ clear existing tables and re-initialize database. """
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(basedir, 'migrations')
    shutil.rmtree(path) # removing the migrations directory... 
    path = os.path.join(basedir, 'app.db')
    os.remove(path) # remove app.db

    flask_migrate.init() # reset everything
    flask_migrate.migrate()
    flask_migrate.upgrade()

    click.echo('Database full reset. done.')

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    db.init_app(app) # configures app's teardown_context and cli
    migrate.init_app(app, db)
    login.init_app(app) # register LoginManager

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    ### register CLI
    app.cli.add_command(reset_db_command)

    ### register email error logging:
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='FastCards Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app

from app.DecksModel import DecksModel
decksmodel = DecksModel(
    '/Users/_mexus/Documents/code/fastcardsonline/app')

from app import models
