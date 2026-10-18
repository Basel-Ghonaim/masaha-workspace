# Design decisions — batch 4, the account and signing in (approved by the owner, 2026-10-11)

> **Amended 2026-10-13** by the owner: **C5's forced-change line** no longer says the temporary
> password was given "when your account was created" — since #62 the admin also issues one to recover
> an account. It reads: «كلمة المرور التي دخلت بها مؤقتة، أُعطيت لك من فريق مساحة أو من صاحب المساحة.
> اختر كلمة مرور خاصة بك للمتابعة.» **The prototype's `shared.jsx` belongs to this batch** while batch
> 5 runs in parallel.

From `REPORT\REVIEW_ACCOUNT_REPORT.md` (AC-001 … AC-022, G1–G4). **Settled**, as the report proposes
unless said otherwise. Where each is done: **prototype**, **web** (worker A — several are in built
code), **API** (worker B), **docs**.

## Decisions
- **C1 — a Google-only account's first password comes through the email** (AC-001): «أرسل رابط
  تعيين كلمة المرور» (`POST /auth/password/forgot` with the session's email), the built "link sent"
  block in place. *(prototype; web with screen 9)*
- **C2 — no "sign out of all devices" in v1** (AC-002): the button goes; under the password form
  «تغيير كلمة المرور يسجّل خروجك من كل الأجهزة الأخرى». *(prototype)*
- **C3 — «استخدم بريدًا آخر» always on the "sent" step**, with the address held by the server shown
  masked (AC-003). *(prototype; **web — built code**)*
- **C4 — getting in keeps the intent** (G1, AC-004, AC-017, AC-018, AC-019): the action that led to
  the sign-in runs on return and is named in the toast; with `next`, the card's way out returns to it;
  every auth card has a way back (the reset form included); the sign-in card speaks to owners and
  reception too; the report's sign-in reason is «لتجد الردّ على بلاغك في «بلاغاتي»». *(prototype;
  web: AC-017, AC-019 in built code; the intent with step 10)*
- **C5 — a session change says what it did elsewhere** (G2, AC-005, AC-007): the password change
  says it signed out the other devices; the Google link's toast stays until closed; the forced change
  reads «كلمة المرور التي دخلت بها مؤقتة، أُعطيت لك عند إنشاء حسابك. اختر كلمة مرور خاصة بك
  للمتابعة.» and lands where the role lands. *(prototype; **web — AC-005 in built code**)*
- **C6 — the account area is one place with one name** (G3, AC-010, AC-011): «إعدادات حسابي» in the
  nav, the h1 and the menu; a «حسابي» label on the nav from `lg`; Settings `max-w-3xl`, the lists full
  width; signed out → `RequireAuth` (no inline sentence). *(prototype)*
- **C7 — a space that left the directory** (G4, AC-008): «لم تعد هذه المساحة معروضة في الدليل», its
  name as text; «إزالة» with undo on Favourites; the report kept on My reports. *(prototype; API:
  `listed: false` on `GET /me/favorites` and `/me/reports`)*
- **C8 — favourites are answered whole** (AC-015), an exception added to api-contract §4; My reports
  pages (P6). *(prototype; docs; API)*
- **Smaller (as proposed):** AC-006 one «تسجيل الدخول» card listing the methods; AC-009 the reply's
  author from the resolver (`repliedBy`); AC-012 the email as text, no change promise; AC-013 the theme
  «حسب الجهاز» by default, where each preference is kept; AC-014 «الأقرب إليّ» on Favourites (U2);
  AC-016 the reports' toggle and filter chips, `dir="auto"`; AC-021 a copyable link in the reset
  email, no name; AC-022 the prototype catches up with the built screens. *(prototype; API: AC-009)*

## Design system
- **AC-020:** `PasswordRules` shows a fourth rule, only when broken, «طويلة جدًا — اختصرها».
  *(design system / shared forms)*

## Rules changed
- **foundation §13, screen 9:** "a Google-only account can add one, through the reset email
  (security.md)". *(docs)*
- **api-contract §4:** favourites answered whole. *(docs, with the API item)*
