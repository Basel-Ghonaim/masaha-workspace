# Review — OWNERS PR 3 (an independent reviewer)

You are the **independent reviewer** of OWNERS PR 3 (`feat/admin-owner-links`) in Basel-Ghonaim/masaha —
the last of three PRs of the OWNERS item. Claude Code executed it in another conversation; you start fresh
and trust nothing you have not seen in the code. Find the PR: `gh pr list --head feat/admin-owner-links
--json number,headRefOid,mergeStateStatus`. Write your report to
`C:\dev\masaha\workspace\WORKER_A\OWNERS\6_REVIEW_PR3_CLAUDE_CODE.md`, in parts: first the verdict and the
five most important findings, then the rest.

## Rules
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/<n>/head`; base = `origin/main`; `git diff origin/main...<head>`,
  `git show <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers,
  database commands, no GitHub comments. CI ran every lane on the head — confirm with `gh pr checks <n>`
  first; if a lane is red or pending, say so and stop. At the end, check the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** No praise, no tool attribution, no project
  skill.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` — the owner's approval note at its top (above
all its last block: #89's leftovers (a)–(d)), and **PR 3 only** (§7 *PR 3*, §9 *PR 3 · commits 1–2*,
§10 *PR 3*, §11, §14 points 1 and 2) — the execution prompt `3_EXEC_PROMPT_PR3.md` (three commits; #90's
`ACCOUNT_PASSWORD_PENDING`), and the report `4_REPORT_PR3.md`: judge every departure and every break that
did not go red. PR 2's review `6_REVIEW_PR2_CLAUDE_CODE.md` says what the leftovers were. Scope:
`apps/web`, `docs`.

## Look at these, in this order — think beyond the plan
1. **#89's leftovers (commit 1):** names isolated in every line naming a record (toasts, the password
   dialog, each option's owners) — mixed Arabic/English names in both languages; the space search's words;
   `useSpaceChoices` reusing the list's row rules and one «مخفية» badge; nothing copied twice.
2. **The consequence said before the act:** linking an unverified space (it becomes verified), a verified
   one (another owner), a `USER` chosen (the role line — only when certain); unlinking the last owner vs.
   one of several, **from the space's owners read on every opening**, never from a row that may be stale;
   the read failing; the action held until the read.
3. **The refusals:** every code the link and the unlink can answer worded in the dialog, which stays open
   (`ACCOUNT_PASSWORD_PENDING`, `RECEPTION_LINK_ACTIVE`, `ACCOUNT_IS_ADMIN`, `ACCOUNT_SUSPENDED`, validation,
   `not_found`); a 429.
4. **The editor (commit 3, finding 59):** a verified space names its owners and offers one unlink per
   owner; an unverified one offers «ربط مالك» — disabled with its reason while there are unsaved changes
   (design issue 7); the editor turning read-only once linked; the cache refreshed so no screen shows the
   old state.
5. **Focus and dialogs:** focus returned to the trigger, or to the list when the row leaves it; no X on the
   `AlertDialog`; the destructive action stays until the answer.
6. **The boundary:** `owners` out of architecture §3 and `dashboardOnly.ts` (§14 point 1) — and
   `check:build` still keeps admin code out of the site's first download; no cross-feature import except
   through `index.ts` and the slot.
7. **The tests:** each would fail with its planned break.
8. Frontend rules (design system only, semantic tokens, no physical direction, every string in both
   catalogues); `space-links.md`, `spaces.md`, `overview.md`, `architecture.md`, finding 59 resolved and the
   new findings true to the code, one home per fact; commit subjects counted (≤ 50) and bodies; the real
   run's screenshots (`shots\pr3\`) — look at them: PR 2's missing English/dark/390/768 ones included.
9. **Against worker B's SETTINGS PR (if open):** the shared documents' text conflicts and the findings'
   numbers.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** (a fix round on this PR / USERS (the next web item) / a finding to record); a short "Checked and
fine" list; then stop.
