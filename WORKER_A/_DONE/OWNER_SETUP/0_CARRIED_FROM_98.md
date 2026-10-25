# Carried from #98 (OWNER_SETUP PR 2, `feat/owner-packages`) into OWNER_SETUP PR 3 (`feat/owner-staff-settings`)

**The owner's review rule (2026-10-20):** a serious or large review fix reopens its PR; small ones are
deferred to the **next PR as a dedicated commit at its start**, named in that PR's description ("Carried
from #98"). #98's review (`6_REVIEW_PR2_CLAUDE_CODE.md`, head `8c429ff4`) found no blocker; the supervisor
confirmed item 1 in the code (`RefusalText` passes no `lines` to `useRefusalView`). These are **PR 3's first
commit(s)**, before the plan's PR 3 commit 1, each code fix with its own red-then-green test and break,
recorded in `4_REPORT_PR3.md`. Read the review for each item's file, line and fix.

Suggested subjects (recount, ≤ 50): `fix(packages): word a row's refusal as the owner's` (items 1, 6–9);
`fix(spaces): let a retired amenity's refusal be undone` (item 2); `fix(spaces): name the prices card one
way` (item 3); the documents folded into the commit they describe.

1. **The row toasts use the generic refusal lines** (review 1): `RefusalText` takes optional `lines`, passed
   to `useRefusalView`; `toastRowFailed` passes `copy.packages.refusals`; a 404 case in test 18 (break: drop
   the lines). PR 3's staff toasts then use the same prop.
2. **The retired-amenity refusal says "untick" what is not drawn** (review 2): on that 422 the section drops
   ids neither offered nor linked from the form's value, and the line says so (the review's wording, both
   catalogues — the Arabic listed for the owner in the PR's description); a test of the save after the 422,
   and its break.
3. **The prices card named two ways** (review 3): one `sectionName(place, group)` for the frame, the toasts
   and the confirm failure; on the owner's place prices gives `publishedTitle`; a test, a break.
4. **A new package stuck on a removed last shift** (review 4): the shift goes back to `''` when `shifts` no
   longer holds it, or the error is drawn in the "none" branch; a test, a break.
5. **`spaces.md`** (review 5): "not built yet" removed; `useSpaceShifts` in the code map.
6. **Review items 6, 7 and 9** as the review says (the held-shift line with an empty shift; a new package's
   404 line; test 18 proving the toast stays).
7. **Review item 8 — fix, not a finding:** an owner-place 404 on a package's route refreshes `['me']`, as
   carried item 8 of #96 did for the editor (one small hook in `packages`; a test, a break).
8. **Review item 10 — record as a finding** (the summary announced on every keystroke), **numbered 102**
   (worker A's next free; 101 is #98's). Any further finding takes 103 and on.

If an item proves larger than this file says, **stop and ask** — never leave one undone silently.
