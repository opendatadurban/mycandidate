from main.database.models import db
from main.app import app

# Initialize db
db.drop_all()
db.configure_mappers()
db.create_all()

# Seeds
from main.database.models.build_db import (
    seed_site_settings,
    seed_data_tables,
    seed_data_candidates
    # seed_political_party, 
    # seed_people, 
    # seed_constituency,
    # seed_province,
    # seed_ward,
    # seed_candidates
)
excel_file_path = f'{app.root_path}/data/MyCandidate Seed Doc.xlsx'
# seed_political_party(db, excel_file_path)
# seed_people(db, excel_file_path)
# seed_constituency(db, excel_file_path)
# seed_province(db, excel_file_path)
# seed_ward(db, excel_file_path)
# seed_candidates(db, excel_file_path)
seed_site_settings(db, excel_file_path)
seed_data_tables(db, excel_file_path)
seed_data_candidates(db, excel_file_path)
