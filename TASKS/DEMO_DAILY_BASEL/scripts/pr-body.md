# Summary

The development-only demo directory set (`apps/api/src/db/seed/demoDirectory.ts`) had two cases bound to the day it was seeded:
- **Full space** (`sada-space`): `capacity: 4, present: 4` — visitors checked in "within today" became stale the next day.
- **Closed today** (`radwan-study-hall`): `closedToday: true` closed the weekday it was seeded on; the next weekday it was open.

The seed returned early when the marker space (`noor-hub`) existed, so running `npm run db:seed` with `SEED_DEMO=true` on a later day changed nothing.

This change makes the seed renew these day-bound states for **today's Gaza day** on every run.

# Changes

- `apps/api/src/db/seed/demoDirectory.ts`: Added `renewDemoDirectory` function that runs when the marker space exists. It:
  1. Deletes open visits from before today (Gaza date) for spaces with `present > 0`.
  2. Counts existing open visits checked in today; inserts `present - count` new visits at `now - i seconds` (i = 0, 1, ...).
  3. Updates the `closedToday` space's hours so today's weekday is closed; other weekdays match the seed's open range. Only updates `hoursUpdatedAt` when hours actually change.
  4. Leaves photos, announcements, and all other space data unchanged.
- `apps/api/src/db/seed/demoDirectory.api.test.ts`: Added 5 renewal tests covering:
  - Day 1 → Day 2: full space reads full, closed-today space reads closed today.
  - Day 2 again: no row changed (idempotent).
  - One visit checked out on Day 2, then Day 2 again: topped up to 4.
  - Run at 20:00 Gaza time (after closing): visits checked in at `now - i seconds`, due at 23:59.
  - Demo space and outside spaces untouched.
- `docs/development/setup.md`: Added sentence documenting the renewal behavior.

# Evidence

**Tests (red → green):**
```
# Original tests (7/11 pass, 4 fail - renewal not implemented)
# After implementation: all 11 pass
PASS  |api| src/db/seed/demoDirectory.api.test.ts (11 tests | 11 passed)
```

**Break test (top-up replaced by skip → checked-out case red):**
```
× one of day 2 visits checked out, then day 2 again: topped up to 4
AssertionError: expected [ ... ] to have a length of 4 but got 3
```

**Real run (masaha_design_dev):**
```
$env:SEED_DEMO='true'; npm run db:seed
# Seeded the directory's demo set.

npm run db:seed
# The directory's demo set exists; left unchanged. (same day = idempotent)

# API live states:
# sada-space (full space): liveStatus = "FULL"
# radwan-study-hall (closed-today space): liveStatus = "CLOSED"
```

**Checks (all pass):**
- `npm run test:unit -w @masaha/api` → 872 passed
- `npm run test:api -w @masaha/api -- src/db/seed/demoDirectory.api.test.ts` → 11 passed
- `npm run lint` → 0 errors
- `npm run typecheck` → 0 errors
- `npm run format:check` → clean
- `npm run check:links` → 2678 links resolve

# Out of scope

- The demo space of `demo.ts` (untouched).
- Any API route (the seed only writes data).
- Schema/migration (no schema change).
- Web app.
- Other seeds.