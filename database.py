import sqlite3
from voice import speak

def setup_database():
    conn = sqlite3.connect("disaster.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

setup_database()

def save_emergency_code(user, code):
    conn = sqlite3.connect("disaster.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE name = ?", (user,))
    cursor.execute("INSERT INTO users (name, code) VALUES (?, ?)", (user, code))
    conn.commit()
    conn.close()
    speak("Emergency code saved successfully.")

def get_emergency_codes():
    conn = sqlite3.connect("disaster.db")
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM users")
    result = cursor.fetchall()
    conn.close()
    return [r[0].lower() for r in result]
