# Review — OWNER_SETUP PR 1 (`feat/owner-space-profile`, #96), one independent reviewer

You are the **independent reviewer** of worker A's OWNER_SETUP PR 1 in Basel-Ghonaim/masaha: the owner's
space profile on the web — the admin's space editor given a *place* (`admin` or `owner`), the shekel helpers
moved to `shared/lib`, the prices table from 1024 px (finding 67), the lookups' public source for owners, and
the owner's profile page. Claude Code executed it in another conversation; you start fresh and trust nothing
you have not seen in the code. Find the PR: `gh pr view 96 --json number,headRefOid,mergeStateStatus`. Write
the report to `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\6_REVIEW_PR1_CLAUDE_CODE.md`: first the verdict
and the five most important findings, then the rest. **Work alone — no subagents** (the owner's choice).

## Rules
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/96/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. Confirm `gh pr checks 96` is green first; if a lane is red or pending, say
  so and stop. At the end, check the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report or screenshots.** No praise, no tool
  attribution, no project skill.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\2_PLAN.md` — **the owner's approval note at its top
binds and wins**: three PRs, this one the plan's commits 1–5 only; the refusal lines corrected (an owner's
403 names no cause; a link ended is the managed boundary's 404); findings from 99. The prompt
`3_EXEC_PROMPT_PR1.md`; the report `4_REPORT_PR1.md`: judge every departure (98 files against ≈ 70; test 1's
break replaced; commit 3's *Why* reworded because foundation §9 no longer holds the cited rule — check where
the rule lives now; the demo accounts' passwords reset through the app during the real run) and every break.

Look hardest at:
- **The admin's editor unchanged** but for the 1024 px table: the threading of `place` through every hook,
  the scope table (keys, what a write marks out of date, the lookups' scope), the admin's refusal lines.
- **The owner's place:** every call on `/manage/spaces/:spaceId/…`, **no `/admin/*` request** from the
  owner's pages (lookups included); the cache under the space's scope; an owner's write marking `['me']`;
  `mayEdit`; the head line and public link; the prices as a link row; no owners' notice; no amenities-list
  link; reception refused the page; the refusal lines as the approval note says.
- **The public lookups:** a hidden area kept and never sent; a retired linked amenity kept in the value,
  never toggled off, counted by its plural line; finding 99 true.
- **Accessibility and the design system:** semantic tokens only, logical classes, names on links and
  buttons, the checklist and the leave guard.
- **Copy:** every new line in both catalogues, Arabic plurals through the plural forms.
- **The documents:** `spaces.md`, `lookups.md`, `frontend/architecture.md`, `overview.md`, `docs/README.md`,
  findings 67 (resolved) and 99 — true to the code, one home per fact, nothing claimed as built that is not
  (Packages & prices is PR 2's: its page must not be documented as built).
- Scope: `apps/web` and `docs` only. Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR's first commit (OWNER_SETUP PR 2); or a finding to record**; a short "Checked and fine" list; then stop.
