from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.db import get_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def admin_dashboard():
    if 'user' not in session or not session['user']['is_admin']:
        return redirect(url_for('auth.login'))

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT b.id, u.name, b.type, b.start_date, b.end_date, b.duration, b.notes, b.status
            FROM bookings b JOIN users u ON b.user_id = u.id
            ORDER BY b.start_date DESC
        ''')
        bookings = cur.fetchall()

    return render_template('admin_dashboard.html', bookings=bookings)


@admin_bp.route('/update/<int:booking_id>', methods=['POST'])
def update_booking(booking_id):
    if 'user' not in session or not session['user']['is_admin']:
        return redirect(url_for('auth.login'))

    status = request.form['status']

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute('UPDATE bookings SET status = %s WHERE id = %s', (status, booking_id))
        conn.commit()

    flash('Booking status updated.', 'success')
    return redirect(url_for('admin.admin_dashboard'))