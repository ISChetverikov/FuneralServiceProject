from . import routes
from flask import render_template

@routes.errorhandler(500)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('500.html', e=e), 500
