# Review — PUBLIC PR 1b (`feat/directory-filters`, #103), one independent reviewer

You are the **independent reviewer** of worker A's PUBLIC PR 1b in Basel-Ghonaim/masaha: the public
Directory's filters (place, price and state, «أخرى», the sheet below 1024 px and the sidebar above it) and
«الأقرب إليّ» (near me, its state line and its privacy line), opened by commits carried from #101's review.
Claude Code executed it in another conversation; you start fresh and trust nothing you have not seen in the
code. Find the PR: `gh pr view 103 --json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR1B_CLAUDE_CODE.md`: first the verdict and the five most
important findings, then the rest. **Work alone — no subagents.**

## Rules
- **This is a review, not a Work Item:** run no project skill (no `start-work-item`, no branch).
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/103/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. A planner may read in the same worktree: never switch or reset it. Confirm
  `gh pr checks 103` is green first; if a lane is red or pending, say so and stop. At the end, check the head
  has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report or screenshots.** Think like someone who must
  not be located (the device's position), like a visitor on a weak phone with a screen reader, and like
  someone pasting a hand-edited link. No praise, no tool attribution.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md` — **the owner's approval note at its top binds
and wins**: this PR is **PR 1b = the plan's PR 1 commits 6–7** (A13 taken), with what PR 1a's split moved
here (the `Masaha-Near` argument and header, `hasNear`, `distanceText`, the card's distance, the
`placeFilter` slot, tests 17, 31–43 and the privacy half of 14) and S6's `useMediaQuery` export; S1–S15; the
design issues as written. The carried items `0_CARRIED_FROM_101.md` (1–11, the owner's decisions) with #101's
review `6_REVIEW_PR1A_CLAUDE_CODE.md`. The prompt `3_EXEC_PROMPT_PR1B.md` — **its §3 is the owner's new rule**
(a test seen red before its code is its own break; component tests of the touched folders locally, the full
lanes CI's; the real run's widths): judge whether each guard the red step did not prove got its own break.
The report `4_REPORT_PR1B.md`: judge every departure — DEMO_SEED waived by the owner; tests 32–35 and 41–43
written after their code; `useFiltersPanel` returning the whole view; «₪» as a catalogue word; a period kept
in the hook's state before any bound, one 400 ms pause for both bounds; **no `distances.*` words** (is the
plan's line wrong, or is something now unsaid?); «الأقرب إليّ» returning to page 1; item 11's zero form; the
shared `src/test/fakeGeolocation.ts`; the button's alignment fix folded into commit 6; the areas' comma as
`%2C` in the address — and every break.

Look hardest at:
- **Privacy of the position:** the device's location only in memory, rounded (three decimals at most) before
  it leaves the browser, sent only in the `Masaha-Near` header and only on `sort=distance` requests, never in a
  URL, a query key that is persisted, a log or storage; cleared by «مسح موقعي»; the privacy line shown only
  when the position is used (`PRIVACY_LINE`, the corrected wording); denied, imprecise and outside the Strip
  each with its one state line.
- **The carried fixes:** each of items 1–11 done as decided (item 4 a check, item 9 finding 132), each with
  its test; item 1's push-versus-replace rule now also under the filters' writes and near me.
- **The filters:** the URL state of every filter (shareable, restorable, a refused value falling back to its
  default and never reaching the request; the inverted budget's line, no 422); the place filter through
  `lookups`' `AreaFilter` slot (no feature imports another); the sheet below 1024 px (its count, its button,
  focus in and back) and the sidebar from 1024; «مسح الفلاتر».
- **Design system, copy, accessibility:** semantic tokens, logical classes, nothing outside the layer;
  `useMediaQuery` exported as S6 says; every string in both catalogues, Arabic plurals' forms; names, the
  sheet as a dialog, `aria-expanded`, live regions.
- **The documents:** `directory.md`, `lookups.md`, `frontend/architecture.md`, foundation (§3, S6), findings
  130 (its new line) and 132, the index, `overview.md`, `docs/README.md` — true to the code, one home per fact,
  only what this PR built.
- Scope: `apps/web` and `docs` only (no API change). Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR (PUBLIC PR 2's first commit, through `0_CARRIED_FROM_103.md`); or a finding to record**; a short "Checked
and fine" list; then stop.
