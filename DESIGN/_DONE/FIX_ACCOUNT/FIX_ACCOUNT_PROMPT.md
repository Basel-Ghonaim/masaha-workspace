# Design fix 4: the account and signing in, in the prototype (plan for OpenCode to build)

**The planner** (Claude Code, Opus 5.5, effort high) · worktree `C:\Users\basel\masaha-design-b`, detached at `origin/main`
(`e30a86c`). **Plan only**: no branch, no edit. The build later uses branch `design/account`, the prototype
served on **port 5347** (`python -m http.server 5347 --bind 127.0.0.1` from `docs/design/prototype`).
**Size cap:** at most 2 subagents, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_ACCOUNT_PLAN.md`. **Report (the executor's):** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_ACCOUNT_REPORT.md`.
**Before/after images:** `C:\Users\basel\Downloads\design-fix-account` (never committed).
Use the `start-work-item` and `write-plan` skills for the reading and the plan's discipline, but this
prompt's §0 and its section list replace `write-plan`'s order where they differ.

## 0. The new way of working (read this first)

This batch is built in a new way, to save tokens:
- **You (Claude Code, Opus 5.5, effort high) write the plan, and only the plan.** You do not cut the
  branch, edit the prototype or open a PR.
- **Another agent (OpenCode) builds it from your plan alone**, then **another OpenCode session reviews**
  the PR against it. Neither has your conversation, the decision files' context or Claude's skills.
- **So the plan must be an execution script that a careful agent can follow without judgment:**
  every decision taken, every change named to the file and the place in it, every new word written
  out in Arabic **and** English, every component, variant and token named, every frame to check given
  as a URL with its parameters and widths. Where a choice remains, take it in the plan and say why.
  Nothing is "as appropriate", "if needed" or "similar to"; when the plan points at existing code, it
  quotes the lines or names the function.

## The plan's sections (save it to `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_ACCOUNT_PLAN.md`, then stop)

1. **Summary** and **contract** (scope, acceptance criteria as a checklist the reviewer will tick,
   out of scope).
2. **Reading done.**
3. **The decisions, as they will be built** — one block per decision (each C1-C8 item and each
   *Amended* / *Decided* note), with: the files; the exact change in each (what to add, remove or
   replace, where); the exact Arabic and English strings; the components and tokens; the states
   (loading, empty, error, pending, success, 429) where the decision touches them; the URL parameters
   added or renamed.
4. **Stronger decisions** and **design issues** found while planning, each with a recommendation —
   the owner answers them before the build; the plan says what to do under each answer.
5. **The files**, each with who owns it, and the boundaries (§6 below).
6. **The commits**, in order: each subject (≤ 50 characters, counted, `docs(design): …`), the files
   it holds, its `CHANGES.md` line written out in full, and the `INDEX.md` rows it adds.
7. **The executor's procedure, step by step:** the branch command; the server command; the check
   scripts' commands at every commit; the frames to open after each commit (URL, widths 390 / 768 /
   1440, Arabic and English, light and dark) and **what to look for in each**; the before/after images
   (names, folder); `format:check` / `check:links` (or why not); the push; the PR command
   (`gh pr create --assignee @me --title ... --label docs --label area:docs --body-file ...`) with the
   **PR description written out** (Summary, Scope / Acceptance criteria / Out of scope, Change type,
   Evidence, Screenshots, Definition of Done checklist); waiting for CI and `CLEAN`
   (`gh pr checks <n>`, `gh pr view <n> --json mergeStateStatus`); the report's file and its sections
   (the PR and head, the commits, what was run, problems met, anything unexpected, the conflict check
   with `git merge-tree --write-tree` against every open PR, departures); stopping every server,
   browser and background shell, and checking the port free. Never merge. `jq` is not installed in
   Git Bash: use `gh ... --jq`.
8. **The reviewer's checklist:** for each acceptance criterion and decision, the file and what to
   verify, and the frames to open; plus the hazards below.
