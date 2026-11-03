# DEPLOY — the report (F-7, `chore/deployment`)

> Worker B, `C:\dev\masaha\app-b`, 2026-11-01. Plan: `2_PLAN.md` (saved, then built in the same session: the owner's
> override, `0_OWNER_DECISIONS.md` item 9).

# Status

```
Status: READY FOR REVIEW
SERIOUS decisions: none
PR: #133 · head f79fdbc0 · CI green · CLEAN · files 31
Mechanism: a Vite project at the root (apps/web/dist at /, SPA fallback) + one Node function api/index.js re-exporting the API's built function.ts, every /api/* rewritten to it (vercel.com/docs/functions/runtimes/node-js; vercel-build per …/advanced-node-configuration)
Findings: closed 33, 46, 64, 213 · Open 23, 65, 152
Commits: 5 — the list in the report
Local proof: 7 pages × ar/en × 390/1440 (28 page loads) · CSP violations 0/28 · deep links 24/24 at 200
Verification (local, on f79fdbc0): npm ci 0 · build shared 0 · format:check 0 · lint 0 · typecheck 0 · check:classes 0 · check:links 0 · check:conflicts 0 · test:unit 0 · test:component 0 · test:api 1 then 0 (121 files, 1380 tests) then 1 (5 timing failures, unrelated) · build (production) 0 · check:build 0
Owner's steps: setup.md › The deployment (8 steps)
Unproven without an account: builder order; the rewrite keeping the path; bcrypt/sharp/Prisma traced into the function; Node 24.x from engines; Neon strings with pg and the Linux schema engine (channel_binding); NODE_ENV at install; Neon's compute hours
Decisions taken without the owner: 10, in the report
Refused commands: rm -rf ../shots/* (from DEPLOY\scripts)
Leftovers: branches backup/deploy-jitless, backup/deploy-late-inputs, backup/deploy-prnum; no servers; Docker's empty create-test-database.sql directory in the owner's folder; container wizardly_robinson (not mine)
Report: C:\dev\masaha\workspace\WORKER_B\DEPLOY\4_REPORT.md
```

## SERIOUS decisions

None. No decision of D1–D10 was changed; nothing needed an account, a secret or a schema change.

## 1. The plan's outcome

Built as planned (§2 of the plan), with three changes found while building:

1. **The findings 33/46/64 closed in the runbook commit**, not the headers commit: their resolution lines link to
   setup › *The deployment*, which only that commit creates (the prompt's own commit example pairs them).
2. **zod's eval probe** (found by the local proof, not in the plan): zod 4 runs `new Function('')` once, building its
   first schema, to see whether it may compile parsers; the CSP refused it and reported it on every page (105
   reports over the first run's 4 contexts, all `script-src` `eval` from the `core` chunk). zod's own source names
   the fix (`jitless` skips the probe, "strict CSPs report the caught `new Function`"). A first attempt,
   `config({ jitless: true })` as `main.tsx`'s first import, did not work: the bundler put it in the entry chunk,
   which runs after the `core` chunk where the shared schemas are built. **Built:** a second inline script in
   `index.html` sets `globalThis.__zod_globalConfig = { jitless: true }` (the global zod reads its settings from),
   hashed in the CSP like the first; `apps/web/src/app/jitlessSchemas.unit.test.ts` holds both the script and zod's
   global name; `zod` declared as the web's devDependency for that test (same `^4.6.5`, no new package in the
   lockfile). Folded into commit 2 (fixup + autosquash, `backup/deploy-jitless` first).
3. **`/health` is not public online** (D1 sends only `/api/*` to the function): the first checks read a public API
   route instead. Recorded as a proposed alternative.

## 1b. The owner's two late inputs (before the push), folded into the runbook commit

1. **Google's consent screen stays in *Testing*** (item 6, amended). The runbook never said "In production" (checked:
   no such text in setup.md); it now says, in step 5, that the screen stays in Testing (publishing needs a
   homepage and a privacy-policy address; no privacy page in v1), that online Google sign-in works only for the test
   users listed there (≤ 100), that everyone else registers by email, and to add each test user's account there;
   the `GOOGLE_CLIENT_ID` row points to it; the first checks sign in with a listed test user.
