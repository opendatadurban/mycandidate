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
    distinct_names = db.session.query(Candidate).with_entities(Candidate.candidate_type).distinct().all()
    tabs = [c[0] for c in distinct_names]
    print(">>>>>>", tabs)
    if request.method == 'GET':
        print("=====================")
        candidates = db.session.query(Candidate).all()
        final_candidates = [c.to_dict() for c in candidates]
        #print(final_candidates)
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


@app.route('/home', methods=['GET', 'POST'])
def home():
    candidates = None
    presidential_candidates = []
    ward = None
    form_url = "/"
    data = get_data()
    area_name = data[0]['candidate_type']
    if request.method == 'GET':
        print("=====================")
        #candidates = db.session.query(Candidate).all()
        #final_candidates = [c.to_dict() for c in candidates]
        #print(final_candidates)
    elif request.method == 'POST':
        #ward = request.form.ds_id.data
        ward = request.form['ds_id']  
        candidates = db.session.query(Candidate).filter(Candidate.ward_id == ward).all()
        candidate = db.session.query(Candidate).filter(Candidate.ward_id == ward).first()
        area_name =candidate.candidate_type
        print(">>>>>>", [c.to_dict() for c in candidates])
        print(">>>>>> request.form", request.form)
    
    return render_template(
            'home.html', 
            candidates=candidates,
            presidential_candidates = presidential_candidates,
            ward= ward, 
            form_url=form_url,
            data = data,
            area_name = area_name
        )


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