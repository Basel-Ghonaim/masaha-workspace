## Review fixes

One round, every point of R1 (security) and R2 (experience). Each fix is folded into its commit (fixup and autosquash; the pre-fix head is kept on `backup/sign-in-in-place-pre-fix`). Each code fix was seen failing first. The new head is `ad0ba75e`.

**Security (R1)**
- **S-1, a held action surviving a sign-out** (commit `7100c799`, *feat(site)*): `shared/routing/guest/guestLeaving.ts` lets every memory hold go on `onSessionEnded`.
  - Two hook tests: hold → a temporary-password session → sign out → another account's session → no `post /me/favorites/7`, and no report dialog. Both failed before the fix.
  - Architecture §4's "let go … on a sign-out" is now true of the memory holds.
- **S-2, another tab's action run here** (`28f9d4e6`, *feat(auth)*): the stored intent carries this tab's mark (`tab`), and a sign-in confirms only its own (or a recovery's, as before). The `heldHere` flag is gone.
  - `heldIntentPreview('tab')` reads only this tab's hold; the link sent's note uses it.
  - Unit cases: another tab's hold over this one runs nothing and leads nowhere; this tab's own still runs; the preview by tab. ADR 0021 point 2 holds.
- **N-1, two sign-ins racing** (`7100c799`): while `useSignInBusy()` is true, Google's block is `inert` and the view switches (`Create account`, `Forgot password?`, `Sign in with this email`, `Sign in`, «العودة إلى تسجيل الدخول») are disabled. One component test.
- **N-2, the path followed** (`28f9d4e6`): the held page is stored as read, and returned and followed as `returnUrlOf` yields it (`/spaces/./noor-hub` → `/spaces/noor-hub`). One unit case.
- **N-3, no e-mail in storage** (`7100c799`): test 10 asserts `masaha.heldIntent` never contains the typed e-mail.
- **N-4** accepted as is: the rule is proven by the two hook tests.

**Experience (R2)**
1. **Focus on the link sent** (`7100c799`): the focus goes to the title whenever the forgotten password's step changes, except back to the request, where the field takes it (C3). That covers `sent`, `linkOpen` and the recovery's retry. The chunk's «Try again» also focuses the title. Test 10 asserts `toHaveFocus()` on «Check your email»; it failed before.
2. **The reset page's held favourite** (`28f9d4e6`): the test also expects `post /me/favorites/7` once.
3. **Documents:**
   - `users.md:42` now says the policy's line (`0c78eb6e`);
   - the `RegisterForm` comment (`7100c799`) and the `ResetPasswordForm` comment (`28f9d4e6`) say the one line;
   - architecture `:139` names the reset page as a caller of `landingPath` (`28f9d4e6`).
4. **The Review Focus checks, in Chrome** (3323 / 5323, `masaha_dev`):
   - **(a) A temporary password's history — a bug, fixed.**
     - What happened: after a sign-in over the page with a temporary password, the gate's redirect waited for the lazy change page, and the overlay's step back interrupted it. It landed on the page's own entry, with the same router key the overlay's entry had copied.
     - The result: the router rested on `/spaces/pal-hub` with the gate rendering nothing, a blank page.
     - The fix (`7100c799`): `PasswordChangeGate` now redirects whenever the router rests idle away from the change, not once per element.
     - Proven by a new gate test with a browser router, an entry pushed as the overlay pushes it, and Back while the change page loads; it failed before the fix.
     - In Chrome after the fix: the change page shows within ~70 ms of the step back; Back from it reaches the earlier page, which the gate redirects; no blank page.
     - The demo reception account's password was set back to the demo one.
   - **(b) Home and the directory** at 390 and 1440: the overlay over a card's heart; after the sign-in the page stays, the heart is saved, and the focus is on that same heart after the grid re-renders.
   - **(c) Slow 3G** (2 s latency, 500 kb/s): the overlay opens at once with its title (focused) and the loading line. **Offline:** the line and «Try again»; back online, «Try again» loads the forms and the focus goes to the title (twice, repeatable).
5. **The promises read again** (`28f9d4e6`): the reset page reads the held action again once the password is set, so a test that lets it go meanwhile sees no return line (it failed before). The link sent's note reads it as it shows, this tab's only.
6. **`site.signInPrompt.loadFailed`:** kept, listed for the owner.
7. **The `sign-in` chunk line** in `auth.md` moved from commit B to commit D (`ad0ba75e`), where the chunk arrives.
8. **Findings recorded** (`7100c799`):
   - **231:** a sign-in over the page switches the page to the account's language;
   - **232:** `PASSWORD_RULES` is read only by its test, and two `users` comments still say "checklist";
   - **233:** `ForgotPasswordSteps` repeats `ForgotPasswordCard`'s switch;
   - **234:** «نسيت كلمة المرور؟» sits at the field's end, not its start.
9. **The field error «…الشروط أدناه»:** left as is, listed for the owner.

**Run locally on `ad0ba75e`** (through the grant, in the foreground):
- `format:check`, `check:classes`, `check:links`, `check:conflicts`, `lint` and `typecheck` are clean.
- `test:unit`: web 1,446, API 924, shared 384.
- `test:component`: 2,261 in 353 files.
- `build` (`NODE_ENV=production`) and `check:build` are clean.
- `test:api` is left to CI.
