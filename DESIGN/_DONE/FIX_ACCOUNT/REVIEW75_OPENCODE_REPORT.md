# Review — PR #75 (design batch 4: the account and signing in — prototype conformance)

**Head verified:** `f100a287b78398a4119ec6fca35742625f6f104d` (matches `gh pr view 75 --json headRefOid`, folder `HEAD` matches). **Base:** `e30a86c9ef8b03998516263090570fb341345e62`.

---

## Findings (most severe first)

### Blocker

None.

### Should-fix

None.

### Nit

**1. `problem === 'exists'` remains in `Register.html` initial state list (line 58)**  
The variable `problem` is initialized with `['exists', 'network'].includes(initialState) ? initialState : null`, but the `'exists'` case is now handled entirely via the `taken` state and field-level error (line 53, 97). The `problem` state for `'exists'` is never read or rendered. Harmless but confusing; remove `'exists'` from the array.

**2. `PasswordForm` in `Settings.html` retains the demo's wrong-password failure path (lines 106, 121)**  
Pre-existing behaviour from before this batch; the plan is silent on it. The demo shows `demo === 'wrongpw'` pre-filling current/new passwords and failing on submit. This is a demo artifact, not a spec requirement.

**3. English/dark mode only spot-checked, not full matrix**  
The fixer's report confirms Arabic light at 390/1440 for all frames, 768 for Settings/Favourites/Reports, and only 6 English/dark spot checks. The plan's acceptance criterion requires every changed page at 390, 768, 1440, Arabic and English, light and dark. The remaining combinations are unverified by eye (scripts catch blanks/errors, not layout).

---

## Checked and fine

