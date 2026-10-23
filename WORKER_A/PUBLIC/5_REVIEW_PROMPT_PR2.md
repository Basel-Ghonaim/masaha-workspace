# Review — PUBLIC PR 2 (`feat/directory-map`, #105), one independent reviewer

You are the **independent reviewer** of worker A's PUBLIC PR 2 in Basel-Ghonaim/masaha: the public
Directory's map (`shared/map`'s `MarkerMap`, the pins by state with their legend, «قائمة | خريطة», a chosen
space's card and sheet, «مركّز على موقعي», and near me's map fallback «حدّد موقعي على الخريطة»), opened by
commits carried from #103's review. Claude Code built it in another conversation; OpenCode squashed its
history (six carried fix commits into one, two findings commits into one; the same tree), pushed and opened
the PR. You start fresh and trust nothing you have not seen in the code. Find the PR: `gh pr view 105 --json
number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR2_CLAUDE_CODE.md`: first the verdict and the five most
important findings, then the rest. **Work alone — no subagents.**

## Rules
- **This is a review, not a Work Item:** run no project skill (no `start-work-item`, no branch).
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/105/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. A planner may read in the same worktree: never switch or reset it. Confirm
  `gh pr checks 105` is green first; if a lane is red or pending, say so and stop.
- **Known and being fixed apart from you — do not report them:** the documents still hold `#PRNUM` (the
  number's replacement failed; it becomes `#105` in their commits), the PR has no labels, and the
  description's *Carried from #103* list misnumbers items 9–12. The head may therefore move during your
  review: at the end, if it moved, check `git diff <the head you reviewed> <the new head>` changes only
  `#PRNUM` → `#105` in documents, and say so; anything else → name it.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report or screenshots.** Think like someone who must
  not be located, like a visitor on a weak phone with a screen reader and a keyboard only, and like someone
  pasting a hand-edited link. No praise, no tool attribution.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md` — **the owner's approval note at its top binds
and wins**: this PR is the plan's **PR 2** (three commits: the map component, the directory's map, picking a
centre; tests 46–60; design issues 19–22 as written; its S-decisions). The carried items
`0_CARRIED_FROM_103.md` (1–12, the owner's decisions) with #103's review `6_REVIEW_PR1B_CLAUDE_CODE.md`. The
prompt `3_EXEC_PROMPT_PR2.md` (its §3: a test seen red before its code is its own break; component tests of
the touched folders locally, the full lanes CI's). The report `4_REPORT_PR2.md`: judge every departure —
shared `MapLayers` and `mapBox`, no `usePickCentre` file; `focusSelected`, `focusMap` and the nullable `under`
slot (the picking card under the map below 768 px, a fix folded after the real run); `sheetOnly` on
`useFiltersPanel`; `useFailureView` shared by list and map; the map's empty state; `clearFilters` keeping the
view; a hand-placed point clamped to the Strip's box; a pin's accessible name not isolated; test 46 after its
code; the two extra tests — and every break. The real run's last three cases were redone by the supervisor
(`scripts\run2b.mjs`, the report's *§3 redone by the supervisor*). The executor's own observation (dark theme:
the hollow and dashed marks filled with `card` on the always-light tiles) is yours to judge.

Look hardest at:
- **Privacy of the position:** the device's or the hand-placed point only in memory, rounded before it leaves
  the browser, only in the `Masaha-Near` header and only on `sort=distance`; never in a URL (the map's
  `bounds` aside), storage or a log; the map's user point and «مركّز على موقعي» reading nothing new; «رجوع»
  restoring the previous location exactly; the privacy line only while the position is used.
- **The map's weight and loading:** Leaflet, its stylesheet and the marks' CSS only after «خريطة»
  (`check:build`'s rule); the 1,000-pin bound and the re-ask within the viewport; no request storm on pan.
- **Keyboard and screen reader:** pins focusable with names, Enter selects, the card or the non-modal sheet
  (focus kept on the pin, Escape and «إغلاق» back to it), arrows pan with the sheet open, the crosshair's
  keys line, «ثبّت الموقع هنا», the legend's words, live regions not nested.
- **The carried fixes:** each of items 1–12 done as decided, each with its test; the squashed commit's body
  true to what it holds.
- **Design system, copy, accessibility:** semantic tokens, logical classes, `leaflet.css` inside the layer
  only; every string in both catalogues; RTL on the map's controls and card.
- **The documents:** `directory.md`, `frontend/architecture.md`, foundation, findings 46, 130 and 133, the
  index — true to the code, one home per fact, only what this PR built.
- Scope: `apps/web` and `docs` only (no API change). Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR (PUBLIC PR 3's first commit, through `0_CARRIED_FROM_105.md`); or a finding to record**; a short "Checked
and fine" list; then stop.
