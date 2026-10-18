F-5b1 — review fixes for PR #29 (the ONE list)

Two independent reviews ran against e49b8be (one on the transport's correctness, one on conformance and documents). The owner's analyst verified the blocker and the transport findings in the code. Apply everything below on this same branch and PR, each fix with its test, in atomic commits. Then re-run every lane, update the PR description, and add ONE "Review fixes" comment (a table: id, severity, commit, or "not done" with the reason). Don't merge.

NEW RULE FOR THIS AND EVERY LATER REPORT: report only after CI is green on the pushed head (`gh pr checks`). A local pass is not enough: CI was red on e49b8be while the report said every check passed.

## Blocker

B1 — CI fails: the web cannot resolve `@masaha/shared` at runtime.
- This item adds the web's first runtime (value) import of `@masaha/shared` (`ERROR_TYPES`, `DOMAIN_ERROR_CODES`, ...). `apps/web/vite.config.ts` has no `@masaha/source` resolve condition, so Vite and Vitest resolve the package's `dist/`, which CI never builds before the test lanes. It passed locally only because a stale `packages/shared/dist` exists. A fresh clone's `npm run dev` would fail the same way.
- Fix: resolve `@masaha/shared` from source in the web, as the API does (`apps/api/vitest.config.ts`, `tsx --conditions=@masaha/source`; the web's tsconfig already has `customConditions`). Add the condition so it applies to the dev server, both Vitest projects (client and node environments), and the build. Mind that Vite has separate client and server/SSR resolve conditions; keep the defaults after the custom one.
- Proof: delete `packages/shared/dist` locally, then run `test:unit`, `test:component`, `build`, `check:build` and a `npm run dev` smoke; all pass. State this in Evidence. Update setup.md's sentence about reading `@masaha/shared` from source if it names only the API.

## Should-fix — transport (verified in the code)

T1 — A re-send keeps a stale token. `authorization.ts` never overwrites an existing `Authorization`, and a retry carries the first attempt's headers. A GET that waits 1–2 s to retry still sends the old token after a refresh, or after a sign-out (getter now null).
- Fix: the interceptor owns the header it sets. Record in the request state that the transport set it; on every attempt, overwrite it with the getter's current value, or remove it when the getter returns null. Keep only a header the caller set explicitly.
- Tests: a retry after the getter's token changes sends the new one; after the getter returns null it sends none; a caller-set header is kept.

T2 — A late 401 from an old token refreshes a second time. After a refresh completes, a slower request sent with the old token gets its 401, finds no refresh in flight, and refreshes again: an extra rotation that counts against the refresh limit (security.md, 30 per 15 min), and a 429 there would reject every waiter.
- Fix: if the 401's request was sent with a token other than the getter's current one, the session is already renewed: replay with the current token, without refreshing.
- Test: two requests sent with token A; the first 401 refreshes to B; the second 401 arrives after the refresh resolved → it replays with B and `refresh` was called once.

T3 — The `/auth/` exclusion matches the raw `config.url` only. `'auth/refresh'` (no leading slash) or a full path is not excluded; in F-5b2, a refresh call answered 401 could then await its own refresh and hang forever.
- Fix: exclude on the resolved request path (for example the pathname of `client.getUri(config)` relative to `/api/v1`), so every spelling of an auth call is excluded. Optionally also an explicit per-request flag for the refresh call.
- Tests: `'auth/refresh'` and `'/auth/refresh'` both never trigger a refresh.

T4 — Field-error codes are not filtered. `isFieldErrors` accepts any string, so a server code the web doesn't know reaches screens typed as `FieldErrorCode`, with no catalogue line. Filter each field's codes against `FIELD_ERROR_CODES` (drop unknown ones), as domain codes already are. Test it.

T5 — The refresh-failure test would pass with wrong code (the refresh fails with 401, the same type as rethrowing the original). Make the refresh fail with a type the original cannot produce (a network error, or 403 `ACCOUNT_SUSPENDED`), and assert the waiting requests are still pending before the refresh settles.

T6 — The retry's backoff ignores `config.signal`. A request cancelled during the wait stays pending up to 3 s and leaks a timer. Make the wait abortable: when the signal aborts, clear the timer and reject at once as canceled. Test it with fake timers.

## Should-fix — documents

D1 — architecture.md §7 states the token getter and the single-flight refresh as working in the app. The mechanism is built, but bootstrap wires `getAccessToken: () => null` and no refresh. Add that the session wires both in F-5b2; until then no token is sent and no refresh runs.

D2 — architecture.md §3's capability layout says `api.ts  Axios calls + TanStack Query hooks`, which D4's lint now forbids. Change it to calls through `apiClient` (`@shared/api`) + TanStack Query hooks. That one line only: worker B edits §3's dashboard-only paragraph, so keep to your line, and keep both sides on a rebase conflict.

D3 — ADR 0004 says the transport retries "for 5xx and network errors only"; D1 approved timeouts too. The owner approves a revision in place: add timeouts, with a `> **Revised:** 2026-10-03 — …` line, as workflow §7 allows.

## Nits (fix all; each is small)

N1 — The lint rule misses `import('axios')` and `require('axios')`. Add a `no-restricted-syntax` selector for an `ImportExpression` (and `require` call) whose source is `axios` or `axios/…`, outside `shared/api`. Prove it with a probe, reverted.
N2 — Narrow the test exemption from `apps/web/src/test/**` to `apps/web/src/test/fakeAdapter.ts`.
N3 — The `shared/errors` type-only block matches `**/*.ts`; make it `**/*.{ts,tsx}` so a `.tsx` there can't escape both blocks.
N4 — `App.tsx` and `bootstrap.ts` import `type QueryClient` from `@tanstack/react-query`, outside the §4.2 graph. Re-export the type from `@shared/api` and import it from there.
N5 — `providers.component.test.tsx` and `App.component.test.tsx` call `bootstrap()`, discard the client it returns and create another. Use the returned client.
N6 — Arabic, owner's decision: «استغرق الخادم وقتًا طويلًا للردّ. حاول مرة أخرى.» (with the shadda, as the rest of the catalogue). The other three lines are approved as they are.
N7 — The PR title understates the item. Retitle the PR (not the commits): `feat(web): add the transport, errors and server state`.

## Not for this PR

- architecture.md §2's "F-5b builds the guards" is worker B's section; B's F-6b changes it. Leave it.

## History: fold the fixes into the commits they correct (the owner's rule)

The PR is not merged, so its history is still the deliverable. A fix is not a unit of its own: it corrects a unit that is already a commit. So:
- **Fold each fix into the commit it corrects.** Commit each fix as `git commit --fixup=<sha of the commit it corrects>`, then run `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash origin/main` (non-interactive: the sequence editor accepts the todo as is). For example, B1 folds into `feat(errors)` (the first runtime import of `@masaha/shared`); T1–T3, T5, T6, N1–N3 into `feat(api-client): add the axios client`; T4 into `feat(errors)`; D3 into the retry's commit; N4–N5 into `set up tanstack query`; D1/D2 into the commit whose unit they describe.
- **A separate commit only for a genuinely new unit.** None is expected in this list; if you think one is, say why in the PR.
- **Every rewritten commit must still build, lint, typecheck and pass its tests on its own.** Check each one, for example with `git rebase --exec "npm run lint && npm run typecheck && npm run test:unit" origin/main` after the autosquash.
- Push with `git push --force-with-lease`. Never force-push anything but this branch.
- **Keep the review traceable:** the "Review fixes" comment names the reviewed head (`e49b8be`) and the new head, so `git diff e49b8be <new head>` shows exactly the fixes, and the table maps each id to the commit it was folded into.

## When done

1. Push; wait for CI green on the head.
2. Update the PR description to the final state (Evidence: every lane, the `dist`-deleted proof, what wasn't run).
3. Add the ONE "Review fixes" comment with every id above: B1, T1–T6, D1–D3, N1–N7.
4. Stop and report.
