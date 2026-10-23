# Review — PUBLIC PR 3b (`feat/space-photos-status`, #108), second reviewer (Claude Code)

You are the **independent reviewer** of a pull request in the Masaha repository (GitHub
`Basel-Ghonaim/masaha`): worker A's PUBLIC PR 3b — the public Space details page gains its **photos** (a
gallery and a viewer) and its **live status read again every 60 s while the page is visible**, opened by
commits carried from #107's review. GitHub Copilot built it; it ran out of quota while fixing CI, and the
owner finished it (a test fix and a formatting commit folded into their commits). **Trust nothing you have not
seen in the code.** This file is self-contained.

## A first review exists

Codex reviewed this head first: `C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR3B_CODEX.md` (verdict: not
mergeable). **Start there:** confirm or refute each of its findings in the code (say which, with the line);
then look for what it missed, hardest where it was thin. Your verdict is your own. Work alone, no subagents.

## Rules

- **Read only.** Work from `C:\dev\masaha\app-design`. Use git commit objects only: `git fetch origin` and `git
  fetch origin pull/108/head`; base = `origin/main`; `git diff origin/main...FETCH_HEAD`, `git show <commit>`,
  `git show <sha>:<path>`. **No** edits to the repository, no checkout or switch (another worker may hold a
  branch in that worktree), no installs, no npm or test runs, no servers, no browser, no comments on GitHub.
  The only file you write is the report below.
- First: `gh pr checks 108` — if any check is red or pending, say so and stop. At the end, `gh pr view 108
  --json headRefOid` again: say whether the head moved.
- **Known, do not report:** the PR description names commit shas from before the history was rewritten (the
  owner corrects the description).
- Report **concrete problems only**, each verified in the code: the file and line, the failing scenario, the
  severity (**blocker / should-fix / nit**), and the fix. Mark "plausible" when unsure, with why. **Say what you
  saw in the code and what you only read in the executor's report or screenshots.** No praise. No tool
  attribution anywhere.
- Think like: a visitor on a weak phone with a screen reader and a keyboard only; a visitor who leaves the tab
  open in the background for an hour; someone opening a space with 0, 1 or 30 photos.

## What to read

1. The project's rules: `git show origin/main:CLAUDE.md` (copy in both languages, the design system only,
   semantic tokens, logical classes, claim only what is true).
2. The approved plan `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md` — **only:** lines 1–40 (the owner's
   approval note; it binds); 625–655 (§8, PR 3's design issues — 32 is this PR's); **1264–1297 (§9, PR 3
   commits 5 and 6 — what this PR must build)**; 1468–1490 (§10, tests **76, 77, 78** and the break each must
   catch).
3. The carried items `C:\dev\masaha\workspace\WORKER_A\PUBLIC\0_CARRIED_FROM_107.md` (items 1–10, the owner's
   decisions) and, for each item's scenario, the findings it cites in `6_REVIEW_PR3A_CLAUDE_CODE.md`.
4. The executor's prompt `3_EXEC_PROMPT_PR3B_COPILOT.md` and report `4_REPORT_PR3B.md` (same folder): judge
   every departure, every test said to be red first, every break, and whatever the report leaves out (it may be
   incomplete: Copilot stopped mid-way).

## Look hardest at

- **The carried items:** each of 1–10 done as decided, each code fix with its test: the contact bar never
  covering the footer; the place map with `dragging` and `touchZoom` off (zoom buttons kept) and
  `architecture.md` §6 saying so; test 75's wiring through the page (the `none` line, then a `mailto:` link);
  the phone's live line with the name's language mark and **outside** the busy section; a hidden `h1` while
  loading or failed; Escape's comment; finding 131's sentence; item 10 (prices naming an unknown shift — the
  report must say whether the API allows it, with a file and line).
- **The gallery (commit 5, design issue 32):** no gallery and the header's caption with no photo; the grid's
  layout by count (1, 2, 3–5, more); «عرض كل الصور (n)» whenever there is more than one photo, at every width;
  each image's `alt` and `loading` (the first eager); the viewer: a dialog titled with the name, its position
  `dir="ltr"`, «السابقة» / «التالية» moving round, Escape and «إغلاق» returning the focus; no layout shift.
- **The live status (commit 6, decision 3):** `refetchInterval: 60_000`, **no** reading in the background
  (`refetchIntervalInBackground` not true), `refetchOnWindowFocus: 'always'`; `StatusPanel`'s states (verified
  with a status, verified without — `unset`, unverified, first read loading, a failed first read, a failed read
  after one keeping the last state); the request scoped to the slug and encoded; the lists never polled.
- **Test 77** really drives visibility and focus (fake timers; `document.visibilityState`; the window's
  `focus`), and its break would turn it red; **the test fixed after CI** (`useSpacePage.component.test.tsx`,
  requests told apart by URL) still proves what its title says.
- **Design system and copy:** semantic tokens, logical classes, nothing outside the layer; every new string in
  both catalogues (`directory.page.gallery`, `directory.page.status`); RTL in the viewer and the panel.
- **The documents:** `directory.md` (*Behaviour*, *Web decisions*, *Web history*), `architecture.md` §6 and §7
  (*Polling*), findings 131 and the index — true to the code, `#108` where the number goes, no `#PRNUM` left.
- **Scope:** `apps/web` and `docs` only (no API change). Commit subjects ≤ 50 characters, each with a body, no
  `fixup!`, `style:` or `wip` commit left. The plan expected about 35 files; this PR has 22 — check nothing of
  commits 5–6 or of the carried items is missing.

## Your output

Write one file: `C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR3B_CLAUDE_CODE.md`. It holds:

1. The head you reviewed, CI's state, and whether the head moved.
2. **A one-line verdict:** mergeable / mergeable after a fix round / not mergeable.
3. **The five most important findings**, most severe first, then the rest. Each with **where its fix belongs**
   under the owner's rule: **a serious or large fix → a fix round on this PR; a small one → worker A's next PR
   (PUBLIC PR 4) first commit, through `0_CARRIED_FROM_108.md`; or a finding to record.**
4. The executor's departures, each judged; and anything the plan or the carried file asked for that is missing.
5. A short "Checked and fine" list.

Then stop.
