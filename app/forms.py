from app.DecksModel import DecksModel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    # DataRequired makes the form refuse empty fields.
    username = StringField('Username', validators=[DataRequired(), ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')


class EntryForm(FlaskForm):
    mwroffo = DecksModel('mwroffo')
    decks = mwroffo.getDecks()
    # create a list of value, label pairs:
    choices = []
    for deckname in decks.keys():  # populate it:
        choices.append((deckname, deckname.upper()))
    deck = SelectField(
        'Choose a deck: ',
        choices=[choices]
    )
    term = StringField('term', validators=[DataRequired()])
    definition = StringField('definition', validators=[DataRequired()])
    submit = SubmitField('Add card to deck')
