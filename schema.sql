-- ChitwanFit database schema
-- A new athlete is stored in `users`.
-- Each logged workout goes in `workouts`.
-- Login/verification codes live in `otps`.

-- path: 'ironman' (swim+bike+run) or 'runner' (run only)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'Nepal',
    city TEXT NOT NULL DEFAULT 'Kathmandu',
    path TEXT NOT NULL DEFAULT 'ironman',
    weight_kg REAL NOT NULL DEFAULT 70,
    is_verified INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS otps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    code TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- city + lat/lng say WHERE in Nepal the workout happened,
-- so we can place it on the Nepal activity map.
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    sport TEXT NOT NULL CHECK (sport IN ('swim', 'bike', 'run')),
    distance_km REAL NOT NULL,
    minutes INTEGER NOT NULL,
    logged_on TEXT NOT NULL DEFAULT (date('now')),
    city TEXT NOT NULL DEFAULT 'Kathmandu',
    lat REAL,
    lng REAL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- A "live" athlete currently sharing their location from the Live Now page.
-- One row per athlete; it is written every few seconds while they broadcast.
CREATE TABLE IF NOT EXISTS live_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE (user_id)
);