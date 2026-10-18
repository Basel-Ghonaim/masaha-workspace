# R2-AU-UX — Round 2 review: Signing in and the account · Experience and flow

## 1. Revisions

- `git rev-parse HEAD`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- `git rev-parse origin/main` (after `git fetch origin`): `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- Verdict: HEAD equals `origin/main`; review ran on the merged tip. (The stray `<<<<<<< HEAD` line before
  INDEX §54 was left alone per the prompt note.)

## 2. Verdict

The account flows are short and consistent except for one break: password recovery drops the sign-in
intent, and three recovery/forced-change steps leave the user with a dead end, a retype, or a vague landing.

## 3. The five most important points

1. Recovering a password loses the action that led to sign-in (saved favourite / open report dialog).
2. Sign in is the only auth card with no connection-failure feedback, on a phone-first, weak-network product.
3. The reset link's 429 state (`checkfailed`) tells the user to go back to their email instead of retrying in place.
4. An expired reset link sends the user to an empty Forgot form although the product holds the address.
5. The forced password change lands per role and toasts generically, saying nothing about other devices.

## 4. Issues

### R2-AU-UX-001 — Recovery drops the sign-in intent

- **type:** defect · **level:** pattern · **impact:** high
- **where:** frame "Sign in · from a space, the way back to it — phone 390" (INDEX §54),
  `http://127.0.0.1:5401/Sign%20in.html?next=Space%20details.html%3Fid%3Dfocus%26auth%3D1%26fav%3D1`,
  390, Arabic light. Board screenshot: none yet (§54).
- **evidence:**
  `C:\Users\basel\Downloads\r2-shots\AU-UX\R2-AU-UX-001.png`
  (card entered with `next`, way back "العودة إلى فوكس هاب" present).
- **What is wrong:** `Sign in.html` carries `next` into `Forgot password.html` (`withNext`, `Sign in.html:75`),
  but `ForgotScreen` never reads `next`, the `linkopen` step links to plain `Reset password.html`
  (`Forgot password.html:92-97`), and reset success links to plain `Sign in.html`
  (`Reset password.html:96`). A guest who tapped heart/report, then "forgot password", returns after
  recovery to Home, not to the space; the favourite is never saved and the report dialog never reopens.
- **proposal:** Carry `next` through the recovery chain: keep it on the Forgot page, append it to the
  `linkopen` → Reset link, and to the reset-success → Sign in link, so `finishAuth`/`nextUrl`
  (`masaha/auth.jsx:3-5`) lands where the direct sign-in lands. Changes `Forgot password.html` and
  `Reset password.html` only.
- **why:** The user finishes the task that made them sign in instead of redoing it from Home; one fewer
  navigation on a phone.
- **cost:** M
- **rule:** DECISIONS_ACCOUNT C4 (intent kept on return); REVIEW_LENS §3 B.3.

### R2-AU-UX-002 — Sign in has no connection-failure feedback

- **type:** defect · **level:** page · **impact:** high
- **where:** frame "Sign in · wrong password — phone 390" (INDEX §06),
  `http://127.0.0.1:5401/Sign%20in.html?state=error`, 390, Arabic light. Board screenshot:
  `docs/design/screens/06-sign-in/06-sign-in-wrong-password-phone-390.webp`.
- **evidence:**
  `C:\Users\basel\Downloads\r2-shots\AU-UX\R2-AU-UX-002.png`
  (the only failure the card designs: wrong credentials).
- **What is wrong:** Register designs `?state=network` (`NetworkAlert` with retry, `Register.html:89`);
  Forgot and Reset design `unreachable` with retry. Sign in designs only `error` (credentials) and
  `ratelimit`. On a weak connection the most-tapped card has no "no connection / try again" path, so a
  failed submit reads as wrong credentials or a hang.
- **proposal:** Mirror Register's `NetworkAlert` + in-place retry on the Sign in card, reusing the same
  components; no new copy shape.
- **why:** The user knows a failure is the network, not their password, and retries with one tap.
- **cost:** S
- **rule:** P8 (every action says it failed, with retry); REVIEW_LENS §3 B.6.

### R2-AU-UX-003 — The unchecked reset link (`checkfailed`) is a dead end

- **type:** defect · **level:** page · **impact:** medium
- **where:** frame "Reset · the link could not be checked — phone 390" (INDEX §54),
  `http://127.0.0.1:5401/Reset%20password.html?state=checkfailed`, 390, Arabic light. Board
  screenshot: none yet (§54).
