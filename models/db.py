import sqlite3
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash


def init_db(app):
    import sqlite3

    db_url = app.config["DATABASE_URL"]
    print("DATABASE_URL (raw):", db_url)
    print("Type of DATABASE_URL:", type(db_url))

    db_path = db_url.split("///")[-1]  # This line will break if db_url is not a str

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

     # Create users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    );
    """)

    # Create bookings table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        start_date TEXT,
        end_date TEXT,
        duration TEXT,
        notes TEXT,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

def create_user(name, email, password, role, db_url):
    from werkzeug.security import generate_password_hash
    db_path = db_url.split("///")[-1]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Check if user already exists
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        print(f"User with email {email} already exists.")
        conn.close()
        return

    hashed_password = generate_password_hash(password)

    cur.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
    """, (name, email, hashed_password, role))

    conn.commit()
    conn.close()
    print(f"User {email} created.")


def get_user_by_email(email, db_url):
    import sqlite3
    db_path = db_url.split("///")[-1]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This makes rows behave like dicts
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    if user:
        return dict(user)  # convert sqlite3.Row to dict
    return None

def update_booking_status(booking_id, new_status, db_url):
    if not isinstance(db_url, str):
        raise ValueError("Invalid database URL provided to update_booking_status()")

    db_path = db_url.split("///")[-1]

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute(
            "UPDATE bookings SET status = ? WHERE id = ?;",
            (new_status, booking_id)
        )

        conn.commit()

    except sqlite3.Error as e:
        print(f"Database error occurred while updating booking: {e}")
        raise

    finally:
        conn.close()

def delete_booking_by_id(booking_id, db_url):
    if not isinstance(db_url, str):
        raise ValueError("Invalid database URL provided to delete_booking_by_id()")

    db_path = db_url.split("///")[-1]

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM bookings WHERE id = ?;",
            (booking_id,)
        )

        conn.commit()

        if cur.rowcount == 0:
            print(f"No booking found with ID: {booking_id}")
        else:
            print(f"Booking with ID {booking_id} deleted successfully.")

    except sqlite3.Error as e:
        print(f"Database error occurred while deleting booking: {e}")
        raise

    finally:
        conn.close()