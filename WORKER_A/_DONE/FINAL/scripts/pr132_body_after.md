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

- **Resolved (57):** 14, 17, 21, 27, 32, 48, 55, 63, 69, 73, 74, 77, 78, 79, 82, 83, 87, 89, 91, 92, 93, 94, 95, 98, 99,
  102, 103, 104, 105, 106, 120, 121, 122, 126, 127, 130, 132, 133, 134, 135, 136, 137, 138, 158, 160, 162, 163, 164,
  165, 166, 168, 171, 172, 180, 184, 204, 212 (204 and 212 in the review fixes).
- **Accepted (6):** 84, 187, 193 (the owner); 22, 112, 115 (OD1–OD3).
- **Left to the deployment (6, Open):** 23, 33, 46, 64, 65, 152.
- **Recorded by this run (2), both resolved by the review fixes:** 204 (a CSV value that reads as a formula), 212 (an
  owner on a phone cannot reach the written-off visits). The index's *Open* group holds the deployment's six only.

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

## Review fixes (2026-11-01)

Six reviews (R2, R3, R5, R14 by Claude; R1, R4 by Copilot, of which R4-F1 is taken), no blocker. Every finding the
fix round lists is fixed, **as new commits on top of `a12c0790`** (the owner's instruction: no fixup, no rebase of the
124, no force-push): 25 commits, each naming the finding it fixes, its test red before the fix.

| # | Review | Commit | Fix |
|---|---|---|---|
| 1 | R2-F1 (114 reopened) | `5e99323a` | A run is *stalled* only when a full batch (500) failed and nothing closed; one failing stay answers 200 with `failed: 1`; contract and 121's resolution say "its batch full" |
| 2 | R2-F2 | `d49d30d0` | An expired pending account is replaceable only if someone else created it (`user.created` names it), read with the footprints in one statement (`mustKeep`); security.md states it |
| 3 | R2-F3 | `4f25d33c` | The expiring-password race passes `RACE_TIMEOUT_MS` |
| 4 | R2-F4 | `c15b7b78` | A subscription's paid sum is `bigint`, `Number()` where it is mapped |
| 5 | R3-F1 (105) | `6e708e5a` | The owners page's «ربط بمساحة» is `held`, reached by the arrow keys |
| 6 | R3-F2 | `716a953f` | Finance's counted Arabic values out of `dir="ltr"`: only the amounts, the peak hour and the attendance figure |
| 7 | R3-F3 | `d569bb3a`, `7bb6d9cb` | «بدون سعر» is `#unpriced` (`UNPRICED_ID`, scroll margin), landing on its heading once it draws; the second commit types the routes test's answer |
| 8 | R3-F4, R14-F7 (204) | `be5c6db1` | `csvOf` writes a text starting `=`, `+`, `-`, `@`, tab or CR after a `'` (the owner's rule); numbers stay numbers |
| 9 | R3-F5 | `95e3ddad` | «تعديل الحقل» lands on `#report`; the notice lands on itself once it draws |
| 10 | R5-F1 (212) | `a559cfea` | For the owner, the empty «غير محصّل» keeps its header and «لن تُحصَّل» below `xl`, only its empty line hidden |
| 11 | R5-F2 (160) | `fbe04292` | `customerId: number \| null` on a `VISIT` `PresentPerson` (an answer change, no migration); the desk holds them present, their row links to the file |
| 12 | R5-F3 | `5a6c0d54` | «استلام {amount}» / «أقدم بند» take the item made first across both kinds (the file's subscriptions carry `createdAt`) |
| 13 | R5-F4 | `72e297a0` | While the file reads, the list's «⋯» holds one held, busy item alone; every item then appears in place |
| 14 | R5-F5 | `fd489782` | Each «تراجع» named «تراجع عن شطب زيارة {name} · {day}», both catalogues |
| 15 | R5-F6 | `3c3c0efd` | A reminder keeps one language: the English default names the space in English (desk file, debts list, settings preview) |
| 16 | R14-F1 (132) | `b2b0c503` | Every paged table passes `refreshing`; every paged card or row list is in `Refreshing`, the Directory's among them |
| 17 | R14-F2 (136) | `2409dfc5` | A prompt that never settles is bounded a minute from the press, the 15 s once granted; the listener removed once settled |
| 18 | R14-F3, R4-F2, R4-F3 (168) | `e870fef9` | The stored guest action runs only for its round trip: a sign-in in the tab that held it, or the one after a reset completed in this browser (the reset page's 10-minute mark); any other sign-in drops it |
| 19 | R14-F4 | `22baadc6` | The map view's search `min-w-0`, «الفلاتر» `shrink-0` |
| 20 | R14-F5 | `34e442c6` | The filters' focus waits a frame, past the shell's rule |
| 21 | R14-F6 | `11640fc7` | Screen 9's set-password link is `auth`'s `SetPasswordByEmail` in `users`' card slot: the 429 with the button held, then the link sent with the masked address and the resend's countdown |
| 22 | R14-F8 | `bf316eea` | Finding 55 states CI run 41288412120's slowest route test (794 ms vs the 3 s wait); `spaces.md`'s two "remain planned" lines dropped |
| 23 | R14-F9 | `677fb1fd` | `downloadFile` revokes the object URL a second after the click |
| 24 | R4-F1 | `427b6973` | `next` kept through the recovery — the forgot page's «متابعة», the reset card's way back, sign-in and new link — validated by `returnUrlOf` |

**The supervisor's decision (on the owner's behalf):** item 18 overrides the earlier "accept" of Copilot's R4-F2/F3,
built as the narrow rule R14-F3 proposed; the owner reviews it. The owner approved R2-F2 and the CSV rule.

**Local verification on `b2b0c503`:** `build -w @masaha/shared` 0 · `format:check` 0 · `lint` 0 · `typecheck` 0 ·
`check:classes` 0 · `check:links` 0 (3203 links) · `check:conflicts` 0 · `test:unit` 28/280 · 76/912 · 184/1181 ·
`test:component` 340 files / 2034 tests · `test:api` 120 files / 1378 tests · `NODE_ENV=production build` 0 ·
`check:build` 0 — all green (free memory 6.6–6.9 GB before each lane).

**Real run** (web 5320, API 3320, `masaha_dev`, headless Chrome): 12/12 — the map at 390 in both languages, `next`
through the recovery (read-only, no reset sent, an off-site `next` dropped), finance in Arabic, the desk at 390,
the customers' «⋯» on a 2.5 s connection, the favourites → the place filter at 1440. One write: the owner's sign-in.
No 5xx.

**CI on `b2b0c503`** (run 41309866551): build, check:classes, check:conflicts, check:links, format:check, lint,
test:api, test:component, test:unit, typecheck — all pass (CodeRabbit skipping); `CLEAN`.

**Not done in the real run:** the empty «غير محصّل» at 390 (the demo has uncollected visits; making it empty is a
write) and the favourites' own «اختر منطقتك» (the demo owner has no favourite, so near me is not offered; the same
in-app navigation was made by the history). Both are proven by component and routes tests.

