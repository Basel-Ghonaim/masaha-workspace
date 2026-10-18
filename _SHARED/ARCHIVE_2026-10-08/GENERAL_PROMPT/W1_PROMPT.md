# F-5b1 — The web transport, errors and server state

**Worker A** · main folder `C:\Users\basel\masaha` · branch `feat/web-transport`

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work

- **Start with the `start-work-item` skill.** It covers the checks, the reading, plan mode and the branch.
- **The owning documents for this item:**
  - `docs/frontend/architecture.md` (§1 zones, §5 errors, §7 server state);
  - ADR 0004 (data and state) and ADR 0014 (one origin, the development ports);
  - `docs/api/api-contract.md` §1–§3 (conventions, envelope, error types);
  - `docs/frontend/localisation.md` (catalogues).
- **For the new copy,** follow the `add-error-code` skill's PR step: list the text in both languages and mark the Arabic as needing the owner's approval. These are client error types, not domain codes, so only that step applies.
- **When finished, follow the `open-pr` skill.**
- **Rules the skills don't carry yet:**
  - every test's title states something the test actually asserts;
  - on a lockfile conflict, take main's `package-lock.json` and run `npm install`, never edit it by hand;
  - after review fixes, keep exactly ONE "Review fixes" comment on the PR, edited in later rounds.

## 2. Context

F-5b, authentication on the web, is split into three Work Items, so the platform exists before any feature uses it:
1. **F-5b1 (this item):** the transport, the errors and server state. No session, no screen.
2. **F-5b2:** `shared/session` and the route guards, wired into this transport.
3. **F-5b3:** the auth screens (to be split further when planned).

The design takes ideas from Quick Tweets (`D:\quick-tweets-app\apps\web\src\shared\errors` and `shared\api`): you may read them for the ideas, and you rebuild them inside Masaha's rules. **Never copy-paste.** Masaha deliberately differs from Quick Tweets in the ways listed in §3.

## 3. Decisions already made (do not reopen)

The owner approved these.

- **D1. Retries live in ONE place: the transport.**
  - The Axios retry re-sends a request only if it is a `GET`, or it carries an `Idempotency-Key` header. It retries on 5xx, network errors and timeouts, with backoff, a small fixed number of times. It never retries a 4xx, including 429.
  - TanStack Query's `retry` is `false`, for queries and mutations, so attempts never multiply.
  - This matches ADR 0004 (Axios retries) and architecture §7 (queries are retried; a mutation only with an idempotency key). State in §7 where retries happen.
- **D2. One Axios client.**
  - `baseURL: '/api/v1'`, relative, in every environment (ADR 0014).
  - It attaches the token when a getter returns one.
  - No separate public or credentialed client: one origin sends the cookies by itself.
- **D3. The timeout:** 15 s by default, overridable per request.
- **D4. A lint rule:** `axios` is imported only inside `apps/web/src/shared/api`, the way Radix is only imported inside the design-system layer (see the existing restricted-import block in `eslint.config.js`). Everything else uses what `@shared/api` exports. Prove it once with a probe import elsewhere, then revert; don't commit the probe.
- **D5. TanStack Query's defaults:**
  - `retry: false` (D1);
  - `refetchOnWindowFocus` stays on (architecture §7: the front desk refreshes on focus);
  - propose `staleTime` and any other default in the plan, each with its reason.
- **D6. New dependencies: `axios` and `@tanstack/react-query` only.** No devtools, no MSW, no axios-retry or other helpers. Check the current major of each in the plan.
- **D7. The four client error types** (`network`, `timeout`, `canceled`, `unknown`) get text in both catalogues. The Arabic needs the owner's approval in the PR.
- **Dependency injection:** the transport never imports the session; it doesn't exist yet. `setupApiClient` receives `getAccessToken` and an optional `refresh` from `app/bootstrap`. In this item, bootstrap wires it with a getter that returns `null` and no refresh. F-5b2 wires the session in.

## 4. The design

### 4.1 Folders

