from app.DecksModel import DecksModel
from flask import render_template, flash, redirect, url_for, request
from app import app, db, decksmodel
from app.forms import LoginForm, BrowseEditForm, DeckForm, CardForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField, FormField, FieldList
from wtforms.validators import DataRequired

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if fields are empty, DataRequired argument in LoginField will make this false,
    # forcing the form to simply reload, until it is completed correctly. bomb.com.
    if form.validate_on_submit():  # false when serving the form, true when submitting the form
        flash('Login request: username={}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index.html'))
    return render_template('login.html', title='Sign In to FastCards', form=form, user={'username': 'mwroffo'})

@app.route('/')  # these @ things are called decorators in python.
@app.route('/index')
def index():
    decks_form = {} # Not actually a Form object. Do not be confused.
    class _DeckForm(DeckForm):
        """ inherits the review and submit buttons from DeckForm """
        pass
    for deckmodel in decksmodel.getDecks().values():
        # Field edits must be made on the class to avoid UnboundField error.
        setattr(_DeckForm, 'browse_edit', SubmitField('Browse/Edit'))
        new_deckform = _DeckForm() # but simple string attributes can be edited on instances:
        setattr(new_deckform, 'deckname', deckmodel.getTablename())
        decks_form[deckmodel.getTablename()] = new_deckform
    setattr(_DeckForm, 'browse_edit', SubmitField('Create a New Empty Deck'))
    empty_deckform = _DeckForm()
    setattr(empty_deckform, 'deckname', '')
    return render_template(
        'index.html',
        title='Home',
        user={'username': 'mwroffo'},
        decks_form=decks_form, # submit dict of deckforms
        empty_deckform=empty_deckform) # requests from an empty deckform will indicate a new deck

@app.route('/browse_edit', methods=['GET', 'POST'])
def browse_edit():
    # if user is creating a new empty deck, render only the deckname field with newtermfield and newdeffield
    # if user is editing a preexisting deck, render the deckname field, <all cards as term, definition, 
    # if request.form['deckname'] == '':
        # pass
    form = BrowseEditForm(DECK) # TODO pass a DeckModel object as parameter. index form should submit a deckname. pass as parameter that deckname's corresponding DeckModel.
    if form.validate_on_submit():
        flash('Card saved: term={}, definition={}'.format(
            form.term.data, form.definition.data))
        return redirect(url_for('browse_edit.html'))
    return render_template('browse_edit.html', title='Enter a card',  \
        user={'username': 'mwroffo'}, form=form)

@app.route('/review', methods=['GET', 'POST'])
def review():
    form = BrowseEditForm(decks) # TODO 2018-08-05 change from placeholder to ReviewForm()
    return render_template('review.html', title='Reviewing deck', form=form, user={'username': 'mwroffo'})
