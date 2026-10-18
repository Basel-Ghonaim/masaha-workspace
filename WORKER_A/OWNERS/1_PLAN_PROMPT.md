# OWNERS — the admin's owners page, adding and linking an owner, the editor naming its owners (web) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, read-only `gh`, and reading files. Where you
are unsure that something works, write it in the plan as **a check the executor makes first, with what to
do if it fails** — never try it yourself. Read only the files the plan needs, each once.

**The task's folder:** `D:\masahaWorkspace\WORKER_A\OWNERS\`. This prompt is `1_PLAN_PROMPT.md`; **save
the plan as `2_PLAN.md` here**; the executor's report will be `4_REPORT.md`, its screenshots in
`shots\`. Never write to `C:\Users\basel\.prompt` or `Downloads\masaha-next` (frozen). If you are Claude
Code: use `write-plan` for its discipline (it saves to `2_PLAN.md` above).

**Where you read.** `C:\Users\basel\masaha` (worker A's folder, on `main`, idle): `git fetch origin`, then
read only `origin/main`'s commit objects (`git show origin/main:<path>`, `git ls-tree`, `git grep`). Never
check anything out. Worker B is planning PACKAGES in `C:\Users\basel\masaha-b` — never work there.

## 0. The base and the parallel item

You plan from today's `origin/main` (`5e8c979d` or later: #84, #85 and #86 merged). Worker B's PACKAGES
(the owner's packages API: `apps/api`, `packages/shared`, `docs`) may run or merge meanwhile. The
documents both items may edit — `docs/project/overview.md`, `docs/architecture/findings/README.md`,
perhaps `docs/api/api-contract.md` — are **shared: re-read on the latest `origin/main` before editing; a
conflict there is documents-only**. The executor's first step: `git diff --name-status <the plan's base>
origin/main`; a change to a code file the plan names that the plan does not cover → stop and ask; if
`packages/shared` changed, `npm run build -w @masaha/shared` before any web check (a stale `dist` once
hid a CI failure).

## 1. The plan must stand alone

A fresh conversation executes it — Claude Code, OpenCode or another agent — and another tool reviews. So:
every decision with its one-line reason; the files; each new hook, component, service and type with its
interface (inputs, what it returns or renders, the query keys it reads or invalidates); every user-facing
string in Arabic and English with its catalogue key; each state named to the design system's components;
each test with its lane, title and the break that must make it fail (`docs/development/testing.md` §3 —
**every break run and its red output recorded in the report**); the commits, subjects counted (≤ 50); a fix
before the push folds into its commit (`git commit --fixup` + `git rebase -i --autosquash` with
`GIT_SEQUENCE_EDITOR=:`); every new decision and history line ends with its date and **`#PRNUM`**, replaced
just before the push (issues and PRs share one sequence; check the highest number then — worker B's
PACKAGES may take the next one); the procedure with its commands (branch `feat/admin-owners` from the
latest `origin/main` in `C:\Users\basel\masaha`; `docker start masaha-postgres-1`, never `db:up`; never
`npm ci` there while VS Code is open; **one full test run at a time on this machine** — check worker B's
folder runs none; per commit `lint` and `typecheck`; on the head **once** `test:unit`, `test:component`,
`NODE_ENV=production npm run build`, `check:build`, `check:classes`, `format:check`, `check:links` — the
owner's rule: no lane re-run unless a file it covers changed after it passed; a real run on 5320 with the
API on 3320 driven by the **`playwright` MCP tools**, screenshots saved to this task's `shots\` (the tool
resolves a relative name from the session's folder: move the files there at the end and check
`git status` is clean); push; `gh pr create --assignee @me --label feat --label area:web --label
area:docs` with the description written out; `gh pr checks` and `CLEAN`; the conflict check with
`git merge-tree --write-tree` against any open PR; the report to `D:\masahaWorkspace\WORKER_A\OWNERS\4_REPORT.md`,
UTF-8, written in parts); a **"Stop and ask"** list; an appendix mapping steps to Claude's skills, "only a
map". No step may depend on a Claude skill. Never merge; no tool attribution; stage by path.

## 2. The task — the owner's decisions (2026-10-17)

The API is built (PRs #60, #62, #67, #82): `GET /admin/users` (`?q=&role=owner&state=`, `AdminUserRow`
with its active owner links), `POST /admin/owners` (`AddedOwner`, the temporary password once),
`POST /admin/users/:userId/temporary-password/handover`, `POST /admin/spaces/:spaceId/owners`,
`DELETE /admin/spaces/:spaceId/owners/:userId`, and `AdminSpace.owners` on the single-space read. The
design system has `Combobox`, `Dialog`, `AlertDialog`, `DataTable`. **Nothing in `apps/api` or
`packages/shared`; if the web needs a change there, stop and say so.**

