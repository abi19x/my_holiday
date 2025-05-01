from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.db import get_db
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/new', methods=['GET', 'POST'])
def new_booking():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user_id = session['user']['id']
        type = request.form['type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        notes = request.form.get('notes')

        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            duration = (end - start).days + 1
        except ValueError:
            flash('Invalid date format.', 'error')
            return redirect(url_for('bookings.new_booking'))

        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO bookings (user_id, type, start_date, end_date, duration, notes, status) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (user_id, type, start_date, end_date, duration, notes, 'Pending')
            )
            conn.commit()

        flash('Booking request submitted.', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('new_booking.html')