# AUTH_IN_PLACE — sign in over the page the user was on: the analysis (2026-11-24)

> The owner chose the direction (A19, `DESIGN\AUTH\0_OWNER_DECISIONS.md`) and asked that it be settled on every axis
> before any drawing or code. This file holds the facts (read from `main` = 17a51adc by two read-only passes and
> checked by the supervisor where they decide something) and, per axis, the options with a recommendation. The
> owner's answers go to `0_OWNER_DECISIONS.md` (I1…).

## 0. The finding that changes the size of the task

**The overlay already exists.** A guest who presses the heart or «الإبلاغ عن معلومة غير صحيحة» gets `SignInPrompt`
(`apps/web/src/pages/site/public/SignInPrompt.tsx`), a `Dialog` titled by the reason («سجّل الدخول لحفظ المساحات في
المفضّلة», «سجّل الدخول للإبلاغ عن معلومة»), holding **two links**, «إنشاء حساب» and «تسجيل الدخول», to the full pages
with `?next=`. The pressed action is **held** (`shared/routing/guest/heldIntent.ts`: memory + `localStorage`
`masaha.heldIntent`, 15 min) and runs after the round trip (`useResumeFavorite`, `useReportAction` reopens the report
dialog). So the change is not a new routing system: **the dialog holds the form itself instead of two links**, and the
round trip disappears.

## 1. Facts that bind the decision

**API (no change needed).**
- Sign in, register and Google answer a `Session` (`{user, accessToken}`) and set the cookies in the same answer;
  the access token lives in memory and goes as `Authorization: Bearer`. A deferred `POST /me/favorites/:id` or
  `POST /spaces/:slug/reports` right after an in-place sign-in needs nothing else: no CSRF token exists (ADR 0003),
  no refresh, no cookie read.
- Everything is same-origin; refresh cookie `SameSite=Strict`; `refuseCrossSite` guards refresh, logout and recovery.
- Google: the client posts a GIS ID token (`POST /auth/google`); no redirect, no callback, no return path on the
  server. A new Google user is **created on the spot** (`created: true`); an existing gmail / Workspace email is
  linked (`linked: true`, other sessions end); otherwise 409 `GOOGLE_LINK_NOT_ALLOWED`; 503 when Google is unreachable.
- Rate limits count failures (10 / 15 min per address + email; 50 per address); 429 carries `Retry-After`. Reports
  have their own 10 / hour per user.
- A temporary password: sign-in succeeds with `user.mustChangePassword: true`; every other route answers 403
  `PASSWORD_CHANGE_REQUIRED` until `POST /me/password`.
- The deferred action can still fail on its own: 404 (space no longer listed), 409 `FAVORITES_LIMIT_REACHED`, 200 for
  a repeated report. The server keeps no intent and no return path.

**Web.**
- `react-router` 8, a data router (`createBrowserRouter`); no modal-route / background-location pattern anywhere.
- `/login`, `/register`, `/forgot-password` under `RequireGuest` in `FocusLayout`; `/reset-password`; `/change-password`
  behind `PasswordChangeGate` (mounted in `RootLayout`, redirects with `next`).
- **The landing has one owner** — `RequireGuest` + `landingPath`: a safe `next`, else by role (admin → admin, owner →
  overview, reception → desk, visitor → `/`) (`docs/frontend/architecture.md` §2, line 128).
- Google: the GIS button in **popup** mode; the script loads only when the button renders; one module-level credential
  handler for "the one button on the page"; used only on the two pages (`docs/features/auth.md:67`); COOP
  `same-origin-allow-popups` already set.
- The session is a zustand store; sign-in calls `establishSession(…, {source:'signIn'})`, shows «أهلًا بعودتك» under
  `RETURN_TOAST_ID`; listeners run the held intent; the favourites query turns on with the session.
- Forms: react-hook-form via `useServerForm`, the shared Zod schemas; mutations with `gcTime: 0`.
- Overlays in the layer: `Dialog` (centred, focus trapped and returned), `Sheet` (start / end / bottom; bottom =
  `max-h-[85svh]`), AlertDialog, Popover. **No component switches between a dialog and a sheet by width.**
- Every site page is lazy; `check:build` keeps the dashboard and heavy libraries out of the first download but has
  **no byte budget**. ADR 0011: "the public site must stay light on a weak connection".
- Focus after sign-in moves to `main` on a path change (`useMainFocus`); an overlay changes no path.
- The held intent's rules were built for a round trip through `/login`: `guestLeaving` treats any path change in the
  site shell as leaving; the intent runs on "a sign-in in the tab that held it" or after a reset.

