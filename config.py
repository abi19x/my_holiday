import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SESSION_TYPE = 'filesystem'
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://your_db_user:your_db_password@localhost/holiday_planner')
