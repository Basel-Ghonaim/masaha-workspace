# WEBBASE — one browser-storage layer, page titles, and two unstable tests (web)

**Worker A** · main folder `C:\Users\basel\masaha`, on `main` (`d7d800e`), tree clean · branch
`refactor/web-storage-titles`, cut with `git switch -c refactor/web-storage-titles origin/main` after
`git fetch --prune origin`. Databases `masaha_dev` / `masaha_test`; API on 3320, web on 5320. Its
`apps/web/.env` sets `NODE_ENV=development`: build with `NODE_ENV=production` before `check:build`.

**Model:** Sonnet 5.5, effort high. **Size cap:** at most 2 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\WEBBASE_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\WEBBASE_REPORT.md` (`final-report`).
**Screenshots:** `C:\Users\basel\Downloads\webbase-shots\` (never committed).
Follow the skills from start to end: `start-work-item`, `write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

While the design batches finish (the shell and the design-system items wait for them), the web takes
three pieces of groundwork that no design decision touches:
- **Issue #37 — one browser-storage layer** that every capability goes through (the owner's decision:
  build it now, not at a third use).
- **Finding 35 — every page has a document title,** in both languages.
- **Findings 47 and 42 — two component tests that fail now and then** in a full run.

## 2. Read first

In the order workflow §2 *Reading before work* gives.
- Issue #37 (`gh issue view 37`); findings 35, 47, 42 in full, and 28 and 6 (the earlier load
  failures) by title and resolution.
- `docs/frontend/architecture.md` §1–§4 (zones, the shared layer, session and preferences, *Where
  state lives*); `docs/frontend/localisation.md` (catalogues, the interface's language);
  `docs/frontend/design-system/foundation.md` §10 (the accessibility baseline); `docs/development/
  testing.md` (all); `docs/development/engineering-principles.md`.
- The code: `apps/web/src/shared/preferences/` (its platform port and how it guards blocked storage),
  `shared/routing/landing/lastSpace.ts`, `shared/session/repository/sessionHint.ts`,
  `src/test/fakeStorage.ts`; the routes and page groups (`pages/`, `shared/routing/`), the dashboard's
  `PageHeader` / `PageHeaderSlot` / `TopBar`, `apps/web/index.html`; the two tests named in findings
  47 and 42.

## 3. The settled decisions (review them in "Stronger decisions")

- **D1 — one storage layer, in `shared/`** (Issue #37). It owns the access to `localStorage` (and
  `sessionStorage` if a use needs it), the guard against blocked or throwing storage (the page works
  without it), and how a key is named. Every capability reaches browser storage only through it: the
  preferences and the last space move to it, and the test helper stubs it the way the code reaches it
  (a platform seam, never `vi.mock`). Settle in the plan: what it knows and does not know (values as
  strings, or typed per key; where the keys are declared), its API, and the rule that keeps a new use
  from bypassing it (a lint rule if one fits). **The keys already stored keep their names,** so no
  user loses a language or theme. The session hint cookie stays the session's (a cookie, not
  storage) unless the plan shows a reason. The PR closes #37; the rule goes into
  `frontend/architecture.md`.
- **D2 — a document title from one place** (finding 35). Each route says its title, and one place
  sets `document.title` (`{page} · مساحة` / `{page} · Masaha`, following the interface's language and
  changing with it); a page whose title is a record's name (a space) gives it itself; `index.html`
  has a default. The dashboard's top-bar title and the document title come from the same source where
  they can. Every built page, site and dashboard, gets one, in both catalogues. Add titles to the
  accessibility baseline (foundation §10).
- **D3 — finding 47:** the test waits for the chosen page's title (`findByRole('heading', { level: 1,
  name })` in the top bar), as its *Resolves when* says. Resolve it.
- **D4 — finding 42:** reproduce it (the lane run repeatedly and under load), find its cause, fix it;
  or show by repeated full runs that it does not recur, and say how many. Resolve it either way, with
  the evidence.
- **Not in this item:** finding 27 (the two chunks; the owner leaves it open), the shell, the design
  system's components.

## 4. Findings

Folded: 35, 47, 42. Your new findings number **55–56**.

## 5. Risks

- **Storage blocked:** the page must render and work with storage throwing on every call, as the
  preferences do today; test it.
- **A key renamed** loses every user's language and theme; D1 forbids it.
- **Unstable tests:** prove 47's and 42's fixes with repeated full component runs (say how many and
  the results), not one green run.

## 6. Boundaries with the other workers

- **The amenities worker** (`masaha-amenities`, its PR may open meanwhile) owns `features/lookups/`
  under its licence: you touch nothing there.
- **Worker B's PR #62** owns the two `shared/copy/*/errors.ts`: you touch neither.
- **The design fixer** works in `docs/design/` only.
- No new dependency (a lint rule uses what ESLint already has).

## 7. Checks, the pull request and the report

- **Locally, once each on the head, one at a time:** `test:unit`, `test:component`;
  `NODE_ENV=production npm run build` and `check:build`; `lint`, `typecheck`, `check:classes`,
  `format:check`, `check:links`. The API lane is not run (no API change); say so.
- **A real run** on 5320 (with the API on 3320): the tab's title on each page group in Arabic and
  English, changing with the language; the language and theme kept after a reload; the page working
  with storage blocked (the browser's site-data setting). Screenshots in the folder above. Stop the
  servers by PID and check the ports free.
- **PR:** title `refactor(web): storage layer and page titles` (≤ 50), labels `refactor`, `area:web`,
  `area:docs`, assigned to the owner, `Closes #37` in the description. The analyst reviews it.
  Don't merge.
- **The documents in this PR:** `frontend/architecture.md` (the storage rule, and the title's place),
  foundation §10, findings 35, 47 and 42 resolved with the index, the capability documents whose code
  maps change, overview's *Built* if a feature line changes.
- At the report, `git merge-tree --write-tree` against every open PR. Stop every background shell
  you start; `jq` is not installed — use `gh … --jq`.
