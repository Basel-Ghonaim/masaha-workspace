# PACKAGES — the owner's packages API (step 5b) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, read-only `gh`, and reading files. Where you
are unsure that something works, write it in the plan as **a check the executor makes first, with what to
do if it fails** — never try it yourself. Read only the files the plan needs, each once.

**The task's folder (the new workspace):** `D:\masahaWorkspace\WORKER_B\PACKAGES\`. Its files follow the
cycle: this prompt is `1_PLAN_PROMPT.md`; **save the plan as `2_PLAN.md` here**; the executor's report
will be `4_REPORT.md`, screenshots (if any) in `shots\`. Nothing of this task goes to `C:\Users\basel\.prompt` (frozen since 2026-10-17).
If you are Claude Code: use `write-plan` for its discipline (the file it saves to is `2_PLAN.md` above).

**Where you read.** Worker A's PR #85 (GALLERY) is open in `C:\Users\basel\masaha` — never work there.
Work in `C:\Users\basel\masaha-b` (detached at `origin/main`, clean; never check anything out):
`git fetch origin`, then read only `origin/main`'s commit objects (`git show origin/main:<path>`, …).

## 0. The base, and when this runs

You plan from today's `origin/main` (`44b8ac7b` or later: HARDEN, #86, is merged). **The executor starts
only after PR #85 has merged**, from the latest `origin/main`. #85 is web and documents only; the
documents it edits that this item may also edit are `docs/features/spaces.md`, `docs/project/overview.md`
and `docs/architecture/findings/README.md` (read `gh pr view 85 --json files`). So the plan:
- names every file it edits, and marks those #85 also edits as **shared — re-read on the merged tree
  before editing; a conflict there is documents-only**;
- gives the executor a first step: `git diff --name-status <the plan's base sha> origin/main`; any change
  to a code file the plan names that the plan does not cover → stop and ask.

## 1. The plan must stand alone

A fresh conversation executes it — Claude Code or another agent — and another tool reviews. So: every
decision with its one-line reason; the files; each new module, route, schema and function with its
interface; each test with its lane, title and the break that must make it fail (`docs/development/testing.md`
§3 rule 7 — **every break run and its red output recorded in the report**); the commits, subjects counted
(≤ 50); a fix before the push folds into its commit (`git commit --fixup` + `git rebase -i --autosquash`
with `GIT_SEQUENCE_EDITOR=:`); every new decision and history line ends with its date and **`#PRNUM`**,
replaced just before the push by the real number (issues and PRs share one sequence; the highest is
#86 today, so expect #87 — the executor checks); the procedure with its commands (branch
`feat/space-packages` from the latest `origin/main` in `C:\Users\basel\masaha-b`; ports 3321/5321;
`masaha_b_dev` / `masaha_b_test`; Docker by `docker start masaha-postgres-1`, never `db:up`; **one full
test run at a time on this machine** — check worker A's folder runs none; `lint`, `typecheck`,
`test:unit`, `test:api`, `format:check`, `check:links`, and `npm run build -w @masaha/shared` if the
shared package changes, so `dist` is current; push; `gh pr create --assignee @me --label feat
--label area:api --label area:docs` with the description written out; `gh pr checks` and `CLEAN`; the
conflict check with `git merge-tree --write-tree` against any open PR; the report to
`D:\masahaWorkspace\WORKER_B\PACKAGES\4_REPORT.md`, UTF-8, written in parts); a **"Stop and ask"** list;
an appendix mapping steps to Claude's skills, "only a map". No step may depend on a Claude skill. Never
merge; no tool attribution; stage by path.

## 2. The task — the owner's decisions (2026-10-17)

The `packages` module (conventions §7: L2, table `packages`, surface *manage*): an owner's subscription
templates for the space, private to its staff. **The table, its model and its CHECK constraints already
exist** (migration `20260929120200_front_desk`, `model Package`). **No schema change, no migration.**

