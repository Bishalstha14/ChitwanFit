# Founder Notebook

Welcome to your Founder Notebook. This is the single source of truth for your startup project. As founder and lead decision-maker, use this file to define your concept, guide OpenCode, and track every important decision.

---

## 0. Founder Decision (Official)

*Recorded: 2026-09-18 · Verified with the 5-Point Filter in Stage 1*

**The Startup:** ChitwanFit — a free training web app for aspiring Ironman athletes.

**The Decision:** Proceed with ChitwanFit through the remaining stages.

**Why (5-Point Filter):**

| Filter | Rating | Notes |
|---|---|---|
| User | Solid | Real, addressable segment (beginning-to-intermediate endurance athletes); founder is the first user |
| Problem | Solid | Real pain (intimidating distances, scattered training); must lean on the stage-ladder + free differentiators vs Strava/Garmin |
| Value | Solid | "Free forever" + 4 real Ironman stages + workout logging with calories + leaderboards & world map |
| Feasibility | Strong | Already built, running, and verified live on the public URL (Flask + SQLite + email OTP) |
| Clarity | Strong | Passes the 20-Second Check: climb the four real Ironman stages by logging workouts |

**The One-Liner (keep forever):**
> ChitwanFit helps aspiring Ironman athletes who are overwhelmed by the distances by giving them a free, stage-by-stage training tracker, so they can climb from Sprint to Full Ironman with clear progress and friendly competition.

**Guardrails (locked in):**
- Always free. No payments, no pricing tiers.
- One clear CTA: start your journey (create an account, log a workout).
- Keep it simple: plain Flask + SQLite, no frameworks, no fancy database tools.

**Open Watch-Item:** The problem is well-served by free incumbents. As we build, sharpen the differentiator (stage progression + community feel) so ChitwanFit is not "just another tracker."

**Stage 2 Refined Scope (recorded 2026-09-18):**
- **First launch user:** The local community (runners, cyclists, and swimmers around Chitwan) — they are the ones who join the leaderboard in Month 1. Global reach stays the long-term goal, but we design, name, and pitch to this ONE group first.
- **20-Second Simplicity Check:** Passed — the founder can explain the app in under 20 seconds, plain words, to anyone.
- **Core Solution (simple version):** Account + OTP login → dashboard with 4 stages → log swim/bike/run workouts → progress bar + calorie estimate → leaderboard → world map of athletes.
- **Primary CTA (locked):** "Start free" / "Start your journey" → create an account and log a workout. One CTA only.

### Nepal-First Pivot (recorded 2026-09-18)

- **Focus:** ChitwanFit now serves **Nepal only** — athletes pick their training city from a list of Nepal cities at signup. No more "Other" countries.
- **Two paths (via founder research):**
  - **Ironman** — swim + bike + run, 4 stages (Sprint → Olympic → 70.3 → Full).
  - **Runner** — run only, 5 official stages (World Athletics): 5K → 10K → Half Marathon → Marathon → 100K Ultra.
- **Nepal activity map:** every logged workout is pinned on a Nepal map at the city where the athlete trained — the map page is the athlete's own training history.
- **Anonymous world map removed** because the app is Nepal-first — replaced by the personal Nepal activity map.

### Brand Logo (recorded 2026-09-18)

- **Concept:** The **one-horned rhino** *(gaṇḍā, the symbol of Chitwan National Park)* in silhouette, standing in front of the Mahabharat mountain range with the sun rising over the Terai.
- **Why:** Chitwan's identity IS the rhino + jungle + mountains + sun. Using it in the logo makes ChitwanFit instantly feel local, strong, and outdoorsy.
- **Design note:** The rhino is drawn in motion (stride + tunes with the "training in progress" message), one horn only, in a cream silhouette on the brand green, with a warm gold sun.
- **File:** `static/logo.svg` — used in the navbar (top-left) and footer of every page. Original hand-drawn design; not a copy of the park's official logo.

### Live Tracking "Live Now" (recorded 2026-09-18)

- **Feature:** Athletes can share their live location while training (Strava-style). Other logged-in athletes see them as pulsing markers on the **Live Now** Nepal map page, refreshed every 3 seconds.
- **How it works:** Member presses **Start sharing my location** → the browser requests location permission → the page sends GPS coords to `/api/live/update` a few times a minute → anyone on `/live` sees a pulsing amber marker with name + city + path.
- **Privacy & safety:** Opt-in only, only shown to logged-in members, stops as soon as you close the tab or press Stop. Renders only on the HTTPS public URL (browser location requires HTTPS).
- **Members-only route + self API:** `/live`, `/api/live/start`, `/api/live/update`, `/api/live/stop`, `/api/live/data`. Table: `live_sessions`.
- **Research basis:** Prospective members seeing "who else is training now, in my area and across Nepal" — the single most Strava-like feature we can ship with plain Flask + SQLite + browser geolocation.

