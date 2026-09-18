"""Red first: recording a workout MUST add one interactions row (kind='workout')."""
import sqlite3, pytest

def test_workout_record_creates_interaction(tmp_db):
    u = tmp_db.execute(
        "INSERT INTO users (name, email, password_hash, country, city) "
        "VALUES (?, ?, 'x', 'Nepal', 'Bharatpur') RETURNING id",
        ("Tester", "tester@example.com"),
    ).fetchone()["id"] if False else None
    # For beginner clarity: plain INSERT then read id back.
    cur = tmp_db.execute(
        "INSERT INTO users (name, email, password_hash, country, city) "
        "VALUES (?, ?, 'x', 'Nepal', 'Bharatpur')",
        ("Tester", "tester@example.com"),
    )
    uid = cur.lastrowid
    assert uid > 0
    # Recreate the app's insert_workout SQL in plain terms for the test.
    tmp_db.execute(
        "INSERT INTO workouts (user_id, sport, distance_km, duration_min) "
        "VALUES (?, 'swim', 1.5, 45)",
        (uid,),
    )
    tmp_db.commit()
    rows = tmp_db.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
    assert rows == 1, f"wanted 1 interaction row, got {rows}"
