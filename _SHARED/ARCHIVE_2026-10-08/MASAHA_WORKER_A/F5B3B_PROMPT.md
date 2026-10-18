# F-5b3b — Google sign-in on the web, and the first toasts

**Worker A** · main folder `C:\Users\basel\masaha` · branch `feat/google-sign-in`, cut from the latest
`origin/main` (the folder is on `main`, clean).

**Size cap:** at most 4 subagents in total, and **no self-review subagent** (an independent review
follows the PR). Do not run any workflow. Read the documents and sections named here; don't sweep the
repository.

## 1. How to work

- **Start with the `start-work-item` skill.** Plan in plan mode before writing code.
- **The owning documents, by section:**
  - `docs/frontend/architecture.md`: §1 (zones, `app/` and its providers), §2 (the guards, landing
    after sign-in, `RequireGuest`), §3 (feature layout, operation folders, "components present; hooks
    prepare", React Query side effects, what a feature exports, Forms), §4 (the session:
    `establishSession`, the account's language on sign-in);
  - `docs/api/api-contract.md` §5 › `POST /auth/google`, and §3 (error types);
  - `docs/backend/security.md` › *Sign-in methods* (Google: linking only where Google is the
    authority, the password removed on a link, `GOOGLE_LINK_NOT_ALLOWED`) and *Rate limits*;
  - `docs/development/testing.md` §1–§3 and *A feature, layer by layer*;
  - `docs/frontend/localisation.md` (the catalogues);
  - `docs/frontend/design-system/foundation.md` › the `Toast` row and z-index layers;
  - `docs/plans/foundation.md` › F-5b3b; `docs/development/setup.md` (environment).
- **The designs:** SCREENS.md rows 5 and 6; `docs/design/screens/06-sign-in/` (default, Google error,
  accounts-linked toast), `07-register/` (Google error), `05-auth-flow/` (the welcome toast).
- **When finished, follow the `open-pr` skill.**
- **The owner's rules:**
  - honest test titles;
  - **no parameter, option or callback that only tests pass or that nothing uses**; tests stub the
    platform's seams (`fakeTransport` / `fakeAdapter`, `vi.stubGlobal`, `vi.stubEnv`), never
    `vi.mock` of a module;
  - **pages pass no navigating callbacks**; guards own navigation;
  - **one responsibility per file**, and files grouped **by operation** inside `hooks/` and
    `components/` (architecture.md §3);
  - no hardcoded user-facing text; both catalogues; no colours or CSS outside the design system;
  - **checks:** lint and typecheck on each commit; the full lanes (`check:classes`, unit,
    component, api, build + `check:build`) once on the head, one at a time;
  - commit subjects of 50 characters or fewer; report only once CI is green on the pushed head;
  - review fixes fold into their commits, with ONE "Review fixes" comment;
  - **rebase only on a real conflict:** if GitHub shows the PR `CLEAN`, don't rebase on `main`;
  - no tool or AI attribution anywhere.

## 2. What this item delivers

The last of F-5b3: signing in (and up) with Google on the web, and the app's first toasts.

**The API is built and merged.** `POST /auth/google` takes `{ idToken, language? }` and answers
`Session & { linked }`; its errors are 422, 401 `GOOGLE_TOKEN_INVALID`, 409
`GOOGLE_LINK_NOT_ALLOWED`, 403 `ACCOUNT_SUSPENDED`, 503 while the API has no client id, and 429.
`GOOGLE_CLIENT_ID` in `apps/api/.env` sets the audience. The owner is setting up the Google Cloud
client (authorized JavaScript origin `http://localhost:5320`) and puts the id in the env files
himself; never ask for it, never print it.

**The design system already exports** `Toaster` and `toast` (Sonner); nothing mounts them yet.

## 3. The proposed decisions

These came out of the analysis and the owner agrees with them, **but they are proposals, not
orders.** You know the code best: if you find a stronger option for any of them, put it in your plan
under a dedicated section, **"Proposed alternatives"**, with its trade-off and your recommendation.
The owner and the analyst weigh it; build an alternative only once it is approved.

- **G1 — how the ID token is obtained:** Google Identity Services' own script, loaded from Google
  only on the sign-in and register pages, rendering **Google's official button** ("Continue with
  Google", outline; the filled-dark theme in dark mode; the interface's locale; full width). No npm
  dependency. (A custom button can't yield an ID token without a redirect flow and a nonce the API
  doesn't check; `@react-oauth/google` adds a dependency for the same script.)
- **G2 — the client id reaches the web as a build-time variable,** `VITE_GOOGLE_CLIENT_ID`, with a
  new `apps/web/.env.example` and a line in setup.md. **Without it, the button is not shown.** The
  web and the API must hold the same id; setup.md says so.
- **G3 — the Toaster is mounted once at the app's root** (`app/`), inside the direction and theme
  providers, so a toast survives the navigation that follows a sign-in. **Each capability's hook
  fires its own toast** from its mutation's own callback (the documented rule: what belongs to the
  capability lives in the hook). The session knows nothing of toasts.
- **G4 — three toasts in this item:**
  - after Google links an account (`linked: true`): a title, and a description saying the account's
    password was removed and can be set again with the reset email (security.md requires it; the
    design's one line is not enough);
  - the welcome after an email registration (the design's "أهلاً سارة، تم إنشاء حسابك", with the
    account's name);
  - "password saved" after the forced password change (`features/users`).
- **G5 — no welcome for an account Google creates:** the answer has `linked` but no `created`, and
  this item stays web-only. Record a finding: the API doesn't say whether Google created the
  account.
- **G6 — Google's failures get their own lines,** in a failure area of their own above the button
  (separate from the email form's failure), through `useRefusalView` (`shared/forms`):
  `GOOGLE_LINK_NOT_ALLOWED` guides the person to sign in with the password or reset it;
  `GOOGLE_TOKEN_INVALID`, `ACCOUNT_SUSPENDED`, the 503 (Google sign-in unavailable), 429 (the m:ss
  countdown) and no connection each get theirs. **Closing Google's window shows nothing.**
- **G7 — where the code lives:** `features/auth`, in a new operation folder `google-sign-in/`
  (`hooks/` and `components/`): the repository's call, a hook that loads the script and renders the
  button, the mutation hook, and **one exported component** with the button and its failure area. The
  two pages compose it above their forms, with the "أو" divider (page composition). The interface
  language goes in the body as `language`, as registration does.

**Fixed by the documents** (flag any you find no longer holds):
- after a Google sign-in, the session is handed to `establishSession(session, { source: 'signIn' })`
  in the mutation's own callback, and `RequireGuest` owns the landing (return URL, else
  `landingPath`); no navigating callback;
- a sign-in makes the account's language the interface's: **check the order** between that switch
  and the toast, so a toast never shows in the language being left;
- `overview.md` › *Built* (Authentication) is written by this item, the last of F-5b3a/b/c;
- TanStack Query's `retry` is off; the transport doesn't retry this `POST`.

## 4. Your plan decides

- the files and their names inside `google-sign-in/`; how the script is loaded once and cleaned up;
  how the button follows the theme and the language when they change;
- where exactly in `app/` the Toaster mounts, and its position and direction (RTL);
- the copy: every new line, both languages; **list the Arabic lines for the owner's approval**,
  including the linked toast's title and description and each Google failure line;
- the tests, per testing.md, one behaviour in one lane:
  - the repository's call in the unit lane (method, path, body with `language`, the unwrapped
    answer, a failure as `AppError`);
  - the hooks with `renderHook` through the fake adapter, the Google script stubbed as a global:
    the session established, the linked toast only when `linked`, each failure's view, a closed
    window showing nothing;
  - the component on rendering: the button shown with the client id and absent without it, the
    failure area, the accessible names;
  - each toast fired by its own hook (the welcome, the linked, the password saved);
- the documents: architecture.md (the Toaster in `app/`, the toast rule in §3), setup.md and the
  web's `.env.example`, `overview.md` › *Built*, `docs/plans/foundation.md` (F-5b3b built), and two
  findings: G5's, and **the deployment's headers** (a future CSP must allow Google's script and
  frames, and the Cross-Origin-Opener-Policy must allow Google's popup);
- the commits (a sketch: the Toaster with the two existing toasts; the Google sign-in; the docs that
  aren't already in those).

## 5. Out of scope

- **Any API change**, including a `created` flag (G5 records it). If the plan finds the API missing
  something, stop and report.
- One Tap, automatic sign-in prompts, and Google sign-out (`disableAutoSelect`) beyond what signing
  out already does.
- The account settings page and adding a password to a Google-only account.
- Deployment headers (recorded, not built); any npm dependency.

## 6. Parallel work

**Worker B** works in `C:\Users\basel\masaha-b`: PR #41 (the admin's lookups API, review fixes), then
S2a-2, the admin's governorates-and-areas screen: `features/lookups`, `pages/dashboard/admin/…`,
the dashboard's routes and navigation, and **the copy catalogues** (its own section).
- **Declare your shared files in the plan:** the copy catalogues (ar, en), `app/` (the providers),
  architecture.md (§1 and §3), `docs/architecture/findings.md` (numbering: whoever merges second
  renumbers).
- Edit them minimally, each side in its own section.
- Your databases are `masaha_dev` and `masaha_test`; web on 5320, API on 3320.

## 7. Pull request

- **Title:** `feat(auth): add Google sign-in` (or the main commit's subject).
- **Labels:** `feat`, `area:web`, `area:docs`. Assigned to the owner.
- **The description:** scope, acceptance criteria and out of scope; the decisions G1–G7 and any
  alternative approved; evidence per lane; what was not run.
- **Screenshots** of every state (the button in light and dark, RTL and LTR, phone and desktop; each
  Google failure; each toast) go to `C:\Users\basel\Downloads\f5b3b-shots`, never committed. The
  real Google flow is checked by hand once the owner's client id is in place; if it isn't yet, say
  so in the report.
- **Review:** an independent review, after you report.
- After CI is green on the pushed head, stop and report: the head, the commits, the counts per lane,
  your tokens. Don't merge. Don't create an Issue.
