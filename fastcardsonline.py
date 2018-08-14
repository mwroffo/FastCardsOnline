from app.models import User, Card
from flask import current_app, g
from app.db import db

@current_app.shell_context_processor
def make_shell_context():
    session = db.get_db()
    db.init_migrate()
    return {'db': session, 'User': User, 'migrate': g.migrate,
        'decksmodel': decksmodel}