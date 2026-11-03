# DEPLOY — the first public deployment (F-7), planned and built in one run, one PR

You are **worker B** in `C:\dev\masaha\app-b` (web on **5321**, API on **3321**, `masaha_b_dev` / `masaha_b_test`).
You make Masaha deployable on **Vercel + Neon** exactly as ADR 0014 decides, in **one small PR**, ready for review.
**The owner creates every account and enters every secret himself, in parallel; you have no account, no secret and no
deployment.** The PR must be ready for review by **2026-11-02 evening** at the latest: the owner merges it and goes live
before his presentation on 2026-11-03. Keep the scope tight. Model Opus, effort high.

## 0. The rules for this run

- **Do not run the `start-work-item` skill.** Read `CLAUDE.md` and `docs/development/workflow.md` yourself instead.
- **Plan, save, then build — no stop between them.** Write your plan (§4) to
  `C:\dev\masaha\workspace\WORKER_B\DEPLOY\2_PLAN.md`, then go straight on to build it in this session. This is the
  owner's explicit override of "plan saved, then stop", for the deadline (`0_OWNER_DECISIONS.md`, item 9); state it in
  the plan and the PR.
- **No stop, no question,** until the PR is open, CI is green on its head, it is `CLEAN`, the report is written and the
  final reply sent. A hard choice: decide by the safest option that keeps the decisions below, **record it** under
  *Decisions taken without the owner* (met, options, chose, why, undo), go on. One that changes a decision below or
  would need an account, a secret or a schema change is **SERIOUS**: leave that part out, keep the rest whole, list it
  first in the report.
