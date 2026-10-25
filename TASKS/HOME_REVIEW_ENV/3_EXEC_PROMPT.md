# HOME_REVIEW_ENV — a separate, temporary test environment for the owner's review of the public site

You are a worker on the Masaha repository, in a fresh session. **This is not a code task:** you write no code
into the repository, make no commit, no branch, no PR and no Issue. You build a **separate, temporary test
environment** — its own git worktree, its own database, its own ports, demo data and accounts — so the owner
can try the public site (Home, the Directory, a space's page, About) and the dashboards by hand. This file is
self-contained: every command is written here. Run commands **in PowerShell**; after each one read
`$LASTEXITCODE` (passed only if `0`). **Never print a password, a secret or a token** in your replies or logs.

**Your folder for notes:** `C:\dev\masaha\workspace\TASKS\HOME_REVIEW_ENV\` (below: `TASK\`). Write there only
`4_REPORT.md` and `logs\`. The accounts' passwords go **only** into
`C:\dev\masaha\app-review\REVIEW_ACCOUNTS.md` (inside the temporary worktree, never committed, deleted with it).

## 0. What you must never touch (two other workers are running)

- **Never** enter, edit or run anything in `C:\dev\masaha\app` (worker A), `C:\dev\masaha\app-b` (worker B) or
  `C:\dev\masaha\app-design` (reviewers read there).
- **Never** touch the databases `masaha_dev`, `masaha_test`, `masaha_b_dev`, `masaha_b_test`,
  `masaha_design_dev`, `masaha_design_test`: no write, no drop, no migrate, no seed. You may only run the two
  read-only counts of §2 step 2 and §2 step 12 on `masaha_dev` and `masaha_b_dev`.
- **Never** run `npm run db:up`, `npm run db:down`, `npm run db:reset`, `prisma migrate reset`, `prisma migrate
  dev`, `docker compose up/down`, or anything that recreates or stops the container `masaha-postgres-1` (it is
  shared by every folder). If it is stopped, `docker start masaha-postgres-1` is allowed; if Docker Desktop
  itself is not running, **stop and tell the owner**.
- **Never** use ports 3320, 3321, 3323, 5320, 5321. Yours: **API 3324, web 5324**.
- **Never** `git commit`, `git push`, `git switch`/`checkout` in any worktree, or create a branch.

## 1. Phase 1 — the environment with the existing demo data (do this now)

The repository's seed already holds realistic, varied demo data: one full demo space with its owner and
reception (`apps/api/src/db/seed/demo.ts`) and the directory's demo set — 24 spaces across the Strip's
governorates and areas, with every state the public pages show: available, busy, **full** and **closed today**
(renewed for today on every seed run since #115), stale data, unverified, without photos, a closure
announcement, prices by audience and shift (`apps/api/src/db/seed/demoDirectory.ts`). Phase 1 uses it as it is.

## 2. Phase 1 — the steps, in order (stop at the first failure, write it in the report, tell the owner)

Start `TASK\4_REPORT.md` now and add each step's result line as you go.

1. **Pre-checks:**
   ```powershell
   node -v                                   # must start with v24
   docker ps --filter name=masaha-postgres-1 --format "{{.Status}}"   # must say Up
   Test-Path C:\dev\masaha\app-review        # must be False
   Get-NetTCPConnection -LocalPort 3324,5324 -State Listen -ErrorAction SilentlyContinue   # must be empty
   Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory   # record it
   ```
   Less than 3 GB free (`FreePhysicalMemory` < 3000000) → stop and ask the owner to close spare windows.
2. **Read-only baseline of the others' data** (proof you touched nothing):
   ```powershell
   docker exec masaha-postgres-1 psql -U masaha -d masaha_dev -tAc "select count(*) from spaces"
   docker exec masaha-postgres-1 psql -U masaha -d masaha_b_dev -tAc "select count(*) from spaces"
   docker exec masaha-postgres-1 psql -U masaha -d postgres -tAc "select datname from pg_database where datname like 'masaha_review%'"
   ```
   Record both counts. The third must print nothing (if a `masaha_review_*` database exists, stop and ask).
3. **The worktree** (detached, at the latest `main`; no branch):
   ```powershell
   git -C C:\dev\masaha\app fetch origin
   git -C C:\dev\masaha\app worktree add --detach C:\dev\masaha\app-review origin/main
   git -C C:\dev\masaha\app-review log -1 --format="%h %s"
   ```
   (This adds a folder; it does not change worker A's branch or files.)
4. **Dependencies:** `cd C:\dev\masaha\app-review; npm ci` (a few minutes). Then `npm run build -w
   @masaha/shared`.
5. **The API's settings:** copy `apps\api\.env.example` to `apps\api\.env` and set exactly these (keep every
   other line as the example has it). Make each secret with `node -e
   "console.log(require('crypto').randomBytes(32).toString('base64url'))"` and each password with `node -e
   "console.log(require('crypto').randomBytes(12).toString('base64url')+'Aa1!')"`:
   - `NODE_ENV=development` · `PORT=3324` · `CORS_ORIGIN=http://localhost:5324`
   - `JWT_SECRET=<new secret>` · `JOBS_SECRET=<new secret>`
   - `DATABASE_URL=postgresql://masaha:masaha@localhost:5433/masaha_review_dev`
   - `TEST_DATABASE_URL=postgresql://masaha:masaha@localhost:5433/masaha_review_test`
   - `SEED_ADMIN_EMAIL=review-admin@example.com` · `SEED_ADMIN_PASSWORD=<new password>` · `SEED_ADMIN_NAME=مدير التجربة`
   - `SEED_DEMO=true` · `SEED_DEMO_PASSWORD=<new password>`
   - `EMAIL_MODE=log` · `STORAGE_MODE=local` (as the example)
   - `SEED_CONTACT_EMAIL` / `SEED_CONTACT_WHATSAPP` and `GOOGLE_CLIENT_ID`: leave as the example (empty is fine).
   Then check: `Select-String -Path apps\api\.env -Pattern 'masaha_dev|masaha_b_dev|masaha_test|:3320|5320'` must
   print **nothing**.
6. **The web's settings:** copy `apps\web\.env.example` to `apps\web\.env` and set `WEB_PORT=5324` and
   `API_PROXY_TARGET=http://localhost:3324`; set `VITE_CONTACT_EMAIL=contact@example.com` so About shows a
   contact; leave the rest as the example.
7. **The databases** (yours only):
   ```powershell
   docker exec masaha-postgres-1 psql -U masaha -d postgres -c "CREATE DATABASE masaha_review_dev"
   docker exec masaha-postgres-1 psql -U masaha -d postgres -c "CREATE DATABASE masaha_review_test"
   cd C:\dev\masaha\app-review\apps\api
   npx prisma migrate deploy
   npx prisma generate
   npx prisma migrate status            # must say: Database schema is up to date!
   cd C:\dev\masaha\app-review
   ```
8. **The demo data:** `npm run db:seed` (from `C:\dev\masaha\app-review`; it reads `apps\api\.env`, so it
   writes only `masaha_review_dev`; photo files go under `apps\api\.storage` of this folder). Then:
   ```powershell
   docker exec masaha-postgres-1 psql -U masaha -d masaha_review_dev -tAc "select count(*) from spaces"
   docker exec masaha-postgres-1 psql -U masaha -d masaha_review_dev -tAc "select email, role from users order by id"
   ```
   Expect about 25 spaces (24 of the set + the demo space) and the accounts of §3. Record the counts (no
   passwords).
9. **Start the two servers in the background**, each logging to a file, and save their process ids:
   ```powershell
   $api = Start-Process -FilePath npm.cmd -ArgumentList 'run','dev','-w','@masaha/api' -WorkingDirectory C:\dev\masaha\app-review -RedirectStandardOutput C:\dev\masaha\workspace\TASKS\HOME_REVIEW_ENV\logs\api.log -RedirectStandardError C:\dev\masaha\workspace\TASKS\HOME_REVIEW_ENV\logs\api.err.log -PassThru -WindowStyle Hidden
   $web = Start-Process -FilePath npm.cmd -ArgumentList 'run','dev','-w','@masaha/web' -WorkingDirectory C:\dev\masaha\app-review -RedirectStandardOutput C:\dev\masaha\workspace\TASKS\HOME_REVIEW_ENV\logs\web.log -RedirectStandardError C:\dev\masaha\workspace\TASKS\HOME_REVIEW_ENV\logs\web.err.log -PassThru -WindowStyle Hidden
   "$($api.Id) $($web.Id)" | Set-Content -Encoding ascii C:\dev\masaha\workspace\TASKS\HOME_REVIEW_ENV\logs\pids.txt
   ```
   (Create `TASK\logs\` first.) Wait until both ports listen (check `Get-NetTCPConnection -LocalPort
   3324,5324 -State Listen` every 10 s, at most 2 minutes; if not, read the `.err.log` files and stop).
10. **The regular user** (a `USER` with no space): register it through the API —
    ```powershell
    $body = @{ name = 'مستخدم التجربة'; email = 'review-user@example.com'; password = '<new password>'; language = 'ar' } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri http://localhost:3324/api/v1/auth/register -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($body))
    ```
    A 422 on the password → read `docs/backend/security.md` › *Passwords* in `C:\dev\masaha\app-review` and
    make one that meets the policy.
11. **Smoke checks** (record each status, never a token):
    - `Invoke-WebRequest http://localhost:3324/health` → 200, its body says the database is up.
    - `Invoke-WebRequest http://localhost:5324/` → 200 (the site's page).
    - `Invoke-RestMethod "http://localhost:5324/api/v1/spaces?limit=1"` → an answer with the spaces' total in
      `meta` (≈ the listed spaces of the set).
    - `POST http://localhost:3324/api/v1/auth/login` with `{ email, password }` for **each** account of §3 → 200.
      (Use `Invoke-WebRequest` and print only `StatusCode`.)
    - `GET http://localhost:5324/spaces/noor-hub` → 200.
12. **Prove the others untouched:** run step 2's two counts again; they must equal the baseline.
13. **Write `C:\dev\masaha\app-review\REVIEW_ACCOUNTS.md`** (Arabic headings are fine) with: the links
    (`http://localhost:5324/` — the site; `/sign-in`; `/dashboard`), and one row per account: its role, email,
    password, and what to try with it (§3). Then finish `TASK\4_REPORT.md` (every step's result, the counts,
    the process ids, the memory before and after; **no password**) and reply in §6's shape.

## 3. The accounts (what each is for)

| Role | Email | Password | Try |
|---|---|---|---|
| Platform admin | `review-admin@example.com` | `SEED_ADMIN_PASSWORD` | the admin dashboard: spaces, owners, users, lookups |
| Owner of the demo space | `demo-owner@example.com` | `SEED_DEMO_PASSWORD` | the owner's dashboard: profile, packages, staff, settings, the desk |
| Owner of the directory set's verified spaces | `demo-directory-owner@example.com` | `SEED_DEMO_PASSWORD` | many spaces in one owner's dashboard |
| Reception of the demo space | `demo-reception@example.com` | `SEED_DEMO_PASSWORD` | the desk as reception (fewer rights) |
| Regular user | `review-user@example.com` | the one you registered | the site signed in, the account area |

Check each email against step 8's user list; if the seed names an account differently, use the seed's.

## 4. Phase 2 — more spaces (only when the owner says "phase 2"; not now)

When the owner asks, add **150 more spaces** to `masaha_review_dev` only, for long pages and a crowded map:
1. Write a script **inside the temporary worktree** (never in `apps/api/src` tracked files):
   `C:\dev\masaha\app-review\apps\api\local\bulkSpaces.ts`. Model every insert on how
   `apps/api/src/db/seed/demoDirectory.ts` creates one space (the same tables and fields, in the same order:
   the space, its area from the existing lookups, its location inside the Strip, hours, prices, amenities,
   contacts, the owner's link, occupancy); read that file whole first.
2. **Guards in the script:** refuse to run unless `process.env.DATABASE_URL` ends with `/masaha_review_dev`;
   slugs `bulk-001` … `bulk-150`; if `bulk-001` exists, do nothing (idempotent).
3. **Variety:** spread over **every** area the lookups hold; about a third verified, a tenth unverified with
   hidden prices; capacities 4–80; some full now, some busy, some closed today, some open around the clock;
   some with no hours; a few with stale "last updated" dates; Arabic names (and English for half); prices
   from ₪3 to ₪60 an hour and some monthly; locations random but inside the Strip's bounding box used by the
   seed.
4. Run it from `C:\dev\masaha\app-review\apps\api`: `npx tsx --env-file=.env local\bulkSpaces.ts`; then the
   step-8 count (≈ 175) and step 11's smoke checks; step 12's proof again.

## 5. Teardown (only when the owner says "teardown")

```powershell
$p = (Get-Content C:\dev\masaha\workspace\TASKS\HOME_REVIEW_ENV\logs\pids.txt).Split(' ')
$p | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'app-review' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
Get-NetTCPConnection -LocalPort 3324,5324 -State Listen -ErrorAction SilentlyContinue   # must be empty
git -C C:\dev\masaha\app worktree remove --force C:\dev\masaha\app-review
docker exec masaha-postgres-1 psql -U masaha -d postgres -c "DROP DATABASE masaha_review_dev"
docker exec masaha-postgres-1 psql -U masaha -d postgres -c "DROP DATABASE masaha_review_test"
git -C C:\dev\masaha\app worktree list      # app-review gone
```
Only those two `DROP DATABASE` lines, with exactly those names. Then step 2's counts once more.

## 6. Your final reply — this shape

```
Status: READY | STOPPED
Site: http://localhost:5324/  ·  API: http://localhost:3324 (health <status>)
Worktree: C:\dev\masaha\app-review at <sha>  ·  databases: masaha_review_dev, masaha_review_test
Data: <n> spaces, <n> users (<the roles>)
Logins: <each account: 200 / failed>
Others untouched: masaha_dev spaces <before>=<after>, masaha_b_dev spaces <before>=<after>
Processes: API <pid>, web <pid> (stop: §5)
Accounts file: C:\dev\masaha\app-review\REVIEW_ACCOUNTS.md
Stopped at (if STOPPED): <the step, the exact command and its output>
Report: C:\dev\masaha\workspace\TASKS\HOME_REVIEW_ENV\4_REPORT.md
```