- **D1 — scope: the API only.** `GET /manage/spaces/:spaceId/packages` (🧾 the space's staff),
  `POST …/packages` and `PATCH …/packages/:id` (🏢 the owner) — `docs/plans/v1-mvp.md`'s managed row.
  No DELETE: a package is retired by `isActive: false` (the model's own comment). Mounted under the
  existing `/manage/spaces/:spaceId` boundary (`requireSpaceAccess`); writes decided by `can()` with the
  existing action `'packages.manage': 'owner'` (`can.ts`), the reads by `'space.read'`. Capacity and the
  stay limit (O2), staff (step 6) and every web screen are **out**.
- **D2 — a package's price is above zero** (the owner's DI-10): validation in the shared schema now
  (whole agorot, ≥ 1, the same upper bound as a space's prices). The database's CHECK stays `>= 0` and
  follows with the desk's steps — **no migration here**.
- **D3 — a repeated name** (`@@unique([spaceId, name])`, the owner's O8: "a repeated name on its field"):
  a `validation` (422) refusal on `name` with an **existing** field code — no new error code. Find the
  code the contract already uses for "taken" on a field; if none fits, stop and ask (no `add-error-code`).
  Decided under the same transaction as the write, so two saves of one name cannot both pass.
- **D4 — order:** no reorder route. The list is ordered by `sortOrder`, then `name`; a new package takes
  `sortOrder` after the last (state the rule).
- **D5 — the read answers every package, active and inactive,** each with `isActive`, **whole** (no
  `page`, no `meta`): the desk's picker needs them all (the owner's batch 5, *Rules changed*). Add it to
  `api-contract.md`'s list of lists answered whole.
- **D6 — the package's body,** as the model and the owner's O8 hold it: `name`; `validityDays` (required,
  ≥ 1); optional limits `totalDays` (≥ 1), `daysPerWeek` (1–7), `hoursPerDay` (1–24), `totalHours` (≥ 1);
  `billing` (`SubscriptionBilling`) with `priceAgorot` (the whole price when fixed, else the rate per
  hour or day); `audience` (`PriceAudience`); an optional `shiftId` of **the space's own shifts**
  (`invalid_choice`, as prices do); `isActive`. PATCH is partial. Name every field's rule from the model
  and the contract's existing conventions (lengths, trimming, bilingual or not — the model has one
  `name`; follow it).
- **D7 — a package is never public:** no public read touches the table; the directory's packages are the
  published `SpacePrice` rows (glossary, foundation §13 #21). Say how a test proves nothing public reads it
  if a test can; otherwise state it as a rule.
- **D8 — audit:** each create and update writes an audit entry in the existing `<module>.<verb>` naming.
- **D9 — the subscriptions made from a package keep their snapshot** (ADR 0010): editing a package changes
  no subscription. State it; no code needed.
- **D10 — the documents:** `api-contract.md` (the three endpoints, their bodies, statuses, errors and the
  whole-list exception), `security.md` and `conventions.md` (the module built; their status headers),
  `plans/v1-mvp.md` (the row built), **a new capability document `docs/features/packages.md`** from the
  template (`docs/architecture/documentation.md` §5) — check `docs/README.md`'s *Deferred documents* for
  what else a first capability document owes — and `docs/project/overview.md`'s *Built* line.

**If the plan finds more than about 40 files, or a decision the owner must take, propose it in
"Decisions needed" — do not decide it alone.**

## 3. Read first (from `origin/main`)

`CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`; `docs/backend/conventions.md`
(§2 the route chain, §7 the modules, §8 module rules and transactions); `docs/backend/security.md`;
`docs/api/api-contract.md` (§2–§4 conventions, the managed spaces, prices and shifts); `docs/architecture/data-model.md`
(Package, Subscription, the same-space rule); `docs/architecture/documentation.md`; `docs/README.md`;
ADR 0009, 0010; `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (DI-10, O6, O8, *Rules changed*)
— the design decisions live there; the code of a sibling L2 module and of the prices group as the
pattern to copy (`git ls-tree`); `apps/api/src/shared/auth/can.ts`; `packages/shared/src/spaces/` (the
prices' schemas).

## 4. Findings

Finding numbers (in `docs/architecture/findings/`, **not** GitHub Issues):
- **77–79 — record these three, in this item** (the owner's decision; a record needs no code): the first
  three findings of #86's review, `D:\masahaWorkspace\WORKER_B\_DONE\HARDEN\REVIEW86_OPENCODE_REPORT.md`
  — 77 `waitingOnLock` counts any waiting backend and its 4 s reach sits under Vitest's 5 s; 78 A1 rests on
  nothing between the space lock and `namesFor` reading `users`; 79 `users.namesFor` keeps an optional
  `tx`. Each with its evidence (file:line on `origin/main`) and *Resolves when*, in finding 63's format.
- **80–81** — new findings this item may need.

## 5. Boundaries

`apps/api`, `packages/shared` and `docs` only. Nothing in `apps/web`. No schema change, no migration, no
dependency. If any is needed, stop and say so.
