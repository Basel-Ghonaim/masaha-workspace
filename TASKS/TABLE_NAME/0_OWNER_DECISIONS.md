# TABLE_NAME — the two notes carried from #152 (2026-11-23)

The owner asked for another small production task, so the day has real activity on GitHub. The supervisor chose the
two notes already owed to the next PR (`0_CARRIED_FROM_152.md`). **Merging is the owner's word, always.**

- **N1 — scope:** only C1 and C2 of `0_CARRIED_FROM_152.md`. Anything else the worker notices is recorded, not fixed.
- **N2 — C1, the table's name said twice:**
  - **While a table fits,** its scrolling container is a plain box: no `group` role, no name, no tab stop. Only the
    `table` carries the name.
  - **While a table overflows,** the container stays a named group and a tab stop, because the keyboard must reach it
    and a focused element needs a name. The name is then heard on the group and on the table; this is accepted.
  - **The other `ScrollRegion` callers do not change.** The photos' list has no name of its own and relies on the
    group's, so the quiet behaviour is something `Table` asks for, not the new default.
- **N3 — C2:** remove `TableCaption` (its component and both exports). No page, showcase or document uses it.
- **N4 — the executor:** a fresh Claude Code worker, **Opus 5.5, effort medium**, in `C:\dev\masaha\app`, branch
  `fix/table-name-once`, PR expected **#153**. A short plan, then it builds without stopping.
- **N5 — the checks:** complete local verification; `test:api` left to CI (no API code); a short Chrome pass with
  `TASKS\TABLE_SCROLL\scripts\axe.mjs`; green CI and `CLEAN` before the report.
