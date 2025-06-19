import os
import psycopg2
from urllib.parse import urlparse
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2.extras


def init_db(app):
    db_url = app.config["DATABASE_URL"]

    # Parse the DATABASE_URL provided by Heroku
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]  # remove leading slash
    hostname = result.hostname
    port = result.port

    # Connect using psycopg2
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )

    cur = conn.cursor()

    # Enable foreign key constraints (Postgres has this on by default)
    # cur.execute("SET session_replication_role = 'origin';")  # optional

    # Create users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    );
    """)

    # Create bookings table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id SERIAL PRIMARY KEY,
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
    # Parse the PostgreSQL URL
    result = urlparse(db_url)
    username = result.username
    password_db = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password_db,
        host=hostname,
        port=port
    )
    cur = conn.cursor()

    # Check if user already exists
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cur.fetchone():
        print(f"User with email {email} already exists.")
        cur.close()
        conn.close()
        return

    hashed_password = generate_password_hash(password)

    cur.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
    """, (name, email, hashed_password, role))

    conn.commit()
    cur.close()
    conn.close()
    print(f"User {email} created.")


def get_user_by_email(email, db_url):
    # Parse the PostgreSQL URL
    result = urlparse(db_url)
    username = result.username
    password_db = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password_db,
        host=hostname,
        port=port
    )
    cur = conn.cursor()

    # Execute query
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    row = cur.fetchone()

    # If a row is found, get column names and zip into a dict
    if row:
        colnames = [desc[0] for desc in cur.description]
        user = dict(zip(colnames, row))
    else:
        user = None

    cur.close()
    conn.close()
    return user

def create_booking(user_id, booking_type, start_date, end_date, notes, duration, db_url):
    # Parse the PostgreSQL connection URL
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    cur = conn.cursor()

    # Execute insert query
    cur.execute("""
        INSERT INTO bookings (user_id, type, start_date, end_date, notes, duration, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'pending')
    """, (user_id, booking_type, start_date, end_date, notes, duration))

    # Commit and clean up
    conn.commit()
    cur.close()
    conn.close()

def get_booking_by_id(booking_id, db_url):
    # Parse the PostgreSQL connection URL
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )

    # Use a cursor that returns dict-like rows
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Execute the query
    cur.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
    booking = cur.fetchone()

    # Cleanup
    cur.close()
    conn.close()

    return dict(booking) if booking else None

def update_booking_record(booking_id, booking_type, start_date, end_date, notes, duration, db_url):
    # Parse the PostgreSQL connection URL
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    cur = conn.cursor()

    # Execute update
    cur.execute("""
        UPDATE bookings
        SET type = %s, start_date = %s, end_date = %s, notes = %s, duration = %s
        WHERE id = %s
    """, (booking_type, start_date, end_date, notes, duration, booking_id))

    conn.commit()
    cur.close()
    conn.close()


def update_booking_status(booking_id, new_status, db_url):
    if not isinstance(db_url, str):
        raise ValueError("Invalid database URL provided to update_booking_status()")

    # Parse PostgreSQL connection URL
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    try:
        conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        cur = conn.cursor()

        cur.execute(
            "UPDATE bookings SET status = %s WHERE id = %s;",
            (new_status, booking_id)
        )

        conn.commit()

    except psycopg2.Error as e:
        print(f"Database error occurred while updating booking: {e}")
        raise

    finally:
        if conn:
            conn.close()

def delete_booking_by_id(booking_id, db_url):
    # Parse PostgreSQL connection URL
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]  # Remove leading '/'
    hostname = result.hostname
    port = result.port

    try:
        conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        cur = conn.cursor()
        cur.execute("DELETE FROM bookings WHERE id = %s;", (booking_id,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Database error occurred while deleting booking: {e}")
        raise
    finally:
        if conn:
            conn.close()
