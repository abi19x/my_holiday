from flask import Flask, render_template
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

    @app.route('/')
    def index():
        return render_template('index.html')

    return app