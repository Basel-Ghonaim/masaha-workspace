# WI-C2 — Plan: sign in where the action is, the form inside the overlay

> Worker: Claude Code (Opus 5.5), worktree `C:\dev\masaha\app-design`, detached at `main` = `e0f9f66a`, clean.
> Prompt: `1_PLAN_AND_EXEC_PROMPT.md`. Status: **waiting for the owner's approval, and for #155 to merge.** Nothing is
> built and no branch is cut. Planned against C1's code as it stands on `feat/adaptive-dialog` (`96472181`, read
> only), which matches C1's approved plan. After the merge I check it again and say where it differs.

## 1. Summary

The guest's sign-in prompt (`SignInPrompt`, on C1's `AdaptiveDialog`) stops being two links to the pages. It
becomes the sign-in itself, over the page, on every page that mounts it: the space page, Directory and Home (their
hearts), and the space page's report. Its views:
- **sign in**: Google, or, e-mail, password, «نسيت كلمة المرور؟», «جديد على مساحة؟ إنشاء حساب»;
- **register**: titled by the reason, with the password's condition, the privacy policy opening in a new tab, and
  «لديك حساب؟ تسجيل الدخول»;
- **the reset link's request** and **the link sent**;
- **the password changed elsewhere** (A1).

A sign-in or register there closes the overlay, keeps the page, and runs the held action at once (the heart saved,
the report's dialog open), with no landing by role. A temporary password goes through today's gate, and the action
waits for the change. The overlay's forms are today's `features/auth` forms and hooks, loaded in a chunk of their own
when the overlay first opens; a new `check:build` rule keeps that chunk off the site's pages.

The reset link's page, when this browser holds a guest's action, says where it returns. Once the password is set, it
signs in right there and lands on the action's page, where the action runs.

**The names:** `SignInPrompt` and `useSignInPrompt` are kept (D3). The hook's API, `signIn(reason, cancel)`, is
unchanged, so the hearts and the report keep calling it as they do. The branch is `feat/sign-in-in-place`.

## 2. Contract

**Scope.**
- The overlay's views and states. Closing it on a sign-in, and the held action run in place.
- The action waiting out a forced password change.
- Google inside it. A1. The reset page's sign-in and its return line.
- The password's one-line condition, where D1 decides.
- The lazy chunk and its `check:build` rule.
- The documents and both catalogues.

**Acceptance criteria**
- [ ] A guest's heart or report opens the overlay, titled by the reason. Its sign-in view shows Google (when
      configured), «أو», e-mail, password with «إظهار», «نسيت كلمة المرور؟», the primary action, and «جديد على
      مساحة؟ إنشاء حساب».
- [ ] «إنشاء حساب» switches to register in place: titled «أنشئ حسابًا لحفظ المساحات في المفضّلة» / «…للإبلاغ عن
      معلومة» (NEW), with the typed e-mail carried over. The privacy link opens `/privacy` in a new tab. «لديك حساب؟
      تسجيل الدخول» goes back.
- [ ] «نسيت كلمة المرور؟» switches to the request, with the e-mail carried over and «العودة إلى تسجيل الدخول» above
      the title. Sent, it shows the link sent: the masked address, the resend with its m:ss clock, «استخدم بريدًا
      آخر» (the empty request, focus in the e-mail), and the NEW line naming the space and what completes after the
      reset.
- [ ] A1: while the overlay waits on the link sent (or the request), a reset completed in another tab of this browser
      turns it into the sign-in view, with the success notice (NEW), the e-mail filled and the focus in the password.
- [ ] Each state of the pictures is shown:
      - wrong credentials;
      - too many attempts (the clock, the submit off, nothing sent by itself);
      - Google unavailable;
      - Google's address taken, with «نسيت كلمة المرور؟» to the request;
      - the e-mail taken, with «سجّل الدخول بهذا البريد» to the sign-in, e-mail filled, focus in the password;
      - busy (no way of closing, the close button off).
- [ ] A sign-in, register or Google sign-in in place closes the overlay. The URL and the page stay; the focus returns
      to the heart or the report link; the held action runs once (the favourite saved and said «حُفظت {name} في
      المفضّلة» in the welcome's place; the report's dialog open). There is no navigation by role.
- [ ] A temporary password: today's gate takes the user to `/change-password?next=<this page>`, and the favourite
      or the report runs only after the change, never into a 403.
- [ ] Escape, the close button, the scrim and Back let the held action go, as today.
- [ ] The pages `/login`, `/register`, `/forgot-password` keep their behaviour. The header's «تسجيل الدخول» stays a
      link, and `RequireAuth`'s redirects stay.
- [ ] The reset page, when this browser holds a guest's action, says it returns to the space (NEW). Once the
      password is set, its sign-in sits on the card: the e-mail filled (D2), the focus in the password. Signing in
      lands on the action's page, where it runs. Without a held action, it lands as a page lands (`next`, else by
      role). A session still held at that point keeps today's link.