- **D1 — scope: the owners half only** (the owner split the item; a later USERS item takes the users page:
  the role change, suspension, the temporary password and AD-021):
  1. **The owners page (A6):** a view of `GET /admin/users?role=owner`, each owner's spaces in the row,
     with the users list's search and state filter (built here so USERS reuses it).
  2. **Adding an owner (A5):** one space at a time (a `Combobox`); the line before the act — «سيُنشأ
     حساب ويظهر رمز مرور مؤقت مرة واحدة — جهّز طريقة تسليمه» for a new email, «سيُرقّى حسابه» for an
     existing one (`upgradeExisting`); the submit «إنشاء حساب وربط»; the refusals `ACCOUNT_IS_ADMIN`,
     `ACCOUNT_SUSPENDED`, `ALREADY_OWNER` worded on their field or form.
  3. **The one-time password dialog (A5):** no X, no Escape, no outside click; «تم», enabled only after
     «نسخ», is its only way out; it asks how the password was handed over (واتساب · شفهيًا · أخرى) and
     sends the handover. **Built so USERS reuses it** for an issued temporary password — say where it
     lives and why (the frontend's dependency rule decides).
  4. **One way to link (A4)** — from a space: a `Combobox` of **one person** (owners and users by name or
     email; suspended and admin accounts excluded; each option says what it is); from a person (the
     owners page row): a `Combobox` of **one space** (its state and current owner shown). Both say the
     consequence before the act («تصبح موثّقة ويعدّلها مالكها»). The refusals (`ACCOUNT_IS_ADMIN`,
     `ACCOUNT_SUSPENDED`, `RECEPTION_LINK_ACTIVE`, `invalid_choice`) worded.
  5. **Unlinking (A4, finding 59):** «فك ربط {name}», one item per owner, an `AlertDialog`, destructive
     (P9), saying the consequence («تصبح غير موثّقة وتختفي حالتها المباشرة» when it is the last owner).
  6. **The editor names its owners (finding 59):** the verified space's notice «يعدّلها {names}» from
     `AdminSpace.owners`, with the unlink items; and from an unverified space's editor, the link action.
     **Finding 59 Resolved** (status, dated resolution, the index, the capability documents).
- **D2 — where the code lives, by the capability that owns each rule:** the users list's read, row, search
  and filters in `features/users` (both pages use them); the link, unlink and add-owner dialogs and hooks
  in `features/space-links` (it owns the linking rules); the page in `pages/dashboard/admin/`, replacing
  the current owners route's placeholder if there is one (read `navigation.ts` and `routes.tsx`).
- **D3 — finding 50 on screen:** an `OWNER` row with no spaces (the API leaves out soft-deleted spaces, so
  an owner whose spaces are all deleted reads as an owner of none) shows «كل مساحاته محذوفة — استرجع
  المساحة لفك ربطه», linking to the admin's spaces list at `?status=deleted`. No API change. Add a dated
  line to finding 50 (it is already Resolved in documents; this is its screen).
- **D4 — commit 0, #85's leftovers** (`D:\masahaWorkspace\WORKER_A\_DONE\GALLERY\GALLERY_REPORT.md`,
  *Review fixes*, "Left alone"): the gallery's removal and order failures titled with an action's
  sentence, not «تعذّر تحميل الصور»; `sendMultipart`'s `onProgress` required (production always passes
  it). One commit, first in the history. No other gallery test gap is taken (the owner's rule).
- **D5 — out:** the users page and its actions (USERS), reception links in a user's row (DI-24, step 6),
  any API change, any design-system component.

**If the plan finds more than about 70 files, or a decision the owner must take, propose it in
"Decisions needed" — do not decide it alone.**

## 3. Read first

From `origin/main`: `CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`;
`docs/frontend/architecture.md` (zones, the dependency rule, what a feature exports, server state, forms);
`docs/frontend/design-system/foundation.md` (§5, §9, §10, §12 the inventory); `docs/frontend/localisation.md`;
`docs/features/space-links.md`, `docs/features/users.md`, `docs/features/spaces.md` (the editor's web
decisions); `docs/api/api-contract.md` (*Owners (the admin)*, *Users (the admin)*, the error codes);
ADR 0009; findings 50 and 59; the design — `docs/design/INDEX.md`'s owners, users and verified-editor
sections, `docs/design/prototype/Admin owners.html`, `Admin users.html`, `Admin space edit.html`, and
`D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (A4, A5, A6, AD-021, and every amendment at its
top) with `DECISIONS_SHARED.md`. Round 2's design reports (`DESIGN\ROUND2\REPORT\`) are **not decisions**:
do not build from them. The code to copy as patterns: `features/space-links/` (the admin's spaces list,
its filters and pages), `features/spaces/` (the editor, its dialogs, its refusals), `shared/forms`.

## 4. Findings

New findings this item may record: **82–83** (finding numbers in `docs/architecture/findings/`, **not**
GitHub Issues; worker B holds 77–81).

## 5. Boundaries

`apps/web` and `docs` only. Nothing in `apps/api`, `packages/shared`, the schema or the dependencies. No
new design-system component (if one seems needed, stop and ask).
