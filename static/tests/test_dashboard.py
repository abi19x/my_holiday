import pytest
from app import app as flask_app
from models.db import init_db
import os

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['DATABASE_URL'] = os.getenv("DATABASE_URL", "sqlite:///:memory:")

    with flask_app.test_client() as client:
        with flask_app.app_context():
            init_db(flask_app)  # Ensure tables are created
        yield client

def test_dashboard_requires_login(client):
    # Try accessing dashboard without login
    res = client.get('/dashboard/', follow_redirects=True)
    assert res.status_code == 200
    assert b'Login' in res.data  # Redirected to login page

def test_dashboard_access_for_logged_user(client):
    # Register a user
    client.post('/register', data={
        'name': 'Eve',
        'email': 'eve@example.com',
        'password': 'evepass'
    }, follow_redirects=True)

    # Log in as that user
    client.post('/login', data={
        'email': 'eve@example.com',
        'password': 'evepass'
    }, follow_redirects=True)

    # Access dashboard
    res = client.get('/dashboard/')
    assert res.status_code == 200
    assert b'Your Bookings' in res.data
