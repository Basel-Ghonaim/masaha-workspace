## Summary

F-7: Masaha becomes deployable on **Vercel + Neon**, exactly as ADR 0014 decides: one Vercel project at the repository root, one origin — the web at `/`, the same Express app as one function answering every `/api/*` path — in Frankfurt, production from `main` only. No account, secret or deployment is part of this PR: the owner creates them, following the runbook, [setup › The deployment](docs/development/setup.md#the-deployment).

**The owner's override (`0_OWNER_Details (met, options, chose, why, undo) in the worker's report. In short:
1. The mechanism: a Vite project plus one function in `api/`, with `vercel-build` (not zero-config Express, not the Build Output API, which would drop `vercel.json`'s headers).
2. `prisma.config.ts` unchanged; the deploy script hands `DIRECT_URL` to the migration as `DATABASE_URL`.
3. `.npmrc` `include=dev`, so `NODE_ENV=production` never strips the build's and the `postinstall`'s tools.
4. `NODEJS_HELPERS=0`, so the function gets Node's own request, as the local server does.
5. zod jitless by an inline script (found by the proof); `zod` declared as the web's devDependency for its test.
6. `/health` not public online (D1 literally); proposed alternative: a rewrite to the function.
7. `Referrer-Policy: strict-origin-when-cross-origin` (OSM's tiles need a referrer) and `X-Frame-Options: DENY`; no `Permissions-Policy`.
8. Finding 213's estimate: about 60 CU-hours a month from the cron; Neon's usage is a first check.
9. The function test's 30 s load timeout (cold transform of the whole app).
10. The shared database container recreated by `npm run db:up` after a machine restart: the old one still bound a file #132 removed from the main folder; setup documents the step, and every database is intact..md` item 9):** the plan was saved and built in the same session, without the usual stop for approval, for the 2026-11-03 deadline.

## Scope / Acceptance criteria / Out of scope

**Scope:** D1–D10 of the owner's decisions (2026-11-01).

- [x] **D1 — one project, one origin.** `vercel.json`: framework `vite`, `npm ci`, the full build with `NODE_ENV=production`, output `apps/web/dist`; rewrites `/api/:path*` → `/api` (the function, its path kept) and every other non-file path → `/index.html`; region `fra1`; Node.js 24 from `engines`. *Mechanism:* a Vite project plus one Node function, `api/index.js`, which re-exports the API's build; the root `vercel-build` script builds it (Vercel's documented step for build outputs inside a function). Zero-config Express was not chosen: it needs the entry at the root or `src/` and takes the project as a backend; *Services* is beta.
- [x] **D2 — the thin entry**, `apps/api/src/function.ts`: `createAppFromEnv` with a logger and the readiness check only — no `startJobs`, `listen`, `exit` or signal handler, no database query at load; the environment validated once per instance; an invalid one answers every request the `server` (500) envelope and names the variables, never their values. `server.ts` unchanged but a comment (D3).
- [x] **D3 — the cron every 15 minutes online** (the local timer stays 5). Finding **213** recorded and resolved; ADR 0014 *Revised*; conventions §12; api-contract *Internal*; setup *Timed jobs*; spaces.md's reclamation line; `server.ts`'s comment.
- [x] **D4 — production from `main` only**, `git.deploymentEnabled: {"**": false, "main": true}`; the runbook says why.
- [x] **D5 — migrations on production deploys only**, after a successful build, over `DIRECT_URL` (`apps/api/scripts/migrateOnDeploy.ts`); a missing `DIRECT_URL` or a failed migration fails the deploy. `prisma.config.ts` **unchanged** (preferring a `DIRECT_URL` there would let the test lane migrate whatever it names); `.env.example` gains comment lines only. The runbook states the rule: every migration works with the code before it.
- [x] **D6 — the web's headers** in `vercel.json` (closes **33, 46, 64**): the CSP below, COOP `same-origin-allow-popups`, `nosniff`, `Referrer-Policy`, `X-Frame-Options: DENY` + `frame-ancestors 'none'`, a year's cache for `/assets/*` only. A web unit test fails when an inline script of `index.html` no longer matches its hash.
- [x] **D7 — `TRUST_PROXY=1`**: Vercel overwrites `x-forwarded-for` with the visitor's address and forwards none a client sends; in the runbook and security.md.
- [x] **D8 — the runbook**, setup › *The deployment*: how it is served, every variable and where its value comes from, the owner's 8 steps, the first checks.
- [x] **D9 — 23, 65, 152 stay Open**, each with a dated line pointing at the first check that measures it.
- [x] **D10 — native and generated parts on Linux**, from the lockfile and the docs (below); what only an account can prove is in the first checks.

**Out of scope:** any account, secret or deployment; previews; findings 23, 65, 152; any module, rule, route or schema change.

## The platform facts (checked 2026-11-01)

- One Node function per file in `api/`; one shared entry with rewrites is Vercel's advice — https://vercel.com/docs/functions/runtimes/node-js
- Zero-config Express: entry at the root or `src/`, statics only from `public/**` — https://vercel.com/docs/frameworks/backend/express
- `vercel-build` builds what a function includes; `NODEJS_HELPERS=0` — https://vercel.com/docs/functions/runtimes/node-js/advanced-node-configuration
- Builders run frontend first, one install scope in one chain — `vercel/vercel` `internals/builder-orchestration/src/sort-builders.ts`, `internals/cli-builder-integration/src/build-concurrency.ts`
- `vercel.json` keys, rewrites after files — https://vercel.com/docs/project-configuration/vercel-json · https://vercel.com/docs/routing/rewrites
- `git.deploymentEnabled` globs, a `true` match wins — https://vercel.com/docs/project-configuration/git-configuration
- Node 26/24/22, `engines` overrides — https://vercel.com/docs/functions/runtimes/node-js/node-js-versions
- Hobby: 300 s, 2 GB, 250 MB bundle, 4.5 MB body, one region — https://vercel.com/docs/functions/limitations
- `VERCEL_ENV` at build and runtime — https://vercel.com/docs/environment-variables/system-environment-variables
- `x-forwarded-for` overwritten, no external IPs forwarded — https://vercel.com/docs/headers/request-headers
- devDependencies installed by default; npm omits them under `NODE_ENV=production` — https://vercel.com/docs/builds/configure-a-build · https://docs.npmjs.com/cli/v11/using-npm/config#omit
- Neon pooled (`-pooler`, transaction mode) vs direct for migrations — https://neon.com/docs/connect/connection-pooling
- GIS CSP and COOP — https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid
- Tracing: `node-gyp-build` evaluated at build, `sharp` special case, literal `import()` — `vercel/nft` `src/analyze.ts`, `src/utils/special-cases.ts`

**D10, from the lockfile and the code:** `@img/sharp-linux-x64` and `@img/sharp-libvips-linux-x64` (glibc) are in the lockfile as optional packages; bcrypt 6 ships `prebuilds/linux-x64/bcrypt.glibc.node`, loaded by `node-gyp-build`; Prisma 7 `prisma-client` with `@prisma/adapter-pg` has no engine binary (the query compiler is a wasm-base64 module, loaded by a literal `import()`), and the API's `postinstall` generates the client in Vercel's install. **`.npmrc` gains `include=dev`**, so that install and the build keep their devDependencies with `NODE_ENV=production` set.

## The CSP, source by source

| Directive | Sources |
|---|---|
| `default-src` | `'self'` |
| `script-src` | `'self'` · the pre-paint script's hash · zod's settings script's hash · `https://accounts.google.com/gsi/client` |
| `style-src` | `'self'` · `'unsafe-inline'` (`sonner`'s and Radix's runtime `<style>` elements) · `https://accounts.google.com/gsi/style` |
| `img-src` | `'self'` · `data:` (Leaflet's icons in its CSS) · `https://tile.openstreetmap.org` · `https://res.cloudinary.com` |
| `font-src` | `'self'` · `data:` (subsets the build inlines) |
| `connect-src` | `'self'` · `https://accounts.google.com/gsi/` |
| `frame-src` | `https://accounts.google.com/gsi/` |
| `object-src` / `base-uri` / `form-action` / `frame-ancestors` | `'none'` / `'self'` / `'self'` / `'none'` |

**Found by the local proof:** zod 4 probes for `eval` once, building its first schema, and the CSP reported it on every page (105 reports in the first run). The schemas are built as their modules load, before any app code, so a second inline script sets `globalThis.__zod_globalConfig = { jitless: true }` first; a unit test holds it to zod's own global (`zod` declared as the web's devDependency for it, same version, no new package).

## Evidence

**Tests, each seen failing first:**
- `apps/api/src/function.api.test.ts` — the exported handler on a Node server answers `/health` 200 and a 404 envelope through the same app, with no `setInterval`; an invalid environment answers 500 and names `JWT_SECRET`, never its value, once. Red: `Cannot find module '/src/function.ts'`. Mutation (a `startJobs` wired in): `expected "setInterval" to not be called at all, but actually been called 1 times`.
- `apps/web/scripts/contentSecurityPolicy.unit.test.ts` — red: `ENOENT … vercel.json`; the prompt's break (the inline script changed from a backup copy, restored by copy): `AssertionError: expected [ Array(1) ] to deeply equal [ Array(1) ]`; with the second script before its hash was added: `vercel.json's script-src must list index.html's inline scripts as … expected [ Array(1) ] to deeply equal [ …(2) ]`.
- `apps/web/src/app/jitlessSchemas.unit.test.ts` — mutation (the setter emptied): `expected {} to deeply equal { jitless: true }`.
- `apps/api/scripts/migrateOnDeploy.unit.test.ts` — red: `Cannot find module './migrateOnDeploy.ts'`. A real run too: unset → skips, exit 0; production without `DIRECT_URL` → exit 1; production with `masaha_b_test` → "No pending migrations to apply", exit 0; an unreachable host → `P1001`, exit 1.

**The production-shaped local proof:** the full `buildCommand` of `vercel.json` in a clean shell (`env -i`), with `NODE_ENV=production` and a dummy `VITE_GOOGLE_CLIENT_ID` generated in the shell and never echoed; the migration step skipped (no `VERCEL_ENV`). The built web served with exactly `vercel.json`'s headers and rewrites (a script outside the repository reading the file) in front of the root `api/index.js` on a plain Node server (`masaha_b_dev`). Headless Chrome over CDP, ar and en, 390 and 1440: home, the directory and its map's tiles, a space's gallery, sign-in with Google's button drawn, register, the admin's add-space map, a photo picked on a space's editor (its POST failed before it was sent) — **28 pages, CSP violations 0, deep-link reloads 24/24 at 200** (`/spaces`, a space, `/login`, `/about`, an unknown path, `/dashboard/admin/spaces/new`). The only console errors: the four photo POSTs failed on purpose.

**Run locally on the head, each green:** on `f79fdbc0`, after `npm ci` and `npm run build -w @masaha/shared`: `format:check` 0 · `lint` 0 · `typecheck` 0 · `check:classes` 0 · `check:links` 0 · `check:conflicts` 0 · `test:unit` 0 · `test:component` 0 · `test:api` **1 on the first run** (the failing test was not kept: the script logged only npm's last lines), then 0 on a re-run alone: 121 files, 1380 tests passed · `NODE_ENV=production npm run build` 0 · `check:build` 0.

**Not run:** anything on Vercel or Neon (no account, by design): the first checks list them.

**Early conflict check:** no other pull request is open.

## The owner's late inputs (2026-11-01)

- **Google's consent screen stays in *Testing*** (amended item 6): online, Google sign-in works only for the test users listed on it (≤ 100); everyone else registers by email. The runbook's step 5 says so (no "In production" step); the first checks use a listed test user.
- **Neon's `sslmode=require&channel_binding=require`** stays in both strings. `pg` 8.23 through `@prisma/adapter-pg` accepts `channel_binding` and ignores it (it reads only its own `enableChannelBinding`; `sslmode=require` means `verify-full` there, with one warning line). Prisma 7's schema engine (`migrate deploy`) accepts and enforces it: without TLS it refuses (`server did not use channel binding`, on `masaha_b_dev`), and against a throwaway PostgreSQL 18 over TLS with SCRAM it applied all 31 migrations with Neon's exact parameters. The runbook names the fallback, should the Linux engine refuse on the first deploy: remove only `&channel_binding=require` from `DIRECT_URL`.

## What the owner does, in order

[setup › The deployment › The owner's steps](docs/development/setup.md#the-owners-steps): 1. Neon (Frankfurt, PostgreSQL 18) · 2. import the repository in Vercel · 3. the variables · 4. the first deploy · 5. the public address in Google's origins (and `CORS_ORIGIN`) · 6. the first admin by `npm run db:seed` from his machine over the direct URL · 7. cron-job.org every 15 minutes · 8. the first checks.

## Findings

- **Resolved:** 33, 46, 64 (the web's headers), 213 (the cron's interval, recorded here).
- **Open:** 23, 65, 152 — measured after the deployment; setup › *The first checks* says how.

## Decisions taken without the owner

Details (met, options, chose, why, undo) in the worker's report. In short:
1. The mechanism: a Vite project plus one function in `api/`, with `vercel-build` (not zero-config Express, not the Build Output API, which would drop `vercel.json`'s headers).
2. `prisma.config.ts` unchanged; the deploy script hands `DIRECT_URL` to the migration as `DATABASE_URL`.
3. `.npmrc` `include=dev`, so `NODE_ENV=production` never strips the build's and the `postinstall`'s tools.
4. `NODEJS_HELPERS=0`, so the function gets Node's own request, as the local server does.
5. zod jitless by an inline script (found by the proof); `zod` declared as the web's devDependency for its test.
6. `/health` not public online (D1 literally); proposed alternative: a rewrite to the function.
7. `Referrer-Policy: strict-origin-when-cross-origin` (OSM's tiles need a referrer) and `X-Frame-Options: DENY`; no `Permissions-Policy`.
8. Finding 213's estimate: about 60 CU-hours a month from the cron; Neon's usage is a first check.
9. The function test's 30 s load timeout (cold transform of the whole app).
10. The shared database container recreated by `npm run db:up` after a machine restart: the old one still bound a file #132 removed from the main folder; setup documents the step, and every database is intact.

## Change type

`chore` — deployment configuration, one entry, one script, documents.

## Definition of Done

- [x] Acceptance criteria met, scope kept (D1–D10).
- [x] Lint and typecheck clean; build passes; `check:build` passes.
- [x] Tests in their owning lanes, each seen failing first.
- [x] No user-facing text added.
- [x] UI unchanged; the headers checked in ar and en at 390 and 1440 (the proof).
- [x] Authorization untouched.
- [x] Triggered documents updated: setup (the runbook), conventions §12, security, api-contract, ADR 0014, spaces, foundation F-7, the findings and their index.
- [x] One home per fact; nothing claimed as live that is not.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed, description complete.
