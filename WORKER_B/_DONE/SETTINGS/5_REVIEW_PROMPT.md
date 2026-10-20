# Review — SETTINGS (an independent reviewer)

You are the **independent reviewer** of worker B's SETTINGS PR (`feat/space-settings`) in
Basel-Ghonaim/masaha: the space's operating settings and capacity for the owner, a migration, DI-41 and the
hand-typed-price rule in the documents. Claude Code executed it in another conversation; you start fresh and
trust nothing you have not seen in the code. Find the PR: `gh pr list --head feat/space-settings --json
number,headRefOid,mergeStateStatus`. Write your report to
`C:\dev\masaha\workspace\WORKER_B\SETTINGS\6_REVIEW_CLAUDE_CODE.md`, in parts: first the verdict and the
five most important findings, then the rest.

## Rules
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/<n>/head`; base = `origin/main`; `git diff origin/main...<head>`,
  `git show <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers,
  database commands, no GitHub comments. Confirm `gh pr checks <n>` is green first; if a lane is red or
  pending, say so and stop. At the end, check the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** No praise, no tool attribution, no project
  skill.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_B\SETTINGS\2_PLAN.md` — the owner's approval note at its top binds
(§13's answers) — and the report `4_REPORT_PR1.md`: judge every departure (among them break B2, rewritten
with the owner's word: a stay limit of 0 tested instead of the bound moved) and every break that did not go
red. Scope: `apps/api`, `packages/shared`, `docs`.

## Look at these, in this order — think like an attacker, then beyond the plan
1. **Authorization on the server:** only an active owner of the space reads or writes the settings and the
   capacity; reception 403 before its body is read; the admin, an owner of another space, a deactivated
   link, a deleted space — 404; `can()` asked again under the space's lock; nothing reachable through
   another route.
2. **Validation:** every bound (the stay limit in whole hours 1–23, the rounding pair sent together, the
   rounding minutes 1–59, capacity 1–1,000 or null, the reminder 1–500 with `{المبلغ}` required and no
   unknown placeholder, bidi controls); a partial `PATCH` that could reach a database `CHECK` as a 500; types
   (`null` for a boolean, strings for numbers).
3. **Writes:** under the lock, only changed fields written and audited (`before`/`after`), a no-change write
   writing and auditing nothing; the capacity's upsert never touching the override's columns; two owners
   writing at once.
4. **The migration:** the column, its default for existing rows, the new-space path, the schema and the
   client agreeing; nothing else changed.
5. **The module boundaries:** the new `occupancy` module and the lock passed into `space-settings` as a
   parameter (P1) — the level rules kept, nothing imported upward.
6. **The documents:** DI-41, the hand-typed-price rule (ADR 0009 revised), "a change applies from then on"
   (Q3, stays already open included), the contract's new routes and codes, `space-settings.md` /
   `occupancy.md`, the build map, finding 94 (or its renumbering) — true to the code, one home per fact;
   `OPEN_DECISIONS.md` point 1 updated by the report (Q4: unpriced, to the owner's queue).
7. **The tests:** each would fail with its planned break; commit subjects counted (≤ 50) and bodies.
8. **Against OWNERS PR 3 (#91) and `main`:** the shared documents' text conflicts and the findings'
   numbers.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** (a fix round on this PR / step 7 / a finding to record); a short "Checked and fine" list; then
stop.
