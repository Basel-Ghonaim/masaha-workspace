F-5b2 — review fixes for PR #33 (the ONE list)

Two independent reviews ran against 89b70f1 (the session's correctness and security; conformance and documents). The owner's analyst verified B1 and O1 in the code. CodeRabbit posted only a summary, with nothing to act on. Apply everything below on this branch and PR, each fix with its test. Don't merge.

## Owner decision

O1 — Amend J4: a cross-site 403 must not sign the user out.
- Today `endsSession` (services/refresh.ts) ends the session on any 403. But the API's cross-site refusal (`refuseCrossSite`: a foreign `Origin`, or `Sec-Fetch-Site: cross-site`) answers 403 with no code and keeps the cookies (api-contract §5 › refresh; security.md › Tokens and cookies). The web then clears the hint and goes `anonymous` while the refresh cookie is still valid. It happens, for example, on `127.0.0.1` instead of `localhost`, or on a preview URL.
- The rule becomes: **a refresh ends the session only on 401, or on 403 with `code === 'ACCOUNT_SUSPENDED'`.** Any other 403 keeps the session: at restore, `unreachable` with reason `error`; mid-session, it rejects and leaves the user signed in.
- Tests: a 403 `ACCOUNT_SUSPENDED` ends the session, and a 403 with no code doesn't, both at restore and mid-session. Update architecture.md §4 and system-overview.md (its refresh step) to say this.

## Blocker (verified)

B1 — `safeReturnUrl` can return a protocol-relative URL. `new URL('/.//evil.example', SITE)` keeps the site's origin but has the pathname `//evil.example`, so `/login?next=%2F.%2F%2Fevil.example` (also `/..//x`, `/%2E//x`) passes the origin check and returns `//evil.example`. That is what the function's own comment says it never returns.
- Fix: after resolving, also refuse when `url.pathname` starts with `//` (or with `/\`), and return `/`.
- Tests: add `/.//x`, `/..//x` and `/%2E//x` to the existing `it.each`, plus a guard test where `RequireGuest` with an unsafe `next` lands on `/`.

## Should-fix

S1 — The new §1 rule is contradicted by existing code, and gives no reason.
- "Inner folders have no `index.ts`" is false for the design-system layer (an `index.ts` per component and in `icons/`, owned by foundation §3) and for the copy's per-language catalogues.
- The rule doesn't say what may stay at a module's root, yet `model.ts`, `store.ts`, `envelope.ts` and `returnUrl.ts` do.
- Fix §1:
  - exempt the design-system layer (foundation §3 owns its layout) and the copy's language folders;
  - say that a module's core (its model, its store, a helper every role uses) may stay at the root;
  - add a one-clause why: so a module's roles read from its tree, and its surface stays one file.
  - Keep it to two or three sentences.

S2 — A listener that throws undoes a transition. Listeners run inline: an established-listener that throws during a restore makes the restore reject, which overwrites `authenticated` with `unreachable` and spends another refresh on Retry. An ended-listener that throws makes `signOut` reject after the session has already ended.
- Fix: run each listener in isolation, so a listener's error never undoes the store's transition. Report it so it isn't swallowed silently: rethrow it asynchronously, or `console.error` it. State which in a comment.
- Test both directions.

S3 — A refresh in flight can resurrect a signed-out session. A transport refresh starts; the user signs out; if the logout answer arrives first, the refresh's late success re-establishes the session.
- Fix: a session generation number that `endSession` increments; a refresh drops its result if the generation changed while it was in flight.
- Test the out-of-order case.

S4 — `LockIcon` is missing from the showcase's icons section (`IconsSection.tsx`, the non-mirrored group). Add it, and flag the file in the PR body.

## Nits (fix all)

N1 — `getPage` casts a missing `meta` to `M` silently. Reject with an `AppError` of type `unknown` when `meta` is absent, or type `meta` as optional. Choose one and say why.
N2 — Tests: Retry while the reason is `error`; two concurrent `restoreSession` calls make one request; a restore answered 401 (and the suspension 403) runs no ended-listener.
N3 — architecture.md §2 says each guard is "wrapping its route's page"; no route uses one yet. Add that the account and auth pages bring the first uses (F-5b3).
N4 — The PR body labels the `1-authenticated`, `2-unreachable` and `3-retried` screenshots "light"; they are dark. Fix the labels.
N5 — `services/dependencies.ts` is wiring (the default endpoints and hint), not a service. Move it to `gateway/`.
N6 — Commit subjects over 50 characters (workflow §3): `8bff8d3` (67), `6909125` (62), `89b70f1` (52). Reword them during the autosquash (`git commit --fixup=reword:<sha>`).

## History (the owner's rules)

- **Fold each fix into the commit whose unit it corrects:** `git commit --fixup=<sha>`, then `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash origin/main`. A logic fix folds into the feature commit that introduced the code, never into one of the three refactor commits, which must stay pure moves.
- **When a fixup meets a later rename during the rebase,** resolve it by applying the change at the file's old path. Then re-run your refactor check: the three refactor commits still change only paths and imports.
- **Every commit still passes on its own.** Push with `--force-with-lease`. Report only once CI is green on the new head.
- **Keep the ONE "Review fixes" comment:** the reviewed head `89b70f1`, the new head, and each id (O1, B1, S1–S4, N1–N6) with its severity and the commit it folded into.
