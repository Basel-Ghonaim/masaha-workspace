# FIX ADMIN REST — review fixes for PR #66

From the analyst's conformance review of head `15039cb` (a read-only reviewer against the prompt,
the plan, the reply, the decisions, the API's contract and your report). No design or API-truth
defect blocks it. **Method:** fold each into the commit of its decision (fixup + autosquash),
`git push --force-with-lease`, ONE "Review fixes" comment, a "Review fixes" section in
`REPORT\FIX_ADMIN_REST_REPORT.md`. Your two scripts at every commit, `format:check`, `check:links`,
your eyes on each fixed part at 390 and 1440. Stop every background shell you start; `jq` is not
installed — use `gh … --jq`.

## Must fix

- **R1 — `CHANGES.md` claims what is not built** (G2's row, line 119): it says hiding is explained "in
  the line above it, the sheet's helper and the switch's toast", but commit 8 removed the sheet's
  helper and the switch's toast (AD-025, P8's exception). Say only what is true: "in the line above
  each panel".

## Should fix

- **R2 — `Admin owners.html?link=o4` opens the link dialog for a suspended owner** (Rima); the API
  refuses it with `ACCOUNT_SUSPENDED`. At `:35`, also require `u.status === 'active'`.
- **R3 — the lookups' «الترتيب» field shows on any list over ten rows, but only the areas apply it**
  (`:57` vs `:115–121`): add three amenities and the field is accepted then ignored. Apply the
  position in the amenities' and the governorates' saves too (preferred: one rule for every list), or
  show the field for the areas only.

## Small

- **English shows Arabic punctuation:** the editor's report alert (`«…» — …، …`, `Admin space
  edit.html:84`) and the new unlink titles ending «؟» in English: put the punctuation through `tr()`.
- **`Admin reports.html?space=olive`** filters while the trigger reads «كل المساحات»: read `?space=`
  only from the spaces the field offers.
- **«مالك مسبقًا — اربطه بالمساحة»** drops the chosen space (`Admin owners.html:92`): carry it
  (`&space=<id>`) and preselect it.
- **The overview's queue counts a missing photo, «عرض الكل» does not** (`Admin overview.html:39`):
  count the same groups in both (photos are no fact group: leave them out of the queue's count).
- **The report:** DI-27 names `map.jsx` as colliding (it has no rest destructuring; only profile-a's
  `ClockInput` does, plus two inline scripts on pages without `ActionButton`); add to the departures:
  «تعديل الحقل» lands on `#report`, not `#<section>`; the role dialog's action is `destructive` for
  «جعله أدمن» too (the plan marked only the demote — say why, or make the promote `primary`); the
  settings line says three cards shared one error object, but two had errors.

## The owner's decisions on your new design issues

Decided by the owner:
- **DI-26 — build it:** the chip reads **«قديمة أو ناقصة»** (A7's wording amended: it keeps the
  missing groups too, so its words say so); the same words wherever that filter is named (the
  overview's link, `INDEX.md`).
- **DI-28** (a disabled item's reason drawn faint): recorded for worker A's design-system item — not
  built here.
- **DI-29 — build it:** the audit sample's lines agree with ZM Hub's state.
- **DI-27:** the root fix goes to the public design fixer's PR #65 (it owns `shared.jsx`); keep your
  workaround as it is.

**Merge order:** whichever of #65 and #66 finishes its fixes first merges first; the second rebases,
keeping both `CHANGES.md` sections (the fast path).

## Recorded, not for this PR

- An inactive amenity's badge reads «مخفية» (feminine, and "hidden" where the panel says «نشط / غير
  نشط»): the lookups' wording, a later polish.
