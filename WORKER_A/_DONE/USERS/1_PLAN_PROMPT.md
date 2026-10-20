# USERS — the admin's users page (screen 29) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, `git diff` between commits, read-only `gh`,
and reading files. Where you are unsure that something works, write it in the plan as **a check the
executor makes first, with what to do if it fails** — never try it yourself. Read only the files the plan
needs, each once.

**The task's folder:** `C:\dev\masaha\workspace\WORKER_A\USERS\`. This prompt is `1_PLAN_PROMPT.md`; **save
the plan as `2_PLAN.md` here**; the report `4_REPORT_PR1.md`; screenshots `shots\`. If you are Claude Code:
use `write-plan` for its discipline (save the file; no plan-mode step is needed).

**Where you read.** Run your git commands from `C:\dev\masaha\app-design` (a detached worktree; it shares
the repository's objects and branches) — commit objects only: `git show <ref>:<path>`, `git ls-tree`,
`git grep <ref>`. Never check anything out. Worker A is executing OWNERS PR 3 in `C:\dev\masaha\app` and
worker B SETTINGS in `C:\dev\masaha\app-b` — never work in either.

## 0. The base: `origin/main` plus OWNERS PR 3, not merged yet

This item **builds on OWNERS PR 3** (`feat/admin-owner-links`, in progress: local commits `aa0c8a4e`
#89's leftovers, `0ee60d62` linking and unlinking, `02cc70ae` the editor names its owners — it may still be
fixed, pushed and reviewed). Plan from `origin/main` **and** that branch: `git diff origin/main...feat/admin-owner-links`,
`git show feat/admin-owner-links:<path>`. **The executor starts only after PR 3 has merged**; its first step
is `git diff --name-status <the plan's PR 3 head> origin/main` — a code file the plan names changed in a
way the plan does not cover → stop and ask. Worker B's SETTINGS (`apps/api`, `packages/shared`, `docs`)
runs in parallel: name any shared document you edit as a likely text conflict. **Finding numbers:** 94
onward are being taken by PR 3 and SETTINGS — the plan writes `<n>`; the executor takes the next free
numbers from the index on the latest `origin/main`.

## 1. The plan must stand alone

A fresh Claude Code conversation executes it (Opus), and another Claude Code conversation reviews it.
Every decision with its one-line reason; the files; each component, hook, service, type and catalogue key
with its interface; the words in both languages; each test with its lane, title and the break that must
make it fail (`docs/development/testing.md` §3 — **every break run and its red output recorded**); **each
consequence-naming confirm and each disabled action gets a deliberate break**; the commits, subjects
counted (≤ 50); fixes before the push folded (`--fixup` + autosquash, `GIT_SEQUENCE_EDITOR=:`); every new
decision and history line ends with its date and `#PRNUM`; the procedure with its commands (the branch from
the latest `origin/main` in `C:\dev\masaha\app`; `docker start masaha-postgres-1`, never `db:up`, never
`npm ci`; one full test run at a time on this machine; per commit `lint` + `typecheck`; on the head once
`test:unit`, `test:component`, the production build then `check:build`, `check:classes`, `format:check`,
`check:links`; a real run on 3320/5320 with a browser tool that takes real screenshots — the `playwright`
MCP tools if present, else local headless Chrome over CDP — Arabic light and English dark, at 390, 768 and
1440; push; `gh pr create --assignee @me --label feat --label area:web --label area:docs`; `gh pr checks`
and `CLEAN`; the conflict check); a **"Stop and ask"** list; the executor's stop rule (**a test it cannot
run stops the work** — the same wording as `C:\dev\masaha\workspace\WORKER_A\OWNERS\3_EXEC_PROMPT_PR3.md`
§2); an appendix mapping steps to Claude's skills, "only a map". Never merge; no tool attribution; stage by
path. **One PR** (the owner's choice) — if the plan finds more than about 60 files, say so in "Decisions
needed" rather than cutting it yourself.

## 2. The owner's decisions (2026-10-19)

1. **The whole screen 29, as the design decided** (`DECISIONS_ADMIN.md` A5, A7, AD-021; DI-24):
   - the list: search (name or email), the role and state filters, the address kept in the URL, pages,
     the empty and no-match states; rows become **cards at 768** (A7); each person's **reception desks**
     shown (DI-24 — `AdminUserRow.receptionSpaces`, #90) beside their owned spaces;
   - each row's actions: **suspend / restore**; **change the role** — «مستخدم» or «أدمن» only («مالك» is
     derived from the links, ADR 0009 rule 2), to or from «أدمن» through an `AlertDialog` naming the
     consequence; **issue a temporary password** — then #89's one-time password dialog (no X, no Escape,
     «تم» after «نسخ», the handover) — disabled with its reason for a Google-only account (AD-021) and
     wherever the API refuses it; **«ربط بمساحة»** from the person — PR 3's link dialog, person side;
   - every refusal the API can answer worded in both catalogues (among them `ACCOUNT_PASSWORD_PENDING`
     on a role change to admin or a link, #90).
2. **Finding 88 resolved here:** the add-owner upgrade confirm also shows the account's reception desks
   (the data is now in `AdminUserRow`). Finding 89 stays open.
3. **One PR**, Claude Code throughout.

**Placement:** judge every file's capability by the rule, not the screen (the users list already lives in
`features/space-links` from OWNERS PR 1 — O2; the temporary password and the handover in `features/users`
from #89; linking in `space-links` from PR 3). Say where each new piece goes and why; reuse, never copy.

## 3. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`; `docs/frontend/architecture.md`;
`docs/frontend/design-system/foundation.md` (the components, the list patterns, §12); `docs/frontend/localisation.md`;
`docs/features/users.md`, `space-links.md`; `docs/api/api-contract.md` (*Users (the admin)*, *Owners (the
admin)*, the error codes); ADR 0009, 0013; `docs/design/SCREENS.md` (29) and the users screen's prototype
in `docs/design/`; `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` and `DECISIONS_SHARED.md`
(P1, P8); the OWNERS plan `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` (its patterns, its words, its
approval note) and PR 3's code; findings 82, 88, 89; the code of `features/space-links` (users list, owners
list, link dialog, owner actions), `features/users` (repository, the password dialog), and the admin pages
and routes.

## 4. Boundaries

`apps/web` and `docs`. No API, shared-package, schema or dependency change — if one seems needed, stop and
put it in "Decisions needed". Design-system changes only if a needed variant is truly missing — its own
commit, said in "Decisions needed".
