# F-5b3c1 — The forced password change, and the recovery session on the API

**Worker A** · main folder `C:\Users\basel\masaha` · branch `feat/forced-change-recovery-session`

**Start only after PR #35 (F-5b3a) is merged.** The owner will tell you.

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work

- **Start with the `start-work-item` skill.**
- **The owning documents:**
  - `docs/backend/security.md` › *Passwords* and *Tokens and cookies*;
  - `docs/api/api-contract.md` §5 (the forgotten password, `/me/password`);
  - `docs/backend/conventions.md` (§7–§9, §13);
  - `docs/architecture/data-model.md`;
  - `docs/frontend/architecture.md` (§1 folders by role; §2 the guards and the landing; §3 the feature rules H1–H8; §4 the session);
  - `docs/development/testing.md` (*A feature, layer by layer*);
  - ADR 0003, ADR 0013, ADR 0014;
  - `docs/architecture/findings.md` (finding 16).
- **For reference only (ideas, never code):** Quick Tweets' recovery design, in `D:\quick-tweets-app\docs\api\api-contract.md` › *Password Reset*, and its ADR 0017. Rebuild the ideas inside Masaha's rules.
- **When finished, follow the `open-pr` skill.**
- **The owner's rules the skills don't carry yet:**
  - every test's title states what it asserts;
  - on a lockfile conflict, take main's `package-lock.json` and run `npm install`;
  - report only once CI is green on the pushed head;
  - review fixes are folded into the commits they correct; a genuinely new unit gets new commits; ONE "Review fixes" comment;
  - **no production code exists only for a test** (testing.md §3): no parameter, option or callback that only tests pass or that nothing uses yet. Tests replace the platform's own seams: the transport through `fakeTransport` / `fakeAdapter`, and browser APIs (the cookie, storage) through `vi.stubGlobal`. PR #35 removed every such seam, so don't bring one back;
  - **run the checks one at a time,** never several lanes in parallel: the machine ran out of memory last time. The per-commit check is still required.

## 2. What this item delivers

Two parts, one PR.

### Part A — The forced password change (web)

A user whose account has a pending temporary password (`mustChangePassword`) must change it before any other page.

