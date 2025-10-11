from flask import request, render_template, redirect, url_for, session, flash
import pandas as pd
from .database.models import *
from .app import app
from sqlalchemy import asc
from .decorators import requires_auth, get_candidates
from .redis import get_cached_data_or_fetch, valkey_client
from flask_minify import decorators as minify_decorators



@app.route('/', methods=['GET', 'POST'])
@minify_decorators.minify(html=True, js=True, cssless=True)
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
        presidential_candidates, party_members, code = get_cached_data_or_fetch(form_id, db, candidate_type)

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

        party_orderno_count = {}
        for item in candidates:
            party = item['party']
            orderno = item['orderno']
            
            if orderno == '1':
                # Check if this is the first candidate with orderno = '1' for this party
                if party not in party_orderno_count:
                    party_orderno_count[party] = 1
                    presidential_candidates.append(item)
                else:
                    party_orderno_count[party] += 1
                    if party_orderno_count[party] == 2:
                        party_members.append(item)
                    else:
                        presidential_candidates.append(item)
            else:
                party_members.append(item)
        candidate_query = f"""
            SELECT * FROM candidates
            WHERE {code} = :form_id
            AND candidate_type = :candidate_type
            LIMIT 1
        """
        params = {'form_id': form_id, "candidate_type": candidate_type}
        candidate_result = db.session.execute(candidate_query, params)
        candidate = candidate_result.fetchone()
    
    party_members = sorted(party_members, key=lambda x: int(x['orderno']))
        
    return render_template(
            'home.html', 
            candidates=party_members,
            presidential_candidates=presidential_candidates,
            candidate = candidate,
            ward=form_id, 
            form_url=form_url,
            data = data,
            config=config,
            area_name = candidate_type,
            domain = request.url_root
        )

@app.route('/insights', methods=['GET', 'POST'])
def insights():
    config_queryset = db.session.query(Config).first()
    config = config_queryset.json()
    return render_template(
            'insights.html',
            config=config,
            domain = request.url_root)

@app.route('/valkey-viewer', methods=['GET', 'POST'])
def valkey_viewer():
    config_queryset = db.session.query(Config).first()
    config = config_queryset.json()
    
    keys_data = []
    search_pattern = "*"
    error_message = None
    
    try:
        if request.method == 'POST':
            search_pattern = request.form.get('search_pattern', '*')
            if not search_pattern:
                search_pattern = "*"
        
        # Get all keys matching the pattern
        keys = valkey_client.keys(search_pattern)
        
        for key in keys:
            try:
                # Get key type
                key_type = valkey_client.type(key).decode('utf-8')
                
                # Get TTL
                ttl = valkey_client.ttl(key)
                
                # Get value based on type
                if key_type == 'string':
                    value = valkey_client.get(key)
                    if value:
                        value = value.decode('utf-8')
                        # Try to format as JSON if possible
                        try:
                            import json
                            parsed_value = json.loads(value)
                            value = json.dumps(parsed_value, indent=2)
                        except:
                            pass
                elif key_type == 'list':
                    value = valkey_client.lrange(key, 0, -1)
                    value = [v.decode('utf-8') if isinstance(v, bytes) else v for v in value]
                elif key_type == 'set':
                    value = valkey_client.smembers(key)
                    value = [v.decode('utf-8') if isinstance(v, bytes) else v for v in value]
                elif key_type == 'hash':
                    value = valkey_client.hgetall(key)
                    value = {k.decode('utf-8') if isinstance(k, bytes) else k: 
                            v.decode('utf-8') if isinstance(v, bytes) else v 
                            for k, v in value.items()}
                else:
                    value = "Unsupported type"
                
                keys_data.append({
                    'key': key.decode('utf-8') if isinstance(key, bytes) else key,
                    'type': key_type,
                    'value': value,
                    'ttl': ttl if ttl > 0 else 'No expiration'
                })
            except Exception as e:
                keys_data.append({
                    'key': key.decode('utf-8') if isinstance(key, bytes) else key,
                    'type': 'error',
                    'value': f"Error reading key: {str(e)}",
                    'ttl': 'N/A'
                })
        
        # Sort keys alphabetically
        keys_data.sort(key=lambda x: x['key'])
        
    except Exception as e:
        error_message = f"Error connecting to Valkey: {str(e)}"
    
    return render_template(
        'valkey_viewer.html',
        keys_data=keys_data,
        search_pattern=search_pattern,
        error_message=error_message,
        config=config,
        domain=request.url_root
    )