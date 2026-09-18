# Feature plan — Admin Panel + Interactions Tracking

**File:** `SPECS/2026-09-18-admin-panel/plan.md`
**Branch:** `feat/admin-panel`
**Date:** 2026-09-18
**Mode:** Red/Green TDD (tests written first, then implementation to make them pass)

## Task Group 1 — Foundation (schema + event hook)

- [ ] **T1.1** Add `interactions` table to `schema.sql`:
      `id, user_id, kind, detail, created_at` + FK to users.
- [ ] **T1.2** Open the existing DB and apply the new table so current
      deployments reconcile (plain `CREATE TABLE IF NOT EXISTS` on boot).
- [ ] **T1.3** Create `tests/` skeleton with the project's existing
      test-style (pytest, `tempfile`-db fixture if pytest is in use —
      verify in `requirements.txt` first).
- [ ] **T1.4** Write FIRST failing test: recording an interaction inserts a
      row with correct `kind`.

## Task Group 2 — Record interactions (radio silence in logs of the app)

- [ ] **T2.1** Add `record_interaction(user_id, kind, detail)` helper — parameterized
      SQL only, single helper used everywhere.
- [ ] **T2.2** Hook the helper into: page view (logged-in only), OTP requested,
      login success, workout saved, leaderboard view.
- [ ] **T2.3** **Tests pass**: signup→OTP→login→save-workout records exactly one
      interaction per kind (assert counts, no duplicates).

## Task Group 3 — Admin auth + access gate

- [ ] **T3.1** `ADMIN_EMAILS` = single ownership email
      (`bishalworkspace333@gmail.com`), read from env with a safe default;
      matching is `casefold` on both sides. No plaintext duplication.
- [ ] **T3.2** `/admin` route: 403 + clear "not authorized" message for
      non-owner; renders panel for owner only.
- [ ] **T3.3** Green test: non-owner hitting `/admin` gets 403; owner gets 200.

## Task Group 4 — The admin panel UI

- [ ] **T4.1** `templates/admin.html` — professional stats grid mirroring the
      existing dashboard design tokens (no new framework).
- [ ] **T4.2** Stats: total users · logins today · OTPs requested ·
      workouts saved · interactions last 7 days (real SQL counts).
- [ ] **T4.3** Tabs: Users table, Interactions table (newest first, LIMIT 200)
- [ ] **T4.4** Owner line: "👑 Founder · Bishal Shrestha · Bharatpur-11,
      Bhojad, Chitwan" (identity from MISSION.md).

## Task Group 5 — Logging & validation polish (constitution)

- [ ] **T5.1** Logging via a decorator-style guard (`@admin_required`) so auth
      logic never mixes into the dashboard route body — per SPECS law.
- [ ] **T5.2** Full test suite green; re-run 5-Point Quality Audit on the new
      surface.

## Task Group 6 — Ship honest to GitHub

- [ ] **T6.1** Commit on `feat/admin-panel` (no secrets: verify `git ls-files`
      excludes `.db`, `secret_key.*`, `.env`).
- [ ] **T6.2** Merge to `main`, push, confirm `/admin` live returns 403 for
      anonymous (proving the gate exists) and the panel data renders for
      the owner email.

---

**Definition of done:** all tests green, admin reachable only by owner,
counts are real SQLite numbers, zero fake email, zero secrets pushed.
