# FIX ADMIN REST — reply to your plan

A strong plan, and truthful to what the API builds (the refusals after the submit, the sample data
corrected where it promised the impossible). **Approved**, with the answers below. **First, save it**
(as approved here) to `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_ADMIN_REST_PLAN.md` if it is not
there yet, then cut `design/admin-rest` from `origin/main` (check it is still the latest) and build.

## The owner's decisions (§13)

1. **S1–S15:** approved as recommended (S5, S6 and S10 included; S10's icons are the prototype's
   own, noted as lucide's, ISC).
2. **DI-21 and DI-25:** fold.
3. **DI-22:** fold — **«ناقصة» is `warning` everywhere** for the admin (A8). The built web's list
   (#50, `neutral`) follows when worker A builds this list's screen; say so in `CHANGES.md`.
4. **DI-23 and DI-24:** record only, in the report. The analyst routes DI-23 to worker A's
   design-system item and DI-24 to step 6 (reception links), where the users row gains them.

## One change to a settled decision (AD-028, with your DI-25)

AD-028 kept `destructive` for `user_suspended` and `space_hidden`, before the log knew deletion and
unlinking. **The owner's decision: the log's red follows P9** — `destructive` for the actions whose
confirmation is destructive: **`space_deleted`, `user_suspended` and the owner's unlink**; hiding
becomes `neutral` (it is undone at once and touches no one else); every other action `neutral`. Note
it in `CHANGES.md` as AD-028 amended by the owner.

## Reminders

- **The shared editor (G1):** after each change, open both editors; #61's fixes must hold (F1's gap,
  R2's shift ids, R3's day errors, the gallery's counting).
- **Your eyes on every changed page** at 390, **768** and 1440: the assertions do not see layout.
- Ten commits, one per decision, as you planned: fine; count each subject.
- At the report, `git merge-tree --write-tree` against every open PR (the amenities worker's, worker
  A's, worker B's): yours touches only `docs/design/`.
- The analyst reviews it. Don't merge. Stop every background shell you start; `jq` is not installed —
  use `gh … --jq`.
