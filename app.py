import psycopg
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_session import Session
from config import Config
from models.db import init_db, get_user_by_email
from models.booking import get_user_bookings, create_booking, get_all_bookings, update_booking_status
from werkzeug.security import generate_password_hash, check_password_hash


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Session(app)  # Initialize session
    init_db(app)  # Create tables

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            hashed_pw = generate_password_hash(password)

            with psycopg.connect(app.config["DATABASE_URL"]) as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s);", (name, email, hashed_pw))
                    conn.commit()
            return redirect("/login")
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            user = get_user_by_email(email, app.config["DATABASE_URL"])
            if user and check_password_hash(user[3], password):  # password is at index 3
                session["user_id"] = user[0]
                session["user_name"] = user[1]
                session["user_email"] = user[2]
                session["is_admin"] = (user[2] == "admin@example.com")
                flash("Successfully logged in!", "success")
                return redirect("/dashboard")
            else:
                flash("Invalid email or password", "error")
                return render_template("login.html")  # stay on login page
            return "Invalid credentials", 401
        return render_template("login.html")

    @app.route("/dashboard")
    def dashboard():
        if "user_email" not in session:
            return redirect("/login")
        bookings = get_user_bookings(session["user_id"], app.config["DATABASE_URL"])
        return render_template("dashboard.html", bookings=bookings)

    @app.route("/new_booking", methods=["GET", "POST"])
    def new_booking():
        if "user_id" not in session:
            return redirect("/login")
        if request.method == "POST":
            booking_type = request.form["type"]
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]
            notes = request.form.get("notes", "")
            create_booking(
                user_id=session["user_id"],
                booking_type=booking_type,
                start_date=start_date,
                end_date=end_date,
                notes=notes,
                db_url=app.config["DATABASE_URL"]
            )
            return redirect("/dashboard")
        return render_template("new_booking.html")

    @app.route("/admin", methods=["GET", "POST"])
    def admin_dashboard():
        if not session.get("is_admin"):
            return redirect("/login")
        bookings = get_all_bookings(app.config["DATABASE_URL"])
        return render_template("admin_dashboard.html", bookings=bookings)

    @app.post("/admin/update/<int:booking_id>")
    def update_booking(booking_id):
        if not session.get("is_admin"):
            return redirect("/login")
        new_status = request.form["status"]
        update_booking_status(booking_id, new_status, app.config["DATABASE_URL"])
        return redirect("/admin")


    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        flash("You have been logged out.", "error")
        return redirect(url_for("login"))

    return app
