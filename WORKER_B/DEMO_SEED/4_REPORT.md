# DEMO_SEED — report

## Plan (written before the build)

**Precondition:** `gh pr view 102` → `MERGED` at `43b34cd3`. Branch `chore/directory-demo-set` from
`origin/main` (`c3391d0e`).

### Files

- `apps/api/src/db/seed/demoDirectory.ts` (new) — `seedDemoDirectory(db, input)`: the directory set, its own
  idempotent unit, gated on its marker slug (`noor-hub`), refused with `NODE_ENV=production`. Spaces, links,
  hours, shifts, prices, amenities, own amenities, contacts, settings, occupancy, present visits and one
  closure announcement in one transaction; then the photos.
- **Photos:** through the spaces module's own `createPhotosService().upload` (exported from its `index.ts`,
  which the seed — a root element — may import), with the storage port passed in. So the key layout, the
  WebP sizes, the cover-first order and the audit entries are the app's own; no new production code. Each
  image is generated in memory with `sharp` (already the API's dependency): an SVG of blocks, rendered to
  JPEG. The actor is the directory owner on a verified space, the admin on an unverified one (`can()`'s
  `adminWhileUnverifiedElseOwner`).
- `apps/api/src/db/seed/run.ts` — calls it after `seedDemo`, with a local storage at `apps/api/.storage` (the
  folder the app's local storage serves), and disconnects the API's own client the photo service reads with.
- `apps/api/src/db/seed/demoDirectory.api.test.ts` (new) — the set's proof, with a test storage.
- `docs/development/setup.md` (the demo paragraph), `apps/api/.env.example` (the demo comment).

### The data set (24 spaces; with the demo space, 25 listed — two pages at 20)

| # | Slug | Area (governorate) | V/U | Names | Case |
|---|---|---|---|---|---|
| 1 | noor-hub (marker) | Al-Rimal (Gaza) | V | ar+en | 3 photos, shifts + shift prices, student prices, phone+WhatsApp, own amenity, Fri closed, capacity, AVAILABLE by day |
| 2 | sada-space | An-Nasr (Gaza) | V | ar+en | **FULL**: open around the clock, capacity 4, 4 visitors present now |
| 3 | tal-al-hawa-desks | Tal al-Hawa (Gaza) | V | ar+en | **AVAILABLE**: open around the clock, capacity 20, 2 present; 2 photos |
| 4 | radwan-study-hall | Sheikh Radwan (Gaza) | V | ar+en | **CLOSED by hours**: today's Gaza weekday closed |
| 5 | shati-sea-view | Al-Shati (Gaza) | V | ar+en | **CLOSED by announcement**: an active closure, no end |
| 6 | daraj-corner | Al-Daraj (Gaza) | V | ar | **no hours** (hours missing) |
| 7 | zeitoun-works | Al-Zeitoun (Gaza) | V | en only | open, **no capacity** (no live state) |
| 8 | sabra-lab | Al-Sabra (Gaza) | V | ar+en | **stale groups**: hours 70 days, prices 40 days back (shown with a note) |
| 9 | tuffah-place | Al-Tuffah (Gaza) | U | ar+en | **stale prices hidden**: prices 60 days back |
| 10–24 | … | Gaza City, North Gaza, Deir al-Balah, Nuseirat, Bureij, Maghazi, Zawaida, Khan Younis, Al-Mawasi | mixed | mixed | Friday-open ones, photos on some, contacts mixed, student prices on some |

At least: 4 governorates, 15+ areas, 12 verified / 12 unverified, 8 spaces with photos, 3 English-only names.

### Tests (`demoDirectory.api.test.ts`) and their breaks

1. Creates 24 listed spaces across ≥ 2 governorates and ≥ 4 areas, inside the Strip's bounds — red before
   the code (the function missing).
2. Verified ones linked as OWNER to `demo-directory-owner@example.com`, never to `demo-owner@example.com`.
3. Each case present: stale unverified prices, photos (cover first) and none, no hours, shift and student
   prices, Friday open and closed, phone and WhatsApp, own amenities, FULL / CLOSED data, English-only names.
4. Created once: a second run returns false and changes nothing — break: the marker check removed.
5. The demo space untouched — break: the set's run edits the demo space.
6. Refused in production — break: the guard removed.

Tests 1–3 are red before the code (their own break); 4–6 each get a separate break. *(As built: the code
came first, so every test got its own break instead; see Breaks.)*

## What was built (against the plan)

As planned, with these changes made while building:

- **The set:** 24 spaces in 4 governorates and 17 areas. 13 verified, 11 unverified. 10 spaces carry
  15 photos and 14 have none. 3 names are English-only.
- **Speed:** the first version hit the 5 s test timeout (6.4 s for the first test). Without touching any
  config or timeout: the generated images are 640×400, the spaces' photos upload concurrently (each
  space's photos one after another, so the cover stays first), and hours, amenities, own amenities and
  contacts are inserted with nested `createMany`. The seeding moved into the test hooks (10 s limit). The
  set now takes about 1.4 s, plus 1.1 s for reset and seed (profiled with a throwaway test file, deleted
  after).
- **Tests:** a single `describe` "on a database holding the demo space". Its hook runs `seedDemo`, takes a
  snapshot of the demo space, then runs the set once. Tests 1–5 only read. The production test sits in its
  own `describe`.
- **The cases test** names each case. A missing case fails as `expected ['<case>'] to equal []`.

## Commits

- `chore(seed): add the directory's demo set` (41)

## Ran and passed

- Per commit: `npm run lint` and `npm run typecheck` (exit 0).
- On the head, once (5.62 GB free, no vitest of `app\` running): `npm run test:api -w @masaha/api -- src/db`
  → 8 files, 100 tests passed. No unit file changed, so `test:unit -w @masaha/api` did not apply.
- `npm run format:check` → clean. `npm run check:links` → 2565 links in 166 documents and 1641 source
  files all resolve.

## Not run locally (CI judges)

The full `test:api`, `test:unit` of the other workspaces, and `test:component`.

## COULD NOT RUN

None.

## Breaks (each from a `cp` backup of `demoDirectory.ts`, restored after; `cmp` confirmed)

Every test was written after the code, so none was seen red before its code. Each got its own break
instead:

| Break | Red test, message |
|---|---|
| the last space dropped from the creation loop | creates 24…: `expected [ …(23) ] to have a length of 24 but got 23` |
| Mawasi's space moved to Abasan (an inactive area) | creates 24…: `expected [ false, null, false, true ] to deeply equal [ false, null, true, true ]` |
| the demo owner linked as a second OWNER | links…: `expected [ Array(2) ] to deeply equal [ [ 'OWNER', …(2) ] ]` |
| Tuffah's prices 20 days back, not 60 | holds each case…: `expected [ Array(1) ] to deeply equal []` |
| the marker check made to look for another slug | changes nothing…: `promise rejected "PrismaClientKnownRequestError…" instead of resolving` |
| the set sets the demo space's capacity to 99 | leaves the demo space untouched: `expected { id: 1, slug: 'masaha-demo', … } to deeply equal …` |
| the production guard compares with another value | never runs in production: `promise resolved "true" instead of rejecting` |

The first attempts at the count and links breaks (dropping the marker space; linking the demo owner
instead) failed only in the hook: all five tests went red on a hook error, not on their own assertion.
They were redone as listed above, and each then went red on its own test alone.

## Real run (`masaha_b_dev`, API on 3321)

- `npm run db:seed` (with `SEED_DEMO=true`): "The demo space exists; left unchanged." then "Seeded the
  directory's demo set."
- Second run: "The directory's demo set exists; left unchanged." Snapshot before and after was identical: 37
  spaces, 23 users, 15 photos, 34 visits, 135 audit rows, the same latest `updated_at`, 30 files in
  `apps/api/.storage`. (`masaha_b_dev` also holds 12 older spaces from earlier runs, so it lists 37. A fresh
  database lists 25.)
- `GET /api/v1/spaces` → page 1: 20 rows, `totalPages: 2`. Page 2: the rest. Covers on the set's spaces that
  have photos.
- `GET …/spaces/:slug/occupancy`: sada-space `FULL`, tal-al-hawa-desks `AVAILABLE`, radwan-study-hall
  `CLOSED` (by hours), shati-sea-view `CLOSED` (closure), daraj-corner `null` (no hours), zeitoun-works
  `null` (no capacity), tuffah-place `null` (unverified), noor-hub `AVAILABLE` (17:16 Gaza, a Wednesday).
- `GET /spaces/tuffah-place`: `prices: null`, `staleGroups: ["prices"]`, unverified. `sabra-lab`: prices
  shown, `staleGroups: ["hours","prices"]`. `noor-hub`: 3 photos, shift and student prices, WhatsApp,
  phone, Instagram, platform and own amenities.
- Photos served: the cover's `card.webp` → 200 `image/webp`, and its `page.webp` → 200 `image/webp`.
- `?openFriday=true` → 16. `?studentPrices=true` → 10, without tuffah-place (its stale prices are left out
  of the filter).
- The API was stopped by PID (3 processes) and port 3321 is free.

## Departures

1. **"Some names with Arabic only"** cannot be built: the schema requires `nameEn` and makes `nameAr`
   optional, and a schema change is out of scope. The set has 3 English-only names instead.
2. **The test file** is a new sibling, `demoDirectory.api.test.ts`, next to the existing
   `demo.api.test.ts`. The set has its own function, `seedDemoDirectory` in `demoDirectory.ts`, called by
   `run.ts` after `seedDemo`.
3. **`demo.ts`** gains one word: its existing `gazaClock` is exported for the set's dates.
4. **`run.ts`** imports `LOCAL_FILES_URL` from `app.ts` (root to root, as `test/storage.ts` does). It
   computes `apps/api/.storage` itself, because `app.ts`'s `LOCAL_STORAGE_ROOT` is not exported and
   changing `app.ts` is outside the seed. It also disconnects the API's singleton client, which the photo
   service reads through.
5. **Photos are local only.** With `STORAGE_MODE=cloudinary` in a development `.env`, the API would not
   serve the seeded files. `setup.md` says they need the default `STORAGE_MODE=local`.
6. **Live states move with the clock.** "Present now" visits are checked in within today, and
   "closed today" is the Gaza weekday of the run. A day later, the closed-by-hours space opens and the
   auto check-out may close the visits. The seed is not re-run on an existing set, so after a day `FULL`
   needs a fresh database (`db:reset`). The closure (no end) and the around-the-clock hours do not expire.
