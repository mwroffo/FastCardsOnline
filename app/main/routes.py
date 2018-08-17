from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required
from app.models import User
from app.main import bp
from app import decksmodel # TODO decksmodel like app needs to be abstracted into a callable context
from app.forms import LoginForm, BrowseEditForm, DeckForm, CardForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, FormField, FieldList, HiddenField
from wtforms.validators import DataRequired

@bp.route('/')  # these @ things are called decorators in python.
@bp.route('/index')
@login_required
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
        decks_form=decks_form, # submit dict of deckforms
        empty_deckform=empty_deckform) # requests from an empty deckform will indicate a new deck

@bp.route('/browse_edit', methods=['GET', 'POST'])
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

@bp.route('/review', methods=['GET', 'POST'])
def review():
    form = BrowseEditForm(decks) # TODO 2018-08-05 change from placeholder to ReviewForm()
    return render_template('review.html', title='Reviewing deck', form=form, user={'username': 'mwroffo'})
