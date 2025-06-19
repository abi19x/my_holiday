import sqlite3 
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_session import Session
from config import Config
from models.db import init_db, get_user_by_email, delete_booking_by_id, get_booking_by_id, update_booking_record, create_booking
from models.booking import get_user_bookings, get_all_bookings, update_booking_status
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



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

            db_path = app.config["DATABASE_URL"].split("///")[-1]
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?);", (name, email, hashed_pw))
            conn.commit()
            conn.close()

            return redirect("/login")
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            user = get_user_by_email(email, app.config["DATABASE_URL"])  # Should return dict

            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                session["user_name"] = user.get("name", "")
                session["user_email"] = user["email"]
                session["user_role"] = user.get("role", "user")
                session["is_admin"] = user.get("role", "") == "admin"

                flash("Successfully logged in!", "success")
                return redirect("/admin" if session["is_admin"] else "/dashboard")

            flash("Invalid email or password", "error")

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

            # Calculate duration
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            duration = (end_date_obj - start_date_obj).days + 1  # +1 to include both start and end

            create_booking(
                user_id=session["user_id"],
                booking_type=booking_type,
                start_date=start_date,
                end_date=end_date,
                notes=notes,
                duration=duration,
                db_url=app.config["DATABASE_URL"]
            )
           
            return redirect("/dashboard")
        return render_template("new_booking.html")
    
    @app.route("/edit/<int:booking_id>", methods=["GET", "POST"])
    def edit_booking(booking_id):
        if "user_id" not in session:
            flash("Please log in.", "error")
            return redirect("/login")

        booking = get_booking_by_id(booking_id, app.config["DATABASE_URL"])

        # Optional: restrict access only to the booking owner
        if booking["user_id"] != session["user_id"]:
            flash("Unauthorized", "error")
            return redirect("/dashboard")

        if request.method == "POST":
            type = request.form["type"]
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]
            notes = request.form["notes"]

            # Calculate duration
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            duration = (end_date_obj - start_date_obj).days + 1  # +1 to include both start and end

            update_booking_record(booking_id, type, start_date, end_date, notes, duration, app.config["DATABASE_URL"])
            flash("Booking updated", "success")
            return redirect("/dashboard")

        return render_template("edit_booking.html", booking=booking)
    
    @app.route("/delete/<int:booking_id>", methods=["POST"])
    def delete_user_booking(booking_id):
        if "user_id" not in session:
            flash("Please log in.", "error")
            return redirect("/login")

        booking = get_booking_by_id(booking_id, app.config["DATABASE_URL"])
        if not booking or booking["user_id"] != session["user_id"]:
            flash("Unauthorized action.", "error")
            return redirect("/dashboard")

        delete_booking_by_id(booking_id, app.config["DATABASE_URL"])
        flash("Booking deleted successfully.", "success")
        return redirect("/dashboard")


    @app.route("/admin", methods=["GET", "POST"])
    def admin_dashboard():
        if not session.get("is_admin"):
            flash("You must be an admin to access the admin dashboard.", "error")
            return redirect("/login")

        bookings = get_all_bookings(app.config["DATABASE_URL"])
        return render_template("admin_dashboard.html", bookings=bookings)

    @app.route("/admin/update/<int:booking_id>", methods=["POST"])
    def update_booking(booking_id):
        if not session.get("is_admin"):
            flash("Unauthorized access", "error")
            return redirect("/login")
        
        new_status = request.form.get("status")

        if new_status not in ["Pending", "Approved", "Rejected"]:
            flash("Invalid status selected.", "error")
            return redirect("/admin")

        update_booking_status(booking_id, new_status, app.config["DATABASE_URL"])
        flash("Booking status updated successfully.", "success")
        return redirect("/admin")

    @app.route("/admin/delete/<int:booking_id>", methods=["POST"])
    def delete_booking(booking_id):
        if not session.get("is_admin"):
            flash("Unauthorized access", "error")
            return redirect("/login")

        print(f"Deleting booking ID: {booking_id}")  # Debug line
        delete_booking_by_id(booking_id, app.config["DATABASE_URL"]) 
        flash("Booking request deleted successfully.", "success")
        return redirect("/admin")



    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        flash("You have been logged out.", "error")
        return redirect(url_for("login"))

    return app
