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


def get_candidates(form_id, db):
    retrieve_query = f"SELECT * FROM candidates WHERE county_code = :form_id"
    params = {'form_id': form_id}
    result = db.session.execute(retrieve_query, params) 
    column_names = result.keys()
    rows_as_dicts = []
    for row in result:
        row_dict = dict(zip(column_names, row))
        rows_as_dicts.append(row_dict)

    return rows_as_dicts