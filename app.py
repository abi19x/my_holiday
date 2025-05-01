from flask import Flask, render_template, request
from flask_session import Session
from flask import flash
from config import Config
from models.db import init_db

from routes.auth import auth_bp
from routes.bookings import bookings_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp

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
            # TODO: Save to DB
            return render_template("register_success.html", name=name)
        return render_template("register.html")

    # Login page
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    # New-booking page
    @app.route("/new_booking")
    def new_booking():
        return render_template("new_booking.html")
    
    # Admin-dashboard page
    @app.route("/admin_dashboard")
    def admin_dashboard():
        return render_template("admin_dashboard.html")

    return app