# DEMO_DAILY_BASEL — Report

## Status
DONE — PR #115 opened, CI green, worktree left at origin/main clean.

## Summary
Implemented renewal of the demo directory's day-bound states so that `npm run db:seed` with `SEED_DEMO=true` renews the full space and closed-today space for today's Gaza day on every run.

## Changes
- `apps/api/src/db/seed/demoDirectory.ts`: Added `renewDemoDirectory` function.
- `apps/api/src/db/seed/demoDirectory.api.test.ts`: Added 5 renewal tests.
- `docs/development/setup.md`: Added documentation sentence.

## Commits
- `d2f4143e` chore(seed): renew the demo directory's day each run (72 chars)

## Test Results

### Red → Green (test file only)
```
# Before implementation (4 renewal tests fail):
× day 1 then day 2: sada-space full and radwan-study-hall closed on day 2 weekday
× day 2 again: no row changed (counts and hoursUpdatedAt unchanged)
× one of day 2 visits checked out, then day 2 again: topped up to 4
× run at 20:00 Gaza time (after closing for radwan): visits checked in at now - i seconds

# After implementation (all 11 pass):
PASS  |api| src/db/seed/demoDirectory.api.test.ts (11 tests | 11 passed)
```

### Break Test (top-up replaced by skip)
```
× one of day 2 visits checked out, then day 2 again: topped up to 4
AssertionError: expected [ ... ] to have a length of 4 but got 3
```
Restored correct implementation → passes.

### Full Test Suite
- `npm run test:unit -w @masaha/api` → 872 passed
- `npm run test:api -w @masaha/api -- src/db/seed/demoDirectory.api.test.ts` → 11 passed
- `npm run lint` → 0 errors
- `npm run typecheck` → 0 errors
- `npm run format:check` → clean
- `npm run check:links` → 2678 links resolve

## Real Run (masaha_design_dev)
```
$env:SEED_DEMO='true'; npm run db:seed
# Seeded the directory's demo set.

npm run db:seed
# The directory's demo set exists; left unchanged. (same day = idempotent)

# API live states (GET /api/v1/spaces?limit=50):
# sada-space (slug: sada-space, full space): liveStatus = "FULL"
# radwan-study-hall (slug: radwan-study-hall, closed-today space): liveStatus = "CLOSED"
```

## Conflicts with Open PRs
- PR #114 (head 8ae243f0): clean merge

## Worktree State
`app-design` left at `origin/main` detached and clean (no uncommitted changes).

## Report Location
C:\dev\masaha\workspace\TASKS\DEMO_DAILY_BASEL\4_REPORT.md