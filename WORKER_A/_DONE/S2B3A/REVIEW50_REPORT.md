# Review — PR #50 (S2b-3a: the admin's spaces list and its actions)

Head reviewed: `cfd1a5a` (base `5d692f3`), read from commit objects only. CI green on that head.

**Verdict: changes requested — no blocker; four behaviour should-fixes, two test gaps, one document's cause.**

## Findings (most severe first)

1. **should-fix — a filter or page change lifts the 429 hold (L5).** `spaces/hooks/hide/useSetSpaceHidden.ts:22` (and the same `gcTime: 0` in delete and restore), `spaces/hooks/hold/useSpaceActionsHold.ts:27`, `space-links/hooks/admin-list/useAdminSpacesList.ts:50`, `DataTable.tsx:180`.
   - **Scenario:** Hide gets a 429 with a 60 s wait. The admin then changes a filter or a page. The new key has no data, so the status is `loading`, and DataTable replaces every row with a placeholder. Every menu unmounts, and `gcTime: 0` removes the failed mutation.
   - **Result:** the banner goes, and the next page's menus act while the server still refuses. No test changes the filter during a hold.
   - **Fix:** keep the 429's deadline somewhere that does not depend on a row being mounted. One way: keep rate-limited actions until `submittedAt + wait`. This touches the `gcTime: 0` rule, so escalate it to the owner.

2. **should-fix — the Undo's restore never leaves the cache, and its 429 holds again for the full wait.** `spaces/hooks/delete/useDeleteSpace.ts:37`, `useSpaceActionsHold.ts:39-48`, `shared/forms/hooks/useRetryCountdown.ts:19-41`.
   - **Cause (verified in query-core 5.104.1, `mutationObserver.js:126-131`):** `restore.mutate` on an unmounted row's observer re-adds that observer to the new mutation. Nothing removes it, so `gcTime: 0` never applies.
   - **Scenario:** that restore fails with a 429. On a later visit to the page, minutes on, the hold finds it as a standing 429. `useRetryCountdown` then counts the full `retryAfterSeconds` again from mount (`endOf` only chooses the longest wait), so every menu waits again for no reason.
   - **Fix:** count the time left as `endOf(action) - Date.now()` and drop expired 429s. Also remove the restore's mutation once it settles. Add a test that the Undo's restore leaves the cache.

3. **should-fix — the search field eats a typed space.** `space-links/hooks/admin-list/useAdminSpacesFilters.ts:36-40`.
   - **Scenario:** type "Gaza " and pause 400 ms. `textSchema` trims, so `q=Gaza` is written, `filters.q !== shownQ` resets the field to "Gaza", and the next key gives "GazaC". People often pause between words.
   - **Fix:** reset `text` only when its own trimmed reading differs from `filters.q`. The test that types `' Focus '` should also assert the field still reads `' Focus '`.

4. **should-fix (a11y) — paging by keyboard loses the place.** `useAdminSpacesList.ts:33,65`, `AdminSpacesList.tsx:39-47`.
   - **Scenario:** while the next page loads, `pagination` is `null`, so the focused link unmounts and focus goes to the region. The keyboard user must tab through the toolbar and up to 20 menus to reach "Next" again, on every page.
   - **Fix:** `placeholderData: keepPreviousData` with the status rules adjusted, or keep the last pagination while loading.

5. **should-fix (test) — no test proves which way Hide/Show flips.** `spaces/hooks/menu/useSpaceActionsMenu.ts:35` sends `isHidden: !space.hidden`. The menu test checks only `put /admin/spaces/7/hidden`, and the hook tests pass `isHidden` in themselves. Changing it to `space.hidden` passes every test.
   - **Fix:** in the menu test, assert the "…is hidden from the site" toast, and add Show on Palm Hub asserting "…is visible again".

