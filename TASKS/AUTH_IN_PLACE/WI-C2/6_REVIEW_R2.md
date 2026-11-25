# WI-C2 — review R2 (experience, accessibility, the PR as a whole) of PR #157

> Head `305c5d3f39fd133e94f0a14b36c6a12914346fde`, read-only (diff, `git show`, `gh`, the code). CI is green on this
> head (all 10 checks) and the merge state is `CLEAN`. Nothing was built or run. Paths are relative to the
> repository root.

## 1. Verdict

**Mergeable after a fix round.** It has no blocker. Two fixes need code (the focus on the link sent, and one test
assertion). One fix is to a document. Three checks from the plan's Review Focus were never done and must be done or
accepted.

## 2. Requirements

**R2.1: the flows match the approved pictures and decisions. PASS.**
- **Heart:** `inPlaceSignIn.component.test.tsx:155-170` (closes, one `post /me/favorites/7`, the toast, the URL,
  the focus on the heart).
- **Report:** `:172-189`. **Register in place:** `:191-216`. **The reset request in place:** `:368-411`.
- **The link sent's NEW line:** `SentNote.tsx:13-24`. The words match the prototype
  (`Space details/inplace.jsx:210-211`).
- **A1:** `InPlaceSignIn.tsx:65-70`, tested at `:413-440`.
- **The reset page:** its return line, the sign-in on its card, and its landing
  (`ResetPasswordPage.tsx:29,40-45,79`; test `resetPasswordPage.component.test.tsx:181-205`).
- **I3:** the header link, `RequireAuth` and the auth pages are untouched; none is in the 90 files.
- **The rest of the pictures** is as approved:
  - the changed view drops Google and puts the notice above the form;
  - «العودة إلى تسجيل الدخول» sits above the title;
  - the privacy policy opens in a new tab.
- **One caveat:** the action *done* after the reset page's sign-in is proven only in two halves. The landing is proven
  here; the save after a recovery by `useResumeFavorite.component.test.tsx` (the finding-168 case). See R2.5.

**R2.2: focus. WEAK.**
- **PASS:**
  - the title on opening, at both widths: `SignInPrompt.tsx:88-91`, `SignInPrompt.component.test.tsx:143`, and the
    Chrome matrix (24 of 24);
  - the title on each `go()`: `SignInPrompt.tsx:74-76`, tested `:539-559`;
  - the password for A1 (`:437-439`) and for «سجّل الدخول بهذا البريد» (`:466-469`);
  - the e-mail for «استخدم بريدًا آخر» (`:405-410`);
  - back on the heart after a sign-in (`:167-169`); the trigger after Back on the phone
    (`SignInPrompt.component.test.tsx:176`).
- **The failure:** the forgot view's step change is not a `go()`, so nothing moves the focus.
  - Input: «أرسل رابط الاستعادة» succeeds.
  - What happens: `ForgotPasswordSteps.tsx:70` swaps the form for the link sent, and the focused submit button is
    removed. Radix's FocusScope then focuses the dialog's container
    (`node_modules/@radix-ui/react-focus-scope/dist/index.mjs:54-58`), not «تفقّد بريدك الإلكتروني».
  - Result: a screen-reader user hears neither the new title nor the masked address.
  - The plan's S4 named exactly this case ("the pressed button unmounts and the focus falls to the dialog's
    container"). Test 10 (`:393-395`) checks that the heading exists, not where the focus is.
- **Smallest fix:** in `OpenSignIn`, focus the title when `step` becomes `sent` or `linkOpen` while
  `view === 'forgot'` (one effect on `step`). Add `toHaveFocus()` on «Check your email» in test 10.
- **Same gap, lower stakes:** the recovery's retry (`unreachable` → `loading`), and the chunk's retry
  (`SignInBody.tsx:65-66`).

**R2.3: Back, Escape, the close button and busy. PASS.**
- `it.each` over Escape, the close button and Back (`:320-346`) checks that the action is let go and the storage key
  is null.
- While busy, the close button is disabled and Escape and Back keep the overlay open (`:348-366`).
- The busy key counts only pending mutations: `useSignInBusy.ts:9`, so Google's rate-limit wait does not trap the
  guest.
- On success, the controlled `open=false` closes the overlay despite busy, and the history mark is gone (`:166`).
- One part is unverified: the history after a temporary password (see R2.8).

**R2.4: catalogue, words, Arabic first, logical classes, tokens, the design system. PASS.**
- Every string goes through `shared/copy/{arabic,english}`, and the Arabic files are the `satisfies Catalogue`
  source.
- The NEW words match the plan and the prototype:
  - the register titles, «جديد على مساحة؟», the sent notes, the changed notice;
  - the reset page's return and done lines (`Reset password/inplace.jsx:31,127`);
  - D1's line, with the Arabic plural forms (`arabic/forms.ts:10-26`);
  - the hidden «(تفتح في تبويب جديد)».
