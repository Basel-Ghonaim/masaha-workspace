# WI-C2 — review R1 (security) of PR #157

> Reviewer R1, read-only, on `feat/sign-in-in-place` at `305c5d3f39fd133e94f0a14b36c6a12914346fde` (CI green, CLEAN).
> Read: the owner's decisions, the analysis (I1–I15), the plan, the approval, the report, ADR 0021, and the diff
> (`git diff origin/main...HEAD`). Nothing was run: no build, test or server.

## 1. Verdict

**Mergeable after a fix round.** One should-fix (S-1) lets a held action run on another account's session. A second
(S-2) can run another tab's action, and should be fixed or recorded as a finding.

## 2. Requirements

**R1.1: no credential in a URL, storage, the held intent, a log, an error report or the query cache. PASS.**
- **The held intent** stores the kind, the space, its name, the page and the time
  (`apps/web/src/shared/routing/guest/heldIntent.ts:14-16`, `:128-131`).
- **The overlay's links carry nothing:**
  - `/privacy` (`pages/site/auth/in-place/PrivacyLine.tsx:105-110`);
  - `/reset-password` with no query and no fragment (`in-place/ForgotView.tsx:39`).
- **Only the email leaves a form** (`features/auth/hooks/useEmailReport.ts:16-18`). Passwords stay inside their
  forms.
- **The password and the Google token** stay in mutations with `gcTime: 0` (`useSignIn`, `useRegister`,
  `useGoogleSignIn.ts:29`). The query cache is never persisted (no persister in `src/`).
- **The reset page** lands through `landingPath` (`pages/site/auth/ResetPasswordPage.tsx:42-45`). The token is
  still taken out of the address as before (`useResetPasswordFlow.ts:77-83`).
- **The chunk's error boundary** (`public/SignInBody.tsx:51-67`) logs only React's caught error, which is a chunk URL.

**R1.2: D2 = B, no email stored. PASS** (nit N-3).
- `renewHeldIntent()` takes no argument (`heldIntent.ts:118-122`). Its unit test asserts the exact stored object,
  so no email key is added.
- `ForgotPasswordSteps` calls `onRequested?.()` and `onResent` with no argument (`ForgotPasswordSteps.tsx`).
- The reset page renders `<SignInForm focus="email" />` with no `defaultEmail` (`ResetPasswordPage.tsx:79`). Its
  test asserts the field is empty, `autocomplete="email"` and focused.
- A1 fills the email from the overlay's `useState('')` in `public/SignInPrompt.tsx` (memory only).
- Architecture §4's "never a credential nor the email" is true of the code.

**R1.3: every return path passes `returnUrlOf`. PASS** (nit N-2).
- **The held path:** `isIntent` → `isOwnPage` → `returnUrlOf` (`heldIntent.ts:55-65`). The unit cases refuse `//`,
  `/\`, `/.//` and `https:` (`heldIntent.unit.test.ts`). `returnUrlOf`'s own tests cover `javascript:`, `/..//` and
  `/%2E//`.
- **The reset page's landing:** `landingPath` → `returnUrlOf` (`shared/routing/landing/landingPath.ts:17`), for both
  the intent's path and the page's own `next` (`ResetPasswordPage.tsx:42-45`). Page test R3 (`/\evil.example`
  lands on `/`) fails without S1, through the return note.
- **The overlay navigates nowhere.** `useGuestIntents.ts:26-27` follows only a path checked when it was read.

**R1.4: the held action runs only where ADR 0021 / I6 / I10 allow. WEAK.**
- **What holds:**
  - The confirmation rule is unchanged: a sign-in in this tab or after a reset; never a restore
    (`heldIntent.ts:173-185`).
  - `intentMayRun` gates both runners (`useResumeFavorite.ts:15-20`, `useReportAction.ts:32-34`), and both hook
    tests fail without it.
  - The action runs once (`takeFavorite`, `takeReport`).
  - Escape, the close button, the scrim and Back call `cancel` (`useSignInPrompt.tsx:26-29`; test 8). A sign-in
    closes the overlay without `cancel` (`:13-17`).
  - The 15 minutes hold (test 15). Leaving the page drops the action, as before (`guestLeaving.ts:23-29`).
