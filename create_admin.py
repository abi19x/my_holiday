from werkzeug.security import generate_password_hash
import psycopg2

conn = psycopg2.connect(
    dbname="mydb",
    user="myuser",
    password="masteRh0512.",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Replace with your desired admin credentials
name = "Admin"
email = "k9ja1xwk@students.codeinstitute.net"
password = "masteRh0512."
hashed_pw = generate_password_hash(password)
role = "admin"

# Check if admin exists
cur.execute("SELECT * FROM users WHERE email = %s", (email,))
if cur.fetchone():
    print("Admin already exists.")
else:
    cur.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
    """, (name, email, hashed_pw, role))
    conn.commit()
    print("Admin created.")

cur.close()
conn.close()