- [ ] The password's condition is one line: before typing, while typing, once met, and after a refused submit (D1).
- [ ] `features/auth` is a chunk of its own, not in the first download, and not reached statically by any chunk of
      `pages/site/public/` or `pages/site/shell/`. `check:build` fails otherwise, and was seen failing once.
- [ ] Tests (§9) in their lanes, each seen failing by its named break. The page tests not listed in §9 as rewritten
      stay green unchanged.
- [ ] Documents: architecture §2, §3, §4; `auth.md`, `favorites.md`, `data-reports.md`; both catalogues.

**Out of scope.**
- The berry primary button (WI-B). The overlay uses `Button`'s default and gets the berry when B merges.
- The full pages' redesign (WI-C3). The dashboard's sign-in paths. GOOGLE_VERIFY.
- Any API, schema, migration, dependency or database write.
- Prefetching on hover (D8).
- `foundation.md` and every design-system file. The overlay composes the layer as it is, so nothing is shared with
  WI-B.

## 3. Reading done

**Project and task:**
- CLAUDE.md; workflow (all); testing §3 and *a feature, layer by layer*.
- The map and its deferred table (nothing triggered); the open findings' titles (23, 65, 152, 215, 221: none touches
  this).
- `0_OWNER_DECISIONS.md` (every entry); `1_ANALYSIS.md` (all); ADR 0021.
- C1's prompt, `2_PLAN.md` and `2b_SUPERVISOR_REVIEW.md`. C1's branch, read only: `AdaptiveDialog.tsx`,
  `historyEntry.ts`, `opener.ts`, `SignInPrompt.tsx`, and its two doc hunks.

