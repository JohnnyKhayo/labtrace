
import re
import hashlib
import secrets
import hmac
import sqlite3

from contextlib import closing
from database import get_connection

ITERATIONS = 600_000

def create_users_table():
    """Create the users table if it does not exist."""

    with closing(get_connection()) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'staff'
                        CHECK(role IN ('admin', 'staff')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

def validate_email(email):
    """Check whether an email has a basic valid format."""

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.fullmatch(pattern, email.strip()))

def validate_password(password):
    """Check password requirements."""

    if len(password) < 10:
        return "Password must contain at least 10 characters."

    if not re.search(r"[A-Za-z]", password):
        return "Password must contain at least one letter."

    if not re.search(r"\d", password):
        return "Password must contain at least one number."

    return ""


def hash_password(password, salt=None):
    """Hash a password using PBKDF2 with a random salt."""

    salt = salt or secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), ITERATIONS).hex()

    return password_hash, salt


def verify_password(password, stored_hash, salt):
    """Check a password against its stored hash."""

    password_hash, _ = hash_password(password, salt)

    return hmac.compare_digest(stored_hash, password_hash)


def register_user(full_name, email, password, confirm_password):
    """Register a new staff account."""

    full_name = full_name.strip()
    email = email.strip().lower()

    # Check required fields
    if not full_name:
        return False, "Full name is required."

    if not email:
        return False, "Email is required."

    # Validate email
    if not validate_email(email):
        return False, "Please enter a valid email address."

    # Validate password
    password_error = validate_password(password)

    if password_error:
        return False, password_error

    # Confirm password
    if password != confirm_password:
        return False, "Passwords do not match."

    # Hash password before storing it
    password_hash, salt = hash_password(password)

    try:
        with closing(get_connection()) as conn:
            with conn:
                conn.execute("""
                    INSERT INTO users (
                        full_name,
                        email,
                        password_hash,
                        salt
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    full_name,
                    email,
                    password_hash,
                    salt
                ))

        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."



def authenticate_user(email, password):
    """Verify login credentials and return safe user details."""

    email = email.strip().lower()

    if not email or not password:
        return False, "Invalid email or password."

    with closing(get_connection()) as conn:
        user = conn.execute("""
            SELECT
                id,
                full_name,
                email,
                password_hash,
                salt,
                role
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()


    if user is None:
        return False, "Invalid email or password."

    if not verify_password(
        password,
        user["password_hash"],
        user["salt"]):

        return False, "Invalid email or password."

    # Return only information needed by the application
    user_details = {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"]
    }

    return True, user_details