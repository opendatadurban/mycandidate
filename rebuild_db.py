from main.database.models import db
from main.app import app

# Initialize db
db.drop_all()
db.configure_mappers()
db.create_all()

# Seeds
from main.database.models.build_db import seed_temp_indicators, seed_site_settings
excel_file_path = f'{app.root_path}/data/MyCandidate Seed Doc.xlsx'
seed_temp_indicators(db, excel_file_path)
seed_site_settings(db, excel_file_path)
# seed_candidates_prov(db)
