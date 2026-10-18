# Review — PR #68 (WEBBASE: one browser-storage layer, page titles, two unstable tests)

You are an **independent reviewer** of PR #68 in the Masaha repository (Basel-Ghonaim/masaha).
Write your report to `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW68_<YOU>_REPORT.md`, where
`<YOU>` is your tool's name in capitals (`OPENCODE`, `CODEX`, `COPILOT`, `CLAUDE`).

## Rules

- **Run from `C:\Users\basel\masaha`**, but **read only commit objects** — that folder is worker A's
  and is checked out on this PR's branch; do not rely on its working tree. No edits, commits,
  checkouts, switches, installs, npm or test runs, database or Docker commands, no GitHub comments.
  `git fetch origin`, then pin to **the PR's current head** (`gh pr view 68 --json headRefOid`,
  written at the top of your report, checked again at the end). Base:
  `git merge-base origin/main <head>`. Use `git diff <base>...<head> -- <paths>` and
  `git show <head>:<file>`.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario,
  the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If unsure, say
  "plausible" and why.
- **No tool attribution** in what you write.

## What the PR must be (the owner's decisions)

Web and documents only. The approved plan is `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\WEBBASE_PLAN.md`
with its reply `PROMPT\WEBBASE_PLAN_REPLY.md`; the worker's report is `REPORT\WEBBASE_REPORT.md`.
- **One storage layer** (`apps/web/src/shared/storage/`, closes #37): `read` / `write` / `remove`
  over `localStorage`, reached inside the guard on every call; a blocked or throwing storage gives
  `null` and harmless writes; keys declared once (`STORAGE_KEYS`, typed `StorageKey`); values plain
  strings, each owner validating what it reads. **The stored key names are unchanged**
  (`masaha.language`, `masaha.theme`, `masaha.lastSpace.<userId>`). The preferences and the last
  space moved onto it; a lint rule forbids `localStorage` / `sessionStorage` elsewhere (exempt: the
  layer, `src/test`, test files). The session-hint cookie stays the session's. The pre-paint script in
  `index.html` is the documented exception.
- **Document titles** (finding 35): each route's handle declares its title; one `DocumentTitle` in the
  root layout sets `{page} · Masaha` / `{page} · مساحة`, following the language; `PageHeader` reads
  the same route title (no `title` prop); `index.html` has a default; a record-name title is a written
  rule served by the same place both read, built with its first page (D2b).
- **Finding 47:** the dashboard test waits for the chosen page's title by name. **Finding 42:** a toast
  is asserted only once visible (`findToast`), every toast test of that shape.
- **New finding 55** (a slow first lazy page under machine load).

## Look at these, in this order

1. **The storage layer's guard:** every path that can throw (reaching the global, `getItem`,
   `setItem`, `removeItem`, quota) is inside it; nothing captures `localStorage` at module load; the
   lint rule really catches `window.localStorage`, `globalThis.sessionStorage`, bare globals and
   destructuring, and its exemptions are only those named.
2. **No user loses a setting:** the key names, the values' format, and the pre-paint script reading
   the same keys as the layer writes.
3. **Titles:** every routed page has one in both catalogues (and the test that enforces it really
   walks every route); the language change updates the tab; `PageHeader` cannot disagree with the
   tab; a route with no title shows the name alone; D2b's rule can carry a record's name to both the
   top bar and the tab without rework.
4. **The first download:** the titles in the route definitions add no copy or dashboard code to the
   site's first chunk (`check:build`'s claims); architecture §3's widened sentence is true.
5. **The tests:** each would fail if its code broke; `findToast` waits for visibility, not presence;
   finding 47's helper requires the name; no `vi.mock`; the storage seam is the global the layer
   reaches. The worker's evidence for findings 42 and 47 (run counts) matches what the resolutions
   say.
6. **The documents:** frontend architecture (the storage rule, the title's place, §3), localisation,
   foundation §10, testing's seam sentence, findings 35, 42, 47 resolved and 55 new, the index — each
   true to the code, one home per fact.
7. **The commits:** four; **count each subject (≤ 50 characters)** — the first may be over.

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.
