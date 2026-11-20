# Review of the WOMEN_EVENING PR (the evening switch and the women's hall) — one reviewer

You are a **read-only reviewer** of one Masaha PR, launched headless by the main supervisor once CI was green and
GitHub said `CLEAN`. **The launch line gives the PR number, its branch and the head** — call the head `<HEAD>` and pin
every read to it. **Work alone — no subagents.** No project skill, no branch. Claude Code, Opus 5.5.

**The owner's bar:** the tests must work and point the right way — never bent to pass; no gap.

## Rules

- **Read only, commit objects only.** Fetch once only if `git cat-file -t <HEAD>` fails. Reads: `git show
  <HEAD>:<path>`, `git diff origin/main...<HEAD>`, `git log origin/main..<HEAD>`, `git grep <pattern> <HEAD>`. **Never**
  edit, checkout, switch, reset, stash or commit; no installs, no npm, no tests, no servers, no database, no comments
  on GitHub. Your working tree is not the PR. The only file you write is your report.
- First `gh pr checks <n>` — red or pending: say so and stop. At the end, say whether the head moved.
- Report **verified defects only**: file and line at `<HEAD>`, the scenario, the severity — **blocker** (a migration
  that can fail on existing rows, lose or corrupt data, or drift from the Prisma schema; a role let through what it must
  not — authorization on the server, never by hidden UI; a page that breaks; a filter that returns wrong spaces; a test
  that cannot fail or one bent to pass; production code only a test uses) · **should-fix** (a real defect a user can
  meet; a missing or weaker planned `T…`; an owner's decision built otherwise without a written reason; accessibility;
  hardcoded text or a string in one language only; a colour or class outside the design system; a false document) ·
  **nit**. The fix and where it belongs (a fix round, folded into `<commit>`; or a finding — check the index for the
  next free number). "Plausible" when unsure. No praise. Check a library's behaviour before calling a bug (Prisma 7,
  PostgreSQL, Express 5, zod, TanStack Query v5, Radix). Do not report what lint, typecheck, Prettier, `check:*` or CI
  enforce. **Known and accepted:** the evening-switch commit's 51-character subject (`6f6a59ab` before the
  wording fold; the owner waived it); the last text change (X6's wordings and `AMENITY_IN_FILTER`) ran no local tests
  or checks — the owner's word, CI judges it.

## Read

1. `git show <HEAD>:CLAUDE.md`; at `<HEAD>`: `docs/development/workflow.md`, `testing.md`, `engineering-principles.md`.
2. **`C:\dev\masaha\workspace\TASKS\WOMEN_EVENING\0_OWNER_DECISIONS.md`** (binding: E1–E9, W1–W6) and
   **`0_CARRIED_FROM_144.md`** (the first commit's ten items).
3. `C:\dev\masaha\workspace\TASKS\WOMEN_EVENING\1_PLAN_AND_EXEC_PROMPT.md` (the task's rules), `2_PLAN.md` (the test
   matrix) and the report **`4_REPORT.md`** — judge every *Decision taken without the owner* (X1–X16) and every
   deviation: sound / acceptable / wrong.
4. The diff commit by commit, then files at `<HEAD>`.

## Look hardest at

- **The migration** (`…_women_evening`): the column and its default; **E8's backfill** (an open day closing at 1200 or
  later — closed days excluded? the `IF NOT EXISTS` on a re-run); **W3's row** (idempotent on the unique key; the
  `HAVING count(*) > 0` rule on an empty catalogue and X9's seed path; the order it takes); no drift from
  `schema.prisma`; existing rows untouched otherwise; what production sees on deploy.
- **The API:** the hours group's save with the switch (X2, X3 — required; a save of the hours alone never clears it,
  nor the shifts' save); its date, staleness and audit; `evening` by the switch only (E7) and `womensHall` by the
  amenity's **key**, active only (X10), each combined with every other filter, on the list and the map; the admin's
  rule on `womens_hall` (X8: retire refused with 409 `AMENITY_IN_FILTER`, nothing written; rename, icon and order
  allowed) enforced on the server; the public page and the card's fields; authorization unchanged.
- **The web:** «ساعات العمل»'s box, line and hint (E6, E9, X4–X6) for the owner and the admin; the panel's «قاعة
  للنساء» in «أخرى» and `women=1` (X10); the card's two marks (muted, after «موثّقة», in the link's description; W6 —
  never «مختلطة»); the public page's «دوام مسائي»; both languages, RTL, axe.
- **The carried fixes** (first commit): the supervisor checked each in the code; confirm they did not break their
  neighbours (the account navigation, the profile's index, NearMe, `check:classes`' normalised spellings).
- **The Arabic texts** of X6 and `AMENITY_IN_FILTER` were approved by the owner (`0_OWNER_DECISIONS.md` › *The Arabic
  texts*): check the built copy, its English, and every test and document quoting them match those words exactly.

## Output

Write `C:\dev\masaha\workspace\TASKS\WOMEN_EVENING\7_REVIEW.md`:

```
# Review of #<n> (WOMEN_EVENING) — Claude Code, Opus 5.5
Head: <HEAD> · commits <n> · files <n> · checks: <green/red> · head moved: <yes/no>
Verdict: <mergeable | mergeable after a fix round | not mergeable>

## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where / Seen in the code (or Only in a report) / Scenario / Fix · Belongs
(None → "None.")

## The test matrix rows (present / missing / weaker · would it fail on its break?)
## Decisions E1–E9, W1–W6 and X1–X16 (built / departed, judged)
## The report's deviations, judged
## The migration, read line by line
## Documents
## Scope and commits
## Not checked, and why
```

Then stop.
