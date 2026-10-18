# Review of PR #40 (feat/recovery-pages) at c5faa76

Independent read-only review. Everything below was checked against the code at `c5faa7660a86802a2c422eba65fad46cbf809dbb`. Line numbers are at that commit.

## Findings

### 1. BLOCKER: a refused check keeps the token in React state through `AppError.cause`

- **Where:** `apps/web/src/features/auth/hooks/reset-password/useResetPasswordFlow.ts:33` and `:46-50` (`setAnswered(error)`).
- **What is wrong:** when the check is answered with a refusal (`readFailure(error) === 'error'`), the hook stores the whole `AppError` in `useState`. `toAppError` sets `cause: error`, the AxiosError (`shared/errors/toAppError.ts`). That AxiosError carries `config` and `response.config`, whose `data` is the serialised body `{"token":"…"}`. Axios's own adapters and the test `fakeAdapter.settle` both attach `config`. So after the verdict, the token stays reachable at `answered.cause.config.data` for as long as the page is mounted.
- **Why it matters:** this breaks the owner's decision that the page "keeps no copy after a verdict". It also contradicts the commit message of 4b960a3, which says "any answer drops it". It matters most for answers that are not a verdict on the link, such as a 429 or a 5xx. After those, the token is still a live credential, and the page holds it with no way to use it, since the retry is offered only when no answer came back.
- **Failure scenario:** a reader opens a valid link and the check gets a 429 or a 500. The `checkFailed` screen shows. `answered` now holds the AppError, and its `cause.config.data` holds the valid token until the reader leaves the page. Anyone inspecting the component state can read it, for example in React DevTools or a heap snapshot. The mutation cache is empty, so the existing test still passes.
- **Test gap:** `useResetPasswordFlow.component.test.tsx:126` ("…when the check refuses it, and drops the token") only checks that `getMutationCache()` is empty. The token's other copy is never examined, so the title claims more than the test proves.
- **Suggested fix:** keep only the verdict's data in state, never the AppError. For example, store `{ verdict: 'bound' } | { verdict: 'refused', type, code, requestId, retryAfterSeconds }`, or derive the `checkFailed` / `invalid` view at the moment of the answer and store that. Then extend the refusal test (and add a 429 case) to assert that nothing reachable from the hook's result contains the token.

### 2. SHOULD-FIX: a reset link opened on an already-mounted `/reset-password` is never taken out of the address or checked

