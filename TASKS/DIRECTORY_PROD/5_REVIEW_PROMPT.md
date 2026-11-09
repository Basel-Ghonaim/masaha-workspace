# Review of #<n> — the directory's filters in web + API (one reviewer, the whole branch)

You are a **read-only reviewer** of Masaha's PR **#<n>** (`feat/directory-filters`; the number is given in the launch line — expected #139, since #138 went to another task), launched headless by the main
supervisor once CI was green and GitHub said `CLEAN`. **The head you review is given in the launch line** — call it
`<HEAD>` below and pin every read to it. **Work alone — no subagents.** This is a review, not a Work Item: run no
project skill, no branch. Tool and model: Claude Code, Opus 5.5.

**What #<n> is:** the production step of refactor round 1 — the directory's filters as the prototype (#137) shows
them, built in `packages/shared`, the API and the web, with their documents: the price by subscription
(`SegmentedControl`, a new design-system component), its range, its order and the card's price; «مفتوحة الآن»
(`openNow`, by the hours on Gaza's clock, replacing `availableNow`), «مفتوحة مساءً», the by-hours state of unverified
spaces (`hoursStatus`), hours optional, the panel's new order, 18 a page; plus finding 214 (a flaky Home test) and
#136's two nits. About 90 files, five planned commits.

**The owner's bar, in his words (2026-11-08):** the tests must work well and point the right way — never bent to
pass; **the filters' tests must be very strong, with no gap.** Judge the tests against that bar first.

## Rules

- **Read only, commit objects only.** The supervisor fetched `origin` and `pull/<n>/head` before launching you; fetch
  once only if `git cat-file -t <HEAD>` fails. Reads: `git show <HEAD>:<path>`, `git diff origin/main...<HEAD>`,
  `git log origin/main..<HEAD>`, `git show <sha>`, `git grep <pattern> <HEAD>`. **Never** edit, checkout, switch,
  reset, stash or commit; no installs, no npm, no test runs, no servers, no database, no comments or reviews on GitHub.
  Other workers use this repository at the same time — your cwd's working tree is not the PR; ignore it. A `git`
  command failing on a `.lock` file: wait 30 s, retry once. The only file you write is your report.
- First `gh pr checks <n>` — red or pending: say so at the top and stop. At the end, `gh pr view <n> --json
  headRefOid`: say whether the head moved from `<HEAD>`.
- Report **verified defects only**: file and line at `<HEAD>`, the scenario (inputs or user action → wrong result),
  severity — **blocker** (a filter that keeps or drops the wrong spaces; a hidden price filtered, shown or ordered; a
  filter applied after the page is cut; the SQL open-now rule and the TypeScript `hoursStatus` able to disagree; a
  by-hours badge in the live status's colours; a page that breaks; **a test that cannot fail**, or one bent to pass;
  production code only a test uses) · **should-fix** (a real defect a user can meet; a missing or weaker planned test
  `T…`; an accessibility gap in `SegmentedControl`; hardcoded user-facing text; a colour/class outside the design
  system; a false document; a departure from the owner's decisions or the approved ODs without need) · **nit** — and
  the fix (`a fix round on #<n>, folded into <commit>` or `a finding`). Mark "Plausible" when unsure, with why. Say
  what you **saw in the code** and what you only **read in a report**. A point whose own conclusion is "no change
  needed" is not a finding. No praise.
- **Check the library's behaviour before calling a bug** (Radix radio group 1.4.7, TanStack Query v5, react-router,
  zod, Prisma 7, Express 5, PostgreSQL date/time semantics).
- Do not report what lint, typecheck, Prettier, `check:*` or CI enforce and passed.
- New findings, if any: numbers **216–219** (check `docs/architecture/findings/` at `<HEAD>` first; 214–215 are this
  task's).

## Read, in this order

1. `git show <HEAD>:CLAUDE.md`, then at `<HEAD>`: `docs/development/workflow.md` (Definition of Done),
   `docs/development/testing.md`, `docs/development/engineering-principles.md`.
2. `C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\0_OWNER_DECISIONS.md` — items 1–15 and the approved ODs (OD1 a,
   OD2 a, OD3 a, OD4 a, OD5 a, OD6 a, OD7 b). These bind.
3. `C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\2_PLAN.md` — whole; above all §4.2, §5, §7, §10 (the test matrix),
   §11, §12, §14.
4. `C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\4_REPORT.md` — its deviations and executor checks; **judge every
   deviation**: sound / acceptable / wrong, with why.
5. The diff, commit by commit (`git log --reverse origin/main..<HEAD>`), then the files at `<HEAD>` where a later
   commit changed them.

## Look hardest at

- **The test matrix (§10), line by line.** For each `T1–T66`, `T80`, `T81`: present / missing / weaker. Would it fail
  if its named break were made? Are its expectations written by hand (not computed from the code under test)? Fixed
  clocks in the API lane (`createTestApp({ clock })`), never the real clock? **T31** (SQL ↔ TypeScript binding at four
  clocks) and **T33** (leave one out: each filter excludes exactly its space, none OR-ed) above all; T16 (price order,
  ties by id ascending in both directions, pages without repeat or gap); T20–T27 (open/close minutes, closed day, no
  hours, closures' bounds, Gaza day boundary, DST, 24:00); T14 (hidden prices everywhere).
- **The SQL:** the lateral price (`audience` = general only, hidden prices out, lowest within the bounds, the same
  value filters, orders and shows — OD4 a); the open-now predicate on Gaza's weekday and minute (`opens ≤ m <
  closes`), closures in force (`startsAt ≤ now < endsAt`, deleted ones out, `OUTAGE` not a closure), OD2 a (a verified
  space with a `CLOSED` override in force leaves `openNow`); `evening` (closes ≥ 1200 on any open day, not today);
  every filter before `LIMIT/OFFSET` and in the count; one `now` per answer (SD-10); parameters bound, no string
  interpolation of user input.
- **`GET /price-ranges`** (OD1 a): which spaces count (listed, shown prices, general audience, not hidden/deleted/
  unlisted area), `null` for an empty period, the 30 s cache and `ETag`; public and safe to expose.
- **`availableNow` gone** everywhere (API, shared, web, Home, docs — EC11), and an old `?availableNow=true` /
  `?available=1` answered unfiltered, not 422.
- **The web:** `filtersOf`/`paramsOf` round trip, the price order present only with a subscription (absent, not
  disabled), «مسح» (SD-7, SD-8), the active count (each box once, the place once), invalid bounds said on their field
  and not sent, Arabic-Indic digits, the card's price LTR-isolated, the neutral by-hours badge, «ساعات العمل غير
  متوفرة», Home on `openNow`, `limit=18`, the sheet's five Arabic plural forms, every string in both catalogues.
- **`SegmentedControl`:** a real radiogroup, arrows following the direction in RTL/LTR, Home/End checking (not only
  focusing), one roving tab stop, named by its `Field`, 44 px on touch, the dark theme's edge, semantic tokens only,
  showcase + `foundation.md`.
- **Finding 214:** the test waits for content only the Directory has and expects exactly one search box; no
  retry, no bare timeout bump; the finding's root cause true.
- **The documents:** `directory.md`, `api-contract.md`, ADR 0008's revision line, `data-model.md`, `occupancy.md`,
  `announcements.md`, `conventions.md`, `foundation.md`, `overview.md` — true to the code, one home per fact, nothing
  claimed as built that is not, `#<n>` where a PR number belongs (no `#PRNUM`).
- **Scope:** nothing of the parallel tasks (space profile, identity/palette, women + evening) touched; no migration;
  commits atomic, Conventional, subject ≤ 50 with a body, no tool attribution, no `fixup!`.

## Your output

Write `C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\6_REVIEW_CLAUDE_CODE.md` as you go:

```
# Review of #<n> — Claude Code, Opus 5.5
Head: <HEAD> · commits <n> · files <n> · checks: <green/red> · head moved during the review: <yes/no>
Verdict: <mergeable | mergeable after a fix round | not mergeable>

## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where: <file>:<line> at <HEAD>
- Seen in the code: <what>      (or: Only in a report: <what>)
- Scenario: <inputs or user action → wrong result>
- Fix: <what to change> · Belongs: <a fix round on #<n> (folded into <commit>) | a finding (216–219)>
(None → "None.")

## The test matrix (each T… : present / missing / weaker · would it fail on its break?)
## The owner's decisions and the ODs (each: built as approved / departed, judged)
## The report's deviations, judged
## Documents
## Scope and commits
## Not checked, and why
```

Then stop.
