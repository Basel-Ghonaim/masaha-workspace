# Review — PR #50 (S2b-3a: the admin's spaces list and its actions)

You are the **independent reviewer** of PR #50. Run from `C:\Users\basel\masaha` (the main folder).
You don't build, fix or merge.

## Budget (hard limits — the owner's)

- **At most 2 subagents. Never a third.** No workflows. Use no plugin skill (workflow §10); you may
  apply testing.md §3's *name the break* and *make the break* as a lens.
- **The whole review stays under 600,000 tokens**, this conversation and both subagents together.
- **Reports:** at most 700 words per subagent, and at most 900 for yours.

## Rules

- **Read-only.** No edits, commits, checkouts, switches, installs, npm or test runs, database
  commands, or GitHub comments. Read only from commit objects. `git fetch origin`, then pin to the
  PR's head: `gh pr view 50 --json headRefOid` (it was `cfd1a5a`); base `5d692f3`. Use
  `git diff 5d692f3...<head> -- <paths>` and `git show <head>:<file>`. State the head in your report.
- **Read in the order workflow §2 gives:** `docs/features/space-links.md` and
  `docs/features/spaces.md` first (at `<head>`: their new web sections and decisions), then only what
  they link and what your area needs. The prompt and the approved plan replies are
  `C:\Users\basel\.prompt\MASAHA_WORKER_A\PROMPT\S2B3A_PROMPT.md`, `S2B3A_PLAN_REPLY.md` and
  `S2B3A_SHOTS_REPLY.md`.
- **Report concrete problems only:** file and line, the failing scenario, the severity
  (blocker / should-fix / nit) and the fix. **Verify each in the code before reporting it.**

## What the PR must be (the owner's decisions)

Web and documents only, no API change, no new dependency. The admin's Spaces page: a table on
desktop and cards on a phone; filters (search, one "Governorate / area" field, the state, "Stale
only"); pagination; the row menu Hide / Show / Delete with a confirmation dialog. Decisions:
- **L1** the page composes three capabilities through two slots on `AdminSpacesList`
  (`actions(row)`, `placeField(field)`): the list's read in `features/space-links`, the actions in a
  new `features/spaces`, the place field in `features/lookups`; no feature imports another.
  `spaces`' writes invalidate the `['admin']` prefix (approved; one platform line in architecture §7)
  and stay pending until the list has arrived.
- **L2** success toasts naming the space (hidden, shown, deleted with a 10 s Undo calling `restore`
  for that id, even after the page has gone; "restored"); **finding 44** recorded.
- **L3** filters and page in the address, each read through the contract's schema, an invalid value
  falling back to its default, a filter change returning to page 1; the search debounced.
- **L4** the place field lists hidden governorates and areas, marked; **L5** a failed action's toast
  names its space with the reference, and a 429 holds every row's menu while it counts down;
  **L6** stale and missing groups both shown; **L7** no "Add space", no "Edit", no owners' items.
- **The plan replies' changes:** an English-only name in an Arabic sentence marked `lang="en"` (the
  dialog's title and the toasts); «صاحب المساحة» for the owner; the dialog's line «…ويمكنك التراجع
  فور الحذف.»; the switcher's files moved into `switcher/` folders (moves only, commit 1).
- **Project rules:** no sibling imports; components present, hooks prepare; one responsibility per
  file, by operation; no parameter, option or callback only tests pass; no `vi.mock` of a module;
  `gcTime: 0` on row actions; no hardcoded text, both catalogues; no CSS outside the design system;
  the dashboard-only rule (`check:build`).

## The split

### Subagent 1 — behaviour, state and accessibility (`apps/web/src`)

**It checks:**
- **The seam (L1):** the slots carry no feature's type into another; the page passes values through
  without logic of its own; nothing a later screen (S2b-4, the owner's) would have to undo.
- **The address (L3):** read and write symmetric; an invalid or conflicting value (`governorate` and
  `area` both, an unknown id, `page` past the last); Back and reload; the debounce not writing a stale
  value after the user has moved on.
- **The mutations:** pending until the refetch; the Undo restoring exactly the deleted space after
  unmount; a delete and an Undo racing; two rows acting at once; the 429 hold (L5) released at the
  right time; a failure never hidden by another (#49's lesson); `gcTime: 0`.
- **Focus and accessibility:** the menu by keyboard, the dialog's focus and its return when the row
  leaves the list; accessible names carrying the space's name; `lang` marking; table vs cards at the
  breakpoint; the phone's filter sheet; axe.
- **The columns' fix** (the table rebuilt its columns each render, losing focus): truly fixed and
  tested.

### Subagent 2 — the tests, the build, the documents and the conformance

**It checks:**
- **Each decision has a test that would fail with broken code** — the breaks the PR lists (a filter
  dropped from the address, Undo restoring another id, the hold following the latest failure only);
  titles match assertions; one behaviour per lane; the repository's calls in the unit lane only.
- **The CI flake's fix** (mutation state delivered on `setTimeout(0)`): every wait now waits on the
  state it asserts, with no fixed sleep; whether the same pattern remains in other new tests.
- **The build:** **finding 45** (TanStack Table in the site's first download, ~70 KB): is the
  evidence right, is the cause the PR's, and is there a fix small enough for this PR (a chunk group
  for what only the dashboard uses) — or is it rightly left for the next item, which adds Leaflet
  and would make it worse? The change to `pages/showcase/fixtures.json`: justified and harmless.
- **The documents:** `space-links.md` and `spaces.md` state the code truly and own only their facts
  (no restated mechanism or endpoint shape); `lookups.md`'s select; architecture §2's built line and
  §7's new invalidation line (a platform rule, one short example); `overview.md`'s lines; findings 44
  and 45 accurate.
- **The copy:** both catalogues have the same keys; the Arabic matches `S2B3A_PLAN_REPLY.md`'s list.
- **The commits:** five, Conventional, ≤ 50 characters, each a complete unit; commit 1 moves only.

## Your output

Write **one file**, `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW50_REPORT.md`: a one-line
verdict; the findings, most severe first, deduplicated (severity, file and line, scenario, fix); a
short "Verified OK" list per area; the tokens used. Then stop.
