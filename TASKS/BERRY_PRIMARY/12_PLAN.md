# WI-B2 — the auth forms' main action, and the audit: the plan

> Prompt: `11_FOLLOWUP_PROMPT.md`. Small and decided: the plan is saved and the work goes on (headless).
> Base `main` = `95c33fe9` (#157, #158 merged). Branch `feat/auth-main-action`, expected PR **#159**.

## 1. The auth forms (WI-B's D4) — `variant="main"` on

| Where | Button | Why |
|---|---|---|
| `features/auth/components/sign-in/SignInForm.tsx` | submit | the form's submit (also the reset page's guest sign-in, C2, and the overlay's sign-in views) |
| `features/auth/components/register/RegisterForm.tsx` | submit | the form's submit (also the overlay's register view) |
| `features/auth/components/forgot-password/ForgotPasswordForm.tsx` | submit | the reset link's request (page and overlay) |
| `features/auth/components/reset-password/ResetPasswordForm.tsx` | submit | the reset form |
| `pages/site/auth/ResetPasswordPage.tsx` | `requestLinkLink`; the signed-in `signIn` link | each the one link of its state (link unusable; done, a session held) |
| `pages/site/auth/ForgotPasswordPage.tsx`, `pages/site/auth/in-place/ForgotView.tsx` | `resetPasswordLink` (LinkOpen's «متابعة») | the link-open state's one forward link; «enter email again» stays outline |

Unchanged: outline / link / ghost buttons (resend, set password by email, another email, way back, forgot-password
link, Google's own button), `RecoveryRetry` (a state), `SignInPrompt`'s back link.

**Tests** (one per form, seen failing first): `SignInForm`, `RegisterForm`, `ForgotPasswordCard` (the form's submit),
`ResetPasswordCard` (the form's submit), `resetPasswordPage` (request-link state, and the signed-in done link),
`forgotPasswordPage` (link-open «متابعة»), `inPlaceSignIn` (the overlay's sign-in submit is the one main action).

## 2. The audit

- **By the code:** every route in `pages/site/routes.tsx` and `pages/dashboard/routes.tsx`, and every Dialog /
  AlertDialog / Sheet / AdaptiveDialog under `features/**` and `pages/**`, listed with its `variant="main"` call
  sites against 6_PLAN §4.3's rule and table.
- **In Chrome** (headless over CDP, as WI-B's `berry.mjs`; light theme): guest, demo owner, admin; 1440 and 390;
  count visible `[data-slot="button"].bg-main-action` per route and per overlay opened without writing data. Dark on
  five screens: zero berry (B1). axe on the auth views. Pages of one user batched to stay under the refresh limiter
  (30 / 15 min).
- **Deviations:** a clear break (two in one view, a named one missing, berry in dark) is fixed as its own commit with a
  test seen failing first; a judgement is listed for the owner, unchanged.

## 3. Commits

1. `feat(auth): draw the forms' main action` — §1 and its tests.
2. one `fix(web): …` per clear deviation, if any.
3. `docs: …` only if a fix changes a document, or WI-B's follow-up note points here (closed).

## 4. Verification

`format:check`, `lint`, `typecheck`, `check:classes`, `check:links`, `check:conflicts`, `test:unit`,
`test:component`, production build, `check:build`, all through `heavy.mjs b2`. Chrome as §2; shots to
`Downloads\berry-audit-shots\`. Push, `open-pr`, green CI and `CLEAN`, `13_REPORT.md`. Never merge.

## Proposed alternatives

None: the task is decided. The LinkOpen «متابعة» is read as "a done state's one link" (its outline sibling is an
alternative, not a second main action); flagged in the report.
