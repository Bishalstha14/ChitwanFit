# Validation — Admin Panel + Interactions Tracking

**File:** `SPECS/2026-09-18-admin-panel/validation.md`
**Branch:** `feat/admin-panel`

## How we know it works (ground truth, not vibes)

### V1 — Admin gate is real
- **Command:** `curl -m 10 -s -o /dev/null -w "%{http_code}" <PUBLIC>/admin`
  while logged OUT → **expect 302 or 403** (never 200). Logged-IN as owner →
  **expect 200**. Non-owner logged-in → **403**.
- **Proves:** the gate is wired to identity, not just hidden UI.

### V2 — Counts are real numbers
- Register a throwaway user, request an OTP, log in, save one workout.
  Then in the panel, the "workouts saved" tile and "OTPs requested" tile must
  increase by exactly 1 each — read from SQLite, not mocked. **Delete the
  throwaway after the check** so the DB stays clean.

### V3 — Interactions list is newest-first
- After V2's flow the Interactions tab shows that user's events (login +
  workout) ordered `created_at DESC`, each with its `kind` label.

### V4 — No secret leaked
- Command: `git ls-files | grep -cE '\.(db|sqlite)$|secret_key|\.env$'` → **0**.
- `grep -R` of `app.py` shows only `?`-parameterized SQL in any new admin query.
  (This box: verify failure could never cause duplicate-count inflation — but
  re-confirm counts equal DB rows.)

### V5 — App still serves
- `curl <PUBLIC>/` → **200** after the whole change set is live (no branch
  killed the site).

## Manual human check (the student's eyes)
1. Open live site, sign up with a NEW email, note the dev-mode OTP banner.
2. Complete OTP → land on dashboard.
3. Visit **/admin** logged in as `bishalworkspace333@gmail.com` → panel shows
   your account's registration + today's login count. Any other email → 403.
4. Dashboard tiles change when a friend registers.

## Merge approval
A green V1–V5, a passing test suite, and zero secrets in `git ls-files`
mean the branch is merge-ready. Reviewer signs off in the commit message.
