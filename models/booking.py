import sqlite3
from datetime import datetime

def create_booking(user_id, booking_type, start_date, end_date, notes, db_url):
    # Calculate duration in days
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    duration = (end - start).days + 1

    db_path = db_url.split("///")[-1]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO bookings (user_id, type, start_date, end_date, duration, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (user_id, booking_type, start_date, end_date, duration, "Pending", notes))

    conn.commit()
    conn.close()



def get_user_bookings(user_id, db_url):
    db_path = db_url.split("///")[-1]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM bookings WHERE user_id = ? ORDER BY start_date DESC;
    """, (user_id,))
    bookings = cur.fetchall()
    conn.close()
    return bookings


def get_all_bookings(db_url):
    db_path = db_url.split("///")[-1]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT b.id, u.name, b.type, b.start_date, b.end_date, b.duration, b.notes, b.status
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        ORDER BY b.start_date DESC;
    """)
    bookings = cur.fetchall()
    conn.close()
    return bookings

def update_booking_status(booking_id, status, db_url):
    db_path = db_url.split("///")[-1]
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        UPDATE bookings SET status = ? WHERE id = ?;
    """, (status, booking_id))
    conn.commit()
    conn.close()
