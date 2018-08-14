# main.__init__.py
# declares the main blueprint for core functionality.

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes