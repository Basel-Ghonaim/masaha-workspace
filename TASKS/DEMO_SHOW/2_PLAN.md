# DEMO_SHOW — plan (2026-11-02)

No branch, no commit, no repository file. Everything in this folder.

## How the data is written
- **One TypeScript script** per deliverable, run by the app's own `tsx` from `<app>/apps/api` (so it
  imports the app's Prisma client, `hashPassword`, `normaliseContact`, `chargeOf`, `gazaClock`):
  `npx tsx --conditions=@masaha/source --env-file=.env <this folder>/scripts/build-demo.ts`.
- **History is written straight through Prisma with explicit timestamps** (the services stamp `now`,
  and the audit table's `createdAt` is the database's default, so going through the running API would
  date 60 days of history tonight). Every row copies the shape its service writes, and every action
  the app audits gets the **same audit entry** (action, entity, before/after as the service builds
  them), dated when the action happened. The database's triggers stay on: the ledger checks every
  payment and void.
- **Photos only through the local API** (`POST …/photos`, multipart), by the actor the app allows:
  the admin on an unverified space, the owner on a verified one (the app refuses the admin there);
  the seed's drawn pictures removed through `DELETE …/photos/:id` first. 429 → wait and retry.
- Guards: refuses unless the database name ends in `_dev`, and refuses `NODE_ENV=production`.

## What it builds (A–D)
- The 13 live spaces (snapshot `scripts/live-spaces.json`), entered tonight (they were entered on the
  live site today), completed; 6 verified (Pal Hub + 5) with fictional owners; Pal Hub backdated
  (created 66 days ago) because it carries 60 days of history.
- Pal Hub: the seed's demo owner and reception linked; «مساحة تجريبية» soft-deleted (app's
  soft delete; its links count for nothing). Packages, ~30 customers, subscriptions in every state,
  a closure with its extension, an offer running, ~60 days of visits/check-ins/payments by both staff,
  voids, partials, uncollected, a write-off, hand-priced visits (the days before prices were
  published), data reports, capacity 40.
- ~40 users with favourites, data reports across spaces (5 open for the admin), a demo user.
- Seed's 24 spaces kept; the full one (`sada-space`, 4/4) gets a larger capacity (an owner's
  capacity edit, audited), so nothing is full.

## today.ts (E)
Deterministic idempotency keys per date, so a second run adds nothing. Fills any missing whole day
between the history and yesterday, then 5–7 people present now at Pal Hub and a few payments.

## Order
Snapshot → build on masaha_b_dev (reset+seed, API 3321) → today → headless Chrome real run (shots/b)
→ fix → backup masaha_dev → reset+seed → API 3320 → build → today → key pages (shots/dev) → stop,
clean → RUN.md, 4_REPORT.md.
