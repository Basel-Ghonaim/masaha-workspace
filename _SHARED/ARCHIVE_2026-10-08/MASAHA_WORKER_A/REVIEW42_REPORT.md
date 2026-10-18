# Review — PR #42 (feat/google-sign-in), head 4e525c3, base 315aa52

**Verdict:** I found no blocker. Three should-fix items and a few nits. The credential handling, the toast order and the architecture placement are sound.

## Findings (most severe first)

### 1. should-fix: the Google ID token stays in React Query's mutation state, and in the cache for 5 minutes after the page has gone
- **Where:** `apps/web/src/features/auth/hooks/google-sign-in/useContinueWithGoogle.ts:16` (`signIn.mutate({ idToken, language })`) and `useGoogleSignIn.ts:21` (`useMutation` with no `gcTime`).
- **What:** React Query stores the variables of every mutation (`{ idToken, language }`) in its state. A failed request also keeps the token in `error.cause.config.data`, because `AppError.cause` holds the AxiosError. The QueryClient (`shared/api/query/queryClient.ts`) sets no mutation `gcTime`, so the default of 5 minutes applies. A sign-in clears nothing (§3 "The cache"), so after the redirect the mutation, with its token, stays in `queryClient.getMutationCache()` for 5 minutes. The item required that the token is not kept after it is sent.
- **Scenario:** the person signs in with Google and lands on `/`. For the next 5 minutes, any script on the origin (an XSS, a malicious extension) can read `getMutationCache().getAll()[0].state.variables.idToken`. The API does not make the token single-use and checks no nonce (commit 8c8be17 says so). For the rest of the token's life (about 1 h), anyone holding it can replay it to `POST /auth/google` from another machine and get a full session there, with a refresh cookie. While a failure is shown (503, network), the token also stays in `signIn.variables` and `signIn.error.cause` until the page unmounts.
- **Fix:** set `gcTime: 0` on `useGoogleSignIn`'s mutation, so it leaves the cache as soon as no observer holds it. That is right after the redirect on success, or when the person leaves after a failure. The same pattern holds the password in `useSignIn`, `useRegister` and `useChangePassword`, and the request body in `AppError.cause`. That part is outside this item, so record it as a finding rather than fixing it here.

### 2. should-fix: the showcase preview now shows every toast twice
- **Where:** `apps/web/src/app/providers.tsx:28` (the new root `Toaster`), together with `apps/web/src/pages/showcase/ShowcasePreview.tsx:39`, which is unchanged and still mounts its own `Toaster`.
- **What:** the showcase routes render inside `App` → `AppProviders`, so `/__showcase/preview` now has two `<Toaster>` elements. In sonner 2.0.8, a Toaster with no `id` renders every toast that has no `toasterId` (`dist/index.mjs:989`), so both Toasters render every toast. The PR also changed the docblock in `Toast.tsx` to "Mount one, at the app's root", and the showcase now breaks that.
- **Scenario:** in the dev showcase's toast section, "Success toast" appears twice: once at the bottom end, in the preview's language and direction, and once at the bottom centre, labelled and directed by the app's own language. Visual review of the toast component becomes unreliable.
- **Fix:** either remove the preview's Toaster, or give it an `id` and send the showcase's sample toasts with `toasterId`. The owner should choose, because the preview's Toaster follows the preview's language and direction settings and the root Toaster does not.

### 3. should-fix: nothing proves that a credential arriving after unmount is dropped, or that there is only one handler
- **Where:** `apps/web/src/features/auth/services/googleIdentity.ts:64,75-78` and `useGoogleButton.ts` (the effect that calls `onGoogleCredential`). No test covers them: there is no `unmount` in `useGoogleButton.component.test.tsx` or `useContinueWithGoogle.component.test.tsx`.
- **What:** the code is correct today. Cleanup clears `credentialHandler`, and the identity check keeps a newer page's handler. But this is the item's priority-1 security property, and no proof covers it. Two scenarios are uncovered: (a) the person chooses an account and the page unmounts before Google's callback, so no request may be sent; (b) moving from `/login` to `/register` must leave exactly one live handler, with `initialize` called once across both mounts (the WeakSet is only proven within one mount).
- **Failure it would catch:** a refactor that drops the `credentialHandler === handler` check, or forgets `stop()`. Then a late credential is sent from a page that has gone, or the new page's handler is cleared, and Google's button silently does nothing.
- **Fix:** in `useContinueWithGoogle.component.test.tsx`, unmount and then `google.choose(...)`, and expect no request. Also mount, unmount and mount again on the same fake, and expect `configs` to have length 1 and the second mount's credential to be sent.

