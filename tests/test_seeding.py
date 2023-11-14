import pytest
from app import app, db
from main.database.models import Candidate, Config
from main.database.models.build_db import seed_temp_indicators, seed_site_settings

def test_seed_candidates_from_excel(client):
    # Create this file with sample data
    excel_file_path = 'tests/sample_data.xlsx'  

    with app.app_context():
        # Call the seeding function
        seed_temp_indicators(db, excel_file_path)

        # Perform assertions
        num_candidates = db.session.query(Candidate).count()

        expected_num_candidates = 38
        assert num_candidates == expected_num_candidates


def test_seed_config_from_excel(client):
    excel_file_path = 'tests/sample_data.xlsx'  

    seed_site_settings(db, excel_file_path)

    num_config = db.session.query(Config).count()
    assert num_config == 0
