# Review — OWNER_SETUP PR 2 (`feat/owner-packages`, #98), one independent reviewer

You are the **independent reviewer** of worker A's OWNER_SETUP PR 2 in Basel-Ghonaim/masaha: the owner's
Packages & prices page on the web — the published prices on their own page («الأسعار المعلنة») and the new
`packages` feature (the private packages, the switch, the package sheet, a paused package's held shift,
finding 81) — opened by three commits carried from #96's review. Claude Code executed it in another
conversation; you start fresh and trust nothing you have not seen in the code. Find the PR: `gh pr view 98
--json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\6_REVIEW_PR2_CLAUDE_CODE.md`: first the verdict and the five most
important findings, then the rest. **Work alone — no subagents.**

## Rules
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/98/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. A planner may be reading in the same worktree: do not switch or reset it.
  Confirm `gh pr checks 98` is green first; if a lane is red or pending, say so and stop. At the end, check
  the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report or screenshots.** No praise, no tool
  attribution, no project skill.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\2_PLAN.md` — **the owner's approval note at its top
binds and wins**: this PR is the plan's commits 6–7 (tests 13, 15–20, test 14's Packages case); the refusal
lines as the note corrects them (a package's 404 names both causes; a 403 none); findings from 101. The
carried items `0_CARRIED_FROM_96.md` (items 1–9) and #96's review `6_REVIEW_PR1_CLAUDE_CODE.md`. The prompt
`3_EXEC_PROMPT_PR2.md`; the report `4_REPORT_PR2.md`: judge every departure (the edit checked with the create
schema; `useRowWrite`; one save hook; the field named `priceAgorot`; the empty-limit line; `too_short` added;
`useSpaceShifts` moved; four extra files; no icon; finding 101; finding 87's local miss under the owner's
rule) and every break.

Look hardest at:
- **The carried fixes:** the retired-amenity count from `value ∩ linked`, both places (owner's and admin's);
  the owner's 404 refreshing `['me']`; architecture §7's two new invalidations; the documents.
- **The prices page:** the same section as the profile's, its own leave guard, its date and confirm, the
  no-shift note's link to `#hours`; the save toast that names «الأسعار» on a card titled «الأسعار المعلنة»
  (the executor's own note — judge it).
- **Packages:** every call on `/manage/spaces/:spaceId/packages`, no `/admin/*`; the sheet's browser checks
  against the contract (a limit on and empty, digits Arabic-Indic, the amount in shekels to agorot, the
  billing's labelled amount, the audience, the shift chips and «بدون وردية»); the edit sending the terms
  whole (S11) — and whether checking it with the create schema can refuse an edit the server would accept;
  a 409 on the name, a 422 on the shift refreshing the space's scope; the switch held while pending, the
  list replaced from the answer; the held shift and «إزالة الوردية» only on a paused package with a shift.
- **Money and words:** amounts through `shared/lib/money`; every counted noun through the plural forms
  (all six Arabic forms); both catalogues; the summary line.
- **Accessibility and the design system:** names on the switch and edit («{name}: متاحة», «تعديل {name}»),
  `aria-live` on the summary, semantic tokens, logical classes; finding 101 true to `Sheet`.
- **The documents:** `packages.md`, `spaces.md`, `architecture.md`, `overview.md`, `docs/README.md`,
  findings 81 (resolved) and 101 — true to the code, nothing claimed as built that is not (staff and
  settings are PR 3's).
- Scope: `apps/web` and `docs` only. Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR's first commit (OWNER_SETUP PR 3); or a finding to record**; a short "Checked and fine" list; then stop.
