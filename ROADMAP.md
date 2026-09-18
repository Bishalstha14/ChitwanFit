# ChitwanFit — Roadmap

*This is the "where are we and where are we going" companion to `MISSION.md`.
The Founder Notebook holds the **why** (vision, brand, decisions); this file
holds the **what's built, what's next** with a status check on every row.*

- **Reading order:** `MISSION.md` first (the story), then this file (the plan).
- **Single source of truth:** `MISSION.md`. If these two ever disagree, MISSION wins.
- **Keeping it real for the launch:** goals below assume just you + first real members in Chitwan. No big marketing promises.

---

## Current State (checked 2026-09-18)

| Area | State | Notes |
|---|---|---|
| **Database** | 0 users · 0 workouts · 0 live sessions | Clean slate for the real launch |
| **Server** | Live on port 3000 | Verified through the public URL — `/` 200, `/login` 200, `/leaderboard` 200, unknown routes 404 |
| **Login** | Email OTP with `secrets.randbelow` codes | 6-digit codes, expire in 10 min, auto-clean, can't be guessed |
| **Workouts** | Working (swim / bike / run, km + minutes + calories + city on the Nepal map) | Parameterized SQL — no injection holes |
| **Leaderboard** | Working, shows empty state gracefully now that test users are gone | A proud "no athletes yet — be the first" message |
| **Live Now** | Working (member shares GPS, others watch a pulsing Nepal map, browsers only) | Opt-in, members only, stops when you leave the tab |
| **Themes** | Light + Dark toggle, saved per browser | Green + amber (light), electric orange + gold (dark) |
| **Logo** | Rhino-in-Nepal-flag pennant (`static/logo.svg`) | Original artwork, no copyright issues |

---

## Stage 1 — Idea & Positioning ✅ Done

- [x] Pick the idea: **ChitwanFit** — free Ironman / running stage tracker for Nepal
- [x] Run a 5-Point Filter (User, Problem, Value, Feasibility, Clarity) → **proceed**
- [x] Write the One-Liner and lock the guardrails (free, simple, one CTA)

## Stage 2 — Brand & Design ✅ Done

- [x] Define brand personality: Professional · Interactive · Outdoorsy
- [x] Pick colors + fonts (Merriweather headings / Inter body; green+amber light, electric dark)
- [x] Design the one-horned rhino logo (`static/logo.svg`)
- [x] Light/dark theme toggle, saved in the browser

## Stage 3 — Pages & Content ✅ Done

- [x] Landing page: hero, the stages, how it works, features, footer
- [x] Signup → email OTP → login flow
- [x] Dashboard (log a workout, "your totals")
- [x] Leaderboard · personal Nepal map · Live Now
- [x] Safety pass: `secrets.randbelow` OTPs, parameterized SQL, no dead code, no test data
- [x] **Public URL verified** — serves live on the Codio box

## Stage 4 — Test & Refine (next) ⏳ Next

*This is the stage before we call it "ready."*

- [ ] Ask 1–2 real Chitwan runners/cyclists to try ChitwanFit and log a real workout
- [ ] Watch where they hesitate (signup? logging? the map?) and fix the roughest click
- [ ] Confirm the empty leaderboard now fills with **real** names, not fake ones
- [ ] Check the app on a **phone** (most athletes will open it on mobile) — tap targets, form size

## Stage 5 — Polish & Launch Prep ⏳ Next (ordered)

- [ ] Final content review: photo of real stage routes, refueling/diet tips per stage
- [ ] Harden email sending so OTPs arrive reliably (and handle the "no mail config" box gracefully)
- [ ] Launch checklist:
  - [ ] Wipe any leftover test data (already done)
  - [ ] Confirm the public URL command (`https://${CODIO_HOSTNAME}-3000.codio.io/`) in one short line
  - [ ] Announce in local Chitwan running/cycling groups

## Stage 6 — Launch & First Athletes 🚧 Backlog

- [ ] Invite the community: first workout + leaderboard debut
- [ ] Gather "first month" numbers: how many athletes, how many workouts logged
- [ ] Plan the next feature from real feedback (candidates: training plans, streak badges, Strava import)

---

## Notes for the founder

- **Keep it free** — that's the whole point. No pricing anywhere.
- **One CTA** — "start your journey" → create an account → log a workout. Don't distract.
- **Move step by step** — each checkmark above is one small, verifiable step. No giant rewrites.
- When you finish a step, update **both** this file and the decision log in `MISSION.md` with today's date.