### 4. nit: other decisions with no proof
- G6's own line for 422 (`validation`) has no test. The `it.each` in `useContinueWithGoogle.component.test.tsx` covers 409, 401, 403, 503 and the network failure, but not 422 or timeout.
- G1's "full width up to 400px" has no test. `componentSetup.ts` stubs ResizeObserver, so the `width` option is never exercised.
- G3's "worded in the account's language" is proven for the Google linked toast only. Nothing proves it for `useRegister`'s welcome, although that is the same pattern.
- Fix: add the 422 case to the `it.each`. A width test needs a ResizeObserver stub that reports a size, so add one only if the owner wants this proven.

### 5. nit: the button is drawn again on resizes that cannot change it
- **Where:** `useGoogleButton.ts:59` stores the raw width, while `:77` caps it at 400.
- **What:** below `md`, the card is `w-full`, so its content can be wider than 400px. Every pixel of resize then changes `width`, removes Google's iframe and draws a new one, which fetches from accounts.google.com again, even though the option stays at 400.
- **Fix:** cap the width in the observer, `setWidth(Math.min(Math.round(entry.contentRect.width), MAX_WIDTH))`, so widths above 400 cause no redraw.

### 6. nit: two stale lines in the architecture doc
- `docs/frontend/architecture.md:193`: the toast bullet names `useRegister` and `useChangePassword` but not `useGoogleSignIn`'s linked toast, which follows the same rule.
- `docs/frontend/architecture.md:177`: it still says `AuthRepository { login, register }`, but the interface now also has `google`.

## Verified OK
- **The token is never stored by the code itself:** not in `useState`, refs or closures. `credential.current` holds the callback, not the token. The module keeps only the handler, and nothing logs the token. A late credential is dropped: cleanup clears the handler, and the identity check means an old page cannot clear a new page's handler.
- **`initialize` runs once per loaded script (WeakSet), StrictMode included.** With two loaders running at once, the first continuation initialises and the second skips. Late results go through a `current` guard.
- **The script:** it is not appended without a client id (proven). An already-pending script is reused. A failed script is removed, so a later visit tries again, and its failure has its own line. Closing Google's window shows nothing.
- **Toast order:** all three hooks fire the toast after `establishSession` or `passwordChanged`, with `currentCopy()` read at that moment. `establishSession` notifies `app/session.ts`, which calls `setLanguage` synchronously, so the order is right. The linked toast appears only when `linked`, lasts 10 s and has a description. `linked` is removed from the session before it is stored. The welcome uses `isolated(name)`. No welcome follows a Google sign-in (finding 32).
- **Busy:** the button is busy and `inert` while pending and during the 429 countdown, through `useRefusalView`. Google's own lines win only over a `refused` view. A 503 has no code, so `service_unavailable` is the key that applies, which matches `auth.service.ts:206`. The 401 from `/auth/google` does not trigger a refresh, because `refreshOn401` skips `/auth/`.
- **Redraws:** the button is drawn again on a theme change (`preferences.theme` is the theme shown, so `system` and dark work) and on a language change. The ResizeObserver is disconnected and `replaceChildren` runs on cleanup.
- **Architecture:** the hooks prepare and `ContinueWithGoogle` only renders, receiving no AppError. The only new export is `ContinueWithGoogle` (and its props type). There are no routes in the feature, and the page passes only a divider slot (A1). The repository call is in `authRepository`. `googleIdentity.ts` in `services/` has a precedent in `services/takeResetToken.ts`, which also has browser side effects, so its placement is acceptable. `types/GoogleIdentity.ts` is used by two files.
- **Tests:** the tests are in the right lanes (repository in unit; hooks and component in component). The seams are `fakeTransport`, `vi.stubGlobal('google')` and `vi.stubEnv`, with no `vi.mock`. No parameter exists only for tests, and the test titles are honest.
- **Copy and styling:** both catalogues have the same keys (Arabic is checked by `satisfies Catalogue`). There is no hardcoded user-facing text. `OrDivider` uses semantic tokens only.
- **Commits:** all three subjects are 50 characters or fewer. The commits are atomic, with no tool attribution.
- **Docs:** `.env.example` (and `.env` stays gitignored), setup.md › The web, findings 32 and 33 (their links resolve), the exports in architecture.md, foundation.md and the overview's Built section all match the code. The overview's entry relies on the owner's manual check of the real Google flow. The known locale issue is excluded, as agreed.

## Tokens used
About 95k.
