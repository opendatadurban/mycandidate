import json, os, pandas as pd
from .decorators import get_candidates
from .app import app

# Try to import valkey, fallback to redis for production compatibility
try:
    import valkey
    valkey_available = True
except ImportError:
    import redis as valkey
    valkey_available = False

valkey_url = app.config['VALKEY_URL']
if valkey_available:
    valkey_client = valkey.StrictValkey.from_url(valkey_url)
else:
    # Fallback to Redis client
    valkey_client = valkey.StrictRedis.from_url(valkey_url)
# valkey_client.delete('cached_candidates')

def sort_data(candidates):
    presidential_candidates = []
    party_members = []
    # Sort alphabetically
    df = pd.DataFrame(candidates)
    sorted_df = df.sort_values(by='party')
    candidates = sorted_df.to_dict(orient='records')

    for item in candidates:
        if item['orderno'] == '1':
            presidential_candidates.append(item)
        else:
            party_members.append(item)

    return presidential_candidates, party_members


def get_cached_data_or_fetch(form_id, db, candidate_type):
    cached_data = valkey_client.get('cached_candidates')
    if cached_data:
        data = json.loads(cached_data)
        return data["candidates"]["presidential"], data["candidates"]["party_members"], data["code"]
    else:
        candidates, code = get_candidates(form_id, db, candidate_type)
        presidential_candidates, party_members = sort_data(candidates)
        # Cache the fetched data for future requests
        data_to_cache = {
            'candidates': {
                'presidential': presidential_candidates, 
                'party_members': party_members
                }, 
            'code': code
        }
        valkey_client.set('cached_candidates', json.dumps(data_to_cache))
        valkey_client.expire('cached_candidates', 86400)  # Cache for 24 hours
        return presidential_candidates, party_members, code