2. **`sslmode=require&channel_binding=require` in Neon's strings:** both connections accept it, so both variables
   keep Neon's strings whole. Checked:
   - **The app's pooled connection** (`pg` 8.23 via `@prisma/adapter-pg` 7.10, which passes the string to
     `pg.Pool` unchanged, `dist/index.mjs:765,776`): `pg-connection-string` 2.14 copies every query parameter into
     the config (`index.js:40-41`); `pg`'s client reads only its own `enableChannelBinding` (`client.js:87`) and
     sends only listed startup keys (`client.js:543-570`), so `channel_binding` is accepted and ignored, and SCRAM
     runs without the `-PLUS` mechanism. `sslmode=require` is treated as `verify-full`, with a `SECURITY WARNING`
     printed once (`index.js:139-150`). Run: against a throwaway PostgreSQL 18 over TLS with SCRAM, `pg.Pool` and
     `PrismaPg` both answered with `?sslmode=no-verify&channel_binding=require` (TLSv1.3), and also with
     `?channel_binding=require` on a plain connection (ignored, not enforced); `sslmode=require` refused the
     throwaway's self-signed certificate (verify-full), as it should — Neon's certificate is a public CA's.
   - **`prisma migrate deploy`** (Prisma 7.10's schema engine, tokio-postgres inside: its parameter table, with
     `channel_binding`, is in the engine binary): accepted and **enforced**. `migrate status` on `masaha_b_dev`
     (no TLS) with `?channel_binding=require` → `authentication error: server did not use channel binding`; with
     `prefer` or an unknown parameter → fine. Against the throwaway TLS server with
     `?sslmode=require&channel_binding=require` → `migrate status` connected and `migrate deploy` applied all 31
     migrations ("All migrations have been successfully applied"). That was the Windows engine; Vercel runs the
     Linux one (same Rust code, another TLS library) — named in the runbook: if the first deploy's migration fails
     with that message, remove only `&channel_binding=require` from `DIRECT_URL`.
   - The throwaway container (`masaha-cbtest`, 127.0.0.1:5499, a generated password never printed, a self-signed
     certificate) was removed with its files afterwards.

## 2. Commits

Head **`f79fdbc0`**, 5 commits on `origin/main` `951107f4`:

1. `c092ccad` feat(api): add the function entry for Vercel — `apps/api/src/function.ts`, `function.api.test.ts`,
   `api/index.js`, root `package.json` (`vercel-build`), conventions §12, security.md.
