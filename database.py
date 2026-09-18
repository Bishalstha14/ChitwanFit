"""database.py — tiny helpers for talking to the SQLite database.

Every request in app.py opens a connection with get_db(), runs some
very plain SQL, and closes it. Nothing fancy — just simple queries.
"""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "chitwanfit.db")


def get_db():
    """Open a connection, run it with row_factory so rows are dicts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _table_columns(conn, table):
    """Return the list of column names a table actually has."""
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return [row["name"] for row in rows]


def init_db():
    """Create the tables (if missing) and add any newer columns to old DBs."""
    conn = get_db()

    # 1. Create tables that don't exist yet (fresh start).
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, encoding="utf-8") as f:
        conn.executescript(f.read())

    # 2. If this is an older database, add the newer columns so nothing breaks.
    user_columns = _table_columns(conn, "users")
    if "city" not in user_columns:
        conn.execute("ALTER TABLE users ADD COLUMN city TEXT NOT NULL DEFAULT 'Kathmandu'")
    if "path" not in user_columns:
        conn.execute("ALTER TABLE users ADD COLUMN path TEXT NOT NULL DEFAULT 'ironman'")

    workout_columns = _table_columns(conn, "workouts")
    if "city" not in workout_columns:
        conn.execute("ALTER TABLE workouts ADD COLUMN city TEXT NOT NULL DEFAULT 'Kathmandu'")
    if "lat" not in workout_columns:
        conn.execute("ALTER TABLE workouts ADD COLUMN lat REAL")
    if "lng" not in workout_columns:
        conn.execute("ALTER TABLE workouts ADD COLUMN lng REAL")

    conn.commit()
    conn.close()