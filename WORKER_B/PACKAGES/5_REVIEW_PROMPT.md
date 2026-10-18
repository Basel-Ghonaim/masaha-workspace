# Review — PR #87, PACKAGES (an independent reviewer)

You are the **independent reviewer** of PR **#87** (`feat/space-packages`, head `9567da9a`) in
Basel-Ghonaim/masaha. It was planned by Claude Code and executed by OpenCode; you are neither executor.
Write your report to `D:\masahaWorkspace\WORKER_B\PACKAGES\6_REVIEW_<YOU>.md` (`<YOU>` = your tool's name
in capitals), in parts: first the verdict and the five most important findings, then the rest.

## Rules
- **Run from `C:\Users\basel\masaha-design-b`, read only commit objects:** `git fetch origin`
  (and `git fetch origin pull/87/head`); base = `5e8c979d`; `git diff 5e8c979d...9567da9a`,
  `git show <commit>`, `git show 9567da9a:<file>`. No edits, checkouts, installs, npm or test runs,
  servers, database commands, no GitHub comments. **Do not run the tests:** CI ran every lane on this head.
  At the end, check the head has not moved (`gh pr view 87 --json headRefOid`).
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario, the
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you
  saw in the code and what you only read in the executor's report** — never present a reported run as
  your own check. No praise. No tool attribution. Do not use any project skill.

## What the PR must be
The plan `D:\masahaWorkspace\WORKER_B\PACKAGES\2_PLAN.md` (the owner's approval at its top: S1 → 409,
S2, S3, the R6 amendment) and the report `D:\masahaWorkspace\WORKER_B\PACKAGES\4_REPORT.md` — judge each
of its seven departures, above all **departure 1's extension to R8** (`null` on `billing`/`audience` →
`invalid_choice`). Scope: `apps/api`, `packages/shared`, `docs`; no schema, migration or dependency.

## Look at these, in this order — think for yourself, beyond the plan
1. **Security:** reception refused on POST and PATCH before the body is read (`requireCan` before
   `validate`); the service's `can()` decided under the space's lock on the links read under it; no route
   outside the `/manage/spaces/:spaceId` boundary; a package of another space unreachable by id (read,
   update) — try to find any path that reads or writes across spaces; nothing public reads `packages`.
2. **The database's answers mapped:** P2002 only on `packages_space_id_name_key` → 409 `not_unique`; P2003
   → `invalid_choice` on `shiftId` — is the comment's claim "the only key a package's write can miss is its
   shift's" really true under the lock? Any other error swallowed or mis-mapped?
3. **Concurrency:** two creates at once (place after the last, the same name); an edit racing a link
   change or a delete of the space.
4. **The shared schemas:** price ≥ 1; the limits' bounds; PATCH partial with `null` clearing only what may
   be cleared; unknown keys; an edit that changes nothing writes nothing.
5. **The tests:** each would fail with its planned break; expectations by hand; whether the 13 breaks
   really cover the properties that matter.
6. **The documents:** `docs/features/packages.md` from the template; the contract's endpoints and the
   whole-list exception; security, conventions, plan, overview, map, `spaces.md`; findings 77–80 honest;
   `#87` on the decision and history lines; one home per fact.
7. The commits: count each subject yourself (≤ 50); each a complete unit.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** (a fix round on this PR / a finding to record / the next item that touches the area); a short
"Checked and fine" list; then stop.
