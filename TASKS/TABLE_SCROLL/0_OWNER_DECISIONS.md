# TABLE_SCROLL — finding 229 and #150's two notes (2026-11-22)

The owner wants a small production task that runs in parallel while he works elsewhere ("prepare a prompt and tune
it"). The supervisor's recommendations stand as the decisions, logged here. **Merging is the owner's word, always.**

- **T1 — scope:**
  - **Finding 229 (new):** the layer's `Table` scrolls sideways in a container nothing can focus. axe reports
    `scrollable-region-focusable` at 320 px on the space page's «الأسعار المعلنة». The worker records the finding,
    then fixes it.
  - **#150's two notes** (`0_CARRIED_FROM_150.md`, C1 and C2) go in as the PR's **first commit**, named in its
    description.
  - Nothing else: anything more the worker notices is recorded, not fixed.
- **T2 — where the fix lives:** in the design system's `Table`, once for every table: the prices, the opening hours on
  the public space page, and every `DataTable`. Its scrolling container becomes reachable by the keyboard while it
  overflows, and is named, the way `ScrollRegion` does it (#150). The details (reuse `ScrollRegion` or share its
  measuring; where the name comes from) are the worker's plan. It decides and records them; nothing waits for the
  owner.
- **T3 — the executor:**
  - a fresh **Claude Code** worker, **Opus 5.5, effort medium**, in `C:\dev\masaha\app`;
  - branch `fix/table-scroll-229`, PR expected **#152** (#151 is the design Issue);
  - one worker on the machine.
- **T4 — no stop for the plan** (a small, decided task while the owner is busy): the worker writes a short plan, then
  builds at once.
- **T5 — the checks:**
  - complete local verification;
  - `test:api` is left to CI, since no API code changes;
  - an axe pass in headless Chrome at 320 and 390 on the three kinds of table;
  - green CI and `CLEAN` before the report.
