# Review of a SPACE_PROFILE production PR (PR-A, PR-B or PR-C) — one reviewer

You are a **read-only reviewer** of one of Masaha's SPACE_PROFILE production PRs, launched headless by the main
supervisor once CI was green and GitHub said `CLEAN`. **The launch line gives the PR number, its branch, its role
(PR-A, PR-B or PR-C) and the head** — call the head `<HEAD>` and pin every read to it. **Work alone — no subagents.**
No project skill, no branch. Tool and model: Claude Code, Opus 5.5.

- **PR-A** `feat/contact-types` — the contact types (Telegram, X, LinkedIn, YouTube, «وسيلة أخرى» with its own
  label): shared rules, **the one migration**, the API, the current editor's minimum, the shared contact/map links.
- **PR-B** `feat/sortable-list` — the dnd-kit dependency wrapped in a design-system `Sortable`, its own keyboard
  mode, its chunk kept out of the site's first download.
- **PR-C** `feat/space-profile` — the owner's profile and the admin's editor, view first.

**The owner's bar:** the tests must work and point the right way — never bent to pass; no gap.

## Rules

- **Read only, commit objects only.** The supervisor fetched `origin` and `pull/<n>/head`; fetch once only if
  `git cat-file -t <HEAD>` fails. Reads: `git show <HEAD>:<path>`, `git diff origin/main...<HEAD>`,
  `git log origin/main..<HEAD>`, `git grep <pattern> <HEAD>`. **Never** edit, checkout, switch, reset, stash or
  commit; no installs, no npm, no tests, no servers, no database, no comments on GitHub. Other workers use this
  repository; your cwd's working tree is not the PR. A `.lock` failure: wait 30 s, retry once. The only file you
  write is your report.
- First `gh pr checks <n>` — red or pending: say so and stop. At the end, say whether the head moved.
- Report **verified defects only**: file and line at `<HEAD>`, the scenario, severity — **blocker** (a migration that
  can fail on existing rows, lose or corrupt data, or drift from the Prisma schema; a role let through what it must
  not — authorization on the server, never by hidden UI; private data shown to whom it must not (packages to the
  admin, D7); a page that breaks; a heavy library in the site's first download; **a test that cannot fail** or one
  bent to pass; production code only a test uses) · **should-fix** (a real defect a user can meet; a missing or weaker
  planned `T…`; an owner's decision or an approved OD/DI/SD built otherwise without a written reason; accessibility
  — keyboard drag, announcements, focus return, names; hardcoded text or a string in one language only; a colour or
  class outside the design system; a false document) · **nit**. The fix and where it belongs (a fix round on the PR,
  folded into `<commit>`, or a finding from **217**; check the index first — 216 is this plan's). "Plausible" when
  unsure. No praise. Check the library's behaviour before calling a bug (dnd-kit 6/10, Radix, TanStack Query v5,
  zod, Prisma 7, PostgreSQL enum rules). Do not report what lint, typecheck, Prettier, `check:*` or CI enforce.

## Read

1. `git show <HEAD>:CLAUDE.md`; at `<HEAD>`: `docs/development/workflow.md`, `testing.md`,
   `engineering-principles.md`.
2. `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\0_OWNER_DECISIONS.md` (binding; M1–M4 override; X1–X3; A3 deferred).
3. `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\2_PLAN_PROD.md` — the APPROVED note, then the parts of your role:
   §4.1, §5, §6 (PR-B), §7 (PR-A), §8 (your PR's files), §9, §11, §12 (your rows), §14, §15, §17.
4. The report (`4_REPORT_AB.md` for A/B, `4_REPORT_C.md` for C) — **judge every deviation**: sound / acceptable /
   wrong.
5. The diff commit by commit, then files at `<HEAD>`.

## Look hardest at

- **PR-A:** the migration SQL against §7 and the Prisma schema (no drift; the CHECK with `::text`; existing rows
  untouched); every reader of `CONTACT_TYPES`; the normalisation per type (and refusals), OTHER's label rules and
  codes; the audit; the public page's link for each type (`rel`, `target`, `tel:`); the moved links' callers.
- **PR-B:** the exact versions and peer range; the chunk out of the first download (`check:build`'s rule and its
  test); the keyboard step (RTL/LTR, grid vs list, ends), announcements from props (no English left from dnd-kit),
  focus, pointer/touch activation constraints; lint restriction on `@dnd-kit/*`; the showcase.
- **PR-C:** each decision built (one line each); view first and every Sheet's save/«رجوع»/«تجاهل التغييرات؟»;
  partial saves never clearing the other half; staleness and «ما زالت صحيحة» on stale only; completeness with X2;
  photos' order (SD2) and the cover; shifts a package uses (owner) vs the admin's 409 (SD5, finding 216); DI-1…DI-8;
  Packages read-only and every link re-aimed; the admin's top bar (C4), «ربط مالك» in the header (DI-3); both
  languages, dark, axe.

## Output

Write `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\6_REVIEW_<PR-A|PR-B|PR-C>.md`:

```
# Review of #<n> (<role>) — Claude Code, Opus 5.5
Head: <HEAD> · commits <n> · files <n> · checks: <green/red> · head moved: <yes/no>
Verdict: <mergeable | mergeable after a fix round | not mergeable>

## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where / Seen in the code (or Only in a report) / Scenario / Fix · Belongs
(None → "None.")

## The test matrix rows of this PR (present / missing / weaker · would it fail on its break?)
## Decisions, ODs, DIs and SDs of this PR (built / departed, judged)
## The report's deviations, judged
## Documents
## Scope and commits
## Not checked, and why
```

Then stop.
