import sqlite3


DB_NAME = "labtrace.db"
from sample import Sample


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

def add_sample(sample: Sample):
    """Add a new sample to the database."""
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO samples (sample_id, sample_type, collected_by, status, notes)
        VALUES (?, ?, ?, ?, ?)""", (
            sample.sample_id,
            sample.sample_type,
            sample.collected_by,
            sample.status,
            sample.notes))