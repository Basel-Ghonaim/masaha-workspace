# DELETED — reply to your plan

A very good plan: the rule written once with every other place linking it, the status table read
backwards in one place, and the web kept exactly as it is. **Approved**, with the answers below and
one change (decision 5). **First, save it** (as approved here) to
`C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\DELETED_PLAN.md` if it is not there yet, then cut the
branch from `origin/main` (check it is still the latest) and build.

## The owner's decisions (§13)

1. **The row's shape:** facts apart — approved (A3: a state is two facts, and the restore screen must
   say what comes back).
2. **`pages/dashboard/routes.component.test.tsx`:** option (a), granted — **the three fixture lines
   only**, in *the admin's spaces page*, as an explicit exception to the new rule's condition (3); say
   so in the PR description. Worker A and the amenities worker edit other parts of that file; whichever
   PR merges second resolves it keeping both sides, with lint and typecheck.
3. **`SPACE_STATES` → `SPACE_STATUSES`:** approved.
4. **A deleted row names its owners:** approved, with the narrowing recorded as you wrote it.
5. **`deletedAt: string | null`, not `isDeleted`** — the owner's choice against your recommendation:
   the screen needs the date now. The design fixer's approved 2b plan shows a deleted row as
   «محذوفة في …», muted with «استرجاع». So the row carries `deletedAt` (the ISO date, `null` for a live
   space) beside `isVerified` and `isHidden`; no `isDeleted`. Update §1, §4, §9 (the mapper's test
   asserts the date) and the contract's row accordingly.
6. **The D1 wording:** approved as written, the *Files* bullet folded into condition (3) and the
   databases widened to every folder that runs the API.

## Reminders

- **The new rule in practice:** you touch no file of the amenities worker or of worker A beyond the
  three granted fixture lines, and no schema. Anything else from their lists: stop and say so.
- Every new test seen failing first; the fixtures follow the shape.
- At the report, `git merge-tree --write-tree` against every open PR (the amenities worker's,
  worker A's, the design fixer's `design/admin-rest`).
- The analyst reviews it. Don't merge. Stop every background shell you start; `jq` is not installed —
  use `gh … --jq`.
