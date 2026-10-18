# F-5b3c2 — The recovery pages (forgot and reset password)

**Worker A** · main folder `C:\Users\basel\masaha` · branch `feat/recovery-pages`

**Start only after F-5b3c1 (the recovery session) is merged.** The owner will tell you.

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work

- **Start with the `start-work-item` skill.**
- **The owning documents:**
  - `docs/frontend/architecture.md` (§2–§4: H1–H8, the guards);
  - `docs/development/testing.md` (the per-layer rule);
  - `docs/api/api-contract.md` and `docs/backend/security.md` (the recovery session, as F-5b3c1 left them);
  - the recovery session's ADR;
  - `docs/frontend/localisation.md`.
- **The designs:** SCREENS.md row 7, and `docs/design/screens/08-forgot-reset-password/` (forgot, sent with its countdown, too many attempts; the new password, the link expired or used, success).
- **For reference only:** Quick Tweets' `apps/web/src/features/recovery` (ideas, never code).
- **When finished, follow the `open-pr` skill.**
- **The owner's rules,** the same as F-5b3c1's §1:
  - honest test titles;
  - the lockfile rule;
  - report on green CI only;
  - fixes folded, and ONE "Review fixes" comment;
  - **no parameter, option or callback that only tests pass or that nothing uses.** Tests stub the platform's seams (`fakeTransport`, `vi.stubGlobal`);
  - **pages pass no navigating callbacks:** a guard or a link owns navigation;
  - checks run one at a time;
  - **one responsibility per file:** one component, one hook, one helper per file, **internal ones included** (no file declares several components), named after what it holds. Logic leaves components for hooks or `services/`. The owner set this rule after F-6c2. If architecture.md doesn't state it yet, follow it anyway.

## 2. What this item delivers

The two recovery pages, on the session the API now holds.

**The API is built and merged** (F-5b3c1, PR #38). Read its contract in api-contract.md §5 *The forgotten password*. In short:
- **The five endpoints,** all under `/auth/password`:
  - `POST /forgot`;
  - `POST /resend` (no body);
  - `GET /recovery` (the position; never 404);
  - `POST /reset/check`;
  - `POST /reset` (the password only).
- **The position:** `RecoveryPosition` in `@masaha/shared/auth`. The steps are `request`, `sent` (the masked email, `resendInSeconds`, `canResend`) and `password` (the account's masked email).
- **The codes:** `RECOVERY_INVALID` and `RESEND_LIMIT_REACHED`, with their copy already in both catalogues.
- **The cookie** `masaha_reset` is `HttpOnly`: the browser carries it, and the web never reads it.

**The owner's decisions:**
- **The server is the source of the position** (Q1, R9). On load and after a reload, the page asks the API where the caller stands. It shows that step, and the resend countdown starts from the server's window.
  - A reload, or another tab, neither resets the countdown nor loses the "sent" step.
  - **No client storage** (no `localStorage`, no `sessionStorage`, no `history.state`) holds the step, the window or the email.
- **The credential never stays in the web** (Q2):
  - the reset page reads `#token` from the URL fragment, removes it from the address bar, and checks it;
  - the check binds it to the session, and the web keeps no copy;
  - setting the password sends only the new password;
  - a reload after the check keeps working, through the session.
- **Resend** sends no email (Q3), and is offered only while the position allows it.
- **The screen is derived from the state** (Q4): a pure function in the feature's `services/` decides which screen shows. **A failed read is not "start over":** it shows a retry, never sends the reader back to the beginning of a recovery the server still holds.
- **M4 — guards:**
  - `/forgot-password` stays under `RequireGuest`;
  - `/reset-password` has **no** guest guard: a signed-in person may open a reset link from their email;
  - record this exception in architecture.md §2.
- **M5 — after a successful reset:** the success state with a "Sign in" action, as designed. The API ends every session and opens none.
- **Where the code lives:**
  - the pages sit under `pages/site/auth/`, inside `FocusLayout`;
  - the logic is in `features/auth` (the recovery is the `auth` module's flow), per H1–H8: the repository, the hooks, components that only render (H6), and the derivation in `services/`.
- **Rate limits:** the server's `429` with `Retry-After` shows the existing m:ss countdown.

## 3. Your plan decides

- the feature's additions (the repository's calls, the hooks, the components, the screen-deriving service), and the pages' composition;
- the tests per testing.md:
  - the repository's calls in the unit lane;
  - the derivation service in the unit lane, every step and the failed read;
  - the hooks with renderHook through the transport's fake adapter;
  - the components on rendering only;
  - one test that the token leaves the address bar before any request is sent;
- the copy, from the designs; lines not in a design are listed for approval;
- the documents: architecture.md §2 (M4); `overview.md` › *Built*, if this is the last of F-5b3a/b/c to merge (otherwise say which is).

## 4. Out of scope

- Any API change. If the plan finds the API missing something, stop and report: don't build it here.
- Google, the account settings, and temporary passwords.

## 5. Parallel work

**Worker B** is working in `C:\Users\basel\masaha-b` on PR #39 (F-6c2, the dashboard shell), now being rebased and restructured.
- **It changes:** `pages/site/routes.tsx`, `RequireGuest` (now `landingPath`), `features/users` (a "Dashboard" item), `shared/routing/index.ts` and architecture.md §1–§3 (the per-file rule).
- **Declare your shared files in the plan:** `pages/site/routes.tsx`, `router.tsx`, `features/auth/index.ts`, architecture.md §2, the copy catalogues.
- **Whoever merges second** rebases and keeps both sides.

## 6. Pull request

- **Labels:** `feat`, `area:web`, `area:docs`.
- **Review:** one independent review, unless the plan changes how the credential is handled; then the review gate.
- **Screenshots** of every state (RTL and LTR, light and dark, phone and desktop) go to `C:\Users\basel\Downloads\f5b3c2-shots`, never committed.
- After CI is green, stop and report. No tool or AI attribution anywhere. Don't merge. Don't create an Issue.