## 2. The decisions, by axis

### I1 — Scope: what happens inside the overlay
- **A. Sign-in only** in the overlay; «إنشاء حساب» and «نسيت كلمة المرور؟» still go to the full pages (today's round
  trip, with `next` and the held intent).
- **B. Sign-in and register in the overlay** (the dialog switches between the two without leaving the page); «نسيت
  كلمة المرور؟» goes to the full page (it needs the e-mail, often in another tab — the held intent already survives a
  reset).
- **C. Everything** in the overlay, forgot / reset included.
- **Recommended: B.** A guest pressing the heart is most often someone **without** an account; sending exactly them
  away defeats the purpose. Google sits at the top of both and already creates an account in one tap. C is not
  possible honestly: the reset link opens from the e-mail in a new tab.

### I2 — React routing: a URL for the overlay or not
- **A. No URL — the overlay is component state** (as `SignInPrompt` is today). `/login` and `/register` stay full pages
  for direct visits, links and bookmarks. The browser's Back does not close it (as every other dialog in the app).
- **B. Modal routes** (a "background location": `/login` drawn over the previous page when reached from inside the app).
  Shareable dialog URLs, Back closes it; but a second render path for every auth route, a pattern nowhere else in the
  app, and the same route meaning two things.
- **Recommended: A.** No router change, one render path per URL, the risk where the value is.

### I3 — Who opens the overlay
- The heart and the report: **yes** (they open `SignInPrompt` today).
- **The header's «تسجيل الدخول» link:**
  - **A. Stays a full page** (`/login`, landing by role). It is the daily door of reception and owners, and has no
    action to hold.
  - **B. Opens the overlay** too, then navigates by role after it.
  - **Recommended: A.** An overlay that then navigates away is a page in disguise.
- **The routes behind `RequireAuth`** («المفضّلة», «بلاغاتي», «إعدادات حسابي», the dashboard): stay redirects to `/login?next=`
  (they are reached by a link to the page itself, not an action).
- **The desk's «تبديل الموظف»**: stays the full page.

### I4 — The landing after an in-place sign-in
- **The rule:** the user stays on the page; the held action runs; **no landing by role**, whatever the role (an owner
  who pressed a heart asked for the favourite, not the dashboard). `RequireGuest` stays the landing's one owner for
  the pages; architecture §2 states the second case explicitly ("an in-place sign-in lands where it was asked").
- **Focus:** the overlay closes and the focus returns to what opened it (the heart, the report link), not to `main`;
  the action's own toast says what happened («أُضيفت إلى المفضّلة»), the welcome toast stays under the same id.
- **No alternative recommended.**

### I5 — Google inside the overlay
- The popup mode suits a dialog; the dialog and the full page are never on one screen, so the "one button on the page"
  handler holds. Two things are **unproven** and become the executor's first checks (no spike now, by the plan rule):
  the GIS iframe inside Radix's focus trap (keyboard reach, the popup's return) and the script loading when the
  dialog opens. If either fails, the fallback is decided then (the button rendered outside the trap, or Google only on
  the pages) — reported, never silently changed.
- `auth.md`'s rule becomes "only where sign-in and register are shown".

### I6 — The temporary password inside the overlay
- Rare on the site (temporary passwords belong to staff accounts the admin or an owner created), but real.
- **The rule:** after the sign-in, a session with `mustChangePassword` goes, as today, through `PasswordChangeGate` to
  `/change-password?next=<this page>`; **the held action waits** and runs only once the change is done (it would get
  403 `PASSWORD_CHANGE_REQUIRED` before). An executor check: the intent's runner must wait for the change.

