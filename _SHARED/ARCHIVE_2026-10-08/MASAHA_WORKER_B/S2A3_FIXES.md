# PR #49 — review fixes (one list)

An independent review ran on `eaf8f4d` (one should-fix, three nits); the analyst verified item 1 and
the commit subject in the code. Fold each fix into the commit it corrects (fixup + autosquash,
`--force-with-lease`); no "fix" commits. Then post ONE "Review fixes" comment and update the PR
description. No subagents. Follow workflow §10: `receiving-code-review` first (push back with reasons
where an item is wrong); **make the break** for each new or strengthened test, and list the breaks.

The report is `C:\Users\basel\.prompt\MASAHA_WORKER_B\REVIEW49_REPORT.md`.

## 0. Rebase, only if needed
PR #48 (the spaces' facts API) may merge before you start; it edits `docs/project/overview.md`'s spaces
line, next to your lookups line, and changes the Prisma schema. If GitHub then shows #49 `DIRTY`,
rebase on `origin/main` keeping both lines, and run `npx prisma generate` in `apps/api` before lint and
typecheck. If it is still `CLEAN`, don't rebase.

## Must fix
1. **One amenity's failure is hidden by a failed action on another row, and the alert never names its
   amenity** (`useAmenityFailure.ts:39–44`: the latest failure per target, then `.at(-1)` across all
   targets, rendered once for the whole list). Retire A → refused; toggle B → refused: A's failure
   disappears though nothing was done on A again — against the rule this hook's own comment states
   ("an action elsewhere leaves it standing"). And `blocked` comes from that same last failure, so a
   429's hold is released when another row fails for another reason.
   - **Fix:** a row action's failure belongs to **its row** (scoped in `useAmenityRow`, shown with that
     row, so it names its amenity by where it is), as the governorates scope theirs to their card; only
     an **order's** failure stays at the list level. **`blocked`** holds every control while **any**
     standing failure is a 429 still counting down, whatever failed after it.
   - **Tests:** the case the suite misses — A fails, then B **fails** → both failures shown, each with
     its row; a 429 on A, then another refusal on B → every control still waits until A's count ends.
     Make each break once.
   - **Document:** `lookups.md` says where an amenity's failure shows (its row) and an order's (the
     list); fix the line that now says "in its card" for amenities.

## Known item (the owner's decision)
2. **`docs/frontend/architecture.md` §2** still says the dashboard's admin screens are not built,
   though the lookups page has been built since #43: correct that sentence (the code governs), in the
   commit that adds the tab.

## Nits — fix
3. **Commit subject over 50 characters:** `fix(design-system): dim controls while aria-disabled` (52) →
   for example `fix(design-system): dim aria-disabled controls` (45).
4. **`SwitchControl.disabled` is written and never read** (`types/RowControlsView.ts`; set in
   `useRowViews.ts` and `useAmenityRow.ts`; `RowSwitch` doesn't read it): drop it from the switch's
   type (the project bans options nothing uses), or read it in `RowSwitch` if a switch can truly be
   disabled — your plan's choice, said in the comment.
5. **Every edit fixture's icon is `wifi`, the first key**, so "editing starts from the amenity's own
   icon" has no test that would fail: give the edit fixtures a non-first icon (`sun` or
   `presentation`). Break: let the form fall back to the first option; see it fail.

## Checks — don't re-run what already passed
- Lint and typecheck on each rewritten commit.
- On the head, once each: `test:component`, `test:unit`, `check:classes`. Skip `test:api` and the
  build locally unless the rebase brought new code under yours (then run `build` + `check:build` once);
  CI runs every lane.
- Report once CI is green and GitHub shows `CLEAN`: the head, what changed per item, the breaks, the
  counts. Don't merge.
