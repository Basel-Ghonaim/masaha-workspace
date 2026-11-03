## Summary

The project's last build mission, in one PR: **every one of the 32 screens of Masaha v1 complete**, the owner's audit
log (O13) included, and **every open finding closed** — 55 built, 12 accepted in all (6 in this PR), 6 left to the
deployment by the owner's F1. Web, API, shared and documents together (F2). Built by a lead with sub-agents on eight
lanes, joined into one branch with no merge commit.

- **124 commits**, two migrations (M1, M2), one new domain error code, three new routes, three new timed jobs.
- The plan: `WORKER_A\FINAL\2_PLAN.md` (approved by the supervisor on the owner's behalf, 2026-10-29). The run's full
  record: `WORKER_A\FINAL\4_REPORT_LEAD.md`.

## The units

- **U0 — the foundation** (6 commits): the error envelope's `details` (83); `PUBLISHED_PRICE_CHANGED` (171); the
  dashboard's navigation grouped by task with the data reports' counts (165, 14's place); the skip link and the focus
  rule in every shell (130, carried 1); the account on a phone (DI-10, SH-005, P4); the routes of every screen to come.
- **U1 — the API of identity** (17): the replay's successor (21), the sweeps (17), Google's `created` (32), an expired
  pending account's address freed (91, S1), the reset link printed (AC-021), `hasPassword`/`hasGoogle`, `ALREADY_OWNER`'s
  owner (83), the exact email (89), one status schema (158), the staff fixes (92, 93, 106), the tests of 69, 77, 78, 79.
- **U2 — the API of the desk and the money** (15): M1 and M2, Gaza's transitions (120), the dated check-ins (127), the
  stalled job (121), the reclamation job (63), a phone under either code (126), a visit for its customer (160), the
  changed price refused (171), who recorded and voided (162), the written-off visits (164), the published period, the
  reminder in the file, the desk's richer reads, one report by id, the retired amenities (99).
- **U3 — the layer and shared web** (10): `Meter`, `BarChart`, `Heatmap`, `Refreshing`, the held menu item (105),
  `Input size="lg"`, the lists' range and steps, the page asked marked (132), no scroll jump (carried 11), one digit
  reader (103), shared row triggers (104), CSV and WhatsApp helpers.
- **U4 — the build and tooling** (5): the site's `public` entries (180), the acyclic dashboard chunk (27), the lazy
  shells warmed before tests wait (55, 87), the test database's script inline (48), the documents' size guide (98).
- **U5 — the owner's screens** (11): the owner's and the admin's overviews (12, 25), finance (19), staff's month and
  start, the settings' account card, Packages' desk words, the packages' live region (102), the staff fixes (105, 106).
- **U6 — the admin's screens** (17): both audit logs (14 / O13, 31), the platform settings (32) and the site's contact
  from the API, the spaces list and editor, owners and users (83, 89, 94, 95, 158), the report notice and deep links
  (184), the handler filter, the lookups' positions and switches, the retired amenities (99), the upload bar (73, 74).
- **U7 — the front desk** (14): the day's log, the written-off visits with their undo (164), the customer's visit
  (160), the price the sheet showed (171), the write-off's focus (172), the phone's order, the names and kinds, renew
  from the desk, the full space by count, the rates, the phone's file, the refused payment, the usage subscriber's due,
  the subscription sheet.
- **U8 — customers, the file, payments** (7): a customer's actions by state, the WhatsApp reminder, who recorded and
  voided (162), the subscription's corrections (163), monthly and weekly, the list and file gaps, the other owners in
  the ledger (166).
- **U9 — the public site and the account** (16): «إعدادات حسابي» (screen 9), Google's welcome (32), `next` and the way
  back, the password's fourth rule, a guest's action through a reset (168), the carried fixes (Home, About, the
  Directory, the space page), the map's marks in dark (135), near me (136), the area cap (133), the marks memoised (134),
  Home's counts (137), the stale status (138), the error states, favourites, the users folders (82).
- **U10 — the closing documents** (4): every step of `v1-mvp.md` and every screen recorded as built, the accepted
  findings, the placeholder page removed, the findings index moved once (S2, OD9).

## The migrations (read the SQL — F3)

- **M1** `apps/api/prisma/migrations/20261029144213_subscription_usage_bigint/` — `subscription_usage` dropped and
  created again with `due_agorot bigint` (finding 122), the plan's §5.2.M SQL exactly.
- **M2** `apps/api/prisma/migrations/20261029154841_subscription_published_period/` — `subscriptions.published_period
  "PricePeriod"` and `CHECK (published_period IS NULL OR (published_period IN ('WEEK','MONTH') AND package_id IS NULL))`.

## The new error code (the Arabic needs the owner's approval)

`PUBLISHED_PRICE_CHANGED` (409) — en "This price changed since the sheet opened. Check the new amount, then confirm."
· ar «تغيّر هذا السعر منذ فتحت النافذة. راجع المبلغ الجديد، ثم أكّد.»

## Findings

- **Resolved (55):** 14, 17, 21, 27, 32, 48, 55, 63, 69, 73, 74, 77, 78, 79, 82, 83, 87, 89, 91, 92, 93, 94, 95, 98, 99,
  102, 103, 104, 105, 106, 120, 121, 122, 126, 127, 130, 132, 133, 134, 135, 136, 137, 138, 158, 160, 162, 163, 164,
  165, 166, 168, 171, 172, 180, 184.
- **Accepted (6):** 84, 187, 193 (the owner); 22, 112, 115 (OD1–OD3).
- **Left to the deployment (6, Open):** 23, 33, 46, 64, 65, 152.
- **Recorded by this run, Open (2):** 204 (a CSV value that reads as a formula), 212 (an owner on a phone cannot reach
  the written-off visits).

## Local verification (on `a12c0790`)

- `npm ci` 0 · `npm run build -w @masaha/shared` 0 · `format:check` 0 · `lint` 0 · `typecheck` 0 · `check:classes` 0 ·
  `check:links` 0 (3198 links) · `check:conflicts` 0
- `test:unit` shared 28 / 280 · api 76 / 912 · web 184 / 1172 — all green
- `test:component` (whole) 339 files / 2006 tests — green
- `test:api` (whole, `masaha_test` after `migrate deploy`) — 120 files / 1374 tests, green
- `NODE_ENV=production npm run build` 0 · `check:build` 0 · design `check-parse` 0, `check-classes` 0
- First download: head 1,158,388 bytes (7 chunks); no leaflet, data-table or dashboard chunk in it (the base was not
  rebuilt for a comparison: the machine's memory).

## The real run

M1 and M2 applied to `masaha_dev`; the API (3320) and the web (5320) run; headless Chrome toured every screen by
every role, English in dark at 1440 and 390 (and 768 where a layout changes), Arabic in light at 1440: **guest 8/8,
reception 6/6, owner 15/15, admin 9/9** (one more check aimed at a section's accessible name, which its component test
proves). The sidebar's groups, the overview's no-amount rule, reception's 403s on finance and the audit log checked.
No 5xx; no write. The write cases of the plan's §11 were not performed (each behaviour is proven by its component and
API tests); named in the report.

## ⚠ One step for the owner after the merge — the database container

This PR replaces the container's bind-mounted init script by an inline Compose config (finding 48). A container made
from the old `docker-compose.yml` still mounts `docker/postgres/create-test-database.sql`, which this PR deletes, so it
will not start from a folder at this branch. **Run `npm run db:up` once after the merge:** it recreates
`masaha-postgres-1` from the new configuration, its volume and every database kept (`setup.md` › *Running a second
folder*). Until then the lead's folder keeps `main`'s copy of the file, untracked.

## Decisions taken without the owner

None SERIOUS in the lead's sense. In the report, under *Decisions taken without the owner*, and in each lane's report
(`scripts\lane-*\REPORT.md`). The ones the owner may most want to see: LEAD-D2 (lane L started early), LEAD-D4 (the
lead's grant first), LEAD-D5 (the first page told apart per router history), LEAD-D6 (W1's two marked SERIOUS,
accepted), LEAD-D7 and LEAD-D10 (findings 206 and 210 fixed in this PR instead of recorded), LEAD-D11 (the index commit
last), LEAD-D12 (the container's one-time recreation left to the owner), and the lead's slip (one `git checkout --` on its own regenerated file, nothing lost).

## Left out

Nothing of the plan. Of the real run, the cases this run did not perform are named in the report with why.
