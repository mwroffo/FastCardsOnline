from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
engine = create_engine('sqlite:////Users/_mexus/Documents/code/fastcardsonline/app.db')
Session = sessionmaker(bind=engine)
session = Session()
migrate = Migrate(app, db)

from app.DecksModel import DecksModel
decksmodel = DecksModel(
    '/Users/_mexus/Documents/code/fastcardsonline/app')

from app import routes, models