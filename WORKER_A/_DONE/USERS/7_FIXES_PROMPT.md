# USERS (#93) — fix round 1

To the executor of PR #93 (`feat/admin-users`, head `4daedc94`, `C:\dev\masaha\app`). The review is
`C:\dev\masaha\workspace\WORKER_A\USERS\6_REVIEW_CLAUDE_CODE.md` — read it whole. Also
`C:\dev\masaha\workspace\WORKER_A\USERS\0_CARRIED_FROM_91.md` (two carried items). Everything in
`3_EXEC_PROMPT.md` still binds: the stop rule, no result claimed unseen, a break counts only when seen red,
the report written as you go, the final-reply template with **COULD NOT RUN**.

## Fix
1. **The blocker — the table rebuilds every row on each render** (verified by the supervisor:
   `useUsersList` returns a new `spacesWords` object each render, so `UsersList`'s `useMemo`s and its
   columns change every time). Make the words stable (memoised, or read where used) so the columns keep
   their identity; a test at 1280 px that an open row dialog survives a list refresh, with its break.
2. **The dialogs live at the page, not in the row** (review finding 3 — **the owner's decision: taken**, it
   amends the plan's Stronger 7): a dialog opened from a row — above all the issued-password dialog — must
   survive the row re-rendering, the list refreshing and the layout switching between cards and table at
   1024 px. Hold the open dialog's state where the row's re-render or the layout switch cannot unmount it;
   keep the capabilities' boundaries (each feature still exports its hook and dialog). A test per case with
   its break. Update the plan's decision line in the documents where it is stated.
3. **«رجوع» and Escape while the issue request is pending** (finding 2): disabled while busy, so the new
   password is never discarded; a test and its break.
4. **The carried items:** (1) #91's unlink line flashing its placeholder after a confirmed unlink; (2) the
   focus after «تم» — `TemporaryPasswordDialog` takes an optional `returnFocus` focused from
   `onCloseAutoFocus`, **also on the owners page's created-password flow** (the review's addition), with a
   test of the path where recording the handover fails too.
5. **The documents (findings 4–6):** the rule "more than five columns become cards below 1024 px" cited to
   A7 (the design decision), not foundation §9 — in all four places; the restore bullet back under its own
   paragraph in `users.md`; `space-links.md`'s toolbar line true (two rows until 1280).
6. **The nits** the review places on this PR, as it says; the two receptionist screenshots that do not show
   the desk option and the one with two stacked dialogs — retaken after the fixes.

## How
- Fixes **fold into their commits** (`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash); bodies extended to say
  why; subjects unchanged (≤ 50).
- **Run only what the change touches** (the owner's rule): lint, typecheck, the touched test files,
  `check:classes`, `check:links`, `format:check`; one test command at a time. CI runs the rest.
- Never print a temporary password: filter that field out of any output that could hold it.
- Push with lease; CI green on the new head; `CLEAN`; the PR description updated.
- **Append** *Fix round 1* to `4_REPORT_PR1.md`; final reply in the fixed template.
