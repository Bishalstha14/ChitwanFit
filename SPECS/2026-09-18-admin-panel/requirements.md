# Feature: Admin Panel + Interactions Tracking

**File:** `SPECS/2026-09-18-admin-panel/requirements.md`
**Branch:** `feat/admin-panel`
**Drafted:** 2026-09-18
**Owner (admin account):** `bishalworkspace333@gmail.com`
**Founder identity for admin UI:** Bishal Shrestha · Bharatpur-11, Bhojad, Chitwan

---

## 1. Why this feature exists

ChitwanFit is being brought to market. Its founder (you) wants to *see the
store is open*: how many athletes register, how often they log in, and how
they actually use the site (which tabs, how many workouts, which OTP stage).
Right now the founder has zero visibility — there is no admin view at all.

This feature adds:

1. A **login-style admin** you can reach with your founder email.
2. A **dashboard** showing thing-flow: registered users, logins, OTP
   requests, workouts logged, and per-tab interactions.
3. A lawful, **parameterized-SQL**, **beginner-friendly** implementation
   (no ORM, no new dependencies, plain SQLite — same stack as the app).

## 2. Scope — in

- Admin identity = the single founder email above (hard-coded owner; no
  separate admin signup — keep it simple).
- App-wide **interactions log**: one row per meaningful user action
  (page view, OTP requested, login success, workout saved).
- **Admin dashboard page** (`/admin`) reachable only when logged in as the
  founder email; shows today's + total counts with a small stats grid.
- A polished **email+OTP** login experience (kept from the working dev-flow,
  shown honestly in dev mode with a visible banner — never a faked email).
- Everything stored via parameterized SQL with a plain schema (one new table
  `interactions` + a tiny `maintenance`/`admin` marker), no migrations tooling.

## 3. Out of scope (explicitly, so nobody gets surprised)

- 🔒 **No fabricated credentials.** Real Gmail sending needs an App Password
  only you can create (`.env`). Until then the app prints OTP codes in a
  loud, obviously-dev banner — it never pretends an email was sent.
- No per-user roles/teams, no admin CRUD of other users yet (next stage if
  you want it).
- No real "social login" (that needs a Google Cloud OAuth client I cannot
  create for you). The professional login here is the polished email+OTP.
- No payments, no ORMs, no async jobs, no third-party analytics SDK.

## 4. Acceptance criteria (how you will know it works)

- **A1 (admin reachable):** logging in as `bishalworkspace333@gmail.com`
  lets you open `/admin` and see the panel. Any other account gets a clear
  "not authorized" message.
- **A2 (God's-eye count):** the panel shows (a) total registered users,
  (b) logins today, (c) OTPs requested, (d) workouts logged — as real
  numbers from SQLite, not mocked.
- **A3 (interactions):** after visiting 3+ pages and saving one workout,
  the panel's per-tab list shows those events, newest first.
- **A4 (safe auth):** all new queries are parameterized (`?` placeholders);
  the founder email comparison doesn't leak into plaintext anywhere.
- **A5 (no secrets):** `git ls-files` shows NO `secret_key.txt`, no `.db`,
  no `.env` — the same secret-safe discipline the launch already has.

## 5. Simplifications proposed (per the repo constitution)

- Track `views`/`otp_requested`/`login_ok`/`workout_saved` as a single
  `interactions` table with one `kind` column — one rule, not four.
- Admin owner as a module constant read from an env var with a safe default
  (`CHITWANFIT_ADMIN_EMAIL`), so it's one line to change later — not a fork.
- Keep the OTP dev-mode banner (already built) and layer the admin panel on
  top; no new auth system is invented.
