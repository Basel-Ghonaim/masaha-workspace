# Review — PR #89, OWNERS PR 2 (an independent reviewer)

You are the **independent reviewer** of PR **#89** (`feat/admin-add-owner`, head `a074e6d2`) in
Basel-Ghonaim/masaha — the second of three PRs of the OWNERS item. OpenCode built it; a Claude Code fix
round completed it (the security step, the missing tests, a defect). The owner chose Claude Code for this
review: you start fresh and trust nothing you have not seen in the code. Write your report to
`D:\masahaWorkspace\WORKER_A\OWNERS\6_REVIEW_PR2_CLAUDE_CODE.md`, in parts: first the verdict and the five
most important findings.

## Rules
- **Run from `C:\Users\basel\masaha-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/89/head`; base = `origin/main` (`02b1067a` when written; if `main` has moved, say
  so); `git diff <base>...a074e6d2`, `git show <commit>`, `git show a074e6d2:<file>`. No edits, checkouts,
  installs, npm or test runs, servers, database commands, no GitHub comments. CI ran every lane on this head.
  First and last: `gh pr view 89 --json headRefOid,mergeStateStatus` — if the head moved, review the new one
  and say so.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** No praise, no tool attribution, no project
  skill.

## What the PR must be
The plan `D:\masahaWorkspace\WORKER_A\OWNERS\2_PLAN.md` — the owner's approval note at its top (the
security addition above all), and **PR 2 only** (§7 *PR 2*, §9 *PR 2 · commits 1–4*, §10 *PR 2*, §11) —
the fix prompt `3b_FIX_PROMPT_PR2.md`, and the report `4_REPORT_PR2.md` (its *Fix round 1* section): judge
every departure in both rounds and the three breaks that did not go red. Scope: `apps/web`, `docs`.

## Look at these, in this order — think beyond the plan
1. **The account check before an upgrade (`useEmailAccount`, `useAddOwnerForm`):** can an admin upgrade an
   account they were not shown? The exact-email match (case, normalisation, the server's email form); a
   search answering more than one page; a failed or stale read; the email edited between the check and the
   submit; the `upgradeRef` set in an effect — can a submit send `upgradeExisting: true` from an earlier
   render; an account that is an admin's or suspended.
2. **The one-time password:** shown once, nowhere in the query cache after it is handed on (both
   mutations); the dialog now rendered beside the sheet (the fixed defect) — does it survive the sheet
   closing and every re-render, and clear only on «تم»; copy failure; the handover's failures (design
   issues 5, 6); no X, no Escape, no outside click.
3. **The `Combobox` change (a design-system change):** `search` and `loading` leave every existing caller
   unchanged; the showcase example; `foundation.md`.
4. **The tests:** each would fail with its planned break; the three that did not go red — is each
   reason true, and is the replacement proof enough?
5. **The capability boundary:** `space-links` reads the users list for the check without importing another
   feature; dashboard-only (nothing new in the site's first download; finding 87).
6. Frontend rules (design system only, semantic tokens, no physical direction, every string in both
   catalogues, mixed-direction names cut with `lineParts`); `users.md`, `space-links.md`,
   `localisation.md`, findings 82, 83, 87 true to the code, one home per fact; commit subjects counted
   (≤ 50) and bodies.
7. **The PR description** still describes the first round — list what it must say now.
8. **Against PR #90** (STAFF, open): the text conflicts (`findings/README.md`, `space-links.md`) and the
   `AdminUserRow` literals this PR adds that need `receptionSpaces: []` if #90 merges after it — name them.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** (a fix round on this PR / PR 3 / a finding to record); a short "Checked and fine" list; then stop.