- **What fails:**
  - **A sign-out does not drop the in-memory hold** (S-1).
  - **Another tab's action can be confirmed by this tab's sign-in** (S-2).

**R1.5: A1 carries no secret, and a forged event acts on nothing. PASS.**
- The listener reads only the key and that a value is present (`shared/routing/guest/recoveryElsewhere.ts:9-12`).
  The value is a timestamp.
- The listener only switches the view to `changed` (`in-place/InPlaceSignIn.tsx:64-69`). It sends nothing and signs
  nobody in. The password must still be typed.
- A same-origin write of `masaha.recoveredAt` can only show the sign-in form with the notice. It gains nothing a
  same-origin script did not already have.
- Tested: the unit tests (another key, a removal, a cleared storage) and overlay test 11 (another key changes
  nothing).

**R1.6: Google in the overlay. PASS.**
- **The credential handler is unchanged** (`features/auth/services/googleIdentity.ts:93-98`). Sign-in and register
  share one `ContinueWithGoogle` at one place in the tree (`InPlaceSignIn.tsx:73-89`; test 4 checks it is the same
  node).
- **The handler is unset when the button unmounts** (the forgot or changed view, or closing). A credential arriving
  after the overlay closes is dropped.
- **No public page has another Google button.** `@features/auth` is imported only under `pages/site/auth/` and
  account settings.
- **Every failure is shown, none retried:**
  - failures go through the unchanged `useGoogleFailure`;
  - the extra action appears only for `GOOGLE_LINK_NOT_ALLOWED` (`useContinueWithGoogle.ts:24`); the component
    test uses `GOOGLE_TOKEN_INVALID` as the negative case;
  - mutations have `retry: false` (`shared/api/query/queryClient.ts:14,25`); the transport retries only GETs and
    requests with an Idempotency-Key, never a 4xx (`interceptors/retry.ts`).
- **Not proven:** Google's real credential coming back in a browser. The localhost origin is not authorised, so
  only `fakeGoogle` covers it. The report says so.

**R1.7: rate limits and errors reach the user; nothing retried; busy blocks double submits. PASS** (nit N-1).
- The forms are the pages' forms: fields disabled while submitting, the submit blocked during the countdown, and
  `useRefusalView`'s clock.
- Test 6: a 429 with `Retry-After: 300` shows the 5:00 countdown, disables the submit, and nothing more is sent.
- `useSignInBusy` covers all five keyed mutations (`features/auth/hooks/useSignInBusy.ts`; a test per mutation).
  It feeds the dialog's `busy`; test 9 shows Escape, Back and the close button held.

**R1.8: the lazy chunk and its `check:build` rule. PASS.**
- `apps/web/scripts/signInChunk.ts` names the chunk. The `vite.config.ts` group builds it, and `signInProblems`
  checks it (`checkBuild.ts:196-214`), exiting 1 on failure (`:325`).
- Five unit cases each reach a branch: no chunk, the first download, a page reaching it deeply, the shell, and an
  auth page allowed.
- **CI's `check:build` on `305c5d3f`** printed the rule's success line, with `sign-in-*.js` at 21.22 kB.
- `SignInBody.tsx` reaches the body only through `import()`. Its other import is `import type`.
- The break the report says it saw fail, a static import in `SignInPrompt.tsx`, is consistent with the rule. I did
  not run it (read-only).

**R1.9: no new dependency, API, cookie or CORS change; no weakened test. PASS.**
- The diff touches only `apps/web/**` and `docs/**`: no `package*.json`, `apps/api` or `packages/shared`.
- **The removed tests are D6's:**
  - the `it.each` "leaves through «$link»" (the links no longer exist);
  - one `SpacePage` assertion;
  - the reset page's "link after the set" assertions, replaced by R1–R4.
- **D1's rewrites are as strict as before:** exact lines instead of the checklist states.
- No security assertion was loosened. New negative cases were added: S1, the refusal's action limited to its code,
  and a storage event for another key.

## 3. Findings

### Should-fix

