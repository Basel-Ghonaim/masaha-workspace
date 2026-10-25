# OWNER_SETUP — the owner sets up their space: profile, prices and packages, staff, settings (screens 20, 21, 22, 24) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, `git diff` between commits, read-only `gh`,
and reading files. Where you are unsure that something works, write it in the plan as **a check the
executor makes first, with what to do if it fails** — never try it yourself. Read only the files the plan
needs, each once.

**The task's folder:** `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\`. This prompt is `1_PLAN_PROMPT.md`;
**save the plan as `2_PLAN.md` here**; reports `4_REPORT_PR<n>.md`; screenshots `shots\pr<n>\`. If you are
Claude Code: use `write-plan` for its discipline (save the file; no plan-mode step is needed).

**Where you read.** Run your git commands from `C:\dev\masaha\app-design` (a detached worktree sharing the
repository's objects and branches) — commit objects only. Never check anything out. Worker A is executing
USERS in `C:\dev\masaha\app` and worker B DESK in `C:\dev\masaha\app-b` — never work in either.

## 0. The base: `origin/main` plus USERS, not merged yet

`origin/main` holds OWNERS (#88, #89, #91), STAFF (#90) and SETTINGS (#92): every API this item needs is
built — the managed space profile and its fact groups, photos, prices (`spaces`), packages (`packages`),
staff (`space-links` staff routes, the managed handover), the space's settings (`space-settings`) and
capacity (`occupancy`). **USERS** (`feat/admin-users`, in progress: local commits from `c7d089bc`) changes
pieces you will reuse — among them `DataTable cardsBelow`, the temporary password dialog's `kind:
'created' | 'issued'`, `RefusalText` moved to `shared/forms`, the users list's shared core. Plan from
`origin/main` **and** that branch (`git diff origin/main...feat/admin-users`); **the executor starts only
after USERS has merged**, and its first step is `git diff --name-status <the plan's USERS head>
origin/main` — a code file the plan names changed in a way it does not cover → stop and ask. Worker B's
DESK runs in parallel (`apps/api`, `packages/shared`, `docs`, and the two errors catalogues): name any
shared document as a likely text conflict. **Finding numbers:** the next free ones on the latest index —
write `<n>`.

## 1. The plan must stand alone

A fresh Claude Code conversation executes each PR, and another reviews it (split across two subagents).
Every decision with its one-line reason; the files; each component, hook, service, type and catalogue key
with its interface; the words in both languages (Arabic plurals through the catalogue's plural forms, O5);
each test with its lane, title and the break that must make it fail (`docs/development/testing.md` §3 —
**every break run and its red output recorded**); **each consequence-naming confirm, each disabled action
and each permission-dependent difference gets a deliberate break**; the commits, subjects counted (≤ 50);
fixes before the push folded; every new decision and history line ends with its date and `#PRNUM`; the
procedure with its commands (each branch from the latest `origin/main` in `C:\dev\masaha\app`; `docker start
masaha-postgres-1`, never `db:up`, never `npm ci`; one full test run at a time on this machine; per commit
`lint` + `typecheck`; on the head once `test:unit`, `test:component`, the production build then
`check:build`, `check:classes`, `format:check`, `check:links`; a real run on 3320/5320 signed in as the demo
owner (`demo-owner@example.com`, its password from `apps/api/.env`'s `SEED_DEMO_PASSWORD` — never printed),
with a browser tool that takes real screenshots — the `playwright` MCP tools if present, else local headless
Chrome over CDP — Arabic light and English dark, at 390, 768 and 1440; push; `gh pr create --assignee @me
--label feat --label area:web --label area:docs`; `gh pr checks` and `CLEAN`; the conflict check); a
**"Stop and ask"** list; the executor's stop rule (the same wording as
`C:\dev\masaha\workspace\WORKER_A\USERS\3_EXEC_PROMPT.md` §2, its break clause included); an appendix mapping
steps to Claude's skills, "only a map". Never merge; no tool attribution; stage by path.

## 2. The owner's decisions (2026-10-19)

1. **All four screens, one plan, two PRs in sequence:**
   - **PR 1 — the space profile and prices & packages** (build map step 5; screens 20, 21);
   - **PR 2 — staff and settings** (step 6's screen and the settings half of step 11; screens 22, 24).
   PR 2 is cut from `main` once PR 1 has merged.
2. **The profile is the admin's editor, one editor with two permissions** (`DECISIONS_OWNER.md` O1): the
   owner's page reuses the `spaces` editor; the differences come from the place, never a second editor —
   the head line, the prices as a link row to Prices & packages, the photos (O7), no capacity, no hide or
   delete. Who may edit what stays the server's (`adminWhileUnverifiedElseOwner`); the page shows it.
3. **Prices live in Prices & packages** (O6): on the owner's side prices are edited only there (the AD-008
   table with its own date and confirm, «الفترة», «لمن: الجميع · الطلاب»); the profile links to it. The
   admin's editor keeps its prices as today. Packages as O8 (the package sheet) and the API answers them.
4. **Settings — the attendance card «الحضور والحالة المباشرة»** (O2) is one card with **one save** that sends
   the two requests in order (capacity, then the settings); if the second fails the card says exactly what
   was saved and what was not, and the form keeps its values — **this resolves finding 96**. The card
   holds capacity, auto check-out at closing, the stay limit in whole hours; the other settings (rounding,
   the cap, student prices, the hand-typed price switch, the reminder) as the design and the API say.
   **The reminder template** is built: an editor with buttons inserting the three placeholders, its two
   refusals worded (a missing amount, an unknown placeholder).
5. **Staff** (OW-017, OW-018, OW-019, O4): add a receptionist in one submit, the consequence said first;
   then #89's one-time password dialog with the managed handover; «إيقاف وصوله» through an `AlertDialog`
   saying the sessions end; re-activation; a new temporary password only while one is pending; the badge
   «لم يغيّر كلمة المرور المؤقتة بعد»; every refusal the staff routes answer, worded.
6. **Claude Code throughout.**

**Your right to challenge (the owner's rule):** the decisions above, and any fixed rule you meet (an ADR, a
convention, a design decision), may be challenged. Build the plan on the decision as given and put your
better solution in a section **"Proposed alternatives"** — what, why, its cost, what changes if taken. Never
apply it yourself.

## 3. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`; `docs/frontend/architecture.md`;
`docs/frontend/design-system/foundation.md`; `docs/frontend/localisation.md`; `docs/features/spaces.md`,
`packages.md`, `space-links.md`, `users.md`, `space-settings.md`, `occupancy.md`; `docs/api/api-contract.md`
(the managed routes: space, photos, prices, packages, staff, settings, capacity; their codes); ADR 0009;
`docs/plans/v1-mvp.md` (steps 5, 6, 11); `docs/design/SCREENS.md` (20, 21, 22, 24) and their prototype screens
in `docs/design/`; `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` and `DECISIONS_SHARED.md`;
findings 96 and those on the editor; the code of `features/spaces` (the editor, photos, the admin's pages),
`features/space-links` (staff-free today), `features/users` (the password dialog), the owner's shell and
routes (`pages/dashboard`), and USERS' branch for the pieces it changes.

## 4. Boundaries

`apps/web` and `docs`. No API, shared-package, schema or dependency change — if one seems needed, stop and
put it in "Decisions needed". A design-system change only if a needed variant is truly missing — its own
commit, said in "Decisions needed".
