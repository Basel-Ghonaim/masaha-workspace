# Post-merge review — PR #84 (the admin's deleted spaces and restore)

**Read-only. No branch, no checkout, no file edit in any repository folder, no install, no npm, no test
run, no server, no database command, no GitHub comment or Issue.** You write exactly one file: your report.

You are an **independent reviewer**. PR #84 is **already merged** into `main` of Basel-Ghonaim/masaha
and had **no review**. Nothing will be rewritten; your findings are recorded and fixed by the **next
branch that touches the same area**. So for each finding, say where its fix belongs (see "Your output").

Report file: `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW84_<YOU>_REPORT.md`
(`<YOU>` = your tool's name in capitals). Write it in parts: first the file with the verdict and the
five most important findings, then append the rest in short steps.

## Where and what
- Run from `C:\Users\basel\masaha-design-b` (worker A builds in `C:\Users\basel\masaha` — never work
  there) and read **only commit objects**: `git fetch origin`; then `git diff 72ceb047 93f152fe`
  (commits `0c062c7f`, `60b2236c`), `git show <commit>`, `git show origin/main:<file>`.
- **Do not run the tests** (CI ran every lane on the head). Judge each test by reading it.
- Do not use any project skill. No praise. No tool attribution.

## What the PR had to be
- Plan `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\ADMINLIST_PLAN.md` (its approval note first);
  reports `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\ADMINLIST_REPORT.md`,
  `ADMINLIST_BROWSER_REPORT.md`, `ADMINLIST_BROWSER_ROUND2_REPORT.md`.
- Rules: `CLAUDE.md`, `docs/development/workflow.md` (Definition of Done), `docs/development/testing.md`,
  `docs/frontend/architecture.md`, `docs/frontend/design-system/foundation.md`,
  `docs/architecture/documentation.md` (one home per fact; a decision carries its date and PR).
- The settled design: `docs/design/INDEX.md` sections for the admin's spaces list, and
  `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` (A3, A7, A8 and amendments).

## Look at these, in this order
1. **The deleted list:** `?status=deleted` read, written and requested as the contract says; rows muted,
   dated on Gaza's calendar, owners named; «استرجاع» the only action; the name not a link; after a
   restore the list fetched again, a toast names the space, focus lands somewhere sensible.
2. **The state as two facts (A3):** the verification badge always, «مخفية» or «محذوفة» beside it; A7's
   chip; A8's «ناقصة» as warning — in `rowView.ts`, `filtersOf.ts` and the components.
3. **The phone's Filters sheet:** what it counts and what «clear» resets
   (`hooks/admin-list/useAdminSpacesFilters.ts`) against what the sheet now holds.
4. **Restore:** no double restore; pending and 429-hold states; errors; hooks before any early return;
   the accessible name holds the visible label.
5. **Frontend rules:** design system only, semantic tokens, no physical direction classes, every string
   from the copy catalogue in both languages.
6. **The tests, against the plan — the main task.** Make a list of every test the plan names. For each:
   present (file:line) / weaker than planned / missing; and whether its planned break would make it fail
   (yes / no / plausible, with why). Name any test that asserts a wrong behaviour.
7. **Findings 44 and 50:** truly resolved in code? Their files, `docs/architecture/findings/README.md`
   and each capability's *Open findings* list agree?
8. **Documents true to the code** (`features/space-links.md`, `features/spaces.md`,
   `project/overview.md`): built claims, one home per fact, labels quoted as the catalogue has them,
   decisions and history lines with `#84`.
9. **The reports:** each claim true? Departures declared and justified? Open questions left unrecorded?
10. **Then, and only then**, check these points from the analyst's earlier read and confirm or refute
    each with evidence (do not copy them unchecked): (a) the Filters sheet still counts and clears the
    stale chip, and a test asserts «2 applied»; (b) `space-links.md` still lists finding 50 as open;
    (c) no `#84` in the new decisions, history or finding resolutions; (d) the plan read the reserved
    finding numbers 69–70 as Issues, so three open questions were not recorded (a deleted row's
    freshness badges; space 41 verified with no owner; `invalid_format` vs the contract's
    `invalid_choice`); (e) finding 50's way out is written only in documents, not on the screen;
    (f) `space-links.md` quotes the chip as «قديمة أو ناقصة» while the catalogue has
    «بيانات قديمة أو ناقصة»; (g) commit `0c062c7f` alone shows deleted rows with the live menu.

## Your output
One file:
1. The merge SHA you reviewed and a one-line verdict.
2. Findings, most severe first, one block each: **ID** (`R84-001`…), title, severity
   (**blocker / should-fix / nit**), **verified** or **plausible** (with why), file:line, the failing
   scenario, the fix, and **where the fix belongs**: *a fix item now* (blocker) / *the next branch
   touching <files or capability>* / *a finding to record* (with its "resolves when").
3. The tests table from step 6.
4. Step 10's points: confirmed / refuted / partly, one line each with evidence.
5. A short "Checked and fine" list.
6. **Decisions for the owner**, each with options and your recommendation.
Then stop.
