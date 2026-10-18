# Review — PR #38 (F-5b3c1: the forced password change, and the recovery session on the API)

You are the **independent reviewer** of PR #38 in `C:\Users\basel\masaha`. You don't build, fix or merge.

## Budget (hard limits — the owner's)

- **Exactly 2 subagents. Never a third,** not even an empty one. No workflows.
- **The whole review stays under 800,000 tokens**, this conversation and both subagents together. Aim for about 250,000 per subagent.
- **Read the diff, not the repository.** Use `git diff origin/main...a4e1685 -- <paths>` and `git show a4e1685:<file>`, only for files the PR changes, plus the few named below.
- **Read the documents only in the sections named.**
- **Reports:** at most 700 words per subagent, and at most 900 for yours.

## Rules

- **Read-only.** No edits, commits, checkouts, installs, npm or test runs, database commands, or GitHub comments.
- **Pin everything to commit `a4e1685`,** compared with `origin/main`. Prefix `git show` with `MSYS_NO_PATHCONV=1` if a path is mangled.
- **Report concrete problems only:** the file and line, the failing scenario, the severity (blocker / should-fix / nit) and the fix.

## What the PR must be (the owner's decisions)

### The recovery session (API)

**Q1 — the session:**
- the server holds the session, in an `HttpOnly` cookie `masaha_reset`;
- a request answers with the position (step, masked email, resend window, can-resend);
- **the answer and the cookie are identical for every address,** known or unknown, and reveal nothing about the account.

**Q2 — the credential:**
- the check binds the link's token to the session, or opens a session on another device (R2);
- the reset reads the token from the session;
- **a token in the reset's body is refused with 422** (R7);
- the web keeps no copy.

**Q3, R3–R5 — resending:**
- no email in the request; at most 3 resends; a 60-second window, the same for every address;
- it shares the forgot request's rate-limit budget, with no budget of its own.

**R1, R6, R9 — storage, cookie and position:**
- a table owned by `sessions`, which stores **no email address**, only a digest and a masked form (D2);
- the cookie is `SameSite=Strict`, `Secure` outside development, scoped to the password routes, cleared on success;
- its endpoints refuse cross-site requests;
- `GET /auth/password/recovery` never 404s.

**R8 — ADR 0017,** short and decision-level.

**Unchanged:**
- the reset link's token in the URL fragment;
- the per-recipient, requester and ceiling caps;
- B3's delivery-dependent replacement;
- every guarantee in `docs/backend/security.md`.

The email is still sent before the answer (ADR 0014), and finding 16 stays open.

### The forced change (web)

- **M1, the gate:** in `shared/routing`, mounted at `RootLayout`. It covers every route, the site's and the dashboard's. The change page and sign-out are exempt.
- **M2, the form:** in `features/users`, through `useServerForm`, `PasswordRules` and `FormFailure`. Components only render (H6).
- **M3, `passwordChanged(token)`** in `shared/session`.
- **M6, landing:** after the change, through `landingPath`, owned by a **guard**. No `onSuccess` and no navigating callback anywhere.
- **"Sign out"** reuses the existing sign-out; it is not a second copy.

### Project rules

- **No production parameter, option or callback that only tests pass or that nothing uses.** Tests stub the platform's own seams (`fakeTransport`, `vi.stubGlobal`).
- **Tests per layer:** testing.md, *A feature, layer by layer*.
- **Commit subjects** are 50 characters or fewer.

## The split

### Subagent 1 — the API: security and correctness

**Its files:** the PR's changes under `apps/api` (the schema, the migration, `modules/sessions`, `modules/auth`, `app.ts`) and `packages/shared` (auth, core errors).

**It reads only these sections:**
- `docs/backend/security.md` › *Tokens and cookies*, *Passwords*, *Rate limits*;
- `docs/backend/conventions.md` §13.

**It checks:**
- **Disclosure:** is anything different for a known vs an unknown address (body, cookie, status, headers, timing apart from finding 16)?
- **The token never leaves through a response or the logs.** Is the token bound in a transaction under the user lock?
- **Single use:** can a token be consumed twice, under a race?
- **The resend bound:** can it be passed in a race? Is the window enforced?
- **The shared budget:** truly shared, with no second budget?
- **Strict schemas:** the reset's body and the resend's body.
- **The cookie's attributes.** Cross-site is refused on all five endpoints.
- **The cascade:** the bound session ends when its link is deleted (a newer link delivered, a reset, a password change).
- **No email address stored.** Session expiry.
- **The migration:** correct and reversible-safe. The unrelated tables are untouched.
- **API tests:** they cover every refusal and the known/unknown equality. Would any pass with broken code?

### Subagent 2 — the web, the documents, the tests and the conformance

**Its files:**
- the PR's changes under `apps/web`: `shared/routing`, `shared/session`, `features/users`, `pages/site`, `app/`, the copy;
- `docs/`: the ADR, `api-contract.md`, `security.md`, `data-model.md`, `conventions.md`, `architecture.md`, `findings.md`, `foundation.md`;
- the commits;
- the PR body (`gh pr view 38 --json body`, read-only).

**It checks:**
- **The gate:** it covers every route; the exemptions are exact; there is no redirect loop; `next` is carried safely; guests and a restoring session pass.
- **`passwordChanged`:** it does nothing unless the user is signed in.
- **Landing:** owned by `RequirePasswordChange` through `landingPath`.
- **Sign-out:** reused (`useSignOutAction`), not copied.
- **H1–H8 and the export rule.** No test-only parameter anywhere.
- **The tests per layer,** and their titles against their assertions.
- **The documents state the new flow truly:** the ADR is decision-level, the contract matches the code, and nothing claims what isn't built.
- **The copy:** both catalogues, and the Arabic listed for approval.
- **The commits:** atomic, Conventional, 50 characters or fewer.

## Your output

Write **one file**, `C:\Users\basel\Downloads\REVIEW38_REPORT.md`:
1. **A verdict in one line.**
2. **The findings,** most severe first, deduplicated. Each gives the severity, the file and line, the scenario and the fix.
3. **"Verified OK":** a short list.

State the total tokens used. Then stop. The owner's analyst verifies the findings and writes the fixes list.
