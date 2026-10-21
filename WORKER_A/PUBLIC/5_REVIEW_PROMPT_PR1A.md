# Review — PUBLIC PR 1a (`feat/directory-list`, #101), one independent reviewer

You are the **independent reviewer** of worker A's PUBLIC PR 1a in Basel-Ghonaim/masaha, the item's first: the
public Directory's list on the web (the space card, the search, the order, the pages, the URL state), the
site's skip link and focus on page change, the public areas offered by `lookups`, and two refactors that move
the list's pages and the name and clock rules from dashboard-only features to `shared/`. Claude Code executed
it in another conversation; you start fresh and trust nothing you have not seen in the code. Find the PR:
`gh pr view 101 --json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR1A_CLAUDE_CODE.md`: first the verdict and the five most
important findings, then the rest. **Work alone — no subagents.**

## Rules
- **This is a review, not a Work Item:** run no project skill (no `start-work-item`, no branch).
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/101/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. A planner may read in the same worktree: never switch or reset it. Confirm
  `gh pr checks 101` is green first; if a lane is red or pending, say so and stop. At the end, check the head
  has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report or screenshots.** Think like a visitor on a
  weak phone connection with a screen reader, and like someone pasting a hand-edited link. No praise, no tool
  attribution.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md` — **the owner's approval note at its top binds
and wins**: this PR is **PR 1a = the plan's PR 1 commits 1–5** (A13 taken), S1–S15 taken, A1–A12 not; design
issues as written; foundation §5's status roles corrected; finding 27 resolved only if the build's manifest
shows the chunks no longer import each other. The prompt `3_EXEC_PROMPT_PR1A.md`; the report
`4_REPORT_PR1A.md`: judge every departure — the split of commit 5 (near me's argument and header, `hasNear`,
the distance, the place-filter slot and tests 17, 31–43 and half of 14 moved to 1b: is anything left
half-wired, dead or untested on this head?); S6's `useMediaQuery` export left to 1b; the `h3` inside
`CardTitle` and the name's `lang`/`dir` span; **the page-past-last rule copied inline from `space-links`'
`usePageInRange`** (a duplicated rule — should it have moved to `shared/lists` with the pages?);
`useMainFocus` comparing paths for StrictMode; the four existing tests changed (SiteLayout, authPages,
changePasswordPage, routes) — not weakened; tests written after their code; finding 27 left open; 99 files
against ≈ 63 — and every break.

Look hardest at:
- **The URL state (S5, S15):** search, order and page restored from the address; a value the server would
  refuse falls back to its default and never reaches the request; a search with no letter to match kept off
  the request with its message; page past the last; Back and reload; a copied link.
- **The list's states:** loading, empty, no match with «مسح الفلاتر», failure and offline (`useRefusalView`),
  the cards kept while the next page loads (S13), focus to the results heading on a new page, the live
  region; the card one link, its cover or mark, the status **by word** (never colour alone), «موثّقة», today's
  hours on Gaza's calendar, **no price**.
- **The shell:** «تخطَّ إلى المحتوى» first, `<main id="main">`, focus on navigation but not on first load
  nor when only the search or hash changes.
- **The refactors:** `shared/lists`, `shared/lib`'s names and time unchanged in behaviour; every importer
  moved; nothing in `shared/` importing a feature; the site's first download free of dashboard code (read
  what `check:build` checks against what the site now imports).
- **`lookups`' slots (S7):** `AreaFilter` and `AreaName` offered so no feature imports another; the space
  editor's `AreaName` source unchanged in behaviour.
- **Design system, copy, accessibility:** semantic tokens, logical classes, no colour or CSS outside the
  layer; every string in both catalogues, Arabic plurals' forms; names, landmarks, headings' order; widths
  390 / 768 / 1440.
- **The documents:** `docs/features/directory.md`, `lookups.md`, `frontend/architecture.md`, foundation §5,
  the findings index (130), `docs/README.md` — true to the code, one home per fact, only what this PR built.
- Scope: `apps/web` and `docs` only (no API change). Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR (PUBLIC PR 1b's first commit, through `0_CARRIED_FROM_101.md`); or a finding to record**; a short
"Checked and fine" list; then stop.