- Logical classes only (`self-start`, `ChevronStartIcon`, `pe`/`ps` none needed); semantic tokens only.
- No design-system file is in the diff. `check:classes` is green in CI.
- Two nits are in §3: an unapproved new line (`loadFailed`), and the field error's «الشروط أدناه».

**R2.5: the tests. WEAK.**
- **The sample of five breaks, checked against the code.** Each would fail its test:
  1. Google remounted per view → `toBe(button)` at `:230`.
  2. The privacy link without `target` → `:508`.
  3. No A1 listener → `:432-439`.
  4. The prompt not closed by the session → `closed()` at `:162`.
  5. `useSignInBusy` never busy → `toBeDisabled()` at `:356`.

  Also checked: the reset page landing without the intent fails at `:202-204`. With `intentMayRun` broken, the
  overlay test still passes, as the report admits, and the hook tests catch it
  (`useResumeFavorite.component.test.tsx`, `useReportAction.component.test.tsx`, the "temporary password" cases).
- **The rewritten tests (D6, D1) still prove what they proved.** Nothing was deleted without a replacement:
  - every removed `it(` is a checklist assertion now stated as the line, or the reset page's link now stated as the
    form;
  - `carries the return page … lands on it after` (`:155`) still proves that `next` is carried after the reset;
  - the one test deleted outright (`SignInPrompt`'s "leaves through «$link»") tested the links this PR removes.
- **The failure:**
  - **The reset page's held-favourite test** (`resetPasswordPage.component.test.tsx:181-205`) checks only that the
    sign-in lands on `/spaces/noor-hub`. The plan's R1 row says "and its save is posted". With the post broken, the
    test stays green.
  - **Smallest fix:** keep the transport's requests and expect `post /me/favorites/7` once, so the reset page's main
    promise is proven end to end.
- **Smaller gaps:** plan items with no assertion:
  - test 2: the welcome toast;
  - test 5: the password focused after wrong credentials;
  - test 16: the focus on the sign-in title after «لديك حساب؟ تسجيل الدخول» or «العودة إلى تسجيل الدخول»;
  - S5: the chunk-retry boundary (`SignInBody.tsx:84-102`) has no test at all, and Chrome did not check it.

**R2.6: scope and commits. PASS.**
- **Files outside the plan's §7 list.** Each is the plan's intent under another name or a direct need; none is a
  drive-by:
  - `RecoveryRetry.tsx`: split, so `RecoveryFailure` can show without a card;
  - `ForgotPasswordSteps.tsx`: new in `features/auth`;
  - `LinkSent.tsx`, `ResendLinkForm.tsx`, `useResendLinkForm.ts` and its test, `useForgotPasswordForm`'s test:
    renew at resend;
  - `ResetPasswordForm.tsx`: the note;
  - `useEmailReport.ts`;
  - `useContinueWithGoogle.ts`: the plan said `useGoogleFailure`;
  - `SignInBody.tsx`, `signInView.ts`, `SentNote.tsx`, `SignInFormView.tsx`: the plan's `SignInPromptFallback` and
    `SignInView`, renamed or split;
  - `docs/features/users.md`: D1;
  - finding 230 and its index line.
- **Commits:** 4, Conventional, subjects ≤ 50 characters, each with a body, no attribution and no `fixup!`. No
  `#PRNUM` is left in the tree. The reset card's slot is consistent at each commit (`signInLink` until `57ccca6e`).
- One nit is in §3: commit `07e89a1d`'s `auth.md` already cites the `sign-in` chunk, which arrives in `305c5d3f`.

**R2.7: the documents. WEAK.**
- **True of the code:**
  - architecture §2: the two landing cases;
  - §3: the chunk, and the password line;
  - §4: the held intent, its contents (no e-mail, D2 = B), the `storage` event;
  - `auth.md`, `favorites.md`, `data-reports.md`; finding 230 (the next free number, the correct format).
- **One home per fact:** the feature documents link to architecture and to `auth.md` rather than repeat them.
- **The failure:** `docs/features/users.md:42` still says the account's password change shows "its rules
  checklist". D1 replaced it with the line everywhere. The PR edited `users.md:50` and missed this one.
  - **Smallest fix:** "its rules checklist" → "the policy's line".
- **Smaller stale points, all nits:**
  - JSDoc in two files this PR touched still says the rules "tick": `RegisterForm.tsx:13`, `ResetPasswordForm.tsx:8`.
  - `architecture.md:139` ("Built: … `RequireGuest` lands the user by it …") does not name the reset page, the new
    caller of `landingPath`, though the text at `:144` does.

**R2.8: the report's claims against the code and CI. WEAK.**
- **Consistent:**
  - CI is green on `305c5d3f` and the PR is `CLEAN`; 90 files.
  - The CI build logs the `sign-in` chunk at 21.22 kB / 6.25 kB gzipped. The report's local 21.29 / 6.30 differs by
    environment only.
  - The `check:build` line appears in CI.
  - The Chrome JSON files match each claim: focus `adaptive-dialog-title` 24 of 24, axe empty, Back and Escape, the
    toast, A1, the reset line, Google's Shift+Tab and Enter.
- **What is missing.** The plan's §10 and §12 named these Chrome checks; the report neither ran them nor says they
  were skipped:
  1. **Temporary password, the history.** The plan's question was the gate's replace racing the overlay's step back.
     The report lists the sign-in as "not run … the component lane proves" it. The component test proves only the
     final URL (`:301-305`), not the history.
     - From the code: the overlay's microtask `history.back()` (`historyEntry.ts` cleanup) can run before the data
       router's asynchronous replace. The router then writes `/change-password` over the overlay's entry and
       `/spaces/x` is popped, or a forward entry is left.
     - Rare (a staff account on the site), but the plan promised to check it.
  2. **Directory and Home**, the overlay over a card's heart: the run was on `/spaces/pal-hub` only. Whether the
     focus returns to a card's heart after the favourites query re-renders the grid is unverified.
  3. **Slow 3G and offline:** the loading line, and the chunk's retry.
- **Fix:** run the three, or state them in the report as not run, for the owner to accept.
- **Not in the report:** in the 1440-English flow, the save toast and the report dialog are in Arabic
  (`chrome-out-flows.json:35-37`). This is the existing language switch on sign-in (`apps/web/src/app/session.ts:17`),
  not this PR's code. Over the page it now changes the language of the page the guest stays on. See §3, nit 1.

## 3. Findings, ranked

**Blockers:** none.

**Should fix (one fix round):**
1. **The link sent: focus.** After «أرسل رابط الاستعادة», the focus falls to the dialog's container, not to «تفقّد
   بريدك الإلكتروني» (R2.2). Fix: focus the title when the forgot `step` changes; assert it in test 10.
2. **The reset page's held-favourite test** asserts the landing but not the save (R2.5). Fix: one expectation on
   `post /me/favorites/7`.
3. **`docs/features/users.md:42`** still says "rules checklist" (R2.7). Fix: one phrase.
4. **The plan's Review Focus checks** were not done and not reported (R2.8): the temporary password's history, the
   card hearts on Directory and Home, slow 3G and the offline retry. Fix: run them in Chrome, or list them in the
   report as open for the owner.

**Nits:**
1. **Language switch on sign-in.** Over the page, a guest reading in English whose account is Arabic sees the page
   flip to Arabic (`app/session.ts:17`). This is existing behaviour, but more visible in place. A finding or an
   owner question; not this PR's to change.
2. **Promises read once.** `SentNote.tsx:15` and `ResetPasswordPage.tsx:29` read the held intent once, when they
   mount. If it lapses later the line still promises the return, and the sign-in lands on `/`:
   - 15 minutes after the last request;
   - the recovery mark's 10 minutes (`heldIntent.ts:30`);
   - the other tab signing in first.

   Fix: read `heldIntentPreview()` again when the done step mounts, and drop the line when it returns null.
3. **`site.signInPrompt.loadFailed`** («تعذّر تحميل تسجيل الدخول…») is a NEW line outside the approved list. The plan
   said to reuse the catalogue's no-connection line. Approve it or replace it.
4. **The field error and the line repeat each other.** The error «كلمة المرور لا تستوفي الشروط أدناه» /
   "…the rules below" (`arabic/auth.ts:40-41`) now stands over one line that already says what is missing in red.
   The wording is the owner's call.
5. **Stale "checklist" wording outside the touched files.**
   - Comments: `ForcedPasswordChangeForm.tsx:8` and `usePasswordChangeForm.ts:20`, in `users`, rightly left alone
     by the plan.
   - `PASSWORD_RULES` is now used only by its own unit test (`packages/shared/src/users/passwordPolicy.ts:30-43`).
   - Record it as a finding, not a drive-by fix.
6. **Duplicated step switch.** `ForgotPasswordSteps` repeats `ForgotPasswordCard`'s switch over the five steps and
   its "enter again" state. The plan said "nothing is forked". The card could be built on the steps later; record
   it.
7. **«نسيت كلمة المرور؟» position.** It sits at the field's end (`SignInForm.tsx:37`, `self-end`); the picture puts
   it at the start (`Space details/inplace.jsx:173`). It is the shared form's existing layout, so it belongs to
   WI-C3.
8. **No `enterKeyHint`.** The plan's I15 «التالي» / «تم» was dropped (report §8, with a reason). The owner should
   confirm.
9. **Per-commit document truth.** At `07e89a1d`, `auth.md` cites the `sign-in` chunk of architecture §3, which only
   `305c5d3f` adds.

**Outside R2 (one line):** the reset page now *announces* and lands on the browser's held action for whoever
completes a reset within its window. On a shared coworking computer, that is another guest's favourite or report
running under this account (finding 168's design, now visible). That is R1's to judge.
