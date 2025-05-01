from flask import Flask, render_template, request
from flask_session import Session
from flask import flash
from config import Config
from models.db import init_db

"""
from routes.auth import auth_bp
from routes.bookings import bookings_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp
"""

from werkzeug.security import check_password_hash
from models.db import get_user_by_email
from models.booking import get_user_bookings, create_booking, get_all_bookings, update_booking_status

#def create_app():
 #   app = Flask(__name__)
  #  app.config.from_object(Config)

   # Session(app)
    #init_db(app)

    #app.register_blueprint(auth_bp)
    #app.register_blueprint(bookings_bp, url_prefix='/bookings')
    #app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    #app.register_blueprint(admin_bp, url_prefix='/admin')

    #return app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Dashboard page
    @app.route("/")
    def dashboard():
        return render_template("dashboard.html")
    
    # Register page
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

    # Login page
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            # TODO: Validate user against database
            user = get_user_by_email(email, app.config["DATABASE_URL"])
            if user and check_password_hash(user[3], password):  # user[3] = password field
                session["user_email"] = user[2]
                session["user_name"] = user[1]
                session["user_id"] = user[0] 
                session["is_admin"] = (user["email"] == "admin@example.com")  # Example check

                return redirect("/dashboard")
            else:
                return "Invalid credentials", 401

        return render_template("login.html")

    # Dashboard page
    @app.route("/dashboard")
    def dashboard():
        if "user_email" not in session:
            return redirect("/login")
        
        bookings = get_user_bookings(session["user_id"], app.config["DATABASE_URL"])
        return render_template("dashboard.html", bookings=bookings)
    
    # New-booking page
    @app.route("/bookings/new", methods=["GET", "POST"])
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
    
    # Admin-dashboard page
    @app.route("/admin", methods=["GET", "POST"])
    def admin_dashboard():
        if not session.get("is_admin"):
            return redirect("/login")

        bookings = get_all_bookings(app.config["DATABASE_URL"])
        return render_template("admin_dashboard.html", bookings=bookings)

    # Admin update
    @app.post("/admin/update/<int:booking_id>")
    def update_booking(booking_id):
        if not session.get("is_admin"):
            return redirect("/login")
        
        new_status = request.form["status"]
        update_booking_status(booking_id, new_status, app.config["DATABASE_URL"])
        return redirect("/admin")

    return app