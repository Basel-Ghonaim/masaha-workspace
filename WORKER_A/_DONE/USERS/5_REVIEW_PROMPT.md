# Review — USERS (an independent reviewer, in two halves)

You are the **independent reviewer** of worker A's USERS PR (`feat/admin-users`) in Basel-Ghonaim/masaha:
the admin's users page (screen 29), seven commits, about 88 files. Claude Code executed it in another
conversation; you start fresh and trust nothing you have not seen in the code. Find the PR: `gh pr list
--head feat/admin-users --json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_A\USERS\6_REVIEW_CLAUDE_CODE.md`: first the verdict and the five most
important findings, then the rest.

## How — two subagents in parallel, then you merge
The PR is large (the owner's choice: one PR, the review split). **Run two subagents at once**, each with
these Rules and its own half, each returning its findings in the output's shape; then **verify every
blocker and should-fix yourself in the code** before it enters the report, merge the two lists, and drop
duplicates.
- **Half 1 — commits 1–4:** `DataTable cardsBelow` (and the spaces list's, the approval note's alternative
  B); the users list's shared core (no behaviour change to the owners page); finding 88 (the upgrade
  confirm's desks); the users page (search, chips, address, pages, cards at 768, the spaces column, «ربط
  بمساحة» from a person — PR 3's dialog reused, the desks unavailable in its choices).
- **Half 2 — commits 5–7:** the role change («مستخدم» ⇄ «أدمن» only, held up front with its reason for an
  owner, an owner of deleted spaces, a receptionist; the `AlertDialog` naming the consequence; every
  refusal, `ACCOUNT_PASSWORD_PENDING` included); suspend and restore (the consequence, a receptionist's
  desk line, no undo after a restore); issuing a temporary password (a confirm first, then #89's dialog with
  `kind="issued"`, disabled with its reason for a Google-only account; finding 49's line); `RefusalText` in
  `shared/forms`; the row menu composed in the page.

## Rules
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/<n>/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. Confirm `gh pr checks <n>` is green first; if a lane is red or pending, say
  so and stop. At the end, check the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** No praise, no tool attribution, no project
  skill.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_A\USERS\2_PLAN.md` — the owner's approval note at its top binds —
the execution prompt `3_EXEC_PROMPT.md`, and the report `4_REPORT_PR1.md`: judge every departure and every
break that did not go red. Scope: `apps/web`, `docs`. Also across both halves: frontend rules (design system
only, semantic tokens, no physical direction, every string in both catalogues, names isolated in lines),
focus after each dialog, the documents true to the code (one home per fact), commit subjects (≤ 50) and
bodies, the screenshots in `shots\` (look at them), the routes test's time (finding 87).

**Known and deferred (do not re-report, but say if the fix it names is wrong or incomplete):**
`C:\dev\masaha\workspace\WORKER_A\USERS\0_CARRIED_FROM_91.md` — the focus after the issued-password dialog,
and #91's carried line.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** (a fix round on this PR / OWNER_SETUP / a finding to record); a short "Checked and fine" list;
then stop.
