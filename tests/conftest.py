"""Bounded test fixtures. DB lives in a temp file per run; ALWAYS wiped after."""
import os, sqlite3, tempfile
import pytest

@pytest.fixture
def tmp_db(tmp_path):
    """A fresh, disposable SQLite DB built from the real schema.sql."""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    conn.executescript(open("schema.sql", encoding="utf-8").read())
    conn.commit()
    yield conn
    conn.close()
    if db_path.exists():
        db_path.unlink()
