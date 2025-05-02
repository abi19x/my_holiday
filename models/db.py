import psycopg
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash


def init_db(app):
    conn = psycopg.connect(app.config["DATABASE_URL"])
    cur = conn.cursor()

    # Create users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    # Create bookings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            type TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            duration INTEGER NOT NULL,
            status TEXT NOT NULL,
            notes TEXT
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
