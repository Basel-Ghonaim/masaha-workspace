# DIRECTORY — the public directory's API: the paged list, the map's pins, a space's page (API)

**Worker B** · worktree `C:\Users\basel\masaha-b`, detached at `origin/main` (`e30a86c`; migrated,
client generated, shared `dist` built) · branch `feat/public-directory`, cut with
`git switch --no-track -c feat/public-directory origin/main` after `git fetch --prune origin`.
Databases `masaha_b_dev` / `masaha_b_test`; API on 3321, web on 5321.

**Model:** Opus 5.5, effort high. **Size cap:** at most 3 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\DIRECTORY_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\DIRECTORY_REPORT.md` (`final-report`).
Follow the skills from start to end: `start-work-item`, `write-plan`, `add-error-code` (for any new
code), `open-pr`, `final-report`.

## 1. The task in brief

Build step 3's API (`docs/plans/v1-mvp.md` › *3. Public directory*): what anyone reads without signing
in — the directory's list, the map's pins and a space's public page — over the publicly listed spaces
(data model › *Publicly listed*). **The owner settled its shape on 2026-10-13, and two settled rules
change with it (D1, D2): read them first.**

## 2. Read first

In the order workflow §2 *Reading before work* gives.
- **The capability documents first:** `docs/features/spaces.md` (the profile, the groups, freshness,
  own amenities, prices above zero) and `docs/features/lookups.md` (the public catalogue).
- `docs/plans/v1-mvp.md` › *3. Public directory* and the planned public API rows (`GET /spaces`,
  `GET /spaces/:slug`): **D1 and D2 change them**; `docs/project/overview.md` › the *Directory* and
  *Near me* lines; `docs/frontend/design-system/foundation.md` §13 › *Directory* (the near-me rule);
- `docs/architecture/data-model.md` › *Conventions*, *Spaces*, *Derived values* (publicly listed,
  stale, the unverified space's stale prices hidden); `docs/api/api-contract.md` §1–§4 (pagination),
  §5 › *Lookups (public)* and *Spaces (the admin)* (the shapes the public ones derive from), §6;
  `docs/backend/conventions.md` §5, §9 (*Composed reads*), §11 (time), §12–§13;
  `docs/backend/security.md` (rate limits, the request log's redaction, *HTTP hardening*);
  `docs/development/testing.md` §1–§4; ADR 0008 (live status is a state, never a count);
- the design (what the web will need; no screen here): `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_PUBLIC.md`
  (its *Amended* notes: no amenity filter, own amenities as the common ones, **no prices on the card**,
  no sort by price, no price of 0; U1–U5, U9, U12) and the prototype's `Directory.html`, `Home.html`,
  `Space details.html`;
- Issue #69.

## 3. The settled decisions (review them in "Stronger decisions")

- **D1 — the list is paged and filtered on the server (the owner: it must hold at a thousand
  spaces).** `GET /spaces` pages by the contract's §4 (20 by default); every filter applies before the
  page is cut: `area` (a list of area ids), the price (`period` with `priceMin` / `priceMax`, the
  general audience's price for that period, `period` required with a bound, bounds whole numbers above
  zero), `studentPrices`, `openFriday`, `verified`, `q`; the sort: recently updated, by name, and by
  distance (D2). **No `amenities` filter, no price sort, no `availableNow`** (live status is step 7:
  send nothing about it). This replaces the plan row's "whole filtered set in one request".
- **D2 — "near me" sorts on the server, so the location reaches the API (the owner's decision, which
  changes a v1 commitment).** The overview and foundation §13 say the device's location is never sent;
  with paging, the server must sort by distance. Settle in the plan, as rules whose reason is privacy
  (security.md owns them): the device sends its coordinates only to sort, **rounded on the device**
  (state the precision and why); the API **never stores or logs them** (the request log's redaction
  covers the query; prove it); no cache keeps them; a distance is answered per space, straight-line,
  labelled approximate. Update `overview.md` (*Directory* / *Near me*: the owner's change, dated),
  foundation §13's rule, and security.md. The prototype's privacy line («يبقى موقعك على جهازك فقط…»)
  becomes untrue: the analyst routes its wording to the design archive — say so in the report.
- **D3 — the map has its own light read:** `GET /spaces/pins` (or the plan's better name) answers the
  **whole** filtered set (the same filters as the list, no paging), each pin with only what a pin and
  its selected card need (id, slug, display names, location, verified); settle a ceiling and what
  happens past it (for example a viewport's bounds), so it too holds at a thousand.
- **D4 — the card has no prices** (the owner): a list item carries the display names, the area's
  names, verified, the week's opening ranges (D5), the distance when sorted by it, and what the card
  shows of freshness, nothing more; no photo (photos are a later decision).
- **D5 — the week's hours go to the device,** which computes "today" in Asia/Gaza at view time (a
  cached list may cross midnight); `openFriday` is derived from the same ranges on the server.
- **D6 — search tolerates the way people type** (the owner: "as forgiving as possible, even with a
  typo"): `q` matches both names and the area's names in both languages; Arabic is normalised (أ إ آ →
  ا, ة → ه, ى → ي, tashkeel and tatweel removed) and the match is **typo-tolerant** (similarity, not
  only containment), ranked by how well it matches when `q` is given. Recommended: PostgreSQL's
  `pg_trgm` over normalised text (one migration: the extension, any normalised column and its index —
  allowed: no other item changes the schema now); weigh it against an in-app similarity in the plan,
  at a thousand spaces.
- **D7 — the list is cached briefly** (a short `Cache-Control` and a validator, so an unchanged list
  is not downloaded again); never a response that holds a location (D2).
- **D8 — a space's page:** `GET /spaces/:slug` answers a publicly listed space only (else
  `not_found`): the profile (both names, descriptions, area, address, landmark, location), the hours
  with the shifts, the prices by audience (a stale price of an unverified space hidden, as the data
  model says), the common and own amenities as one list, the contacts, each group's freshness, and
  verified. **No capacity, no counts, no live status, no announcements** (steps 7 and 10).
- **D9 — Issue #69** in its own commit: the contract's prices line names both refusals
  (`out_of_range` outside the range, `invalid_format` when not an integer). Closes #69.

## 4. Findings

Read the open findings' titles; open those that touch listing, search, time or privacy. Your new
findings number **61–62**.

## 5. Risks

- **Privacy (D2):** the coordinates in a query string pass through the request log, proxies and the
  cache — prove none keeps them (a test on the log's redaction; `no-store` or no cache on that answer).
- **Paging under sort by distance and by similarity:** the total and every page right, stable order
  on ties.
- **The migration (D6, if `pg_trgm`):** Neon must support the extension (it does; say so with its
  documentation); create it once with `migrate dev --create-only`, then `ls`; on data loss it refuses:
  `migrate diff --script`.
- **The machine (the owner's rule):** **one full test run at a time on this machine.** Before a full
  lane (`test:api`, `test:component`), check that worker A is not running one (the main folder); if it
  is, wait.

## 6. Boundaries with the other workers

- **Worker A** builds the admin's space editor (web) in the main folder: `apps/web`, no
  `packages/shared` change. You touch nothing in `apps/web` (unless a shared type you change breaks
  it: declare it in the plan). `spaces.md`'s *API* parts are yours, its *Web* parts A's; the overview's
  *Built* line is shared (fast path).
- **Two design fixers** work in `docs/design/` only; you touch nothing there.
- Test files that change because a shared type changes are listed in the plan too.
- No new dependency (declare one in the plan if fuzzy search truly needs it — `pg_trgm` is an
  extension, not a dependency).

## 7. Checks, the pull request and the report

- **Locally, once each on the head, one at a time:** `test:unit`, `test:api`; `lint`, `typecheck`,
  `format:check`, `check:links`; `test:component`, the build and `check:build` only if a shared type
  reaches the web (say why if not run).
- **Real requests** against 3321, each in the report: the list's first and second page with two
  filters; a search with a typo and with mixed hamzas finding the space; a sort by distance (and the
  request log showing no coordinates); the pins for the same filters; a space's page, and a hidden one
  answering 404; the cache's validator answering 304 on a repeat.
- **PR:** title `feat(spaces): the public directory's API` (≤ 50), labels `feat`, `area:api`,
  `area:docs`, assigned to the owner, `Closes #69`. An independent review follows (privacy, a
  migration). Don't merge.
- **The documents:** the contract (the public endpoints, payloads, codes; §4 for the pins' exception;
  the prices line, D9); `spaces.md` (*API decisions*, *API history*, code map); the data model if a
  normalised column is added; security.md (D2); `overview.md` and foundation §13 (D2); the plan's API
  rows (D1–D3); the overview's *Built* line.
- At the report, `git merge-tree --write-tree` against every open PR. Stop every background shell
  you start; `jq` is not installed — use `gh … --jq`.
