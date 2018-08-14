from flask import render_template, flash, redirect, url_for,\
    request, Request, current_app, g
from app import decksmodel # TODO decksmodel like app needs to be abstracted into a callable context
                                # LOL hows THAT for some jargon? 
from app.forms import LoginForm, BrowseEditForm, DeckForm, CardForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, FormField, FieldList, HiddenField
from wtforms.validators import DataRequired

@current_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if fields are empty, DataRequired argument in LoginField will make this false,
    # forcing the form to simply reload, until it is completed correctly. bomb.com.
    if form.validate_on_submit():  # false when serving the form, true when submitting the form
        print('\n', 'LOGIN FORM SAYS: ', request.form, '\n')
        flash('Login request: username={}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In to FastCards', form=form, user={'username': 'mwroffo'})

@current_app.route('/')  # these @ things are called decorators in python.
@current_app.route('/index')
def index():
    decks_form = {} # Not actually a Form object. Do not be confused.
    class _DeckForm(DeckForm):
            pass
    for deckmodel in decksmodel.getDecks().values():
        # Field edits must be made on the class to avoid UnboundField error.
        setattr(_DeckForm, 'browse_edit', SubmitField('Browse/Edit'))
        # deckname as StringField so that it can be submitted:
        setattr(_DeckForm, 'deckname_field', HiddenField(label='deckname', default=deckmodel.getTablename()))
        new_deckform = _DeckForm()
        # deckname as str attribute so that it can be printed to the view:
        setattr(new_deckform, 'deckname', deckmodel.getTablename())
        decks_form[deckmodel.getTablename()] = new_deckform
    
    setattr(_DeckForm, 'browse_edit', SubmitField('Create a New Empty Deck'))
    setattr(_DeckForm, 'deckname_field', HiddenField(label='deckname', default=''))
    empty_deckform = _DeckForm()
    return render_template(
        'index.html',
        title='Home',
        user={'username': 'mwroffo'},
        decks_form=decks_form, # submit dict of deckforms
        empty_deckform=empty_deckform) # requests from an empty deckform will indicate a new deck

@current_app.route('/browse_edit', methods=['GET', 'POST'])
def browse_edit():
    """
    Renders a browse/edit view of a certain deck.
    TODO does this also handle adding to the deck, or just rendering it?
    """
    # if user is creating a new empty deck, render only the deckname field with newtermfield and newdeffield
    # if user is editing a preexisting deck, render the deckname field, all cards as term, definition, a term/def row for new entries, a "return to decks" button, and a "review this deck" button
    
    if request.method == 'POST':
        class _BrowseEditForm(BrowseEditForm):
            pass

        # set decktitle field to the deck's name:
        deckname = request.form['deckname_field']
        deckmodel = decksmodel.getDecks()[deckname]
        _BrowseEditForm.deckname.default = deckname
        browse_edit_form = _BrowseEditForm()
        class _CardForm(CardForm):
            pass
        
        print('deckmodel.getCards() is ', deckmodel.getCards())
        for card in deckmodel.getCards():
            _CardForm.term = StringField(default=card.term, label='Term', validators=[DataRequired()])
            _CardForm.definition = StringField(default=card.definition, label='Definition', validators=[DataRequired()])
            browse_edit_form.cards.append_entry(_CardForm())
        # for empty decks, `cards` will not render.
    if browse_edit_form.validate_on_submit:
        return render_template('browse_edit.html', title='Enter a card',  \
            user={'username': 'mwroffo'}, form=browse_edit_form)
    return redirect(url_for('browse_edit.html'))

@Request.application
def respond_deck(request, deckname):
    """ Handles a request to render an already existing deck in browse/edit view """


@Request.application
def respond_empty_deck(request):
    """ Handles a request to render an empty browse/edit page """

@current_app.route('/review', methods=['GET', 'POST'])
def review():
    form = BrowseEditForm(decks) # TODO 2018-08-05 change from placeholder to ReviewForm()
    return render_template('review.html', title='Reviewing deck', form=form, user={'username': 'mwroffo'})