---

## 1. Vision & Problem Discovery

*The foundation: Knowledge → Problem → Solution → Value → Product*

- **Domain / Industry:** Fitness / endurance sports / triathlon training
- **Target Audience (Who is this for?):** The local community first — runners, cyclists, and swimmers around Chitwan (including the founder) who dream of Ironman stages. Long-term: growing global. The app is free for everyone.
- **The Core Problem (What pain point are you solving?):** Aspiring Ironman athletes don't know where to start. The distances are intimidating, progress is scattered or untracked, and there's no simple free way to see which real stage they're ready for or how they compare with people around them.
- **Proposed Solution:** ChitwanFit — a free web app with two training paths: the 4 real Ironman stages (Sprint → Olympic → 70.3 → Full) for swim+bike+run athletes, and the 5 official running stages (5K → 10K → Half → Marathon → 100K) for runners. Includes workout logging (distance + time), pace & calorie tracking, progress toward the next stage, diet tips per stage, friendly leaderboards, a personal Nepal activity map, and Strava-style live location sharing.
- **Value Proposition (Why choose this over existing alternatives?):** Free, simple, stage-by-stage, beginner-friendly. Big apps are costly/complex; ChitwanFit makes the Ironman dream approachable and measured.

---

## 2. Brand Identity & Design System

*Define the visual and emotional tone before generating code or copy.*

- **Company / Product Name:** ChitwanFit
- **Tagline:** *(to finalize in Stage 4)*
- **Brand Personality / Tone of Voice:** Professional · Interactive · Outdoorsy
- **Color Palette:** Light & clean is the default theme; users can toggle to Dark & electric (both shipped).
  - Light (default):
    - Primary: `#16914a` (nature green — outdoorsy, calm, trusted)
    - Secondary: `#d97706` (warm amber accent)
    - Background: `#f7f9fc` · Surface: `#eef2f7` · Card: `#ffffff`
    - Text: `#1b2536` · Muted: `#5b6678`
  - Dark (electric):
    - Primary: `#ff6a2b` (electric orange) · Accent: `#ffd166` (gold)
    - Background: `#0b1020` · Surface: `#141b33` · Card: `#1a2240`
    - Text: `#f4f6ff` · Muted: `#9aa4c7`
- **Typography:** Classic & trustworthy
  - Heading Font: Merriweather (serif) — classic, solid, trustworthy
  - Body Font: Inter (clean, easy to read)
