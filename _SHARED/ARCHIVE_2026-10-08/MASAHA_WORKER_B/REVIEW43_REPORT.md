# Review — PR #43 (S2a-2: the admin's lookups screen), pinned to `2a98662` vs `315aa52`

**Verdict:** not ready to merge as the pattern to copy. There are no blockers, but 6 should-fix findings, 4 of them in the row-action pattern every admin screen will reuse.

Paths are relative to `apps/web/src/features/lookups/` unless stated.

## Findings

**1. Should-fix: a failure that arrives after a later action starts is never shown.** `hooks/list/useGovernorateCard.ts:105-106`
- **Scenario:** the admin hides area A, and the request is slow and later fails. Meanwhile the admin hides area B on the same card; per-row `busy` allows that. Because `last = onCard.at(-1)` is B, the card shows no failure while B is pending and still none after B succeeds. A's failure never appears, and its switch quietly stays as it was.
- **Why it matters:** K4's "next action clears it" should clear a failure that was already shown, never one that arrives afterwards.
- **Fix:** show the newest failure unless an action that started after it has settled. Or keep the failure in card state, set it in `onError`, and clear it when a new action starts.

**2. Should-fix: a card's failure comes back after leaving the page.** `hooks/list/useGovernorateCard.ts:39-47`
- **Cause:** `useMutationState` reads the whole MutationCache. Row mutations keep the default 5-minute `gcTime` (`shared/api/query/queryClient.ts` sets none).
- **Scenario:** an action fails, and the admin leaves and comes back within 5 minutes. The old "change wasn't saved" shows again. For a 429, `useRetryCountdown` restarts the full countdown on mount.
- **Fix:** keep only actions submitted since the card mounted (`state.submittedAt >= since`). Or give the row mutations `gcTime: 0`. Add a remount test.

**3. Should-fix: the card ignores the 429 wait.** `hooks/list/useGovernorateCard.ts:107`
- **Scenario:** `useRefusalView` returns `blocked`, but the card drops it. The card says "Try again in 0:30" while every switch and arrow stays enabled. Each click is refused again and replaces the countdown. Forms honour `blocked`; this card does not.
- **Fix:** add `blocked` to the row's busy state and the list-moving state in `controlsOf`.

**4. Should-fix: adding the first governorate destroys the open sheet and loses focus.** `components/list/GovernoratesSection.tsx:31-41`
- **Cause:** the same `add` element is rendered inside `EmptyState` when the list is empty, and inside `<div>` under a fragment when it is ready. These are different parents, so React remounts it.
- **Scenario:** on an empty platform the admin adds a governorate and saves. The refetch turns the status to `ready`, so the sheet and its trigger unmount and focus falls to `<body>`. This breaks the sheet rule "focus returns to its trigger", and no test covers the empty-to-ready path.
- **Fix:** render the add sheet in one stable position for every status. Add a test that adds from empty and expects focus back on the trigger.

**5. Should-fix: pressing an arrow or the switch disables the focused control, which drops keyboard focus.** `components/list/RowControls.tsx:23,33,42` (states from `useGovernorateCard.ts:69,74,81`)
- **Scenario:** a keyboard admin presses ↓. The row becomes busy, so the focused button becomes `disabled` and focus falls to `<body>`. The same happens with a press that reaches the edge, where the arrow stays disabled. The admin then has to tab back from the top after every move or toggle, against foundation §10 (full keyboard use in dashboards).
- **Why it matters:** this is the list pattern every admin screen will copy.
- **Fix:** for pending states, use `aria-disabled` with a guarded handler instead of `disabled`. When a row reaches an edge, move focus to its other arrow.

**6. Should-fix: the governorate header's controls never wrap on a phone.** `components/list/GovernorateCard.tsx:44-50`
- **Cause:** `CardAction` is a fixed second grid column (`col-start-2 row-span-2`, `Card.tsx:53`).
- **Scenario:** on a phone, two 44px arrows, the switch and Edit squeeze the names and count into the space that is left. The PR body's line "a row's controls wrap under its names" is true only for `AreaRow`.
- **Fix:** let the header's controls wrap under the title on narrow screens, or narrow the PR's claim.

