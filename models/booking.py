import os
import psycopg2
from urllib.parse import urlparse
from datetime import datetime

def create_booking(user_id, booking_type, start_date, end_date, notes, db_url):
    # Calculate duration in days
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    duration = (end - start).days + 1

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
        cur.execute("""
            INSERT INTO bookings (user_id, type, start_date, end_date, duration, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (user_id, booking_type, start_date, end_date, duration, "Pending", notes))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Database error occurred while creating booking: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_user_bookings(user_id, db_url):
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]  # strip leading '/'
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
        cur.execute("""
            SELECT * FROM bookings WHERE user_id = %s ORDER BY start_date DESC;
        """, (user_id,))
        bookings = cur.fetchall()
        return bookings
    except psycopg2.Error as e:
        print(f"Database error occurred while fetching bookings: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_bookings(db_url):
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:]  # strip leading '/'
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
        cur.execute("""
            SELECT b.id, u.name, b.type, b.start_date, b.end_date, b.duration, b.notes, b.status
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            ORDER BY b.start_date DESC;
        """)
        bookings = cur.fetchall()
        return bookings
    except psycopg2.Error as e:
        print(f"Database error occurred while fetching all bookings: {e}")
        raise
    finally:
        if conn:
            conn.close()

def update_booking_status(booking_id, status, db_url):
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path.lstrip('/')
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
        cur.execute("""
            UPDATE bookings SET status = %s WHERE id = %s;
        """, (status, booking_id))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Database error occurred while updating booking status: {e}")
        raise
    finally:
        if conn:
            conn.close()