- **evidence:**
  `C:\Users\basel\Downloads\r2-shots\AU-UX\R2-AU-UX-003.png`
  (429 warning + "open the link from your email again", no retry control).
- **What is wrong:** The state's only instruction is "افتح الرابط من بريدك الإلكتروني مرة أخرى"
  (`Reset password.html:69-79`): no in-place re-check, although the 429 countdown shown above it will
  clear. The neighbouring `unreachable` state on the same card offers "إعادة المحاولة". The user must
  leave the app, reopen email, and tap again for what is usually a transient refusal.
- **proposal:** Add an outline "إعادة المحاولة" that re-runs the link check (same `retry` shape as
  `unreachable`), keeping the open-from-email line as the secondary path.
- **why:** One tap recovers a transient 429 instead of an app → email → app round trip.
- **cost:** S
- **rule:** P8; REVIEW_LENS §3 B.3/B.6.

### R2-AU-UX-004 — An expired reset link makes the user retype a known address

- **type:** defect · **level:** page · **impact:** medium
- **where:** frame "Reset · link expired or used — phone 390" (INDEX §08),
  `http://127.0.0.1:5401/Reset%20password.html?state=invalid`, 390, Arabic light. Board screenshot:
  `docs/design/screens/08-forgot-reset-password/10-reset-link-expired-or-used-phone-390.webp`.
 
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-UX\R2-AU-UX-004.png`
  (single "اطلب رابطًا جديدًا" button).
- **What is wrong:** The button links to plain `Forgot password.html` (`Reset password.html:86`) while the
  reset form already shows the server-held masked address and Forgot prefills from `?email=`
  (`Forgot password.html:30`). The user retypes an address the product holds.
- **proposal:** Append `?email=` to the "request a new link" href so Forgot opens prefilled (masked display
  unchanged).
- **why:** Nothing asked twice; the recovery continues with one tap.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.3.

### R2-AU-UX-005 — The forced change stays silent about other devices

- **type:** defect · **level:** page · **impact:** medium
- **where:** frame "Forced change · typing — phone 390" (INDEX §18),
  `http://127.0.0.1:5401/Change%20password.html?auth=1&state=typing`, 390, Arabic light. Board
  screenshot: `docs/design/screens/18-forced-password-change/04-forced-change-typing-phone-390.webp`.
 
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-UX\R2-AU-UX-005.png`.
- **What is wrong:** Saving hands off a plain "حُفظت كلمة المرور الجديدة" toast
  (`Change password.html:40`). The Settings change — the same session event — says under the form and in
  its toast that other devices were signed out (`Settings.html:128,184`). The user is not told the temporary password stopped working elsewhere.
- **proposal:** Use the Settings completion copy for the forced-change handoff toast
  ("تم تغيير كلمة المرور، وسُجّل خروجك من الأجهزة الأخرى").
- **why:** Session changes say what they did elsewhere, so the user trusts the new password everywhere.
- **cost:** S
- **rule:** DECISIONS_ACCOUNT C5.

### R2-AU-UX-006 — `spent` clears a correctly typed address

- **type:** improvement · **level:** page · **impact:** medium
- **where:** frame "Forgot · resends spent — phone 390" (INDEX §54),
  `http://127.0.0.1:5401/Forgot%20password.html?state=spent`, 390, Arabic light. Board screenshot:
  none yet (§54).
- **evidence:**
  `C:\Users\basel\Downloads\r2-shots\AU-UX\R2-AU-UX-006.png`
  ("أدخل بريدك الإلكتروني من جديد" as the only action).
- **What is wrong:** The step resets the email to empty (`setStep('request'); setEmail('')`,
  `Forgot password.html:89`). The resend limit does not require forgetting the address — the server holds
  it and the `sent` step displays it masked. A user with a correct address retypes it every cycle, and a
  typo'd address must be retyped rather than edited.
