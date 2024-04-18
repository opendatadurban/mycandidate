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
    print(data)
    area_name = data[0]['candidate_type']
    config_queryset = db.session.query(Config).first()
    config = config_queryset.json()
    print(config)
    if request.method == 'POST' and request.form['ds_id'] is not None:
        form_id = request.form['ds_id']  
        print(form_id)
        area_name = request.form['candidate_type']
        candidates, code = get_candidates(form_id, db, area_name)
        # print("final result", candidates[0:2])
        # print(form_id, area_name)
        candidate_query = f"""
            SELECT * FROM candidates
            WHERE {code} = :form_id
            AND candidate_type = :area_name
            LIMIT 1
        """
        params = {'form_id': form_id, "area_name": area_name}
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
            area_name = area_name,
            domain = request.url_root
        )