# Design fix 4: the account and signing in — the build plan

Planner: Claude Code (Opus 5.5), plan only. Read at `origin/main` `e30a86c` (#66 merged), tree clean, in
`C:\Users\basel\masaha-design-b` (the session itself ran in `masaha-design`, at the same commit, and edited
nothing in either). Subagents used: 0 of 2. **The executor (OpenCode) builds from this file alone; the
reviewer (OpenCode) checks the PR against §8.** Branch `design/account`, prototype on **5347**, images in
`C:\Users\basel\Downloads\design-fix-account\`, report in
`C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_ACCOUNT_REPORT.md`.

**Before the build, the owner answers §4** (Q1–Q3, S1–S10). Every block below says what to do under each
answer. Where nothing is said, the recommended answer is built.

---

## 1. Summary and contract

Batch 4 of the design review — signing in, registering, the forgotten password, the forced change,
«إعدادات حسابي», Favourites, «بلاغاتي», the account menu — applied to the living prototype, as
`DECISIONS_ACCOUNT.md` has it with the owner's amendment of 2026-10-13 (C5's forced-change line), plus
the owner's addition of the same day: the location's privacy line becomes true (prompt §7).

- **The auth pages catch up with the built code** (AC-022): the 429 clock, `EMAIL_TAKEN` on its field,
  Google per code, the recovery's server-held steps, the masked address.
- **A mistyped email has a way out** (C3).
- **Getting in keeps the intent** (C4: AC-004, AC-017, AC-018, AC-019).
- **One «تسجيل الدخول» card** in the account settings (AC-006 with C1, C2 and C5's password toast).
- **A session change says what it did elsewhere** (C5: the Google link's toast, the forced change).
- **One account area with one name** (C6 with AC-011, AC-012, AC-013).
- **A space that left the directory** (C7).
- **Favourites whole, My reports paged** (C8 with AC-009, AC-014, AC-016).
- **The reset email carries a link to copy** (AC-021).
- **The location's privacy line tells the truth** (prompt §7), in its own commit.

### Scope
Inside `docs/design/` only. The pages and modules of the prompt's §6 list, plus the shared archive files in
their own sections: `CHANGES.md` (a *Batch 4* section), `INDEX.md` (a *Batch 4* parameters table, a new
section 54, and the changed rows of sections 05, 14, 16, 17), `Flows - states.html` (section 54 and the
changed frames of 05, 14, 16, 17), `README.md` (the frame count only). `Space details.html` and
`Directory.html` only if the owner answers yes to Q1 and Q2.

### Acceptance criteria (the reviewer ticks each)
- [ ] **AC-022 · 429.** `Sign in.html?state=ratelimit`, `Register.html?state=ratelimit`,
  `Forgot password.html?state=ratelimit` and `Settings.html?auth=1&state=ratelimit` show «محاولات كثيرة،
  حاول بعد 0:42» counting down each second, the submit disabled while it runs; at 0:00 the line goes and
  the submit is enabled. No page of the account says «15 دقيقة».
- [ ] **AC-022 · email taken.** `Register.html?state=exists` shows «يوجد حساب بهذا البريد الإلكتروني.» as
  the email field's error and the link «سجّل الدخول بهذا البريد» under it; no Alert above the form.
- [ ] **AC-022 · Google.** `?google=error`, `?google=notallowed`, `?google=unavailable` each show the Alert
  «تعذّرت المتابعة باستخدام Google» with its own line; `?google=off` shows no Google button and no «أو».
- [ ] **AC-022 · recovery.** `Forgot password.html?state=loading|unreachable|linkopen|spent` and
  `Reset password.html?state=loading|unreachable|checkfailed` draw the built steps; every address shown is
  masked (`s•••@example.com`); the resend waits on an m:ss clock («أعد الإرسال بعد 0:59»).
- [ ] **C3.** On `Forgot password.html?state=sent`, «استخدم بريدًا آخر» is under the resend at every
  moment of the clock; pressing it returns to the empty email form with the focus in the field;
  `?state=sent&email=sara@gmial.com` reads «أُرسلت إلى s•••@gmial.com».
- [ ] **C4 · intent.** From `Space details.html?id=focus` (signed out) → heart → «تسجيل الدخول» → sign in:
  the space page shows the filled heart and one toast «أهلًا بعودتك — حُفظت فوكس هاب في المفضّلة»;
  the same through «إنشاء حساب» says «أهلًا سارة، تم إنشاء حسابك — حُفظت فوكس هاب في المفضّلة».
- [ ] **C4 · way back.** `Sign in.html` and `Register.html` with that `next` show «العودة إلى فوكس هاب»
  (→ `Space details.html?id=focus`) where «تصفّح المساحات بدون حساب» was; without `next` the sign-in card
  keeps «تصفّح المساحات بدون حساب» and Register gains it. «نسيت كلمة المرور؟» and the forgot page's
  «العودة إلى تسجيل الدخول» keep `next`. The reset card has «العودة إلى تسجيل الدخول» in its footer in
  every state but success.
- [ ] **AC-017.** The sign-in card's description reads «سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة
  بلاغاتك، أو لإدارة مساحتك.»
- [ ] **AC-018** (Q1 yes). The report variant of the space page's sign-in dialog reads «سجّل الدخول لتجد
  الردّ على بلاغك في «بلاغاتي».»
- [ ] **AC-006 / C1 / C2.** Settings has one card «تسجيل الدخول» and no card «الأمان»; it lists the
  methods as rows; «تغيير» opens the password form in place with «رجوع»; the line «تغيير كلمة المرور
  يسجّل خروجك من كل الأجهزة الأخرى» sits in the form above «حفظ كلمة المرور»; no «تسجيل الخروج من كل
  الأجهزة» anywhere; `?auth=google` offers «أرسل رابط تعيين كلمة المرور» and no password field, and on
  press shows the link-sent block in place.
- [ ] **C5.** The password change's toast reads «تم تغيير كلمة المرور، وسُجّل خروجك من الأجهزة الأخرى».
  `Home.html?loc=none&toast=linked` shows «ربطنا حساب Google بحسابك» with its description and a close
  button, and it does not leave by itself. `Change password.html` reads «كلمة المرور التي دخلت بها مؤقتة،
  أُعطيت لك من فريق مساحة أو من صاحب المساحة. اختر كلمة مرور خاصة بك للمتابعة.»; saving lands on
  `Owner overview.html` (default / `?role=owner`), `Desk.html?role=reception`, `Admin overview.html`
  (`?role=admin`) or `Home.html?auth=1` (`?role=user`).
- [ ] **C6.** The account nav, the Settings h1, its `<title>` and the menu say «إعدادات حسابي»; from 1024
  the nav shows the caption «حسابي» above its items; Settings is `max-w-3xl`, Favourites and My reports
  full width; `Favorites.html?auth=0` (and Reports, Settings) goes straight to `Sign in.html` with `next`,
  with no inline sentence.
- [ ] **AC-012.** The email shows as text (label, value, «تسجّل الدخول بهذا البريد»); no input, no
  «لتغيير البريد».
- [ ] **AC-013.** With no `?theme`, the theme toggle has «حسب الجهاز» pressed; the captions read «تُحفظ في
  حسابك» (language) and «على هذا الجهاز» (theme); `?fail=language` returns the toggle and raises «تعذّر
  حفظ اللغة» with «إعادة المحاولة».
- [ ] **C7.** Favourites shows Palm Hub as a row under the grid (not a card in it): the name as text,
  «لم تعد هذه المساحة معروضة في الدليل», «إزالة» with «تراجع». My reports shows Palm Hub's report with the
  same line, its name as text, its status and reply.
- [ ] **C8 / AC-014.** Favourites has no pagination; a count and «الأقرب إليّ» sit above the grid, the
  `LocationStatus` line under them; with the location on the grid is sorted by distance and the cards
  show distances, with it off neither.
- [ ] **C8 / AC-016 / AC-009.** My reports pages (`usePaged`, «عرض 1–7 من 7» with its steps
  `aria-disabled`; `?demo=pages` gives 28 and two pages); the chips read «الكل · قيد المراجعة · تمت
  المراجعة»; «عرض المزيد» shows only on a message the clamp cuts; a report with no message shows its field
  line alone; messages and replies are `dir="auto"`; the reply label follows `repliedBy` (Number One's
  old report reads «ردّ فريق مساحة» though the space is verified).
- [ ] **AC-021.** `Reset email.html` greets «مرحبًا،» and «Hi,» (no name) and has, under the button,
  «إن لم يعمل الزر، انسخ هذا الرابط:» with the link as LTR text.
- [ ] **§7.** No page says «يبقى موقعك على جهازك فقط» or "stays on your device"; the four location states
  say «يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.» (Q2 yes: the map's picking card
  too).
- [ ] Every changed page opens at 390, 768 and 1440, Arabic and English, light and dark, with no blank
  render, no console error, no horizontal overflow. Every new or changed `INDEX.md` URL opens its state.
- [ ] `check-parse.mjs` and `check-classes.mjs` pass at every commit; `format:check` and `check:links`
  pass in CI.
- [ ] A before/after pair per decision in the images folder, not committed.

### Out of scope
- **AC-020** (the fourth password rule): design system / `@shared/forms`, worker A — unless Q3 is yes.
- The API's `listed: false` and `repliedBy` (worker B): the prototype draws them now.
- `foundation.md` §13 screen 9 and `api-contract.md` §4 (docs items).
- The web: C3, C5, AC-017, AC-019 in built code, and the intent with step 10 (worker A).
- The dashboards' «محاولات كثيرة» line (`RateLimitNote`, owner and admin pages): DI-30.
- The owner's batch files (§5). `apps/`, `packages/`, `docs/features/`, the findings. `screens/`.
- Anything on *Not in v1*.

---

## 2. Reading done

- **Bootstrap:** `CLAUDE.md`; the `start-work-item` runbook; the prompt (§0–§7, the §7 addition re-read).
- **Decisions:** `DECISIONS_ACCOUNT.md` (the *Amended* note first, then C1–C8, the smaller items, the
  design-system and rules lines); `DECISIONS_SHARED.md` (P1–P10 with both *Amended* notes, SH-005,
  SH-017); `DECISIONS_PUBLIC.md` (*Changed 2026-10-13*: "near me" sorts on the server).
- **The review:** `REVIEW_ACCOUNT_REPORT.md` (G1–G4, AC-001…AC-022, rules in doubt).
- **The archive:** `docs/design/CHANGES.md` (batches 1, 2a, 2b, 3), `README.md`, `INDEX.md` (the parameters
  tables, sections 05–09, 13–19, 53), `SCREENS.md`; the previous plan `FIX_ADMIN_REST_PLAN.md` and PR #66's
  description (their shape).
- **The prototype:** `masaha/auth.jsx`, `account.jsx`, `shared.jsx` (all), `location.jsx`, `i18n.js`;
  `Sign in.html`, `Register.html`, `Forgot password.html`, `Reset password.html`, `Change password.html`,
  `Reset email.html`, `Settings.html`, `Favorites.html`, `Reports.html`; `Home.html` (its `NearMeButton` /
  `LocationStatus` use); `Space details.html` (`SignInDialog`, `authHref`); `Directory.html:353`; the board's
  account frames; `scripts/check-classes.mjs`; the prebuilt CSS, for every class named below.
- **The built web:** `features/auth/components/*` (`LinkSent`, `LinkOpen`, `ForgotPasswordCard`,
  `ResetPasswordCard`, `RecoveryLoading`, `RecoveryRetry`, `CheckFailed`, `RegisterForm`,
  `ContinueWithGoogle`), `shared/routing/guards/RequirePasswordChange.tsx`, `landing/landingPath.ts`; the
  copy catalogues `auth.ts`, `errors.ts`, `forms.ts`, `users.ts`, `status.ts` (ar and en); the API's
  `resetEmail.copy.ts` and `resetEmail.ts` (the link `…/reset-password#token=…`).
- **Rules:** `api-contract.md` §4, *Session*, *The forgotten password*, *Me*; `security.md` › *Sign-in
  methods*, *Passwords* (72 bytes, no name in the email, Google link removes the password);
  `foundation.md` §13 (screens 5–11).

**What shapes the build:**
- **The built web is behind on C3, AC-017 and AC-019** (its `LinkSent` shows «أدخل بريدك الإلكتروني من
  جديد» only once the resends are spent; its sign-in description and reset card are the old ones). For those
  the prototype leads and worker A follows; for AC-022 the prototype catches up. `CHANGES.md` says which.
- **The vendored `Toaster` takes `closeButton` per toast** (`toast.closeButton ?? closeButtonFromToaster`),
  so the linked toast can stay until closed without touching the bundle.
- **`Space details.html` and `Directory.html` are in neither batch's list** (§6 of the prompt). C4's
  AC-018 line and save-failure state live in the first; §7's map wording in the second (Q1, Q2).
- **Prebuilt CSS:** every class below was checked present: `max-w-3xl`, `lg:block`, `px-3`, `pb-1`,
  `self-start`, `self-center`, `items-start`, `line-clamp-2`, `text-caption`, `text-label`, `h-px`,
  `bg-border`, `md:grid-cols-2`, `xl:grid-cols-3`, `flex-wrap`, `justify-between`, `gap-3`. `break-all`,
  `whitespace-pre-line` and `font-mono` are **absent**: not used (the email is inline-styled).

---

## 3. The decisions, as they will be built

Conventions for every block:
- **Strings** are given as `tr("Arabic", "English")`, to be written exactly.
- **`Ltr`** is `shared.jsx`'s `<span dir="ltr" className="num-iso">`. Every address, clock and URL goes in it.
- **Board frame HTML**, one line each, at the end of `Flows - states.html` (before `</body>`):
  `<div class="frame" style="left:Lpx;top:Tpx"><p>LABEL</p><iframe loading="lazy" src="SRC" width="W" height="H" title="LABEL"></iframe></div>`,
  with a space as `%20` and `&` as `&amp;` in SRC; `H` is 844 for 390 and 1000 for 1440.
- **INDEX row:** `| LABEL | \`URL\` | 390×844 | — |` (or `1440×1000`), URL with plain spaces and `&`.

### 3.0 Shared helpers (built in the commit that first needs them)

**`masaha/shared.jsx`** (commit 1):
- Line 528's `Object.assign(window, { … })`: add `actionFails, ACTION_MS`.
- After `handOffToast` (line 524), add:
  ```js
  // C4: the line naming the favourite saved on the way in.
  const favSavedLine = (s) => tr(`حُفظت ${spaceName(s)} في المفضّلة`, `${spaceName(s)} saved to your favourites`);
  ```
  and add `favSavedLine` to the line-528 export list.
- **`PageToaster` takes objects as well as strings** (C5). Replace line 510 and the effect's body
  (lines 514–518) with:
  ```js
  // A toast handed over is a string, or { title, description, persist } for one that must not
  // vanish on its own (C5: the Google link tells of a lost password).
  const demoToast = (key) => {
    const s = M && M.spaces ? M.spaces.find((x) => x.id === (pageParams.get('id') || 'focus')) : null;
    const welcome = tr("أهلًا سارة، تم إنشاء حسابك", "Welcome Sara, your account is ready");
    return {
      welcome,
      welcomefav: s ? welcome + ' — ' + favSavedLine(s) : welcome,
      linked: { title: tr("ربطنا حساب Google بحسابك", "We linked your Google account to your account"), description: tr("حُذفت كلمة مرور حسابك وسُجّل خروجك من الأجهزة الأخرى. لتعيين كلمة مرور جديدة، استخدم «نسيت كلمة المرور».", "Your account’s password was removed and you were signed out on other devices. To set a new password, use “Forgot password”."), persist: true }
    }[key];
  };
  ```
  and in the effect:
  ```js
  if (demo) list = demo.split(',').map(demoToast).filter(Boolean);
  list.forEach((m, i) => setTimeout(() => {
    const t = typeof m === 'string' ? { title: m } : m;
    toast.success(t.title, { description: t.description, duration: demo || t.persist ? Infinity : 5000, closeButton: t.persist ? true : undefined });
  }, 300 + i * 150));
  ```
  `DEMO_TOASTS` is removed (grep: no other reader).

**`masaha/auth.jsx`** (commit 1), replacing line 6 (`RATE_LIMIT`) and lines 137–139 (`RateLimitAlert`):
```js
// AC-022: a 429 counts down from the server's Retry-After, as the built forms do; the submit waits with
// it, and the line beside it says why (foundation §10). The prototype's Retry-After is 42 seconds.
const RETRY_AFTER = 42;
const mmss = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
function useCountdown(start) {
  const [left, setLeft] = React.useState(start);
  React.useEffect(() => { if (left <= 0) return; const t = setTimeout(() => setLeft(left - 1), 1000); return () => clearTimeout(t); }, [left]);
  return [left, setLeft];
}
const useRetryAfter = (on) => useCountdown(on ? RETRY_AFTER : 0)[0];
function RateLimitAlert({ left }) {
  if (left <= 0) return null;
  return <AAlert variant="warning"><AAlertDescription>{tr("محاولات كثيرة، حاول بعد ", "Too many attempts. Try again in ")}<Ltr>{mmss(left)}</Ltr>{tr("", ".")}</AAlertDescription></AAlert>;
}
// The address the server holds, masked as it answers it: "s•••@example.com".
const maskEmail = (e) => { const at = e.indexOf('@'); return at < 1 ? e : e[0] + '•••' + e.slice(at); };
```
Export list (line 141): remove `RATE_LIMIT`; add `RETRY_AFTER, mmss, useCountdown, useRetryAfter, maskEmail`.
**Remove `useCountdown` from `Forgot password.html` (lines 28–32)**: the name must exist once per page (§9).

### 3.1 AC-022 — the auth pages catch up with the built code (commit 1)

**The 429** on four forms. In each, `const left = useRetryAfter(<condition>)` replaces the `limited` state;
`{left > 0 && …}` is not needed (the Alert returns null at 0): render `<RateLimitAlert left={left} />` where
`<RateLimitAlert />` was; the submit gets `disabled={left > 0}`; the submit handler returns early when
`left > 0` (in place of `|| limited`).
- `Sign in.html` line 38 → `const left = useRetryAfter(initialState === 'ratelimit');`; line 47 `|| left > 0`;
  line 69; line 77's `Button` gets `disabled={left > 0}`.
- `Register.html`: `const left = useRetryAfter(initialState === 'ratelimit');`; `problem` no longer takes
  `'ratelimit'` (line 55's list becomes `['exists', 'network']`); line 87 → `<RateLimitAlert left={left} />`;
  submit returns early when `left > 0`; line 96's button `disabled={left > 0}`.
- `Forgot password.html` line 39 and 70, and line 74's button.
- `Settings.html` `PasswordForm` (rebuilt in 3.4) uses `useRetryAfter(demo === 'ratelimit')`.

**`EMAIL_TAKEN` on its field** (`Register.html`):
- Delete lines 82–86 (the `exists` Alert).
- `problem === 'exists'` no longer exists as a problem: on a taken address (initial `?state=exists`, or an
  email starting with `taken` on submit) set `errors.email = tr("يوجد حساب بهذا البريد الإلكتروني.", "An account with this email already exists.")`
  and a state `taken = true` (initial `initialState === 'exists'`; reset to false on every submit).
- Wrap the email `Field` (lines 92–94) in `<div className="flex flex-col gap-1">…</div>` and add after the
  `Field`, when `taken`:
  `<Button variant="link" size="sm" className="self-start px-0" asChild><a href={withNext('Sign in.html')}>{tr("سجّل الدخول بهذا البريد", "Sign in with this email")}</a></Button>`.
- `errors` initial: `initialState === 'errors' ? validate(DEMO.errors) : initialState === 'exists' ? { email: <the line above> } : {}`.

**Google per code** (`auth.jsx`, `useGoogleSignIn` and `GoogleBlock`):
- `failed` holds a code or `null`: initial `({ error: 'token', fail: null, notallowed: 'notallowed', unavailable: 'unavailable' })[pageParams.get('google')] || null`;
  in `start`, `mode === 'fail'` sets `'token'`.
- Add `const off = pageParams.get('google') === 'off';` to the hook's return (`{ busy, failed, start, off }`).
- `GoogleBlock`: `if (google.off) return null;` (no button, no «أو», as the built `ContinueWithGoogle`
  returns null without a client id). The Alert becomes:
  ```js
  const GOOGLE_LINES = () => ({
    token: tr("لم يتمكّن Google من تأكيد حسابك. حاول مرة أخرى، أو استخدم البريد الإلكتروني وكلمة المرور.", "Google couldn’t confirm your account. Try again, or use your email and password."),
    notallowed: tr("يوجد حساب بهذا البريد الإلكتروني. سجّل الدخول بكلمة مروره، أو أعد تعيينها من «نسيت كلمة المرور».", "An account with this email already exists. Sign in with its password, or reset it under “Forgot password”."),
    unavailable: tr("الدخول باستخدام Google غير متاح الآن. استخدم البريد الإلكتروني وكلمة المرور، أو حاول لاحقًا.", "Google sign-in isn’t available right now. Use your email and password, or try again later.")
  });
  …
  <AAlert variant="destructive"><AAlertTitle>{tr("تعذّرت المتابعة باستخدام Google", "Couldn’t continue with Google")}</AAlertTitle><AAlertDescription>{GOOGLE_LINES()[google.failed]}</AAlertDescription></AAlert>
  ```
  (`GOOGLE_LINES` is top-level in `auth.jsx`, defined above `GoogleBlock`.)

**The recovery's steps** (`Forgot password.html`). `state` replaces `sent`:
`const [step, setStep] = React.useState(['loading', 'unreachable', 'sent', 'linkopen', 'spent'].includes(initialState) ? initialState : 'request');`
The email's initial value: `pageParams.get('email') || (initialState ? 'sara@example.com' : '')`.
`?state=loading` resolves to `request` after `ACTION_MS` only when opened without `?state` (it is a frame:
it stays). Per step, inside the existing `Card`:
- **`loading`** — `CardTitle` «نسيت كلمة المرور» / "Forgot password"; `CardContent className="flex items-center justify-center py-6"`
  holding `<Spinner label={tr("جارٍ التحميل", "Loading")} />` (`Spinner` from the bundle).
- **`unreachable`** — same title; `CardContent` with
  `<EmptyState icon={<CircleAlertIcon />} title={tr("لا يوجد اتصال بالإنترنت", "No internet connection")} description={tr("ستظهر البيانات عند عودة الاتصال.", "The data will appear when you’re back online.")}><Button variant="outline" onClick={…}>{tr("إعادة المحاولة", "Try again")}</Button></EmptyState>`;
  the retry shows `loading` for `ACTION_MS` then sets `request`.
- **`request`** — as now (title, description, form).
- **`sent`** — C3's block (3.2).
- **`spent`** — title «تفقّد بريدك الإلكتروني» / "Check your email"; content: the sent message
  (current line 62), «أُرسلت إلى » + `<Ltr>{maskEmail(email)}</Ltr>`,
  `<p className="text-body-sm">{tr("طلبت الرابط مرات كثيرة. أدخل بريدك الإلكتروني من جديد لطلب رابط آخر.", "You’ve asked for the link too many times. Enter your email again to ask for another.")}</p>`,
  and `<Button variant="outline" className="w-full" onClick={otherEmail}>{tr("أدخل بريدك الإلكتروني من جديد", "Enter your email again")}</Button>`.
- **`linkopen`** — `CardTitle` «فتحت رابط الاستعادة» / "You’ve opened a reset link"; `CardDescription`
  `tr(\`للحساب ${maskEmail(email)}. عيّن كلمة المرور الجديدة، أو اطلب رابطًا جديدًا.\`, \`For ${maskEmail(email)}. Set your new password, or ask for a new link.\`)`;
  content `flex flex-col gap-2`: `<Button className="w-full" asChild><a href="Reset password.html">{tr("تعيين كلمة مرور جديدة", "Set a new password")}</a></Button>`
  and the outline «أدخل بريدك الإلكتروني من جديد» → `otherEmail`.
- `otherEmail` (shared with C3): `setStep('request'); setEmail(''); setError();` then, in an effect on
  `step === 'request'` that runs only after a change (a ref set by `otherEmail`), focus
  `document.querySelector('main input[type=email]')`.

**`Reset password.html`.** `state` accepts `loading`, `unreachable`, `checkfailed` besides `invalid`,
`success`, `form`. `loading` and `unreachable` as on the forgot page, with the title «تعيين كلمة مرور جديدة» /
"Set a new password". **`checkfailed`**: that title; content `flex flex-col gap-4` with
`<RateLimitAlert left={useRetryAfter(true)} />` (call the hook at the top of `ResetScreen`:
`const checkLeft = useRetryAfter(initialState === 'checkfailed');`) and
`<p className="text-body-sm">{tr("افتح الرابط من بريدك الإلكتروني مرة أخرى.", "Open the link in your email again.")}</p>`.
The form's description (line 49 of the script) becomes `{tr("للحساب ", "For ")}<Ltr>{maskEmail('sara@example.com')}</Ltr>`.

**The resend clock** (C3 block, 3.2) reads «أعد الإرسال بعد 0:59» — `mmss(left)`, no «ثانية».

**Board and INDEX** (commit 1): section 54's header and frames F1–F6 (§6, commit 1); the parameters rows
(§6).

### 3.2 C3 — a mistyped email has a way out (commit 2)

A shared block in `auth.jsx` (after `NetworkAlert`), used by the forgot page and by Settings (3.4):
```js
// C3 (AC-003): the link sent — what happens next, the address the server holds (masked, so a typo shows),
// another link on an m:ss clock, and, where the address was typed, «استخدم بريدًا آخر» at every moment.
function LinkSent({ message, email, left, onResend, resending, onOtherEmail, fullWidth = true }) {
  return (
    <div className="flex flex-col gap-4">
      <p className="text-body" role="status">{message}</p>
      <p className="text-body-sm text-muted-foreground">{tr("أُرسلت إلى ", "Sent to ")}<Ltr>{maskEmail(email)}</Ltr></p>
      <AButton variant="outline" className={fullWidth ? 'w-full' : 'self-start'} disabled={left > 0} loading={resending} onClick={onResend}>
        {left > 0 ? <>{tr("أعد الإرسال بعد ", "Resend in ")}<Ltr>{mmss(left)}</Ltr></> : tr("أعد الإرسال", "Resend")}
      </AButton>
      {onOtherEmail && <AButton variant="link" size="sm" className="self-center" onClick={onOtherEmail}>{tr("استخدم بريدًا آخر", "Use another email")}</AButton>}
    </div>
  );
}
```
Export `LinkSent`. In `Forgot password.html`, the `sent` step's content (lines 61–67) becomes
`<LinkSent message={<the current line 62 text>} email={email} left={left} onResend={() => submit()} resending={loading} onOtherEmail={otherEmail} />`.
The «تواصل معنا» and «العودة إلى تسجيل الدخول» footer stays in every step.

Board/INDEX: F7.

### 3.3 C4 — getting in keeps the intent (commit 3)

**`auth.jsx`**, after `withNext` (line 5):
```js
// C4 (G1): the action that led to the sign-in rides in `next` (`fav=1`, `dialog=report`); on the way back
// it is done and named. The report reopens its dialog, so only the favourite needs a line.
const nextSpace = () => {
  const n = pageParams.get('next'); if (!n) return null;
  const [path, qs] = n.split('?'); const q = new URLSearchParams(qs || '');
  if (path !== 'Space details.html') return null;
  const s = M.spaces.find((x) => x.id === (q.get('id') || 'focus'));
  return s ? { space: s, fav: q.get('fav') === '1' } : null;
};
const withIntent = (welcome) => { const n = nextSpace(); return n && n.fav ? welcome + ' — ' + favSavedLine(n.space) : welcome; };
// C4: with `next`, the card's way out returns there; without it, to the directory.
function AuthWayBack() {
  const n = nextSpace();
  const back = n ? { href: `Space details.html?id=${n.space.id}`, label: tr(`العودة إلى ${spaceName(n.space)}`, `Back to ${spaceName(n.space)}`) }
    : pageParams.get('next') ? { href: 'Home.html', label: tr("العودة إلى الرئيسية", "Back to home") }
    : { href: 'Directory.html', label: tr("تصفّح المساحات بدون حساب", "Browse spaces without an account") };
  return <AButton variant="ghost" size="sm" asChild><a href={back.href}>{back.label}</a></AButton>;
}
```
Export `nextSpace, withIntent, AuthWayBack`.
- **The toasts:** `Sign in.html` line 50 → `finishAuth(withIntent(tr("أهلًا بعودتك", "Welcome back")))`;
  `Register.html` line 68 → `finishAuth(withIntent(tr(…the existing welcome…)))`; `useGoogleSignIn`: a new
  account → `finishAuth(withIntent(tr("أهلًا سارة، تم إنشاء حسابك", "Welcome Sara, your account is ready")))`;
  linked → `finishAuth({ title: <linked title>, description: <linked description>, persist: true }, ...(nextSpace() && nextSpace().fav ? [favSavedLine(nextSpace().space)] : []))`
  (the two strings of `demoToast('linked')`, 3.0). The linked toast and the welcome are two different
  kinds, so a linked return with a heart gives two toasts (S8).
- **The way back:** `Sign in.html` line 85 → `<AuthWayBack />`. `Register.html` footer: after the «لديك
  حساب؟» `<p>` (line 103) add `<AuthWayBack />`.
- **`next` kept:** `Sign in.html` line 75 → `href={withNext('Forgot password.html')}`; `Forgot
  password.html` line 80 → `href={withNext('Sign in.html')}`. The reset link comes through the email and
  cannot carry `next`; the reset's success «تسجيل الدخول» stays plain.
- **AC-019:** `Reset password.html`: after the three state blocks, inside `Card`, add
  `{state !== 'success' && <CardFooter className="flex flex-col gap-2"><Button variant="link" size="sm" asChild><a href="Sign in.html">{tr("العودة إلى تسجيل الدخول", "Back to sign in")}</a></Button></CardFooter>}`
  (`CardFooter` is already destructured).
- **AC-017:** `Sign in.html` line 58 → `tr("سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.", "Sign in to save your favourite spaces and follow your reports, or to manage your space.")`.
- **Board section 05:** frame «3 · Back on the space · toast» → `toast=welcomefav` (board `src` and the
  INDEX row of section 05).
- **Q1 yes — `Space details.html`:**
  - line 44 (report description) → `tr("سجّل الدخول لتجد الردّ على بلاغك في «بلاغاتي».", "Sign in to find the reply to your report in “My reports”.")`;
  - line 134 → `pageParams.get('dialog') === 'signin' ? 'fav' : pageParams.get('dialog') === 'signin-report' ? 'report' : false`;
  - **the save failing on return (P8):** line 45 → `React.useState(pageParams.get('fav') === '1' && !actionFails('fav'))`,
    and an effect: when `fav=1` and `actionFails('fav')`, after 400 ms
    `toast.error(tr(\`تعذّر حفظ ${spaceName(space)} في المفضّلة\`, \`Couldn’t save ${spaceName(space)} to your favourites\`), { action: { label: tr("إعادة المحاولة", "Try again"), onClick: () => { setFav(true); toast.success(favSavedLine(space)); } } })`.
  - frames F11, F12.
- **Q1 no:** AC-018 and the failure state are not drawn; `CHANGES.md`'s C4 line ends «**AC-018's line and
  the save's failure on return wait on the space page's next item.**».

Board/INDEX: F8–F10 (+F11, F12).

### 3.4 One «تسجيل الدخول» card — AC-006 with C1, C2 and C5's password toast (commit 4)

`Settings.html`, replacing `PasswordForm` and `SecurityCard` (lines 88–173):

**`PasswordForm({ onDone, onBack })`** — always with the current password:
- state as now (`cur`, `pw`, `errors`, `submitted`, `loading`), `const left = useRetryAfter(demo === 'ratelimit');`
- `<form id="pw-form" …>`: `<RateLimitAlert left={left} />`; the current `PasswordField`; the new
  `PasswordField`; then
  `<p className="text-caption text-muted-foreground">{tr("تغيير كلمة المرور يسجّل خروجك من كل الأجهزة الأخرى", "Changing your password signs you out on all your other devices")}</p>`
  (C2, above the submit: S2);
  then `<div className="flex flex-wrap gap-2"><Button type="submit" loading={loading} disabled={left > 0}>{tr("حفظ كلمة المرور", "Save password")}</Button><Button type="button" variant="ghost" onClick={onBack}>{tr("رجوع", "Back")}</Button></div>`.
- On open, an effect focuses `#pw-form input` (the current password).
- Success → `onDone()`.

**`MethodRow({ label, caption, end })`**:
`<div className="flex flex-wrap items-center justify-between gap-2"><div className="flex flex-col gap-1"><span className="text-label">{label}</span><span className="text-body-sm text-muted-foreground">{caption}</span></div>{end}</div>`.

**`SetPasswordByEmail({ user })`** (C1):
```js
const [sent, setSent] = React.useState(demo === 'linksent');
const limit = useRetryAfter(demo === 'ratelimit');
const [left, setLeft] = useCountdown(demo === 'linksent' ? 60 : 0);
const send = useActionRun('setlink');            // ?fail=setlink: the P8 failure toast with «إعادة المحاولة»
const ask = () => send.run(() => { setSent(true); setLeft(60); });
```
- Sent → `<LinkSent message={tr("أرسلنا إلى بريدك رابطًا لتعيين كلمة المرور. الرابط صالح لمدة ساعة. تفقّد مجلد الرسائل غير المرغوب فيها.", "We sent a link to set your password to your email. The link is valid for one hour. Check your spam folder.")} email={user.email} left={left} onResend={ask} resending={send.busy} fullWidth={false} />`
  — no «استخدم بريدًا آخر»: the address is the account's (S3).
- Not sent → `<div className="flex flex-col gap-2"><RateLimitAlert left={limit} /><p className="text-body-sm text-muted-foreground">{tr("لتسجيل الدخول بالبريد وكلمة مرور أيضًا، نرسل رابطًا إلى بريدك", "To also sign in with your email and a password, we send a link to your email")}</p><Button variant="outline" className="self-start" loading={send.busy} disabled={limit > 0} onClick={ask}>{tr("أرسل رابط تعيين كلمة المرور", "Send a link to set a password")}</Button></div>`.

**`SignInCard({ user })`** (replaces `SecurityCard`):
```js
const hasPassword = user.method !== 'google';
const hasGoogle = user.method !== 'email';
const [open, setOpen] = React.useState(hasPassword && (pageParams.get('pw') === 'open' || demo === 'wrongpw' || demo === 'ratelimit'));
const focusChange = () => setTimeout(() => { const b = document.getElementById('pw-change'); if (b) b.focus(); }, 0);
```
```jsx
<Card>
  <CardHeader>
    <CardTitle>{tr('تسجيل الدخول', 'Signing in')}</CardTitle>
    <CardDescription>{tr('الطرق التي تدخل بها إلى حسابك.', 'The ways you sign in to your account.')}</CardDescription>
  </CardHeader>
  <CardContent className="flex flex-col gap-4">
    {hasGoogle && <MethodRow label="Google" caption={<>{tr('تسجّل الدخول باستخدام Google', 'You sign in with Google')} · <Ltr>{user.email}</Ltr></>} end={<Badge variant="success">{tr('مربوط', 'Linked')}</Badge>} />}
    {hasGoogle && <Separator />}
    <MethodRow label={tr('كلمة المرور', 'Password')}
      caption={hasPassword ? tr('تسجّل الدخول ببريدك وكلمة المرور', 'You sign in with your email and password') : tr('لم تُعيَّن بعد', 'Not set yet')}
      end={hasPassword && !open && <Button id="pw-change" variant="outline" size="sm" aria-expanded={false} aria-controls="pw-form" onClick={() => setOpen(true)}>{tr('تغيير', 'Change')}</Button>} />
    {hasPassword && open && <PasswordForm onBack={() => { setOpen(false); focusChange(); }} onDone={() => { setOpen(false); toast.success(tr('تم تغيير كلمة المرور، وسُجّل خروجك من الأجهزة الأخرى', 'Password changed, and you were signed out on your other devices')); focusChange(); }} />}
    {!hasPassword && <SetPasswordByEmail user={user} />}
  </CardContent>
</Card>
```
- `Separator` from the bundle; if `window.MasahaDesignSystem.Separator` is undefined, use
  `<div role="none" className="h-px bg-border" />` instead (say so in the report).
- **No footer, no `AlertDialog`** (C2). Remove `AlertDialog…` from line 26's destructuring.
- Rows only for the methods the account has: no «Google — غير مربوط» row, since Settings cannot link
  Google (S4).
- `SettingsScreen`: `<SecurityCard>` → `<SignInCard>`.

**Board:** section 17's two frames «Settings · sign out of all devices (confirm) — desktop 1440 / phone 390»
→ label «Settings · changing the password (signs out the other devices) — desktop 1440» / «… — phone 390»,
`src` `Settings.html?auth=1&pw=open`; the same two INDEX rows (screenshot links unchanged). New frames F13,
F14.

### 3.5 C5 — a session change says what it did elsewhere (commit 5)

- **The Google link's toast** is 3.0's `linked` (title, description, `persist`) and 3.3's linked
  `finishAuth`. Nothing more in this commit for it but the board label: section 06's frames «After Google ·
  accounts linked (toast)» keep their URL; their label gains « — kept until closed» (board and INDEX).
- **`Change password.html`:**
  - line 7's comment → `// A first sign-in with a temporary password, given by the Masaha team (an owner; an admin's recovery) or by the space's owner (reception). No site navigation until it's changed; then on to where the role lands, as RequirePasswordChange does (C5).`
  - add above `ForcedChangeScreen`:
    ```js
    const ROLE_HOME = { owner: 'Owner overview.html', reception: 'Desk.html?role=reception', admin: 'Admin overview.html', user: 'Home.html?auth=1' };
    const forcedRole = ROLE_HOME[pageParams.get('role')] ? pageParams.get('role') : 'owner';
    ```
  - line 19's `location.href = carryParams('Home.html?auth=1')` → `carryParams(ROLE_HOME[forcedRole])`.
  - line 31 → `tr('كلمة المرور التي دخلت بها مؤقتة، أُعطيت لك من فريق مساحة أو من صاحب المساحة. اختر كلمة مرور خاصة بك للمتابعة.', 'The password you signed in with is temporary, given to you by the Masaha team or by the space’s owner. Choose your own password to continue.')`.
  - The toast «حُفظت كلمة المرور الجديدة» stays (built `passwordChange.saved`); `OwnerShell` and
    `AdminShell` render `PageToaster`, so it shows on arrival.
- Board/INDEX: F15.

### 3.6 C6 — one account area, one name (commit 6); with AC-011, AC-012, AC-013

**`masaha/account.jsx` `AccountShell`:**
- line 148's settings link label → `tr('إعدادات حسابي', 'Account settings')`.
- After `const user = getUser();` add:
  ```js
  // C6 (AC-011): the account's pages need a session, as the route's RequireAuth does: signed out, the
  // visitor is sent to sign in, and comes back here.
  React.useEffect(() => { if (!user) location.replace(carryParams('Sign in.html?next=' + encodeURIComponent(location.pathname.split('/').pop() + '?auth=1'))); }, []);
  if (!user) return null;
  ```
  and delete the signed-out branch (line 167–169): the children render unconditionally.
- The nav (line 155): `aria-label` → `aria-labelledby="account-nav-label"`; first child
  `<span id="account-nav-label" className="hidden px-3 pb-1 text-caption text-muted-foreground lg:block">{tr('حسابي', 'My account')}</span>`.
- Add `const UNLISTED_LINE = tr('لم تعد هذه المساحة معروضة في الدليل', 'This space is no longer listed in the directory');`
  (used by C7) and export it.

**`Settings.html`:** `<title>` → `إعدادات حسابي — مساحة`; line 179's `title` → `tr('إعدادات حسابي', 'Account settings')`;
line 181's `max-w-2xl` → `max-w-3xl`.

**AC-012 (`ProfileCard`):** replace the email `Field` (lines 45–47) with:
```jsx
<div className="flex flex-col gap-1">
  <span className="text-label">{tr('البريد الإلكتروني', 'Email')}</span>
  <span dir="ltr" className="self-start text-body">{user.email}</span>
  <span className="text-caption text-muted-foreground">{tr('تسجّل الدخول بهذا البريد', 'You sign in with this email')}</span>
</div>
```
No link (the decision: no change promise).

**AC-013 (`PreferencesCard`):**
- mode: `const p = pageParams.get('theme'); const [mode, setMode] = React.useState(p === 'dark' || p === 'light' ? p : 'system');`
  with the comment `// AC-013: the device's setting until a choice is stored (foundation §6). The prototype stores none: ?theme= stands for one.`
- Language `Field` gets `helper={tr('تُحفظ في حسابك', 'Saved to your account')}`, theme `Field` `helper={tr('على هذا الجهاز', 'On this device')}`.
- Language toggle: `const [lang, setLang] = React.useState(LANG);` `value={lang}`, and
  ```js
  // P8's exception: the change shows in place, so only its failure is announced.
  const pickLang = (v) => {
    if (!v || v === LANG) return;
    setLang(v);
    setTimeout(() => {
      if (!actionFails('language')) return switchLang();
      setLang(LANG);
      toast.error(tr('تعذّر حفظ اللغة', 'Couldn’t save the language'), { action: { label: tr('إعادة المحاولة', 'Try again'), onClick: () => pickLang(v) } });
    }, ACTION_MS);
  };
  ```
- **Reports' width:** `Reports.html` line 78's `max-w-3xl` is removed (the lists are full width).
- **Board:** section 14's description: «الإعدادات» → «إعدادات حسابي»; section 17's h2 → `Settings «إعدادات حسابي»`
  and its description → «One sign-in card lists how the account signs in»; INDEX heading `## 17 · Settings «إعدادات حسابي»`.
  No new frame (sections 14–19 show it).

### 3.7 C7 — a space that left the directory (commit 7)

**`Favorites.html`:**
- line 28–30 →
  ```js
  // Newest saved first (C8). Palm Hub was saved, then left the directory (`listed: false`, its name only).
  const SAVED = ['focus', 'branch', 'golden', 'unlisted:palm'];
  const UNLISTED = { palm: 'Palm Hub' };
  ```
- The list (lines 60–79): the grid draws only listed ids; after the grid, when any unlisted id is left,
  `<ul className="flex flex-col gap-3">` with, per id:
  ```jsx
  <li key={id}><Card className="bg-muted"><CardHeader>
    <CardTitle className="text-muted-foreground"><SpaceName space={{ name: UNLISTED[id.slice(9)] }} /></CardTitle>
    <CardDescription>{UNLISTED_LINE}</CardDescription>
    <CardAction><Button variant="outline" size="sm" onClick={() => remove(id, UNLISTED[id.slice(9)])}>{tr('إزالة', 'Remove')}</Button></CardAction>
  </CardHeader></Card></li>
  ```
  (S5: a row under the grid, so it never stretches to a card's height).

**`Reports.html`** — the data (lines 27–32) becomes, newest first:
| id | space | field | sent | status | message | note | repliedBy |
|---|---|---|---|---|---|---|---|
| r4 | numberone | ساعات العمل | قبل ساعتين | review | as now | — | — |
| r3 | golden | الأسعار | قبل 3 أيام | fixed | as now | — | — |
| r5 | zm | `tr('الموقع','Location')` | `tr('قبل 5 أيام','5 days ago')` | review | **none** | — | — |
| r2 | white | التواصل | قبل أسبوعين | rejected | as now | as now | `'masaha'` |
| r6 | `listed: false, name: 'Palm Hub'` | الأسعار | `tr('قبل 3 أسابيع','3 weeks ago')` | fixed | `tr('السعر اليومي صار 12 ₪.','The daily price is now ₪12.')` | `tr('صحّحنا السعر اليومي.','We corrected the daily price.')` | `'masaha'` |
| r1 | focus | المرافق | قبل شهر | fixed | as now | as now | `'space'` |
| r0 | numberone | `tr('التواصل','Contact')` | `tr('قبل شهرين','2 months ago')` | fixed | `tr('رقم الهاتف في الصفحة قديم.','The phone number on the page is old.')` | `tr('صحّحنا رقم الهاتف.','We corrected the phone number.')` | `'masaha'` |

r0 carries the comment `// AC-009: answered by the team before Number One's owner was linked; the label follows who answered (repliedBy, from the resolver), not today's verification.`
In `ReportItem`: `const s = r.listed === false ? null : M.spaces.find((x) => x.id === r.space);`
- title: `s ? <a href={spaceHref(s)} className="text-foreground"><SpaceName space={s} /></a> : <span className="text-muted-foreground"><SpaceName space={{ name: r.name }} /></span>`;
- description: `{r.field} · {tr('أُرسل', 'Sent')} {r.sent}{!s && <span className="block">{UNLISTED_LINE}</span>}`.
(The rest of `ReportItem` is commit 8.)

Board/INDEX: F16.

### 3.8 C8 — Favourites whole, My reports paged; with AC-014, AC-016, AC-009 (commit 8)

**`Favorites.html`** (`location.jsx` is already loaded):
- comment above `FavoritesScreen`: `// C8: favourites are answered whole (an exception the API item adds to api-contract §4): no pages. U2 applies here as on Home (AC-014).`
- above the grid, when `ids.length` and the state is ready:
  ```jsx
  <div className="flex flex-wrap items-center justify-between gap-2">
    <ResultCount>{savedCount(ids.length)}</ResultCount>
    <NearMeButton near={near} on={!!near.coords} />
  </div>
  <LocationStatus near={near} sorting={!!near.coords} onPickOnMap={toPick} onChangePick={toPick} onChooseArea={() => { location.href = carryParams('Directory.html?sheet=filters'); }} />
  ```
  with `const toPick = () => { location.href = carryParams('Directory.html?view=map&pick=1'); };` (Home's) and
  ```js
  const savedCount = (n) => (LANG === 'en' ? `${n} saved space${n === 1 ? '' : 's'}` : n === 1 ? 'مساحة واحدة محفوظة' : n === 2 ? 'مساحتان محفوظتان' : n <= 10 ? `${n} مساحات محفوظة` : `${n} مساحة محفوظة`);
  ```
- the listed items: `const items = listed.map((id) => { const s = M.spaces.find((x) => x.id === id); return { s, km: near.coords ? M.distanceKm(near.coords, s) : null }; });`
  and `if (near.coords) items.sort((a, b) => a.km - b.km);` — distances only while the location is in use.
- The description (line 50) stays.

**`Reports.html`:**
- tabs: `React.useState(['open', 'closed'].includes(pageParams.get('tab')) ? pageParams.get('tab') : 'all')`;
  line 76's label → `tr('تمت المراجعة', 'Reviewed')`.
- `?demo=pages` (S6), after the table of 3.7:
  ```js
  // P6 needs a list long enough to page: ?demo=pages adds 21 older reports, generated the same way each time.
  const DEMO_FIELDS = [tr('الأسعار', 'Prices'), tr('ساعات العمل', 'Opening hours'), tr('التواصل', 'Contact'), tr('الموقع', 'Location'), tr('المرافق', 'Amenities')];
  const DEMO_REPORTS = pageParams.get('demo') !== 'pages' ? [] : Array.from({ length: 21 }, (_, i) => {
    const sp = ['focus', 'branch', 'golden', 'numberone', 'white', 'zm'][i % 6];
    return { id: 'g' + i, space: sp, field: DEMO_FIELDS[i % 5], sent: tr('في ', 'on ') + longDate(isoLocal(new Date(2026, 7, 10 - 3 * i))), status: i % 4 === 3 ? 'rejected' : 'fixed',
      message: i % 3 === 0 ? undefined : tr('المعلومة في الصفحة لم تعد صحيحة.', 'The information on the page is no longer right.'),
      note: tr('شكرًا، راجعنا المعلومة.', 'Thanks, we checked it.'), repliedBy: M.spaces.find((x) => x.id === sp).verified ? 'space' : 'masaha' };
  });
  ```
  and `const ALL_REPORTS = REPORTS.concat(DEMO_REPORTS);` read by the screen in place of `REPORTS`.
- the list: `const paged = usePaged(list);` the section renders `paged.rows.map(…)`, then, when
  `list.length`, `<div className="flex flex-wrap items-center justify-between gap-3"><ResultCount>{paged.summary}</ResultCount>{paged.nav}</div>`
  (Announcements' layout).
- `ReportItem`:
  - **message optional:** `{r.message && <p …>}`; the toggle only with a message.
  - **`dir="auto"`** on the message `<p>` and on the reply's `<p>`.
  - **the toggle only when the clamp cuts:**
    ```js
    const ref = React.useRef(null);
    const [cut, setCut] = React.useState(false);
    React.useLayoutEffect(() => {
      const check = () => { const el = ref.current; if (el && !open) setCut(el.scrollHeight > el.clientHeight + 1); };
      check(); window.addEventListener('resize', check); return () => window.removeEventListener('resize', check);
    }, [open]);
    ```
    `ref={ref}` on the message `<p>`; the button shows when `cut || open`; `long` (line 43) is removed.
  - **AC-009:** the reply label → `r.repliedBy === 'space' ? tr('ردّ إدارة المساحة', 'Reply from the space') : tr('ردّ فريق مساحة', 'Reply from the Masaha team')`.
- **Board:** section 16's description → «Newest first · الكل · قيد المراجعة · تمت المراجعة». F17, F18.

### 3.9 AC-021 — the reset email (commit 9)

`Reset email.html`:
- line 18: `مرحبًا سارة،` → `مرحبًا،`.
- after the button's `</td></tr></table>` (line 22), before the validity `<p>` (line 23), insert:
  ```html
  <p style="clear:both;margin:0;padding-top:16px;font-size:13px;line-height:20px;color:#5c6567;">إن لم يعمل الزر، انسخ هذا الرابط:</p>
  <p dir="ltr" style="margin:4px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:20px;color:#02787d;text-align:left;word-break:break-all;">https://masaha.example/reset-password#token=…</p>
  ```
  and change the validity `<p>`'s `padding-top:24px` to `padding-top:16px` (the `clear:both` moves up).
- line 26 (English): `Hi Sara, you asked…` → `Hi, you asked…`, and after its `</p>` insert
  `<p style="margin:0 0 8px;font-size:13px;line-height:20px;color:#5c6567;">If the button doesn't work, copy this link: <span style="color:#02787d;word-break:break-all;">https://masaha.example/reset-password#token=…</span></p>`.
- The domain is `masaha.example` (an archive stands-in; the API builds `${webOrigin}/reset-password#token=…`).
  The email is the archive's own file with inline hex colours, outside the design system's token rule,
  as it was.

### 3.10 §7 — the location line tells the truth (commit 10)

"Near me" now sorts on the server: the device's location reaches the API, rounded on the device, never
stored or logged. The new wording says exactly that and no more (no precision is documented yet):
- **`shared.jsx` line 526** → `const PRIVACY_LINE = tr("يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.", "Your location is sent rounded, only to sort spaces by distance, and is never stored.");`
- **`shared.jsx` line 18's comment** → `// The location is kept in this tab; it is sent, rounded on the device, only to sort by distance, and the server neither stores nor logs it (DECISIONS_PUBLIC, 2026-10-13).`
- **Where it shows** (no change needed in those files, they read `PRIVACY_LINE`): `location.jsx`'s four
  states — locating, imprecise, denied, in use — on Home, the Directory (list and map) and Favourites (3.8).
- **Q2 yes — `Directory.html` line 353** (the map's picking card): `… نحسب المسافات منه، ويبقى على جهازك فقط.` →
  `… نرتّب المساحات حسب المسافة منه، ويُرسَل مقرَّبًا ولا يُحفظ.`; English `… We measure distances from it, and it stays on your device.` →
  `… We sort the spaces by distance from it; it is sent rounded and never stored.`
- **Q2 no:** `CHANGES.md`'s line ends «**The map's picking card still says «ويبقى على جهازك فقط» (`Directory.html`): it waits on the public pages' next item.**».
- No new frame: `Home.html?loc=granted`, `Directory.html?loc=denied` and `Directory.html?view=map&loc=picking`
  (board) show it.

---

## 4. Questions for the owner, stronger decisions, design issues

### Questions (the build waits on these)
| | Question | Recommend | Under yes | Under no |
|---|---|---|---|---|
| **Q1** | `Space details.html` is in neither batch's list. C4 needs it for AC-018's line, the report variant's frame (`?dialog=signin-report`) and the save failing on return (`?fail=fav`). Add it to this batch for those three? | **yes** — no other batch touches it; three small edits | 3.3's Q1 block, F11, F12 | 3.3's Q1-no line in `CHANGES.md` |
| **Q2** | `Directory.html:353` repeats the old promise («ويبقى على جهازك فقط») in the map's picking card. Add that one line to this batch? | **yes** — §7 asks for every place it shows | 3.10's Q2 block | 3.10's Q2-no line |
| **Q3** | AC-020 is the design system's (`PasswordRules`). Draw the fourth rule in the prototype's own `PasswordRules` too («طويلة جدًا — اختصرها», only when broken, in `destructive`, over 72 UTF-8 bytes; `Register.html?state=toolong`)? | **yes** — the prototype is what the web is built from; one rule in `auth.jsx` | add to commit 1: `PASSWORD_RULES` gains `{ id: 'bytes', label: tr("طويلة جدًا — اختصرها", "Too long — shorten it"), test: (v) => new TextEncoder().encode(v).length <= 72, onlyBroken: true }`, `PasswordRules` skips an `onlyBroken` rule that passes and draws a broken one in `text-destructive` with `ACircleAlert` at once; `DEMO.toolong` = 40 «ب» + `1`; an INDEX parameter row | `CHANGES.md`'s AC-022 line notes AC-020 as worker A's |

### Stronger decisions (proposed; recommended as built above)
| | What | Why | Recommend |
|---|---|---|---|
| **S1** | The 429 clock goes on the account pages only; `shared.jsx`'s `RateLimitNote` (owner and admin pages) keeps «15 دقيقة» | Changing it renders differently on the owner's pages while their batch runs; recorded as DI-30 | yes |
| **S2** | C2's line sits **inside the form, above «حفظ كلمة المرور»**, not under the buttons | The consequence is read before the act (2b's rule: say what an act does, before it) | yes |
| **S3** | Settings' link-sent block has **its own message and no «استخدم بريدًا آخر»** | The forgot page's «إذا كان هذا البريد مسجّلًا لدينا» is untrue for a signed-in account, and its address is the account's | yes |
| **S4** | The card lists **only the methods the account has**; no «Google — غير مربوط» row | Settings cannot link Google (the API links on a Google sign-in); a row with no action is noise | yes |
| **S5** | An unlisted favourite is a **row under the grid** | AC-008's own alternative; it never stretches, and the grid keeps equal cards | yes |
| **S6** | `Reports.html?demo=pages` adds 21 generated reports | A person with 20+ reports is rare, but the second page must be seeable | yes |
| **S7** | `Change password.html?role=owner|reception|admin|user`, owner by default; `user` lands on Home | `landingPath`: a recovered user with no space lands on `/` (#62's recovery reaches users too) | yes |
| **S8** | A Google **link** that also saves a favourite raises **two toasts**: the linked one (kept until closed) and «حُفظت … في المفضّلة» | One is a warning that must stay, the other a confirmation; merged, the confirmation would stay forever | yes |
| **S9** | The privacy wording «يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.» | True to the 2026-10-13 change, names no precision the docs do not yet hold, keeps one line | yes |
| **S10** | «حسابي» is the nav's visible caption from 1024 and its accessible name at every width (`aria-labelledby`) | One name seen and heard; a hidden element still names by `aria-labelledby` | yes |

### Design issues (recorded in the report and `CHANGES.md`'s notes; not built)
| | Issue | For |
|---|---|---|
| **DI-30** | The dashboards' `?state=ratelimit` line still says «15 دقيقة»; the built forms count down | the fix phase's last item, or the next one owning `shared.jsx` |
| **DI-31** | The built `LinkSent` needs C3's always-visible «استخدم بريدًا آخر» and a `message` prop for C1's use in Settings | worker A (C1 with screen 9; C3) |
| **DI-32** | `?auth=linked` stands for both "Google and a password" and "has a dashboard" (`dashboardHref`); right after a link the password is gone (security.md) | the prototype, later; no screen is wrong today |

---

## 5. The files and the boundaries

**This batch's (prompt §6):** `Sign in.html`, `Register.html`, `Forgot password.html`, `Reset password.html`,
`Change password.html`, `Settings.html`, `Favorites.html`, `Reports.html`, `Reset email.html`,
`masaha/auth.jsx`, `masaha/account.jsx`, `masaha/shared.jsx`. **If Q1/Q2 yes:** `Space details.html`,
`Directory.html` (the lines named, nothing else).

**Shared, own section only:** `docs/design/CHANGES.md` (the *Batch 4* section, appended after *Batch 2b*),
`INDEX.md` (the *Batch 4* parameters table after *Batch 3*'s; section 54 after 53; the named rows of 05, 06,
14, 16, 17), `Flows - states.html` (section 54 after the last frame; the named frames of 05, 06, 14, 16, 17),
`README.md` (the frame count in line 23 only).

**Never touched:** the owner's batch — `Owner overview.html`, `Owner space profile.html`, `Packages.html`,
`Announcements.html`, `Staff.html`, `Finance.html`, `Owner settings.html`, `Data reports.html`,
`masaha/owner.jsx`, `owner-data.js`, `finance.jsx`, `profile-a.jsx`, `profile-b.jsx`. Also `location.jsx`,
`data.js`, `details-data.js`, `admin*.{jsx,js}`, `Home.html`, `SCREENS.md`, `_ds/`, `_vendor/`,
`scripts/`, `masaha.css` (no new rule is needed), everything outside `docs/design/`.

**The second to merge** (this or `design/owner`) rebases: keeps both `CHANGES.md` sections, renumbers its
INDEX section (54 → 55) and moves its board section's `top` values below the other's last row, and sets
README's count to the sum.

---

## 6. The commits, in order

Each subject counted (`docs(design): ` is 14). Stage by path only. No `Co-Authored-By`, no "generated with".
**Board positions:** section 54's header `left:40px;top:145730px`; rows R1 `top:145820px`, R2 `146900`,
R3 `147980`, R4 `149060`; phone lefts 40, 510, 980, 1450, 1920, 2390 (R1, R2); R3/R4: 1440 at 40, then
phones/desktops as given.

**Commit 1 — `docs(design): auth pages catch up with the code` (47)**
Files: `masaha/shared.jsx`, `masaha/auth.jsx`, `Sign in.html`, `Register.html`, `Forgot password.html`,
`Reset password.html`, `docs/design/CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
- Section header: `<div class="section" style="left:40px;top:145730px"><h2>Batch 4 — the account</h2><p>The auth pages as built · getting in keeps the intent · one sign-in card · one account area · a space that left the directory</p></div>`
- Frames (R1, 390×844): F1 «Sign in · too many attempts, counting down — phone 390» `Sign in.html?state=ratelimit` (40); F2 «Sign in · Google refused, the address has a password — phone 390» `Sign in.html?google=notallowed` (510); F3 «Register · email already registered, on its field — phone 390» `Register.html?state=exists` (980); F4 «Forgot · a reset link already open — phone 390» `Forgot password.html?state=linkopen` (1450); F5 «Forgot · resends spent — phone 390» `Forgot password.html?state=spent` (1920); F6 «Reset · the link could not be checked — phone 390» `Reset password.html?state=checkfailed` (2390).
- INDEX: `## 54 · Batch 4 — the account`, the line «Added by the account fix (`CHANGES.md` › *Batch 4*). No screenshot yet: `screens/` is regenerated once, at the end of the fix phase.», the table header, rows F1–F6. The parameters table `### Batch 4 — the account and signing in` (after *Batch 3*'s), its rows for this commit:
  - `| \`?state=ratelimit\` | Sign in, Register, Forgot password, Settings | the 429 counting down from 0:42 (the server's \`Retry-After\`), the submit disabled until it ends (AC-022) |`
  - `| \`?google=error\` · \`notallowed\` · \`unavailable\` · \`off\` | Sign in, Register | Google's failure, worded per code; \`off\`: no client id, so no button and no «أو» |`
  - `| \`Forgot password.html?state=loading\` · \`unreachable\` · \`linkopen\` · \`spent\` | the forgot page | the recovery's server-held steps, the address masked as the server holds it |`
  - `| \`Reset password.html?state=loading\` · \`unreachable\` · \`checkfailed\` | the reset page | the same; \`checkfailed\`: the link's check refused (a 429), «افتح الرابط من بريدك الإلكتروني مرة أخرى.» |`
- README: `493 frames in 53 sections` → `499 frames in 54 sections`.
- `CHANGES.md`: the heading `## Batch 4 — the account and signing in (2026-10-13)`, the intro
  «Reviewed as AC-001…AC-022 (G1–G4); decided in `DECISIONS_ACCOUNT.md` as the owner amended it on 2026-10-13 (the forced change's author), with the owner's addition of the same day: the location's privacy line. The design-system item (AC-020), the API's `listed` and `repliedBy`, the documents' rule changes and the web's own items belong to their owners. Where the built web is ahead (AC-022) the prototype catches up; where it is behind (C3, AC-017, AC-019) the prototype leads and the web follows.»,
  the table header `| Decision | What changed | Where |`, and the row:
  `| **AC-022** | The auth pages catch up with the built code. A 429 counts down from the server's \`Retry-After\` — «محاولات كثيرة، حاول بعد 0:42» — with the submit disabled beside it, where it said a fixed «15 دقيقة». An address that already has an account is told on its field («يوجد حساب بهذا البريد الإلكتروني.») with «سجّل الدخول بهذا البريد» under it, not in an Alert above the form. Google's failures say what happened, per code, under «تعذّرت المتابعة باستخدام Google»; with no client id there is no button and no «أو». The recovery's steps the server holds are drawn — loading, unreachable, «فتحت رابط الاستعادة», a link that could not be checked, resends spent — with the address masked as the server answers it («s•••@example.com»), and the resend waits on an m:ss clock. The dashboards' 429 line keeps its wording (DI-30) | \`masaha/auth.jsx\`, \`shared.jsx\`, \`Sign in.html\`, \`Register.html\`, \`Forgot password.html\`, \`Reset password.html\`, \`INDEX.md\` |`
  (Q3 yes: append to the row «, and a password over 72 bytes is refused by a fourth rule, «طويلة جدًا — اختصرها», shown only once broken (AC-020, drawn ahead of worker A)».)

**Commit 2 — `docs(design): a mistyped email has a way out` (44)**
Files: `masaha/auth.jsx`, `Forgot password.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
- F7 «Forgot · sent to a mistyped address, another email — phone 390» `Forgot password.html?state=sent&email=sara@gmial.com` (R2, 40).
- INDEX parameter row: `| \`Forgot password.html?state=sent&email=<address>\` | the forgot page | the link sent to that address, shown masked, so a typo shows («s•••@gmial.com») |`
- README → `500 frames`.
- `CHANGES.md`: `| **C3 (AC-003)** | A mistyped address no longer strands the forgotten password. The sent step always offers «استخدم بريدًا آخر» under the resend, at every moment of its clock, back to an empty email form with the focus in it (a new request ends the old recovery); and it shows the address the server holds, masked, so «s•••@gmial.com» gives the typo away. Once the resends are spent, the built «أدخل بريدك الإلكتروني من جديد» stays. **The built \`LinkSent\` shows the way back only then; it follows (DI-31)** | \`masaha/auth.jsx\` (\`LinkSent\`), \`Forgot password.html\` |`

**Commit 3 — `docs(design): getting in keeps the intent` (41)**
Files: `masaha/auth.jsx`, `Sign in.html`, `Register.html`, `Forgot password.html`, `Reset password.html`,
(Q1: `Space details.html`), `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
- F8 «Sign in · from a space, the way back to it — phone 390» board `Sign%20in.html?next=Space%20details.html%3Fid%3Dfocus%26auth%3D1%26fav%3D1`, INDEX `Sign in.html?next=Space details.html?id=focus&auth=1&fav=1` (R2, 510); F9 «Back on the space · welcome and the saved favourite — phone 390» `Space details.html?id=focus&loc=none&auth=1&fav=1&toast=welcomefav` (R2, 980); F10 «Reset · new password, a way back — phone 390» `Reset password.html?state=typing` (R2, 1450). Q1: F11 «Report → sign-in dialog, the reply in «بلاغاتي» — phone 390» `Space details.html?id=focus&loc=none&dialog=signin-report` (R2, 1920); F12 «Back on the space · the save failed — phone 390» `Space details.html?id=focus&loc=none&auth=1&fav=1&fail=fav&toast=welcome` (R2, 2390).
- Section 05's frame 3 URL → `toast=welcomefav` (board and INDEX).
- INDEX parameter rows: `| \`?toast=welcomefav\` | \`Space details.html\` | the return from signing in to save: «أهلًا سارة، تم إنشاء حسابك — حُفظت فوكس هاب في المفضّلة» (C4) |`; Q1: `| \`Space details.html?dialog=signin-report\` | the space page | the sign-in dialog of «الإبلاغ», with AC-018's reason |` and `| \`Space details.html?…&fav=1&fail=fav\` | the space page | the favourite's save failing on the way back: the failure toast with «إعادة المحاولة» |`.
- README → `503` (Q1: `505`).
- `CHANGES.md`: `| **C4 (G1: AC-004, AC-017, AC-018, AC-019)** | Getting in keeps the intent. The heart that sent someone to sign in is saved on the way back and named in the one toast — «أهلًا بعودتك — حُفظت فوكس هاب في المفضّلة» — and the report reopens its dialog; a Google link, whose toast must stay, raises the saved line as a second toast. With \`next\`, the card's way out returns there («العودة إلى فوكس هاب»), the forgot page and its way back keep it, and Register gains the way out too; the reset form has «العودة إلى تسجيل الدخول». The sign-in card speaks to everyone who signs in: «سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.» <Q1 yes: The report's sign-in reason is the true one, «سجّل الدخول لتجد الردّ على بلاغك في «بلاغاتي».», and a save that fails on the way back says so with «إعادة المحاولة» (P8).> <Q1 no: the sentence of 3.3.> **The web carries the intent with step 10; AC-017 and AC-019 follow in built code** | \`masaha/auth.jsx\`, \`shared.jsx\`, \`Sign in.html\`, \`Register.html\`, \`Forgot password.html\`, \`Reset password.html\`<Q1: , \`Space details.html\`>, \`INDEX.md\` |`

**Commit 4 — `docs(design): one card for how I sign in` (40)**
Files: `Settings.html`, `masaha/auth.jsx` (only if a helper changes), `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
- Section 17's two signout frames repointed (3.4). F13 «Account settings · how I sign in — desktop 1440» `Settings.html?auth=linked` (R3, 40, 1440×1000); F14 «Account settings · Google-only, the link sent — phone 390» `Settings.html?auth=google&state=linksent` (R3, 1512).
- INDEX parameter rows: `| \`Settings.html?pw=open\` | account settings | the password form open in the «تسجيل الدخول» card. Replaces \`?state=signout\`: v1 has no sign-out of all devices (C2) |`; `| \`Settings.html?auth=google&state=linksent\` · \`?fail=setlink\` | the same, a Google-only account | the link to set a password sent, in place; or its sending failing |`.
- README → `505` (Q1: `507`).
- `CHANGES.md`: `| **AC-006, C1 (AC-001), C2 (AC-002)** | One card, «تسجيل الدخول», in place of «الأمان»: a row per method the account has — «Google» with «مربوط», «كلمة المرور» with «تغيير», which opens the form in place (current, new, the rules, «حفظ كلمة المرور», «رجوع») and gives the focus back to «تغيير» when it closes. **A Google-only account sets its first password through the email**, never in a form (security.md; the API answers \`PASSWORD_NOT_SET\`): «لتسجيل الدخول بالبريد وكلمة مرور أيضًا، نرسل رابطًا إلى بريدك» and «أرسل رابط تعيين كلمة المرور», which asks \`POST /auth/password/forgot\` for the session's address and shows the link sent in place, masked, with its clock. **No «تسجيل الخروج من كل الأجهزة» in v1**: the API ends one device's session; the form says, above its submit, «تغيير كلمة المرور يسجّل خروجك من كل الأجهزة الأخرى», and its toast «تم تغيير كلمة المرور، وسُجّل خروجك من الأجهزة الأخرى» (C5). Every dismiss here says «رجوع» | \`Settings.html\`, \`INDEX.md\`, \`Flows - states.html\` |`

**Commit 5 — `docs(design): a session change says so` (38)**
Files: `Change password.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
- Section 06's linked-toast frame labels gain « — kept until closed» (board and INDEX). F15 «Forced change · reception, a neutral author — phone 390» `Change password.html?auth=1&role=reception` (R3, 1982).
- INDEX parameter row: `| \`Change password.html?role=owner\` · \`reception\` · \`admin\` · \`user\` | the forced change | where saving lands: the owner's overview (the default), the desk, the admin's overview, Home |`.
- README → `506` (Q1: `508`).
- `CHANGES.md`: `| **C5 (G2: AC-005, AC-007)** | A session change says what it did elsewhere, in true words. The Google link's toast says the password was removed and the other devices signed out, and stays until it is closed. The forced change no longer says the Masaha team made every temporary password — a receptionist's comes from the space's owner: «كلمة المرور التي دخلت بها مؤقتة، أُعطيت لك من فريق مساحة أو من صاحب المساحة. اختر كلمة مرور خاصة بك للمتابعة.» (the owner's amendment of 2026-10-13, since #62's recovery) — and saving lands where the role lands (\`?role=\`), not on Home. The password change's line is in AC-006's row. **The built \`users.passwordChange.description\` follows** | \`masaha/shared.jsx\` (\`PageToaster\`), \`masaha/auth.jsx\`, \`Change password.html\`, \`INDEX.md\` |`

**Commit 6 — `docs(design): one account area, one name` (40)**
Files: `masaha/account.jsx`, `masaha/shared.jsx` (exports, if not done in 1), `Settings.html`, `Reports.html` (width only), `CHANGES.md`, `INDEX.md`, `Flows - states.html`.
- Board/INDEX: sections 14 and 17 labels (3.6). No new frame; README unchanged.
- INDEX parameter rows: `| \`?auth=0\` | Favourites, My reports, account settings | signed out: straight to sign-in with \`next\`, as the route's \`RequireAuth\` does (AC-011) |`; `| \`Settings.html?fail=language\` | account settings | the language's save failing: the toggle returns, «تعذّر حفظ اللغة» with «إعادة المحاولة» |`.
- `CHANGES.md`: `| **C6 (G3: AC-010, AC-011), AC-012, AC-013** | The account area is one place with one name. The nav, the page's title and h1, and the account menu say «إعدادات حسابي»; from 1024 the nav shows its caption «حسابي», which also names it for a screen reader. The settings are one \`max-w-3xl\` column, Favourites and My reports full width. A signed-out visitor is sent to sign in and back, with no sentence inside the shell. The email is text — the address and «تسجّل الدخول بهذا البريد» — with no input and no change promise (no endpoint changes an email); U11's «تواصل معنا» link there goes with it. The theme starts on «حسب الجهاز» (foundation §6); each preference says where it is kept, «تُحفظ في حسابك» and «على هذا الجهاز»; a failed language save returns the toggle with a failure toast, and a successful one raises none (P8's exception) | \`masaha/account.jsx\`, \`Settings.html\`, \`Reports.html\`, \`Flows - states.html\`, \`INDEX.md\` |`

**Commit 7 — `docs(design): a space that left the directory` (45)**
Files: `masaha/account.jsx`, `Favorites.html`, `Reports.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
- F16 «Favourites · one left the directory — desktop 1440» `Favorites.html?auth=1&loc=none` (R4, 40, 1440×1000). README → `507` (Q1: `509`).
- `CHANGES.md`: `| **C7 (G4: AC-008)** | A space that left the directory is said so, in a word that is not a live status: «لم تعد هذه المساحة معروضة في الدليل» («لم تعد متاحة» read as "full now"). Its name is text, not a link to a page that would not open. On Favourites it is a row under the grid — so it no longer stretches to a card's height — with «إزالة» and «تراجع» (P9); on My reports the report stays, with its status and reply. **The API's \`listed: false\` on \`GET /me/favorites\` and \`/me/reports\` comes later**; the prototype draws it now | \`Favorites.html\`, \`Reports.html\`, \`masaha/account.jsx\` |`

**Commit 8 — `docs(design): favourites whole, reports paged` (45)**
Files: `Favorites.html`, `Reports.html`, `CHANGES.md`, `INDEX.md`, `Flows - states.html`, `README.md`.
- Section 16's description (3.8). F17 «Favourites · nearest first — phone 390» `Favorites.html?auth=1&loc=granted` (R4, 1512); F18 «My reports · two pages, a space that left — desktop 1440» `Reports.html?auth=1&demo=pages` (R4, 1982, 1440×1000).
- INDEX parameter row: `| \`Reports.html?demo=pages\` · \`?tab=open\` · \`?tab=closed\` | My reports | 28 reports, so the list has a second page (P6); the chips set |`.
- README → `509` (Q1: `511`).
- `CHANGES.md`: `| **C8 (AC-015), AC-014, AC-016, AC-009** | **Favourites are answered whole** — a person saves a handful, and a grid that pages is awkward (an exception api-contract §4 gains with the API item) — newest saved first, with their count and U2's «الأقرب إليّ» above them: pressed, the grid is sorted by distance and the cards measure it, under the one \`LocationStatus\` line; off, no distances. **My reports pages** (P6). Its chips are «الكل · قيد المراجعة · تمت المراجعة» («مغلقة» named no badge); «عرض المزيد» shows only when the clamp cuts the message; a report sent without a message shows its field alone; the reporter's and the reply's words are \`dir="auto"\`. **The reply says who really answered** (\`repliedBy\`, from the resolver), not today's verification: Number One's old report reads «ردّ فريق مساحة». **The API's \`repliedBy\` comes later** | \`Favorites.html\`, \`Reports.html\`, \`INDEX.md\` |`

**Commit 9 — `docs(design): the reset email has a link to copy` (49)**
Files: `Reset email.html`, `CHANGES.md`.
- `CHANGES.md`: `| **AC-021** | The reset email greets no one by name («مرحبًا،», "Hi,"), as the built email does (security.md: registration proves no inbox), and under its button carries the link as text, «إن لم يعمل الزر، انسخ هذا الرابط:», for clients that strip a styled link | \`Reset email.html\` |`

**Commit 10 — `docs(design): the location line tells the truth` (47)**
Files: `masaha/shared.jsx`, (Q2: `Directory.html`), `CHANGES.md`.
- `CHANGES.md`: `| **The privacy line** (the owner, 2026-10-13) | "Near me" now sorts on the server, so the device's location reaches the API — rounded on the device, never stored or logged (\`DECISIONS_PUBLIC.md\`). «يبقى موقعك على جهازك فقط، ولا يُرسَل إلى أي جهة.» became untrue; it reads «يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.» wherever a location is in play — the four states of the location line on Home, the Directory and Favourites<Q2 yes: , and the map's picking card>. **The web says the same when it builds the line** | \`masaha/shared.jsx\`<Q2: , \`Directory.html\`> |`

Then, once, at the end of the section, a `### Notes` list:
- «**DI-30:** the dashboards' 429 line (\`RateLimitNote\`) still says «15 دقيقة».»
- «**DI-31:** the built \`LinkSent\` needs C3's way back at every moment and a \`message\` for Settings.»
- «**DI-32:** \`?auth=linked\` stands for both "Google and a password" and "has a dashboard".»
(The notes go in commit 10.)

PR title: `design: the account and signing in`. Labels `docs`, `area:docs`; assignee the owner. Not merged.

---

## 7. The executor's procedure

1. **Branch** (in `C:\Users\basel\masaha-design-b`): `git fetch origin`; check `git status` clean and
   `git rev-parse HEAD origin/main` equal; `git switch --no-track -c design/account origin/main`.
2. **Server** (background): `cd docs/design/prototype && python -m http.server 5347 --bind 127.0.0.1`.
   Base URL `http://127.0.0.1:5347/`, spaces as `%20`.
3. **Before images**, from the clean tree, before any edit, headless Chrome (CDP), saved to
   `C:\Users\basel\Downloads\design-fix-account\` as `<decision>-<page>-<width>-before.png`
   (decision: `AC022`, `C3`, `C4`, `AC006`, `C5`, `C6`, `C7`, `C8`, `AC021`, `PRIV`): for each frame of §8's
   table, at 390 and 1440 (and 768 for Settings, Favourites, Reports), Arabic light. The same names with
   `-after` after the commit that changes them.
4. **Per commit:** make the commit's changes (§3), then run from the repository root
   `node docs/design/scripts/check-parse.mjs` and `node docs/design/scripts/check-classes.mjs` (both must
   pass; a new dead class is fixed, never added to `KNOWN`); `grep -n` each new top-level name (§9) across
   `docs/design/prototype` to prove it is declared once; open the commit's frames (§8) at 390, 768, 1440 ×
   ar/en × light/dark and look (§8 says what for); capture the `-after` images; `git add <each path>`;
   `git commit -m "<subject>"`; count the subject again before committing.
5. **`npm run format:check` and `npm run check:links`** are not run locally: nothing is installed in
   `masaha-design-b`. CI runs both; `.prettierignore` excludes `docs/design/` and `*.md`, so format cannot
   see this item; `check:links` checks the INDEX and CHANGES links.
6. **Push:** `git push -u origin design/account`.
7. **PR:** write the body to `C:\Users\basel\Downloads\design-fix-account\PR_BODY.md` (below), then
   `gh pr create --assignee @me --title "design: the account and signing in" --label docs --label area:docs --body-file "C:\Users\basel\Downloads\design-fix-account\PR_BODY.md"`.
8. **Wait for CI and `CLEAN`:** `gh pr checks <n>` until every check passes (bound the wait: at most 20
   checks, 60 s apart); `gh pr view <n> --json mergeStateStatus --jq .mergeStateStatus` must print `CLEAN`.
   A failure is fixed in the commit it belongs to (fixup + `git rebase --autosquash`, then
   `git push --force-with-lease`), never with a fix commit. **Never merge.** `jq` is not installed: use
   `--jq`.
9. **Conflict check:** `gh pr list --state open --json number,headRefName --jq '.[] | "\(.number) \(.headRefName)"'`;
   for each: `git fetch origin <head>` and `git merge-tree --write-tree --name-only HEAD origin/<head>`;
   report each result (clean, or the conflicting files: for `design/owner`, expected only in `CHANGES.md`,
   `INDEX.md`, `Flows - states.html`, `README.md`).
10. **Report** to `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_ACCOUNT_REPORT.md`, sections: *The PR and
    its head* (number, URL, head SHA, CI, `CLEAN`); *The commits* (subject, files); *What was run* (each check
    with its numbers, the frames looked at); *Problems met*; *Anything unexpected*; *The conflict check*
    (step 9); *Departures from the plan* (each, with why; "none" if none); *Q1–Q3 as answered*.
11. **Stop everything:** stop the server by its PID, close every Chrome started, stop every background
    shell; `netstat -ano | findstr :5347` must print nothing.

**The PR description** (fill the bracketed numbers):
```
## Summary

Design fix 4, batch 4 of the design review: signing in, registering, the forgotten password, the forced change, «إعدادات حسابي», Favourites, «بلاغاتي», in the living prototype. It applies `DECISIONS_ACCOUNT.md` as the owner amended it on 2026-10-13 (the forced change's author), and the owner's addition of the same day: the location's privacy line.

- **The auth pages catch up with the code** (AC-022): the 429 clock, `EMAIL_TAKEN` on its field, Google per code, the recovery's steps, the masked address.
- **A mistyped email has a way out** (C3).
- **Getting in keeps the intent** (C4).
- **One «تسجيل الدخول» card** (AC-006): a Google-only account sets its password through the email (C1); no sign-out of all devices (C2).
- **A session change says so** (C5).
- **One account area, one name** (C6, AC-011…013).
- **A space that left the directory** (C7).
- **Favourites whole, My reports paged** (C8, AC-009, AC-014, AC-016).
- **The reset email** has a link to copy and no name (AC-021).
- **The privacy line** says the location is sent rounded and never stored.

`docs/design/CHANGES.md` › *Batch 4* has one line per decision; `INDEX.md` lists every URL and parameter added or renamed.

## Scope / Acceptance criteria / Out of scope

**Scope:** the plan's §3, inside `docs/design/` only ([n] files).

**Acceptance criteria:** [the §1 checklist, one line each, as built]

**Out of scope:** AC-020 (worker A)[, unless drawn per Q3]; the API's `listed` and `repliedBy`; foundation §13 and api-contract §4; the web's items; the dashboards' 429 line (DI-30); the owner's batch files; `apps/`, `packages/`, features docs, findings; `screens/`.

## Change type

Documentation: the design archive. No product code.

## Evidence

**Run:**
- `node docs/design/scripts/check-parse.mjs`: [x/x] at every commit.
- `node docs/design/scripts/check-classes.mjs`: 0 new dead classes, at every commit.
- `npm run format:check`, `npm run check:links`: in CI ([result]); not run locally (nothing installed in this worktree). Format cannot see `docs/design/`.
- **Frames by eye:** [n] targets × 390/768/1440 × ar/en × light/dark.

**Not run:** the test lanes, build, lint, typecheck: no product code.

## Screenshots

Before/after pairs per decision, in the owner's `Downloads\design-fix-account\` ([n] pairs, [n] new frames). Not committed.

## Definition of Done checklist

- [ ] Acceptance criteria met, scope kept (`docs/design/` only)
- [ ] Lint/typecheck/build: not applicable, no product code
- [ ] Tests in the owning lane: none owns `docs/design/`; the two scripts and the frames stand in
- [ ] No hardcoded user-facing text in product code: none touched; every new prototype string in both languages
- [ ] UI checked RTL/LTR, light/dark, phone/tablet/desktop
- [ ] Authorization: not applicable (the prototype only draws `RequireAuth`'s redirect)
- [ ] Triggered documentation updated: `CHANGES.md`, `INDEX.md`, the board, README's count
- [ ] Nothing claimed as built that is not (the API's `listed`, `repliedBy`; the web's C3, C5, AC-017, AC-019 said to follow)
- [ ] Every claim names its check
- [ ] Atomic history: ten commits, one per decision
```

---

## 8. The reviewer's checklist (and the executor's eyes)

Open each at **390, 768, 1440 × ar/en × light/dark** unless a width is named. Always: no blank page, no
console error, no sideways scroll, nothing cut at the edge.

| Decision | Files to read | Frames | Verify by eye |
|---|---|---|---|
| AC-022 | `auth.jsx` (`RateLimitAlert`, `useRetryAfter`, `GOOGLE_LINES`, `maskEmail`), the four pages | `Sign in.html?state=ratelimit`, `Register.html?state=ratelimit`, `Forgot password.html?state=ratelimit`, `Register.html?state=exists`, `Sign in.html?google=error|notallowed|unavailable|off`, `Forgot password.html?state=loading|unreachable|linkopen|spent`, `Reset password.html?state=loading|unreachable|checkfailed|typing` | the clock ticks, the submit is disabled, both re-enable at 0:00; the email error sits on its field with the link under it and no Alert; each Google line differs, `off` has no «أو»; every address reads `s•••@…` LTR inside Arabic; no «15 دقيقة», no «ثانية» |
| C3 | `LinkSent`, `Forgot password.html` | `?state=sent`, `?state=sent&email=sara@gmial.com` | «استخدم بريدًا آخر» visible while the clock runs; pressing it empties the form and focuses the field |
| C4 | `nextSpace`, `withIntent`, `AuthWayBack`; `Reset password.html` | F8, F9, F10; the live flow from `Space details.html?id=focus&loc=none` (heart → sign in, then → register); `Sign in.html` without `next`; Q1: F11, F12 | one toast naming both; «العودة إلى فوكس هاب» in place of «تصفّح…»; Register's way out; the forgot link keeps `next` (look at its `href`); reset footer in every state but success; the new sign-in description |
| AC-006 C1 C2 | `Settings.html` (`SignInCard`, `MethodRow`, `PasswordForm`, `SetPasswordByEmail`) | `Settings.html?auth=1`, `?auth=linked`, `?auth=google`, `?auth=google&state=linksent`, `?auth=google&fail=setlink` (press the button), `?auth=1&pw=open`, `?auth=1&state=wrongpw`, `?auth=1&state=ratelimit` | one card «تسجيل الدخول», rows aligned at 390 (status/action wraps under the label, not off-screen); «تغيير» opens the form, focus in «كلمة المرور الحالية»; «رجوع» closes it and focus returns to «تغيير»; C2's line above the submit; no «تسجيل الخروج من كل الأجهزة»; Google-only has no password field; sent block in place, button not full width |
| C5 | `shared.jsx` (`PageToaster`, `demoToast`), `Change password.html` | `Home.html?loc=none&toast=linked`; `Change password.html?auth=1`, `?role=reception|admin|user` (save with `gaza2026x1`) | the linked toast has its description and an X, and stays past 10 s; the new forced-change line; each role lands on its page with «حُفظت كلمة المرور الجديدة» |
| C6 AC-011 AC-012 AC-013 | `account.jsx`, `Settings.html` | `Settings.html?auth=1` (1440: caption «حسابي», h1 «إعدادات حسابي», tab title); `Favorites.html?auth=0`, `Reports.html?auth=0`, `Settings.html?auth=0`; `Settings.html?auth=1&fail=language` | redirect with no flash of the shell; email as text, aligned at the start in Arabic; «حسب الجهاز» pressed; captions; the language toggle returns on failure; Settings narrower than Favourites/Reports at 1440 |
| C7 | `Favorites.html`, `Reports.html`, `UNLISTED_LINE` | `Favorites.html?auth=1&loc=none` (1440, 768, 390); `Reports.html?auth=1` | Palm Hub as a short row under the grid; «إزالة» then «تراجع» restores it; the report's name not a link, the line under its field line |
| C8 AC-014 AC-016 AC-009 | `Favorites.html`, `Reports.html` | `Favorites.html?auth=1&loc=granted|denied|none`; `Reports.html?auth=1`, `?demo=pages`, `?tab=closed` | count and «الأقرب إليّ» on one row; sorted by distance with distances only when on; no pagination; reports' summary and steps under the list, page 2 opens; «عرض المزيد» absent on short messages at 1440, present when cut at 390; r5 has no message line; r0's label «ردّ فريق مساحة» |
| AC-021 | `Reset email.html` | at 720 and 390 | no «سارة»/"Sara"; the copy line and the link under the button, the link wrapping inside the card |
| §7 | `shared.jsx` lines 18, 526; Q2 `Directory.html:353` | `Home.html?loc=granted`, `Directory.html?loc=denied`, `Directory.html?loc=imprecise`, `Directory.html?view=map&loc=picking`, `Favorites.html?auth=1&loc=granted` | the new line in each; `grep -rn "على جهازك فقط\|stays on your device" docs/design/prototype` prints nothing (Q2 yes) or only `Directory.html` (Q2 no) |
| Archive | `CHANGES.md`, `INDEX.md`, the board, README | the board, section 54 and the changed frames | each frame label matches its INDEX row; INDEX section 54 rows = the board's; README's count = the INDEX frame count; positions do not overlap batch 3's frames |
| Boundaries | `git diff --stat origin/main...` | — | no file of §5's *Never touched*; ten commits, subjects ≤ 50 |

## 9. The hazards

- **Babel's shared globals.** Every page's scripts share one global scope. **No object rest**
  (`{ a, ...rest }`) anywhere: its `_excluded` helper is page-wide (DI-27). **No top-level `name`** or other
  name the browser owns. **Each new top-level name exists once per page** — `useCountdown` moves from
  `Forgot password.html` to `auth.jsx`, and the page's copy must be deleted, or the page blanks. The new
  names: `RETRY_AFTER`, `mmss`, `useCountdown`, `useRetryAfter`, `maskEmail`, `GOOGLE_LINES`, `LinkSent`,
  `nextSpace`, `withIntent`, `AuthWayBack`, `favSavedLine`, `demoToast`, `UNLISTED_LINE`, `ROLE_HOME`,
  `forcedRole`, `MethodRow`, `SignInCard`, `SetPasswordByEmail`, `savedCount`, `DEMO_FIELDS`,
  `DEMO_REPORTS`, `ALL_REPORTS`, `UNLISTED` — grep each before adding. `README.md`'s check-scripts paragraph
  says so.
- **Hooks order.** `AccountShell` calls its `useEffect` before `if (!user) return null`; `Reset password.html`
  calls `useRetryAfter` at the top of `ResetScreen`, never inside a state branch.
- **The prebuilt CSS.** A utility class not in `_ds_bundle.css` is silently dead. Every class in §3 was
  checked; any other must be checked with `grep -F ".<class>" _ds_bundle.css` (escape `:` as `\:`), and a
  layout-only rule goes to `masaha.css` with tokens only. `check-classes.mjs` must pass, but it does not see
  classes chosen in a condition (`fullWidth ? 'w-full' : 'self-start'`): check those by eye.
- **The vendored bundle** (`prototype/_ds/`, `_vendor/`) is never edited.
- **Truth to the API and the data model.** Nothing on screen the API cannot do: no sign-out of all devices,
  no email change, no password form for a Google-only account, no Google linking from Settings. Live
  status is a state, never a count; «متاحة» never names a space that left the directory.
- **The owner's batch.** Its files (§5) are not opened for editing; `Owner overview.html`,
  `Desk.html`, `Admin overview.html` are only link targets.
- **Look with your eyes.** The scripts and a load matrix see blanks and errors, not layout: #59's F2 and
  #61's eleven fixes were found by eyes. Settings' rows at 390, the redirect, the toast's X, the
  unlisted row under the grid and the reports' toggle can only be judged by looking.