- **Hard limits:** never merge; never push to `main`; no force-push but your own branch with a lease; no Issue; **no
  migration and no schema change**; no `vercel login`, `vercel link`, `vercel deploy` or any call to Vercel's, Neon's,
  Cloudinary's or Google's accounts; **never print, write or commit a secret** (dummy values only, generated in the
  shell and never echoed); never touch `C:\dev\masaha\app` (the owner's presentation environment), `masaha_dev`,
  `masaha_test`, ports 3320/5320, `app-review` or `app-design`; nothing on the *Not in v1* list; never weaken, skip or
  delete a test or a check; no tool attribution; no `git add -A`/`.`; never `git checkout -- <file>`, `stash` or
  `reset --hard` (restore from a backup copy); never stop for the file count.
- A refused command (the permission classifier): carry on without it, and name the exact command in the report.

## 1. Read first (closed list; search before reading more)

1. This file and `C:\dev\masaha\workspace\WORKER_B\DEPLOY\0_OWNER_DECISIONS.md`, whole.
2. `CLAUDE.md`, `docs/development/workflow.md`.
3. `docs/architecture/decisions/0014-deployment.md`; `docs/backend/conventions.md` §12; `docs/plans/foundation.md`
   *F-7*; `docs/development/setup.md`; `apps/api/.env.example`, `apps/web/.env.example`.
4. Findings **33, 46, 64** (they close here), **23, 65, 152** (they stay Open, see D9), and the findings index.
5. The code you wrap: `apps/api/src/server.ts`, `createAppFromEnv` in `apps/api/src/app.ts`, `apps/api/src/config/`,
   `apps/api/prisma.config.ts`, `apps/api/src/db/`, the seed's entry `apps/api/src/db/seed/run.ts`;
   `apps/web/index.html` (its inline theme script), `apps/web/vite.config.ts`, the web's `check:build`.
6. **Vercel's and Neon's current official documentation** (WebFetch/WebSearch), for every platform fact you rely on:
   how one project serves a Vite build and an Express function (zero-config Express or a catch-all function under
   `api/`; not the beta *Services*), monorepo/npm-workspaces installs, the Node.js 24 runtime, function region
   (`fra1`), duration and size limits, `vercel.json` `headers`/`rewrites`/`git.deploymentEnabled`, `VERCEL_ENV`,
   the client address Vercel forwards (`x-forwarded-for`, for `TRUST_PROXY`), Neon's pooled vs direct connection
   strings, Google Identity Services' CSP/COOP guidance. **Cite each URL with its check date in the plan.** Where the
   docs and ADR 0014 disagree on a fact, the docs win for the fact, ADR 0014 for the decision; record it.

## 2. The base

`git fetch origin`; `app-b` is detached at `origin/main` (`951107f4` or later), clean. `npm ci`; `npm run build -w
@masaha/shared`; `npx prisma migrate status` on `masaha_b_dev` and `masaha_b_test` (nothing pending). Docker:
`docker start masaha-postgres-1` if down. Branch: `git switch -c chore/deployment origin/main`. Finding numbers: check
the index; **213 is the next free** — 213 is yours for D3, then 214–219 for anything else you find.

## 3. The decisions (bind; the owner's, 2026-11-01)

- **D1 — One Vercel project at the repository root, one origin.** The static web (`apps/web` built with
  `NODE_ENV=production`) at `/`, with every non-`/api` path falling back to `index.html` (the SPA's routes, deep links
  and reloads); the **same Express application** as one function answering every `/api/*` path, its routes unchanged
  (`/api/v1/…`). Region `fra1`; Node.js 24 (the engines field). Choose the mechanism from the docs (§1.6), record it
  and why.
- **D2 — The thin function entry** (conventions §12): it calls `createAppFromEnv` with what a function needs and
  nothing more — **no `startJobs`** (no timer online), no `listen`, no `process.exit`, no signal handlers; the env is
  validated once per instance (an invalid env answers an error and logs it, never prints a secret); the database
  check stays the readiness route's. No module, rule or route changes. `server.ts` stays as it is.
- **D3 — The cron every 15 minutes online** (the local timer stays 5). Record **finding 213** — Neon's free compute
  hours against a 5-minute cron (the evidence is in `0_OWNER_DECISIONS.md`, item 2) — resolved in this PR by the
  interval. Update every document that says the online cron runs every 5 minutes (ADR 0014 gets a *Revised* line —
  the decision is unchanged; conventions §12's table; api-contract *Internal*), and the comment in `server.ts` if it
  then misleads (comment only).
- **D4 — Production from `main` only; no previews** (`vercel.json`, from the docs). The runbook (D8) says so and why.
- **D5 — Migrations run on production deploys only,** after the build has succeeded, with Neon's **direct**
  connection (a new variable, e.g. `DIRECT_URL`; the app keeps the **pooled** `DATABASE_URL`); a failed migration fails
  the deploy. `prisma.config.ts` and `.env.example` changed as little as possible; local and CI behaviour unchanged.
  The runbook states the rule that follows: every migration must work with the code before it (a rollback on Vercel
  never rolls the database back).
- **D6 — The web's security headers** (closes **33, 46, 64**), in `vercel.json`, on the web's pages (the API keeps
  Helmet's): a Content-Security-Policy that allows exactly what the site loads — `'self'`; the inline theme script of
  `index.html` **by its SHA-256 hash** (no `'unsafe-inline'` for scripts); Google Identity Services
  (`https://accounts.google.com/gsi/client` script; `https://accounts.google.com/gsi/` frame, connect, style);
  OpenStreetMap's tiles (`https://tile.openstreetmap.org` in `img-src`); Cloudinary (`https://res.cloudinary.com` in
  `img-src`); whatever else the build truly uses (`blob:`/`data:` for the photo resizing and previews, Leaflet's style
  attributes, the self-hosted fonts) — each source justified in the plan; plus `Cross-Origin-Opener-Policy:
  same-origin-allow-popups`, and the usual safe ones (`X-Content-Type-Options`, `Referrer-Policy`, `frame-ancestors
  'none'`, a long-cache rule for hashed assets only). **A check fails** when the hash in `vercel.json` no longer
  matches the inline script (wire it into an existing `check:*` or a unit test — not a new manual step).
- **D7 — `TRUST_PROXY` for Vercel,** settled from Vercel's docs on how the client address reaches the function, so the
  rate limits count the real visitor and a forged header cannot pick its bucket; written in the runbook and in
  security.md where the trusted proxies are described.
- **D8 — The runbook:** `docs/development/setup.md` gets *The deployment* (F-7's acceptance; one home, summarise and
  link): the production environment, **every variable** with where its value comes from (no value, ever) —
  `NODE_ENV`, `DATABASE_URL` (pooled), the direct one, `CORS_ORIGIN`, `JWT_SECRET` and `JOBS_SECRET` (new, generated
  with the documented command, never the development ones), `TRUST_PROXY`, `GOOGLE_CLIENT_ID` and
  `VITE_GOOGLE_CLIENT_ID` (read at build time: a change needs a redeploy), `EMAIL_MODE=smtp` and the Gmail SMTP set,
  `STORAGE_MODE=cloudinary` and `CLOUDINARY_URL`, `LOG_LEVEL`; then **the owner's steps in order**: import the
  repository in Vercel (root, framework, build and output as `vercel.json` sets them), the variables, the first
  deploy, the public address added to the Google client's origins and as `CORS_ORIGIN` (then redeploy), the first
  admin by `npm run db:seed` from his machine against the **direct** URL with `NODE_ENV=production` (verify the seed
  allows the admin there and refuses the demo, by reading the code — never by running it against anything but
  `masaha_b_dev`), cron-job.org every 15 minutes with the `Authorization: Bearer` header, and **the first checks**
  (D9).
- **D9 — Measured after the deployment, not here:** findings **23** (a per-address ceiling), **65** (the reset send's
  wait) and **152** (the audit's retention) stay Open; the runbook's *first checks* name how each is measured
  (and the smoke list: home, directory with map, a space's photos, register, sign in, reload, sign out, Google
  sign-in, a reset email, a photo upload, the cron's 200 with its `done` counts).
- **D10 — Native and generated parts on Linux:** prove from the lockfile and the docs that Vercel's Linux install gets
  `sharp`'s Linux binaries, `bcrypt`'s build (or prebuild) and Prisma 7's generated client with the `pg` adapter
  (no engine binary), and that the function bundle includes them; the generated client is produced by `postinstall`
  there too. A gap that only an account could prove → recorded, and named in the runbook's first checks.

## 4. The plan (`2_PLAN.md`, then build it)

Short and numbered: the facts from the docs (URLs, dates); D1–D10 each as built (files, commits); the commits in order
(Conventional Commits, subject ≤ 50, each with a body, atomic — for example: the function entry; the deploy config and
headers with its hash check; the migrations step; the cron interval and finding 213; the runbook and the findings
closed); the tests and how each is red first; the local proof (§5); *Proposed alternatives* (where you would decide
otherwise, and why — recorded, not acted on).

## 5. Tests and the local proof

- **Tests, red before their code** (copy the red line): the function entry answers a real request through the same
  app (e.g. the health route and a 404 envelope, by invoking the exported handler on a Node `http` server, in the
  lane its suffix picks), with no timer started; the CSP hash check fails on a changed inline script (break it from a
  backup copy, restore by copy, record the red line). No production code that only a test uses.
- **The production-shaped proof, locally:** the full build command `vercel.json` names, run in a clean shell with
  `NODE_ENV=production` and dummy values generated in the shell (never echoed); then serve the built web with
  **exactly the headers of `vercel.json`** (a small script outside the repo, in
  `C:\dev\masaha\workspace\WORKER_B\DEPLOY\scripts\`) in front of the API on 3321, and drive it with headless Chrome over
  CDP (the model: `C:\dev\masaha\workspace\WORKER_A\_DONE\PAYMENTS_STEP10\scripts\cdp2.mjs`, `run2.mjs`): home,
  directory with its map tiles, a space's gallery, the sign-in page with Google's button, the admin's add-space map,
  a photo picked for upload (stop before sending), Arabic and English, 390 and 1440 — **zero CSP violations in the
  console** (copy the console log), every deep link reloads to its page. Never keep an `/auth/` body; no write beyond
  what you name; `masaha_b_dev` only.
- **The complete local verification before the PR** (the owner's standing rule; memory ≥ 4 GB free per heavy run, two
  at most at once; a run killed for memory → re-run once, then in parts, until every file ran green): `npm ci`; `npm
  run build -w @masaha/shared`; `format:check`; `lint`; `typecheck`; `check:classes`; `check:links`;
  `check:conflicts`; `test:unit`; `test:component`; `test:api` (whole, on `masaha_b_test` after `migrate deploy`);
  `NODE_ENV=production npm run build` then `npm run check:build`. All green, each line recorded.
- Stop every server you started by its process id; ports 3321/5321 free; `git status --short` clean.

## 6. Push, PR, CI

- The PR number just before the push: `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq
  '.[0].number'` plus one; write it for `#PRNUM` in the documents of every commit's tree before the first push; after
  `gh pr create`, compare, and redo with a lease if it differs.
- `git push -u origin chore/deployment`; `gh pr create --assignee @me --label chore --label area:api --label area:web
  --label area:docs`, title ≤ 50 (e.g. `chore: deploy to Vercel and Neon` — recount). Description: summary; D1–D10 each
  and how it is met; the platform facts with their sources; findings closed (33, 46, 64, 213) and left Open (23, 65,
  152) with why; the CSP source by source; the local proof (console log result); the verification lines; **what the
  owner must do, in order** (pointing to the runbook); the override of item 9; decisions taken without the owner.
- `gh pr checks <n> --watch` (bounded) → green; `CLEAN`. Red → fix, fold into its commit (`--fixup` + autosquash, a
  `backup/deploy-<what>` branch first), re-run locally, push with a lease, watch again.

## 7. The report and the final reply

`C:\dev\masaha\workspace\WORKER_B\DEPLOY\4_REPORT.md`, written as you go (the plan's outcome, each commit, red/green
lines, the local proof, the verification, push/PR/CI, decisions, leftovers). Write only `2_PLAN.md`, `4_REPORT.md` and
files under `scripts\` and `shots\` in that folder, outside the repository. Scripts in files (heredocs can fail to
parse); Python writes with `newline=""`; `jq` is absent — use `gh --jq`; never `cd` into `node_modules`.

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
SERIOUS decisions: <each, one line>   (or "none")
PR: #<n> · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Mechanism: <how Vercel serves the web and the function, with its source>
Findings: closed 33, 46, 64, 213 · Open 23, 65, 152
Commits: <n> — the list in the report
Local proof: <pages × languages × widths> · CSP violations <0/n> · deep links <ok/n>
Verification (local, on <sha>): <each command with its result line>
Owner's steps: setup.md › The deployment (<n> steps)
Unproven without an account: <each, or "none">
Decisions taken without the owner: <count>, in the report
Refused commands: <command>   (or "none")
Leftovers: <branches, backups, servers>
Report: C:\dev\masaha\workspace\WORKER_B\DEPLOY\4_REPORT.md
```
