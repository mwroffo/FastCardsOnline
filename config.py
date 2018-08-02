import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sirius black'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # database changes according to user logged in? would this cause problems
    # when multiple users are signed in?
    SQLALCHEMY_TRACK_MODIFICATIONS = False
