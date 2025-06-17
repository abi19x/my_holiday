# create_admin.py
from models.db import create_user
from config import Config

email = "k9ja1xwk@students.codeinstitute.net"
password = "masteRh0512."
is_admin = 1

create_user(email, password, is_admin, Config.DATABASE_URL)
print("Admin user created successfully.")
