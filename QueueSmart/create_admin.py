import sqlite3
from werkzeug.security import generate_password_hash

# Connect to database
conn = sqlite3.connect("database/queuesmart.db")
cursor = conn.cursor()

# Admin details
name = "Sai Bolla"   # updated name with space
email = "admin@queuesmart.com"
password = "admin123"  # you can change
role = "admin"

# Hash password
hashed_password = generate_password_hash(password)

# Insert into users table
cursor.execute("""
INSERT INTO users (name, email, password, role)
VALUES (?, ?, ?, ?)
""", (name, email, hashed_password, role))

conn.commit()
conn.close()

print("✅ Admin user 'Sai Bolla' created successfully!")