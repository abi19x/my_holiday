import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SESSION_TYPE = 'filesystem'
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://myuser:masteRh0512.@localhost:5433/mydb')
