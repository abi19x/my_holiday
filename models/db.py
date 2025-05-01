import psycopg
from flask import g
from config import Config

conn = None

def init_db(app):
    global conn
    conn = psycopg.connect(Config.DATABASE_URL)

    @app.teardown_appcontext
    def close_connection(exception):
        if conn:
            conn.close()


def get_db():
    global conn
    return conn