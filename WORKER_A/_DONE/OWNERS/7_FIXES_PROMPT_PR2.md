# OWNERS PR 2 (#89) — fix round 2 (short)

To the executor of fix round 1 on PR #89 (`feat/admin-add-owner`, head `a074e6d2`, `C:\dev\masaha\app`).
The review is `C:\dev\masaha\workspace\WORKER_A\OWNERS\6_REVIEW_PR2_CLAUDE_CODE.md` — read it whole. The owner
decided (2026-10-18) to fix **only what must not reach `main`** now; the rest goes to PR 3's first commit
(written into the plan's approval note — do **not** do it here). Everything in `3_EXEC_PROMPT_PR2.md` still
binds: the stop rule, no result claimed unseen, the report written as you go, the final-reply template with
**COULD NOT RUN**.

## Fix now
1. **The upgrade bound to the confirmed account (finding 1).** `submit` sends `upgradeExisting: true` only
   when the email being sent equals (normalised as `emailSchema` does) the email whose account was shown and
   found — read at submit time, not from a ref an effect fills. Test it on **what is sent**: an email edited
   after the confirm sends no upgrade; break (the comparison removed) seen red.
2. **«تم» during a rate-limit countdown** on the handover: blocked while the refusal's countdown runs, as
   the project's other forms do; a test with its break.
3. **The upgrade toast (finding 2)** names the account's own name (the one shown in the confirm, which the
   upgrade keeps), not the typed one; a test with its break.
4. **The add sheet's layout (finding 3):** the form and `SheetBody` take the classes every other form sheet
   in the project uses (find them; copy nothing new into the design system) — fields spaced, the footer at
   the bottom. A screenshot after: `shots\pr2\upgrade-confirm-ar-fixed.png` (outside the repository).
5. **`users.md` (finding 4):** the one-time password dialog's *Behaviour* and *Web decisions* sections the
   plan §9 commit 3 requires; `space-links.md`'s link to them resolves.
6. **Two findings recorded:** the confirm does not show a receptionist's front desks; «تحقّق من البريد»
   stands for three causes. Numbers **88** and **89** (this PR merges before #90, which will renumber its
   own), with their index lines.
7. **The PR description:** rewritten to the head it ends on — the review's list of what it must say.

## Not now (PR 3, commit 1 — already in the plan's approval note)
Names isolated in lines (`NamedLine`/`namedLine`/`toastNamed` used or removed), the space search's words,
`useSpaceChoices` reusing the list's row rules and badge, the English / dark / 390 / 768 screenshots.

## How
- Fixes **fold into their commits** (`--fixup` + non-interactive `--autosquash`): 2 and 5 into commit 3;
  1, 3, 4 and 6 into commit 4. Bodies extended to say why; subjects unchanged (≤ 50).
- **Run only what the change touches** (the owner's rule): lint, typecheck, the touched component/unit test
  files, `check:classes`, `check:links`, `format:check`; one test command at a time. CI runs the rest.
- Push with lease; CI green on the new head; `CLEAN`. **Append** *Fix round 2* to `4_REPORT_PR2.md`.
