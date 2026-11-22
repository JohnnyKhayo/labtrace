import sqlite3


DB_NAME = "labtrace.db"


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    """Create the samples table if it does not exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_id TEXT UNIQUE NOT NULL,
                sample_type TEXT NOT NULL,
                collected_by TEXT NOT NULL,
                status TEXT NOT NULL,
                notes TEXT
            ) """)