6. **should-fix (test, plausible) — the flake's pattern remains.** `useAdminSpacesList.component.test.tsx:148`, "keeps the rows already shown when a later fetch fails", asserts `ready` straight after `act(() => client.refetchQueries())`. The failure reaches `useQuery` on a later `setTimeout(0)`, so the assertion can read the render from before the failure. The test would pass with the rule broken.
   - **Fix:** `waitFor` until the refetch has settled (`useIsFetching() === 0`, or the query's `isError`), then assert.

7. **should-fix (document, plausible — not built) — finding 45's cause and its fix.** `docs/architecture/findings.md:512,514`.
   - **Evidence:** `apps/web/package.json` declares no `sideEffects`, and the site's entry imports the design-system barrel, which re-exports `DataTable` (`design-system/index.ts:71`). So the table is reached statically from the entry.
   - **What is wrong:** finding 27's chunk is lazy, so "the same placement as finding 27's" is wrong, and a chunk group would very likely still be imported statically.
   - **Fix:** reword the cause (this PR triggers it; the barrel/`sideEffects` setup was already there), and make "Resolves when" a `sideEffects` declaration or a separate data barrel, proven by the manifest. Leaving the fix itself to the next item is right.

8. **nits**
   - `spaces/hooks/useRefreshAdmin.ts:12` (plausible): two rows acting at once. B's `invalidateQueries` cancels A's refetch (`cancelRefetch` defaults to true), so A's toast can come before the list shows A's change. Use `cancelRefetch: false`, or document it.
   - `docs/features/space-links.md:50` says "placeholder rows while the first page loads". They show on every filter or page change too.
   - `docs/features/lookups.md:49`: the select sits in the list's own Field (`AdminSpacesToolbar`), not the page's.
   - Paths are tested in two lanes: `useDeleteSpace.component.test.tsx:84` and the menu test's `writes()` (lines 95, 172) repeat the repository's unit test. Two route tests repeat `filtersOf`.
   - The Undo test has one space. Delete two and undo the first, to catch "restores the latest deleted".
   - `pages/dashboard/admin/SpacesPage.tsx:17` maps `hidden: row.state === 'hidden'` itself. It is harmless; note it, or move it to the slot's type.
   - An unknown but valid `?area=` or `?governorate=` shows a blank place field. "No match" with Clear recovers it.

## Verified OK

- **Seam (L1):** no feature imports another. `AdminSpacesList` takes only the shared row and its own `PlaceField`. Both slots are made once in the page module, and S2b-4 can reuse `SpaceRef`.
- **Columns:** `useMemo` on `[headers, noOwner, actions]`, all stable. The "leaves the focus where it is when another row leaves" test would fail with rebuilt columns.
- **Address (L3):**
  - each value is read with the contract's schema, an invalid one falling back to its default; an area wins over a governorate; the defaults are left out
  - a filter change replaces the address and returns to page 1; the pages are links; a page past the last is replaced by the last
  - the debounce reads `latest` and is cleared on unmount
  - the tests fail if a filter is dropped
- **Mutations:**
  - each write stays pending through `await invalidateQueries(['admin'])`
  - the Undo restores the row's own id after unmount (tested)
  - the toasts have no ids, so no failure replaces another; failures stay with their reference
  - the hold takes the longest standing 429, not the latest failure (tested)
  - `gcTime: 0` is on all three actions
- **Focus and a11y:** the dialog opens on Cancel and returns the focus to the busy trigger; the focus moves to the region when its row leaves. Names are isolated in accessible names and marked `lang="en"` in the title and toasts (tested). There is one layout per breakpoint, and axe runs on the table, the cards, the menu and the dialog.
- **Copy:** the keys match (`satisfies Catalogue`), and the Arabic matches S2B3A_PLAN_REPLY, «صاحب المساحة» and «…ويمكنك التراجع فور الحذف.» included.
- **Scope:** no API, shared or lock-file change, no `vi.mock`. `fixtures.json` is justified and harmless.
- **Commits:** five Conventional Commits, 41–50 characters, no trailers; `f6dd4ed` only renames files and changes import paths.
- **Documents:** the §7 line is one rule with one example; §2, overview and the other anchors are accurate; finding 44 is accurate.

## Tokens

Subagents: 128.5k + 149.7k = 278k. This conversation: about 130k. Total about 410k, under the 600k limit.
