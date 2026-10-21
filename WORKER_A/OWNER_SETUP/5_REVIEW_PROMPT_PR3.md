# Review — OWNER_SETUP PR 3 (`feat/owner-staff-settings`, #99), one independent reviewer

You are the **independent reviewer** of worker A's OWNER_SETUP PR 3 in Basel-Ghonaim/masaha, the item's last:
the owner's Staff page (the reception accounts: add with a one-time password and its handover at the space,
deactivate, reactivate, re-issue) and Settings page (visit pricing, reception's hand-typed prices, the debt
reminder, and the attendance card saving the capacity then the settings in one save) — opened by three
commits carried from #98's review. Claude Code executed it in another conversation; you start fresh and trust
nothing you have not seen in the code. Find the PR: `gh pr view 99 --json number,headRefOid,mergeStateStatus`.
Write the report to `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\6_REVIEW_PR3_CLAUDE_CODE.md`: first the
verdict and the five most important findings, then the rest. **Work alone — no subagents.**

## Rules
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/99/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. Another review may read in the same worktree: never switch or reset it.
  Confirm `gh pr checks 99` is green first; if a lane is red or pending, say so and stop. At the end, check
  the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report or screenshots.** Think like an attacker on
  the one-time password and like an owner whose link ends mid-session. No praise, no tool attribution, no
  project skill.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\2_PLAN.md` — **the owner's approval note at its top
binds and wins**: this PR is the plan's "PR 2" (commits 1–6, tests 21–41); **A3 replaces S4** (the dialog
takes the handover's write from its caller; `staff` owns the space's call); the refusal lines as the note
corrects them; «لا يوجد موظفون»; design issue 15 folded. The carried items `0_CARRIED_FROM_98.md` (1–8) and
#98's review. The prompt `3_EXEC_PROMPT_PR3.md`; the report `4_REPORT_PR3.md`: judge every departure (the
`RecordHandover` type and `recordAdminHandover`; the slot's `ShownPassword`; finding 90 resolved in commit 3;
the menu's order; `shared/lib`'s `wholeNumberOf`; `FormSchema`/`FailureLines` exported from `shared/forms`;
the attendance hook's file and test 36 rendering the card; the reminder's default flag as a ref;
`useMenuTriggers` copying the admin page's `useRowTriggers`) and every break.

Look hardest at:
- **The one-time password:** never in the cache (`gcTime: 0`, reset once handed on), never logged, never in
  a URL; the handover recorded on the space's route by `staff`, on the admin's by `users`; a 404 or
  `TEMPORARY_PASSWORD_NOT_PENDING` closing with its line; focus returning to the row.
- **Staff:** the consequence said before the submit; `EMAIL_HAS_ACCOUNT` on the email in the owner's words;
  a 429 counting down; the deactivation `AlertDialog` (opens on «رجوع», its action staying until the answer,
  the sessions line); reactivation at once with no success toast; the re-issue held with its reason (S10);
  every refusal of the staff routes worded (finding 90); a 404 not refreshing `['me']` (the executor's note —
  judge it against #98's carried item 7).
- **Settings:** each card's dirty, discard and "nothing changed"; the rounding pair always sent together; the
  attendance card's order (capacity, then settings), its partial line, the capacity as the new baseline, the
  values kept, only the settings re-sent (finding 96); the reminder's inserts at the caret, its two refusals,
  the default as `null`, the preview's names.
- **The carried fixes** (items 1–8 of `0_CARRIED_FROM_98.md`), and the reworded amenity refusal.
- **Design system, copy, accessibility:** semantic tokens, logical classes, names on menus and buttons,
  plurals' six Arabic forms, both catalogues.
- **The documents:** `space-links.md`, `space-settings.md`, `occupancy.md`, `users.md`,
  `frontend/architecture.md`, `overview.md`, `docs/README.md`, findings 90, 96 (resolved) and 102 — true to the
  code, one home per fact.
- Scope: `apps/web` and `docs` only. Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR of worker A's next item (PUBLIC PR 1); or a finding to record**; a short "Checked and fine" list; then stop.
