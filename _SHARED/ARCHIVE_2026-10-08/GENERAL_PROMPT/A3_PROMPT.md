Work Item A-3 — Record the cross-cutting decisions · branch `docs/cross-cutting`

## How to work (mandatory)

1. Read CLAUDE.md, then docs/development/workflow.md, then docs/README.md. Follow the project's workflow exactly: task classes, Git lifecycle, scope control, Definition of Done, decision authority, stop rules.
2. Work in the MAIN folder (this repository's working tree). Do NOT create a git worktree: the existing worktree is reserved for other work.
3. Start in PLAN MODE. No edit, no branch and no commit before the owner approves a written plan. The plan lists:
   - every file to create or change, and what changes in each;
   - the commits (atomic units per workflow §3);
   - how you verify;
   - any question or divergence you found.

   Wait for approval.

4. After approval:
   - check `git status`. If the tree is not clean, or not on `main`, stop and report;
   - fetch and pull `main`, then cut the branch;
   - implement only the approved plan. Anything outside it: stop and ask. Unrelated problems are recorded as findings, not fixed.
5. Finish at "Ready for review": self-review against the Definition of Done, push, open the PR. Never merge.

## Context

A-1 (PR #18) recorded the backend architecture: ADR 0012, ADR 0013 and docs/backend/conventions.md. A-2 (PR #19) moved the space settings and occupancy into their own tables.

A-3 was drafted in docs/plans/foundation.md as "decide the cross-cutting topics". The owner and an analyst have since DECIDED all of them. So A-3 now RECORDS approved decisions in their owning documents. It is documentation only, like A-1.

The decisions below count as the owner's explicit instruction (CLAUDE.md, decision precedence 1): document them; do not re-open them. If the code or a document contradicts one in a way you can't document around, stop and report it in the plan.

## Parallel work (read before planning)

Another conversation runs at the same time: **DS-1, design-system categories and showcase navigation**.
- It works in the git worktree `C:\Users\basel\masaha-ds`, on the branch `refactor/design-system-categories`. Never open, edit or run anything in that folder; it is not yours.
- **Its files:** `apps/web/src/shared/design-system/**`, `apps/web/src/pages/showcase/**`, `apps/web/components.json`, `.design-sync/**`, `docs/frontend/design-system/foundation.md`. A-3 never touches them.
- **A-3's files:** the ADRs, `docs/backend/**`, `docs/api/**`, `docs/frontend/architecture.md`, `docs/plans/**`, `docs/README.md` (the ADR list). DS-1 is told the same list.
- **Shared risk:** if either item truly needs a file from the other's list, its plan says so first. Keep any such edit minimal.
- **Before opening the PR:** fetch and rebase on the latest `main`. Merge order doesn't matter: whoever merges second rebases, and resolves any conflict by keeping both sides.
- Neither item installs or changes dependencies, so `package-lock.json` stays untouched on both sides.

ADR style (the owner's standing rule):

- short and decision-level: Context · Decision · Alternatives (the main ones only) · Consequences;
- no file names, paths or implementation details;
- ADR 0011–0013 are the style reference;
- the operative rules go in the owning documents, linked from the ADR.

## Approved decisions

### Deployment → ADR 0014

Context:

- The graduation defence runs on the local environment (Docker and the dev servers). It works offline, which matters with Gaza's power and internet cuts.
- A public deployment is needed as a portfolio showcase, at zero cost and with no purchased domain, behaving like the real product.
- The session model (ADR 0003) needs the web and the API on one origin: the refresh cookie is SameSite=Strict, and the web reads the session-hint cookie.

Decision:

1. Vercel serves the web and the API under one origin (masaha.vercel.app, or the nearest available name): the static web at /, the same Express application as a function under /api. Neon hosts PostgreSQL. Both run in one European region near Gaza.
2. The deployment adapts to the architecture, never the reverse. It changes only:
   - infrastructure port implementations (storage, email, scheduler, clock);
   - configuration;
   - one thin entry.

   The same composition root assembles the application everywhere: a long-running server locally, a function on Vercel. No module, rule or API contract changes for it.

3. Development runs from one origin too: the web dev server proxies /api to the API, so cookies behave locally exactly as online.
4. Every free-tier difference from a paid setup is listed under "Deviations to revisit", so none is lost when the project moves to a paid host and its own domain.

Deviations to revisit (free tier → what a paid setup with its own domain would change):

- **Address:** masaha.vercel.app → the project's own domain. Update the OAuth origins and CORS_ORIGIN, and re-check the cookie settings.
- **Scheduler:** there is no long-running process.
  - The scheduler port's job runs through an internal, secret-protected endpoint, called by an external free cron every few minutes. Vercel's free cron runs daily only.
  - A paid setup would use an in-process or platform scheduler at full precision.
  - Check-outs always record the cut-off time, so a late run never corrupts data.
- **Files:** no persistent disk, and a request-size limit of about 4.5 MB.
  - Photos go to free object storage through the storage port, with client-side resizing or direct upload.
  - A paid setup would use a paid bucket with a CDN.
- **Email:** without a domain, no domain-verified provider is possible; a single verified sender (or Gmail SMTP) is used. A paid setup would use a domain-verified provider with SPF and DKIM.
- **Rate limiting:** function instances share no memory, so the limits are stored in PostgreSQL. On a single server they could stay in memory, or move to a dedicated store.
- **Database:**
  - a pooled connection for the app and a direct one for migrations;
  - the free tier's storage and compute limits;
  - the PostgreSQL major the free tier offers. If it is not 18, add a revision line to ADR 0001.
- **Logs:** the free tier keeps them only briefly. A paid setup would use a log drain or service.
- **Cold starts:** the first request after idle is slower. A paid setup would use always-on instances.
- **Usage terms:** Vercel's free plan is for non-commercial personal projects; real paying spaces mean a paid plan.

Alternatives:

- **Web on Vercel, API on Render's free tier behind a proxy.** Rejected. The free server sleeps after about 15 minutes, and the next request takes 30–60 s. Keeping it awake with pings works against the provider's terms.
- **An Oracle Cloud always-free VM.** Rejected. It needs a credit card, sign-ups are often refused, HTTPS needs a domain, and one developer would have to operate a server.
- **Separate origins for the web and the API.** Rejected: the session's cookies would not reach the API.

Consequences:

- One application with two entries; what runs locally is what runs online.
- No work runs after a response is sent (a rule for every environment).
- Revisit when the project is used commercially or gets its own domain: then work through the deviations list.

**VERIFY before writing:** check the current free-tier terms and limits on the providers' official pages (Vercel Hobby: functions, cron, request-size limit, log retention, terms; Neon free: limits, regions, PostgreSQL versions). Correct any figure above that changed, and date the check in the ADR.

### Idempotency and concurrency → ADR 0015

- **I1.** Every create the front desk performs stores the client's request id, with a unique key per space. Every update or delete is designed to be idempotent: a repeated check-out returns the closed record, and a repeated void returns the voided payment. There is no generic store of responses. Today payments, visits and check-ins carry the request id (F-3b).
- **I2 (recorded, not built).** Subscriptions and customers still lack a request id. A new subscription without a payment, retried, would create two. The subscriptions-and-customers slice adds it. Note it on that slice in docs/plans/v1-mvp.md.
- **I3.** A retried request returns the first result, with the same status and body, never a conflict.
- **I4.** Isolation stays at PostgreSQL's default, read committed. The database's constraints and row locks are the guarantee. Rows are always locked in one fixed order (oldest first, then id), so spreading one payment over several items can't deadlock.
- **G1.** The database owns the three payment rules its triggers enforce: append-only, voided once, never above the due amount. The last one locks the item's row, so concurrent payments are already safe. Services do not duplicate these rules (one owner per fact).
- **G2.** One translation table in the shared errors maps a constraint's name to a domain error code (for example, payments_within_due → PAYMENT_EXCEEDS_DUE), the way P2002 already maps to NOT_UNIQUE. The text comes from the copy catalogues.
- **G3.** API integration tests hit each trigger and check the code returned.

### Dashboard URLs → ADR 0016

- **R1.** The selected space is in the URL, not in client state. Links can be shared, back works, two tabs can hold two spaces, and the path mirrors the API's.
- **R2.** The dashboard is /dashboard/admin/… for the admin and /dashboard/spaces/:spaceId/… for a space. /dashboard redirects by role.

### Into the owning documents (no ADR)

**Time → conventions.md:**

- T1: Gaza time is computed with @date-fns/tz and date-fns. Both are already in the lockfile, through react-day-picker. They are added as direct dependencies of the API and packages/shared by the first slice that needs them; not now.
- T2: the day and week rules ("today", and the week from Saturday to Friday) are pure functions in packages/shared, taking the time as a parameter.
- T3: date-only columns (a subscription's start and end) are Gaza dates and are never converted.
- T4: an injected clock (R5's port); no `new Date()` inside a rule.
- T5: Palestine's daylight-saving rules change by decree. This is a known risk, mitigated by keeping Node updated and by a test that pins a known Gaza transition.

**Errors and logging → conventions.md** (L1 also in security.md):

- **L1:** the HTTP logger redacts cookie, authorization, set-cookie, and any password or token field, and never logs request bodies. Today pino-http runs with no redaction and logs request headers. No cookie or token exists yet, so F-5 must ship the redaction together with the first token (an acceptance criterion in F-5's contract).
- **L2:** every request gets a UUID. It goes in the log, in an `X-Request-Id` response header and in the error envelope (api-contract.md), and the web shows it in error states.
- **L3:** log fields: request id, user, role, space, route, status, duration. 4xx is logged at warn, 5xx at error.
- **L4:** adding a domain error code: the code in packages/shared → both copy catalogues (the typecheck enforces this) → api-contract §6 → a test.

**Routes and server state → frontend/architecture.md:**

- **R3, landing after sign-in:** the return URL if any. Otherwise the admin goes to the admin overview, an owner to the overview of the last space they used, and reception to the front desk.
- **R4, failed guards:** a guest goes to sign-in with a return URL. A signed-in user without access gets a clear 403 page, never a silent redirect. An unknown space gets a 404.
- **R5, the space switcher:** it shows for anyone with more than one active link, whatever their role.
- **R6, identifiers:** the id in dashboard URLs, the slug on public pages.
- **Q1, query keys:** they start with their scope: ['space', spaceId, '<capability>', …], ['me', …], ['public', …].
- **Q2, invalidation:** each feature invalidates its own keys. desk's cross-capability operations invalidate the whole space prefix, without importing other features.
- **Q3, retries:** queries are always retried. A mutation is retried only when it carries an idempotency key, generated once per user action and reused on every retry. Add a revision line to ADR 0004.
- **Q4, polling:** the live status every 60 s, paused while hidden (already decided); the desk's present list every 30 s, and on window focus.
- **Q5, optimistic updates:** never for money or presence; only for favourites.
- **Q6, offline:** no offline queue. A clear "no connection" state, and the user retries.

**Dev ports → recorded now, built in F-5:**

- **P1:** a port of its own for each app: 5320 for the web, 3320 for the API, with Vite's strictPort, and CORS_ORIGIN to match.
- **P2:** the Vite proxy for /api, and the web calls /api/v1 relatively in every environment.

setup.md changes only when F-5 builds this; until then, ADR 0014 records the decision.

## Plans

- **docs/plans/foundation.md, F-5's contract gains:**
  - L1 redaction and the L2 request id;
  - the P1 ports and the P2 proxy, with setup.md;
  - the rate-limit store in PostgreSQL (a table, so a schema change inside F-5);
  - the email constraint: no domain-verified provider, plus a development mode that logs the link.
- **A-3** is marked as decided and recorded.
- **docs/plans/v1-mvp.md:** the I2 note on the subscriptions-and-customers slice.
- **Propose in the plan (owner approves):** a drafted later item for the first public deployment, after F-6, which sets up Vercel and Neon per ADR 0014.

## Out of scope

- Any code, config or dependency change: L1, L2, P1, P2 and the rate-limit store belong to F-5, and the time dependencies to their first slice.
- Re-opening any decision.

## Verification

- Every relative link and anchor resolves.
- One owner per fact; the ADRs contain no paths.
- `npm run lint`, `prettier --check .` and `typecheck` pass. Run checks from the uppercase `C:\` path (finding 9).

## PR

Per workflow §3:

- labels `docs` + `area:docs`, assigned to me (`--assignee @me`);
- the description template, with `@coderabbitai ignore` in the body;
- no AI attribution anywhere.

Don't merge.
