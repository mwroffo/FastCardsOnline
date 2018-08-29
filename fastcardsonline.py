from app import create_app, db, migrate, bootstrap
from app.models import User, Card, Deck

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Card':Card, 'Deck':Deck, 'migrate':migrate, 'bootstrap':bootstrap}