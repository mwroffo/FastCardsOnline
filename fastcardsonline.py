from app import app, db, migrate, decksmodel, session
from app.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'migrate': migrate, 'decksmodel': decksmodel, 'session': session}