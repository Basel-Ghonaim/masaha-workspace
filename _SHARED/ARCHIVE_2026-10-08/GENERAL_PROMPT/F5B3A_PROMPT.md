# F-5b3a — Sign in and register by email (the first feature)

**Worker A** · main folder `C:\Users\basel\masaha` · branch `feat/auth-email`

**Start only after F-5b2 (the session) is merged.** The owner will tell you.

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work

- **Start with the `start-work-item` skill.**
- **The owning documents for this item:**
  - `docs/frontend/architecture.md` (§1–§4, §7);
  - ADR 0004;
  - `docs/frontend/design-system/foundation.md` (§8, §11–§12);
  - `docs/frontend/localisation.md`;
  - `docs/backend/security.md` › *Passwords* and *Rate limits*;
  - `docs/api/api-contract.md` §3 and §5: `POST /auth/login`, `POST /auth/register`.
- **The designs:**
  - `docs/design/SCREENS.md` rows 5–6;
  - `docs/design/screens/06-sign-in/` (states 01–08), `07-register/` (01–14) and `05-auth-flow/`;
  - the prototypes `Sign in.html` and `Register.html`;
  - for the header's account menu, `17-settings/01-…` (the header).
- **Read the code you build on:**
  - `shared/session`, `shared/api`, `shared/routing` (F-5b2);
  - `pages/site/**` (F-6b);
  - `packages/shared/src/{auth,password,text,errors}.ts`;
  - the API's Zod-issue mapping in `apps/api/src/shared/validation/validate.ts`.
- **When finished, follow the `open-pr` skill.**
- **The owner's rules the skills don't carry yet:**
  - every test's title states what it asserts;
  - on a lockfile conflict, take main's `package-lock.json` and run `npm install`;
  - **report only once CI is green on the pushed head**;
  - **review fixes are folded into the commits they correct** (fixup + autosquash, `--force-with-lease`), with ONE "Review fixes" comment.

## 2. Context

F-5b, authentication on the web, is in three parts: **F-5b3a (this)**, sign in and register by email; F-5b3b, Google; F-5b3c, forgot, reset and the forced change. This is **the first feature in the project**: its shape, its React Query usage and its export rule become the pattern for every feature after it. Get the pattern right; the screens are its first use.

## 3. Decisions already made (do not reopen)

The owner approved these.

### Q1 — The feature's shape

A layer the capability doesn't need is **absent, not empty**.
```
features/auth/
  index.ts            the only entry (Q3)
  api/
    endpoints.ts      AuthEndpoints + createAuthEndpoints(client = api): server calls, no React
    mutations.ts      useSignIn, useRegister (useMutation)
    queries.ts        (useQuery hooks: none in this item, so absent)
    keys.ts           (query keys: none here, so absent)
  forms/
    signInForm.ts     the react-hook-form setup: defaults, resolver, server-error mapping
    registerForm.ts
  components/
    SignInForm.tsx    the fields, the submit and the error states
    RegisterForm.tsx
  model/              (the capability's own types: none here, so absent)
```
- **Q1a — growth:** a file that grows becomes a folder, with one file per resource, as the backend's growth rule says.
- **Q1b — folders by role** (architecture.md §1, set in F-5b2): a module groups its files into folders by role once it holds more than one role. Inner folders have no `index.ts`, and tests sit beside their files. The feature's folders above already follow it.
- **`AuthEndpoints`** holds only what this item calls: `login` and `register`. F-5b3b and F-5b3c add their own calls to it.

### Q2 — React Query in a feature

- **Q2a — one job per file:** `endpoints.ts` holds plain calls; `queries.ts` reads; `mutations.ts` writes; `keys.ts` holds the keys (scoped as architecture §7 says).
- **Q2b — side effects:**
  - **what belongs to the capability lives in the hook:** `useSignIn` and `useRegister` call `establishSession(session, { source: 'signIn' })` themselves;
  - **what belongs to the place lives in the page:** navigation after success comes from the page, through an `onSuccess` the page passes.
- **Q2c — names:** a verb and the resource (`useSignIn`, `useRegister`; later `useSpaces`).
- **Q2d — the cache:** no cache clearing on sign-in. Clearing happens on sign-out (F-5b2).
- **Q2e — tests:** they run the real path: the form, then the hook, then `endpoints`, then the transport, with `fakeAdapter` on `apiClient`. No test-only injection.

### Q3 — What a feature exports

