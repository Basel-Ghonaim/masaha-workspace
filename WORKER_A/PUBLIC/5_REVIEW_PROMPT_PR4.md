# Review — PUBLIC PR 4 (`feat/home-about`, #111), one independent reviewer

You are the **independent reviewer** of worker A's PUBLIC PR 4 in Basel-Ghonaim/masaha: the site's Home page,
About page and error states (the plan's PR 4 commits 1–5: the routing's retry and offline state with its new
`WifiOffIcon`; the public areas for Home; Home's spaces and counts; the Home page; the About page and the
footer), opened by eight commits carried from #108 (a failed refresh keeping the last status; the viewer's
total; one tile on a phone; test 77 driven by page events; the bar's room only with a bar; the place map's
props test; focus back to the tile after the viewer; finding 131's sentence). Claude Code built it in another
conversation; you start fresh and trust nothing you have not seen in the code. Find the PR: `gh pr view 111
--json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR4_CLAUDE_CODE.md`: first the verdict and the five most
important findings, then the rest. **Work alone — no subagents.**

## Rules
- **This is a review, not a Work Item:** run no project skill (no `start-work-item`, no branch).
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/111/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. Never switch or reset that worktree. Confirm `gh pr checks 111` is green first;
  if a lane is red or pending, say so and stop. At the end, check the head has not moved.
- **Read the plan by its parts:** in `2_PLAN.md`, the approval note at its top (lines 1–40), §2 for PR 4, §4,
  §5 as it names PR 4, §7 *PR 4*, §8 *PR 4* (design issues 36–44), §9's opening paragraph and *PR 4 ·
  Commits 1–5*, §10 *PR 4* tests 80–86, §11, §13's PR 4 parts. For the carried items: `0_CARRIED_FROM_108.md`
  whole and `6_REVIEW_PR3B_CODEX.md` (#108's review) for their files and lines.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report or screenshots.** Think like a first-time
  visitor on a weak phone with a screen reader and a keyboard only, like a visitor who loses the connection
  mid-page, like an owner arriving to learn how to list a space, and like someone pasting a hand-edited link.
  No praise, no tool attribution.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md` — **the owner's approval note at its top binds and
wins** — PR 4's commits 1–5 (tests 80–86; design issues 36–44 as written, their Arabic word for word). The
carried items `0_CARRIED_FROM_108.md` (1–8). The prompt `3_EXEC_PROMPT_PR4.md`. The report `4_REPORT_PR4.md`:
judge **every departure** — all three site error boundaries on `SiteRouteError` (the plan said two);
`useHomeSpaces` taking `chooseArea` and `openMap`; the owners' anchor and path in commit 4, not 5;
`statusViewOf` exported beside `LiveStatusBadge`; two tests outside the plan's list changed for Home's heading;
the carried history line in commit 3's docs; the offline case's order; the touch scroll by `dispatchTouchEvent`;
a ninth carried commit (the focus fix). Also: **test 77's first rewrite left its breaks green** — check the
final test would really turn red under both breaks; and the two site tests the report says time out at 3 s on
clean `main` (finding 87's family?) — say whether that is a real slowness or a test defect, plausible if you
cannot tell from the code.

Look hardest at:
- **The carried fixes:** each of 1–8 done as decided, each with its test and a break that would fail it; the
  last status kept on a failed poll but a first-ever failure still said; the viewer's position across more than
  five photos and its wrap; the phone's single tile with «عرض كل الصور (n)» still on it; test 77 dispatching the
  browser's events, not calling `focusManager`; the bar's room tied to the bar actually drawn, given back on
  leaving the page; focus back to the tile that opened the viewer.
- **Home:** the hero's search encoding `q`; «متاحة الآن» six at most; near me sending the point **only in the
  `Masaha-Near` header**, never in a URL or log, by the Directory's privacy rules; «المساحات الأقرب إليك» and
  «عرض الكل» keeping the order; the areas' cards only for areas with spaces, «كل المناطق» with the total, one
  retry for both reads; the owners' card's words (the status shows automatically, design issue 36); the empty
  state offering browsing all.
- **About:** `#contact` before `#owners`; each section drawing only the configured channels and its text alone
  with none (design issue 44); no hard-coded contact; no university line; the legend's words (design issue 41).
- **Errors and offline:** a retry while still offline says «ما زال الاتصال مفقودًا.» and does not reload; back
  online works; `WifiOffIcon` from the layer, not mirrored; the general error's line (design issue 39) in both
  shells; a route error inside the site keeps the site's shell.
- **Layout and accessibility:** one `h1` per page; headings in order; landmarks; anchors reachable and focused;
  RTL and logical classes; the layouts at 390, 768, 1440.
- **Weight:** Home and About add nothing heavy to the site's first download (no Leaflet, no TanStack Table).
- **Design system and copy:** semantic tokens, nothing outside the layer; every string in both catalogues; the
  new icon in the layer, the showcase and foundation §12.
- **The documents:** `directory.md`, `lookups.md`, `architecture.md`, foundation, `overview.md`,
  `docs/README.md`, finding 131 and the index — true to the code, one home per fact, only what this PR built,
  `#111` where the number goes.
- Scope: `apps/web` and `docs` only (no API, no `packages/shared` change). Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the public
site's fix PR that follows the owner's in-person review (through `0_CARRIED_FROM_111.md`); or a finding to
record**; a short "Checked and fine" list; then stop.
