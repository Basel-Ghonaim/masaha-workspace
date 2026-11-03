# DEPLOY — the plan (F-7, `chore/deployment`)

> Worker B, `C:\dev\masaha\app-b`, 2026-11-01. **The owner's override (`0_OWNER_DECISIONS.md` item 9):** this plan
> is saved and then built in the same session, with no stop for approval, for the 2026-11-03 deadline. Stated here
> and in the PR.

## 0. Contract

- **Scope:** make Masaha deployable on Vercel + Neon as ADR 0014 decides (D1–D10): one function entry, `vercel.json`
  (build, routing, region, no previews, the web's headers), the production-only migration step, the online cron at
  15 minutes, the runbook in `setup.md`, findings 33, 46, 64 and 213 resolved.
- **Acceptance:** each D below met as written in §2; the function answers through the same app with no timer (test);
  the CSP hash check fails on a changed inline script (test); the production-shaped local proof shows zero CSP
  violations; every lane and check green locally and in CI.
- **Out of scope:** any account, secret or deployment; findings 23, 65, 152 (measured after the deployment, D9);
  any module, rule, route or schema change; previews (D4).

## 1. Platform facts (checked 2026-11-01)

| # | Fact | Source |
|---|---|---|
| P1 | A Node function is any file in the root `api/`; Vercel advises one shared entry with rewrites sending related paths to it, the handler routing by pathname. Handlers get Node's own `IncomingMessage`/`ServerResponse`. | https://vercel.com/docs/functions/runtimes/node-js |
| P2 | Zero-config Express needs the entry at the project root or `src/` (`app`/`index`/`server`), takes the project as a backend and serves statics only from `public/**`. Not usable for a Vite web in `apps/web` + an API in `apps/api` at one root; **not chosen**. | https://vercel.com/docs/frameworks/backend/express |
| P3 | "Custom build step for Node.js": a `vercel-build` script in the nearest `package.json` above the function is run before the function is built, so build outputs can be included in it. | https://vercel.com/docs/functions/runtimes/node-js/advanced-node-configuration |
| P4 | Helpers (`req.query`, `req.body` …) are added unless `NODEJS_HELPERS=0`. | same page |
| P5 | Builders are ordered frontend first (`sortBuilders`), and builds sharing one install scope run in one chain, in that order. | `vercel/vercel` `internals/builder-orchestration/src/sort-builders.ts`, `internals/cli-builder-integration/src/build-concurrency.ts` (read with `gh api`, 2026-11-01) |
| P6 | `vercel.json`: `buildCommand`, `installCommand`, `outputDirectory`, `framework`, `regions` (Hobby: one region), `functions` (`maxDuration`; memory not in `vercel.json` with Fluid), `rewrites`, `headers` (`source` matches the incoming pathname). The SPA fallback is a rewrite of every path to `/index.html`; files are served before rewrites. | https://vercel.com/docs/project-configuration/vercel-json · https://vercel.com/docs/routing/rewrites |
| P7 | `git.deploymentEnabled`: an object of branch globs (minimatch) to booleans; unspecified branches default to `true`; a branch matching several rules deploys if one is `true`. So `{"**": false, "main": true}` deploys `main` only. | https://vercel.com/docs/project-configuration/git-configuration |
| P8 | Node versions 26.x (default), 24.x, 22.x; `engines.node` overrides the project setting; `^24` / `24.x` map to the latest 24.x. Ours, `>=24.15.0 <25`, is satisfied by 24.x only. | https://vercel.com/docs/functions/runtimes/node-js/node-js-versions |
| P9 | Hobby, Fluid compute: 300 s default and maximum duration, 2 GB / 1 vCPU, 250 MB uncompressed bundle, 4.5 MB request/response body, one region (default `iad1`). | https://vercel.com/docs/functions/limitations |
| P10 | `VERCEL_ENV` (`production` / `preview` / `development`) is available at build and runtime. | https://vercel.com/docs/environment-variables/system-environment-variables |
| P11 | `x-forwarded-for` is the client's public IP; Vercel **overwrites** it and does not forward external IPs, to prevent spoofing (a custom XFF only on Enterprise's trusted proxy). | https://vercel.com/docs/headers/request-headers |
| P12 | Install: devDependencies are installed by default. npm's own rule: `omit` defaults to `dev` when `NODE_ENV=production`, and a type in both `include` and `omit` is included. | https://vercel.com/docs/builds/configure-a-build · https://docs.npmjs.com/cli/v11/using-npm/config#omit |
| P13 | Neon: the pooled host carries `-pooler`, PgBouncer in transaction mode; schema migrations use the **direct** string (tools may not support transaction pooling; session advisory locks unsupported when pooled). Examples carry `?sslmode=require`. | https://neon.com/docs/connect/connection-pooling |
| P14 | GIS CSP: `script-src https://accounts.google.com/gsi/client`; `frame-src` and `connect-src https://accounts.google.com/gsi/`; `style-src https://accounts.google.com/gsi/style`. COOP `same-origin-allow-popups` (a plain `same-origin` breaks the popup). Origins: scheme + host, `http://localhost:<port>` for development. | https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid |
| P15 | Function tracing (`@vercel/nft`): `node-gyp-build` is evaluated at build (bcrypt's `prebuilds/linux-x64`), `sharp` has a special case (its `@img/*` packages), literal `import()` is traced (Prisma's `query_compiler_fast_bg.postgresql.*`). | `vercel/nft` `src/analyze.ts`, `src/utils/special-cases.ts` (`gh api`, 2026-11-01) |