> **A feature exports UI (components) first.** It exports a hook only when a higher layer needs the capability's data or actions to compose something the capability doesn't own. **Nothing internal leaves `index.ts`:** no endpoints, no keys, no form setup, no internal types. Outside sees only the abstractions the capability chooses to offer.

- **Q3a — one capability, several places.** Ask who owns the variation (screen ≠ capability):
  - **the places show the capability's own fact differently** → the feature exports the UI, with props or two components;
  - **a place mixes the capability with others, or arranges its own layout** → the feature exports small pieces or hooks, and the page composes.

  A component that combines several capabilities never lives in one of them: it lives in the page.
- **Here:** `index.ts` exports `SignInForm` and `RegisterForm` only. The page composes the card, the title, the links ("Create account", "Browse spaces without an account"), and later the Google button.

### Q4 — Dependencies

`react-hook-form` and `@hookform/resolvers` (ADR 0004). Check their current majors in the plan. Add nothing else.

### Q5 — `shared/forms`, the forms platform

One place every form uses:
- binding a Zod schema from `packages/shared` to the form;
- mapping a server `AppError` onto the form: `errors` (field → codes) become field errors, and a `code` or `type` becomes the form-level message;
- the browser's own validation produces **the same field-error codes** the server sends (Q6), so one catalogue line serves both.

### Q6 — One owner for the Zod-issue → field-code rule

- **Today:** the API's `validate.ts` maps Zod issues to the field-error codes.
- **Move it** to `packages/shared`, so the API's `validate()` and the web's forms both use it.
- **No behaviour change for the API:** its tests prove it.

### Q7 — The password rules checklist

- **The evaluation** lives in `packages/shared`, beside the policy (`password.ts`): a function saying which rules a value meets (at least 8 characters, a letter, a digit). The API's policy and the checklist then come from one source.
- **The presentation** lives in `shared/forms`, as a `PasswordRules` component: the rules ticking as the user types, as in `07-register/03–04`.
- **The policy itself is unchanged:** 8–72 characters, at least one letter and one digit (security.md). That is the owner's "medium" strength.

### Q8 — Features know no routes

No path is written inside a feature. Links and navigation are props the page passes.

### Q9 — Too many attempts

On `rate_limit` (429):
- show the design's state, with a countdown from `retryAfterSeconds`;
- keep the submit disabled until it reaches zero.

### Q10 — The header's account menu

- **Where:** after sign-in, the site header (F-6b's `SiteHeader`, and the phone menu) shows the account (the avatar and the name, as in the settings design's header) in place of "Sign in".
- **Its only item:** "Sign out", through `useSignOut()` from `shared/session`, with its pending and error states.
- **Later:** other account links come with their pages.

### Q11 — Field details