- **Where:** `useResetPasswordFlow.ts:29` (`carriesLink` is frozen in the initial `useState`) and `:58-64` (the effect's dependencies are `[navigate, pathname, search, send]`, with no `hash`).
- **What is wrong:** the token is read once, at mount. A later navigation that changes only the fragment re-renders the mounted page but does not re-run the effect, and `carriesLink` stays `false`.
- **Failure scenario:**
  1. A reader is on `/reset-password` in a tab, showing "The link has expired or was already used".
  2. They paste a new emailed link (`/reset-password#token=NEW`) into that same tab.
  3. Only the fragment differs, so the browser makes a same-document navigation: no reload, and React Router updates `location.hash`.
  4. The page stays mounted, so `takeResetToken` never runs. The token stays in the address bar and in a new history entry, it is never checked, and the page keeps showing "invalid".
- **Suggested fix:** key the take-and-check on the current hash. Add `hash` from `useLocation()` to the effect's dependencies, and derive "a link is pending" from a state the effect sets (for example, set `pending` before `send`) rather than from a mount-time snapshot. Add a hook test that navigates the router to `#token=…` on the mounted page.

### 3. SHOULD-FIX: a 429 on the link's check shows no m:ss countdown

- **Where:** `useResetPasswordFlow.ts:93-104`. The test at `useResetPasswordFlow.component.test.tsx:162-178` pins the current behaviour.
- **What is wrong:** the owner decided that a 429 with `Retry-After` shows the m:ss countdown. The `checkFailed` view rebuilds `useFormFailure`'s "refused" branch by hand, so a `rate_limit` failure gets the generic "Too many attempts. Please wait a moment and try again." and the reader never sees the server's wait. Because `code` is undefined for a 429, the view also adds a request reference line, which `useFormFailure` deliberately leaves out for rate limits. This is a second, divergent copy of shared/forms' failure wording.
- **Failure scenario:** a reader trips the `PASSWORD_TOKEN` limit by reopening a link several times. The server answers 429 with `Retry-After: 600`. The page says "wait a moment" and "Open the link in your email again." The reader reopens it at once, gets another 429, and still sees no wait.
- **Suggested fix:** for `rate_limit` with `retryAfterSeconds`, render the countdown with the shared `clock` and a `secondsLeft`-style count from the answer's time. Ideally, reuse one shared failure-view helper instead of copying the refused branch, so there is still one owner of failure wording. Change the test to expect the `m:ss` wait.

### 4. NIT: the gate's exemption is exact but narrower than the route's match

- **Where:** `apps/web/src/shared/routing/guards/PasswordChangeGate.tsx:17-18`.
- **What is wrong:** the exemption is not broader than intended, which is good. But React Router matches routes case-insensitively and accepts a trailing slash, so `/reset-password/#token=…` or `/Reset-Password#token=…` renders the reset page while the gate does not exempt it.
- **Failure scenario:** a user with a pending temporary password opens a hand-edited or reformatted link such as `/reset-password/#token=T`. The gate redirects to `/change-password?next=%2Freset-password%2F%23token%3DT`, which copies the token into the return URL that the gate's rule forbids. The API's own email always uses the canonical path, so this needs an altered link.
- **Suggested fix:** compare with the router's matching semantics, for example `matchPath(RESET_PASSWORD_PATH, location.pathname) !== null` (and the same for the change page), and add a trailing-slash case to `passwordChange.component.test.tsx`. Alternatively, have the gate drop the fragment from any `next` it builds, as architecture.md already requires of any future guard.

### 5. NIT: `useForgotPassword` is named like a write

- **Where:** `apps/web/src/features/auth/hooks/forgot-password/useForgotPassword.ts:12`.
- **What is wrong:** architecture.md §3 reserves `useX` for a write. This hook is the page's screen hook: it reads the position and holds the restart choice. The actual write is `useRequestLink`. The reset side uses `useResetPasswordFlow` for the same role and `useResetPassword` for the write.
- **Suggested fix:** rename it `useForgotPasswordFlow`, along with its test, to mirror the reset side.

### 6. NIT: an intermediate commit links to a route that does not exist yet

- **Where:** d8a862e adds `SITE_PATHS.resetPassword` and the forgot page's "Set a new password" link to `/reset-password`. The route arrives only in 4b960a3.
- **What is wrong:** at d8a862e and 3a9c693, the `linkOpen` step's link lands on the site 404.
- **Suggested fix:** optional. Either accept it as part of a stacked series, or move the `linkOpen` link into the reset commit.

## Checked and found sound

- **Fragment removal:** the token is removed from the address before any request. `takeResetToken` calls `history.replaceState` before `navigate(..., {replace})` and before `send`. The position query is disabled while a link is pending. The proof is the test that records `window.location.href` at request time.
- **StrictMode:** the double effect checks the link once, because the second `takeResetToken` finds nothing. This is tested.
- **No other copies of the token:**
  - The check mutation's variables, error and cache entry go after any answer (`reset()` plus `gcTime: 0`). The offline retry keeps the token only while no answer has come, which is by design.
  - The token is in no query key or `next`, and `ResetPasswordRequest` sends the password alone (repository test).
- **Return URL:** `/reset-password` has no guard, and the gate exempts that exact pathname. `RESET_PASSWORD_PATH` is the single source for both the route and the gate, and it matches the API's `resetLink`.
- **Server as the source of the position:**
  - Both pages read `GET /recovery` on load, and every mutation writes the server's answer into the one query (`['public','recovery']`).
  - No `localStorage`, `sessionStorage` or `history.state` holds the step, the window or the email.
  - The resend countdown counts from `dataUpdatedAt`, so a return shows what is left (tested). It counts against a deadline, and a new answer restarts it.
- **Screen derivation:**
  - `forgotPasswordScreen` and `resetPasswordScreen` are pure, in `services/`, and unit-tested.
  - A failed first read shows a retry, never the email form. A position already read is kept through a later failed read.
  - The "enter the email again" choice ends when the server's standing changes. A new `forgot` always opens a fresh recovery with `canResend: true`, so the request form gives way to `sent`.
- **Resend:**
  - The resend sends no body (repository and hook tests).
  - It is offered only while `canResend`, and disabled while the window or a 429 counts down.
  - `RECOVERY_INVALID` and `RESEND_LIMIT_REACHED` re-read the position, and a 429 keeps it.
- **After the reset:**
  - The mutation's own `onSuccess` sets the position to `request` and makes one `refreshSession()` only when authenticated, so it runs even after unmount. A 401 ends the session, and another account's session is kept. All of this is tested.
  - `done` survives the session's `queryClient.clear()`.
- **Architecture:**
  - Components only render view models.
  - Pages pass links only, with no navigating callbacks.
  - The feature names no paths (the self-`navigate` in the flow carries the current pathname and search only).
  - Operation folders follow the new rule, with shared pieces at the role root.
  - `types/` files are each used by more than one file.
  - The exports (`ForgotPasswordCard`, `ResetPasswordCard`) match architecture.md §3.
  - No hook takes a test-only parameter: `enabled`, `saved`, `seconds/since` all have production callers.
- **Tests:**
  - Lanes match the suffixes: repository and services are unit tests, hooks and components are component tests.
  - No `vi.mock` is used; the seams are `fakeTransport`/`fakeAdapter`, the session hint and fake timers.
- **Copy:** the ar and en `forgotPassword` and `resetPassword` blocks have the same keys, held by `satisfies Catalogue['auth']`. No hardcoded user-facing text. Classes use semantic tokens only (`text-success`, `text-muted-foreground`, `text-caption`, …).
- **Docs:** the architecture.md §2 and §3 edits match the code: the guard table, the gate's exemption, "a credential never travels into `next`", the exports, the operation-folder rule, "`features/users` has no `services/`", and "Where a flow stands". bc93246 is a pure move of `clock`/`isolated`. Finding 29 is accurate as recorded.
