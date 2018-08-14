from flask import Flask
from config import Config
import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    db.init_app(app) # configures app's teardown_context and cli
    return app

from app.DecksModel import DecksModel
decksmodel = DecksModel(
    '/Users/_mexus/Documents/code/fastcardsonline/app')

from app import routes, models
