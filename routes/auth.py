from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO users (name, email, password_hash, is_admin) VALUES (%s, %s, %s, false)',
                (name, email, hashed_password)
            )
            conn.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cur.fetchone()

            if user and check_password_hash(user[3], password):
                session['user'] = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'is_admin': user[4]
                }
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash('Invalid email or password.', 'error')

    return render_template('login.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))