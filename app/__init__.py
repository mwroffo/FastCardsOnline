from flask import Flask, Blueprint
from config import Config

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    from . import db
    db.init_app(app) # configures app's teardown_context and cli
    return app

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)
# uncomment these lines after the other blueprints are built.
# from app.core import bp as core_bp
# app.register_blueprint(core_bp)
# from app.auth import bp as auth_bp
# app.register_blueprint(auth_bp)

from app.DecksModel import DecksModel
decksmodel = DecksModel(
    '/Users/_mexus/Documents/code/fastcardsonline/app')

from app import routes, models