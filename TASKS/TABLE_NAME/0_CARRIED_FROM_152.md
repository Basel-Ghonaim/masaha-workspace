# Carried from #152 (TABLE_SCROLL) — into the next PR's first commit

These are the small notes from the supervisor's check of #152 (2026-11-22). Under the owner's rule for small review
findings, they go into the next Work Item's first commit and are named in that PR's description. When the next task's
prompt is written, move this file into its folder.

- **C1 — the table's name is said twice.**
  - **Where:** `Table` (`shared/design-system/components/data/Table/Table.tsx`).
  - **What:** it puts its one name on both the `ScrollRegion` group and the `table`, so a screen reader hears
    «الأسعار المعلنة» twice: once for the group, once for the table. That holds even while the table fits and the
    group is no tab stop.
  - **Fix to weigh:** name the group only while it overflows, or let the table alone carry the name, as #150 did for
    the photos' list. Then check again with axe and a screen reader's accessibility tree.
- **C2 — `TableCaption` is unused.** No page draws it since #152. Remove it with its showcase use and its §12 mention,
  or keep it with a reason. The worker recorded this rather than doing it.
