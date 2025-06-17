import sqlite3
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash


def init_db(app):
    import sqlite3

    db_url = app.config["DATABASE_URL"]
    db_path = db_url.split("///")[-1]  # Get path for SQLite

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create users table
    cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0
);
""")

    conn.commit()
    cur.close()
    conn.close()

def create_user(email, password, is_admin, db_url):
    from werkzeug.security import generate_password_hash
    db_path = db_url.split("///")[-1]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    hashed_password = generate_password_hash(password)
    
    cur.execute("""
        INSERT INTO users (email, password, is_admin)
        VALUES (?, ?, ?)
    """, (email, hashed_password, is_admin))
    
    conn.commit()
    conn.close()


def get_user_by_email(email, db_url):
    conn = sqlite3.connect(db_url.split("///")[-1])
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    return user

def update_booking_status(booking_id, new_status, db_url):
    conn = sqlite3.connect(db_url.split("///")[-1])
    cur = conn.cursor()
    cur.execute(
        "UPDATE bookings SET status = ? WHERE id = ?;",
        (new_status, booking_id)
    )
    conn.commit()
    conn.close()

def delete_booking_by_id(booking_id, db_url):
    conn = sqlite3.connect(db_url.split("///")[-1])
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM bookings WHERE id = ?;",
        (booking_id,)
    )
    conn.commit()
    conn.close()