"""app.py — ChitwanFit.

A small Flask app, focused on Nepal. It has:
  - a public landing page,
  - signup / login with a 6-digit email OTP (via Gmail SMTP),
  - two training paths: Ironman (swim+bike+run) and Runner (run only),
  - a dashboard to log workouts and climb the stages for your path,
  - a Nepal map where every logged workout is placed as a marker,
  - a leaderboard of Nepal athletes.

Run it with:  python3 app.py
"""

import os
import secrets
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from hashlib import pbkdf2_hmac
from pathlib import Path

from flask import (
    Flask,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database import get_db, init_db

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent
SECRET_KEY_FILE = BASE_DIR / "secret_key.txt"

if SECRET_KEY_FILE.exists():
    app_secret = SECRET_KEY_FILE.read_text().strip()
else:
    app_secret = secrets.token_hex(32)
    SECRET_KEY_FILE.write_text(app_secret)

app = Flask(__name__)
app.secret_key = app_secret

EMAIL_ADDRESS = os.environ.get("CHITWANFIT_EMAIL", "")
EMAIL_PASSWORD = os.environ.get("CHITWANFIT_EMAIL_PASSWORD", "")
PORT = int(os.environ.get("PORT", "3000"))


def load_env_file():
    """Read KEY=VALUE lines from .env if it exists (no extra packages)."""
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


load_env_file()
EMAIL_ADDRESS = os.environ.get("CHITWANFIT_EMAIL", "")
EMAIL_PASSWORD = os.environ.get("CHITWANFIT_EMAIL_PASSWORD", "")

# The four real Ironman stages (swim + bike + run).
STAGES = [
    {
        "name": "Sprint",
        "swim": 0.75,
        "bike": 20,
        "run": 5,
        "total": 25.75,
        "tip": "Keep swims short and smooth. Eat mostly carbs the night before.",
    },
    {
        "name": "Olympic",
        "swim": 1.5,
        "bike": 40,
        "run": 10,
        "total": 51.5,
        "tip": "Practice quick transitions. Hydrate during the bike leg.",
    },
    {
        "name": "Half Ironman (70.3)",
        "swim": 1.9,
        "bike": 90,
        "run": 21.1,
        "total": 113.0,
        "tip": "Fuel on the bike: aim for 60-90g of carbs per hour.",
    },
    {
        "name": "Full Ironman",
        "swim": 3.8,
        "bike": 180,
        "run": 42.2,
        "total": 226.0,
        "tip": "Train long, eat real food, and walk the aid stations if needed.",
    },
]

# The official running ladder (World Athletics): 5K → 10K → Half → Marathon → 100K.
RUNNER_STAGES = [
    {
        "name": "5K",
        "run": 5,
        "tip": "Start easy. Finish your first 5K feeling like you still had more.",
    },
    {
        "name": "10K",
        "run": 10,
        "tip": "Run some 'long and slow' days each week to build the base.",
    },
    {
        "name": "Half Marathon (21.1K)",
        "run": 21.1,
        "tip": "Practice a proper warm-up and carry water on longer runs.",
    },
    {
        "name": "Marathon (42.2K)",
        "run": 42.2,
        "tip": "Test your fuelling on long runs. The wall comes from empty legs, not weak will.",
    },
    {
        "name": "Ultramarathon (100K)",
        "run": 100,
        "tip": "Respect the distance: hydration and electrolytes matter more than pace.",
    },
]

# Approximate calories burned per km, given a runner's weight in kg.
CALORIES_PER_KM = {"swim": 1.2, "bike": 0.4, "run": 1.0}

# Where ChitwanFit athletes train: Nepal cities with rough centre points.
NEPAL_CITIES = {
    "Kathmandu": [27.72, 85.32],
    "Lalitpur (Patan)": [27.66, 85.32],
    "Bhaktapur": [27.67, 85.43],
    "Pokhara": [28.21, 83.99],
    "Bharatpur (Chitwan)": [27.68, 84.43],
    "Hetauda": [27.43, 85.03],
    "Butwal": [27.70, 83.45],
    "Biratnagar": [26.45, 87.27],
    "Birgunj": [27.01, 84.87],
    "Janakpur": [26.73, 85.93],
    "Nepalgunj": [28.05, 81.62],
    "Dhangadhi": [28.68, 80.61],
    "Itahari": [26.67, 87.27],
    "Dharan": [26.81, 87.27],
    "Ghorahi (Dang)": [27.98, 82.49],
    "Surkhet (Birendranagar)": [28.60, 81.49],
    "Tansen (Palpa)": [27.87, 83.55],
    "Baglung": [28.27, 83.59],
    "Gorkha": [28.02, 84.76],
    "Jomsom (Mustang)": [28.78, 83.72],
}

# Nepal's centre for the map, plus a close zoom.
NEPAL_CENTER = [28.39, 84.12]
NEPAL_ZOOM = 7


def hash_password(password, salt):
    """Simple, safe-enough password hashing with a per-user salt."""
    return pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


@app.before_request
def load_logged_in_user():
    """Attach the logged-in user (if any) to g so templates can see them."""
    g.user = None
    user_id = session.get("user_id")
    if user_id is not None:
        conn = get_db()
        g.user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        conn.close()


def send_otp_email(to_email, code):
    """Email the 6-digit code. Needs Gmail SMTP credentials in .env."""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        # No credentials configured: fall back to printing the code.
        print(f"[DEV MODE] OTP for {to_email} is {code}")
        return

    body = (
        f"Welcome to ChitwanFit!\n\n"
        f"Your verification code is: {code}\n"
        f"It stays valid for 10 minutes.\n\n"
        f"If you did not request this, you can ignore this email."
    )
    message = MIMEText(body)
    message["Subject"] = "Your ChitwanFit verification code"
    message["From"] = EMAIL_ADDRESS
    message["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, [to_email], message.as_string())


def athlete_totals(user_id):
    """Return total km logged per sport for one athlete."""
    conn = get_db()
    rows = conn.execute(
        "SELECT sport, SUM(distance_km) AS total FROM workouts "
        "WHERE user_id = ? GROUP BY sport",
        (user_id,),
    ).fetchall()
    conn.close()
    totals = {sport: 0.0 for sport in CALORIES_PER_KM}
    for row in rows:
        totals[row["sport"]] = row["total"] or 0.0
    return totals


def stages_for(path):
    """Which stage ladder does this athlete climb?"""
    return RUNNER_STAGES if path == "runner" else STAGES


def current_stage(totals, path):
    """The highest stage matched. Runners only count their run distance."""
    ladder = stages_for(path)
    stage_index = -1
    for index, stage in enumerate(ladder):
        if path == "runner":
            reached = totals["run"] >= stage["run"]
        else:
            reached = (
                totals["swim"] >= stage["swim"]
                and totals["bike"] >= stage["bike"]
                and totals["run"] >= stage["run"]
            )
        if reached:
            stage_index = index
    if stage_index == -1:
        return None  # still working toward the first stage
    return ladder[stage_index]


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------


@app.route("/")
def landing():
    return render_template("index.html")


@app.route("/leaderboard")
def leaderboard():
    conn = get_db()
    rows = conn.execute(
        "SELECT u.name, u.city, u.path, "
        "       SUM(w.distance_km) AS total_km, "
        "       SUM(w.minutes) AS total_min "
        "FROM workouts w JOIN users u ON u.id = w.user_id "
        "GROUP BY u.id ORDER BY total_km DESC"
    ).fetchall()
    conn.close()
    board = []
    for row in rows:
        minutes = row["total_min"] or 0
        hours = minutes // 60
        board.append(
            {
                "name": row["name"],
                "city": row["city"],
                "path": row["path"],
                "total_km": round(row["total_km"] or 0, 1),
                "hours": hours,
                "minutes": minutes % 60,
            }
        )
    return render_template("leaderboard.html", board=board)


@app.route("/map")
def nepal_map():
    """Members only: your workout history pinned on a Nepal map."""
    if g.user is None or not g.user["is_verified"]:
        return redirect(url_for("login"))

    conn = get_db()
    workouts = conn.execute(
        "SELECT * FROM workouts WHERE user_id = ? ORDER BY logged_on DESC, id DESC",
        (g.user["id"],),
    ).fetchall()
    conn.close()

    markers = []
    for w in workouts:
        if w["lat"] is None or w["lng"] is None:
            continue
        minutes = w["minutes"]
        markers.append(
            {
                "city": w["city"],
                "sport": w["sport"],
                "distance_km": w["distance_km"],
                "minutes": minutes,
                "hours": minutes // 60,
                "day": w["logged_on"],
                "lat": w["lat"],
                "lng": w["lng"],
            }
        )

    return render_template(
        "map.html",
        markers=markers,
        center=NEPAL_CENTER,
        zoom=NEPAL_ZOOM,
        with_workouts=bool(markers),
    )


# ---------------------------------------------------------------------------
# Live tracking (like "Strava live"): athletes share their location in real time
# ---------------------------------------------------------------------------


def _require_live_member():
    """Small guard for the live pages/APIs; returns True when allowed."""
    if g.user is None or not g.user["is_verified"]:
        return False
    return True


@app.route("/live")
def live_map():
    """Members only: watch every athlete training live on the Nepal map."""
    if not _require_live_member():
        return redirect(url_for("login"))
    return render_template(
        "live.html", center=NEPAL_CENTER, zoom=NEPAL_ZOOM, user=g.user
    )


@app.route("/api/live/start", methods=["POST"])
def live_start():
    """Begin sharing: create (or refresh) the athlete's live row."""
    if not _require_live_member():
        return jsonify({"ok": False, "error": "not logged in"}), 401
    conn = get_db()
    conn.execute(
        "INSERT INTO live_sessions (user_id, lat, lng, updated_at) "
        "VALUES (?, 0, 0, datetime('now')) "
        "ON CONFLICT(user_id) DO UPDATE SET updated_at = datetime('now')",
        (g.user["id"],),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/live/update", methods=["POST"])
def live_update():
    """Keep the athlete's position fresh. Called every few seconds."""
    if not _require_live_member():
        return jsonify({"ok": False, "error": "not logged in"}), 401
    data = request.get_json(silent=True) or {}
    lat = data.get("lat")
    lng = data.get("lng")
    if lat is None or lng is None:
        return jsonify({"ok": False, "error": "lat/lng required"}), 400
    try:
        lat = float(lat)
        lng = float(lng)
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "lat/lng must be numbers"}), 400
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        return jsonify({"ok": False, "error": "lat/lng out of range"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO live_sessions (user_id, lat, lng, updated_at) "
        "VALUES (?, ?, ?, datetime('now')) "
        "ON CONFLICT(user_id) DO UPDATE SET "
        "lat = excluded.lat, lng = excluded.lng, updated_at = datetime('now')",
        (g.user["id"], lat, lng),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/live/stop", methods=["POST"])
def live_stop():
    """Stop sharing: remove the athlete's live row."""
    if not _require_live_member():
        return jsonify({"ok": False, "error": "not logged in"}), 401
    conn = get_db()
    conn.execute("DELETE FROM live_sessions WHERE user_id = ?", (g.user["id"],))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/live/data")
def live_data():
    """Everyone who moved in the last 30 seconds, as JSON for the map."""
    conn = get_db()
    rows = conn.execute(
        "SELECT u.name, u.city, u.path, s.lat, s.lng, s.updated_at "
        "FROM live_sessions s JOIN users u ON u.id = s.user_id "
        "WHERE datetime('now') < datetime(s.updated_at, '+30 seconds') "
        "ORDER BY s.updated_at DESC"
    ).fetchall()
    conn.close()
    athletes = [
        {
            "name": row["name"],
            "city": row["city"],
            "path": row["path"],
            "lat": row["lat"],
            "lng": row["lng"],
        }
        for row in rows
    ]
    return jsonify(athletes)


# ---------------------------------------------------------------------------
# Account routes (signup -> OTP -> login -> session)
# ---------------------------------------------------------------------------


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        city = request.form.get("city", "Kathmandu").strip()
        path = request.form.get("path", "ironman").strip()

        if path not in ("ironman", "runner"):
            path = "ironman"

        if not name or not email or not password:
            flash("Please fill in name, email, and password.")
            return redirect(url_for("signup"))

        conn = get_db()
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            conn.close()
            flash("That email is already registered. Log in instead.")
            return redirect(url_for("login"))

        salt = secrets.token_hex(16)
        password_hash = hash_password(password, salt)
        conn.execute(
            "INSERT INTO users (name, email, password_hash, country, city, path) "
            "VALUES (?, ?, ?, 'Nepal', ?, ?)",
            (name, email, f"{salt}:{password_hash}", city, path),
        )
        conn.commit()
        conn.close()

        issue_otp(email)
        session["pending_email"] = email
        return redirect(url_for("verify"))

    return render_template("signup.html", cities=NEPAL_CITIES)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()

        if user is None:
            flash("No account found with that email. Create one first.")
            return redirect(url_for("signup"))

        salt, expected = user["password_hash"].split(":", 1)
        if hash_password(password, salt) != expected:
            flash("Wrong password. Try again.")
            return redirect(url_for("login"))

        issue_otp(email)
        session["pending_email"] = email
        return redirect(url_for("verify"))

    return render_template("login.html")


def issue_otp(email):
    """Create a fresh 6-digit code and try to email it."""
    code = f"{secrets.randbelow(1_000_000):06d}"
    conn = get_db()
    conn.execute("DELETE FROM otps WHERE email = ?", (email,))
    conn.execute(
        "INSERT INTO otps (email, code) VALUES (?, ?)",
        (email, code),
    )
    conn.commit()
    conn.close()
    send_otp_email(email, code)


@app.route("/verify", methods=["GET", "POST"])
def verify():
    email = session.get("pending_email")
    if not email:
        return redirect(url_for("login"))

    if request.method == "POST":
        code = request.form.get("code", "").strip()

        conn = get_db()
        row = conn.execute(
            "SELECT id, code FROM otps "
            "WHERE email = ? AND datetime('now') < datetime(created_at, '+10 minutes') "
            "ORDER BY created_at DESC LIMIT 1",
            (email,),
        ).fetchone()

        if row is None:
            conn.close()
            flash("That code expired. Request a new one by logging in again.")
            return redirect(url_for("login"))

        if code != row["code"]:
            conn.close()
            flash("Wrong code. Try again.")
            return redirect(url_for("verify"))

        # Correct code: activate the account and start a session.
        conn.execute(
            "UPDATE users SET is_verified = 1 WHERE email = ?", (email,)
        )
        conn.execute("DELETE FROM otps WHERE email = ?", (email,))
        user = conn.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.commit()
        conn.close()

        session.pop("pending_email", None)
        session["user_id"] = user["id"]

        g.user = None
        return redirect(url_for("dashboard"))

    return render_template("verify.html", email=email)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


# ---------------------------------------------------------------------------
# Member routes (require login)
# ---------------------------------------------------------------------------


@app.route("/dashboard")
def dashboard():
    if g.user is None or not g.user["is_verified"]:
        return redirect(url_for("login"))

    path = g.user["path"] or "ironman"
    ladder = stages_for(path)

    conn = get_db()
    workouts = conn.execute(
        "SELECT * FROM workouts WHERE user_id = ? ORDER BY logged_on DESC, id DESC "
        "LIMIT 15",
        (g.user["id"],),
    ).fetchall()
    conn.close()

    totals = athlete_totals(g.user["id"])
    stage = current_stage(totals, path)
    stage_number = ladder.index(stage) + 1 if stage else 0

    calories = {
        sport: round(totals[sport] * g.user["weight_kg"] * factor)
        for sport, factor in CALORIES_PER_KM.items()
    }

    return render_template(
        "dashboard.html",
        path=path,
        stages=ladder,
        totals=totals,
        stage=stage,
        stage_number=stage_number,
        calories=calories,
        workouts=workouts,
        cities=NEPAL_CITIES,
    )


@app.route("/log", methods=["POST"])
def log_workout():
    if g.user is None or not g.user["is_verified"]:
        return redirect(url_for("login"))

    path = g.user["path"] or "ironman"

    # Runners only log run workouts.
    sport = "run" if path == "runner" else request.form.get("sport", "run")
    distance = request.form.get("distance_km", type=float)
    minutes = request.form.get("minutes", type=int)
    day = request.form.get("logged_on", "") or datetime.now().strftime("%Y-%m-%d")
    city = request.form.get("city", "Kathmandu").strip()

    if sport not in CALORIES_PER_KM or distance is None or minutes is None:
        flash("Please pick a sport and enter numbers for distance and time.")
        return redirect(url_for("dashboard"))
    if distance <= 0 or minutes <= 0:
        flash("Distance and time must be greater than zero.")
        return redirect(url_for("dashboard"))

    lat, lng = NEPAL_CITIES.get(city, [None, None])

    conn = get_db()
    conn.execute(
        "INSERT INTO workouts "
        "(user_id, sport, distance_km, minutes, logged_on, city, lat, lng) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (g.user["id"], sport, distance, minutes, day, city, lat, lng),
    )
    conn.commit()
    conn.close()

    flash("Workout logged and placed on the Nepal map!")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    print(f"Serving ChitwanFit on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT)