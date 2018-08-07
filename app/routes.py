from app.DecksModel import DecksModel
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, EntryForm

@app.route('/')  # these @ things are called decorators in python.
@app.route('/index')
def index():
    user = {'username': 'mwroffo'}
    # render_template takes as args: the template file, and any objects
    # that are necessary for dynamic content
    # TODO this should prob be done with url_for()
    mwroffo = DecksModel('/Users/_mexus/Documents/code/fastcardsonline/mwroffo')
    decks = mwroffo.getDecks()
    return render_template(
        'index.html',
        title='Home',
        user=user,
        decks=decks.keys())


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

@app.route('/browse_edit', methods=['GET', 'POST'])
def browse_edit():
    form = EntryForm()
    if form.validate_on_submit():
        flash('Card saved: term={}, definition={}'.format(
            form.term.data, form.definition.data))
        return redirect(url_for('browse_edit.html'))
    return render_template('browse_edit.html', title='Enter a card',  user={'username': 'mwroffo'}, form=form)

@app.route('/review', methods=['GET', 'POST'])
def review():
    form = EntryForm() # TODO 2018-08-05 change from placeholder to ReviewForm()
    return render_template('review.html', title='Reviewing deck', form=form, user={'username': 'mwroffo'})
