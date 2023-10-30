import pytest
from app import app, db
from main.models import Candidate, Config
from main.models.build_db import seed_temp_indicators, seed_site_settings  

@pytest.fixture
def client():
    app.config['TESTING'] = True
     # Use an in-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    client = app.test_client()
    db.create_all()
    yield client
    db.session.remove()
    db.drop_all()

def test_seed_candidates_from_excel(client):
    # Create this file with sample data
    excel_file_path = 'tests/sample_data.xlsx'  

    # Call the seeding function
    seed_temp_indicators(db, excel_file_path)

    # Perform assertions
    num_candidates = Candidate.query.count()
    # print(">>>>>>>>", num_candidates)
    expected_num_candidates = 18 
    assert num_candidates == expected_num_candidates


def test_seed_config_from_excel(client):
    excel_file_path = 'tests/sample_data.xlsx'  

    seed_site_settings(db, excel_file_path)

    num_config = Config.query.count()
    assert num_config == 0
