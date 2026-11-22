# Carried from #150 (AXE_FIXES) — into the next PR's first commit

#150 merged 2026-11-19 (merge `9b4c4fc1`). Its small notes, found by the supervisor's verification, go into **the next
Work Item's first commit** (the owner's rule for small review findings), named in that PR's description. Move this file
into the next task's folder when its prompt is written.

- **C1 — a comment past 100 columns:** `apps/web/src/features/finance/components/OccupancyTab.tsx`, the component's doc
  comment, its second line (about 123 columns: "…768 px, reached by the keyboard — and visits and members per day. While
  it loads, …"). Rewrap at 100, words unchanged.
- **C2 — foundation §3's category table lags §12:** `docs/frontend/design-system/foundation.md` §3, the *Categories*
  table — `display` lacks `Meter`; `data` lacks `BarChart` and `Heatmap`; `feedback` lacks `Refreshing` (all four in §12
  and in the code). Add them to their rows.

**Not carried — a task of its own, for the owner to decide:** the space profile's «الأسعار المعلنة» table fails axe's
`scrollable-region-focusable` at 320 px (its container `div[data-slot="table-container"]`, the layer's `Table`, scrolls
with nothing focusable in it) — on `main` before #150 too, outside finding 224. Seen by the worker's Chrome pass and by
the supervisor's. Would become finding **229** (check the index) and its fix would use `ScrollRegion`.