**Docs vs ADR 0014:** no conflict with a decision. Facts updated: the cron is 15 min (D3); the ADR's "every few
minutes" stays true. ADR 0014 calls the function "under `/api`": it is `api/index.js`, answering every `/api/*` path
by rewrite (P1).

## 2. D1–D10 as built

- **D1 — mechanism: a Vite project at the root, plus one Node function `api/index.js`.** `vercel.json`:
  `framework: "vite"`, `installCommand: "npm ci"`, `buildCommand` = the full build with `NODE_ENV=production`, then
  the migration step (D5); `outputDirectory: "apps/web/dist"`; `regions: ["fra1"]`; rewrites, in order:
  `/api/:path*` → `/api` (the function sees the original path, P1), and `/((?!api(?:/|$)).*)` → `/index.html` (deep
  links and reloads; files first, P6). `api/index.js` re-exports the API's built entry
  (`apps/api/dist/function.js`); the root `vercel-build` script builds `@masaha/shared` and `@masaha/api` so the
  function's inputs exist whatever the builders' order (P3, P5). Node 24 from `engines` (P8). *Why not zero-config
  Express:* P2. *Why not Services:* beta (the prompt).
- **D2 — `apps/api/src/function.ts`:** validates the environment once per instance; on success
  `createAppFromEnv(env, { logger, checkDatabase })` and exports that app as the handler — no `startJobs`, no
  `listen`, no `process.exit`, no signals, no startup database query (the readiness route keeps it). On an
  `EnvError` it writes the error's message (variable names and rules only, never a value) to stderr once, and every
  request answers the error envelope, `server` (500). `server.ts` unchanged (but D3's comment).
- **D3 — finding 213** recorded as Resolved (Neon's 100 CU-hours vs a 5-minute cron, the owner's evidence); ADR 0014
  *Revised*; conventions §12 table; api-contract *Internal*; setup *Timed jobs*; spaces.md's reclamation line;
  `server.ts`'s comment (the local timer, "as the external cron does online" no longer true).
- **D4 —** `git.deploymentEnabled: {"**": false, "main": true}` (P7); runbook says why (the owner's item 3).
- **D5 — `apps/api/scripts/migrateOnDeploy.ts`,** run by `buildCommand` after `npm run build` succeeded: on
  `VERCEL_ENV=production` it runs `prisma migrate deploy` with `DATABASE_URL` set to `DIRECT_URL` for that process
  only, and fails (exit ≠ 0, so the deploy fails) when `DIRECT_URL` is missing or the migration fails; otherwise it
  says it skips. **`prisma.config.ts` unchanged**: preferring a `DIRECT_URL` there would make the test lane's
  `migrate deploy` (which sets only `DATABASE_URL`) migrate whatever `DIRECT_URL` names. `.env.example`: one comment
  line pointing online's two URLs to the runbook.
- **D6 — `vercel.json` `headers`** on `/((?!api/).*)` (the API keeps Helmet's): the CSP of §3, COOP
  `same-origin-allow-popups`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`
  (OSM's tile policy needs a referrer), `X-Frame-Options: DENY` beside `frame-ancestors 'none'`; on `/assets/(.*)`
  only, `Cache-Control: public, max-age=31536000, immutable`. **The hash check:** a web unit test
  (`apps/web/scripts/contentSecurityPolicy.unit.test.ts`) hashes every inline `<script>` of `apps/web/index.html`
  and expects exactly those hashes in `script-src`, no `'unsafe-inline'` there, and the same CSP on the pages'
  rule. The built `index.html` keeps the script byte for byte (checked: same SHA-256 in source and `dist`).
- **D7 — `TRUST_PROXY=1`:** Vercel overwrites `x-forwarded-for` with the client's address (P11), so Express trusting
  one hop takes `req.ip` from it and a forged header never reaches the function. Runbook + security.md.
- **D8 — `setup.md` › *The deployment*:** the environment, every variable and where its value comes from, the
  owner's steps in order, the first checks. The seed (read, not run online): `seed.ts` has no production guard and
  creates the admin; `demo.ts` and `demoDirectory.ts` throw on `NODE_ENV=production`; `process.loadEnvFile` does
  not override a variable already set (checked), so the shell's `DATABASE_URL` and `NODE_ENV` win over
  `apps/api/.env`, and `SEED_DEMO=false` must be set in the shell when that file says `true`.
- **D9 —** 23, 65, 152 stay Open, each with a dated line naming the runbook's check that measures it.
- **D10 —** `sharp`: lockfile lists `@img/sharp-linux-x64` and `@img/sharp-libvips-linux-x64` (glibc) as optional
  packages; `bcrypt` 6 ships `prebuilds/linux-x64/bcrypt.glibc.node`, loaded by `node-gyp-build`; Prisma 7
  `prisma-client` + `@prisma/adapter-pg`: no engine binary, the query compiler as a wasm-base64 module; the client is
  generated by the API's `postinstall` in Vercel's install; tracing per P15. **`.npmrc` gets `include=dev`**: with
  `NODE_ENV=production` in the project's variables, npm would otherwise omit devDependencies (P12), and the API's
  `postinstall` (`prisma generate`, a devDependency) and the build (Vite, tsc) would fail. Unproven without an
  account → the first checks.

## 3. The CSP, source by source

`default-src 'self'` · `script-src 'self' 'sha256-dy6NDMUPHxzM7v6Q6+dcqVVieSYsVYsvW6OAgGvMQlE='
https://accounts.google.com/gsi/client` (the bundles; the theme script; GIS) · `style-src 'self' 'unsafe-inline'
https://accounts.google.com/gsi/style` (the bundle's CSS; `sonner` and `react-style-singleton` (Radix's scroll lock)
insert `<style>` elements at runtime, which neither a hash nor a nonce can name on a static host; GIS's sheet) ·
`img-src 'self' data: https://tile.openstreetmap.org https://res.cloudinary.com` (local files; Leaflet's icons as
`data:image/png` in its CSS; OSM tiles; Cloudinary photos) · `font-src 'self' data:` (the self-hosted IBM Plex,
three subsets inlined as `data:font/woff` by Vite) · `connect-src 'self' https://accounts.google.com/gsi/` (the API;
GIS, FedCM) · `frame-src https://accounts.google.com/gsi/` (the button) · `object-src 'none'` · `base-uri 'self'` ·
`form-action 'self'` · `frame-ancestors 'none'`. No `blob:`: nothing in the web shows a blob URL (the CSV download
navigates to one, which no fetch directive governs). The proof (§6) settles any miss.

## 4. Commits, in order

1. `feat(api): add the function entry for Vercel` — `apps/api/src/function.ts`, `function.api.test.ts`,
   `api/index.js`, root `package.json` (`vercel-build`), conventions §12 (the two entries), security.md (startup).
2. `chore: add the deployment config and headers` — `vercel.json` (all but the migration step), `.npmrc`, the CSP
   unit test, findings 33, 46, 64 resolved + index.
3. `chore(api): migrate on production deploys` — `apps/api/scripts/migrateOnDeploy.ts` + its unit test, `vercel.json`
   `buildCommand`, `.env.example` comment.
4. `docs: run the online cron every 15 minutes` — finding 213 + index, ADR 0014, conventions, api-contract,
   spaces.md, setup *Timed jobs*, `server.ts` comment.
5. `docs(setup): add the deployment runbook` — setup › *The deployment*, security.md (`TRUST_PROXY`), findings 23,
   65, 152 lines, foundation F-7 note (previews off).

## 5. Tests, each red first

- `function.api.test.ts` (API lane): the exported handler on a Node `http` server answers `GET /health` 200 `db up`
  and `GET /api/v1/no-such-route` 404 with the envelope; `setInterval` never called (a `startJobs` would call it);
  an invalid environment answers the 500 envelope and stderr names the variable, never its value. Red: the module
  does not exist yet.
- `contentSecurityPolicy.unit.test.ts` (web unit lane): red first against a `vercel.json` without the hash; then the
  break of §5 of the prompt (index.html's script changed from a backup copy, restored by copy).
- `migrateOnDeploy.unit.test.ts` (API unit lane): the decision — skips off production, refuses production without
  `DIRECT_URL`, runs with `DATABASE_URL = DIRECT_URL`. Red: module missing.

*Review focus* (no test exercises): the real Vercel build (builder order, tracing, Node 24), Neon's strings, GIS on
the public origin, Cloudinary over the CSP online — all in the runbook's first checks.

## 6. Local proof

`NODE_ENV=production` full build command in a clean Git Bash shell, dummies generated by `node -e` into variables,
never echoed (`VITE_GOOGLE_CLIENT_ID` a dummy). The API: the built `dist/function.js` on a plain `http` server on
3321 (`masaha_b_dev`, development env). The web: `scripts/serve.mjs` serving `apps/web/dist` with `vercel.json`'s
own headers and rewrites, read from the file, on 5321, `/api/*` proxied to 3321. CDP (headless Chrome): home,
directory + map tiles, a space's gallery, sign-in with Google's button, the admin's add-space map, a photo picked (not
sent); ar and en; 390 and 1440; console and CSP reports logged; every deep link reloaded. Then the full verification.

## 7. Proposed alternatives (recorded, not acted on)

- **`/health` online:** D1 sends only `/api/*` to the function, so the readiness route is not public online; the
  first checks read a public API route instead. A rewrite `/health` → `/api` would expose it; left to the owner.
- **A Neon branch for previews** later (the owner's item 3).
- **CSP `style-src` without `'unsafe-inline'`** would need `sonner`'s and Radix's runtime styles moved into the
  stylesheet; a later item if wanted.