- **proposal:** Keep the address filled with a "request another link" submit, and keep "استخدم بريدًا آخر"
  for the typo case (the `sent` step's existing shape).
- **why:** Fewer steps per cycle and typo correction becomes editing, not retyping.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.3.

### R2-AU-UX-007 — Switching report tabs keeps the old page

- **type:** defect · **level:** page · **impact:** low
- **where:** frame "My reports · two pages, a space that left — desktop 1440" (INDEX §54; captured at 390),
  `http://127.0.0.1:5401/Reports.html?auth=1&demo=pages`, 390, Arabic light; also INDEX §16
  "Reports · list — phone 390" (`docs/design/screens/16-my-reports/02-reports-list-phone-390.webp`).
 
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-UX\R2-AU-UX-007.png` (tabs + paged list).
- **What is wrong:** `usePaged` resets to page 1 only when the current page exceeds the last
  (`masaha/shared.jsx:639`); `ReportsScreen` keeps `page` across `tab` changes (`Reports.html:87-89`).
  Moving from page 2 of All to a filtered tab with ≥2 pages stays on page 2, hiding the newest reports
  although the list promises "الأحدث أولًا".
- **proposal:** Reset to page 1 on tab change in `ReportsScreen` (set page in `onValueChange`; no change to
  the shared hook, so no other list is touched).
- **why:** The newest reports — the user's goal — are always on the first screen after filtering.
- **cost:** S
- **rule:** P6 (paging); REVIEW_LENS §3 B.3.

### R2-AU-UX-008 — "Save and continue" does not say where it continues

- **type:** improvement · **level:** page · **impact:** low
- **where:** frame "Forced change · reception, a neutral author — phone 390" (INDEX §54; captured at 1440),
  `http://127.0.0.1:5401/Change%20password.html?auth=1&role=reception`, 1440, Arabic light; desktop
  reference INDEX §18 "Forced change · empty — desktop 1440"
  (`docs/design/screens/18-forced-password-change/01-forced-change-empty-desktop-1440.webp`).
 
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-UX\R2-AU-UX-008.png`.
- **What is wrong:** The button is identical for four different landings (owner overview, desk, admin
  overview, Home; `ROLE_HOME`, `Change password.html:27-28`). A first-time reception user cannot tell
  "continue" means the front desk; an owner cannot tell it means the overview.
- **proposal:** Name the destination per role under the button or in it ("حفظ والمتابعة إلى مكتب
  الاستقبال" etc.), reusing the existing role landing; no new step.
- **why:** The user taps forward knowing what comes next, on a one-time screen with no learned habit.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.3.

### R2-AU-UX-009 — `linkopen` gives the escape the same weight as the way forward

- **type:** improvement · **level:** page · **impact:** low
- **where:** frame "Forgot · a reset link already open — phone 390" (INDEX §54),
  `http://127.0.0.1:5401/Forgot%20password.html?state=linkopen`, 390, Arabic light. Board screenshot:
  none yet (§54).
- **evidence:**
  `C:\Users\basel\Downloads\r2-shots\AU-UX\R2-AU-UX-009.png`
  (two equal full-width buttons).
- **What is wrong:** "تعيين كلمة مرور جديدة" and "أدخل بريدك الإلكتروني من جديد" are identical
  full-width targets (`Forgot password.html:92-97`). A mis-tap on the second discards the open link and
  restarts the flow from an empty form, while the `sent` step demotes the same escape to a link button.
- **proposal:** Keep the primary full-width; demote the restart to the `sent` step's link-style
  "استخدم بريدًا آخر" shape.
- **why:** The forward path stays the easy tap; the costly restart stops competing with it.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.2/B.3.

## 5. Decisions in doubt

None. C4/C5 hold; the issues above are gaps in applying them (recovery branch, forced-change toast), not
reasons to change them.

## 6. What was not reviewed and why

- Visual polish, hierarchy/tokens (VD), overflows/mirroring (DF), element removals (EX), wording quality
  (CP), focus/naming/touch targets (AX), API/data-model/role permissions (TR): owned by the other AU
  prompts per the axis split.
- `Sign in - board.html`: a design-doc canvas, not a user flow.
- Widths/modes: issues were captured at phone 390, Arabic light (the account's primary width); 1440 is
  captured in R2-AU-UX-008; 768 (`Settings.html?auth=1`), dark (`Sign in.html?theme=dark`) and EN
  (`Register.html?state=filled&lang=en`) default frames were spot-checked with no flow divergence — the
  auth/account flow logic has no width, theme, or language branches (only layout classes and `tr()` copy),
  verified in `masaha/auth.jsx`, `masaha/account.jsx`, and the page scripts. Headless 390 captures show an
  RTL viewport-offset artifact (right-anchored content, left edge cut); regions cited above are legible and
  each claim was cross-checked against source.
- API-contract pagination/429 expectations (lens §2c) beyond what the prototype states: TR-owned.
- Server stopped after the run (PID 30344) and port 5401 verified free.
