# TABLE_SCROLL — status, paused for memory (2026-11-22, ~12:30 local)

Branch `fix/table-scroll-229` (local only, nothing pushed).

**Done**
- Plan: `2_PLAN.md`.
- Commit 1 `9ad9dbff chore: carry #150's two notes` (C1, C2).
- Commit 2's work, **uncommitted** in the tree: `Table` in `ScrollRegion` with one required name (table + group),
  `ScrollRegionName` exported, PricesView / HoursSection on `aria-label`, Table test rewritten, three caller tests
  extended, finding 229 + index, foundation §10/§12, spaces.md / directory.md change-log lines. Message drafted in the
  session scratchpad (`msg2.txt`).
- Run: web typecheck; the touched component tests (58 pass); breaks B1–B8 each seen failing, then restored (B7: the
  jsdom axe test cannot see `scrollable-region-focusable`, no layout — Chrome's pass owns it); format:check,
  check:classes, check:conflicts, check:links.

**Stopped**
- The grant script waited 19 tries (~38 min) with 3.4–3.7 GB free (< 4 GB); then Claude Code stopped every background
  task of the session for low machine memory: the API and web dev servers, the queued Chrome run, a watch loop. Their
  orphaned children (tsx watch 17732, API 24600, vite 13420) were stopped by PID; 3320 and 5320 are free; no grant slot
  held. Docker Desktop and `masaha-postgres-1` were started for the run and are still up.

**Left**
- lint, typecheck (root), test:unit, test:component (full), production build + check:build — all through the grant.
- Commit 2 (after lint/typecheck), the Chrome axe pass (`scripts/axe.mjs`, ready: public hours 320/390 as a guest;
  owner's profile prices 320/390; customers DataTable 390/768; ar/en, light/dark; rings), `#PRNUM` → 152, push, PR,
  CI green + CLEAN, `4_REPORT.md`.
- Departure to report: the public page shows prices as a grid, not a table; the prices table lives on the owner's
  profile, so the script checks the profile for prices and the public page for hours. At 390 a DataTable draws cards
  (no Table), so 768 is added for its table.
