# Design fix 6: the front desk, in the prototype (plan for OpenCode to build) — the last batch

**The planner** (Claude Code, Opus 5.5, effort high) · worktree `C:\Users\basel\masaha-design-b`,
detached at `origin/main` (`1240736`: batches 1–4 merged). **Plan only**: no branch, no edit. The
build later uses branch `design/desk`, the prototype served on **port 5347**
(`python -m http.server 5347 --bind 127.0.0.1` from `docs/design/prototype`).
**Size cap:** at most 2 subagents, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_DESK_PLAN.md`. **Report (the executor's):**
`C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_DESK_REPORT.md`.
**Before/after images:** `C:\Users\basel\Downloads\design-fix-desk` (never committed).
Use the `start-work-item` and `write-plan` skills for the reading and the plan's discipline, but this
prompt's §0 and its section list replace `write-plan`'s order where they differ.

**Batch 5 (the owner, PR #76, branch `design/owner`) is not merged yet** — it is taking a rebase and
three small fixes. The desk inherits its shell, its phone top bar (DI-10), its plurals (O5) and its
navigation. **Plan against batch 5 as it will merge:** read `origin/design/owner`'s files
(`git show origin/design/owner:<path>`) wherever the desk touches what batch 5 changed
(`masaha/owner.jsx`, `owner-data.js`, `finance.jsx`, the owner's pages), and say in the plan which
lines you relied on. **The executor cuts `design/desk` only once #76 has merged** (the plan's
procedure says so, with a check that `origin/main` contains it).

## 0. The way of working (as batch 5)

- **You write the plan, and only the plan.** You do not cut the branch, edit the prototype or open a
  PR.
- **OpenCode builds it from your plan alone**, then **another OpenCode session reviews** the PR
  against it. Neither has your conversation, the decision files' context or Claude's skills.
- **So the plan is an execution script a careful agent follows without judgment:** every decision
  taken; every change named to the file and the place in it; every new word written out in Arabic
  **and** English; every component, variant and token named; every frame to check given as a URL with
  its parameters and widths. Where a choice remains, take it and say why. Nothing is "as
  appropriate", "if needed" or "similar to"; when the plan points at existing code, it quotes the
  lines or names the function.

## The plan's sections (save to the path above, then stop)

1. **Summary** and **contract** (scope, acceptance criteria as a checklist the reviewer will tick,
   out of scope).
2. **Reading done.**
3. **The decisions, as they will be built** — one block per decision (K1–K8, each smaller DK item
   marked *prototype*, and the routed items below), with: the files; the exact change in each; the
   exact Arabic and English strings; the components and tokens; the states (loading, empty, error,
   pending, success, 429, offline) where the decision touches them; the URL parameters added or
   renamed.
4. **Stronger decisions** and **design issues** found while planning, each with a recommendation —
   the owner answers them before the build; the plan says what to do under each answer.
5. **The files**, each with who owns it, and the boundaries (§6 below).
6. **The commits**, in order: each subject (≤ 50 characters, **counted**, `docs(design): …`), the
   files it holds, its `CHANGES.md` line written out in full, and the `INDEX.md` rows it adds.
7. **The executor's procedure, step by step:** the check that #76 is in `origin/main`; the branch
   command; the server command; the check scripts at every commit; the frames to open after each
   commit (URL, widths 390 / 768 / 1440, Arabic and English, light and dark) and **what to look for in
   each**; the before/after images (names, folder); `format:check` / `check:links` (this folder has
   no `node_modules`: say that CI runs them, or how to run them); the push; the PR command
   (`gh pr create --assignee @me --title ... --label docs --label area:docs --body-file ...`) with the
   **PR description written out**; waiting for CI and `CLEAN` (`gh pr checks <n>`,
   `gh pr view <n> --json mergeStateStatus`); the report's file and its sections (the PR and head, the
   commits, what was run, problems met, anything unexpected, the conflict check with
   `git merge-tree --write-tree` against every open PR, departures); stopping every server, browser
   and background shell, and checking the port free. Never merge. `jq` is not installed: use
   `gh ... --jq`.
8. **The reviewer's checklist:** for each acceptance criterion and decision, the file and what to
   verify, and the frames to open; plus the hazards below.
9. **The hazards** an executor must not trip on (write them out):
   - **Babel's shared globals:** every page's scripts share one global scope: no object rest
     destructuring (`{ a, ...rest }`) anywhere (its `_excluded` helper is page-wide, DI-27); no
     top-level `name` or other generic top-level names; each new top-level name defined once per page
     (grep before adding); `O` is already global where `owner.jsx` loads.
   - **Hooks:** called unconditionally and before any early return (batch 5 fixed a
     `useIsTablet() && !useIsDesktop()` crash in `OwnerShell`; do not reintroduce the pattern).
   - **The prebuilt CSS:** a utility class not in `_ds_bundle.css` is silently dead; layout-only rules
     go to `masaha.css`, tokens only; `check-classes.mjs` must pass, and classes chosen in conditions
     are checked by eye.
   - **The vendored bundle** (`prototype/_ds/`, `_vendor/`) is never edited.
   - **Truth to the API and the data model:** nothing on screen the API or the data model cannot hold;
     **live status is a state, never a public count** (ADR 0008; the desk's own counts are private);
     money is never hidden (K4); a payment is never deleted, only voided with who and why.
   - **Look with your eyes:** the scripts see blanks and errors, not layout.

## 1. The task in brief

Batch 6 of the design review — **the front desk** (the desk itself, check-in and check-out, visits,
the money block, customers and their file, subscriptions and renewals, payments and «دفعاتي اليوم»)
— is decided. Plan its application to the prototype. **It is the last batch:** after it, the
screenshots in `docs/design/screens/` are regenerated once and the owner reviews every screen.

## 2. Read first

1. **The decisions:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_DESK.md` (K1–K8 and the smaller
   DK items). Apply only what is marked **prototype**; design-system (DK-024 with OW-010), API and docs
   items are other workers'.
