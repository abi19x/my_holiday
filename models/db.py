import psycopg
from flask import g
from config import Config

from werkzeug.security import generate_password_hash, check_password_hash
"""
conn = None

def init_db(app):
    global conn
    conn = psycopg.connect(Config.DATABASE_URL)

    @app.teardown_appcontext
    def close_connection(exception):
        if conn:
            conn.close()


def get_db():
    global conn
    return conn
    """
def init_db(app):
    conn = psycopg.connect(app.config["DATABASE_URL"])
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_email(email, db_url):
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
            return cur.fetchone()