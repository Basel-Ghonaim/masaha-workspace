Approved by the owner, 2026-10-24.

> **The supervisor's corrections (2026-10-24) — binding; they win where the plan below differs:**
> 1. **Top up, do not skip.** For each space with `present > 0`: delete its open visits checked in **before**
>    today's Gaza date; count its open visits checked in today; insert `present − count` (none when ≥ present).
>    "Any visit today → skip" leaves a space short when one of today's visits was checked out (a real run, the
>    auto check-out). A second run the same day then inserts nothing — still idempotent.
> 2. **The check-in time survives the auto check-out.** Not a random time from midnight: the `i`-th inserted
>    visit is checked in at `now − i seconds` (i = 0, 1, …). A check-in before the space's closing is due at that
>    closing (still ahead); one after the closing, or on a closed day, is due at 23:59 (`spaces/autoCheckout.ts`;
>    data model › *Auto check-out*), so the space stays as seeded until the day ends whatever the hour of the
>    run. Check first that the set's spaces have no `maxStayMinutes` setting that would close them sooner; if one
>    has, stop and report.
> 3. **The closed-today space writes only when it must.** If today's weekday row is already closed and the other
>    six match the seed's own `open` range (read from its `SpaceSeed`, not hard-coded 09:00–17:00), write nothing
>    and leave `hoursUpdatedAt` as it is; otherwise update the rows and set `hoursUpdatedAt = now`. A same-day
>    second run then changes no column.
> 4. **Deleting open visits:** check first (`schema.prisma`) that no table references a visit with a foreign key
>    an open visit could have rows in (payments are made at or after a check-out, so an open visit has none);
>    if one does, stop and report. Delete only the set's spaces' **open** visits from earlier days; closed visits
>    stay.
> 5. **The tests** (the seed's existing `now` input; no new parameter): day 1 then day 2 → `sada-space` full and
>    `radwan-study-hall` closed on day 2's weekday; day 2 again → no row changed (counts, and `hoursUpdatedAt`
>    unchanged); **one of day 2's visits checked out, then day 2 again → topped up to 4**; **a run at 20:00 Gaza
>    time (after closing) → the visits are due at 23:59** (`autoCheckoutDue` on one of them, or the occupancy read
>    at 20:05 still full); the demo space of `demo.ts` and a space outside the set untouched (their visit counts
>    before and after). Each test seen red before its code; one break: the top-up replaced by the skip → the
>    checked-out case red.
> 6. **Use the existing helpers** (`gazaClock` in `demo.ts`, already imported by the set; `gazaClockOf` in
>    `@masaha/shared`) — no new date code.

## Problem

`seedDemoDirectory` returns early when its marker space (`noor-hub`) exists, so the two day-bound cases never update:
- **Full space** (`sada-space`, line 133): `capacity: 4, present: 4` — visitors checked in "within today" become stale the next day.
- **Closed today** (`radwan-study-hall`, line 168): `closedToday: true` closes the weekday it was seeded on; the next weekday it is open.

## Goal

When the set already exists, `npm run db:seed` with `SEED_DEMO=true` renews these states for **today's Gaza day**:
- Every space with `present > 0` gets exactly `present` open visits checked in today.
- The `closedToday` space is closed today (its `SpaceHours` row for today's weekday has `isClosed: true`).
- Idempotent within a day: a second run the same day changes nothing.
- Nothing else changes: names, prices, photos, contacts, `profileUpdatedAt`, `hoursUpdatedAt` (except the closed-today space), `pricesUpdatedAt`, `amenitiesUpdatedAt`, `contactsUpdatedAt` stay as they are.
- Still refuses to run in production.

## How the renewal finds the set and what it writes

### Finding the set
The set's spaces are exactly the 24 slugs in `DIRECTORY_SPACES`. The marker `noor-hub` proves the set exists. On renewal we:
1. Load all spaces where `slug IN (DIRECTORY_SPACES.map(s => s.slug))`.
2. For each, get its `SpaceSeed` definition from `DIRECTORY_SPACES` (by slug).

### Rows written (by table)

| Table | Action | Details |
|-------|--------|---------|
| `Visit` | **Delete** old open visits (`checkedOutAt: null`) for spaces with `present > 0`. | These are demo visits from earlier days; the auto-checkout job closes them at the space's closing time or 23:59. Leaving them would distort today's `present` count (rule 6). |
| `Visit` | **Insert** `present` new visits per space, checked in **today**. | `checkedInAt` = random time between start of today (Gaza midnight) and `now`. `idempotencyKey` = new UUID. Rates copied from the space's prices (`hourRateAgorot`, `dayRateAgorot`). |
| `SpaceHours` | **Update** the `closedToday` space (`radwan-study-hall`) only. | For today's weekday: set `isClosed = true`, `opensMinute = null`, `closesMinute = null`. For the other 6 weekdays: ensure they match the seed's `open` range (they already do; no-op). Update `hoursUpdatedAt` on the space to `now`. |
| `Announcement` | **No change**. | The closure announcement (idempotencyKey) is left as-is (#112). |

### Idempotency within a day
Before renewing a space with `present > 0`, check its existing open visits:
- If **any** open visit has `checkedInAt` on **today's Gaza date** (same calendar day as `now` in Asia/Gaza), the space is already renewed today → skip it entirely (no delete, no insert).
- This works because the seed creates visits with `checkedInAt` within today, and the auto-checkout job never back-dates `checkedInAt`.

### Rule 6 — old visits from earlier days
**Delete them.** They are open visits (`checkedOutAt: null`) from previous seed runs. The auto-checkout job closes them at the space's closing time or 23:59, but a seed run after closing would leave visits that get closed at once. They would also inflate `present` (open visits count as present). The set's visits are demo data in a development database only; removing them is correct.

### The `closedToday` space renewal
- Space: `radwan-study-hall` (the only one with `hours.closedToday === true`).
- Compute today's Gaza weekday: `gazaClock(now).date(0).getUTCDay()` (0 = Sunday … 6 = Saturday).
- Update its 7 `SpaceHours` rows: the row for today → `isClosed: true`; the other 6 → `isClosed: false`, `opensMinute: 540` (09:00), `closesMinute: 1020` (17:00).
- Set `space.hoursUpdatedAt = now`.

## Commits

1. `chore(seed): renew the demo directory's day each run` (49 chars)
   - Modify `seedDemoDirectory` to renew when the marker exists.
   - Add the renewal test in `demoDirectory.api.test.ts`.
   - Update `docs/development/setup.md` with one sentence.

## Files changed

1. `apps/api/src/db/seed/demoDirectory.ts` — core renewal logic.
2. `apps/api/src/db/seed/demoDirectory.api.test.ts` — new test for renewal across days.
3. `docs/development/setup.md` — one sentence added to the demo data section.

## Test (in `demoDirectory.api.test.ts`)

Add a test in a new `describe` block:
- Seed with `now = day 1` (Wednesday, 2026-10-14).
- Seed again with `now = day 2` (Thursday, 2026-10-15).
- Assert through the public reads (`setSpaces()`):
  - `sada-space` reads `visits.length === 4` and `occupancy.capacity === 4` → **full**.
  - `radwan-study-hall` reads `hours.some(day => day.dayOfWeek === 4 && day.isClosed)` → **closed today** (Thursday = 4).
- Third run with `now = day 2` again → counts unchanged (idempotent).

## Setup.md sentence

Add after the paragraph describing the demo set (line 110):
> "Running the seed again on another day renews the set's day-bound states: spaces with present visitors receive today's visitors, and the space marked closed today is closed for the current weekday."