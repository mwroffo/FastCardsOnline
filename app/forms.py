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

class CardForm(FlaskForm):
    """
    Represents a `Card` as a term StringField and a definition StringField.`
    `CardForm` is passed to `FormField` in `BrowseEditForm`.

    passing a term and definition (or `Card` object?) inits these fields
    with their current values in database.
    """
    term = StringField(label='Term', validators=[DataRequired()], default='Enter a new term')
    definition = StringField(label='Definition', validators=[DataRequired()], default='Enter a new definition')

class BrowseEditForm(FlaskForm):
    """
    `BrowseEditForm` uses `CardForm`s to dynamically render a Deck in rows,
    with cards displayed as mutable textfields.
    """
    deckname = StringField('Enter a name for this Deck: ', validators=[DataRequired()])
    cards = FieldList(FormField(CardForm), min_entries=1)
    # empty field goes at bottom to invite new card entries.
    entry_row = FormField(CardForm)
    # submit makes the changes in the deck, a table in the database.
    add_card = SubmitField('+')
    review = SubmitField('Review this Deck') # sends request.form['deckname'] to inform load the proper review page.
