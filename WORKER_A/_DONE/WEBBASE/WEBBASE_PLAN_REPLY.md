# WEBBASE — reply to your plan

A careful plan: the layer that knows keys but not meanings, the title from one source the top bar
shares, and finding 42's method (reproduce and prove the cause before any fix) are exactly right.
**Approved.** **First, save it** (as approved here) to
`C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\WEBBASE_PLAN.md` — `PLAN\` does not hold it yet.

## Start from the latest main

`main` moved while you planned: it is now **`068efc6`** (#62, the users item, and #61, the design
archive, merged). The main folder is already there, clean. Run `git fetch --prune origin`, check
`HEAD` is `origin/main` and the tree clean, then cut `refactor/web-storage-titles` from it.
- #62's edits to `findings/README.md` and `workflow.md` are in `main`: build on them; no conflict
  remains there. Findings 51–54 are taken (B's and the amenities worker's); yours stay **55–56**.
- **The amenities worker's PR may open meanwhile** (`feat/space-own-amenities`). It edits
  `features/lookups/`, the `lookups.ts` catalogues and **one fixture line** of
  `pages/dashboard/routes.component.test.tsx`, which your D3 also edits: keep to your hunks; whichever
  PR merges second resolves it keeping both sides.

## The owner's decisions (§13)

1. **Stronger decisions 1–5 and 7:** approved.
2. **The lint rule's exemptions** (`shared/storage`, `src/test`, test files): approved.
3. **D2b:** approved — written as a rule now, built with its first page. **One condition:** the rule
   must serve the **top bar** as well as the tab. The space's edit screen (S2b-4, next) shows the
   space's own name as its page title (the design's SH-016: a sub-page's h1 is the record's name), and
   with your Stronger decision 3 `PageHeader` reads only the route. Write D2b so the record's name
   reaches the one place both read (the top bar and `document.title`), and check now that your
   `usePageTitle` / `DocumentTitle` shape lets that be added without reworking them; say how in the
   plan's D2b paragraph.
4. **Architecture §3's first-download sentence, widened to titles:** approved.

## Reminders

- Every new test seen failing first; finding 42's counts (loops, load, the five full runs) written in
  its resolution and the report, whatever they show.
- At the report, `git merge-tree --write-tree` against every open PR (the amenities worker's, the
  design fixer's `design/admin-rest`).
- The analyst reviews it. Don't merge. Stop every background shell you start; `jq` is not installed —
  use `gh … --jq`.
