from flask import Flask, Blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    from . import db
    db.init_app(app) # configures app's teardown_context and cli

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app.DecksModel import DecksModel
decksmodel = DecksModel(
    '/Users/_mexus/Documents/code/fastcardsonline/app')

from app import models
