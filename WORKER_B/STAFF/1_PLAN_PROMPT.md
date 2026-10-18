# STAFF — the owner's reception accounts (step 6), and accounts created by someone else made safe — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, read-only `gh`, and reading files. Where you
are unsure that something works, write it in the plan as **a check the executor makes first, with what to
do if it fails** — never try it yourself. Read only the files the plan needs, each once.

**The task's folder:** `D:\masahaWorkspace\WORKER_B\STAFF\`. This prompt is `1_PLAN_PROMPT.md`; **save the
plan as `2_PLAN.md` here**; reports `4_REPORT_PR<n>.md`. Never write to `C:\Users\basel\.prompt` or
`Downloads\masaha-next` (frozen). If you are Claude Code: use `write-plan` for its discipline.

**Where you read.** `C:\Users\basel\masaha-b` holds worker B's open PR #87 (PACKAGES) branch — read only
commit objects there: `git fetch origin`, then `git show origin/main:<path>`, `git ls-tree`, `git grep`.
Never check anything out. Worker A builds OWNERS in `C:\Users\basel\masaha` — never work there.

## 0. The base and when this runs

Plan from today's `origin/main`, **and read PR #87's diff** (`git fetch origin pull/87/head`): it edits
`app.ts`, the contract, `security.md`, `conventions.md` and the findings index, and **this item runs only
after #87 has merged**. Worker A's OWNERS (web) runs in parallel: its PR 2 adds an owner through the
existing `POST /admin/owners`, so **a change to that endpoint's contract must be additive or said in
"Decisions needed"**. The executor's first step: `git diff --name-status <the plan's base> origin/main`;
a code file the plan names changed in a way the plan does not cover → stop and ask.

## 1. The plan must stand alone

A fresh conversation executes it — Claude Code or OpenCode — and another tool reviews. Every decision with
its one-line reason; the files; each route, schema, service function and type with its interface; each
test with its lane, title and the break that must make it fail (`docs/development/testing.md` §3 —
**every break run and its red output recorded**); **security properties get a deliberate break each**;
the commits, subjects counted (≤ 50); fixes before the push folded (`--fixup` + autosquash,
`GIT_SEQUENCE_EDITOR=:`); every new decision and history line ends with its date and `#PRNUM`; the
procedure with its commands (branch(es) from the latest `origin/main` in `C:\Users\basel\masaha-b`;
`masaha_b_dev` / `masaha_b_test`; `docker start masaha-postgres-1`, never `db:up`, never `npm ci`; one full
test run at a time on this machine; per commit `lint` + `typecheck`; on the head once `test:unit`,
`test:api`, `format:check`, `check:links`, and `npm run build -w @masaha/shared` if the shared package
changes; **if the schema changes**: a migration by `migrate dev --create-only` run **once** — then the
executor checks the folder; on data loss Prisma refuses: use `migrate diff --script` — and both B
databases migrated; a real run on 3321; push; `gh pr create --assignee @me --label feat --label area:api
--label area:docs`; `gh pr checks` and `CLEAN`; the conflict check); a **"Stop and ask"** list; the
executor's stop rule (**a test it cannot run stops the work** — the same wording as
`D:\masahaWorkspace\WORKER_B\PACKAGES\3_EXEC_PROMPT.md` §2); an appendix mapping steps to Claude's skills,
"only a map". Never merge; no tool attribution; stage by path.

## 2. The owner's decisions (2026-10-18) — the security discussion

