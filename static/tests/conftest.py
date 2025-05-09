import pytest
from app import create_app
from models.db import init_db, get_db
import psycopg
import os

TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL', 'postgresql://your_db_user:your_db_password@localhost/holiday_planner_test')

@pytest.fixture(scope='session')
def app():
    os.environ['DATABASE_URL'] = TEST_DATABASE_URL
    app = create_app()
    app.config['TESTING'] = True

    # Init test DB schema
    conn = psycopg.connect(TEST_DATABASE_URL)
    with conn.cursor() as cur:
        with open('scripts/init_db.sql') as f:
            cur.execute(f.read())
        conn.commit()
        conn.close()

    yield app

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()
