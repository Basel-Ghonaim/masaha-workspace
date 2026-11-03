# Review of #131 — the rules common to the three reviewers (read whole, after your role file)

#131 (`feat/backend-final`) is worker B's **one PR for the rest of Masaha v1's API**, built by a lead and sub-agents
under the owner's no-stop rule, on the approved plan
`C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\2_PLAN.md`: #130's review fixes and finding 153, the `payments`
totals, the space's **finance** (income, who owes and who paid, occupancy), **the owner's and the admin's overviews**
(step 12), and the API items left (finding 170, `GET`/`PATCH /me`, `GET …/visits`, finding 167's filter). **Three
independent Claude reviewers run in parallel, each on its own commit range** (your role file names yours). **API
only** (`apps/api`, `packages/shared`, `docs`). **Work alone — no subagents.** This is a review, not a Work Item: run
no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/131/head`; **pin every read to a sha** — your range's commits and the PR's head (your role file names it);
  another process's fetch may overwrite `FETCH_HEAD`. No edits, checkout, switch or reset, no installs, no npm or test
  runs, no servers, no database commands, no comments on GitHub. The only file you write is your report. A `git`
  command failing on a `.lock` file: wait 30 s, retry once.
- First `gh pr checks 131` — a red or pending check: say so and stop. At the end, `gh pr view 131 --json headRefOid`
  again: say whether the head moved.
- **Your range is yours; the head is the truth.** Read a file at the head when a later commit changed it, and say so.
  A defect in another range: one line under *Outside my range*, not a finding.
- Report **verified defects only**: file and line at the head, the scenario (inputs → wrong result), severity —
  **blocker** (wrong money computed or shown; any amount reaching the owner's overview (OV1); a role let through —
  finance is the owner's alone, the overview the owner's (OV3), the admin's overview the admin's; private data reaching
  whom it must not; a lock or snapshot rule broken; a 500 a client can cause; a test that cannot fail) ·
  **should-fix** (a real defect; a missing planned test or break; a false document; a decision departing from the
  approval note without need) · **nit** — and the fix, belonging to **a fix round on #131** (this is worker B's last
  plan: nothing carries to a next PR) or **a finding** (your role file's numbers). "Plausible" when unsure, with why.
  Say what you **saw in the code** and what you only **read in a report**. A point whose own conclusion is "no change
  needed" is not a finding. No praise.
- Do not report what lint, typecheck, Prettier, `check:*` or CI enforce and passed.

## What every reviewer reads

1. `git show origin/main:CLAUDE.md`.
2. `2_PLAN.md`: **the owner's approval note at its top and §2 (binding: the finance's 12 decisions, Q1–Q12, OV1–OV8,
   OD1–OD11)**; then the sections your role file names.
3. `3_EXEC_PROMPT_LEAD.md` and `4_REPORT_LEAD.md` (same folder): *Decisions taken without the owner* (SERIOUS first)
   and the sections for your range; the lanes' reports under `scripts\lane-*\REPORT.md`. **Judge every decision taken
   without the owner in your range:** sound / acceptable / wrong, with why.
4. The contract at the head for your routes, and the shared types (`packages/shared`).

## Your output

Write `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\6_REVIEW_<R>_CLAUDE_CODE.md` (your role file gives `<R>`), as you
go:

```
# Review of #131 — <R>: <your role> — Claude Code
Head: <sha> · range <from>..<to> (<n> commits) · checks: <green/red> · head moved during the review: <yes/no>
Verdict for my range: <mergeable | mergeable after a fix round | not mergeable>

## Findings (verified defects only, most severe first)
### <R>-F1 — <blocker|should-fix|nit> · <title>
- Where: <file>:<line> at <head>
- Seen in the code: <what>      (or: Only in a report: <what>)
- Scenario: <inputs → wrong result>
- Fix: <what to change> · Belongs: <a fix round on #131 (folded into <commit>) | a finding (<your numbers>)>
(None → "None.")

## The plan's tests and breaks for my range (one line each: present / missing / weaker; would it fail?)
## Decisions taken without the owner in my range, judged
## Outside my range
## Checked and fine
## Not checked, and why
```

Then stop.
