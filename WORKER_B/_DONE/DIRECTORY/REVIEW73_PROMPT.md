# Review — PR #73 (DIRECTORY: the public directory's API — the list, the map's pins, a space's page, search, "near me")

You are an **independent reviewer** of PR #73 in the Masaha repository (Basel-Ghonaim/masaha). Two
reviewers work on it at the same time, apart; do not read the other's report.
Write your report to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW73_<YOU>_REPORT.md`, where
`<YOU>` is your tool's name in capitals (`OPENCODE`, `COPILOT`).

## Rules

- **Run from `C:\Users\basel\masaha`**, but **read only commit objects** (that folder's working tree
  is on another PR's branch). No edits, commits, checkouts, switches, installs, npm or test runs,
  database or Docker commands, no GitHub comments. **Do not run the tests:** CI ran every lane on this
  head and passed; your job is to read. `git fetch origin`, then pin to **the PR's current head**
  (`gh pr view 73 --json headRefOid` — expected `28275b2`; write it at the top of your report and
  check it again at the end). Base: `git merge-base origin/main <head>`. Use
  `git diff <base>...<head> -- <paths>` and `git show <head>:<file>`.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario,
  the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If unsure, say
  "plausible" and why. A web search is allowed for a fact about PostgreSQL, Neon or a library; cite it.
- **No tool attribution** in what you write.

## What the PR must be (the owner's decisions)

API, `packages/shared/src/directory/` and documents; one migration (`pg_trgm` and SQL functions, no
table change); no dependency; nothing in `apps/web`. The approved plan is
`C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\DIRECTORY_PLAN.md` with its reply
`PROMPT\DIRECTORY_PLAN_REPLY.md` (the owner's decisions 1–5 and two additions); the prompt is
`PROMPT\DIRECTORY_PROMPT.md`; the worker's report is `REPORT\DIRECTORY_REPORT.md` (read its
departures).
- **The list (`GET /spaces`)** is paged and filtered on the server: every filter (area list, price
  period with bounds, student prices, open on Friday, verified, `q`) applies **before** the page is
  cut; sorts: latest update, name, best match, distance. **No** amenity filter, price sort, live
  status, capacity, counts, announcements or photos. **No prices on the card.**
- **The pins (`GET /map/spaces`):** the whole filtered set, at most 1,000, marked truncated past it;
  `bounds` narrows; a pin carries only what a pin and its card need (including `areaId` and the week's
  days).
- **A space's page (`GET /spaces/:slug`):** publicly listed only, else 404; an unverified space's
  stale prices hidden; the common and own amenities as one list.
- **Search:** both names and the area's names, Arabic folded (أ إ آ → ا, ة → ه, ى → ي, tashkeel and
  tatweel removed), typo-tolerant; a `q` that normalises to nothing is `invalid_format`.
- **"Near me" (privacy — the owner changed a v1 commitment for it):** the point travels **only** in
  the `Masaha-Near: lat,lng` header, never the query; at most **3 decimals**, a finer point refused;
  the header without `sort=distance` refused, `sort=distance` without it refused; **never stored,
  never logged** (the request log redacts the header), **never cached** (`no-store`); the distance
  answered rounded to 100 m.
- **Issue #69:** the contract's price line names both refusals, in its own commit.

## Look at these, in this order

1. **Privacy, end to end.** Follow the header from the request to the answer. Can the point reach
   any log line (the request log, an error log, a 4xx's `warn` line, a validation error's message or
   `details` that echoes the received value, an exception's stack), the response body beyond
   `distanceMeters`, an `ETag`, a cache, the database, or `req` where the logger serialises it? Is
   `no-store` on **every** answer that used the point, errors included? Can a client send the point
   another way (query, body, a differently cased or duplicated header) and have it used? Does the
   proof test read the whole line and would it fail if the redaction path went?
2. **The migration.** `pg_trgm` and the two functions: `IMMUTABLE`/`STABLE` truthful; the
   normalisation identical for stored names and the query; safe on an empty database and on Neon;
   that a later `prisma migrate` will not drop them; `COLLATE "ar-x-icu"` and `"en-x-icu"` exist on
   Neon's PostgreSQL (the worker did not confirm it — check the documentation) and what happens if not.
3. **The SQL.** Every raw query parameterised (no string building from input); paging right under
   each sort (the total, every page, a stable order on ties — the worker says the id tie-break under
   the default order is unproven); the price filter's meaning (the general audience, the period, the
   bounds) and stale prices of unverified spaces; publicly listed exactly as the data model defines
   it, in the list, the pins and the page alike; the cost at 1,000 spaces (no N+1, the week read for
   a set of ids).
4. **The levels and the boundaries.** `directory` at its level, importing only lower modules through
   their `index.ts`; `spaces`, `lookups` and `space-links` additions placed by their rules; nothing
   in `apps/web`; the shared package's new folder at its level.
5. **The cache.** The list's short `Cache-Control` and its validator (304 on a repeat) correct; a
   private or user-specific answer never cached; the page and the pins' rules.
6. **The tests.** Each would fail if its code broke; expectations written by hand; the distance
   order, the typo and hamza search, the truncation, the 404 of a hidden or unlisted space really
   exercised.
7. **The documents.** The contract (§4's pins exception, §5 *Directory (public)*, the price line),
   `directory.md` (new; the template of documentation rules §5, ≤ ~1,200 words), `spaces.md`,
   `lookups.md`, `space-links.md`, the data model, security.md (*Location*, the redaction),
   conventions, `overview.md` and foundation §13 (the changed "near me" commitment, dated), the plan's
   rows, the map line — each true to the code, one home per fact.
8. **The commits:** three; count each subject's characters yourself (≤ 50, no exception).

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.
