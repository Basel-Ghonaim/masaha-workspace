# Review of #129 — the rules common to the three reviewers (read whole, after your role file)

#129 (`feat/step10-screens`, head **`fcf46637`**, 16 commits, 248 files) is worker A's **one PR for the rest of the
PAYMENTS_STEP10 plan**, built by a lead and three sub-agents (lanes) under the owner's no-stop rule: the plan's PR 2
(announcements), PR 3 (data reports), PR 4a (report wrong information), PR 4b (favourites), plus findings 169 and 173
(the calendar). **Three independent Claude reviewers run in parallel, each on its own commit range** (your role file
names yours). **Web only** (`apps/web`, `docs`, the root `eslint.config.js`); the API is built and merged. **Work
alone — no subagents.** This is a review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/129/head`; **pin every read to a sha** — your range's commits and the head `fcf46637` (`git show <sha>:<path>`,
  `git diff <from>..<to>`); another process's fetch may overwrite `FETCH_HEAD`. No edits, checkout, switch or reset,
  no installs, no npm or test runs, no servers, no database commands, no comments on GitHub. The only file you write
  is your report. A `git` command failing on a `.lock` file: wait 30 s, retry once.
- First `gh pr checks 129` — a red or pending check: say so and stop. At the end, `gh pr view 129 --json
  headRefOid` again: say whether the head moved.
- **Your range is yours; the head is the truth.** Review the commits of your range; read a file at the head
  `fcf46637` when a later commit (another reviewer's range) changed it, and say so. A defect that lives in another
  range: name it in one line under *Outside my range* (file, line, why), not as a finding — its reviewer owns it.
- Report **verified defects only**: file and line at the head, the scenario (user action → wrong result), severity —
  **blocker** (wrong money or dates shown, sent or recorded; a role offered what it must not; private data shown to
  whom it must not — the reporter to the owner above all; a key renewed on a retry or missing; a page that breaks; a
  test that cannot fail) · **should-fix** (a real defect a user can meet; a missing planned test or break; a
  document that says something false; a lane's decision that departs from the plan's binding approval note without
  need) · **nit** — and the fix. "Plausible" when unsure, with why. Say what you **saw in the code** and what you only
  **read in a report**. A point whose own conclusion is "no change needed" is not a finding. No praise.
- **Check the library's defaults before calling a bug** (TanStack Query v5 — dedupe of in-flight queries,
  `invalidateQueries` while fetching; Radix — `AlertDialog`/`Dialog` auto focus, `onCloseAutoFocus`; react-hook-form;
  react-day-picker 10 — `resetOnSelect`, `addToRange`; `Intl.DateTimeFormat`).
- Do not report what lint, typecheck, Prettier, `check:*` or CI enforce and passed.
- **New findings** (a defect outside the PR's scope to fix): number them from your role file's range only.

## What every reviewer reads

1. `git show origin/main:CLAUDE.md` — the project's rules.
2. `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\2_PLAN.md`: **the owner's approval note at its top (binding:
   DI-1 … DI-61 and §9's Arabic approved as written; S1–S16; the real run's writes, the extension applied with 1
   day)**; then the sections your role file names.
3. `3_EXEC_PROMPT_LEAD.md` (what the lead was told — §2 lists what changed since the plan: #127, #128's extension
   count) and `4_REPORT_LEAD.md` (same folder): *Decisions taken without the owner* (LEAD-D1–D12) and the sections
   your role file names. Lane reports: `scripts\lane-a\REPORT.md`, `scripts\lane-b\REPORT.md`,
   `scripts\lane-c\REPORT.md`. **Judge every decision taken without the owner in your range** (the lane's LA/LB/LC-D*
   and the lead's that touch it): sound / acceptable / wrong, with why.
4. The contract at `origin/main` (`docs/api/api-contract.md`) for the routes your range calls, and the shared types
   the web imports (`packages/shared`).

## Your output

Write `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\6_REVIEW_LEAD_<R>_CLAUDE_CODE.md` (your role file gives `<R>`),
**as you go**, in this shape:

```
# Review of #129 — <R>: <your role> — Claude Code
Head: fcf46637 · range <from>..<to> (<n> commits) · checks: <green/red> · head moved during the review: <yes/no>
Verdict for my range: <mergeable | mergeable after a fix round | not mergeable>

## Findings (verified defects only, most severe first)
### <R>-F1 — <blocker|should-fix|nit> · <title>
- Where: <file>:<line> at fcf46637
- Seen in the code: <what>      (or: Only in a report: <what>)
- Scenario: <user action → wrong result>
- Fix: <what to change> · Belongs: <a fix round on #129 (folded into <commit>) | a finding (<your range>)>
(None → "None.")

## The plan's tests and breaks for my range (one line each: present / missing / weaker; would it fail?)
## Decisions taken without the owner in my range, judged
## Outside my range (one line each, for the other reviewers)
## Checked and fine
## Not checked, and why
```

Then stop.