**Documents:**
- architecture §1, §2 (the groups, the landing and guards), §3 (the dashboard-only rule, heavy libraries, public
  entries, what a feature exports, forms), §4 (*Where state lives*, `shared/storage`, the session's events).
- `auth.md` (all); `favorites.md` and `data-reports.md` (the guest's press).

**Code:**
- **Auth:** `features/auth`: every form, hook and repository; Google's button, loader and failure; the forgotten
  password's and the reset's cards and flows.
- **Forms:** `shared/forms`: `useServerForm`, `useRefusalView`, `FormFailure`, `PasswordRules`, `usePasswordRules`.
- **Routing:** `heldIntent.ts`, `guestLeaving.ts`, `returnUrl.ts`, the four guards, `PasswordChangeGate`,
  `landingPath`.
- **The site:** `useGuestIntents`, `SiteLayout` (`ResumeFavorite`); `useSignInPrompt`, `useHeart`, `SpacePage`, the
  site's routes, the auth pages and `nextSearch`.
- **The actions:** favourites' intent, toggle, resume and toasts; data-reports' intent, `useReportAction`,
  `ReportAction`.
- **The session store.** The copy: `auth`, `site.signInPrompt`, `forms.passwordRules`.
- **Shared:** `PASSWORD_RULES`; `RecoveryPosition` (the e-mail is always masked).
- **Build:** `checkBuild.ts` and `libraryChunks.ts`; the test helpers (`warmLazy`, `fakeGoogle`, `fakeTransport`).

**Existing tests:** the tests that assert today's behaviour: `SpacePage.component.test.tsx`,
`resetPasswordPage.component.test.tsx`, `SignInPrompt.component.test.tsx`, `ResetPasswordCard.component.test.tsx`,
and the password checklist's six files.

**The prototype** (local clone at `b3b9f4d`):
- `decisions/Space details.md`; `Space details/inplace.jsx` + `.css`; `Reset password/inplace.jsx`.
- Captures: P2 rate, sent, register 1440, changed, register-taken, reset-done.

## 4. The settled decisions, as they will be built

### 4.1 The overlay: a light shell and a lazy body

**`SignInPrompt`** (pages/site/public; on every page's load, as today) is the shell. It holds what must not wait for
the chunk:
- the `AdaptiveDialog` and its content;
- **the header** (title, line), so the phone's focus target exists at once and never changes node;
- the view `signIn | register | forgot | changed`;
- the e-mail carried between views, in memory;
- `busy`.

The header comes from one pure function, `inPlaceHeading(reason, view, step)`, which reads the catalogue already
loaded:
- sign-in and changed: the reason's title and line (today's copy);
- register: the reason's register title (NEW) and `auth.register.description`;
- forgot, by the recovery's step: `forgotPassword.title` + `description`, `sentTitle`, or `linkOpenTitle`.

«العودة إلى تسجيل الدخول» is a link-styled button above the title in the forgot view, at every step.

**The body** (`pages/site/auth/in-place/`, loaded with `React.lazy` the first time the overlay opens, in a
`Suspense` with a short `Spinner` line):
- the views' forms, all from `features/auth`;
- the forgot view's step, reported up to the shell (`onStep`), which titles it.

If the chunk fails to load (offline), an error boundary inside the overlay shows the catalogue's no-connection line
and «إعادة المحاولة», which imports it again. Nothing is retried by itself.

**Focus on a view switch:**
- to the new title, in general;
- to the password: `changed` (A1), and «سجّل الدخول بهذا البريد»;
- to the e-mail: «استخدم بريدًا آخر», as today's C3.

On opening, the focus goes to the title at both widths (D4).

**Busy:** `features/auth` exports `useSignInBusy()`: true while a sign-in, register, Google sign-in, link request or
resend is under way. It reads the mutations' shared key, and the key stays internal. The shell passes it as the
`AdaptiveDialog`'s `busy`, so Escape, the scrim, the close button and Back are held, as C1 built.

### 4.2 After a sign-in in place

`useSignInPrompt` watches the session. When it becomes `authenticated` while the overlay is open (password, register
or Google), it closes the overlay **without** `cancel`. The action is kept.
- C1's `AdaptiveDialog` then goes back from its history entry and returns the focus to the heart or the report
  link.
- The held action is today's machinery, unchanged in path. The `signIn` sign-in in the tab that held it confirms the
  stored intent. Its path is this page, so `useGuestIntents` navigates nowhere (I4).
- `useResumeFavorite` saves once and says «حُفظت {name} في المفضّلة» under `RETURN_TOAST_ID`, in the welcome's
  place. `useReportAction` opens the report's dialog.
- A register is welcomed by name as today, then the save's toast (design issue 3).

### 4.3 The action waits for a forced change (I6)

A new pure `intentMayRun(session)` in `shared/routing` is true only for an authenticated session with no
`mustChangePassword`. `useResumeFavorite` and `useReportAction`'s `resumed` read it.
1. With a temporary password the gate redirects to `/change-password?next=<this page>`.
2. The favourite and the report stay held in memory, their 15 minutes running.
3. After the change, `RequirePasswordChange` lands on the page, and they run there.

Today this holds only because the gate unmounts the site shell in the same render. Now it is a stated rule with a
test.

### 4.4 Google in place

- `ContinueWithGoogle` sits at the top of both the sign-in and register views, at one place in the tree. Switching
  between them keeps it mounted: the same credential handler, and no redraw.
- The page has no other Google button, so the one module-level handler holds (I5).
- **GOOGLE_LINK_NOT_ALLOWED:** `ContinueWithGoogle` gains an optional `linkRefusedAction` slot. `FormFailure` gains
  an optional `action` for a refused view. The overlay passes «نسيت كلمة المرور؟» there, to the request view.
- **Executor checks, in Chrome, first** (I5; if any fails I stop and report the fallback, never change silently):
  - Tab reaches Google's iframe inside the trap, and leaves it;
  - the popup's credential returns and signs in;
  - the overlay's busy holds while the answer is pending.

### 4.5 The reset link's request in place and A1

**The forgot view** reuses `features/auth`:
- `useForgotPasswordFlow` (the server's step);
- `ForgotPasswordForm` (with `defaultEmail`);
- `LinkSentLines` and `ResendLinkForm`;
- «استخدم بريدًا آخر».

The cards keep their `Card` frames. The overlay arranges the same parts without one, so nothing is forked. A
`linkOpen` step (a link already checked in this browser) shows today's `LinkOpen`, its «متابعة» a link to
`/reset-password` in a new tab.

**The NEW line on the link sent** names the space from the stored intent (`heldIntentPreview()`, new in
`heldIntent.ts`, read without taking it). It shows only when an action is held in storage, since without storage the
promise could not be kept.

**At a link request or resend from the overlay**, `renewHeldIntent({ email })` (new) restamps the stored intent's
time and keeps the e-mail typed (D2, D5). It writes only when an intent is stored. It never creates one.

**A1:** `shared/routing` gains `onRecoveryDoneElsewhere(listener)`. It is the window's `storage` event for
`masaha.recoveredAt` written by another tab. The body listens while the forgot view is shown, and on it switches to
`changed`:
- the sign-in view under an `Alert` (`success`, `CircleCheckIcon`): «تم تغيير كلمة المرور» and «وسُجّل خروجك من كل
  الأجهزة. سجّل الدخول بكلمة المرور الجديدة.» (NEW);
- no Google block, the e-mail filled from memory, the focus in the password.

### 4.6 The reset page

`ResetPasswordPage` reads `heldIntentPreview()`.
- **With a held action:** the form step shows the NEW `Alert` (info): «بعد الحفظ سجّل الدخول هنا، ونعيدك إلى
  {space} لنكمل حفظها في مفضّلتك.», or for a report «…لتكمل بلاغك.».
- **Once the password is set and no session is held:** the done step holds the sign-in itself (`SignInForm`,
  `defaultEmail` from the stored intent per D2, the focus in the password). Its description names the return (NEW),
  or is today's `doneDescription`.
- **On the sign-in,** the page lands on `landingPath(user, ?next=<the confirmed intent's path, else the page's own
  next>)`.
  - The intent's path is taken with `takeIntentPath()`, so the site shell does not navigate again.
  - `returnUrlOf` checks it like any `next`.
  - The action then runs on its page, as the recovery's round trip already allows (`masaha.recoveredAt`).
- **No sign-in by itself:** the person types the new password again (ADR 0021 point 4).
- **A session still held after the reset's refresh** (another account's) keeps today's «تسجيل الدخول» link.
- `ResetPasswordCard`'s `signInLink` slot becomes a `signIn` slot (ReactNode), and it gains an optional
  `returnNote` slot. The feature still knows no route.

### 4.7 The held intent's shape

- **The report's intent carries the space's name,** as the favourite's does. `holdReport(slug, name)`;
  `ReportAction` passes the name it already has. This lets the sent line and the reset page name the space.
- **An optional `email`**, written only by `renewHeldIntent` (D2), removed with the intent.
- **When the intent is read,** its path is checked by `returnUrlOf`'s rule (S1).

### 4.8 The forms (features/auth), shared by the pages and the overlay

- `SignInForm`, `RegisterForm` and `ForgotPasswordForm` take optional `defaultEmail` and `onEmailChange`. The
  overlay carries the e-mail between views; the password never leaves its form.
- `SignInForm` takes `focusPassword`.
- Every e-mail input gets `inputMode="email"` and `enterKeyHint="next"` (or `"send"` alone). The password inputs get
  `enterKeyHint="done"` (I15). The pages get them too, with no change of behaviour.

### 4.9 The lazy chunk and `check:build` (I8)

- **The chunk:** `scripts/signInChunk.ts` names a `sign-in` chunk, every module under `src/features/auth/`.
  `vite.config.ts`'s groups make it, before `dashboard-shared`.
- **The rule:** `check:build` refuses:
  - a build with no such chunk;
  - the chunk in the first download;
  - any chunk of `src/pages/site/public/` or `src/pages/site/shell/` whose static imports, deeply, reach it.
- **Allowed by design:** the auth pages (`pages/site/auth/`, the in-place body included) and the account's settings
  (`SetPasswordByEmail`) load it.
- **Seen failing:** a static import of a `features/auth` export in `SignInPrompt.tsx`.
- **No prefetch** (D8).

### 4.10 The password's condition (A7), where D1 decides

**One line under the password** (its `aria-describedby`, `aria-live="polite"`; the text changes only when what is
missing changes):
- before typing: «8 أحرف على الأقل، فيها حرف ورقم»;
- while typing: only what is missing, «ينقصها: رقم» / «ينقصها: حرف ورقم» / «ينقصها: {n} أحرف أخرى» (NEW wording,
  for approval);
- met: «✓ كلمة المرور مناسبة», in `text-success`;
- too long: «طويلة جدًا — اختصرها» (today's);
- after a refused submit: the missing part in `text-destructive`.

It is still computed from `passwordRules`, so it says exactly what the server accepts. `PasswordRules` and
`usePasswordRules` keep their names and props; the view's shape changes.

## 5. Stronger decisions

- **S1. The held intent's path is checked as `next` is.**
  - What: `isIntent` accepts any path that starts with `/` and not `//`, so `/\host` passes. Today the site shell
    navigates to it (the browser then refuses a cross-origin `pushState`: an exception, not a redirect). Reading it
    with `returnUrlOf`'s rule closes that, and makes "`next` validated everywhere" true of the intent's path too.
  - Why: only a script of this origin writes the key, but this is defence in depth on the one return path the
    overlay's reset adds.
  - Cost: one line and two unit cases. **Recommended.**
- **S2. The action's wait for a forced change becomes a rule** (§4.3), not a render-order accident.
  - Cost: one pure function, two call sites, a unit test and a component test. **Recommended.**
- **S3. The held intent is renewed at a link request** (§4.5, D5).
  - Why: the NEW line promises the action completes after the reset. A reset that takes longer than 15 minutes
    would break the promise silently.
  - Cost: one function.
  - **Recommended.** Bounded: 15 minutes from the last request or resend, only for an intent already held.
- **S4. Focus on every view switch** (§4.1). The pictures do not say; without it, the pressed button unmounts and the
  focus falls to the dialog's container. **Recommended.**
- **S5. A chunk that fails to load** gets the overlay's own retry (§4.1), so a guest offline is not left with a
  spinner. **Recommended.**
- **No rule of the documents is weakened.** The rules held:
  - **Catalogue:** every string goes through it, in both languages.
  - **Design system:** semantic tokens and logical classes only; no file of the layer is touched.
  - **Features know no routes:** links and views are the page's slots.
  - **`shared/storage`:** it stays the only way to storage. The A1 listener reads the key's name from `STORAGE_KEYS`
    and the value through `storage`.
  - **What changes, and is written down:** architecture §4's "the `storage` event is heard by the preferences alone"
    gains A1.

## 6. Related findings

- The open findings (23, 65, 152, 215, 221) do not touch this item. **None folded.**
- Nothing in today's code needs a finding yet.
  - S1 is fixed in place, as part of this item's security condition.
  - Anything found during the work is recorded at the next free number of the index after #155 (C1 said "230 or
    next"), and named in the report.

## 7. Files

**New:**
- `apps/web/src/pages/site/auth/in-place/InPlaceSignIn.tsx`: the lazy body, the view's body by `view`.
- `apps/web/src/pages/site/auth/in-place/` views:
  - `SignInView.tsx`, `RegisterView.tsx`, `ForgotView.tsx`;
  - `ChangedNotice.tsx`;
  - `PrivacyLine.tsx` (the new-tab link).
- `apps/web/src/pages/site/auth/in-place/inPlaceSignIn.component.test.tsx`.
- `apps/web/src/pages/site/public/inPlaceHeading.ts` + `.unit.test.ts`.
- `apps/web/src/pages/site/public/SignInPromptFallback.tsx`: the loading line and the chunk's retry.
- `apps/web/src/shared/routing/guest/intentMayRun.ts` + `.unit.test.ts`.
- `apps/web/src/shared/routing/guest/recoveryElsewhere.ts` + `.unit.test.ts`.
- `apps/web/src/features/auth/hooks/useSignInBusy.ts` + `.component.test.tsx`.
- `apps/web/scripts/signInChunk.ts`.

**Edited:**
- **The prompt:** `pages/site/public/SignInPrompt.tsx`, `useSignInPrompt.tsx`, and
  `SignInPrompt.component.test.tsx` (rewritten: the links are gone).
- **The pages:** `pages/site/auth/ResetPasswordPage.tsx` and `resetPasswordPage.component.test.tsx`.
- **`pages/site/public/space/SpacePage.component.test.tsx`:** one assertion (§9, *Rewritten by design*).
- **Routing:** `shared/routing/guest/heldIntent.ts` (preview, renew, e-mail, S1) + `heldIntent.unit.test.ts`, and
  `shared/routing/index.ts`.
- **`features/auth`:**
  - forms and hooks: `SignInForm`, `RegisterForm`, `ForgotPasswordForm` (+ their hooks for `defaultEmail`);
  - `ContinueWithGoogle` (+ `useGoogleFailure` for the slot);
  - `ResetPasswordCard`;
  - the mutations' key: `queryKeys.ts`, `useSignIn`, `useRegister`, `useGoogleSignIn`, `useRequestLink`,
    `useResendLink`;
  - `index.ts`;
  - their existing tests, only where a slot was renamed (`ResetPasswordCard`'s «Sign in» slot).
- **`shared/forms`:** `FormFailure` and `FormFailureView` (`action`). For D1: `PasswordRules`, `usePasswordRules`,
  `PasswordRulesView` and their tests.
- **`features/favorites`:** `hooks/resume/useResumeFavorite.ts` + test.
- **`features/data-reports`:**
  - `hooks/intent/reportIntent.ts` + unit test;
  - `hooks/report/useReportAction.ts` + test;
  - `components/report/ReportAction.tsx`.
- **D1, if everywhere:** the assertions of `RegisterForm`, `useRegisterForm`, and `features/users`'
  `ForcedPasswordChangeForm` and `useForcedPasswordChangeForm` tests on the list. No `users` production file.
- **Copy:** `shared/copy/{arabic,english}/` `auth.ts`, `site.ts`, and `forms.ts` (D1).
- **Build:** `apps/web/vite.config.ts`, `scripts/checkBuild.ts`, `scripts/checkBuild.unit.test.ts`.
- **Docs:**
  - `docs/frontend/architecture.md`: §2, the landing's two cases and the intent's run; §3, the sign-in chunk; §4,
    *Where state lives* and `shared/storage`'s `storage` event;
  - `docs/features/auth.md`, `favorites.md`, `data-reports.md`.

**About 45–55 files** (say so; the workflow's review threshold of 25 is passed, and it touches auth: a separate
review follows, as planned).

**Shared with another open item:**
- **#155 (C1):** merged before I branch.
- **WI-B, beside me:** I touch no design-system file and not `foundation.md`. Shared documents and catalogue lines
  are append-only per section. Checked again at the report with `git merge-tree` against B's head.
- **No other layer**, no licence.

## 8. Design issues (built only once approved)

1. **Too many attempts.** The picture draws a red line above the button. Production's form pattern shows a warning
   `Alert` above the fields with the same clock, and the submit off; the pages and every form use it.
   - **Recommended:** keep production's, one pattern for every form. The words and the clock are the picture's.
2. **Google unavailable.** The picture uses a warning `Alert`; production shows every refusal as destructive.
   - **Recommended:** keep production's. A tone for one refusal would add a variant to the shared failure for one
     case.
   - The alternative, if the owner prefers the picture: a `tone` on the refused view, warning for
     `service_unavailable` and the script's failure.
3. **The register's toasts.** The picture shows one toast (the welcome, with the save under it). Production says the
   welcome by name, then the save under `RETURN_TOAST_ID`, so two toasts (as today's round trip through `/register`).
   - **Recommended:** keep production's. Merging them changes favourites' toast for one path.
4. **«جديد على مساحة؟»** is not in production (the page says «ليس لديك حساب؟»). The prompt names it, so the overlay
   uses it as a new catalogue line; the page keeps its own until WI-C3.
5. **The privacy link opening a new tab** gives no warning that it does. **Recommended:** a visually hidden «(تفتح
   في تبويب جديد)» / "(opens in a new tab)" (NEW), as WCAG's G201 advises.
6. **On desktop, the picture's first focus** is Google's button (Radix's default). With the body lazy and Google's
   button an iframe that may not take the focus, the title is the one stable target (D4).
7. **The link sent:** the picture puts «استخدم بريدًا آخر» as a centred link; production uses an outline button.
   **Recommended:** the picture's link inside the overlay. The parts are reused, only the arrangement differs.

## 9. Tests

Every new test is seen failing by the break named, then restored.
- Breaks marked † are made once (security or ordering), as testing §3 rule 7 says.
- The files that render lazy routes warm the overlay's body and the routes in a `beforeAll` (rule 8).
- Widths are set with `stubScreenWidth`.

**Component — `pages/site/auth/in-place/inPlaceSignIn.component.test.tsx`** (the space page in the site's routes, a
browser router for Back)

| # | Proves | Break that fails it |
|---|---|---|
| 1 | From the heart: sign in → the overlay closes, `post /me/favorites/7` once, «حُفظت Noor Hub…» toast, the heart pressed and focused, the location and the history length as before opening | navigate by `landingPath` after sign-in †; or close with `cancel` |
| 2 | From the report: sign in → the report's dialog opens, the welcome toast shown | `useReportAction` ignoring the held report |
| 3 | Register in place: the reason's register title, the e-mail carried, the account made, the favourite saved | register view titled «إنشاء حساب»; e-mail not carried |
| 4 | Google in place (`fakeGoogle`): the button in the overlay, its credential signs in, the favourite saved; switching to register keeps one handler (one request per credential) | unregister the handler on view switch |
| 5 | Wrong credentials: the refusal shown, the overlay open, the action still held (a later in-place sign-in saves it), the password field focused | close the overlay on any settle |
| 6 | 429 with `Retry-After: 300`: «…حاول بعد 5:00», the submit off, no request until the clock ends (fake timers) | not disabling while blocked |
| 7 | A temporary password: lands on `/change-password?next=%2Fspaces%2Fnoor-hub`, no `post /me/favorites/7`; after `passwordChanged`, back on the space, one post | drop `mustChangePassword` from `intentMayRun` † |
| 8 | `it.each` Escape, the close button, Back: closed, then a sign-in elsewhere saves nothing | closing without `cancel` |
| 9 | Busy: while the sign-in is pending, Escape and Back keep it open and the close button is disabled | `busy` not passed (`useSignInBusy` → false) |
| 10 | «نسيت كلمة المرور؟» → the request with the e-mail carried and «العودة إلى تسجيل الدخول» above the title; sent → the masked address, the resend clock, «استخدم بريدًا آخر» (the empty request, the e-mail focused), the NEW line naming Noor Hub | the e-mail not carried; the line without the preview |
| 11 | A1: on the link sent, a `storage` event for `masaha.recoveredAt` → the sign-in, the notice, the e-mail filled, the focus in the password; an event for another key changes nothing | remove the listener |
| 12 | Register's e-mail taken → «سجّل الدخول بهذا البريد» → the sign-in, the e-mail filled, the password focused | the button keeping the register view |
| 13 | Google's address taken → «نسيت كلمة المرور؟» in its alert → the request view | the slot not rendered |
| 14 | The privacy link: `href="/privacy"`, `target="_blank"`, `rel` with `noopener`, its hidden «(opens in a new tab)» | a plain router link |
| 15 | No held action (its 15 minutes past, fake timers): a sign-in in place only signs in and closes, no post (I10) | resume without the hold |
| 16 | At 390: the panel, the focus on the title at opening and on the new title at each switch; axe on sign-in, register, forgot, sent, changed at 390 and 1280 | no focus move on a switch |
| 17 | A link request from the overlay renews the stored intent's time and keeps the e-mail; none stored, none written | `renewHeldIntent` creating an intent |

**Component — `resetPasswordPage.component.test.tsx`** (new cases)

| # | Proves | Break |
|---|---|---|
| R1 | A favourite held in storage: the form step's NEW line names the space; once set, the done step's sign-in has the e-mail filled (D2) and the password focused; signing in lands on `/spaces/noor-hub` and its save is posted | land by `landingPath` without the intent's path |
| R2 | No held action: the done step's sign-in lands on the page's `next`, else by role (a visitor: `/`) | ignore `next` |
| R3 | A held intent whose path is `/\evil.example` is never followed (lands on `/`) | `isIntent` without S1 † |
| R4 | A session held at the done step keeps today's link to sign in | always render the form |

**Component — elsewhere:**
- `useSignInBusy` (true across each of the five mutations; break: a mutation without the key);
- `useResumeFavorite` / `useReportAction` (nothing runs while a change is pending);
- `ContinueWithGoogle` (the refusal's slot, only for GOOGLE_LINK_NOT_ALLOWED);
- `FormFailure` (the action);
- the forms' `defaultEmail` / `onEmailChange` / `focusPassword`;
- D1's line in `PasswordRules` (each state and its announcement).

**Unit**

| File | Proves | Break |
|---|---|---|
| `intentMayRun` | anonymous, restoring, a pending change: false; authenticated: true | drop a clause |
| `heldIntent` | the preview reads without removing and refuses an expired or malformed intent; renew restamps and adds the e-mail only to a stored intent; drop removes the e-mail; S1 refuses `/\host` and `/.//host` | preview that takes; renew that creates; S1 removed † |
| `recoveryElsewhere` | the listener runs for `masaha.recoveredAt` with a value, not for another key or a removal | the key check |
| `reportIntent` | the report's intent carries the name | the name dropped |
| `inPlaceHeading` | each view's and step's title and line, by reason; register keeps the reason | register's generic title |
| `checkBuild` | `signInProblems`: no chunk; the chunk in the first download; a public page and the shell reaching it; an auth page reaching it allowed | drop the page reach check |
| D1's pure line (if built) | the missing parts by value | the length counted in bytes |

**Rewritten by design** (they assert what the prompt changes; every other existing test stays unchanged):
- `SignInPrompt.component.test.tsx` (C1's): the two links are gone. Its focus and Back cases are kept against the
  form.
- `SpacePage.component.test.tsx`, *"asks a guest to sign in to report…"*: its one assertion of the prompt's
  `/login` link becomes the form's sign-in button.
- `resetPasswordPage.component.test.tsx`, *"links to sign in once the password is set…"*, *"carries the return
  page to sign in… after"*, *"marks the recovery done…"*: the link after the set becomes the form. The "before"
  half and the way back stay.
- `ResetPasswordCard.component.test.tsx`, *"says the password was set, and offers to sign in"*: the slot's name.
- D1 everywhere: the six checklist tests assert the line instead of the list.

**`check:build`:** run once with the break of §4.9 and seen failing, then restored.

## 10. Review Focus (inputs no planned test exercises)

- **Google's real iframe and popup inside Radix's trap,** at both widths. The component lane fakes Google, so the
  Chrome pass is its only proof (§4.4).
- **A temporary password's history:** the gate's replace and C1's going back from the entry race on a lazy route. The
  expected end is `/change-password` with no dead Back entry; checked in Chrome. If it shows a hop, the order is
  fixed and reported.
- **The real loading line on a slow 3G profile,** and the chunk's retry offline (Chrome's throttling).
- **A1 when the reset tab signs in first:** the waiting tab's sign-in then saves the same favourite again. It is
  idempotent, but a second toast shows. Stated, not fixed.
- **The phone's keyboard and password manager** (`enterKeyHint`, autofill into a lazily mounted form), and iOS's
  edge swipe. No real device here.
- **Directory and Home:** the overlay over a card's heart. The same component, checked once in Chrome, no separate
  test.
- **A guest who leaves the overlay open past 15 minutes:** the sign-in only signs in (test 15). The guest sees no
  saved favourite and is not told. Is that acceptable? (The analysis's I10 says yes.)

## 11. Commits

Each commit has a body, a subject of 50 characters or fewer, and no attribution. `#PRNUM` in the documents is
replaced just before the push (expected #156, after checking the PR and Issue lists).

1. `feat(forms): password condition as one line`: D1's line, its catalogue, its tests (and the checklist tests'
   assertions). If D1 chooses "overlay and reset page only", this becomes a variant inside step 3's commit instead.
2. `feat(auth): share the e-mail between auth forms`:
   - `defaultEmail`, `onEmailChange`, `focusPassword`;
   - the input hints;
   - `useSignInBusy` and its key;
   - the Google refusal's slot and `FormFailure`'s action;
   - their tests.
3. `feat(site): sign in where the action is`:
   - the shell and the lazy body: sign-in, register, Google;
   - closing on the session; `intentMayRun` in the favourite and the report;
   - the catalogue lines; tests 1–9, 12–16, the units;
   - architecture §2 (the landing's two cases, the intent's run), `auth.md`, `favorites.md`, `data-reports.md`.
4. `feat(site): ask for a reset link in place`:
   - the forgot view;
   - the preview and renew of the held intent (S3, D2), and the report's name;
   - A1's listener;
   - tests 10, 11, 17 and the units;
   - architecture §4, `auth.md`.
5. `feat(auth): sign in on the reset page`:
   - the reset page's return line, its sign-in and its landing, and S1;
   - R1–R4 and the rewritten reset tests;
   - architecture §2, `auth.md`.
6. `chore(build): keep the sign-in off site pages`: the chunk group, the rule, its unit tests, architecture §3.

## 12. Verification

- **Heavy commands** go through `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs c2 …` from the
  worktree's root, one at a time.
- **On the head:**
  - `format:check`, `lint`, `typecheck`, `check:classes`, `check:links`, `check:conflicts`;
  - `test:unit`, `test:component`;
  - `build` with `NODE_ENV=production`, then `check:build`, the new rule seen failing once.
  - A run killed for memory is retried once, then CI judges, and the report says so.
- **Not run:** `test:api` (no API change; CI runs it).
- **Chrome** (the API on 3323, the web on 5323, `masaha_dev`; the browser pane shown before each layout or axe
  check):
  - as a guest on a space page, at 390 and 1440, Arabic and English, light and dark:
    - the heart → sign in → saved, the focus back;
    - the report → sign in → its dialog;
    - register in place; the request → the link sent; A1 with a second tab;
    - wrong password; Back and Escape;
    - Google's checks (§4.4);
  - a temporary password's account (seeded by the admin's issue, through the UI);
  - the reset page's sign-in landing;
  - axe on each view.
  - Shots go to `C:\Users\basel\Downloads\c2-shots\`, curated.
  - Servers are stopped by PID and the ports checked free. If the memory guard stops them, I restart them once at
    ≥ 4 GB free; if that fails, I skip the pass and say so.
- **The PR:** push, open it with `open-pr`, wait for `gh pr checks` to be green on the pushed head and for `CLEAN`.
  Then `4_REPORT.md` with `final-report`. **Never merge.**

## 13. Decisions needed from the owner

- **D1 — where the password's one line lands.**
  - **Recommended: the shared `PasswordRules` everywhere it shows** (register, the reset, the forced change, the
    account's change). One pattern for one policy. A7 chose it for the auth pages, and the change forms are the
    same rule.
  - Cost: the six checklist tests' assertions rewritten; no production file of `users` changes.
  - The alternative: the overlay's register and the reset page only, through a variant prop. Two patterns side by
    side until WI-C3.
- **D2 — the reset page's e-mail filled.** The e-mailed link carries no address (the API builds it; masked
  everywhere). To fill it in another tab, the e-mail must be in this browser's storage.
  - **Recommended: A.** Keep the e-mail the guest typed in the overlay's request inside the stored held intent: only
    when an action is held, for its 15 minutes, removed when it runs, closes or expires. It is an identifier the
    same device typed, never a credential.
  - **B.** Store nothing: the reset page's sign-in opens with the e-mail empty and the focus in it (autofill helps).
    A1's waiting tab fills it either way, from memory.
- **D3 — the names:** keep `SignInPrompt` / `useSignInPrompt` (the API unchanged, no churn in favourites and
  data-reports). Recommended.
- **D4 — the first focus at both widths is the title**, not Google or the e-mail on desktop (design issue 6).
  Recommended.
- **D5 — S3, renewing the held intent at a link request or resend.** Recommended.
- **D6 — the tests rewritten by design** (§9) instead of "the existing page tests stay green unchanged", which cannot
  hold where a test asserts the links this item removes. Approve the list.
- **D7 — S1, the intent's path checked as `next`.** Recommended.
- **D8 — no prefetch on the heart's hover or focus:**
  - the press is the signal, and the body is small (measured and reported);
  - a prefetch would need the heart and the report, two capabilities, to know a page's chunk.
- **The NEW words** (for approval in both languages):
  - the register titles;
  - the sent line ×2;
  - the changed notice;
  - the reset page's return line ×2 and its done line ×2;
  - «جديد على مساحة؟»;
  - D1's "missing" lines;
  - the hidden «(تفتح في تبويب جديد)»;
  - the overlay's loading line.

## Proposed alternatives

1. **"When the recovery carries a `next` from the overlay"** (item 4) cannot hold as written. The e-mailed link
   carries no `next`: the API builds it, and the API is out of scope. The reset page learns the return from this
   browser's held intent instead (§4.6), which is exactly the case the line serves. On another device there is no
   held action, and the page is today's (the analysis's A3).
2. **"Existing page tests stay green unchanged"**: the tests that assert the removed links are rewritten (D6). No
   other test is touched.
3. **I15's «رجوع» in the top bar** is superseded by the prompt's and the picture's «العودة إلى تسجيل الدخول» above
   the title. C1's bar holds only the close button. Kept as the picture.
