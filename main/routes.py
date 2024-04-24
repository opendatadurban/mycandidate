from flask import request, render_template, redirect, url_for, session, flash
from .database.models import *
from .app import app
from sqlalchemy import asc
from .decorators import requires_auth, get_candidates

@app.route('/', methods=['GET', 'POST'])
def home():
    candidates = None
    candidate = None
    presidential_candidates = []
    form_id = None
    form_url = "/"
    data = get_data()
    candidate_type = data[0]['candidate_type']
    config_queryset = db.session.query(Config).first()
    config = config_queryset.json()
    if request.method == 'POST' and request.form['ds_id'] is not None:
        form_id = request.form['ds_id']
        candidate_types = form_id.split(" - ")
        candidate_type = request.form['candidate_type']
        candidates, code = get_candidates(candidate_types, db, candidate_type)
        # print("final result", candidates[0:2])
        candidate_query = f"""
            SELECT * FROM candidates
            WHERE party = :form_id
            AND candidate_type = :candidate_type
            AND list_type = :location
            LIMIT 1
        """
        params = {'form_id': candidate_types[1], "candidate_type": candidate_type, "location": candidate_types[0]}
        candidate_result = db.session.execute(candidate_query, params)
        candidate = candidate_result.fetchone()
        # print(candidate)
        
    return render_template(
            'home.html', 
            candidates=candidates,
            presidential_candidates = presidential_candidates,
            candidate = candidate,
            ward=form_id, 
            form_url=form_url,
            data = data,
            config=config,
            area_name = candidate_type,
            domain = request.url_root
        )
