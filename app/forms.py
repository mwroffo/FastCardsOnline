from app.DecksModel import DecksModel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    # DataRequired makes the form refuse empty fields.
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')

class EntryForm(FlaskForm):
    mwroffo = DecksModel('mwroffo')
    decks = mwroffo.getDecks()
    # create a list of value, label pairs:
    choices = [] # declare choices:
    for deckname in decks.keys():  # populate choices.
        choices.append((deckname, deckname.upper()))
    # define fields:
    selectedDeck = SelectField(
        'Choose a deck: ',
        choices=choices,
        validators=[DataRequired()]
    )
    term = StringField('Term', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])
    # dont forget submit button:
    submit = SubmitField('Add card to deck')