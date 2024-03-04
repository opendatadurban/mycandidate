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


def get_candidates(form_id, db, area_name):
    distinct_types_query = """
        SELECT DISTINCT candidate_type, locator FROM candidates
    """
    distinct_types_result = db.session.execute(distinct_types_query)

    rows_as_dicts = []
    for row in distinct_types_result:
        if row[0] == area_name:
            most_common_values = row[1].strip("{}").split(',')
            code = most_common_values[0]
            name = most_common_values[1]
            retrieve_query = f"""SELECT * FROM candidates 
                    WHERE {code} = :form_id 
                    AND candidate_type = :area_name
                """ 
            params = {'form_id': form_id, "area_name": area_name}
            result = db.session.execute(retrieve_query, params) 
            column_names = result.keys()
            for row in result:
                row_dict = dict(zip(column_names, row))
                rows_as_dicts.append(row_dict)

    return rows_as_dicts, code