**S-1 (R1.4): a held action survives a sign-out in memory and runs for the next account.**
- **Scenario:**
  1. A guest presses the heart on `/spaces/A`.
  2. They sign in over the page with an account that has a temporary password. The gate sends them to
     `/change-password?next=/spaces/A`.
  3. They press «تسجيل الخروج» and land on `/login` (`RequirePasswordChange.tsx:25`).
  4. Within 15 minutes another person signs in there. A visitor lands on `/`.
  5. `SiteLayout`'s `ResumeFavorite` sees `intentMayRun` true, and `takeFavorite()` returns A.
- **Result:** `POST /me/favorites/A` is sent on the second account, with its toast. The report variant: the report
  dialog opens by itself for the next account on `/spaces/A`.
- **Cause:**
  - A session end drops only the stored copy (`heldIntent.ts:186`).
  - The features' memory holds (`favoriteIntent.ts:22,61`, `reportIntent.ts:21,59`) are dropped only when a guest
    lands on another page, or when they expire.
  - Nothing in between is a guest landing on the site shell, so neither drop happens.
- **Pre-existing (#132)?** Yes, through the old round trip. But this PR makes the wait a stated rule (S2,
  `intentMayRun`), and architecture §4 now says "let go … on a sign-out", which is not true of the memory holds. The
  worker's §6 note (a held report surviving a sign-out) has the same cause.
- **Fix:**
  - In `shared/routing/guest/guestLeaving.ts`, add `onSessionEnded(() => { for (const letGo of listeners) letGo(); })`.
    One line covers both features, and `shared/routing` already imports `@shared/session`.
  - Add one component test: hold → `establishSession` with `mustChangePassword` → `endSession` → another user's
    `establishSession` → nothing posted.

**S-2 (R1.4): "the tab that held it" is a stale per-tab flag, not this tab's intent.**
- **Scenario:**
  1. Tab X holds favourite A.
  2. Tab Y in the same browser holds B, overwriting `masaha.heldIntent`.
  3. X signs in over its page. `here` is true (`heldIntent.ts:41,176`), so `takeStored` returns B.
- **Result:**
  - X's shell navigates to `/spaces/B` (`useGuestIntents.ts:26-27`).
  - `keep(B)` replaces A in memory (`favoriteIntent.ts:64-66`). B is saved and A is lost.
  - ADR 0021 point 2 ("stays on the page") is broken.
  - `SentNote` and the reset page's note name B in X.
- **Pre-existing (#132), with the round trip.** Acceptable as a recorded finding if the owner prefers.
- **Fix:**
  - Stamp the stored intent with a per-tab id (or remember the `at` this tab wrote, updated by `renewHeldIntent`).
  - Set `here` only when the stored intent is this tab's.
  - Add a unit case: two holds from different "tabs", and a sign-in in the first runs nothing stored.

### Nits

- **N-1 (R1.7):** while a password sign-in or register is pending, Google's button and the view switches stay live.
  - `ContinueWithGoogle.tsx:32` makes the button inert only on its own busy state, so two sign-ins can race,
    possibly as two accounts.
  - The pages have the same behaviour today.
  - Fix: in the overlay, make it inert while `useSignInBusy()` is true.
- **N-2 (R1.3):** `isOwnPage` checks the path but keeps and follows the raw string (`heldIntent.ts:55-60,181`),
  while `next` everywhere else follows `returnUrlOf`'s normalised result.
  - No exploit: it is the same parser, and a cross-origin `replaceState` throws.
  - Storing or returning the normalised value would make "read as `next`" literally true.
- **N-3 (R1.2):** no test asserts that the overlay's request leaves the email out of storage. Fix: one line in test
  10, `expect(localStorage.getItem('masaha.heldIntent')).not.toContain('sara@')`.
- **N-4 (R1.4):** the overlay's temporary-password test passes without `intentMayRun`, because the gate unmounts the
  shell first (the report's §4 says so). The rule is proven by the two hook tests only. Acceptable.

### Outside R1 (one line)

- **For R2:** the reset page computes its return note once, as it opens (`ResetPasswordPage.tsx:29`). If the waiting
  tab's overlay is closed meanwhile, the stored action is dropped: the done step still promises the return, but the
  sign-in lands by role.
