from flask import request, render_template, redirect, url_for, session, flash
from .database.models import *
from .app import app
from sqlalchemy import asc
from .decorators import requires_auth, get_candidates

# Predefined secret key for authentication
# predefined_secret_key = app.config['CLIENT_SECRET_KEY']

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         entered_secret_key = request.form['secret_key']

#         # Check if the entered secret key matches the predefined secret key
#         if entered_secret_key == predefined_secret_key:
#             session['authenticated'] = True
#             flash('Login successful!', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Login failed. Check your secret key.', 'error')

#     return render_template('login.html')


# @app.route('/logout')
# def logout():
#     # Clear the authentication flag from the session
#     session.pop('authenticated', None)
#     flash('You have been logged out.', 'success')
#     return redirect(url_for('login'))


# @app.route('/dashboard')
# @requires_auth
# def dashboard():
#     return render_template('dashboard.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    candidates = None
    candidate = None
    presidential_candidates = []
    form_id = None
    form_url = "/"
    data = get_data()
    area_name = None
    config_queryset = db.session.query(Config).first()
    config = config_queryset.json()
    if request.method == 'GET' :
        area_name = data[0]['candidate_type']
        print(area_name)


    if request.method == 'POST' and request.form['ds_id'] is not None:
        form_id = request.form['ds_id']  
        candidates = get_candidates(form_id, db)
        area_name = next(i['candidate_type'] for i in data if candidates[0]['candidate_type'] in i['candidate_type'])
        print(candidates[0])
        # area_name = candidates[0]['candidate_type'] # Should be passed as param
        print(form_id, area_name)
        candidate_query = """
            SELECT * FROM candidates
            WHERE county_code = :form_id
            LIMIT 1
        """
        params = {'form_id': form_id}
        candidate_result = db.session.execute(candidate_query, params)
        candidate = candidate_result.fetchone()
        print(candidate)
        
    return render_template(
            'home.html', 
            candidates=candidates,
            presidential_candidates = presidential_candidates,
            candidate = candidate,
            ward=form_id, 
            form_url=form_url,
            data = data,
            config=config,
            area_name = area_name
        )

