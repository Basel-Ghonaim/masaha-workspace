# Post-merge review — PRs #82 and #83 (the spaces API: owners read, managed space API)

**Read-only. No branch, no checkout, no file edit in any repository folder, no install, no npm, no test
run, no server, no database command, no GitHub comment or Issue.** You write exactly one file: your report.

You are an **independent reviewer**. Both PRs are **already merged** into `main` of Basel-Ghonaim/masaha
and neither had a full independent review: #82 had none, #83 only Codex's. Nothing will be rewritten;
your findings are recorded and fixed by the **next branch that touches the same area**. So for each
finding, say where its fix belongs (see "Your output").

Report file: `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW82-83_<YOU>_REPORT.md`
(`<YOU>` = your tool's name in capitals). Write it in parts: first the file with the verdict and the
five most important findings, then append the rest in short steps.

## Where and what
- Run from `C:\Users\basel\masaha-b` and read **only commit objects**: `git fetch origin`; then
  `git diff a82541b1 1efe2b8a` (#82, one commit `8ed0a5fa`), `git diff 1efe2b8a 72ceb047` (#83,
  commits `d5726ddf`, `5e4e610b`), `git show <commit>`, `git show origin/main:<file>` for today's state.
- **Do not run the tests** (CI ran every lane on both heads; the test database belongs to a worker).
  Judge each test by reading it.
- Do not use any project skill. No praise. No tool attribution.

## What the PRs had to be
- #82: plan `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\OWNERSREAD_PLAN.md`, report
  `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\OWNERSREAD_REPORT.md`.
- #83: plan `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\MANAGE_PLAN.md` (its approval note first),
  report `MANAGE_REPORT.md`, earlier reviews `REVIEW_MANAGE_CODEX_REPORT.md` and
  `REVIEW_MANAGE_COPILOT_REPORT.md` (same folder).
- Rules: `CLAUDE.md`, `docs/development/workflow.md` (Definition of Done), `docs/development/testing.md`
  (lanes; rule 7: every authorization property's test proven by a break),
  `docs/architecture/documentation.md` (one home per fact; a decision carries its date and PR; API history).
  Note: the owner allows a small review fix as a new commit on top — do not report `5e4e610b` for that alone.

## Look at these, in this order
1. **Security of `/manage/spaces/:spaceId`:** `requireSpaceAccess` once after `requireAuth`; 404 with no
   active link, for owner/reception/stranger/other owner/admin/deactivated link/deleted space; reception
   refused on every write, decided again under the space's lock; rate and upload limits in the same
   order as `/admin`; nothing admin-only reachable (hide, delete, restore).
2. **What each role receives:** the managed read returns `AdminSpace` with `owners` (`{id, name}`, from
   #82) — to reception too. Any other admin-only field leaking? State it as a fact for the owner's decision.
3. **Transactions (#82):** every read inside `runInTransaction` gets the same `tx` (including
   `users.namesFor` in `space-links/admin-spaces/adminSpaces.service.ts`); no two queries at once on one
   transaction (`Promise.all` in `space.service.ts` `get` and in `facts/groupEdit.ts` against the rule in
   `facts/facts.ts`, finding 11). Failing scenario for each.
4. **The tests, against both plans — the main task.** Make a list of every test each plan names. For each:
   present (file:line) / weaker than planned / missing; and whether its planned break would make it fail
   (yes / no / plausible, with why). Name the stubbed tests that do not run the real request path.
   Name each authorization property with no proving test.
5. **One implementation:** `/manage` routers call the same services as `/admin`; no copied rule; `can()`
   where security.md and ADR 0002 put it.
6. **Documents true to the code** (`api-contract.md`, `backend/security.md`, `backend/conventions.md`
   status header, `features/spaces.md`, `features/space-links.md`, `plans/v1-mvp.md`,
   `project/overview.md`): built claims, one home per fact, facts removed without replacement,
   broken Markdown, decisions and API history lines with `#82` / `#83`.
7. **The reports:** each claim true? Departures from the plan declared and justified?
8. **Then, and only then**, check these points from the analyst's earlier read and confirm or refute
   each with evidence (do not copy them unchecked): (a) `namesFor` without `tx`; (b) `Promise.all` on
   one transaction; (c) removing `tx` from the owner reader left the tests green and no finding was
   recorded; (d) #83's planned tests 3, 8, 9, 11, 12 missing and no deliberate break run; (e)
   `conventions.md` header still lists the refusing middleware as not built; (f) unescaped `|` in the
   `v1-mvp.md` managed row; (g) the 404 rule written in five documents; (h) reception's upload read
   into memory before the refusal; (i) `space-links.md` says the names are read under the share lock.

## Your output
One file:
1. The merge SHAs you reviewed and a one-line verdict.
2. Findings, most severe first, one block each: **ID** (`R82-83-001`…), title, severity
   (**blocker / should-fix / nit**), **verified** or **plausible** (with why), file:line, the failing
   scenario, the fix, and **where the fix belongs**: *a fix item now* (blocker or security) / *the next
   branch touching <files or capability>* / *a finding to record* (with its "resolves when").
3. The tests table from step 4.
4. Step 8's points: confirmed / refuted / partly, one line each with evidence.
5. A short "Checked and fine" list.
6. **Decisions for the owner** (e.g. owners' names to reception), each with options and your recommendation.
Then stop.