### I7 — Design (shape, phone, content)
- **Desktop:** a dialog, wider than today's (`max-w-md` is small for Google + two fields + register), with the reason
  as its title and one line under it (today's copy).
- **Phone — the choice:**
  - **A. A full-screen sheet** sliding up, the close button at the top, the form scrolling under it.
  - **B. A bottom sheet** (`85svh`, today's `Sheet` side `bottom`).
  - **Recommended: A.** Two fields and the phone's keyboard leave a bottom sheet little room and make it jump; a
    full-screen panel is how phone apps ask for a sign-in.
- **The layer:** a new design-system component that is a dialog from `md` and a full-screen sheet below it (one
  component, named in the plan; added to foundation §12), built on the existing Radix primitives.
- **Content order:** the reason (title + line) · «المواصلة باستخدام Google» · «أو» · e-mail · password («إظهار», «نسيت
  كلمة المرور؟») · the primary action in the berry (A18) · «جديد على مساحة؟ إنشاء حساب» switching to register in place
  (and back), register showing the password line of A7 and the privacy link.
- **States drawn before code:** idle, submitting, wrong credentials, rate-limited (with the wait), Google unavailable,
  `GOOGLE_LINK_NOT_ALLOWED`, register's e-mail taken, success (closing + the action's toast) — Arabic first, English,
  light / dark, desktop / phone.
- **Links that leave the page** from inside the overlay: «نسيت كلمة المرور؟» (the reset round trip keeps the intent, as
  today); the privacy policy **opens in a new tab** from the overlay only, so the held action is not dropped.
- **The full `/login` and `/register` pages:** the same form block, as a focused page (round 6's direction 2 without
  the panel's filling, or a focused column) — **settled after the overlay's pictures**, so both share one form.

### I8 — Performance (ADR 0011)
- **The rule:** the overlay's form (react-hook-form, the schemas, the auth hooks, Google) is **not** in any site
  page's load; it loads when the overlay first opens (a lazy chunk), with a short loading state inside the overlay; it
  may be prefetched when the pointer or the focus reaches a heart (optional, the executor's call).
- **Option:** add a `check:build` rule that the auth form never reaches the first download — **recommended**, it is
  cheap and keeps the rule true.

### I9 — Accessibility
- The dialog's title is the reason; focus on open goes to the first control (Google's button or the e-mail — the
  executor's check, whichever the trap reaches reliably); Escape and the close button close it and **let the held
  action go** (as today); closing is blocked while submitting (as `ReportDialog`); errors are announced in the form's
  live region as on the pages; the phone sheet keeps the safe-area insets. axe on every state, both widths.

### I10 — The held action's rules
- The intent stays (memory + `localStorage`, 15 min); the in-place sign-in runs it at once (same tab, no navigation);
  `guestLeaving` is unchanged (no path change happens); the round trip remains for the full pages and the reset.
- An executor check: a sign-in in place with **no** held action (if any future trigger opens the overlay without one)
  does nothing but sign in.

### I11 — Documentation and decisions
- **ADR 0021** "Sign in where the action is" (short, decision-level): the overlay for an action that needs an account,
  the pages for direct visits, no modal routes, the landing rule of I4.
- Updated: `docs/frontend/architecture.md` §2 (the landing's two cases, the intent's run), `docs/features/auth.md`
  (Google's place, the overlay), `favorites.md` and `data-reports.md` (a guest's press), foundation §12 (the new
  component), and the copy catalogue (both languages).
- Not touched: the API contract, the backend docs, the schema.

### I12 — Tests
- Component lane: the overlay from the heart (sign in → saved → focus back), from the report (sign in → the report
  dialog reopens), register in place, Google in place (`fakeGoogle`), wrong credentials, 429, the temporary password
  (the action waits), Escape lets the action go; the phone variant of the layer component.
- Unit lane: the intent's runner (waits for the password change).
- The existing page tests stay green unchanged (the pages keep their behaviour). E2E stays at the end of the project.

### I13 — Delivery
- **Order:** the overlay's pictures (I7) with the owner, short loops → the Work Item's plan → the owner's approval →
  execution → a Claude review (it touches auth) → merge on the owner's word.
- **One Work Item, one PR** (the layer component and its first use together), expected around 15–25 files.
- **Executor:** a Claude Code worker, Opus high (auth, focus, Google — not a free model's task).
- **Not in this task:** the redesign of the full `/login` / `/register` pages beyond sharing the form block, the
  dashboard's sign-in paths, GOOGLE_VERIFY.

## 3. What would make us regret it — and how each is closed

| Risk | Closed by |
|---|---|
| Google's button misbehaves inside the dialog | I5: the executor's first check; a stated fallback, reported |
| A second landing owner creeps in | I4: one stated rule, the pages unchanged |
| Every site page grows heavier | I8: a lazy chunk + a `check:build` rule |
| The phone keyboard breaks the sheet | I7: a full-screen panel on phones |
| A temporary password runs the action into a 403 | I6: the action waits for the change |
| The held action is lost by a link inside the overlay | I7: privacy in a new tab; forgot keeps today's reset path |
| A URL pattern for one feature | I2: no modal routes |

## 4. Asked after the approval (2026-11-24)

### I14 — The forgotten password: is a page right?
**Today's flow** (`docs/features/auth.md` §40, ADR 0017): three steps. (1) **Ask for a link** with the e-mail — the
server opens a recovery held by an `HttpOnly` cookie and answers the step («أرسلنا رابطًا إلى b•••@gmail.com», a resend
countdown, «استخدم بريدًا آخر»); (2) **open the link** from the e-mail — `/reset-password`, the token read from the
fragment and checked once; (3) **set the password** — the recovery ends; the reset card then offers sign-in, carrying
`next`; that sign-in runs the held action (`masaha.recoveredAt`, 10 min). `next` travels through the e-mail's link.

**The correction.** I1 sent step 1 to a page. That was wrong: step 1 has no reason to leave — the recovery's place is
held by the server, not the page (ADR 0017), and `ForgotPasswordCard` is already a self-contained card. Only step 2
must be a page, because it is an address opened from an e-mail, often in another tab or on another device.

**The options:**
- **A. Step 1 in place, step 2 a page** — «نسيت كلمة المرور؟» switches the overlay to the request view (the e-mail
  carried from the sign-in field), then to «أرسلنا رابطًا…» with the resend, «استخدم بريدًا آخر» and «العودة إلى
  تسجيل الدخول»; nothing leaves the page, the held action stays. The link opens `/reset-password` (a focused page);
  after the password is set, its sign-in lands on `next` — the space page — and the held action runs there.
- **B. All of it as pages** (I1 as first written): the guest leaves at step 1. Rejected now: it sends away exactly
  the person who is already stuck.
- **C. All of it in place:** impossible — step 2 is a link in an e-mail.

**Refinements to A (each a decision):**
- **A1 — the waiting tab learns of the reset.** When the reset completes in another tab of the same browser
  (`masaha.recoveredAt` is written to `localStorage`, which fires a `storage` event in the waiting tab), the overlay
  still open on «أرسلنا رابطًا…» turns into the sign-in view with the e-mail filled and a line «تم تغيير كلمة المرور.
  سجّل الدخول بكلمة المرور الجديدة». Cheap, no API change. **Recommended.**
- **A2 — sign in automatically after the reset** (the reset answers a session). **Not recommended:** OWASP's
  forgot-password guidance is to let the user sign in through the usual mechanism, not log them in automatically; it
  is also a change to the API, the security rules and ADR 0017. The reset page's sign-in with `next` costs one form.
- **A3 — another device** (asked on the laptop, opened on the phone): the phone's reset page signs in there and lands
  on `next`; the laptop's overlay still says «أرسلنا رابطًا…» and offers «العودة إلى تسجيل الدخول»; a sign-in there
  runs the held action (the same tab). Nothing to build; stated so nobody builds it.
- **The full `/forgot-password` page stays** for the path from the `/login` page; it renders the same card.

**Recommended: A with A1, without A2.** I1 becomes: sign-in, register **and the request for a reset link** in place;
only the reset link's page is a page.

### I15 — The phone's full-screen panel: what "a very good experience" means here
- **Back closes it.** On a phone a full-screen panel looks like a page, and Android's Back (and the iOS edge swipe)
  is the first thing people try. Today Back would leave the space page and drop the held action. **Recommended:**
  opening the overlay adds one history entry **with the same address** (no new URL — I2 stands), Back closes it, and
  closing it by its button removes that entry. One behaviour on every width. An executor check: the data router keeps
  the page mounted, and a reload while it is open shows the page with the overlay closed.
- **The top bar:** the close button («إغلاق», 44 px, at the top's inline start of the reading direction as the phone's
  conventions place it — settled in the pictures), the reason as the title under it; the bar stays while the form
  scrolls.
- **No keyboard on open** on a phone: the focus goes to the title (the panel is announced), so the reason and Google
  are seen before the keyboard covers half the screen; on desktop the focus may go to the first field (I9).
- **The fields:** `inputmode="email"`, the existing `autoComplete` (`email`, `current-password`, `new-password`) so the
  phone's password manager fills them; «التالي» moves from the e-mail to the password and «تم» submits.
- **The keyboard open:** the focused field and the primary button stay visible (the panel scrolls them into view; no
  button pinned above the keyboard — iOS moves pinned elements unreliably).
- **Motion:** it slides up in `--duration-medium`; reduced motion shows it at once.
- **Safe areas:** the top bar under the notch, the form's end above the home indicator.
- **Success:** the panel closes, the page underneath shows the result (the heart filled, or the report dialog open),
  the toast says it.
- **The switch to register or the forgotten password** happens inside the same panel, with «رجوع» in the top bar to
  the sign-in view (not the browser's Back, which closes the panel).
