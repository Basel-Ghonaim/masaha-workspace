# STAFF — fix round 1 on PR #90

To the executor that built PR #90 (`feat/space-staff`, head `ea56e225`, `C:\Users\basel\masaha-b`). The
review is `D:\masahaWorkspace\WORKER_B\STAFF\6_REVIEW_CLAUDE_CODE.md` — read it whole. The owner's decisions
below bind; everything else in `3_EXEC_PROMPT.md` still does (the stop rule, never claiming a result not
seen, the report written as you go, the final-reply template with **COULD NOT RUN**).

## The owner's decisions (2026-10-18)

1. **Finding 1 (S5's hole) is fixed in this PR, not recorded.** The server refuses to give an account whose
   temporary password is still pending any new power: the admin's **upgrade** (`POST /admin/owners` with
   `upgradeExisting`) and the admin's **link** of a person to a space both refuse it, under the account's
   lock, with a new error code `ACCOUNT_PASSWORD_PENDING` (409; follow the project's `add-error-code`
   skill: `packages/shared`, the contract, both catalogues). The admin's line — Arabic «لم يغيّر صاحب هذا
   الحساب كلمة المرور المؤقتة بعد؛ لا يُرقّى ولا يُربط حتى يدخل ويغيّرها.», English "This person hasn't
   changed their temporary password yet; the account can't be upgraded or linked until they sign in and
   change it." **First check:** list every path on `ea56e225` that adds a link or a role to an existing
   account (admin owners, admin roles, anything else) and apply the rule to each that grants power; say in
   the report which paths you found and why each is or is not covered. Tests: each refused path, with its
   break (the check removed) seen red; the race (the password issued while the upgrade waits on the lock)
   if the lock order allows a test, else said under Review Focus. `security.md`, ADR 0009's rule 4 text if
   it states the closures, `space-links.md`, and a stronger-decision line (S6) in the report.
2. **Finding 2:** a test that the staff re-issue counts under the 10-an-hour limit (S3); the limit removed
   from the re-issue route must turn it red.
3. **Finding 3:** the documents follow the code — a re-issue is allowed for **any** pending temporary
   password, not only the first (the contract, `security.md`, `space-links.md`).
4. **Finding 4:** no new code (a distinct one would tell an unauthenticated caller that an account has a
   pending password). Reword `GOOGLE_LINK_NOT_ALLOWED` in both catalogues (`auth.ts` and `errors.ts`) so it
   no longer promises a reset that may send nothing — e.g. Arabic «يوجد حساب بهذا البريد الإلكتروني. سجّل
   الدخول بكلمة مروره؛ وإن لم تعرفها فأعد تعيينها من «نسيت كلمة المرور»، أو اطلبها ممّن أنشأ حسابك.»,
   English "An account with this email already exists. Sign in with its password; if you don't know it,
   reset it under “Forgot password”, or ask whoever created your account." (fit `errors.ts`'s shorter form).
5. **The nits:** record each as a finding from **88** upward (88 is the next free number; check the index on
   the merged tree), with its index line — no code change for them.

## How

- Each fix **folds into the commit it belongs to** (`--fixup` + non-interactive `--autosquash`); bodies
  kept and extended to say why; subjects unchanged and ≤ 50; no fix commits.
- **Run only what the change touches** (the owner's rule: the full lanes passed on `ea56e225`): lint,
  typecheck, `npm run build -w @masaha/shared` first when `packages/shared` changes, the touched API test
  files (with `npm run test:api -- <files>`), the touched unit/component files, `check:links`,
  `format:check`. One test command at a time. CI runs the rest.
- Every break seen red, recorded. A short real run of the new refusal on 3321 (`masaha_b_dev`).
- Push with lease; CI green on the new head; update the PR description (Evidence, the new code, S6).
- **The merge order (the owner's):** PR #89 (worker A) merges **first**. Do not wait for it to do this
  round. Once the supervisor tells you #89 has merged: rebase on the new `main`, resolve the text conflicts
  (`docs/architecture/findings/README.md`, `docs/features/space-links.md`), add `receptionSpaces: []` to
  the `AdminUserRow` literals #89 added (`AddOwner.component.test.tsx`, `useAddOwnerForm.component.test.tsx`
  — find them all with `git grep -n "AdminUserRow" origin/main -- apps/web`, and look at any users row in
  the showcase's JSON fixtures by eye), renumber your findings if #89 took a number, then run `typecheck`
  and the touched web test files on the merged tree, push, CI green, `CLEAN`.
- **Append** *Fix round 1* to `4_REPORT_PR1.md`; final reply in the fixed template.