2. **Already settled:** `DECISIONS_SHARED.md` with its amendments (**P1:** the desk's «تسجيل زيارة» is
   the phone's one bottom-bar action; **P8:** the desk keeps its success toasts, every money action one
   with its amount (K7); **P9:** archiving a customer — settled at once with «تراجع», owing through an
   `AlertDialog` naming the debt); `DECISIONS_OWNER.md` (the shell and DI-10 the desk inherits; O3's
   «زيارات لم تُحصَّل» → the desk); `docs/design/CHANGES.md` (batches 1–5: what is built, the patterns
   to reuse); `docs/design/README.md`, `INDEX.md`.
3. **Routed to this batch by batch 5** (`PLAN\FIX_OWNER_PLAN.md` lines ~1141–1142,
   `REPORT\FIX_OWNER_REPORT.md`): **DI-35** — the desk's uncollected card gets `id="unpaid"` and the
   owner overview's link becomes `Desk.html#unpaid`; **DI-36** — `Payments.html` reads `?month=YYYY-MM`
   and Finance's «عرض الكل» carries it. Plan both (the owner overview's and Finance's link changes are
   one-line edits to batch 5's files once merged: say so).
4. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_DESK_REPORT.md`.
5. **What the API and the data model hold:** the data model's desk entities (customers, packages,
   subscriptions, visits, payments, the ledger's rules), ADR 0010 (a manual, append-only ledger),
   ADR 0015 (idempotency, the database owns the ledger's rules), ADR 0009 (who may do what at the
   desk; its table), ADR 0008; `docs/api/api-contract.md` and `docs/plans/v1-mvp.md` steps 7–9 for what
   is planned; `docs/project/overview.md` (*Not in v1*: no online payment, no QR check-in, no booking).
6. **The rules:** `docs/frontend/design-system/foundation.md` §5, §7–§10, §12, §13 (the desk's
   screens); `docs/project/glossary.md`.

## 6. Boundaries

- **Your files:** `Desk.html`, `Customers.html`, `Customer file.html`, `Payments.html`,
  `My payments.html`, `masaha/desk-core.jsx`, `desk-sheet.jsx`, `desk-data.js`; and, **only after #76
  merges and only for DI-35 and DI-36's links**, one line each in `Owner overview.html` and
  `Finance.html` (or `finance.jsx`). Anything else in batch 5's files that the desk seems to need:
  stop and say so in the plan.
- **Never edited:** `shared.jsx`, `auth.jsx`, `account.jsx` and the account pages (batch 4, merged);
  `Admin space edit.html` and `profile-a.jsx` / `profile-b.jsx` (worker A builds the editor in code);
  `admin.jsx` and the admin's pages; `_ds/`, `_vendor/`; `docs/design/screens/`; anything outside
  `docs/design/`.
- Shared archive files, your section only: `CHANGES.md` (batch 6), `INDEX.md` (your rows, section
  56), the board `Flows - states.html` (your frames, placed after batch 5's section 55 without
  overlap), `README.md`'s counts (counted from the frames, not added by hand).
- No other design batch runs; workers A, B and the media worker work outside `docs/design/`.
- Issue #72 (the admin editor page's DI-27 comment) is **not** this batch's.
