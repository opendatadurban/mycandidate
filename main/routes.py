from flask import request, render_template
from .models import *
from .app import app
from sqlalchemy import asc

@app.route('/', methods=['GET', 'POST'])
def home():
    form = CandidateForm()
    form_ward = WardCandidateForm()
    candidates = False
    ward_candidates = False
    constituency = False
    constituency_ward = False
    area_name = "Ward"
    form_url = "/"
    domain = app.config['SITE_URL']
    if request.method == 'POST' and form_ward.ds_id.data and form_ward.validate():
        constituency_ward = form.ds_id.data
        ward_candidates = db.session.query(WardCandidate).filter(WardCandidate.local_authority == form.ds_id.data)\
            .order_by(asc(WardCandidate.ward_no)).all()
        area_name = "Ward"
    elif request.method == 'POST' and form.ds_id.data and form.validate():
        constituency = form.ds_id.data
        candidates = db.session.query(Candidate).filter(Candidate.constituency == form.ds_id.data).all()
        area_name = "Constituency"
    return render_template('index.html', form=form, form_ward=form_ward, candidates=candidates, ward_candidates=ward_candidates, area_name=area_name,
                           constituency=constituency, constituency_ward=constituency_ward, 
                           domain=domain,form_url=form_url)

@app.route('/local-authority', methods=['GET', 'POST'])
def local_authority():
    form_url="/local-authority"
    form = WardCandidateForm()
    area_name = "Ward"
    candidates = False
    constituency = False
    domain = app.config['SITE_URL']
    if request.method == 'POST' and form.validate():
        constituency = form.ds_id.data
        candidates = db.session.query(WardCandidate).filter(WardCandidate.local_authority == form.ds_id.data)\
            .order_by(asc(WardCandidate.ward_no)).all()
    return render_template('ward_layout.html', form=form,candidates=candidates,area_name=area_name,
                           constituency=constituency,domain=domain,form_url=form_url)