9. **The hazards** an executor must not trip on (write them out):
   - **Babel's shared globals:** every page's scripts share one global scope: no object rest
     destructuring (`{ a, ...rest }`) anywhere (its `_excluded` helper is a page-wide global), and no
     top-level `name` or other generic top-level names; `README.md`'s check-scripts paragraph says so.
   - **The prebuilt CSS:** a utility class not in `_ds_bundle.css` is silently dead: layout-only rules
     go to `masaha.css`, with tokens only; `check-classes.mjs` must pass.
   - **The vendored bundle** (`prototype/_ds/`, `_vendor/`) is never edited.
   - **Truth to the API and the data model:** nothing on screen the API cannot do; live status is a
     state, never a count.
   - **Look with your eyes:** the scripts and a load matrix see blanks and errors, not layout: #59's
     F2 and #61's eleven fixes were found by eyes.

## 1. The task in brief

Batch 4 of the design review (signing in, registering, the forgotten password, the forced change, «إعدادات حسابي», the favourites, «بلاغاتي», the account menu) is decided. Plan its application to the prototype, as the owner amended it on 2026-10-13 (C5's forced-change line).

## 2. Read first

1. **The decisions:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ACCOUNT.md`: every *Amended* /
   *Decided* note first (they win), then C1-C8 and the smaller items. Apply only what is marked
   **prototype**; design-system, API, docs and web items are other workers'.
2. **Already settled:** `DECISIONS_SHARED.md` (P1-P10 as amended); `docs/design/CHANGES.md` (batches
   1, 2a, 2b and 3: what is built, and the patterns to reuse); `docs/design/README.md`, `INDEX.md`.
3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_ACCOUNT_REPORT.md`.
4. **What the API and the web already do:** `docs/features/auth.md`, `users.md` (the forced change,
   the reset by email, Google; #62's admin-issued temporary password); the API contract's *Session*,
   *Me* and *The forgotten password*; the built web screens these pages mirror (C3, C5, AC-017 and
   AC-019 are in built code: the prototype catches up). Nothing is installed in `masaha-design-b`:
   `format:check` and `check:links` run in CI; the plan's procedure says so.
5. **The rules:** `docs/frontend/design-system/foundation.md` §5, §7-§10, §12; `docs/project/glossary.md`;
   `docs/project/overview.md` (*Not in v1*).

## 6. Boundaries (the parallel-work rule)

- **The owner's batch** (design worker in `masaha-design`, branch `design/owner`) runs in parallel. Its files: the owner's pages (`Owner overview`, `Owner space profile`, `Packages`, `Announcements`, `Staff`, `Finance`, `Owner settings`, `Data reports`), `masaha/owner.jsx`, `owner-data.js`, `finance.jsx`, `profile-a.jsx`, `profile-b.jsx`. **You edit none of them.** `shared.jsx` is yours this round; it does not touch it.
- Shared by both design batches, each in its own section: `docs/design/CHANGES.md` (your batch's
  section), `INDEX.md` (your rows), the board `Flows - states.html` (your frames), `README.md`'s frame
  count. Whichever PR merges second rebases and keeps both sides (the fast path).
- Workers A and B work outside `docs/design/`.
- Your files: `Sign in.html`, `Register.html`, `Forgot password.html`, `Reset password.html`, `Change password.html`, `Settings.html`, `Favorites.html`, `Reports.html`, `Reset email.html`, `masaha/auth.jsx`, `masaha/account.jsx`, and **`masaha/shared.jsx` (yours in this round: the account menu, C6)**.

## 7. One addition, the owner's (2026-10-13)

The public directory's "near me" now sorts on the server, so the device's location reaches the API
(rounded on the device, never stored or logged; see `DECISIONS_PUBLIC.md`'s *Changed 2026-10-13*
note). The privacy line `PRIVACY_LINE` in `masaha/shared.jsx` («يبقى موقعك على جهازك فقط، ولا يُرسَل إلى
أي جهة.» / "Your location stays on your device and is never sent anywhere.") becomes untrue. You own
`shared.jsx` this round: plan its true wording (Arabic and English) and every place it shows, as its
own commit.
