# Review — PR #88, OWNERS PR 1 (an independent reviewer)

You are the **independent reviewer** of PR **#88** (`feat/admin-owners`, head `e4e13e9e`) in
Basel-Ghonaim/masaha — the first of three PRs of the OWNERS item. It was executed by Claude Code; you are
another tool. Write your report to `D:\masahaWorkspace\WORKER_A\OWNERS\6_REVIEW_PR1_<YOU>.md`
(`<YOU>` = your tool's name in capitals), in parts: first the verdict and the five most important findings.

## Rules
- **Run from `C:\Users\basel\masaha-design-b`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/88/head`; base = `5e8c979d`; `git diff 5e8c979d...e4e13e9e`, `git show <commit>`,
  `git show e4e13e9e:<file>`. No edits, checkouts, installs, npm or test runs, servers, database commands,
  no GitHub comments. CI ran every lane on this head. At the end, check the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** No praise, no tool attribution, no project
  skill.

## What the PR must be
The plan `D:\masahaWorkspace\WORKER_A\OWNERS\2_PLAN.md` — the owner's approval at its top, and **PR 1 only**
(§7 *PR 1*, §9 *PR 1 · commits 1–3*, §10 *PR 1*) — and the report
`D:\masahaWorkspace\WORKER_A\OWNERS\4_REPORT_PR1.md`: judge its five departures. Scope: `apps/web`, `docs`.

## Look at these, in this order — think beyond the plan
1. **Commit 2, the refactor:** truly no behaviour change in the admin's spaces list (pagination, states,
   paused search, page-in-range, focus) — compare old and new line by line; anything lost.
2. **The owners page:** `GET /admin/users?role=owner` with search and the state chips; addresses kept in the
   URL; pages; the empty and no-match states; finding 50's line («كل مساحاته محذوفة…») shown exactly when it
   should be and linking to `?status=deleted`; the words («مالك» in actions, «صاحب المساحة» the role, the
   glossary line).
3. **The capability boundary:** the users list in `features/space-links` (O2) built so a later USERS item
   reuses it; nothing imports across features; dashboard-only (no admin code in the site's first download).
4. **Commit 1 (#85's leftovers):** the gallery's failed writes titled by their action; `onProgress` required
   and every caller passing it.
5. **The slower route test:** the report says `routes.component.test.tsx` › *lists the owner's eleven pages*
   now takes ~2.4–2.5 s alone against a 3 s limit, because the shell also loads the owners list, and failed
   twice locally under load. Is the owners list (or anything new) loaded where it should not be — e.g. for
   an owner's shell, not only the admin's? A real defect, or a test budget to record as a finding?
6. **The tests:** each would fail with its planned break; the axe substitute (departure 2) acceptable?
7. Frontend rules (design system only, semantic tokens, no physical direction, every string in both
   catalogues); the documents true to the code, one home per fact; commit subjects counted (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** (a fix round on this PR / PR 2 or PR 3 / a finding to record); a short "Checked and fine" list;
then stop.