**The owner's decisions:**
- **M1 — the gate:** it lives in `shared/routing` and is mounted at `RootLayout`, so it covers every route, the site's and the dashboard's. The change page itself and signing out are exempt.
- **M2 — the change form:** it belongs to `features/users` (the `/me/password` endpoint is the `users` module's).
  - `features/users` already exists, with the account menu. Extend it: a `usersRepository` made once at module level, with no parameter (the pattern of `createAuthRepository()` and `createSpaceLinksRepository()`), plus the form's hooks and component.
  - The form reuses `shared/forms`: `useServerForm`, `PasswordRules` (fed ready rule views by the hook) and `FormFailure`. Components only render (H6).
- **M3 — the session:** `/me/password` answers with an access token only, so the session gains `passwordChanged(accessToken)`. It renews the token and clears `mustChangePassword`. Add it in `shared/session` like the existing operations, with no test-only parameter.
- **M6 — after the change:** the user lands through `landingPath`, which F-6c1 merged.
  - **The landing's owner is a guard, never the page** (the rule PR #35 set: `RequireGuest` owns the sign-in landing, and pages pass no navigating callback).
  - So once `mustChangePassword` clears, the guard that holds the change page sends the user on through `landingPath`. Don't thread an `onSuccess`.
  - Don't wire `landingPath` into `RequireGuest` or the sign-in pages: that is F-6c2's job.
- **The page:** `/change-password`, under `FocusLayout`, with the short header the design draws (the wordmark and "Sign out"; `docs/design/screens/18-forced-password-change/`). "Sign out" reuses the session's existing sign-out (`useSignOut`, as the account menu does), with its pending and error states. Don't write a second one.

### Part B — The recovery session (API)

The forgotten-password flow on the API is reworked, so the **server** holds where a person stands in a recovery, and the web never holds the reset credential.

**The owner's decisions:**
- **Q1 — the session:**
  - a request for a reset link opens a recovery session, kept by the server and carried in an `HttpOnly` cookie;
  - the request answers with the session's **position**: its step, the email masked, the resend window, and whether a resend is allowed;
  - **the answer is identical for every address,** whether or not an account exists.
- **Q2 — the credential:**
  - checking the link's token **binds it to the recovery session**;
  - setting the new password reads the token **from the session**;
  - a token sent in the reset request's body is **refused**;
  - the web stops holding the token once it is checked.
- **Q3 — resending:** asks the session for another link **without an email**, a bounded number of times.
- **R1 — storage:** the recovery session is a database table, owned by the `sessions` module, which owns the other tokens. This is a schema change: a new migration.
- **R2 — another device:** checking a link in a browser with no recovery session opens one there. Most people open the email on their phone.
- **R3 — the bound:** at most **3** resends per session.
- **R4 — the window:** **60 seconds**, the same for every address, so it reveals nothing.
- **R5 — the rate limit:** resending shares the forgot request's existing budget, not a budget of its own.
- **R6 — the cookie:**
  - `masaha_reset`: `HttpOnly`, `SameSite=Strict`, `Secure` outside development;
  - scoped to the password routes;
  - it lives as long as the reset link;
  - cleared when the reset succeeds;
  - its endpoints refuse cross-site requests, as refresh and logout do.
- **R7 — a token in the body:** refused with 422.
- **R8 — an ADR:** write a short ADR, "the recovery session": the decision and its reason, with no file names (the owner's ADR style).
- **R9 — reading the position:**
  - an endpoint answers where the caller stands, and never 404s;
  - with no session, the step is "request";
  - otherwise it is "sent" (with the masked email, the window and whether a resend is allowed) or "password".
- **Not taken from Quick Tweets: sending the email after the answer.** ADR 0014 forbids work after a response, because the function may be frozen as it answers. Finding 16 stays open.

**What stays as it is:**
- the reset link carries its token in the URL fragment;
- the existing per-recipient caps, the requester cap, the ceiling and B3's delivery-dependent replacement;
- every existing guarantee in security.md.

Nothing here makes a weaker promise than today.

## 3. Your plan decides

- **On the API:**
  - the endpoints' paths and shapes, within api-contract's conventions;
  - the table's columns;
  - how the request, check, resend and reset steps use the session;
  - the order of operations under the session lock where tokens are written (conventions §13).
- **On the web:**
  - the gate's mechanism;
  - the `users` feature's additions (repository, hooks, components), per H1–H8;
  - the page's composition.
- **The tests in each lane,** per testing.md:
  - the API lane for every recovery endpoint and its refusals (no session, a spent bound, a token in the body, cross-site, an unknown address answering the same as a known one);
  - the unit lane for the rules;
  - per testing.md's *A feature, layer by layer*: the users repository's call in the unit lane; the hooks with renderHook through the transport's fake adapter; components on rendering only;
  - the gate and its exemptions (the change page, signing out), and the landing after the change, in the component lane.
- **The documents:**
  - security.md, api-contract.md and data-model.md for the new flow;
  - the ADR;
  - architecture.md §2/§4 for the gate and `passwordChanged`;
  - the plan's F-5b3c entry, recording that F-5b3c is split into c1 (this) and c2 (the recovery pages).

  The API changes the recovery's contract, but the web's recovery pages come in c2. Say in the PR that the old web flow has no pages yet, so nothing breaks.

## 4. Out of scope

- The forgot and reset **pages** (F-5b3c2).
- Google (F-5b3b).
- Changing the password from the account settings, and `PASSWORD_NOT_SET` (a later item, with `/me`).
- Issuing temporary passwords.
- Signing out of all devices.
- Any new dependency, unless the plan proposes it with a reason.

## 5. Parallel work

**Worker B** may work in `C:\Users\basel\masaha-b` at the same time, on one of:
- F-6c2: the dashboard shell, `pages/dashboard`, wiring `landingPath` into `RequireGuest`;
- the storage layer (Issue #37): `shared/preferences`, `shared/routing/landing/lastSpace.ts`.

The owner will tell you which.

- Declare in the plan the shared files you expect (`shared/routing/index.ts`, `router.tsx`, `RootLayout`, `architecture.md` sections, `foundation.md` entries, the copy catalogues), and keep to your sections.
- Whoever merges second rebases and keeps both sides.
- **The migration:** after the merge, the owner applies it to `masaha_dev` and `masaha_b_dev`.

## 6. Pull request

- **Labels:** `feat`, `area:api`, `area:web`, `area:docs`.
- **The review gate:** two independent reviews. This item changes how a password is recovered and adds a gate on every route. After CI is green, stop and report. Don't start fixes until the owner sends the list.
- **The Arabic** for any line not in a design is listed for the owner's approval.
- No tool or AI attribution anywhere. Don't merge. Don't create an Issue.