- **Logo:** One-horned rhino silhouette (Chitwan National Park's symbol) before the mountains and rising sun — `static/logo.svg`

### Personality → Design Traceability (why each choice)

| Brand Word | What it means | Design evidence |
|---|---|---|
| Professional | Clean, polished, trustworthy | Serif Merriweather headings, generous whitespace, one clear CTA |
| Interactive | Feels alive, responsive | Light/Dark toggle, hover lift on cards, scroll-reveal, glowing progress dots |
| Outdoorsy | Nature, stamina, openness | Green + amber palette (light theme), earthy green primary |

### Theme Toggle (interactive by design)

- Light & clean is the default (green primary `#16914a`).
- Dark & electric (orange `#ff6a2b` + gold `#ffd166`) is one click away.
- The user's choice is remembered on every page (saved in the browser).

---

## 3. Website Structure & Page Architecture

*Outline the narrative flow and layout of the public-facing website.*

- **Primary Goal / Conversion Action:** Get the athlete to log their first workout / start their journey.
- **Page Sections:**
  1. **Hero Section:** Name, rhino logo, tagline, the stages at a glance, CTA
  2. **The Stages:** Ironman (Sprint → Olympic → 70.3 → Full) + Runner (5K → 10K → Half → Marathon → 100K)
  3. **Feature Highlights:** track time, calories, Nepal map, Live Now, leaderboards
  4. **Leaderboards:** comparison for fun competition
  5. **How It Works / Product Demo:**
  6. *(Pricing — n/a, always free)*
  7. **FAQ / Objection Handling:**
  8. **Footer / Secondary CTAs:**

---

## 4. Decision Log

*Follow the cycle: Think → Ask → Evaluate → Decide → Build*

| Date | Topic / Area | Options Considered | Final Decision & Rationale | Status |
| :--- | :--- | :--- | :--- | :--- |
| 2026-09-18 | Product idea | Study-group app vs ChitwanFit (Ironman tracker) | Ironman tracker — founder's real passion; free for everyone | Done |
| 2026-09-18 | Stage model | Custom 6/12/21/42/100 km running ladder vs real Ironman stages | Real Ironman stages (Sprint → Olympic → 70.3 → Full) — accurate to the sport | Done |
| 2026-09-18 | Competition vs solo | Leaderboard vs personal tracking | Both — personal progress + friendly public leaderboards | Done |
| 2026-09-18 | Diet feature | Calorie logging vs guides & tips | Guides & tips only — no logging, keeps it simple | Done |
| 2026-09-18 | Tech stack | Static landing page vs dynamic app | Flask + SQLite dynamic app (server + database) — needed for workouts & leaderboards | Done |
| 2026-09-18 | App name | IronPath / StageUp / other | ChitwanFit | Done |
| 2026-09-18 | Founder Decision | 5-Point Filter (User, Problem, Value, Feasibility, Clarity) | Solid → proceed into Stages 2-6 | Done |
| 2026-09-18 | Nepal-First Pivot | World map vs Nepal map; one path vs two paths | Nepal-only; Ironman path + Runner path (5 official running stages); personal Nepal activity map | Done |
| 2026-09-18 | Logo | Official park logo (copyrighted) vs original Chitwan-inspired design | Original SVG: one-horned rhino + mountains + sun (`static/logo.svg`) — instantly local, no copyright issues | Done |
| 2026-09-18 | Logo rework (v2) | Round rhino badge vs mixing the real Nepal flag into the mark | Nepal-flag pennant (crimson + dark-blue border, official proportion) holding a white crescent moon, gold sun, and a cream one-horned rhino inside the lower pennant — flag + park mammal in one mark | Done |
| 2026-09-18 | "Made in Nepal" eyebrow | "Free · Made in Nepal · For every athlete" vs dropping "free" | Drop the word "free" everywhere (eyebrow, nav CTA, footer, feature card) — the app is free forever but "free" sounds cheap; say "Made in Nepal · For every athlete" instead | Done |
| 2026-09-18 | Landing sections | Sparse hero vs full trust + features layout | Added a stats trust band (real athlete/city/km/workout counts from the DB), a social-proof + trust checklist, a "features & benefits" grid, and a column footer — page now sells why to join first | Done |
| 2026-09-18 | Front-page trust band | Keep the athlete/city/km stats strip vs remove it | Removed the stats strip from `index.html` entirely (it looked "nasty" with tiny test numbers) — the hero now flows straight into the stage cards. Kept the shared `.stats-grid`/`.stat-card` CSS (the dashboard's "Your totals" still uses it) | Done |
| 2026-09-18 | Test data | Ship the demo athletes Bigya &amp; Anisha vs launch clean | Wiped both test users, their workouts, live sessions, and OTPs from `chitwanfit.db` (0 users / 0 workouts / 0 live sessions) — a fresh start for the real launch | Done |
| 2026-09-18 | OTP randomness | `random.randint` vs `secrets.randbelow` for the 6-digit code | Switched to `secrets.randbelow(1_000_000)` — same 6-digit OTP athletes type, but cryptographically unpredictable (login codes can't be guessed) | Done |
| 2026-09-18 | Live tracking | Real GPS integration vs browser-geolocation "Live Now" | Browser-geolocation Live Now (Strava-like) — members share location, others watch live on a pulsing Nepal map; no extra services | Done |

---

## 5. Notes & Prompts for OpenCode

*Use this section to draft prompt briefs, review feedback, and keep track of pending tasks.*

- [ ] Decide brand personality words, palette, typography (Stage 3)
- [x] Brand identity set: Professional · Interactive · Outdoorsy; light & clean default + dark/electric toggle; Merriweather + Inter (Stage 3)
- [ ] Draft the 8-section landing page architecture (Stage 4)
- [ ] Set up SQLite schema: users, workouts, leaderboard (Stage 5)
- [ ] Build Flask `app.py` with routes (Stage 5)
- [ ] Build landing page + dashboard pages (Stage 5)
- [ ] Add professional motion/shades/animations within the motion budget (Stage 5)
- [ ] Serve on public URL and verify (Stage 6)