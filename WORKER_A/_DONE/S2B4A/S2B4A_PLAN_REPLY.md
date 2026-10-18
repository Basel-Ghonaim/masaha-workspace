# S2b-4a — reply to your plan

A strong plan: the profile saved by its changes alone (with the reason a whole resend would fail),
one record-title context both readers share, the sections made for the owner's reuse, and a save that
says the truth when nothing changed. **Approved**, with the answers below. **First, save it** (as
approved here) to `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\S2B4A_PLAN.md` if it is not there yet,
then cut the branch from `origin/main` (check it is still the latest) and build.

## The owner's decisions (§13)

1. **Q1 — option (b):** the verified page's Alert reads «يعدّلها مالكها», without a name; record
   **finding 59**. The owner's name, and «فك ربط {name}», arrive with the owners item (A4's one
   dialog), which needs the owners on a space's read anyway. Nothing in `apps/api` or
   `packages/shared` in this item.
2. **Q2 — design issues 1–5:** approved.
3. **Q3 — stronger decisions 1–9:** approved.
4. **Q4 — the new Arabic lines:** list them in the PR description for the owner's approval.

## Two corrections

- **Two commit subjects are over 50 characters** (counted): `feat(lookups): the amenities checklist
  and an area's name` (57) and `feat(spaces): reach the editor from the list and a creation` (60).
  Shorten them, for example `feat(lookups): amenities checklist and area name` (48) and
  `feat(spaces): open the editor from list and add` (47); count every subject before each commit.
- **Finding 60** (the area field shows no area for a space whose area was hidden since): record it as
  planned; say in the report what the admin sees in a real run.

## Reminders

- **One full test run at a time on this machine:** before `test:component`, check worker B is not
  running a lane in `masaha-b`; if it is, wait.
- Every new test seen failing first; the leave guard's and the record title's tests named by their
  breaks.
- About 65 files: an independent review follows (the owner's reviewer). Don't merge.
- At the report, `git merge-tree --write-tree` against every open PR (worker B's directory item, the
  design fixers'). Stop every background shell you start; `jq` is not installed — use `gh … --jq`.
