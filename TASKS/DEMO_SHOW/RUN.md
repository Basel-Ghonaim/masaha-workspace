# DEMO_SHOW — how to run the demo

## 1. What was done tonight (2026-11-02)

1. `masaha_dev` backed up: `scripts\masaha_dev_before.dump` (pg_dump `-Fc`, 218 KB).
2. Reset and seeded with the demo data (`prisma migrate reset`, then `SEED_DEMO=true prisma db seed`).
3. The API on 3320, then `scripts\build-demo.ts` (data, then photos through the API), then `scripts\today.ts`.
4. Checked in Chrome on 5320 (`shots\dev\`). Servers stopped. Nothing in the repository changed.

## 2. Tomorrow morning

Start Docker Desktop if it isn't running (the database is the `masaha-postgres-1` container). Then, in **two
PowerShell windows** in `C:\dev\masaha\app`:

```powershell
npm run dev -w @masaha/api      # window 1: the API on http://localhost:3320
npm run dev                     # window 2: the site on http://localhost:5320
```

Then **the one command**, in a third window, also in `C:\dev\masaha\app`, with the API running:

```powershell
Push-Location apps\api; npx tsx --conditions=@masaha/source --env-file=.env C:\dev\masaha\workspace\TASKS\DEMO_SHOW\scripts\today.ts; Pop-Location
```

It takes a few seconds. You can run it again any time: a second run adds nothing. It:

- closes last night's open stays at closing time, the way the app's auto check-out does;
- fills yesterday (Nov 2) as a full day;
- puts 5 to 7 people at Pal Hub now (visitors and subscribers);
- after 10:30 or so, adds visitors who came and left this morning, with their payments.

Run it **during Pal Hub's hours** (Saturday to Thursday 08:00–22:00; Friday 12:00–20:00), ideally after
08:30. Before opening or after closing, the app's own auto check-out closes the stays.

## 3. Accounts (password: "the demo password", the `SEED_DEMO_PASSWORD` in `apps/api/.env`)

| Role | Email | Pages to show |
|---|---|---|
| Admin (your own) | the `SEED_ADMIN_EMAIL` in `.env`, with its own password | Overview · Spaces · Owners · Users · Data reports (7 open) · Audit log |
| Owner of Pal Hub — أحمد الشوا | `demo-owner@example.com` | Overview · Front desk · Customers → سارة خالد · Payments · Finance (October; November) · Packages · Announcements · Data reports · Staff · Audit log |
| Reception at Pal Hub — ليلى النجار | `demo-reception@example.com` | Front desk (people present, uncollected visits) · My payments today |
| User — سلمى الأغا | `demo-user@example.com` | Favourites (5) · My reports (pending, resolved, dismissed) |

Public pages to show without signing in: Home, Spaces (list, and the map), `/spaces/pal-hub`,
`/spaces/branch-hub`, `/spaces/masahat`.

The other owner accounts (Elevate, Branch, Number One, Focus, Garden) and `demo-directory-owner@example.com`
use the same demo password. Reception's session ends after 15 minutes idle, so sign in again if needed.

**Note:** the map's legend lists «ممتلئ» as one of its four keys. That comes from the app's code, not the data:
no space is full.

## 4. Rebuild from scratch (only if something goes wrong)

API stopped, in `C:\dev\masaha\app\apps\api`:

```powershell
npx prisma migrate reset --force          # Prisma asks for your consent when an AI runs it; you can just run it yourself
$env:SEED_DEMO = 'true'; npx prisma db seed; Remove-Item Env:SEED_DEMO
```

Then start the API (`npm run dev -w @masaha/api` from `C:\dev\masaha\app`), and from `apps\api`:

```powershell
Remove-Item C:\dev\masaha\workspace\TASKS\DEMO_SHOW\scripts\photos-done-masaha_dev.json -ErrorAction SilentlyContinue
npx tsx --conditions=@masaha/source --env-file=.env C:\dev\masaha\workspace\TASKS\DEMO_SHOW\scripts\build-demo.ts
npx tsx --conditions=@masaha/source --env-file=.env C:\dev\masaha\workspace\TASKS\DEMO_SHOW\scripts\today.ts
```

`build-demo` takes about a minute. It refuses anything but a `*_dev` database on localhost, refuses
`NODE_ENV=production`, and refuses to run twice on the same seeding.

To put back what `masaha_dev` held before tonight (API stopped), from this folder:

```powershell
docker cp scripts\masaha_dev_before.dump masaha-postgres-1:/tmp/before.dump
docker exec masaha-postgres-1 pg_restore -U masaha -d masaha_dev --clean --if-exists /tmp/before.dump
```
