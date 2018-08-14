from flask import render_template
from app.db import get_db
from app.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('../templates/errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    with get_db() as session:
        session.rollback() # mitigate partial db writes.
    return render_template('../templates/errors/500.html'), 500
