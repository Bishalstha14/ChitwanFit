# ChitwanFit

**A free Ironman & runner stage tracker for Nepal.**
Swim. Bike. Run. Climb every stage. Stay live.

ChitwanFit is a free web app that helps athletes in Nepal track triathlon-style workouts one stage at a time: swim, bike, and run. It also provides a live scoreboard and public leaderboard where athletes can see real recorded times.

The project is designed around a simple idea: keep fitness tracking accessible, easy to use, and focused on the sport.

## What it does

* Stage-by-stage tracking for swim, bike, and run workouts
* Public leaderboard with recorded times
* “Live Now” sessions for following a workout or race as it happens
* Light and dark themes
* Nepal-focused branding and design
* Free to use with no subscription or paywall
* Simple and lightweight interface

## Tech stack

* **Backend:** Python 3 + Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS, and JavaScript
* **Authentication:** Email + one-time password (OTP)
* **Deployment:** Render

The application uses a single Flask backend in `app.py`. SQLite is used for storing application data, with database operations handled through `database.py`.

The frontend does not use a JavaScript framework or separate build process, which keeps the project simple to run and deploy.

## Project structure

```text
ChitwanFit/
├── app.py
├── database.py
├── index.html
├── script.js
├── style.css
├── schema.sql
├── requirements.txt
├── run_server.sh
├── render.yaml
├── .env.example
├── .gitignore
├── README.md
├── MISSION.md
├── ROADMAP.md
└── DELIVERABLES.md
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Bishalstha14/ChitwanFit.git
cd ChitwanFit
```

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Add the required values to `.env` according to the variables documented in `.env.example`.

Make sure sensitive information such as secret keys and database files are not committed to GitHub.

### 4. Run the application

```bash
python3 app.py
```

The application runs on the host and port configured by the Flask application.

Open the local address shown by the application in your browser.

## Deployment

ChitwanFit is deployed using **Render**.

The repository contains a `render.yaml` configuration file for the deployment setup. Render installs the Python dependencies from `requirements.txt` and starts the Flask application.

The main deployment commands are:

**Build Command**

```bash
pip install -r requirements.txt
```

**Start Command**

```bash
python app.py
```

For the application to work correctly on Render, the Flask server listens on the host and port provided by the deployment environment.

Every new commit pushed to the configured GitHub branch can be deployed through Render.

## Environment and security

Sensitive information is intentionally excluded from the repository.

The `.gitignore` file prevents files such as secret keys, database files, caches, and other local-only files from being committed.

Environment-specific values should be stored using environment variables rather than being written directly into the source code.

The `.env.example` file is provided as a reference for the required configuration.

## How it works

A user can create or participate in a fitness session and track the different stages of a triathlon-style workout.

The application separates the activity into:

1. **Swim**
2. **Bike**
3. **Run**

Recorded results can be displayed through the leaderboard, while “Live Now” sessions allow users to follow an active session.

The backend handles authentication, session information, database operations, and leaderboard data. The frontend provides the interface through HTML, CSS, and JavaScript.

## The build journey

ChitwanFit was developed as a small build project that documents the process from the original idea through to a working deployed application.

The repository includes supporting project documents:

* `MISSION.md` — project mission and design decisions
* `ROADMAP.md` — development roadmap
* `DELIVERABLES.md` — project deliverables
* `schema.sql` — database structure
* `render.yaml` — Render deployment configuration

The project started with the idea of creating a simple fitness tracker focused on swim, bike, and run stages. The development process then moved through planning, visual design, implementation, testing, and deployment.

## Running locally

For local development, install the dependencies and run:

```bash
pip install -r requirements.txt
python3 app.py
```

You can also use the provided `run_server.sh` script if your local environment is configured for it.

## Contributing

ChitwanFit is a small project built around the idea of making fitness tracking simple and accessible.

If you want to contribute, you can fork the repository, create a branch for your changes, test the application locally, and submit a pull request.

## Author

**Bishal Shrestha**

Chitwan, Nepal

---

**Swim. Bike. Run. Climb every stage. Stay live.**
