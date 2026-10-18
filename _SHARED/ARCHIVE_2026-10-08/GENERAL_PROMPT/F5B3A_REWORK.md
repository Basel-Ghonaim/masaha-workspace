# F-5b3a — rework of PR #35 (the owner's structure decisions)

**Worker A** · main folder · branch `feat/auth-email` · PR #35

**Size cap:** at most 4 subagents; no workflows.

## 0. What this is, and what it is not

The owner reviewed PR #35's structure before the review gate and changed it. This is a **refactor of the work you already did**, not a restart:
- **Keep your work.** The shared field-code mapping and password rules, `CircleIcon`, the pages, `FocusLayout`, the account menu (with the `<bdi>` fix), the copy, the tests and the screenshots stay. You **move and reshape** code; you don't rewrite it from nothing.
- **Behaviour stays the same.** Every user-visible state, every test's assertion and the manual end-to-end check must hold afterwards, unless this file changes them.
- **At the end, you redraw the whole history** (§6): the final state is committed again as clean atomic units on top of the latest `main`. In between, work freely; temporary commits are fine.

**SH-1 (#34) is merged into `main`.** Rebase first (§1).

## 1. First: rebase on SH-1

1. `git fetch origin` and rebase `feat/auth-email` on `origin/main`.
2. **`packages/shared` now has one folder per capability, with subpath imports and no root barrel** (`docs/architecture/shared-package.md`). Move your two additions:
   - the Zod-issue → field-code mapping (`fieldErrors.ts`) goes into `core/`, exported from `core/index.ts`;
   - `passwordRules()` and `PASSWORD_RULES` go into `users/passwordPolicy.ts`.
3. **Switch every import** of `@masaha/shared` to its subpath (`@masaha/shared/core`, `/users`, `/auth`), including `validate.ts` in the API.
4. **Resolve each conflict keeping both sides' intent.** Run every lane before going on.

## 2. The owner's decisions (do not reopen)

### H1 — The feature's structure (replaces the earlier Q1 and Q2a)

A feature (and a shared module, where the roles apply) is grouped by **the kind of code**:
```
features/<capability>/
  index.ts        the only entry
  repository/     what fetches the data: the API calls (later also DTOs, mappers and request types,
                  split into files when it grows, for example types in one file and the calls in another)
  hooks/          React hooks: queries, mutations, form hooks
  components/     React components: presentation only (H6)
  services/       plain, non-React helpers
  types/          types shared inside the capability (only when a type is used in more than one place)
```
- A folder that would be empty is **absent**.
- **Names inside `hooks/`:**
  - `useXQuery` for a read;
  - `useX` for a write (`useSignIn`);
  - `useXForm` for a form;
  - query keys live in `hooks/queryKeys.ts`.

### H2 — One generic form hook, in `shared/forms`

Sign-in and register are one pattern. So is every form the project will have. `shared/forms` owns it once (for example `useServerForm`):
- **It takes:** the contract's schema, the default values, the fields in display order, and **the server call as an argument** (`submit: (values) => Promise<…>`).
- **It returns everything a component renders, ready** (H6):
  - the form's field bindings;
  - `submit`;
  - `isPending`;
  - each field's error as **text**;
  - the form's failure as a **view model** (H6).
- **It owns:** the resolver, `applyServerError`, the field-code → text mapping, and the failure's view model.

`useSignInForm` and `useRegisterForm` become thin. Each passes its schema, fields and call. Register adds the interface language.

### H3 — One exported unit per file, named after it

`hooks/useSignIn.ts`, `hooks/useSignInForm.ts`, `repository/authRepository.ts`, … No file groups several hooks.

### H4 — One name for the data layer: `repository`

- **features/auth:** `AuthRepository { login, register }` and `createAuthRepository(client = api)`, in `repository/authRepository.ts`.
- **shared/session, for consistency:**
  - `gateway/` becomes `repository/`, with `sessionRepository.ts` (`SessionRepository { refresh, logout }`, `createSessionRepository`), `sessionHint.ts`, and the default dependencies (today `gateway/dependencies.ts`);
  - rename every mention in the code, the tests and the documents.

  Do this as a pure move-and-rename: no behaviour change.

### H5 — The documents

Rewrite `docs/frontend/architecture.md` §3's feature rules to H1–H8:
- **replace** the earlier Q1 / Q2a shape and the `Endpoints` naming;
- **keep** what still holds: Q2b (the capability's effects in the hook, the place's in the page), Q2c's verbs, Q2d, Q2e, Q3 / Q3a (the export rule), Q8 (features know no routes);
- **update §1's folders-by-role rule** if its examples name `gateway/`.

### H6 — Components are presentation only

> **A component renders, and that is all.** It gets everything it needs from its hook, **ready to render**: values, actions (submit, retry), states (pending, disabled), and errors as **text and view models**. A component never touches `AppError`, error codes, `Retry-After`, a mutation, the transport or a query client.

**Applied here:**
- **The failure's interpretation** moves out of the components into a hook in `shared/forms` (for example `useFormFailure`), used by H2's form hook. That interpretation is:
  - rate limit with its countdown;
  - offline;
  - the general error with its `requestId`;
  - the title, the message and retry.

  The hook returns a view model, for example `{ kind, title, message, secondsLeft, requestId, retry }`.
- **`FormFailure`** takes that view model, not an `AppError`.
- **`fieldMessage`** moves into H2's hook: the component receives each field's text.
- **`SignInForm`, `RegisterForm` and the account menu** call their hook and render what it returns. `useRetryCountdown(failure)`, `fieldMessage(...)` and `AppError` disappear from every component.

### H7 — Where state lives (a summary of decisions already made)

Write it as one short list in §3, linking its owners:
- server data → TanStack Query (ADR 0004);
- global client state → Zustand (the session and the preferences);
- what must survive a reload or be shared by link (filters, views, the selected space) → the URL (ADR 0016);
- one component's own state → `useState`.

### H8 — Context inside a feature (EXPERIMENTAL: write it with this marker)

Write it in §3 exactly with its marker:

> **Context inside a feature** *(experimental: not part of the stable core; to be judged after its first use)*: only when several components of the capability, in one subtree, share client state that none of H7's places fits. The capability's own component mounts it; it is never exported.

No Context is built in this item.

## 3. The target shape of this item

```
features/auth/
  index.ts                 SignInForm, RegisterForm (unchanged surface)
  repository/authRepository.ts
  hooks/useSignIn.ts
  hooks/useRegister.ts
  hooks/useSignInForm.ts   thin: useServerForm(loginSchema, fields, signIn)
  hooks/useRegisterForm.ts thin: useServerForm(registerSchema, fields, register + language)
  components/SignInForm.tsx, RegisterForm.tsx (+ their tests)
shared/forms/
  index.ts
  validation/              schemaResolver, applyServerError, fieldMessage (internal now)
  hooks/                   useServerForm, useFormFailure, useRetryCountdown
  components/              FormFailure (view model), PasswordInput, PasswordRules
shared/session/
  repository/              sessionRepository.ts, sessionHint.ts, the default dependencies
  services/ hooks/ model.ts store.ts   (unchanged)
```

- **`shared/forms`' public surface** is what features need: `useServerForm`, `FormFailure`, `PasswordInput` and `PasswordRules`. Whether `schemaResolver` and `applyServerError` stay exported depends on whether anything outside still needs them; if nothing does, they become internal.
- **Propose any deviation** in a short plan (§5) before you build it.

## 4. Tests

- **Every existing behaviour test keeps passing.** Where a test exercised logic that moved from a component into a hook, the test moves with it, and its assertion stays the same.
- **New unit and component tests:**
  - `useServerForm`: the schema's field codes become field texts; the server's field errors land on their fields; a form-level failure becomes the view model; `isPending`;
  - `useFormFailure`: each kind (rate limit with its countdown reaching zero, offline with retry, the general error with its `requestId`);
  - `FormFailure` renders each view model.
- **A component test may not need an `AppError`** to render a failure state. Feed it through the real path (`fakeAdapter`), or through the hook's view model.
- **The renamed session layer:** the session's tests pass unchanged apart from the names.
- **Proof, in the PR's Evidence:**
  - every lane before (`31391a7`) and after, with counts;
  - the manual end-to-end check run again (all five steps);
  - the screenshots re-taken only if something visible changed (it shouldn't).

## 5. Plan first

Present a **short plan** (no more than about 40 lines) in plan mode:
- the target tree;
- `useServerForm`'s and `useFormFailure`'s signatures;
- the session rename;
- what moves where;
- the final commit list (§6).

Then wait for approval.

## 6. At the end: redraw the history

When everything passes on the final state:
1. **Rebuild the branch as clean atomic commits on top of the latest `origin/main`.** For example, `git reset --soft origin/main`, then stage by path and commit unit by unit. Never `git add -A` or `git add .`.
2. **A likely list** (propose yours in the plan):
   1. `docs(plans): split f-5b3 into three items`
   2. `feat(shared): share the field-code rule and password rules`
   3. `refactor(session): name its data layer repository`
   4. `feat(design-system): add the circle icon`
   5. `feat(forms): add the forms platform`
   6. `feat(auth): add sign-in and register forms` (with §3's rules H1–H8)
   7. `feat(site): add the sign-in and register pages`
   8. `feat(site): show the account in the header`
3. **Every commit:**
   - builds and passes lint, typecheck and the unit and component lanes on its own (check with `git rebase --exec … origin/main`);
   - has a subject of 50 characters or fewer;
   - is in Conventional Commits format, with no attribution.
4. **Push** with `--force-with-lease`, to this branch only.
5. **Update the PR description** to the final state. It names the owner's decisions H1–H8, the Arabic lines awaiting approval, the deviations and the Evidence.
6. **Wait for CI green on the new head, then stop and report.** The review gate (two independent reviews) runs on that head. Don't merge.

## 7. Also record

- **A finding:** `npm run format -- --check` writes files instead of only checking them. A check that rewrites is a trap. Record it in `docs/architecture/findings.md`; don't fix it here.
