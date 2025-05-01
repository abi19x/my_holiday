import psycopg
from datetime import datetime

def get_user_bookings(user_id, db_url):
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM bookings WHERE user_id = %s ORDER BY start_date DESC", (user_id,))
            return cur.fetchall()


def create_booking(user_id, booking_type, start_date, end_date, notes, db_url):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    duration = (end - start).days

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO bookings (user_id, type, start_date, end_date, duration, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, booking_type, start_date, end_date, duration, "Pending", notes))
            conn.commit()
