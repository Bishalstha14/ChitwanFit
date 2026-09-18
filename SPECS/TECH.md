# Tech Stack & Engineering Rules

## Languages & Tools

| What | How |
|---|---|
| Structure | HTML5 — semantic tags (`<header>`, `<section>`, `<footer>`, etc.) |
| Styling | CSS3 — CSS custom properties (variables) for your design tokens |
| Interactivity | Vanilla JavaScript — no libraries, no frameworks |
| Animations | CSS keyframes + `IntersectionObserver` for scroll effects |
| Backend | Flask (Python) — a simple web server (`app.py`) |
| Data | SQLite — a single database file using plain SQL |
| Version Control | Git + GitHub |
| Deployment | Vercel, PythonAnywhere, or a Codio/public URL host |
| AI Coworker | OpenCode (your junior engineer in the terminal) |

ChitwanFit is a **dynamic app**, not just a landing page. It stores workouts and
leaderboard entries in SQLite, so the site must be served by a Flask server,
not opened as a static file.

## Codebase Layout

```
build-lab/
├── app.py            ← Flask app that serves pages and handles forms
├── database.py       ← Creates the SQLite database and table schema
├── schema.sql        ← The plain-SQL schema for our tables
├── templates/        ← HTML files rendered by Flask (Jinja)
│   └── index.html
├── static/
│   ├── style.css     ← All styles and design tokens
│   └── script.js     ← Interactions and animations
└── MISSION.md        ← Your Founder Notebook (fill this in as you go)
```

The `SPECS/` folder holds your project constitution (these files). It is not
part of the website — it is your planning space.

## Engineering Rules

### Keep it simple
Write the most obvious solution, not the cleverest one. If a beginner can't
read your code and understand it in 30 seconds, simplify it. Use only
straightforward SQLite patterns — no ORMs, no migrations.

### One thing at a time
Build in layers: database → server → first page → forms → leaderboard. Never
generate the whole site in one prompt.

### Design tokens first
Before writing any component, define your CSS variables (colors, fonts,
spacing) in `style.css`. Every component uses those variables — never hardcoded
hex codes.

### No heavy frameworks
No React, Vue, Angular, or npm packages on the front end. The backend is plain
Flask serving Jinja templates. This keeps the project readable and deployable.

### Motion budget
Maximum: 1 hero effect + 1 scroll effect + 1 microinteraction. Every animation
must have a purpose.

### Server rules (Codio)
- Bind to `0.0.0.0`, never `127.0.0.1`.
- Use a port in the range 1024–9499 (default `3000`).
- Public URL: `https://${CODIO_HOSTNAME}-${PORT}.codio.io/`
- Print and verify the public URL before announcing the site is live.

### Think before you prompt
Follow the cycle: **Think → Ask → Evaluate → Decide → Build**. Never accept AI
output without reviewing it first.

### Better AI Requests
Every prompt to OpenCode should include:
1. **Context** — what are we building?
2. **Goal** — what needs to happen right now?
3. **Constraints** — what must not change?
4. **Design** — reference `build-lab/MISSION.md` for tokens.
5. **Validation** — how will you know it worked?