```
apps/web/src/shared/
  errors/
    index.ts          public: AppError, toAppError, isAppError, AppErrorType
    AppError.ts       type, status, code?, errors?, requestId?, retryAfterSeconds?
    errorTypes.ts     the client-only types (network, timeout, canceled, unknown);
                      the server's types come from @masaha/shared, never repeated
    toAppError.ts     the one normaliser: any failure → AppError
    retryAfter.ts     reads Retry-After (delta-seconds only)
    *.unit.test.ts
  api/
    index.ts          public: apiClient, setupApiClient, unwrap, ApiEnvelope, createQueryClient
    client.ts         the one Axios instance
    envelope.ts       ApiEnvelope<T> with meta, and unwrap at the call site
    setupApiClient.ts installs the interceptors with the injected dependencies
    interceptors/
      authorization.ts  attaches the Bearer token from the getter
      retry.ts          D1
      refreshOn401.ts   single-flight refresh through the injected function
      normalise.ts      last: every rejection leaves as an AppError
    queryClient.ts    createQueryClient(): the defaults of D5
    *.unit.test.ts
app/
  bootstrap.ts        + setupApiClient(...)
  providers.tsx       + QueryClientProvider, from createQueryClient()
```

Propose a different file split in the plan if you have a reason. The folders and the public surfaces are the contract.

### 4.2 The dependency graph

```
app/bootstrap ──► shared/api (setupApiClient)
app/providers ──► shared/api (createQueryClient) + @tanstack/react-query
shared/api    ──► shared/errors + axios + @tanstack/react-query (queryClient.ts only)
shared/errors ──► @masaha/shared (ErrorType) + axios (the error type only)
shared/copy   ──► shared/errors (AppErrorType, for the catalogue's completeness check)
```

- `shared/errors` decides a failure's **type** only. It never words it: screens pick the catalogue text from `code ?? type` (architecture §5). `AppError` carries no user-facing message.
- `shared/api` never imports the session, the copy or any feature.

### 4.3 The rules each part must hold

**`toAppError`:**
- **The server's envelope** (api-contract §2): use its `type` when it is a known `ErrorType`, else infer from the status; carry `code`, `errors` and `requestId`.
- **The `requestId`** comes from the body, else from the `X-Request-Id` header (for example, a 502 from a proxy has no body).
- **No response:** `ERR_NETWORK` → `network`; `ECONNABORTED` / `ETIMEDOUT` → `timeout`; `ERR_CANCELED` → `canceled`.
- **An `AppError`** passes through unchanged. **Anything else** becomes `unknown`.

**`refreshOn401`:**
- **No token, no refresh:** a 401 without a token is a refused sign-in, not an expired session.
- **Excluded paths:** the refresh never runs for `/auth/*` requests (sign-in, register, refresh, logout, passwords).
- **Single-flight:** one refresh at a time. Every concurrent 401 waits for the same promise, then replays with the new token.
- **Failure:** a failed refresh rejects every waiting request with an `AppError`.
- **No loops:** a replayed request that gets 401 again is not refreshed again.
- **Order:** interceptors run in a defined order. The retry sees the raw error, and normalisation is last. State the order in a comment.

