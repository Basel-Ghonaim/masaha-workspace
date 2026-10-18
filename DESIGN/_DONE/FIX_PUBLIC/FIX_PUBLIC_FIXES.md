# FIX PUBLIC — review fixes for PR #65

From the analyst's conformance review of head `51685d0` (a read-only reviewer against the prompt,
the plan with the reply's changes, the decisions and your report). Nothing must be fixed before
review; the items below are for this round. **Method:** fold each into the commit of its decision
(fixup + autosquash), `git push --force-with-lease`, ONE "Review fixes" comment, a "Review fixes"
section in `REPORT\FIX_PUBLIC_REPORT.md`. Your two scripts at every commit; CI for `format:check` and
`check:links`; your eyes on each fixed part at 390 and 1440 (and 1024 where it is the Directory).
Stop every background shell you start; `jq` is not installed — use `gh … --jq`.

## Should fix

- **R1 — U2: «اختر منطقتك» is dead on a desktop list.** At `lg` and up in list view it only sets
  `sheetOpen` (`Directory.html:236`), and the sheet draws nothing there (`wide='none'`); the stale flag
  then opens the sheet by surprise on the next switch to the map. At `lg` in list view, scroll to the
  sidebar's «المنطقة» field and focus it; open the sheet only below `lg` or in the map view.
- **R2 — U7: «تغيير الموقع» on Home leaves a dead state.** Home has no map; `startPick` empties the
  location and `LocationStatus` shows nothing for `picking`. On Home, send «تغيير الموقع» to
  `Directory.html?view=map&pick=1`, as `onPickOnMap` does.
- **R3 — U3: the space page's map label uses the raw English name** (`space-parts.jsx:350`,
  «موقع Focus Hub» on the Arabic page). Use `spaceName(space)`.
- **R4 — the report:** add to §8/§9 (a) the new top-level `const spaceName` in `shared.jsx` (on `main`,
  `Admin owners.html` declares its own; #66 removes it, so the merged tree is clean — say so), and
  (b) the conflict check against `design/admin-rest` (now pushed: only `CHANGES.md` conflicts).
  Also list Golden's profile note («قبل شهرين», not the decision's example «قبل 4 أشهر») and U4's
  sections without a date (about, location) as departures.

## Small

- Remove what nothing reads: `M.minPrice` (`data.js:50`, `:63`) and each space's `updated` text
  (`data.js:36–41`); the unused `Tabs, TabsList, TabsTrigger` (`Directory.html:25`).
- Duplicate ids below `lg` (the hidden sidebar and the sheet both mount `FiltersForm`:
  `price-group`, `spaces-group`): use `React.useId`.
- Two identical `HeartIcon`s (`shared.jsx:490`, `account.jsx:38`; the latter wins on the account
  pages): keep the shared one, remove `account.jsx`'s.

## The owner's decisions on your new design issues and on DI-27

Decided by the owner; build them in this round, each in the commit of the decision it belongs to:
- **The map in light theme is pale** beside the new cards: strengthen its drawing (tokens only).
- **The space page's gallery** still shows the old grey «صورة n» tiles: draw them as the card's
  stand-in, so a card and its page match.
- **The phone's map view has five rows of controls above the map:** reduce them so the map leads on a
  phone (fold what can live in the filter sheet or one row); show the result at 390.
- **DI-27, the shared globals bug, fixed at its root in `shared.jsx` (yours now):** `ActionButton`
  (and any shared component) must not use object rest destructuring, whose Babel helper
  (`_excluded`) is a page-wide global that a later script overwrites (profile-a's `ClockInput`, inline
  scripts on the overview and the lookups). Rewrite it without rest (pick the props, pass the others
  explicitly), check no other shared part relies on `_excluded`, and say in `CHANGES.md` and the
  README's check-scripts paragraph that a module or page script must not use object rest. Verify on
  a page that loads the editor's modules (`Admin space edit.html`, `Owner space profile.html`) that an
  `ActionButton` works. The other design worker's workaround stays in its file.

**Merge order:** whichever of #65 and #66 finishes its fixes first merges first; the second rebases,
keeping both `CHANGES.md` sections (the fast path).

## Recorded, not for this PR

- The editor's map pin now draws as the dashed "no live status" mark (`profile-a.jsx:139`): a location
  pin reading as a state; batch 5 (the editor's map).