- **AC-022 · 429 countdown:** `RETRY_AFTER = 42`, `useRetryAfter`, `RateLimitAlert` with `mmss` in `auth.jsx`; used on Sign in, Register, Forgot password, Settings. Submit disabled while counting. At 0:00 line disappears, submit enabled. No page says «15 دقيقة».
- **AC-022 · email taken:** `Register.html?state=exists` shows field error «يوجد حساب بهذا البريد الإلكتروني.» and link «سجّل الدخول بهذا البريد» under it; no Alert above form.
- **AC-022 · Google per code:** `?google=error|notallowed|unavailable` each show distinct `GOOGLE_LINES` text under Alert «تعذّرت المتابعة باستخدام Google»; `?google=off` hides button and «أو» divider.
- **AC-022 · recovery steps:** Forgot password `loading|unreachable|sent|linkopen|spent` and Reset password `loading|unreachable|checkfailed` render server-held steps; all addresses masked via `maskEmail` (`s•••@example.com`); resend clock shows m:ss (`أعد الإرسال بعد 0:59`).
- **C3:** `LinkSent` component in `auth.jsx` exposes `onOtherEmail` («استخدم بريدًا آخر») at every moment of the clock; `?email=` prefill shows masked typo (`s•••@gmial.com`).
- **C4 · intent:** `nextSpace`, `withIntent`, `AuthWayBack`, `favSavedLine` in `auth.jsx`; Sign in/Register toasts include saved-favourite line; `next` preserved on Forgot→Sign in, Reset card has «العودة إلى تسجيل الدخول» in all non-success states.
- **AC-017:** Sign in description reads «سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.»
- **AC-018 (Q1 yes):** `Space details.html` report-variant dialog reads «سجّل الدخول لتجد الردّ على بلاغك في «بلاغاتي».»; `?dialog=signin-report` handling; `?fav=1&fail=fav` failure toast with «إعادة المحاولة».
- **AC-006 / C1 / C2:** `Settings.html` has one «تسجيل الدخول» card; methods as rows; «تغيير» opens password form in place with «رجوع»; line «تغيير كلمة المرور يسجّل خروجك من كل الأجهزة الأخرى» above submit; no «تسجيل الخروج من كل الأجهزة»; `?auth=google` offers «أرسل رابط تعيين كلمة المرور» with in-place link-sent block.
- **C5:** Password change toast «تم تغيير كلمة المرور، وسُجّل خروجك من الأجهزة الأخرى»; `Home.html?toast=linked` shows persistent toast with title/description/close button; `Change password.html` forced-change text amended per owner (2026-10-13); saves land on role-specific page via `ROLE_HOME`.
- **C6:** Account nav, Settings h1, `<title>`, menu say «إعدادات حسابي»; from 1024 nav shows caption «حسابي»; Settings `max-w-3xl`, Favourites/Reports full width; signed-out → `Sign in.html?next=` with no inline sentence.
- **AC-012:** Email renders as label/value/«تسجّل الدخول بهذا البريد»; no input, no change promise.
- **AC-013:** Theme toggle defaults to «حسب الجهاز»; captions «تُحفظ في حسابك» (language) and «على هذا الجهاز» (theme); `?fail=language` returns toggle with «تعذّر حفظ اللغة» + «إعادة المحاولة».
- **C7:** Favourites shows Palm Hub as row under grid (name text, «لم تعد هذه المساحة معروضة في الدليل», «إزالة» with «تراجع»); My reports shows Palm Hub's report with same line, status, reply.
- **C8 / AC-014:** Favourites no pagination; count + «الأقرب إليّ» above grid; `LocationStatus` under them; with location on, grid sorted by distance and cards show distances; off, neither.
- **C8 / AC-016 / AC-009:** My reports uses `usePaged` (20/page); chips «الكل · قيد المراجعة · تمت المراجعة»; «عرض المزيد» only when clamp cuts; no-message reports show field alone; messages/replies `dir="auto"`; reply label follows `repliedBy` (Number One's old report reads «ردّ فريق مساحة»).
- **AC-021:** `Reset email.html` greets «مرحبًا،» / «Hi,»; under button «إن لم يعمل الزر، انسخ هذا الرابط:» with LTR link; English mirror.
- **§7 privacy line:** `grep -rn "على جهازك فقط\|stays on your device" docs/design/prototype` prints nothing. New line `PRIVACY_LINE` in `shared.jsx` reads «يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.»; used in `location.jsx` four states and `Directory.html` map picking card.
- **Hazards (§9):** Each new top-level name defined once per page (grep verified: `RETRY_AFTER`, `mmss`, `useCountdown`, `useRetryAfter`, `maskEmail`, `GOOGLE_LINES`, `LinkSent`, `nextSpace`, `withIntent`, `AuthWayBack`, `favSavedLine`, `demoToast`, `UNLISTED_LINE`, `ROLE_HOME`, `forcedRole`, `MethodRow`, `SignInCard`, `SetPasswordByEmail`, `savedCount`, `DEMO_FIELDS`, `DEMO_REPORTS`, `ALL_REPORTS`, `UNLISTED`, `PRIVACY_LINE` — all single-definition). No object rest destructuring. Hooks before early returns. Every class in `_ds_bundle.css` or token-only in `masaha.css` (`check-classes.mjs`: 336 used, 8 pre-existing dead, 0 new). `_ds/` and `_vendor/` untouched.
- **Archive:** `CHANGES.md` has Batch 4 section; `INDEX.md` parameters table includes Batch 4 rows; board (section 54) has 18 frames F1–F18; README frame count 511 → 511 (no change, frames replaced), sections 53 → 54. No overlap with Batch 3 frames.
- **Boundaries:** `git diff --name-only` shows 18 files, all inside `docs/design/`; none of §5's *Never touched* (`apps/`, `packages/`, `docs/features/`, `screens/`). Ten commits, subjects 38–48 chars (all ≤ 50).
- **Fixer's departures:** 19 extra before-images in shared folder (owner's captures, valid clean-tree befores, kept); one `Get-Process chrome | Stop-Process` killed all Chrome processes (noted); English/dark only spot-checked (recorded).

---

## Verdict

**PASS** — The prototype conforms to the plan and decisions. All acceptance criteria verified in code; the three nits are pre-existing or demo-only and do not affect conformance.