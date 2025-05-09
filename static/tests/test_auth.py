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
            init_db(flask_app)
        yield client

def test_user_registration(client):
    res = client.post('/register', data={
        'name': 'Alice',
        'email': 'alice@example.com',
        'password': 'alicepass'
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b'Login' in res.data  # Redirected after successful registration

def test_user_login_success(client):
    client.post('/register', data={
        'name': 'Bob',
        'email': 'bob@example.com',
        'password': 'bobpass'
    })

    res = client.post('/login', data={
        'email': 'bob@example.com',
        'password': 'bobpass'
    }, follow_redirects=True)

    assert b'Welcome' in res.data or b'Dashboard' in res.data

def test_user_login_failure(client):
    res = client.post('/login', data={
        'email': 'nonexistent@example.com',
        'password': 'wrongpass'
    }, follow_redirects=True)

    assert b'Invalid email or password' in res.data
