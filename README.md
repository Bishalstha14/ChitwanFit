# ChitwanFit

**A free Ironman & runner stage tracker for Nepal.** Swim. Bike. Run.
Climb every stage. Stay live.

ChitwanFit is a small, free web app that lets athletes in Nepal (and any
living room Ironwoman or Ironman) follow the triathlon stages — swim, bike,
run — one stage at a time, with a live scoreboard to prove it. It is free
foreverchers: no subscriptions, one call to action, and no data sold.

## What it does

- Stage-by-stage tracking for swim / bike / run workouts
- A public leaderboard (sorted, real times, no fake entries)
- “Live Now” sessions so an athlete can follow a race as it happens
- Light & dark themes
- A Nepal-focused brand: colors and language built for the local community
- One free CTA — no paywall, no Metasla groundwork, just the sport

## Tech stack

- **Backend:** Python 3 + Flask (single `app.py`)
- **Database:** SQLite via `database.py` (simple schema, all queries parameterized)
- **Frontend:** plain HTML/CSS/JS — no frameworks, no build step
- **Auth:** email + one-time code (OTP generated with `secrets`, never stored in the repo)

Secrets and the live database are excluded from this repo via `.gitignore`
(`secret_key.txt`, `*.db`, caches) — nothing sensitive is tracked.

## Getting started

```bash
pip install -r requirements.txt
cp .env.example .env        # add your values (see .env.example)
python3 app.py              # binds 0.0.0.0:3000
```

Then open <http://localhost:3000/>. On a Codio box the public URL is
`https://<CODIO_HOSTNAME>-3000.codio.io/`.

> Note: the app needs a `secret_key.txt` (or matching secret in the env) to
> sign sessions and OTPs. Create it locally — it is intentionally not in this
> repository. See `.env.example`.

## How it's run

`run_server.sh` launches the Flask app detached (binds `0.0.0.0`, writes logs,
disowned so it survives the shell). The live public copy serves exactly what is
committed here.

## The build journey

This repo tracks the whole founder journey as a *build lab*:

- `MISSION.md` — the founder decision log and design system
- `ROADMAP.md` — the six-stage plan from idea to launch
- `SPECS/` — mission, roadmap, tech notes

Stages 1–3 (idea, scope, visual identity) and Stage 5's core (the app itself)
are done. Stage 6 has shipped here: this code is public, and a live copy runs
on the Codio public URL.

## Coded by

**Bishal Shrestha** · Bharatpur-11, Bhojad, Chitwan

Swim. Bike. Run. Climb every stage. Stay live.
