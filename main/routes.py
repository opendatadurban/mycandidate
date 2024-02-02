from flask import request, render_template, redirect, url_for, session, flash
from .database.models import *
from .app import app
from sqlalchemy import asc
from .decorators import requires_auth

# Predefined secret key for authentication
predefined_secret_key = app.config['CLIENT_SECRET_KEY']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_secret_key = request.form['secret_key']

        # Check if the entered secret key matches the predefined secret key
        if entered_secret_key == predefined_secret_key:
            session['authenticated'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your secret key.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Clear the authentication flag from the session
    session.pop('authenticated', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html')

    

# TODO: route to get candidates
@app.route('/', methods=['GET', 'POST'])
def index():
    candidates = None
    ward = None
    final_candidates = None
    form = CandidateForm()
    form_url = "/"
    if request.method == 'GET':
        print("=====================")
        candidates = db.session.query(Candidate).all()
        final_candidates = [c.to_dict() for c in candidates]
        print(final_candidates)
    elif request.method == 'POST':
        ward = form.ds_id.data
        final_candidates = db.session.query(Candidate).filter(Candidate.ward_id == form.ds_id.data).all()
        print(">>>>>>", [c.to_dict() for c in final_candidates])
    
    return render_template(
            'index.html', 
            candidates=final_candidates, 
            ward= ward,  
            form=form, 
            form_url=form_url
        )


# @app.route('/', methods=['GET', 'POST'])
# def home():
#     form = CandidateForm()
#     form_ward = WardCandidateForm()
#     candidates = False
#     ward_candidates = False
#     constituency = False
#     constituency_ward = False
#     area_name = "Ward"
#     form_url = "/"
#     domain = app.config['SITE_URL']
#     if request.method == 'POST' and form_ward.ds_id.data and form_ward.validate():
#         constituency_ward = form.ds_id.data
#         ward_candidates = db.session.query(WardCandidate).filter(WardCandidate.local_authority == form.ds_id.data)\
#             .order_by(asc(WardCandidate.ward_no)).all()
#         area_name = "Ward"
#     elif request.method == 'POST' and form.ds_id.data and form.validate():
#         constituency = form.ds_id.data
#         candidates = db.session.query(Candidate).filter(Candidate.constituency == form.ds_id.data).all()
#         area_name = "Constituency"
#     return render_template('index.html', form=form, form_ward=form_ward, candidates=candidates, ward_candidates=ward_candidates, area_name=area_name,
#                            constituency=constituency, constituency_ward=constituency_ward, 
#                            domain=domain,form_url=form_url)

# @app.route('/local-authority', methods=['GET', 'POST'])
# def local_authority():
#     form_url="/local-authority"
#     form = WardCandidateForm()
#     area_name = "Ward"
#     candidates = False
#     constituency = False
#     domain = app.config['SITE_URL']
#     if request.method == 'POST' and form.validate():
#         constituency = form.ds_id.data
#         candidates = db.session.query(WardCandidate).filter(WardCandidate.local_authority == form.ds_id.data)\
#             .order_by(asc(WardCandidate.ward_no)).all()
#     return render_template('ward_layout.html', form=form,candidates=candidates,area_name=area_name,
#                            constituency=constituency,domain=domain,form_url=form_url)