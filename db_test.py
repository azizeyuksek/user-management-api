import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")

cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)", (1, "Azize"))

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

print(rows)

conn.commit()
conn.close()