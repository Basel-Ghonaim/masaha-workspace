# OWNERS PR 3 (#91) — fix round 1

To the executor of PR #91 (`feat/admin-owner-links`, head `54dae070`, `C:\dev\masaha\app`). The review is
`C:\dev\masaha\workspace\WORKER_A\OWNERS\6_REVIEW_PR3_CLAUDE_CODE.md` — read it whole. Everything in
`3_EXEC_PROMPT_PR3.md` still binds: the stop rule, no result claimed unseen, a break counts only when seen
red, the report written as you go, the final-reply template with **COULD NOT RUN**.

## Fix
1. **The unlink dialog words its consequence only from a fresh read (finding 1, verified by the
   supervisor:** `useUnlinkOwnerDialog` reads `owners.isPending`, which is false while a cached answer
   refetches). The consequence is "reading" and «فك الربط» disabled until the read of **this** opening
   has arrived — e.g. `gcTime: 0` on `useSpaceOwnersQuery`, or treating a refetch as reading; choose the
   simpler that holds. A test that opens the dialog twice with the owners changed between, and its break.
2. **Focus after a successful link or unlink from the editor (finding 2):** when the opener is gone, focus
   moves to a stable element (the notice, or what the review proposes); a test per case (link, last
   unlink, one of several), each with its break.
3. **The link dialog's verification (finding 4):** if the fresh data needed is already in hand, word the
   line and the toast from the space's current state, not the state at opening/choice; if it needs a new
   read, record a finding instead — say which.
4. **`users.md` (finding 5):** the history line for commit 1's change to the password dialog.
5. **The nits the review places on this PR:** «ربط مالك» reachable by keyboard with its reason (as the
   project's other disabled-with-reason actions do); the refusal that says «اختر غيره» where nothing can be
   chosen; the dialog-state type declared once. Record as findings (next free numbers from the index on
   the latest `origin/main`): the receptionist shown as «مستخدم» in the person search; the editor's
   unsaved rule written in two documents, unless you can keep one home in this round.
6. **Screenshots (finding 3):** the missing ones — Arabic at 390 and 768, English at 1440 — of the link and
   unlink dialogs and the editor's notice; or untick what the PR description claims. Into `shots\pr3\`.

## How
- Fixes **fold into their commits** (`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash); bodies extended to say
  why; subjects unchanged (≤ 50).
- **Run only what the change touches** (the owner's rule): lint, typecheck, the touched test files,
  `check:classes`, `check:links`, `format:check`; one test command at a time. CI runs the rest.
- Push with lease; CI green on the new head; `CLEAN`; the PR description updated.
- **Append** *Fix round 1* to `4_REPORT_PR3.md`; final reply in the fixed template.
