# OWNERS PR 2 (#89) — complete it before review

You are the executor of PR **#89** (`feat/admin-add-owner`, head `8548308e`) in `C:\dev\masaha\app`.
The supervisor checked it against the plan before sending it to review and found it **incomplete**. The
review waits for this round. Read first: `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` (the approval note
at its top, §9 *PR 2*, §10 *PR 2*) and your report `4_REPORT_PR2.md`. Everything in
`3_EXEC_PROMPT_PR2.md` still binds — its stop rule and its final-reply template above all.

## What is missing (verified in the code at `8548308e`)

1. **The security step of the approval note is not built.** After `EMAIL_HAS_ACCOUNT` the form only swaps the
   notice to `hasAccount` / `willUpgrade` (`useAddOwnerForm.ts:95–107`). The note requires that the upgrade
   step **show whose account it is before the admin confirms**: the account's name, when it joined and its
   current spaces, read with `GET /admin/users?q=<the email>` (PR 1's users list, reused, no API change),
   with the line «تأكّد أنه الشخص المقصود: سيصبح مالكًا لهذه المساحة» (and its English). **With no exact
   email match in that read, no upgrade is offered.** A mistyped email must never become an owner by one
   click. Words in both catalogues.
2. **Most of §10 *PR 2*'s tests are absent.** The PR changes three test files only (`Combobox`,
   `lineParts`, `usersRepository`). Missing, each with its planned title and its break seen red:
   `useTemporaryPasswordDialog.component.test.tsx` (6 tests), `TemporaryPasswordDialog.component.test.tsx`
   (5), `spaceLinksRepository.unit.test.ts` (adds an owner · finds up to fifty spaces),
   `useAddOwnerForm.component.test.tsx` (6, the `it.each` included), `AddOwner.component.test.tsx` (4),
   `routes.component.test.tsx` (offers «Add owner» above the owners list — your departure 5 is **not**
   accepted: a real run does not replace a planned test).
   **Plus the approval note's test:** the upgrade confirm shows the matched account; with no exact email
   match, no upgrade is offered — each with a break (the read skipped / the match not exact) seen red.
3. **The report claims breaks that were never made.** §3 lists repository breaks "verified by passing
   tests" for calls that have no test. Correct §3: a break counts only when you saw it red.

## How

- Each fix **folds into its commit** (`git commit --fixup` + `git rebase -i --autosquash` non-interactively,
  e.g. `GIT_SEQUENCE_EDITOR=true`): the dialog's tests into commit 3; the security step, its test and the
  rest into commit 4. Bodies kept and extended to say why; subjects unchanged (≤ 50); no fix commits.
- Docs: `space-links.md` (*Behaviour*, *Web decisions*) states the account check before the upgrade.
- Run what the change touches: lint, typecheck, `test:component` and `test:unit` (one at a time), the
  build with `NODE_ENV=production` then `check:build`, `check:classes`, `format:check`, `check:links`.
- Real run of the new step: an existing user's email shows their name, joined date and spaces before
  «ترقية وربط»; a screenshot to `shots\pr2\upgrade-confirm-ar.png` (moved out of the repository).
- Force-push with lease, CI green on the new head, `CLEAN`.
- **Append** a section *Fix round 1* to `4_REPORT_PR2.md` (do not rewrite history in it; correct §3 in place
  with a note). Final reply in the fixed template, with **COULD NOT RUN**.
