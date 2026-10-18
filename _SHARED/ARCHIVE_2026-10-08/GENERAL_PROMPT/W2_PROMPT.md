# F-5b2 — The session and the guards

**Worker A** · main folder `C:\Users\basel\masaha` · branch `feat/web-session`

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work

- **Start with the `start-work-item` skill.**
- **The owning documents for this item:**
  - `docs/frontend/architecture.md` (§1, §2 *Landing and guards*, §4 *Session and preferences*, §5, §7);
  - ADR 0003 (the session model) and ADR 0004 (data and state);
  - `docs/backend/security.md` › *Tokens and cookies*;
  - `docs/api/api-contract.md` §2 and §5 › *Session*, `POST /auth/refresh` and `POST /auth/logout`.
- **Read the code you build on:** `apps/web/src/shared/api/**` (F-5b1), `shared/routing/**` and `pages/site/**` (F-6b), `shared/preferences/**`, `app/bootstrap.ts`.
- **When finished, follow the `open-pr` skill.**
- **The owner's rules the skills don't carry yet:**
  - every test's title states something the test actually asserts;
  - on a lockfile conflict, take main's `package-lock.json` and run `npm install`;
  - **report only once CI is green on the pushed head** (`gh pr checks`);
  - **review fixes are folded into the commits they correct** (`git commit --fixup`, then `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash origin/main`, then `--force-with-lease`), never added as separate fix commits. Keep exactly ONE "Review fixes" comment.

## 2. Context

F-5b1 built the transport: one Axios client, `AppError`, TanStack Query, with the token getter and the refresh **injected** at bootstrap. Today bootstrap injects a getter that returns `null` and no refresh. This item builds `shared/session` and the route guards, and wires the session into the transport. There are no screens: the sign-in screens are F-5b3.

## 3. Decisions already made (do not reopen)

The owner approved these.