2. `70d9d87f` chore: add the deployment config and headers — `vercel.json`, `.npmrc`,
   `apps/web/scripts/contentSecurityPolicy.unit.test.ts`, `apps/web/index.html` (zod's settings script),
   `apps/web/src/app/jitlessSchemas.unit.test.ts`, `apps/web/package.json` + lockfile (`zod` devDependency).
3. `b11a1872` chore(api): migrate on production deploys — `apps/api/scripts/migrateOnDeploy.ts` + unit test,
   `vercel.json` `buildCommand`, `.env.example` comment.
4. `cdad0617` docs: run the online cron every 15 minutes — finding 213 + index, ADR 0014 *Revised*, conventions,
   api-contract, spaces.md, setup *Timed jobs*, `server.ts` comment.
5. `f79fdbc0` docs(setup): add the deployment runbook — setup › *The deployment* (with the late inputs), docs map,
   security.md, `.env.example`, foundation F-7, findings 33/46/64 resolved, 23/65/152 lines, index.

History work: two fixup+autosquash folds and two rewords (`backup/deploy-jitless`, `backup/deploy-late-inputs`
first); `#PRNUM` → `#133` in every commit's tree by `filter-branch` (`backup/deploy-prnum` first), 13 places.
31 files changed.

## 3. Tests, red and green

| Test (lane) | Red first | Green |
|---|---|---|
| `apps/api/src/function.api.test.ts` (api) | `Error: Cannot find module '/src/function.ts' imported from …/function.api.test.ts` (both tests) | 2 passed |
| — mutation: `startJobs: (run) => startEvery(300_000, run, logger)` wired in | `AssertionError: expected "setInterval" to not be called at all, but actually been called 1 times` | restored by copy, 2 passed |
| `apps/web/scripts/contentSecurityPolicy.unit.test.ts` (web unit) | `Error: ENOENT: no such file or directory, open 'C:\dev\masaha\app-b\vercel.json'` | 3 passed |
| — the prompt's break: `index.html`'s `LANGUAGES` changed to add `'fr'` (backup copy, restored by copy) | `× allows exactly index.html's inline scripts…` `AssertionError: expected [ Array(1) ] to deeply equal [ Array(1) ]` | restored, 3 passed |
| — the second inline script before its hash was in `vercel.json` | `AssertionError: vercel.json's script-src must list index.html's inline scripts as 'sha256-dy6N…' 'sha256-huEn…': expected [ Array(1) ] to deeply equal [ …(2) ]` | hash added, 27 passed (with prePaint) |
| `apps/web/src/app/jitlessSchemas.unit.test.ts` (web unit) — mutation: the setter emptied | `AssertionError: expected {} to deeply equal { jitless: true }` | restored by copy, passed |
| `apps/api/scripts/migrateOnDeploy.unit.test.ts` (api unit) | `Error: Cannot find module './migrateOnDeploy.ts'` | 5 passed |

The migration step run for real: unset → `Not a production deploy (VERCEL_ENV=unset): no migration.` exit 0;
production without `DIRECT_URL` → its message, exit 1; production with `DIRECT_URL` = `masaha_b_test` → `No pending
migrations to apply.` exit 0; an unreachable host → `Error: P1001: Can't reach database server`, exit 1.

## 4. The local proof

- **Build:** `vercel.json`'s `buildCommand` (`NODE_ENV=production npm run build && node apps/api/scripts/migrateOnDeploy.ts`)
  in `env -i` with only the OS's paths and a dummy `VITE_GOOGLE_CLIENT_ID` generated in the shell, never echoed;
  `dist`s removed first. Exit 0; the migration step skipped. `npm run vercel-build`: exit 0.
- **Served:** `scripts/serve.mjs` (outside the repo) serves `apps/web/dist` on 5321 with `vercel.json`'s headers and
  rewrites read from the file; `/api/*` to `scripts/api.mjs`, the root `api/index.js` on a plain Node server on 3321
  (`masaha_b_dev`, app-b's development `.env`, `LOG_LEVEL=warn`).
- **Driven:** `scripts/run.mjs` + `scripts/cdp.mjs` (from the model), headless Chrome, ar and en × 390 and 1440. Run 4
  (the final build and headers): **28 pages, CSP violations 0, deep-link reloads 24/24 at 200**; Google's button
  iframe drawn in all four; the directory's and the admin's map tiles loaded in all four; noor-hub's gallery
  loaded; a photo picked on space 10's editor in all four, its `POST /api/v1/admin/spaces/10/photos` failed by CDP
  before it was sent. Console errors: only those four failed POSTs (`net::ERR_BLOCKED_BY_CLIENT.Inspector`). Log:
  `scripts/run-log.txt`; shots: `shots/run4/`.
- **Earlier runs, kept as evidence:** run 1 (`shots/`): 105 eval reports, zod's probe, plus 429s on `/auth/refresh` in
  the fourth context (the proof's own refreshes from one address); run 2 (`shots/run2/`): `config()` in the entry
  chunk, still 105; run 3 (`shots/run3/`): the new build behind a `serve.mjs` started before the new hash —
  `script-src-elem` `inline` reports for the second script; servers restarted on the current files for run 4.
- **Writes:** `masaha_b_dev`'s `rate_limits` rows deleted before run 2 and before each context of runs 3–4 (the
  proof's own counters); the admin's sign-ins (sessions, refresh tokens). No photo stored, nothing else written.
  No `/auth/` body kept: no request body is logged at all.
- **Seen in the shots:** after the admin signs in, the dashboard shows in Arabic in the en contexts — the account's
  saved language wins over the browser's stored one (the app's rule, not a deployment matter).

## 5. The complete local verification (on the pushed head)

On `f79fdbc0` (`scripts/verify.sh`, `scripts/verify-log.txt`), 2026-11-02, one command at a time:

| Command | Result | Free memory at start |
|---|---|---|
| `npm ci` | exit 0 | 2.9 GB |
| `npm run build -w @masaha/shared` | exit 0 | 3.1 GB |
| `format:check` | exit 0 | 3.1 GB |
| `lint` | exit 0 | 3.1 GB |
| `typecheck` | exit 0 | 4.0 GB |
| `check:classes` | exit 0 | 4.6 GB |
| `check:links` | exit 0 (3239 links, 213 documents, 2607 source files) | 4.6 GB |
| `check:conflicts` | exit 0 | 4.5 GB |
| `test:unit` | exit 0 | 4.5 GB |
| `test:component` | exit 0 | 4.8 GB |
| `test:api` | **exit 1** — which test failed was not kept (the script logged only npm's last six lines) | 5.5 GB |
| `test:api`, re-run alone | exit 0: **121 files, 1380 tests passed** (`scripts/test-api-log.txt`) | |
| `NODE_ENV=production npm run build` | exit 0 | 4.0 GB |
| `check:build` | exit 0 | 4.2 GB |

The `npm ci`–`lint` steps started under the standing 4 GB rule (2.9–3.1 GB free); none was killed. **Unexpected,
unsolved:** the first `test:api` failure, cause unknown (no output kept; no memory kill shown). A third run went
beside CI to catch it: exit 1, **5 of 1380 failed, all timing, none in a file this PR touches** (`scripts/test-api-log-3.txt`, 1150 s against the green run's 1019 s): four `Test timed out in 5000ms` (`password.api.test.ts` › refuses the access tokens signed before it; `users.api.test.ts` › works for an account whose role is OWNER; `idle.api.test.ts` › never ends an owner's session…; `demoDirectory.api.test.ts` › day 2 again) and one countdown read a second late (`password.api.test.ts:631`, `resendInSeconds` 59 for 60). The first run's failure was most likely the same kind; CI's `test:api` on the same head passed (7m55s). **Proposed finding 214, not written:** the API lane's bcrypt-heavy tests and second-bound countdowns fail on a loaded local machine; left out of the PR so its head stays green and CLEAN — the owner decides whether to record it.

An earlier full run on 2026-11-01 (head `14fd2ecb`) was cut short by a machine restart: everything to
`test:unit` green; `test:component` exit 1 (cause not kept, the restart's moment); `test:api` interrupted. After the
restart the shared database container would not start (decision 10).

## 6. Push, PR, CI

- PR number checked just before the push: `issues?state=all&per_page=1` → 132, so **#133**; written in every
  commit's tree before the first push; `gh pr create` gave **#133** — no redo.
- `git push -u origin chore/deployment` (first push, no force). `gh pr create --assignee @me`, labels `chore`,
  `area:api`, `area:web`, `area:docs`; title `chore: deploy to Vercel and Neon` (32 characters).
  https://github.com/Basel-Ghonaim/masaha/pull/133
- **CI on `f79fdbc0`: all green** — typecheck 1m34s, format:check 56s, lint 2m34s, test:unit 1m19s,
  test:component 8m59s, test:api 7m55s, build (with check:build) 53s, check:classes 1m6s, check:conflicts 47s,
  check:links 1m9s; CodeRabbit skipping. `mergeStateStatus` **CLEAN**. The first watch ended on a dropped
  connection (`wsarecv: … forcibly closed`) while two jobs were pending; the second watch saw them pass.
- Early conflict check: no other pull request is open.

## 7. Decisions taken without the owner

Each: met · options · chose · why · undo.

1. **The mechanism (D1).** Met: how one project serves a Vite web and an Express function. Options: zero-config
   Express; the Build Output API from the build command; a Vite project plus one function in `api/`. Chose the last,
   with the root `vercel-build` building the API. Why: zero-config Express wants its entry at the root or `src/` and
   statics in `public/`; the Build Output API would drop `vercel.json`'s headers (D6 puts them there) and needs our
   own bundling of native modules; `api/` is Vercel's documented path, and `vercel-build` its documented step for
   build outputs. Undo: delete `api/` and the script, pick another mechanism.
2. **`prisma.config.ts` unchanged (D5).** Met: how migrations reach the direct URL. Options: `DIRECT_URL ??
   DATABASE_URL` in the config; the deploy script hands it in. Chose the script. Why: in the config, a `DIRECT_URL`
   left in a developer's shell or `.env` would redirect the test lane's `migrate deploy` (it only overrides
   `DATABASE_URL`) to that database. Undo: move the preference into the config.
3. **`.npmrc` `include=dev`.** Met: npm omits devDependencies under `NODE_ENV=production` (npm's documented
   default), which the owner sets on Vercel. Options: ask the owner not to set `NODE_ENV` at build (impossible:
   Vercel shares variables between build and runtime); an `installCommand` flag (does not reach the function
   builder's own install); `.npmrc`. Chose `.npmrc`. Why: covers every install; no local or CI change. Undo: delete
   the line.
4. **`NODEJS_HELPERS=0` in the variables.** Met: Vercel's helpers add `req.body`/`req.query` before Express. Chose to
   disable them. Why: the function then gets Node's own request, as `server.ts` does; Express parses itself. Undo:
   remove the variable.
5. **zod jitless by an inline script** (found by the proof). Met: zod 4's eval probe, reported by the CSP on every
   page. Options: `'unsafe-eval'` (no); accept the reports (fails "zero violations"); `config()` in app code (tried:
   runs too late, see §1); a second inline script setting `globalThis.__zod_globalConfig`. Chose the last, with a
   test holding zod's global name and `zod` as the web's devDependency for that test. Why: the only point before
   every module; zod's own source names jitless as the CSP fix. Undo: remove the script, its hash and the test.
6. **`/health` not public online.** Met: D1 routes only `/api/*` to the function. Chose D1 literally. Why: the
   decision says so; the first checks read a public API route. Undo: a rewrite `/health` → `/api`.
7. **Two extra safe headers:** `Referrer-Policy: strict-origin-when-cross-origin` (OpenStreetMap's tile policy needs
   a referrer, so not `no-referrer`) and `X-Frame-Options: DENY` beside `frame-ancestors 'none'`. No
   `Permissions-Policy` (the GIS iframe's FedCM could be restricted). Undo: edit `vercel.json`.
8. **Finding 213's estimate:** about 60 CU-hours a month from a 15-minute cron (each call keeps the compute up for
   the 5 idle minutes after it, a third of 730 hours at 0.25 CU). Recorded as an estimate; Neon's usage page is a
   first check. Undo: correct the number once measured.
9. **The test's load timeout (30 s)** for the function test: its first load transforms the whole app, which took
   more than Vitest's 5 s cold. Undo: drop the argument.
10. **The shared database container recreated** (2026-11-02, after a machine restart). Met: `masaha-postgres-1`
    would not start: it still bound `C:\dev\masaha\app\docker\postgres\create-test-database.sql`, a file #132 moved
    inline and the main folder no longer has; Docker had made an empty directory of that name there (09:50) while
    trying to mount it. Options: wait for the owner; recreate it as setup › *Running a second folder* documents
    ("the first `npm run db:up` recreates the container … the data stays in the volume"). Chose the documented
    step, from app-b, after the owner wrote "docker on now". Result: healthy, every database present
    (`masaha_dev`, `masaha_test`, `masaha_b_*`, `masaha_design_*`, `masaha_review_*`), no bind into the owner's
    folder. Not touched: the empty `create-test-database.sql` directory Docker left in `C:\dev\masaha\app\docker\postgres\`
    (the owner's folder: his to delete). Undo: none needed; the volume is the same.

## 8. Unproven without an account (in the runbook's first checks)

- Vercel runs the web's build before it traces the function (from `sortBuilders` and the install-scope chains in
  Vercel's CLI source; `vercel-build` covers the other order).
- The rewrite to `/api` keeps the request's path for Express (Vercel's guidance for one shared entry routing by
  pathname; the community's Express guide relies on it).
- The function's tracing includes bcrypt's Linux prebuild, sharp's Linux packages and Prisma's wasm query
  compiler (from `@vercel/nft`'s source); the Node.js version maps to 24.x from `engines`.
- Neon's connection strings with `pg` 8.23 (`sslmode=require`; an unknown `channel_binding` is ignored by
  `pg-connection-string`'s mapping).
- `NODE_ENV=production` in the project's variables at install, kept harmless by `.npmrc`'s `include=dev`.
- Neon's compute hours with the 15-minute cron (about 60 CU-hours estimated, finding 213).

## 9. Refused commands

- `rm -rf ../shots/*` from `C:\dev\masaha\workspace\WORKER_B\DEPLOY\scripts` (with a `docker exec … delete from
  rate_limits` before it in the same command, which therefore did not run then): refused by the safety check as an
  unresolvable glob. Not worked around: later runs wrote to `shots/run2`–`run4`; the first run's shots stay in
  `shots/` for the owner to delete if wanted.

## 10. Leftovers

- **Branches (local only, never pushed):** `backup/deploy-jitless`, `backup/deploy-late-inputs`,
  `backup/deploy-prnum` — the owner's to delete. `refs/original` from `filter-branch` removed.
- **Servers:** none; ports 3321 and 5321 free; no headless Chrome left. `git status --short` clean.
- **Docker:** `masaha-postgres-1` recreated and healthy (decision 10). The throwaway `masaha-cbtest` removed. A
  container `wizardly_robinson` (postgres:18-alpine, created 2026-11-02 09:50 local, exited) is **not mine**:
  it appeared with the restart, at the same minute as the empty directory below; left as it is.
- **In the owner's folder (not touched):** the empty directory `C:\dev\masaha\app\docker\postgres\create-test-database.sql\`
  that Docker created while trying to mount the old file.
- **Workspace files:** `scripts\` (serve.mjs, api.mjs, cdp.mjs, run.mjs, verify.sh, photo.jpg, pr-body.md, logs);
  `shots\` (run 1 at its root, then run2–run4). The function's local log (`scripts\api-log.txt`) holds request
  lines from the first two runs (cookies and the authorization header redacted by the logger; no body) — delete if
  unwanted.
- **`masaha_b_dev`:** the admin's sessions from the proof; `rate_limits` cleared during it.
- **Open questions for the owner:** Google's branding and publishing (2026-11-02, outside this PR); `/health`
  online (proposed alternative); a Neon branch for previews later.
