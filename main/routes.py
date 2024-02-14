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
    ward_candidates = None
    config = None
    final_candidates = None
    candidates_final = None
    candidate_form = CandidateForm()
    ward_form = WardForm()
    form_url = "/"
    area_name = "candidates"
    if request.method == 'POST' and candidate_form.ds_id.data:
        candidates_final = candidate_form.data
        candidates = db.session.query(Candidate).filter(Candidate.candidate_type == candidate_form.ds_id.data).all()
        final_candidates = [c.to_dict() for c in candidates]
        area_name = "candidate_type"
        # print(">>>>>>", [c.to_dict() for c in candidates])
    elif request.method == 'POST' and ward_form.ds_id.data:
        ward_candidates = ward_form.ds_id.data
        candidates = db.session.query(Candidate).filter(Candidate.ward_id == ward_form.ds_id.data).all()
        final_candidates = [c.to_dict() for c in candidates]
        # print(">>>>>>", [c.to_dict() for c in candidates])
        area_name = "ward"
    elif request.method == 'GET':
        candidates = db.session.query(Candidate).all()
        final_candidates = [c.to_dict() for c in candidates]
        config_queryset = db.session.query(Config).first()
        config = config_queryset.json()
    
    return render_template(
            'index.html', 
            final_candidates=final_candidates, 
            candidates_final=candidates_final,
            config=config,
            ward_candidates=ward_candidates,  
            candidate_form=candidate_form, 
            form_url=form_url,
            ward_form=ward_form, 
            area_name=area_name
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