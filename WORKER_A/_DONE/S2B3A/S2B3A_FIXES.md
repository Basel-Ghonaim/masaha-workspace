# PR #50 — review fixes (one list)

An independent review ran on `cfd1a5a`: no blocker; four behaviour should-fixes, two test gaps, one
document, and nits. The report is `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW50_REPORT.md`
(read each item there for its file, line and scenario). The analyst verified items 2, 3 and 7 in the
code. Fold each fix into the commit it corrects (fixup + autosquash, `--force-with-lease`); ONE
"Review fixes" comment; the PR description updated. No subagents. Check each item against the code
first and push back with reasons where one is wrong.

## Must fix

1. **The 429 hold must not depend on a row being mounted** (report items 1 and 2). Today a filter or
   page change unmounts every row, `gcTime: 0` drops the failed action and the hold lifts while the
   server still refuses; and a hold found again later counts the full wait from mount.
   - **The owner's decision:** the hold becomes **client state of the `spaces` feature**: one deadline
     ("the actions wait until T"), set by any action's 429 to `now + retryAfter` (the later of the two
     when one already stands), read by `useSpaceActionsHold`, which counts down **the time left**
     (`T - now`) and clears itself at `T`. Where it lives follows architecture §3 *Where state lives*
     (your choice; say which). **`gcTime: 0` stays** on every row action; each failure keeps its own
     toast.
   - **The Undo's restore leaves the cache once it settles** (it stays today, through the unmounted
     row's observer). Test that it is gone.
   - **Tests:** a 429, then a filter change, then a page change → every menu still waits until `T`;
     a page left and opened again during the wait → the wait shown is the time left, not the full
     one; at `T` the menus act again. Make each break once (the old mutation-state reading; the full
     wait from mount).
2. **The search keeps a typed space** (item 3): reset the field only when its own trimmed reading
   differs from the address's `q`. The test that types `' Focus '` also asserts the field still reads
   `' Focus '`; add "Gaza " then "C" → "Gaza C". Make the break.
3. **Paging by keyboard keeps its place** (item 4): `placeholderData: keepPreviousData` on the list's
   query, so the rows and the pagination stay while the next page loads (the region `aria-busy`
   meanwhile, the status rules adjusted so it is not "loading"); the focused page link keeps the
   focus. Test it. This also keeps the rows' menus mounted through a page change.
4. **Hide/Show's direction is tested** (item 5): in the menu test, Hide asserts "…is hidden from the
   site" and the body `isHidden: true`; Show on a hidden space asserts "…is visible again" and
   `false`. Break: `isHidden: space.hidden`.
5. **The refetch-failure test waits for the failure** (item 6): `waitFor` until the refetch has
   settled, then assert the rows stay. Break: drop the "a failed refetch keeps the list" rule.
6. **Finding 45's cause** (item 7): reword it — the site's entry imports the design-system barrel,
   which re-exports `DataTable`, and the web package declares no `sideEffects`, so the table is a
   static import; drop "the same placement as finding 27". *Resolves when:* a `sideEffects`
   declaration or a separate barrel for the data components keeps it out of the first download,
   proven by the manifest. The fix itself waits for S2b-3b (Leaflet).

## Nits — fix
7. `useRefreshAdmin`: `cancelRefetch: false`, so a second row's write doesn't cancel the first's
   refetch.
8. `space-links.md`: the placeholder rows show on the first load only once item 3 is in — word it as
   the code then does. `lookups.md`: the select sits in the list's own field, not the page's.
9. One behaviour, one lane: drop the request paths repeated in the hook and menu tests (the
   repository's unit test owns them) and the two route tests that repeat `filtersOf`.
10. The Undo test deletes two spaces and undoes the first. Break: restore the latest deleted.
11. `SpacesPage` passes the row through; the `hidden` mapping moves to the slot's own type or the
    menu's hook, so the page holds no logic.

## Not fixed (the owner's call)
- An unknown but valid `?area=` / `?governorate=` shows a blank place field; "No match" with Clear
  recovers it. Leave it; one line in `space-links.md` is enough.

## Checks
- Lint and typecheck on each rewritten commit.
- On the head, once each, one at a time: `test:unit`, `test:component`, `test:api`; then
  `NODE_ENV=production npm run build` and `check:build`. Servers stopped afterwards, ports free.
- Report once CI is green and GitHub shows `CLEAN`: save it to
  `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\S2B3A_FIXES_REPORT.md` and summarise it here — the
  head, what changed per item, the breaks, the counts, anything unexpected, and
  `git merge-tree --write-tree` of your head against worker B's open PR (`docs/work-method`) if it
  exists by then. Don't merge.
