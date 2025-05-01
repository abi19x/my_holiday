from flask import Blueprint, render_template, session, redirect, url_for
from models.db import get_db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM bookings WHERE user_id = %s ORDER BY start_date DESC', (session['user']['id'],))
        bookings = cur.fetchall()

    return render_template('dashboard.html', bookings=bookings, user=session['user'])