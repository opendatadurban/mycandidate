from flask import session, redirect, flash, url_for
from functools import wraps

def requires_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if 'authenticated' in session and session['authenticated']:
            return func(*args, **kwargs)
        else:
            flash('You need to log in first.', 'error')
            return redirect(url_for('login'))
    return decorated