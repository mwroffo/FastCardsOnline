from app import decksmodel # import the application superglobal decksmodel
from app.DecksModel import DecksModel
from app.DeckModel import DeckModel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, FormField, FieldList
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')

class DeckForm(FlaskForm):
    """
    `DeckForm` represents a row that shows a single deck,
    with review and browse_edit buttons that submit
    the corresponding DeckModel.

    `DeckForm` helps DecksForm render a list of the user's decks in index.html.

    `DeckForm` is passed to `FormField` in `DecksForm`.
    """
    review = SubmitField('Review')
    browse_edit = SubmitField('Browse/Edit')
    
class DecksForm(FlaskForm):
    """
    DecksForm helps render index.html. DecksForm populates itself
    with DeckForm rows with help from the global `decksmodel`.

    self._rows is a dict of all deckname:deckforms in the database.
    """
    rows = {}
    # for deckname, deckmodel in decksmodel._decks.items():
        # rows[deckname] = FieldList(FormField(DeckForm))
    

class CardForm(FlaskForm):
    """
    Represents a `Card` as a term StringField and a definition StringField.`
    `CardForm` is passed to `FormField` in `BrowseEditForm`.

    passing a term and definition (or `Card` object?) inits these fields
    with their current values in database.
    """
    term = StringField('Term', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])

class CardsForm(FlaskForm):
    """
    `CardsForm` uses `CardForm`s to dynamically render a Deck in rows,
    with cards displayed as mutable textfields.
    """
    # TODO

class BrowseEditForm(FlaskForm):
    """ Represents a Deck as a series of `CardForm`s. """
    # populate StringField deckname with the current deckname:
    deckname = StringField('deckname', validators=[DataRequired()])
    cards = FormField(CardsForm)
    entry_row = FormField(CardForm) # empty field goes at bottom to invite new card entries.
    submit = SubmitField('Add card to deck') # submit makes the changes in the deck, a table in the database.

    def __init__(self, deckmodel):
        """ takes a `DeckModel` as argument and creates a BrowseEditForm """
        self._deck = deckmodel
    def getDeckModel(self):
        return self._deck
