import pytest
from app import app as flask_app
from models.db import init_db
from werkzeug.security import generate_password_hash
import psycopg
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

def test_admin_login_and_access(client):
    # Create admin user manually
    hashed_pw = generate_password_hash("adminpass")
    db_url = flask_app.config['DATABASE_URL']
    
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s);
            """, ("admin", "admin@example.com", hashed_pw, "admin"))
            conn.commit()

    # Login as admin
    client.post('/login', data={
        'email': 'admin@example.com',
        'password': 'adminpass'
    }, follow_redirects=True)

    # Access admin page
    res = client.get('/admin', follow_redirects=True)
    assert b'Admin Dashboard' in res.data or b'All Bookings' in res.data

def test_non_admin_access_denied(client):
    client.post('/register', data={
        'name': 'RegularUser',
        'email': 'user@example.com',
        'password': 'userpass'
    })

    client.post('/login', data={
        'email': 'user@example.com',
        'password': 'userpass'
    })

    res = client.get('/admin', follow_redirects=True)
    assert b'Access denied' in res.data or res.status_code == 403