**`unwrap`:** returns `data`, and leaves `meta` reachable for the calls that need it (pagination, the desk's `meta.warnings`).

### 4.4 The development ports (ADR 0014, F-5b's planned scope)

- **The web:** port 5320, with `strictPort`.
- **The proxy:** Vite forwards `/api` to `http://localhost:3320`.
- **The API:** its default `PORT` becomes 3320, and `.env.example`'s `PORT` and `CORS_ORIGIN` follow (`http://localhost:5320`).
- **The documents:** `setup.md` and `CLAUDE.md` *Commands* say so.
- **The owner's own `apps/api/.env`** still holds the old values. Put that action in the PR description, in an "On your machine" section.

## 5. Tests

**The unit lane:** use Axios's own `adapter` option as the fake transport, and Vitest's fake timers for backoff. Add no test library.

| File | Proves |
|---|---|
| `toAppError` | every rule of §4.3, one case each |
| `retryAfter` | delta-seconds; empty, negative and HTTP-date values are ignored |
| `retry` | a GET is retried on 503 and on a network error, up to the limit, with backoff; a POST is not; a POST with `Idempotency-Key` is; 4xx and 429 never are |
| `refreshOn401` | no token, no refresh; one 401 with a token gives one refresh and one replay; **N concurrent 401s give exactly ONE refresh**; a failed refresh rejects all of them as `AppError`; `/auth/*` never refreshes; a second 401 after the replay doesn't loop |
| `normalise` | every rejection is an `AppError`; the retry sees the raw error before it |
| `envelope` | `unwrap` returns `data`; `meta` stays reachable |
| `queryClient` | the agreed defaults |

**The component lane:** `AppProviders` provides a `QueryClient`. Extend `providers.component.test.tsx`.

**Already guarded:** the catalogue parity test and the typecheck (the errors catalogue `satisfies` every `AppErrorType` and domain code) catch a missing text.

## 6. Documents

Each update goes in the commit of the unit it describes.
- **`architecture.md`:**
  - the status line: `shared/api` and `shared/errors` are built;
  - §5: what is built (the normaliser with `requestId`) and what is not yet (error states showing it);
  - §7: where retries live (D1), and the Query defaults.
- **`docs/plans/foundation.md`:** record the F-5b split into F-5b1, F-5b2 and F-5b3 in its F-5b entry, the way the F-5 split was recorded, in its own first commit.
- **`setup.md` and `CLAUDE.md` *Commands*:** the ports (§4.4).
- **Deferred documents:** `system-overview.md` is NOT written here: no request crosses web → API → database yet.

## 7. Contract

**Acceptance criteria**
- [ ] `shared/errors` and `shared/api` exist with the public surfaces of §4.1, and the dependency graph of §4.2 holds.
- [ ] Every rule of §4.3 has its unit test (§5).
- [ ] Concurrent 401s trigger exactly one refresh, proven by a test.
- [ ] `axios` imported outside `shared/api` fails `lint`, proven once by a probe and reverted.
- [ ] `AppProviders` provides a `QueryClient` whose `retry` is false.
- [ ] `npm run dev` serves the web on 5320; `/api/v1/...` reaches the API on 3320 through the proxy; `/health` reaches it directly on 3320.
- [ ] Both catalogues have the four client error types; the Arabic is listed for approval.

**Out of scope**
- `shared/session`, the guards, any feature, any page, any screen.
- Any change to `apps/api` beyond the default `PORT` and `.env.example`.
- An offline queue, request cancellation helpers, or anything Quick Tweets has that §4 doesn't list (for example `media.ts`).
- Any dependency beyond D6.

## 8. Parallel work

**Worker B** will work in `C:\Users\basel\masaha-b` on the public shell (F-6b): the header, the footer and the error pages, in `pages/` and the design-system-facing parts of the app.

- **Your files, which B won't touch:** `shared/api/**`, `shared/errors/**`, `app/bootstrap.ts`, `app/providers.tsx`, `vite.config.ts`, `apps/api/**`, `eslint.config.js`.
- **Shared files.** Declare them in the plan, and keep to your section:
  - the copy catalogues: you edit only `errors.ts` in each language; B adds its own entries elsewhere;
  - `docs/frontend/architecture.md`: you own §5, §7 and the shared/api and shared/errors parts of the status line; B may touch §2;
  - `docs/development/setup.md` and `CLAUDE.md` *Commands*: the ports are yours;
  - `package-lock.json`: only you add dependencies in this wave. B adds none.
- **Rebasing:** before the PR, fetch and rebase on `origin/main`. Whoever merges second rebases again and keeps both sides.

## 9. Commits

Propose the split in the plan. A likely one:
1. `docs(plans): split f-5b into three items`
2. `feat(errors): add the app error and its normaliser`, with the client types' copy
3. `feat(api-client): add the axios client and its interceptors`, with the lint rule
4. `feat(api-client): set up tanstack query`, with providers and bootstrap
5. `chore(dev): serve the web on 5320 and proxy /api to 3320`

## 10. Pull request

- **Labels:** `feat`, `area:web`, `area:api`, `area:docs`.
- **Review:** this item goes through the review gate (two independent reviews). After opening the PR, stop and report; don't start fixes until the owner sends the fixes list.
- **No tool or AI attribution** anywhere. Don't merge. Don't create an Issue.