**Why:** an email typed by someone else can be wrong. Today (a) a mistyped address that has an account
would be **linked** — a stranger at the desk, seeing customers and payments; (b) a mistyped address with no
account gets a new account whose temporary password is handed over in person — but **a password reset
works while that temporary password is pending** (`security.md` › reset success "settles a pending
temporary one"), so whoever owns the mistyped mailbox can take the account over; (c) **a pending temporary
password never expires**. (b) and (c) hold **today for the owners the admin creates** — the most powerful
accounts. All are fixed here.

**Part A — accounts created by someone else (the admin's owners and the owner's staff), platform-wide:**
- **A1 — no reset by email while a temporary password is pending.** A reset request for such an account
  sends nothing and answers exactly as for any address (no disclosure); once the person has signed in and
  changed it, the reset works again. *Recovery meanwhile:* a new temporary password from whoever created
  it (A4, and the admin's existing issue).
- **A2 — at the first sign-in, the person confirms or corrects their email,** with the forced password
  change (they hold the temporary password handed over in person — the proof). A corrected email must be
  free (else `EMAIL_TAKEN`, as registration). Audited. Design the API so the web's change-password page can
  add it later (worker A); say which endpoint and body.
- **A3 — a temporary password expires 7 days after it is issued** (the owner may change the number at the
  plan's approval): sign-in with an expired one is refused with a code that says so, and a new one must be
  issued. Decide whether that needs a column (`temporaryPasswordExpiresAt` or the issue time) — if so, a
  migration; state it.
- **A4 — the handover question** («واتساب · شفهيًا · أخرى») is asked wherever a temporary password is
  shown, the owner's staff included: a managed handover route beside the admin's, on the same `users`
  service.
- **Not here (web, worker A's OWNERS PR 2):** the admin's upgrade of an existing account shows whose
  account it is before confirming — already given to worker A.

**Part B — staff (step 6), on `space-links`:**
- **B1 — the owner creates new accounts only:** name and email → a new account, a reception link, the
  temporary password once. **An email that already has an account is refused** (`EMAIL_HAS_ACCOUNT`, the
  existing code) — **no existing account is ever linked by an owner.** This **amends ADR 0009 rule 4** (its
  second bullet) and the design's OW-019 ("both outcomes"): write the ADR's *Revised* line in this item.
  A person working at two spaces is out of v1 — record a finding (a later in-person code).
- **B2 — the list** `GET /manage/spaces/:spaceId/staff` (owner only — `staff.manage`): each reception
  link, active or not, with whether its temporary password is still pending (OW-018's badge «لم يغيّر
  كلمة المرور المؤقتة بعد»), no last sign-in. Whole, not paged (a space has few staff) — or paged if the
  conventions say so; decide.
- **B3 — deactivate and re-activate through the same `PATCH …/staff/:userId`** (OW-017). Deactivating
  **ends every session of the person** — kept, because a deactivated receptionist must not stay signed in
  on the shared desk device (the per-request link check alone would already refuse the space). Audited.
- **B4 — the owner may issue a new temporary password for a staff account only while it is still pending**
  (never signed in); after the first sign-in the account is the person's, and recovery is theirs (email, or
  the admin).
- **B5 — a rate limit on staff creation:** 10 per hour per owner, counted before the body is read; the
  routes behind `requireSpaceAccess` and `requireCan('staff.manage')` before `validate` (the photos'
  pattern).
- **B6 — DI-24's API half:** `AdminUserRow` gains the person's active reception links (additive), so the
  admin's users page can show them later (worker A's USERS item).
- **B7 — reception keeps reading the owners' names** on the managed space read (#86's D5): unchanged; the
  staff list is the owner's alone.
- **Out:** every web screen; reception's permissions at the desk (recorded for steps 7–9 in
  `D:\masahaWorkspace\_SHARED\OPEN_DECISIONS.md` — do not build them); packages; capacity.

**Size:** if the item is above about 60 files, **propose two PRs in "Decisions needed"** — the natural cut
is **PR 1 = Part A** (it protects the admin's owners at once, and PR 2 builds on it) and **PR 2 = Part B**.

## 3. Read first (from `origin/main`, and #87's diff)

`CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`; `docs/backend/security.md`
(passwords, the temporary password, reset, revocation, rate limits); `docs/backend/conventions.md`;
`docs/api/api-contract.md` (auth, `/me/password`, *Owners (the admin)*, *Users (the admin)*, the managed
routes); `docs/architecture/data-model.md` (users, `SpaceManager`); ADR 0009, 0013, 0017; `docs/features/auth.md`,
`users.md`, `space-links.md`; findings 17, 21, 23, 49; `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md`
(O4, OW-017, OW-018, OW-019); the code of `auth` (reset), `users` (temporary password, forced change,
handover), `space-links` (`admin-owners`, links), `sessions` (revoke all), `shared/auth` (`can.ts`,
`requireCan`, `spaceAccess`), `shared/rate-limit`.

## 4. Findings

New finding numbers for this item: **84–86** (in `docs/architecture/findings/`, not GitHub Issues). Record
the reset-while-pending hole and the never-expiring temporary password **as findings resolved in this
item** only if the documents' rules ask a resolved problem to be recorded; otherwise the decisions and
`security.md` carry them. Record the two-space staff case (B1).

## 5. Boundaries

`apps/api`, `packages/shared`, `docs`. Nothing in `apps/web`. A schema change only if A3 needs it (say so).
No dependency. No new error code unless A3's expired password needs one — then follow `add-error-code`'s
rules and say so in "Decisions needed".
