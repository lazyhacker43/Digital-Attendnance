import sqlite3
from auth import hash_password
from datetime import datetime

conn = sqlite3.connect("attendance.db")
hashed = hash_password("test123")

conn.execute("""
    INSERT INTO users (role, full_name, email, password_hash, created_at)
    VALUES (?, ?, ?, ?, ?)
""", ("Teacher", "Integration Test Teacher", "integrationtest@test.com", hashed, datetime.utcnow().isoformat()))

conn.commit()
print("Test teacher created with email: integrationtest@test.com / password: test123")
conn.close()