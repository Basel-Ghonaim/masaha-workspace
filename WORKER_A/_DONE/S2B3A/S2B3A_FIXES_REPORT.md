# S2b-3a — review fixes report (PR #50)

**Head:** `a65e08c` (reviewed: `cfd1a5a`), still on `5d692f3`. CI green on the head (9/9), GitHub `CLEAN`. One "Review fixes" comment posted; the PR description updated. Not merged.

**Commits** (fixes folded in, no fix commits):
1. `b448069 refactor(space-links): group the switcher's files`
2. `1dc3333 feat(lookups): add the governorate and area select` — nit 8 (lookups.md)
3. `b5954bc feat(space-links): list the admin's spaces` — items 2, 3, 5, nit 8
4. `6c1610b feat(spaces): hide, show and delete a space` — items 1, 4, nits 7, 9, 10, 11 (type)
5. `a65e08c feat(spaces): add the admin's spaces list` — item 6, nit 9 (page tests), nit 11 (page), item 1's page test

Each item was checked against the code; all held, none pushed back.

## Per item

1. **The 429 hold no longer depends on a mounted row.** Where it lives: the query cache, `['admin', 'spaces', 'hold']`. That is architecture › *Where state lives*' TanStack Query: the server holds the rate-limit window, and the cache keeps its last answer, cleared with the user's data at sign-out.
   - `useRecordHold` sets the time from any action's 429, the Undo's restore included: `now + Retry-After`, the later of two.
   - `useSpaceActionsHold` reads the time left (`T - now`), counts it down through `useRefusalView`, so the wording keeps its one owner, and clears the time at T.
   - `gcTime: 0` stays on every action, and each failure keeps its toast.
   - The Undo's restore leaves the cache once it settles (`restore.reset()`).
   - Tests (hook): the hold survives the refused rows unmounting; a page opened 10 s into a 30 s wait shows 0:20; at T the menus act again and the time is cleared.
   - Test (page): a 429, a filter change that removes the refused row, then a page change; every menu still waits.
   - Test (delete hook): the Undo's restore leaves the cache.
2. **The search keeps a typed space:** the field resets only when its trimmed reading differs from the address's `q`. The `' Focus '` test now also asserts the field; new test: "Gaza " → pause → "C" gives "Gaza C" and `q=Gaza+C`.
3. **Paging keeps its place:** `placeholderData: keepPreviousData`. The rows and pages stay while the next page loads, with the region `aria-busy`. The status stays `ready` (placeholder rows show on the first load only), and the page-past-the-last rule ignores the placeholder. Tests: hook (rows, pages, busy) and component (the focused "Page 2" link keeps the focus and becomes current).
4. **Hide/Show's direction** is tested in the menu test: the toast and the body (`isHidden: true` for Hide, `false` for Show on Palm Hub).
5. **The refetch-failure test** waits until the refetch has failed in the cache, then asserts the rows stay.
6. **Finding 45 reworded:**
   - Cause: the barrel re-exports `DataTable`, with no `sideEffects` in the web package.
   - Dropped: "the same placement as finding 27".
   - *Resolves when*: a `sideEffects` declaration or a separate data entry keeps the table out, proven by the manifest, the fix waiting for S2b-3b.
7. `useRefreshAdmin`: `cancelRefetch: false`.
8. Documents:
   - `space-links.md`: the states line as the code does now; two decisions (keep the previous page; the search keeps what was typed); the line on an unknown but valid place id.
   - `lookups.md`: the select sits in the list's own Field.
9. Paths no longer asserted in the hook and menu tests (counts, bodies and toasts instead). The two page tests that repeated `filtersOf` are removed.
10. The Undo test deletes Palm Hub then Focus Hub and undoes Palm Hub's; on the fake server only Palm Hub's restore succeeds.
11. `SpacesPage` passes the row through. `SpaceRef` is `Pick<AdminSpaceRow, 'id' | 'nameEn' | 'nameAr' | 'state'>`, and the menu's hook reads `hidden`.

Not fixed (the owner's call): an unknown but valid place id; one line in `space-links.md`.

## Breaks made once (each test failed, then restored)

- Hold, old mutation-state reading: 3 hook tests failed (rows unmounted, time left, cleared at T).
- Hold, the full wait counted from mount: "counts the time left…" failed.
- Undo restores the latest deleted: failed. The restore kept in the cache: failed.
- Search, the old reset: 2 failed.
- Paging: both new tests failed before `keepPreviousData`.
- Hide/Show direction (`isHidden: hidden`): 2 failed.
- Refetch failure, `error` on any `isError`: failed.

## Counts on `a65e08c`

- Lint and typecheck: on each rewritten commit.
- Lanes, one at a time:
  - `test:unit`: 158 + 622 + 665
  - `test:component`: 746
  - `test:api`: 534
- `NODE_ENV=production npm run build` and `check:build`: "No showcase code in 32 build files (1014 strings checked). No dashboard code in the site's first download."
- `format:check` and `check:classes`: clean.
- CI on the head: 9/9 pass.

## Unexpected

- **The autosquash replanted the branch.** `main` had moved to `8310d6e` (worker B's #51, `docs/work-method`, merged), and running the autosquash onto `origin/main` moved the commits onto it. My standing notes already say to autosquash onto the branch's own base; I didn't. The commits were moved back onto `5d692f3` before the push (`git rebase --onto 5d692f3 origin/main`), since GitHub showed no conflict.
- **`git merge-tree --write-tree` of the head against the new `main`** (worker B's PR is already merged): clean, tree `f4fd3b3`, exit 0.
- **A filtered run that starts with the spaces page fails its first 3 s wait.** It fails the same way on the code before these fixes, so this is the finding-28 class: the cold first transform of the lazy shell. The whole file passes (31/31), and so does the full lane.
- **Docker Desktop had to be started again** for `test:api`. No servers were left running (the API lane uses Supertest), and ports 3320 and 5320 are free.
