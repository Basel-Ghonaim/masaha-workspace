F-5b3a — review fixes for PR #35 (the ONE list)

An independent review ran against acee7f6 (report: C:\Users\basel\Downloads\REVIEW35_REPORT.md, for line references). The owner's analyst verified the blocker and item 5 in the code. The owner approved every decision below. Don't merge.

## Blocker — a new unit of work (NEW commit, not folded)

B1 — Drop the session's test-only seams.
- `useSignOut(dependencies = appDependencies)`, `refreshSession(dependencies)`, `restoreSession(dependencies)` and `signOut(dependencies)` take a parameter that only tests pass. The PR's documents claim none exists; that is false today.
- **Owner's decision (A): remove them now.** The functions use their real dependencies only.
- **Tests replace the platform's own seams:** the transport through `fakeTransport` / `fakeAdapter`, and the cookie through the browser's `document` (`vi.stubGlobal`, or a jsdom environment for those files). No production parameter, no `vi.mock` of modules.
- **Every existing session behaviour test keeps its assertion.** Prove it with the counts.
- **One new commit,** for example `refactor(session): drop the test-only seams`. It's a new unit, so it stays separate from the original commits.

## Should-fix (fold each into the commit it corrects)

S2 — Remove the `client` parameters nothing passes: `createAuthRepository(client = api)` and `createSessionRepository`'s `client`. Correct the lines in architecture.md (§3 and the session's section) that describe them, including "a test passes a plain fake".
S3 — Component tests re-check hook logic. Keep one rendering assertion per view state, and delete the logic re-checks the report lists:
- the countdown re-enabling the submit;
- the stale failure cleared;
- the code-to-line mapping;
- `EMAIL_TAKEN` and the server field errors.

Assert the screen-reader "met / not met" text, not the `text-destructive` class.
S4 — The `users` components get their own rendering tests in `features/users/components/` (`AccountMenu`, `AccountMenuSection`). The page test keeps only the swap between "Sign in" and the account. Remove its re-checks of `useAccount`'s pending and failure logic.
S5 — A schema issue at the root (path `[]`) makes the form send `{}`. In `schemaResolver`, turn a `null` from `toFieldErrors` into a non-empty root error, so the form never submits. Add a unit test with `.refine(() => false)`. Correct the comment.
S6 — The Evidence's "before" counts must be `origin/main`'s, not the old PR head's.
S7 — Owner's decision: keep the "Forgot password?" link. It shows the 404 until F-5b3c builds the page, as the sign-in button did in F-6b. State it in the PR's Out of scope.

## Nits (fix all; fold each)

N8 — H6: `PasswordRules` computes the rules itself. It gets the rules' views ready from a hook (`useRegisterForm`, or a small hook in `shared/forms`), and only renders them.
N9 — The `{' — '}` separator rendered as screen-reader text moves into both catalogues (`forms.passwordRules.met` / `notMet`, or as you see fit).
N10 — The landing has two owners. **Owner's decision: `RequireGuest` owns it.** The pages pass no navigating `onSuccess`. A test proves that signing in at `/login?next=/about` lands on `/about` through the guard alone. The hooks keep their `onSuccess` option for other uses.
N11 — The focus test: answer `{ password, email }` and expect `email` focused, both in the form test and in a `useServerForm` test of display order.
N12 — Add a test that unmounts before the answer arrives, then expects both the session and `onSuccess`.
N13 — Rename `shared/forms/validation/` to `services/` (plain, non-React helpers: H1's name for that role).
N14 — Move finding 25 into its own `docs(findings): record the format check trap` commit (a new commit).
N15 — Fix the stale comment in `apps/web/src/test/fakeTransport.ts` ("the hook, the endpoints").

## History and reporting

- **Fold every should-fix and nit** into the commit it corrects (fixup + autosquash). B1 and N14 are new commits. Every commit still passes on its own, and every subject is 50 characters or fewer.
- **Push** with `--force-with-lease`. **Report only once CI is green** on the new head.
- **Update the PR description:**
  - the claim about test-only parameters is now true, everywhere;
  - the Evidence counts against `origin/main`;
  - S7 in Out of scope.
- **ONE "Review fixes" comment:** the reviewed head `acee7f6`, the new head, and each id (B1, S2–S7, N8–N15) with its severity and its commit.
