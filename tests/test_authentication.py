import pytest
from flask import url_for
from urllib.parse import urlparse
from app import app, db

def test_login(client):
    response = client.post('/login', data={'secret_key': 'your_secret_key'})
    assert response.status_code == 302
    with app.test_request_context():
        # Use urlparse to extract the path from the URL
        location_path = urlparse(response.location).path
        expected_path = url_for('dashboard')
    assert location_path == expected_path

def test_dashboard_authenticated(client):
    # Log in before accessing the dashboard
    client.post('/login', data={'secret_key': 'your_secret_key'})
    
    response = client.get('/dashboard')
    assert response.status_code == 200

def test_dashboard_unauthenticated(client):
    response = client.get('/dashboard')
    assert response.status_code == 302
    with app.test_request_context():
        # Use urlparse to extract the path from the URL
        location_path = urlparse(response.location).path
        expected_path = url_for('login')
    assert location_path == expected_path

def test_logout(client):
    # Log in before logging out
    client.post('/login', data={'secret_key': 'your_secret_key'})

    response = client.get('/logout')
    assert response.status_code == 302
    with app.test_request_context():
        # Use urlparse to extract the path from the URL
        location_path = urlparse(response.location).path
        expected_path = url_for('login')
    assert location_path == expected_path