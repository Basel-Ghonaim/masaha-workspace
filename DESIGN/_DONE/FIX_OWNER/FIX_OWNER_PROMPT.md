# Design fix 5: the owner's management, in the prototype (plan for OpenCode to build)

**The planner** (Claude Code, Opus 5.5, effort high) · worktree `C:\Users\basel\masaha-design`, detached at `origin/main`
(`e30a86c`). **Plan only**: no branch, no edit. The build later uses branch `design/owner`, the prototype
served on **port 5346** (`python -m http.server 5346 --bind 127.0.0.1` from `docs/design/prototype`).
**Size cap:** at most 2 subagents, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_OWNER_PLAN.md`. **Report (the executor's):** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_OWNER_REPORT.md`.
**Before/after images:** `C:\Users\basel\Downloads\design-fix-owner` (never committed).
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

## The plan's sections (save it to `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_OWNER_PLAN.md`, then stop)

1. **Summary** and **contract** (scope, acceptance criteria as a checklist the reviewer will tick,
   out of scope).
2. **Reading done.**
3. **The decisions, as they will be built** — one block per decision (each O1-O13 item and each
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

Batch 5 of the design review (the owner's overview, space profile, packages and prices, announcements, staff, finance, settings, data reports and audit log) is decided. Plan its application to the prototype, as the owner amended it (O3: **no money on the overview**; DI-10: the phone's top bar; a package's price above zero; the editor boundary).

## 2. Read first

1. **The decisions:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_OWNER.md`: every *Amended* /
   *Decided* note first (they win), then O1-O13 and the smaller items. Apply only what is marked
   **prototype**; design-system, API, docs and web items are other workers'.
2. **Already settled:** `DECISIONS_SHARED.md` (P1-P10 as amended); `docs/design/CHANGES.md` (batches
   1, 2a, 2b and 3: what is built, and the patterns to reuse); `docs/design/README.md`, `INDEX.md`.
3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_OWNER_REPORT.md`.
4. **What the API holds:** `docs/features/spaces.md` (the groups, save and confirm, own amenities,
   prices above zero), `space-links.md`, `users.md`; the data model's *Spaces* and the desk's entities
   (packages, subscriptions, announcements, staff links); `docs/api/api-contract.md` for what is built
   and `docs/plans/v1-mvp.md`'s owner rows for what is planned. Issue #72 is **not** this batch's (it
   is in the admin's editor page).
5. **The rules:** `docs/frontend/design-system/foundation.md` §5, §7-§10, §12; `docs/project/glossary.md`;
   `docs/project/overview.md` (*Not in v1*).

## 6. Boundaries (the parallel-work rule)

- **The editor boundary (the owner's decision):** worker A is building the **admin's** space editor in code from `Admin space edit.html` and the shared `profile-a.jsx` / `profile-b.jsx`. **Change nothing the admin's editor shows.** O1's owner differences (prices as a link row, capacity moved to Settings by O2, no hide or delete, photos per O7) appear on `Owner space profile.html` only, behind a page-level prop or a separate component, never by changing a shared section's look for both. A defect you find in the shared editor is recorded as a design issue, not built. Do not touch `Admin space edit.html` (Issue #72 waits).
- **The account batch** (design worker in `masaha-design-b`, branch `design/account`) runs in parallel. Its files: the auth and account pages, `masaha/auth.jsx`, `account.jsx`, and **`masaha/shared.jsx`, which is theirs this round.** You edit none of them. If a decision needs `shared.jsx` (DI-10's top bar and the drawer's header live in `owner.jsx`), stop and say so in the plan.
- **The desk** (batch 6) follows this batch: do not edit `Desk.html`, `Customers.html`, `Customer file.html`, `Payments.html`, `My payments.html`, `desk-core.jsx`, `desk-sheet.jsx`, `desk-data.js`; if the overview needs a desk part, read it, do not change it.
- Shared by both design batches, each in its own section: `docs/design/CHANGES.md` (your batch's
  section), `INDEX.md` (your rows), the board `Flows - states.html` (your frames), `README.md`'s frame
  count. Whichever PR merges second rebases and keeps both sides (the fast path).
- Workers A and B work outside `docs/design/`.
- Your files: the owner's pages (`Owner overview.html`, `Owner space profile.html`, `Packages.html`, `Announcements.html`, `Staff.html`, `Finance.html`, `Owner settings.html`, `Data reports.html`, and an owner's audit page if O13 adds one), `masaha/owner.jsx`, `owner-data.js`, `finance.jsx`; `profile-a.jsx` / `profile-b.jsx` **only for the owner's own differences, shown on the owner's page alone**.
