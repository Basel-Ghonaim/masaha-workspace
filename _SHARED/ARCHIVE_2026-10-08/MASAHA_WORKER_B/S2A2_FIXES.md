# PR #43 — review fixes and rebase (one list)

The review gate ran on `2a98662` (no blockers, six should-fix); the analyst verified items 1, 3, 4
and 6 in the code. Four of the six sit in the pattern every later admin screen will copy, so fix them
as patterns. Fold each fix into the commit it corrects (fixup + autosquash, `--force-with-lease`); no
"fix" commits. Then post ONE "Review fixes" comment and update the PR description. No subagents.

**Keep this round tight:** only these items, the smallest change that closes each; add only the tests
an item names. If an item turns out bigger than described, stop and report.

## 0. Rebase first

PR #42 (Google sign-in) has merged, so #43 now conflicts with `main` in
`docs/frontend/architecture.md` (the status line, and §3's list of what each feature exports).
`git fetch --prune origin`, rebase on `origin/main`, keep both sides (#42's `features/auth` and
Toaster lines, and your `features/lookups` lines). `findings.md` should merge on its own; your finding
28 widening stays as it is, after main's findings up to 35.

## Must fix

1. **A failure can disappear unseen** (`useGovernorateCard.ts:105`, `onCard.at(-1)`): with two rows
   acted on together, the card shows only the newest action, so the first one's failure is never
   shown if the second is pending or succeeds. Rule: **a failure stays visible until the user acts
   again on that same row (or list, for an order)**; an action on another row never hides it. Test:
   row A fails while row B succeeds → A's failure shows.
2. **A failure comes back after leaving the page:** finished mutations stay in the cache for 5
   minutes, so returning shows an old failure and restarts a 429 count. Give the card's mutations
   `gcTime: 0` (they still show while the page is mounted). Test: unmount and mount again → no
   failure.
3. **The card ignores the 429 wait** (`useGovernorateCard.ts:107` keeps only `view` from
   `useRefusalView`): honour `blocked`, so the switches and arrows of that card stay disabled while
   the count runs. Extend the existing 429 test.
4. **Adding the first governorate closes the sheet and loses focus** (`GovernoratesSection.tsx`): the
   add button is rendered inside the empty state, then elsewhere once a governorate exists, so React
   rebuilds it. Render **one** add button in one place whatever the state (the empty state keeps its
   title and description only), so the sheet's trigger survives and focus returns to it. Test: add
   the first governorate → focus is back on "Add governorate".
5. **Keyboard focus is lost on every toggle or move** (`RowControls.tsx`): the pressed control
   becomes `disabled` and focus falls to the page. Keep the pressed control focusable while pending
   (`aria-disabled` and ignore presses, instead of `disabled`), or move focus deliberately to the same
   control in its new place after an order. Test: after pressing "Move down" with the keyboard, focus
   is on that row's control, not `body`.
6. **The governorate header's controls don't wrap on a phone** (`GovernorateCard.tsx`, `CardAction`):
   make the header wrap as the area rows do (frames 02 and 04), and retake the two phone screenshots.

## Cheap nits — fix
- The list's load failure goes through `useRefusalView` too (countdown and request reference), so
  the section's error state follows the same pattern as the card's.
- An empty governorate says "no areas" once, not twice.
- Remove the duplicate edge-arrow test (same lane).
- Correct the misleading comment in `plural.ts`.

## Left as they are
- A refetch that fails after a successful write shows no message (the next action or the page's own
  focus refetch recovers); the K7 test in Arabic.

## Your database
If the owner tells you "yes, reset masaha_b_dev", reset and reseed it before retaking the
screenshots; otherwise leave it.

## Checks — don't re-run what already passed
- Lint and typecheck on each rewritten commit.
- On the head, once: `check:classes`, `test:unit`, `test:component`. Skip `test:api` and
  `build` + `check:build` locally (no API or route change in this round); CI runs every lane on the
  pushed head.
- Report once CI is green and GitHub shows `CLEAN`: the head, what changed per item, the counts.
  Don't merge.
