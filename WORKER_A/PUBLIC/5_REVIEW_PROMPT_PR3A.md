# Review — PUBLIC PR 3a (`feat/space-page`, #107), one independent reviewer

You are the **independent reviewer** of worker A's PUBLIC PR 3a in Basel-Ghonaim/masaha: the public Space
details page at `/spaces/:slug` (the plan's PR 3 commits 1–4: the shared carrier and date rules; the platform's
public contact; one place on a map; the space's page — one order at every width, prices per audience and by
shift, hours with today, amenities, the location, the contacts, the unverified notice and its dialog, the bar
below 768 px, the way back to the Directory), opened by eight commits carried from #105's review (the map's
pick, tab order, rounding, near-me line, loading, ceiling, documents and findings 134–136). The owner split the
plan's PR 3: the photos and the live status's refresh are PR 3b, not this one. Claude Code built it in another
conversation; you start fresh and trust nothing you have not seen in the code. Find the PR: `gh pr view 107
--json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR3A_CLAUDE_CODE.md`: first the verdict and the five most
important findings, then the rest. **Work alone — no subagents.**

## Rules
- **This is a review, not a Work Item:** run no project skill (no `start-work-item`, no branch).
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/107/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. A planner or another reviewer may read in the same worktree: never switch or
  reset it. Confirm `gh pr checks 107` is green first; if a lane is red or pending, say so and stop. At the
  end, check the head has not moved.
- **Read the plan by its parts:** in `2_PLAN.md`, the approval note at its top, §2 for PR 3, §4, §5 as it names
  PR 3, §7 *PR 3*, §8 *PR 3*, §9 *PR 3 · Commits 1–4*, §10 tests 61–75 and 79, §11, §13's PR 3 parts.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report or screenshots.** Think like a visitor on a weak
  phone with a screen reader and a keyboard only, like an owner whose space hides its prices, and like someone
  pasting a hand-edited link. No praise, no tool attribution.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md` — **the owner's approval note at its top binds and
wins** — PR 3's commits 1–4 only (tests 61–75 and 79; design issues of §8 *PR 3* as written). The carried items
`0_CARRIED_FROM_105.md` (1–14, the owner's decisions of 2026-10-22, the map line's words included) with #105's
review `6_REVIEW_PR2_CLAUDE_CODE.md`. The prompt `3_EXEC_PROMPT_PR3A.md` (the owner accepted ≈ 100 files as one
PR). The report `4_REPORT_PR3A.md`: judge every departure — the overlay stacked with `isolate` and `z-sticky`;
**the phone line's words, proposed by the executor, for you to judge** («{name}: التفاصيل في أسفل الصفحة» /
"{name}: details at the bottom of the page"); «1,000» formatted in Arabic; `.env.example`'s placeholder email;
`PlaceMapProps` and the shared fixture `src/test/publicSpace.ts`; price labels carrying their language; no
`spacePath` (`publicSpacePath` kept); the way back keeping the Directory's address on every change; **tests
70–75 and 79 written after their code** — check each planned break would really turn its test red.

Look hardest at:
- **The carried fixes:** each of items 1–14 done as decided, each with its test: the pick ended on the map's
  unmount (StrictMode's double mount included); the overlay before the panes in the tab order; nothing sent
  while picking and the box rounded outward; the map's own near-me line with no privacy sentence and no stop;
  `aria-busy` and the loading line; the card under the map below `lg`; Escape on the card.
- **What the page claims:** hidden prices said with their date and why; prices never saved said so; the
  unverified notice dating the profile; stale groups marked; a 404 «لم نجد هذه المساحة» distinct from a failure;
  nothing shown that the API did not send (`PublicSpace`; no announcements, no closure notice — finding 131).
- **Links and contacts:** `wa.me` digits only, `tel:`, `mailto:`, the stored address; a phone's carrier in its
  label; the platform's contact from `VITE_CONTACT_EMAIL` / `VITE_CONTACT_WHATSAPP`, an invalid or empty one
  left out; «الاتجاهات» to the right place; no secret or private data in the bundle.
- **Layout and accessibility:** one `h1`; the sections in U8's order, each named by its heading; the aside from
  1024 px and the status card first and contacts last below it; the bar only below 768 px; the breadcrumb from
  768 px keeping the last search; the place's pin a picture, not a button; `lang`/`dir` on names in the other
  language; RTL throughout.
- **Weight:** the place map lazy (Leaflet out of the first download; the report's 999,477 bytes); the moved
  `carrierOf` and `updatedAgo` with no behaviour change for `spaces`.
- **Design system and copy:** semantic tokens, logical classes, nothing outside the layer; every string in both
  catalogues; the Sheet's non-modal clause in the layer's comment and foundation.
- **The documents:** `directory.md`, `spaces.md`, `architecture.md`, foundation, `setup.md`, `overview.md`,
  `docs/README.md`, findings 40, 131 and 134–136, the index — true to the code, one home per fact, only what this
  PR built, `#107` where the number goes.
- Scope: `apps/web` and `docs` only (no API change). Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR (PUBLIC PR 3b's first commit, through `0_CARRIED_FROM_107.md`); or a finding to record**; a short "Checked
and fine" list; then stop.
