F-5b3c1 — review fixes for PR #38 (the ONE list)

An independent review ran against a4e1685 (report: C:\Users\basel\Downloads\REVIEW38_REPORT.md, for line references). No blockers. The owner's analyst verified S1 in the code. Apply everything below on this branch and PR, each fix with its test. Don't merge.

## Should-fix

S1 — The reset reveals whether an address has an account.
- A forgot request for a known address stores the user's id on the recovery, and a successful reset deletes every recovery with that id (`endRecoveries` → `deleteUserRecoveries`).
- An attacker who asked for a reset of the victim's address in their own browser sees their recovery turn from `sent` to `request` when the victim resets. For an unknown address it stays `sent`. This breaks Q1.
- **Fix:** remove `endRecoveries` and `deleteUserRecoveries` (they have no other caller). The bound recoveries already end through the `reset_token_id` cascade when `endResetTokens` deletes the links, the resetting browser's included.
- **The owner's decision on the wording:** security.md's "ends every session and every recovery of the user" becomes "ends every session, and every recovery bound to a link of the user". Update any other document that says the same.
- **Test:** a second, unbound recovery for the same known address still reads `sent` after the owner's reset, exactly as for an unknown address.

S2 — The commit subject `feat(routing): gate every route on a pending change` is 51 characters. Reword it to `feat(routing): gate all routes on a pending change` (`--fixup=reword:`).

## Nits (fix all; fold each into its commit)

N3 — A race in the link check can answer 500. If a newer delivered link deletes the old one between `findValidResetToken` and the bind, the upsert fails on its foreign key (P2003). In `bindRecovery`, catch that violation and answer `RESET_TOKEN_INVALID`, as a link that went invalid. Add a test if you can provoke it deterministically; otherwise a unit test of the mapping.
N4 — The gate test "lets a guest and a user without a pending change through" passes on the guest render's leftover text. Sign in before rendering, or wait for the location to be `/spaces`, so a gate that redirects every signed-in user would fail it.
N5 — `passwordChanged` checks that someone is signed in, not who. If A signs out and B signs in before A's `/me/password` answer arrives, B's session takes A's token.
- **Fix:** the change records the user's id when it starts. `passwordChanged` applies the token only if the signed-in user is still that user.
- Keep the existing promise (a sign-out answered first stays signed out).
- Test the A-then-B case.
- Add no parameter that only tests pass: the hook that starts the mutation captures the id it already reads from the session.
N6 — Exports nothing outside their module uses:
- make `positionOf` (auth.service.ts) module-private;
- in `shared/routing/index.ts`, export `changePasswordPath` (and `signInPath`) only if something outside `shared/routing` uses it; otherwise unexport.
N7 — API test gaps:
- a resend from a checked recovery, and from one a check opened, is refused (the `linkChecked` / unbound guard in `recordResend`);
- concurrent resends at the bound of 3 cannot pass it;
- a real `/me/password` change ends a bound recovery through the cascade, not a simulated deletion.

## The Arabic (the owner's approval)

The three lines not in a design are approved as written in the PR:
- «تعذّر حفظ كلمة المرور»;
- «انتهت مدة طلب استعادة كلمة المرور. اطلب رابطًا جديدًا.»;
- «طلبت الرابط مرات كثيرة. أدخل بريدك الإلكتروني من جديد لطلب رابط آخر.»

## History and reporting

- **Fold each fix into the commit it corrects** (fixup + autosquash). Every commit still passes on its own; check one lane at a time.
- **Push** with `--force-with-lease`. **Report only once CI is green** on the new head.
- **Update the PR description:** the S1 wording, and that the Arabic is approved.
- **ONE "Review fixes" comment:** the reviewed head `a4e1685`, the new head, and each id (S1, S2, N3–N7) with its severity and commit.
- **The migration:** don't touch `masaha_dev`. Run Prisma's create-only command only once.
