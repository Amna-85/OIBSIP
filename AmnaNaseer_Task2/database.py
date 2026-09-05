import sqlite3
import os

DB_NAME = "bmi_tracker.db"

def get_connection():
    """Establish and return a database connection."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row  # Enables column access by name
        return conn
    except sqlite3.Error as e:
        print(f"[DB Error] Connection failed: {e}")
        raise

def init_db():
    """Create tables if they don't exist."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"[DB Error] Initialization failed: {e}")
        raise

def add_user(name):
    """Add a new user or return existing user ID."""
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("User name cannot be empty.")
    
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO users (name) VALUES (?)", (clean_name,))
            cursor.execute("SELECT id FROM users WHERE name = ?", (clean_name,))
            return cursor.fetchone()["id"]
    except sqlite3.Error as e:
        print(f"[DB Error] Failed to add/get user '{clean_name}': {e}")
        raise

def get_all_users():
    """Fetch list of all user names."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM users ORDER BY name ASC")
            return [row["name"] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"[DB Error] Failed to fetch users: {e}")
        return []

def save_bmi_record(user_id, weight, height, bmi, category):
    """Save a calculation record into the database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bmi_records (user_id, weight, height, bmi, category)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, weight, height, bmi, category))
            conn.commit()
    except sqlite3.Error as e:
        print(f"[DB Error] Failed to save BMI record: {e}")
        raise

def get_user_history(user_id):
    """Fetch historical records for a given user."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT weight, height, bmi, category, timestamp
                FROM bmi_records
                WHERE user_id = ?
                ORDER BY timestamp ASC
            """, (user_id,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[DB Error] Failed to fetch history: {e}")
        return []