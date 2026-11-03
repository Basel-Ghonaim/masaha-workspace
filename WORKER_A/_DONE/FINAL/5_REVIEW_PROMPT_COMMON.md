# Review of #132 — the rules common to the five reviewers (read whole, after your role file)

#132 (`feat/final`, head **`a12c0790`**, 124 commits, 1001 files) is worker A's **last build PR of Masaha v1**: every
one of the 32 screens complete with no gap, and every open finding closed (built, or accepted by the owner) — web,
API, shared and documents together. It was built by a lead and sub-agents under the owner's no-stop rule, on the
approved plan `C:\dev\masaha\workspace\WORKER_A\FINAL\2_PLAN.md`. CI is green and the owner ran the whole suite
locally, green. **Five independent reviewers run in parallel, each on its own commits** (your role file lists them).
**Work alone — no subagents.** This is a review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/132/head` — **but five reviewers run at once in this folder: do not fetch.** The supervisor fetched both
  before launching you; fetch once only if `git cat-file -t a12c0790` fails. **Pin every read to a sha** — your commits (`git show <sha>`, `git show <sha> --stat`) and the head
  `a12c0790` (`git show a12c0790:<path>`). No edits, checkout, switch or reset, no installs, no npm or test runs, no
  servers, no database commands, no comments on GitHub. The only file you write is your report. A `git` command
  failing on a `.lock` file: wait 30 s, retry once.
- First `gh pr checks 132` — red or pending: say so and stop. At the end, `gh pr view 132 --json headRefOid` again: say
  whether the head moved.
- **Your commits are yours; the head is the truth.** Read a file at the head when a later commit changed it, and say
  so. A defect in another reviewer's commits: one line under *Outside my range*, not a finding.
- Report **verified defects only**: file and line at the head, the scenario (user action or inputs → wrong result),
  severity — **blocker** (wrong money computed, shown, sent or recorded; any amount on the owner's overview; a role
  offered or let through what it must not; private data shown to whom it must not; a key renewed on a retry or
  missing; a lock or snapshot rule broken; a migration that loses or corrupts data; a page that breaks; a test that
  cannot fail) · **should-fix** (a real defect a user can meet; **a gap left on a screen** — the mission's condition is
  "complete, no gap"; a missing planned test or break; a false document; a decision departing from the approval note
  without need) · **nit** — and the fix, belonging to **a fix round on #132** (nothing carries: this is the last build
  PR) or **a finding** (your role file's numbers). "Plausible" when unsure, with why. Say what you **saw in the code**
  and what you only **read in a report**. A point whose own conclusion is "no change needed" is not a finding. No
  praise.
- **Check the library's defaults before calling a bug** (TanStack Query v5, Radix, react-hook-form, react-day-picker
  10, Prisma 7, Express 5).
- Do not report what lint, typecheck, Prettier, `check:*` or CI enforce and passed.

## What every reviewer reads

1. `git show origin/main:CLAUDE.md`.
2. `C:\dev\masaha\workspace\WORKER_A\FINAL\2_PLAN.md`: **the approval note at its top and §2 (binding)**; then the
   units and sections your role file names (§5's `D…`, §6's `DI…`, §9.1's commits, §10's tests and breaks, §11's real
   run, §12's documents).
3. `C:\dev\masaha\workspace\WORKER_A\FINAL\4_REPORT_LEAD.md`: *Decisions taken without the owner* (SERIOUS first) and
   the sections for your units; the lanes' reports under `scripts\lane-*\REPORT.md` for your lanes. **Judge every
   decision taken without the owner in your range:** sound / acceptable / wrong, with why.
4. For screens: the prototype pages your role file names (`docs/design/prototype/*.html` at `a12c0790`) and
   `docs/frontend/design-system/foundation.md` §13 — **is each screen complete, with no gap, as the plan's §4.1 listed
   its gaps?**

## The checklist — answer every line in your report

1. Every commit of your range read (list them with one line each).
2. The plan's decisions for your units built as approved (or the departure judged).
3. Money, roles, privacy, keys and locks in your range — each checked, or "none in my range".
4. Each planned test and break of your range — present / missing / weaker; would it fail if its behaviour regressed?
5. Each screen of your range — complete against its prototype and §4.1's gaps (both languages, dark, 390 / 768 / 1440,
   empty / loading / error states, accessibility) — or the gap named.
6. Each finding your range closes — built as its *Resolves when* says, or accepted with the owner's line.
7. The documents your range changes — true to the code, one home per fact, `#132` where it goes.

## Your output

Write `C:\dev\masaha\workspace\WORKER_A\FINAL\6_REVIEW_<R>.md` (your role file gives `<R>`), as you go:

```
# Review of #132 — <R>: <your role> — <tool and model>
Head: a12c0790 · commits <n> · checks: <green/red> · head moved during the review: <yes/no>
Verdict for my range: <mergeable | mergeable after a fix round | not mergeable>

## Findings (verified defects only, most severe first)
### <R>-F1 — <blocker|should-fix|nit> · <title>
- Where: <file>:<line> at a12c0790
- Seen in the code: <what>      (or: Only in a report: <what>)
- Scenario: <user action or inputs → wrong result>
- Fix: <what to change> · Belongs: <a fix round on #132 (folded into <commit>) | a finding (<your numbers>)>
(None → "None.")

## The checklist (lines 1–7, each answered)
## Decisions taken without the owner in my range, judged
## Outside my range
## Not checked, and why
```

Then stop.
