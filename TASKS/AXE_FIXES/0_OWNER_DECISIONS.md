# AXE_FIXES — the owner's decisions (2026-11-18)

The owner paused AUTH and asked for a small task drawn from the open findings. Of the six open (23, 65, 152 — measured
on the deployment, the owner's accounts first; 215 — the prototype, paused; 221 — the README's shots, better after the
design work settles; 224), he chose **finding 224** on the supervisor's recommendation, every point below as
recommended ("نعم، 224 كما توصي"), except the executor (X5), which he set himself.

Finding 224 (checked in the code on `main` `05822b5e`, all three still there): axe-core in Chrome reports
`aria-tooltip-name` on the directory map's tooltip beside a selected mark (`LeafletMarkerMap.tsx`), and
`scrollable-region-focusable` at 390 px on the phone's row of thumbnails in the space profile's «الصور»
(`PhotosView.tsx`) and on «ساعات الذروة»'s card in Finance › Occupancy (`OccupancyTab.tsx`).

- **X1 — scope:** finding 224 alone, its three places, one PR. Web only: no API, no schema, no dependency.
- **X2 — the scrolling strips: one small piece in the design system** (not attributes in each place): a region that
  scrolls sideways, reached by the keyboard, named, showing the layer's one focus style; both places use it. *Why:*
  the rule ("a region that scrolls sideways is reached by the keyboard") is the design system's, not the photos' or
  finance's (judge by the capability that owns the rule), and the next such place gets it ready. The supervisor's
  details, open to the worker's *Proposed alternatives*: it is a tab stop **only while its content overflows** (a tab
  stop with nothing to scroll is noise); its role is `group`, not `region` (Occupancy's card is already a region of
  the same name, and two nested regions of one name fail axe's `landmark-unique`).
- **X3 — the map's tooltip: hidden from assistive technology** (not given a name). *Why:* the mark is a button already
  named by the space and its state; a named tooltip would have its name read twice. Leaflet also points the mark's
  `aria-describedby` at the tooltip — that goes too.
- **X4 — the proof:** component tests of what can be seen in jsdom (the names, the tab stop, axe), each broken once and
  seen failing; jsdom has no layout, so axe there cannot see a scrolling region — **axe-core in a real Chrome** on the
  three places, both themes, decides the finding (its *Resolves when*). The worker runs it before marking 224
  Resolved; **the supervisor runs it again in Chrome before asking the owner for the merge.**
- **X5 — the executor (the owner, mid-turn: "لا claude code هيشتغل عالمهمة"):** **a Claude Code worker**, not Copilot
  CLI (the supervisor's recommendation, overridden). Opus 5.5, effort high, in `C:\dev\masaha\app` (on `main`, clean,
  no other worker), branch `fix/axe-224`, expected **#150**. It follows the project's own skills (`start-work-item`,
  `write-plan`, `open-pr`, `final-report`): **plan → STOP → the owner's approval → execute.** Prompt:
  `1_PLAN_AND_EXEC_PROMPT.md` → `2_PLAN.md`, `4_REPORT.md`.
- **X6 — local checks:** the complete verification on the worker's machine **except `test:api`**, left to CI — the
  owner's allowance for this task (no API code changes). Heavy runs through the grant script.
- **X7 — review (the standing rule, §3 of the handoff):** small, no money, auth or schema → no separate Claude review;
  the supervisor verifies in the code, in the screens and with axe (X4). The owner may still ask for one.
- **Merge:** the owner's word only; it deploys to production.
