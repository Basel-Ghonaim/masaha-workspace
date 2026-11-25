# WI-C2 — the fix round for PR #157 (one round, every point; the owner's rule C11)

Both reviews say **mergeable after a fix round**, no blocker: `6_REVIEW_R1.md` (security) and `6_REVIEW_R2.md`
(experience and the PR). Read both whole first. Then fold every fix below into the commit it belongs to (`--fixup` +
autosquash on the same base, a `backup/sign-in-in-place-pre-fix` branch first), run the full local verification, push
with `--force-with-lease` pinned to `305c5d3f39fd133e94f0a14b36c6a12914346fde`, post one "Review fixes" comment on the
PR listing each point and its commit, update the PR description if it changes, wait for green CI and `CLEAN`, and
add a "Fix round" section to `4_REPORT.md`. Never merge. Run heavy commands in the foreground. **Prove each code fix
with a test seen failing first.**

## Security (R1) — the owner's condition is "no security risk"
1. **S-1** A held action survives a sign-out in memory and runs for the next account. Fix as R1 says:
   `onSessionEnded` lets every memory hold go (`shared/routing/guest/guestLeaving.ts`), plus the component test R1
   describes (hold → temporary-password session → sign out → another user's session → nothing posted, no report
   dialog). Make architecture §4's "let go … on a sign-out" true of the memory holds.
2. **S-2** "The tab that held it" is a stale per-tab flag: another tab's action can run here. **Fix it (not a
   finding):** stamp the stored intent with this tab's id (or the `at` this tab wrote, renewed by `renewHeldIntent`),
   confirm only this tab's intent, and add the two-tab unit case. ADR 0021 point 2 (stays on the page) must hold.
3. **N-1** While a password sign-in or register is pending, Google's button and the view switches stay live: make them
   inert in the overlay while `useSignInBusy()` is true; one assertion.
4. **N-2** Store / return the normalised path `returnUrlOf` yields for the held intent, so "read as `next`" is literally
   true.
5. **N-3** One assertion that the overlay's request leaves the e-mail out of `masaha.heldIntent`.
6. **N-4** Accepted as is (the rule is proven by the hook tests): say so in the report.

## Experience (R2)
7. **Focus on the link sent:** focus the title when the forgot view's step changes (`sent`, `linkOpen`, and the
   recovery's and the chunk's retries); `toHaveFocus()` in test 10.
8. **The reset page's held-favourite test:** also expect `post /me/favorites/7` once.
9. **`docs/features/users.md:42`:** "its rules checklist" → the policy's one line; the two stale JSDoc lines
   (`RegisterForm.tsx:13`, `ResetPasswordForm.tsx:8`); architecture `:139` names the reset page as a caller of
   `landingPath`.
10. **The plan's Review Focus checks not done:** in Chrome (3323 / 5323, `masaha_dev`), run (a) the temporary
    password's history after an in-place sign-in (the gate's replace against the overlay's step back — fix it if the
    history is wrong), (b) the overlay over a card's heart on Home and the directory, focus back on that heart after
    the grid re-renders, (c) slow 3G and offline: the loading line and the chunk's retry. Report each.
11. **Promises read once:** re-read `heldIntentPreview()` when the reset page's done step mounts and when the link-sent
    note shows; drop the line when it returns null.
12. **`site.signInPrompt.loadFailed`:** keep it (the supervisor approves the wording on the owner's behalf only if he
    has not answered; it is listed for him).
13. **Commit `07e89a1d`'s `auth.md`** cites the `sign-in` chunk that arrives in `305c5d3f`: move the line to that
    commit.
14. **Record as findings (no code here):** the language switch on sign-in over the page (R2 nit 1, existing
    behaviour); `PASSWORD_RULES` used only by its test and the stale checklist comments in `users` (nit 5);
    `ForgotPasswordSteps` repeating `ForgotPasswordCard`'s switch (nit 6); «نسيت كلمة المرور؟» at the field's end vs
    the picture's start (nit 7). Next free numbers after 230.
15. **The field error «كلمة المرور لا تستوفي الشروط أدناه»** repeats the one line: left as is unless the owner says
    otherwise (listed for him).