**7. Nit: a write whose refetch fails shows nothing.** `hooks/useRefetchGovernorates.ts:10`, `hooks/list/useGovernoratesSection.ts:15-25`
- **Scenario:** `invalidateQueries` absorbs refetch errors, so the mutation succeeds. The section reports an error only when it has no list at all, so the old list stays on screen with no message.
- **Fix:** add a "couldn't refresh" line when `isRefetchError` is true.
- **Related:** a network failure or timeout on a write does not refetch, though the server may have applied the write.

**8. Nit: the list's load failure skips `useRefusalView`.** `hooks/list/useGovernoratesSection.ts:40-45`
- **Scenario:** a 429 shows a fixed line with no countdown, a 5xx shows no request reference, and Retry stays enabled while a fetch is already running.
- **Fix:** read the error through `useRefusalView`, and expose `blocked` and a `retrying` flag from `isFetching`.

**9. Nit: K7 is not tested in Arabic.** Every component test runs in English (`GovernoratesSection.component.test.tsx:69`), so a hook that swapped the primary name by language would still pass. **Fix:** add an Arabic case that expects the level-2 heading to be the English name.

**10. Nit: an empty governorate says so twice.** The count line «لا مناطق» / "0 areas" (`GovernorateCard.tsx:42`) repeats "No areas yet" (`:55`). **Fix:** drop one of them at zero.

**11. Nit: the edge-arrow rule is proven twice in the same lane.** `GovernoratesSection.component.test.tsx:93` and `useGovernorateCard.component.test.tsx`. **Fix:** keep the hook's proof, and retitle the component test to cover names and the switch only.

**12. Nit: misleading comment.** `shared/copy/plural.ts:10` says "pinned to Western digits", but `Intl.PluralRules` formats no digits; the number comes from `String(count)`. **Fix:** drop the comment.

## Verified OK

**Hooks, Query, security (subagent 1, plus my own check)**
- **K1 keys:** the query key is `['admin','lookups','governorates']`, and row mutation keys are `['admin','lookups','row',kind]`.
- **A1:** `onSuccess` returns `invalidateQueries`, and the order hooks' `onError` refetches on a 409. Mutations stay pending until the list arrives, with no stale window.
- **K3 per-row filtering:** it is done by variables, not key prefix. A governorate isn't blocked by its areas, area orders are scoped to their card, and edge arrows and `moved()` at both ends are handled.
- **No retries:** `retry: false` is set globally for queries and mutations.
- **StrictMode and window focus:** no request is sent twice, and a focus refetch leaves the pending UI alone.
- **Sheet:** it closes only after the refetch, and `not_unique` lands on `nameAr`.
- **Route:** it keeps `RequireRole roles={['ADMIN']}`, the page is a lazy import, and the routes file holds only paths, guards and lazy imports.
- **Text and tests:** no user text is inserted as HTML, no `vi.mock`, and no parameter exists only for tests.

**Components, accessibility, plurals, tests, documents (subagent 2)**
- **Plurals:** all six Arabic categories and English are tested, including 100–102 and 111. `plural.ts` is not exported from the barrel, and both catalogues have the same keys.
- **A3:** accessible names use the interface's language and are isolated. The Edit names keep their visible label.
- **A2(a):** a hidden row or card is shown by the badge and the switch state, not only by colour, and without a surface tint.
- **Sheet:** it opens at `side="end"` with the first field focused, the first invalid field takes focus, and errors are linked to their fields. The Active switch appears only when editing (K8). Focus returns after an edit, and axe runs on the section and on the open sheet.
- **Components only render:** no component holds an `AppError` or a mutation.
- **Styling:** logical classes and tokens only, and the arrows don't mirror.
- **Documents:** the architecture.md status line, §2, §3 and §7, localisation.md and finding 28 match the code.
- **Commits:** 5 Conventional commits, all subjects ≤ 50 characters, each a complete unit.

## Tokens

About 295k in all:
- subagent 1: 97k;
- subagent 2: 103k (it restarted once after a connection drop);
- this conversation: about 97k.

That is well under the 600k limit. Two subagents were used, with no third.