**The design**
- **Place.** The session lives in `shared/session` (platform), not in a feature. Every zone reads it; `features/auth` (F-5b3) produces it.
- **Contract types.** The wire types come from `@masaha/shared` (`Session`, `SessionUser`). No DTO and no mapper: the shared types are the contract, defined once.
- **Store.** A Zustand store, like `shared/preferences`: the raw store is never exported. Reads go through `useSession(select)` inside React and `getSession()` outside it; writes go only through the session's own named functions.
- **The endpoints layer** (the owner's design). One explicit interface and a factory with a default, injected into the services, so tests pass a plain fake:
  ```ts
  export interface SessionRequests {
    refresh: () => Promise<Session>;
    logout: () => Promise<void>;
  }
  export function createSessionRequests(client = api): SessionRequests { … }
  ```
  The session owns only `refresh` and `logout`. Sign-in, register and Google are `features/auth`'s (F-5b3); they hand their result to `establishSession`.
- **One public surface** (`index.ts`), with two faces:
  - React: `useSession(select)`, `useSignOut()`;
  - outside React: `getSession()`, `establishSession(session, { source })`, `refreshSession()`, `restoreSession()`, `onSessionEstablished(listener)`, `onSessionEnded(listener)`;
  - the types.
- **The token has one source** (F-5b1's contract). The injected `refresh` updates the store, then resolves with nothing. The transport always reads the token from the getter.

**J1 — what the store holds.** The `SessionUser` as the server sends it, the access token, and the status. No copy, no reshaping.

**J2 — language.**
- When the user **signs in** (`source: 'signIn'`), the account's language becomes the interface language.
- A **restore or a refresh** (`source: 'restore'`) never changes it: the user's later choice on this device wins.
- The wiring is in `app/bootstrap.ts` through `onSessionEstablished`, so the session never imports `shared/preferences`.

**J3 — sign-out.**
- The server is the source of truth. On success, the session ends locally.
- If the request fails (network, 5xx), nothing is cleared locally: the refresh cookie is still valid, so a local-only sign-out would be false. The failure is surfaced (`useSignOut()` returns its pending and error state), and the user retries.
- After the session ends, `onSessionEnded` listeners run. Bootstrap wires `queryClient.clear()` there.

**J4 — restore and refresh failures; the status model.**
- **The status has four values:** `restoring`, `authenticated`, `anonymous`, `unreachable`.
- **No session-hint cookie** (`masaha_session`) → `anonymous` at once, with no request.
- **A hint and a successful refresh** → `authenticated`.
- **Only a refresh answered `401` or `403`** ends the session: clear the hint, status `anonymous`.
- **A network error, a timeout or a 5xx** does NOT end it: the hint stays, and the status becomes `unreachable`, with a way to retry the restore. Without this rule, a power or internet cut in Gaza while the site opens would sign the user out.
- The same rule applies to a refresh triggered by the transport's 401.

**J5 — request helpers in `shared/api`.** Add small typed helpers that unwrap the envelope, so no capability ever writes `unwrap` or sees the envelope:
- `api.get<T>(url, config?)` and `api.post<T>(url, body?, config?)` (and `put`/`patch`/`delete` if trivial) resolve to `data`;
- `api.getPage<T>(url, config?)` resolves to `{ data, meta }`, for paginated lists and `meta.warnings`;
- keep `apiClient` and `unwrap` exported for the edge cases.

**J6 — which guards now.** In `shared/routing`, with tests using test routes:
- `RequireAuth`: signed in;
- `RequireGuest`: guests only (the auth pages, F-5b3);
- `RequireRole`: a global role (for example `ADMIN`).

The **space-role guard** (OWNER or RECEPTION at the `:spaceId` in the URL, ADR 0016) is built with the dashboard in F-6c, where its routes exist.

**J7 — the guards' behaviour** (architecture.md §2):
- **while `restoring`:** the design-system layer's loading indicator (`Spinner`), centred;
- **`unreachable`:** the offline state from `shared/routing` (as F-6b built it), with Retry re-running the restore;
- **a guest on a protected route:** redirected to `/login` with the return URL;
- **a signed-in user without the role:** a clear 403 state, never a silent redirect. Add a `ForbiddenState` beside `NotFoundState`, from the layer's `EmptyState`, with copy in both catalogues;
- **a signed-in user on a guest-only route:** redirected away. The full landing rule is F-6c's; until then, the return URL or `/`;
- **guards sit visibly on each route,** never inherited silently.

**J8 — the forced password change** is NOT built here. The session carries `mustChangePassword` in the user; the gate and its screen come with F-5b3.

## 4. The design

### 4.1 Folders

```
apps/web/src/shared/session/
  index.ts          the public surface (§3)
  model.ts          SessionState, SessionStatus; re-exports the contract types
  store.ts          the Zustand store (internal) and its only writers
  requests.ts       SessionRequests + createSessionRequests(client = api)
  sessionHint.ts    reads and clears masaha_session: the only place that knows its name
  refresh.ts        single-flight refresh: one shared promise for the restore and the transport; J4
  restore.ts        the startup restore; J4
  signOut.ts        the server-confirmed sign-out; J3
  hooks.ts          useSession(select), useSignOut()
  *.unit.test.ts
apps/web/src/shared/api/
  request helpers (J5), with their tests
apps/web/src/shared/routing/
  RequireAuth.tsx, RequireGuest.tsx, RequireRole.tsx, ForbiddenState.tsx (+ index exports)
  *.component.test.tsx
app/bootstrap.ts    setupApiClient({ getAccessToken: () => getSession().accessToken, refresh: refreshSession });
                    onSessionEnded(() => queryClient.clear());
                    onSessionEstablished(J2's language rule);
                    void restoreSession();   // non-blocking: public pages render at once
```

Propose a different split in the plan if you have a reason. The public surface and the rules are the contract.

### 4.2 Dependencies

```
app/bootstrap   ──► shared/session, shared/api, shared/preferences
shared/routing  ──► shared/session (guards), shared/design-system, shared/copy
shared/session  ──► shared/api (api helpers), @masaha/shared (types)
shared/api      ──► shared/errors   (never the session: injected)
```
`shared/session` never imports `shared/preferences`, `@tanstack/react-query`, the copy, routing or any feature.

## 5. Tests

**The unit lane** (fakes for `SessionRequests`, the hint and the clock; no network):
- **restore:**
  - no hint → `anonymous`, no request;
  - hint + success → `authenticated` with the user and the token;
  - hint + 401 → `anonymous`, hint cleared;
  - hint + 403 → same;
  - hint + network error / timeout / 5xx → `unreachable`, hint kept;
  - retrying from `unreachable` works;
- **refresh:**
  - concurrent calls (the restore and the transport) make ONE request;
  - success updates the store before the promise resolves;
  - 401/403 ends the session and rejects;
  - a network failure leaves the session and rejects;
- **establish:**
  - `source: 'signIn'` vs `'restore'` reaches the listeners correctly;
- **sign-out:**
  - success ends the session and runs `onSessionEnded`;
  - failure keeps the session, and `useSignOut` exposes the error;
- **the request helpers:** `get`/`post` resolve to `data`; `getPage` keeps `meta`; errors arrive as `AppError`;
- **bootstrap wiring:**
  - a session ending clears the QueryClient;
  - sign-in applies the account language, a restore does not.

**The component lane**, for each guard with test routes:
- `restoring` shows the spinner;
- `unreachable` shows offline, and Retry re-runs the restore;
- a guest is redirected to `/login` with the return URL;
- the wrong role shows `ForbiddenState`;
- a signed-in user on a guest route is redirected.

## 6. Documents

- **`architecture.md`:**
  - §4 (the session's design as built: the status model, J2, J3, J4);
  - §2 *Landing and guards*: what is built (the three guards, the 403 state) and what is F-6c's (the space guard, landing, switcher);
  - §1's status line;
  - §7: the request helpers.
- **`docs/architecture/system-overview.md`** (deferred, owed now): restoring the session is the first request web → API → database. Write it (the zones, the transport, the session, the API layers, the database; one request traced end to end), and remove its row from the *Deferred documents* table in `docs/README.md`.
- **`docs/plans/foundation.md`:** the F-5b2 entry stays as it is unless the plan changes its scope.

## 7. Contract

**Acceptance criteria**
- [ ] `shared/session` exists with the public surface of §3; the raw store is not exported.
- [ ] Bootstrap wires the getter, the refresh, `onSessionEnded` → `queryClient.clear()`, the language rule (J2), and a non-blocking restore.
- [ ] J4 holds, proven by tests: only 401/403 end the session; a network failure gives `unreachable` and keeps the hint.
- [ ] Concurrent refreshes make one request, proven by a test.
- [ ] The three guards and `ForbiddenState` exist, with their component tests.
- [ ] **A manual end-to-end check, described in Evidence:**
  - sign in through the proxy (for example `fetch('/api/v1/auth/login', …)` in the browser console, or a seeded account);
  - reload: the session restores (`authenticated`);
  - stop the API and reload: `unreachable`, the hint kept;
  - start the API again and Retry: `authenticated`.
- [ ] `system-overview.md` is written, and its deferred row removed.
- [ ] Every new string is in both catalogues; the Arabic for any line not in a design is listed for the owner's approval.

**Out of scope**
- Any screen, the sign-in forms, Google on the web, the forced-change gate (F-5b3).
- The space-role guard, the landing rule, the switcher, the dashboard (F-6c).
- `PATCH /me` or syncing a language change back to the account.
- Any new dependency. Ask before adding one.

## 8. Parallel work

**Worker B** may restructure `packages/shared` later (a separate item, tracked in an Issue); it is **not** running now. If it starts while you work, the owner will tell you. Its main effect on you: import paths from `@masaha/shared` would change.

- **Your files:** `shared/session/**`, `shared/api/**`, `shared/routing/**` (the guards and `ForbiddenState`), `app/bootstrap.ts`, the copy you add, `architecture.md` §1/§2/§4/§7, `system-overview.md`, `docs/README.md`'s deferred table.
- **Rebasing:** before the PR, fetch and rebase on `origin/main`.

## 9. Commits

Propose the split in the plan. A likely one:
1. `feat(api-client): add request helpers that unwrap the envelope`
2. `feat(session): add the session store, restore, refresh and sign-out`
3. `feat(session): wire the session into the app`: bootstrap, `onSessionEnded`, the language rule
4. `feat(routing): add the auth, guest and role guards`: with `ForbiddenState`
5. `docs(architecture): write the system overview`

## 10. Pull request

- **Labels:** `feat`, `area:web`, `area:docs`.
- **Review:** this item goes through the review gate (two independent reviews: it handles the session and its tokens). After opening the PR and seeing CI green, stop and report. Don't start fixes until the owner sends the list.
- **No tool or AI attribution** anywhere. Don't merge. Don't create an Issue.