- the email field is `dir="ltr"`;
- the right `autocomplete` values (`email`, `current-password`, `new-password`);
- show and hide the password (the layer's `Input` with its `InputAction`);
- focus the first invalid field on submit.

### Q12 — Documents

- **`architecture.md` §3:** write Q1, Q2 and Q3 (with Q3a) as the feature rules. Replace "Whether a feature exports screens or only hooks is not decided yet". Fix the capability layout's `api.ts` line, which becomes the `api/` folder.
- **`architecture.md` §1:** the status line gains `shared/forms`.
- **`overview.md` › Built:** NOT yet. Authentication becomes Built with the last of F-5b3a/b/c.

### Q13 — Review

The full review gate: two independent reviews. This is the first feature, and its pattern repeats everywhere.

## 4. The pages (in `pages/site/auth/`)

- **`FocusLayout`**, in `pages/site/shell/`, as architecture §2's tree has it: the short header (wordmark, language and theme toggles) and no footer, per `11-variants/19-sign-in-…`.
- **The routes:** `/login` and `/register`, each visibly wrapped in `RequireGuest`, under `FocusLayout`. Lazy, like the rest of the site.
- **`SignInPage`:** the card (title, description), `SignInForm`, the "Forgot password?" link (to `/forgot-password`, which F-5b3c builds; until then it shows the 404), "No account? Create account", and "Browse spaces without an account".
  - **On success:** navigate to `safeReturnUrl(next)` (F-5b2).
  - **No Google button yet** (F-5b3b). Leave the card ready for it, with nothing rendered.
- **`RegisterPage`:** the card, `RegisterForm`, and "Already have an account? Sign in". On success, the same landing.
- **The states,** from the designs:
  - **sign in:** default; wrong email or password (`INVALID_CREDENTIALS`); account suspended (`ACCOUNT_SUSPENDED`); too many attempts (Q9); submitting; network error;
  - **register:** default; rules ticking (Q7); field errors; email already registered (`EMAIL_TAKEN`, on the email field); too many attempts; network error; submitting.

## 5. Tests

**The unit lane:**
- the Zod-issue → field-code mapping, from its new home;
- the password rules' evaluation;
- `shared/forms`' mapping of an `AppError` onto field and form errors;
- the API's existing `validate` tests stay green, unchanged.

**The component lane:**
- **`SignInForm` and `RegisterForm`,** each through the real path with `fakeAdapter`:
  - success calls `establishSession` with `signIn`, then the page's `onSuccess`;
  - every state of §4;
  - the countdown re-enables the submit;
  - the field errors from the server land on their fields;
  - client validation shows the same codes' text;
  - register sends the interface language;
- **`PasswordRules`:** it ticks each rule as the value changes;
- **the pages and routes:**
  - `/login` under `RequireGuest`: a signed-in user is redirected away;
  - after sign-in, the user lands on `next`;
- **the header's account menu:** it shows after sign-in; "Sign out" ends the session; a failed sign-out shows its error and keeps the session.

**The manual end-to-end check** (Evidence): with the database, the API and the web up:
1. register a new account;
2. sign out;
3. sign in with a wrong password, then with the right one;
4. reload: the session restores;
5. confirm the header shows the account.

**Screenshots** (`C:\Users\basel\Downloads\f5b3a-shots`, never committed): the states of §4 and the account menu, in RTL and LTR, light and dark, phone and desktop.

## 6. Parallel work — read this carefully

**Worker B** works at the same time in `C:\Users\basel\masaha-b` on **SH-1**, which restructures `packages/shared` by capability:
- `core/` (errors, envelope, pagination, fields, languages);
- `users/`, including `passwordPolicy.ts`;
- `auth/`, `space-links/`, `lookups/`;
- subpath imports such as `@masaha/shared/auth`, with no root barrel.

**Expect conflicts, and don't try to avoid them.** The owner decided to run both items side by side and resolve the conflicts. So:
- **Write your code in the structure that exists on `main` when you start.** Put the Zod-issue mapping (Q6) and the password rules' evaluation (Q7) in `packages/shared` beside their closest current files (`errors.ts` and `password.ts`), and import from `@masaha/shared`.
- **If SH-1 merges while you work,** the owner will tell you. Then, at a commit boundary:
  1. `git fetch` and rebase on `origin/main`;
  2. move your two additions into SH-1's structure: the field-code mapping into `core/` (beside `errors` or `fields`), the password rules into `users/passwordPolicy.ts`;
  3. switch your imports to the subpaths;
  4. resolve every conflict keeping both sides' intent, and re-run every lane.

  Each rewritten commit must still pass on its own. Say in the PR what moved in the rebase.
- **If you merge first,** worker B adapts SH-1 to your additions instead.
- **Your files, which B won't touch:** `features/auth/**`, `shared/forms/**`, `pages/site/auth/**`, `pages/site/shell/FocusLayout.tsx`, the header's account-menu parts, your copy entries, `architecture.md` §3 and §1's status line.
- **The shared zone:** `packages/shared` (your two additions against B's move); the importers of `@masaha/shared` in `apps/api` (`validate.ts`) and `apps/web`; `package-lock.json` (only you add dependencies; B adds none).

## 7. Commits

Propose the split in the plan. A likely one:
1. `feat(shared): share the field-code mapping and the password rules`: Q6 and Q7's evaluation, the API switched to it, tests
2. `feat(forms): add the forms platform`: `shared/forms`, `PasswordRules`, the dependencies, tests
3. `feat(auth): add sign-in and register forms`: `features/auth`, tests, architecture §3
4. `feat(site): add the sign-in and register pages`: `FocusLayout`, the routes, the pages, copy, tests
5. `feat(site): show the account in the header`: Q10

## 8. Pull request

- **Labels:** `feat`, `area:web`, `area:api`, `area:docs`.
- **The Arabic** for any line not in a design is listed for the owner's approval.
- **The review gate:** after CI is green, stop and report. Don't start fixes until the owner sends the list.
- No tool or AI attribution anywhere. Don't merge. Don't create an Issue.
