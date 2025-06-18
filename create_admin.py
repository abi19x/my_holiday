from models.db import create_user
from config import Config

#admin user
name = "Abi19x"
email = "k9ja1xwk@students.codeinstitute.net"
password = "masteRh0512."
role = "admin"

create_user(name, email, password, role, Config.DATABASE_URL)

print("Admin user created successfully!")
