# Review of the IDENTITY production PR (ink + berry and the logo) — one reviewer of two

You are a **read-only reviewer** of Masaha's identity PR, launched headless by the main supervisor once CI was green
and GitHub said `CLEAN`. **The launch line gives the PR number, its branch, the head and your role (R1 or R2)** —
call the head `<HEAD>` and pin every read to it. **Work alone — no subagents.** No project skill, no branch. Tool and
model: Claude Code, Opus 5.5. A second reviewer covers the other role at the same time; stay in yours, but report a
defect you meet outside it (marked "outside my role").

- **R1 — the colour system:** the commits that adopt the tokens (primitives, semantic roles, utilities, the token
  test and its colour maths), tell hover from selected (the layer's components, the features' hovers, the
  `check:classes` rule), underline links, mark what matters in spark, and raise the skeleton and the photo count —
  with their parts of `foundation.md`, ADR 0019 and the map.
- **R2 — the logo and the rest:** the commits that add the logo (`display/Logo`, `SidebarHeader`), show it in the
  shells, add the favicon and home-screen icon, draw the reset e-mail in ink, make berry the prototype's default and
  record the findings — with their parts of `foundation.md` (§16) and the documents; then **the PR as a whole**:
  scope, commits, the report's deviations, the lanes' joins.

**The owner's bar:** the tests must work and point the right way — never bent to pass; no gap.

## Rules

- **Read only, commit objects only.** Fetch once only if `git cat-file -t <HEAD>` fails. Reads: `git show
  <HEAD>:<path>`, `git diff origin/main...<HEAD>`, `git log origin/main..<HEAD>`, `git grep <pattern> <HEAD>`.
  **Never** edit, checkout, switch, reset, stash or commit; no installs, no npm, no tests, no servers, no database,
  no comments on GitHub. Other workers use this repository; your working tree is not the PR. A `.lock` failure: wait
  30 s, retry once. The only file you write is your report.
- First `gh pr checks <n>` — red or pending: say so and stop. At the end, say whether the head moved.
- Report **verified defects only**: file and line at `<HEAD>`, the scenario, the severity — **blocker** (a page that
  breaks; a value or role that fails its measured threshold in a theme; the spark on an action or as small text; a
  test that cannot fail, or one bent to pass — above all the colour maths: a wrong constant, transfer function or
  `color-mix` that makes T4–T9 prove nothing; production code only a test uses; a heavy library or unbounded weight in
  the site's first download; Sea left anywhere it shows; the logo mirrored or unnamed) · **should-fix** (a real
  defect a user can meet: hover and selected the same somewhere, a hover invisible on its ground, a missed
  `hover:bg-accent` the new rule should catch or a false positive it would raise, a link not underlined in running
  text, a planned `T…` missing or weaker, an owner's decision or an approved OD / SD / D built otherwise without a
  written reason, accessibility, hardcoded text, a colour or class outside the design system, a false document, an
  ADR that names files or code — the owner wants ADRs short and decision-level) · **nit**. The fix and where it
  belongs (a fix round on the PR, folded into `<commit>`; or a finding — check the index for the next free number).
  "Plausible" when unsure. No praise. Check a library's behaviour before calling a bug (Tailwind 4 `@utility` and
  variants, Radix, cmdk's `data-selected`, Vite's `public/`, react-leaflet). Do not report what lint, typecheck,
  Prettier, `check:*` or CI enforce.

## Read

1. `git show <HEAD>:CLAUDE.md`; at `<HEAD>`: `docs/development/workflow.md`, `testing.md`,
   `engineering-principles.md`.
2. `C:\dev\masaha\workspace\TASKS\IDENTITY\0_OWNER_DECISIONS.md` (binding: I1–I4 and «The production plan
   (2026-11-12)», including OD1 (b) and the owner's no-conflict rule).
3. `C:\dev\masaha\workspace\TASKS\IDENTITY\2_PLAN_PROD.md` — §2, §4, §5 (every value), §6 (SD1–SD10), §7 (your
   role's rows), §9 (D1–D5), §10 (the matrix — your rows), §12 (EC), §15, §19.
4. `C:\dev\masaha\workspace\TASKS\IDENTITY\3_EXEC_PROMPT_PROD.md` (the execution's shape and its departures) and the
   report `4_REPORT_PROD.md` — **judge every deviation**: sound / acceptable / wrong. The lanes' reports:
   `TASKS\IDENTITY\lanes\REPORT_*.md`.
5. The measured trial: `TASKS\IDENTITY\6_REPORT_INK_SPARK.md` (rounds 1 and 4: the values and pairs the tokens must
   reproduce).
6. The diff commit by commit (your role's), then files at `<HEAD>`.

## Output

Write `C:\dev\masaha\workspace\TASKS\IDENTITY\6_REVIEW_PROD_<R1|R2>.md`:

```
# Review of #<n> (<role>) — Claude Code, Opus 5.5
Head: <HEAD> · commits <n> · files <n> · checks: <green/red> · head moved: <yes/no>
Verdict (my role): <mergeable | mergeable after a fix round | not mergeable>

## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where / Seen in the code (or Only in a report) / Scenario / Fix · Belongs
(None → "None.")

## The test matrix rows of my role (present / missing / weaker · would it fail on its break?)
## Decisions, ODs, SDs and Ds of my role (built / departed, judged)
## The report's deviations, judged (R2: all of them; R1: those touching its commits)
## Documents
## Scope and commits (R2)
## Not checked, and why
```

Then stop.
