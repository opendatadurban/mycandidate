from flask import request, render_template, redirect, url_for, session, flash
import pandas as pd
from .database.models import *
from .app import app
from sqlalchemy import asc
from .decorators import requires_auth, get_candidates

@app.route('/', methods=['GET', 'POST'])
def home():
    candidates = None
    candidate = None
    presidential_candidates = []
    party_members = []
    form_id = None
    form_url = "/"
    config_queryset = db.session.query(Config).first()
    config = config_queryset.json()
    data = get_data()
    candidate_type = data[0]['candidate_type']
    if candidate_type == 'national' and request.method == 'GET':
        form_id = 'National'
        candidates, code = get_candidates(form_id, db, candidate_type)
        # Sort alphabetically
        df = pd.DataFrame(candidates)
        sorted_df = df.sort_values(by='party')
        candidates = sorted_df.to_dict(orient='records')

        for item in candidates:
            if item['orderno'] == '1':
                presidential_candidates.append(item)
            else:
                party_members.append(item)
        print("final pres result", presidential_candidates[0:2])
        print("final can result", party_members[0:2])

        candidate_query = f"""
            SELECT * FROM candidates
            WHERE {code} = :form_id
            AND candidate_type = :candidate_type
            LIMIT 1
        """
        params = {'form_id': form_id, "candidate_type": candidate_type}
        candidate_result = db.session.execute(candidate_query, params)
        candidate = candidate_result.fetchone()

    if request.method == 'POST' and request.form['ds_id'] is not None:
        form_id = request.form['ds_id']
        candidate_type = request.form['candidate_type']
        candidates, code = get_candidates(form_id, db, candidate_type)
        # Sort alphabetically
        df = pd.DataFrame(candidates)
        sorted_df = df.sort_values(by=['party', 'orderno'])
        candidates = sorted_df.to_dict(orient='records')

        for item in candidates:
            if item['orderno'] == '1':
                presidential_candidates.append(item)
            else:
                party_members.append(item)
        print("final pres result", presidential_candidates[0:2])
        print("final can result", party_members[0:2])

        candidate_query = f"""
            SELECT * FROM candidates
            WHERE {code} = :form_id
            AND candidate_type = :candidate_type
            LIMIT 1
        """
        params = {'form_id': form_id, "candidate_type": candidate_type}
        candidate_result = db.session.execute(candidate_query, params)
        candidate = candidate_result.fetchone()
        print(candidate)
        
    return render_template(
            'home.html', 
            candidates=candidates,
            presidential_candidates=presidential_candidates,
            candidate = candidate,
            ward=form_id, 
            form_url=form_url,
            data = data,
            config=config,
            area_name = candidate_type,
            domain = request.url_root

        )
