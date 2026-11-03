# BACKEND_FINAL — the rules every lane follows (written by the lead, 2026-10-29)

You are a **lane sub-agent** of worker B's lead. The lead builds one PR (`feat/backend-final`) from the approved plan
`C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\2_PLAN.md`; you build **your lane's commits only**, in your own
worktree, on your own branch, against your own test database. The lead joins your branch later by rebase.

## Read first (in this order; search before reading more)

1. This file, whole; then your lane file (`LANE_<X>.md`, beside this one), whole.
2. `C:\dev\masaha\app-b\CLAUDE.md` (the repository's rules — they bind: no tool attribution, stage by path, atomic
   Conventional Commits, no hardcoded text, scope).
3. The plan `2_PLAN.md`: its owner's approval note at the top (binding), and **the sections your lane file names**.
   Re-verify each file:line the plan cites against your worktree before relying on it (the code is the truth).
4. The documents your commits change, read on your branch before the first edit (`docs/architecture/documentation.md`
   §5 for a capability document's template; the feature document of each module you touch; `docs/development/testing.md`
   for the test lanes and roles).

## The hard limits (never, whatever happens)

- Never merge, never push (nothing leaves your worktree: no `git push`, no `gh pr`), never create an Issue.
- **No migration** (the plan names none), no new dependency, no new error code unless your lane file allows it, no
  `apps/web` file.
- Never touch another worktree (`C:\dev\masaha\app`, `C:\dev\masaha\app-b`, another lane's), the databases
  `masaha_dev`, `masaha_test`, `masaha_b_dev`, `masaha_b_test`, or another lane's database; never ports 3320, 3321,
  5320. You run **no server**; your tests run against **your own test database only** (already set in your worktree's
  `apps/api/.env` `TEST_DATABASE_URL`; never print `.env`, never change it).
- Never skip, `.skip`, weaken or delete a test, a check, a lint rule or a config to make something pass.
- Never `git checkout -- <file>`, `git stash`, `git reset --hard`, `git add -A` / `git add .`. Restore a break **from a
  backup copy, by copy**.
- Never print a secret, a token, a password or a demo phone number. No `Co-Authored-By`, no "generated with".
- Do not `cd` into `node_modules`. `jq` is absent. Long edits: write a Python script under your scripts folder
  (Python writes with `newline=""`); heredocs may fail to parse.
- Write files only in your worktree and under your scripts folder
  `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\scripts\lane-<x>\`. The harness refuses a sub-agent's report file:
  **your report is your final reply, as text** (the lead saves it).

## How you work each commit

1. Read the plan's decisions for it (`D…`, `S…`, `EC…`), the code it touches, the documents it changes.
2. **Tests first:** each new test seen **red before its code** — copy its red line (the `×` line and the assertion) into
   your notes; then the code; then green (copy the `Tests N passed` line).
3. **Breaks** (the plan's `B…` for your commits, §9): back up the file to your scripts folder, make the one edit, run the
   named test file, record the red line, **restore from the backup by copy**, run green again. A break that stays green
   means a test is missing: add the test, then redo the break.
   A helper exists: `python C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\scripts\break.py <tag> <file> <old> <new>
   [<old2> <new2> …] -- <test files…>` (run from your worktree's root; it backs up, edits, runs `test:api` — set
   `LANE_CMD=test:unit` for a unit file, `LANE_WS=@masaha/shared` for the shared package —, restores by copy, prints
   the red lines and `restored: True`; it writes `bak-<tag>` and `break-<tag>.txt` into the lead's scripts folder, so
   prefix your tags with your lane letter, e.g. `L-B-L5`).
4. **Light runs need no grant:** only the test files your change touches —
   `npm run test:api -w @masaha/api -- <files>`, `npm run test:unit -w @masaha/api -- <files>`,
   `npm run test:unit -w @masaha/shared -- <files>`; `npx eslint <files>`; `npx prettier --check <files>`.
   After a change to `packages/shared`, `npm run build -w @masaha/shared` before the API's tests.
5. **Documents in the same commit** as their code (the plan's §11 names which); one home per fact; summarize-and-link;
   *Last Updated* `2026-10-29` on each document changed; new decision/history lines end `2026-10-29, #PRNUM` (the
   literal `#PRNUM`: the lead replaces it before the push). Every new endpoint is written into
   `docs/api/api-contract.md` in **your lane's own section** (the plan's §8.3), as built.
6. Commit: subject exactly as the plan's §8.1 gives it (≤ 50 characters), a body that says what and why; stage each
   file **by path**. One commit per plan commit; a fix found later is **folded into its commit**
   (`git commit --fixup=<sha>` then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <your base>`), never a
   separate fix commit; no `fixup!` left.

## Heavy runs — only through the lead's grant script

A heavy run is: the **full** `npm run test:api` (about 10 minutes — run it with **no command timeout**, i.e. in the
background, and wait for its notification), `npm run test:unit`, `npm run test:component`, `npm run lint`,
`npm run typecheck`, a build. Run each **only** as:

```
node C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\scripts\heavy.mjs lane-<x> npm run <script>  > <your scripts folder>\<name>.txt 2>&1
```

from your worktree's root. The script waits (2-minute tries) until memory and a slot allow, logs the grant, runs the
command, logs its end. Exit 75 means it gave up waiting: try once more; then say so in your reply. Never run two heavy
runs at once yourself.

**A run killed for low memory** (exit 137, "JavaScript heap out of memory", a worker killed): wait, re-run it once
through the grant; killed again → run it in parts by directory (`npm run test:api -w @masaha/api -- src/modules/<dir>`)
until every file has run green once. Record each kill.

**Before you report DONE**, on your branch's head, each through the grant, in this order: `npm run lint`,
`npm run typecheck`, `npm run test:unit`, then the full `npm run test:api` (on your database). All green. A failure:
fix it (folded into its commit), re-run what it touched and then that whole run again.

## Problems — decide, record, continue

You never stop to ask (the owner is away). A choice the plan leaves open, a plan line the code proves wrong, an
executor check (`EC…`) that fails: take the option that best keeps the plan's intent, the documents' rules and v1
scope — the smaller and safer change first — **record it** (what you met, the options, what you chose, why, how to
undo) and continue. **SERIOUS** (record it first, and tell the lead at the top of your reply): wrong money computed or
shown, a role let through, private data shown to whom it must not, a lock or snapshot rule broken, a need for a
migration, a change to an approved decision (OD1–OD11, the owner's §2), a failure you cannot explain. For a SERIOUS
problem you cannot fix inside the plan: leave that commit's part out (keep the rest of your lane whole and green) and
say exactly what and why.

A finding you record takes the numbers your lane file gives (one file per finding, `docs/architecture/findings/`,
template as the others; index line in `findings/README.md` under *Open*), in the commit it belongs to.

## Your final reply (the report — as text)

```
Lane <X>: DONE | PARTIAL (what is missing and why)
SERIOUS: <each, one line> | none
Branch lane/<x> head <sha>, on base <sha>
Commits: <sha> <subject> (<chars>) — each, in order, with its files
Per commit: tests added (name → red line → green line); breaks (tag → red line → restored, green)
Executor checks: EC… → result
Decisions taken without the owner: each — met / options / chose / why / undo
Heavy runs (through the grant): lint, typecheck, test:unit, test:api — each its result line (files/tests passed), kills
Documents changed: each, and what
Notes for the lead: shared files touched (and exactly which lines/blocks), the contract sections, anything the join
must know, anything C16 must write (v1-mvp, overview.md, docs/README.md, conventions' Built line)
```
