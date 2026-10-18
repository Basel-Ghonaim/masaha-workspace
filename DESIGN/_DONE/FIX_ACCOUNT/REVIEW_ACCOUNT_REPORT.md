# Design review 4 — the account and signing in (AC-001 … AC-022)

Reviewer: design-review-account · 2026-10-11 · archive from `origin/main` (b66ddfe), served on
`http://localhost:5343/` · evidence in `C:\Users\basel\Downloads\design-review-account\`.
Scope: screens 5, 6, 7, 9, 10, 11 (board sections 05–09, 13, 15–19). Every page was captured in ar/en ×
light/dark × 390/768/1440 (161 captures), and tab-stepped at 1440. Nothing overflows sideways at
any width, and the tab order follows the reading order on every page.

Built in code: sign-in, register, Google, forgot/reset, the forced change, and the account menus.
**Not built:** Settings, Favourites, My reports.

## 1. Summary

1. **Settings asks a Google-only account for its first password in a form.** security.md forbids
   this (the first password comes only through the reset email) and the API refuses it with
   `PASSWORD_NOT_SET`. It has to become "send me a link" (AC-001).
2. **"Sign out of all devices" has no endpoint.** `POST /auth/logout` ends one device. The owner
   chooses: drop the button in v1, or add an API item (AC-002).
3. **The forgotten password can strand a user who mistyped the email.** In the prototype and in the
   built code, the "link sent" step offers only "resend" to the same address until the resends run
   out (AC-003).
4. **Getting in loses what the person came to do.** The return after sign-in, register or Google
   does not confirm the saved favourite, and the ways out ignore `next` (AC-004, pattern G1).
5. **The words of a session change are not always true.** The forced change tells receptionists
   that the Masaha team made their password. Neither a password change nor a Google link says it
   signed out the other devices or removed the password. A space taken off the directory is called
   «لم تعد متاحة», the live-status word (AC-005, AC-007, AC-008).

## 2. Patterns

### G1 — Getting in keeps your place and your intent *(AC-004, AC-017, AC-018, AC-019)*
- **Now:** sign-in ↔ register carry `next`. "Forgot password", "Browse without an account" and the
  reset's success drop it. The return confirms only the account («أهلًا سارة، تم إنشاء حسابك»),
  not the action that sent the person there (saving Focus Hub). The reset form has no way out.
- **Proposal:** (1) whatever action led to the sign-in (the heart, the report) is done on return
  and named in the toast: «حُفظت Focus Hub في المفضّلة» (heart), or the report dialog reopens.
  (2) When `next` is present, the auth card's secondary way out returns to it («العودة إلى Focus
  Hub»), in place of "Browse spaces without an account". (3) Every auth card has a way back in its
  footer, the reset form included. (4) The cards' descriptions speak to everyone who signs in here,
  owners and reception too.
- **Pages:** Sign in, Register, Forgot, Reset, Space details (the sign-in dialog), the auth flow
  frames (section 05). **Cost:** M.

### G2 — A session change says what it did elsewhere *(AC-005, AC-007, AC-002)*
- These actions reach beyond this device: a password change and a reset sign out every other device;
  a Google link removes the password and signs out the others; the forced change follows a password
  someone else made. Each must say so, in true words, **when** it happens.
- **Proposal:** one line per event, in the toast or card that confirms it:
  - password change — «تم تغيير كلمة المرور، وسُجّل خروجك من الأجهزة الأخرى»;
  - Google link — the built `linkedTitle` / `linkedDescription`, kept until closed (it tells of a
    lost password, so it must not vanish after four seconds);
  - reset — as now;
  - forced change — a neutral author (AC-005).
- **Pages:** Settings, Home (the linked toast), Change password. **Cost:** S.

### G3 — The account area is one place with one name *(AC-010, AC-011, AC-015)*
- **Now:** the page is «الإعدادات» in the nav and the h1. The account menu calls it «إعدادات حسابي»
  (P4), and an owner's dashboard has a second «الإعدادات» (the space's). The nav has no label you can
  see. The three pages use three widths (`max-w-2xl`, `max-w-3xl`, full). A signed-out visitor gets
  a sentence inside the shell. Neither list pages.
- **Proposal:**
  - one name per destination: the nav, the h1 and the menu read «إعدادات حسابي» (AD-029's rule:
    one name in the menu and on the page);
  - from `lg`, the nav carries a caption-level label «حسابي»;
  - AD-029's widths: Settings at `max-w-3xl`, the two lists full width;
  - signed out → the route's `RequireAuth` sends the visitor to sign in with `next` (as built), and
    the inline sentence goes;
  - My reports pages (P6). For Favourites, see AC-015.
- **Pages:** Settings, Favourites, My reports, the account menu. **Cost:** S.

### G4 — A space that has left the directory *(AC-008)*
- Favourites draws a hidden space as a muted card. My reports has no such state: its link would land
  on a 404.
- **Proposal:** one treatment on both pages:
  - the space's name as text, not a link;
  - the line «لم تعد هذه المساحة معروضة في الدليل»;
  - on Favourites, «إزالة» (with undo, P9). On My reports, the report stays, with its status and
    reply.
- **API:** `GET /me/favorites` and `GET /me/reports` return such a space with a `listed: false` flag
  and its name only. **Pages:** Favourites, My reports. **Cost:** S.

## 3. Issues

### AC-001 — A Google-only account sets its first password in a form
- **type:** defect · **level:** page · **impact:** high
- **where:** 17 · *Settings · Google-only account* — `http://localhost:5343/Settings.html?auth=google`
  — `screens/17-settings/04-settings-google-only-account-phone-390.webp`
- **evidence:** `AC-001.png`
- **what is wrong:** «إضافة كلمة مرور» opens a password form, which `POST /me/password` would
  refuse with `PASSWORD_NOT_SET`. security.md says the first password is set "through the reset
  email, which proves the inbox, never here".
- **proposal:**
  - The Google row stays.
  - Under it: «لتسجيل الدخول بالبريد وكلمة مرور أيضًا، نرسل رابطًا إلى بريدك» and an outline
    `Button` «أرسل رابط تعيين كلمة المرور». It calls `POST /auth/password/forgot` with the session's
    email.
  - On success the card shows the forgot page's "sent" block in place (masked address, resend, m:ss
    countdown), reusing the built `LinkSent`.
  - The reset page then sets the password, as it does for any account.
- **why:** it is the only path the API serves, and it tells the user up front that the inbox is the
  proof. **cost:** S
- **rule:** security.md › Passwords; api-contract `POST /me/password`; foundation §13 item 9 (see
  Rules in doubt).

### AC-002 — "Sign out of all devices" has no endpoint
- **type:** defect · **level:** page · **impact:** medium
- **where:** 17 · *Settings · sign out of all devices (confirm)* —
  `…/Settings.html?auth=1&state=signout` —
  `screens/17-settings/12-settings-sign-out-of-all-devices-confirm-phone-390.webp`
- **evidence:** `AC-002.png`
- **what is wrong:** `POST /auth/logout` ends only this device's family, and nothing ends every
  session apart from a password change or reset. The dialog promises what the API cannot do.
- **proposal (the owner's choice):**
  - **(a) recommended for v1:** drop the button. Under the password form, say «تغيير كلمة المرور
    يسجّل خروجك من كل الأجهزة الأخرى». The password change already does exactly this.
  - **(b)** add `POST /auth/logout-all` (API item, worker B). The dialog stays, and P9 applies: it
    is felt by others (it signs out the reception desk the person also uses), so `AlertDialog` with
    a `destructive` action «تسجيل الخروج من كل الأجهزة», and «رجوع».
- **why:** a security control that does nothing is worse than none. **cost:** S (a) / M (b)
- **rule:** api-contract §5 *Session*; security.md › Tokens and cookies (Revocation); P9.

### AC-003 — A mistyped email strands the forgotten-password flow
- **type:** defect · **level:** page · **impact:** high
- **where:** 08 · *Forgot · sent (60s countdown)* — `…/Forgot password.html?state=sent` —
  `screens/08-forgot-reset-password/04-forgot-sent-60s-countdown-phone-390.webp`
- **evidence:** `AC-003.png`
- **what is wrong:** the sent step offers only «أعد الإرسال», which goes to the same address. The
  built `LinkSent` shows «أدخل بريدك الإلكتروني من جديد» only once the three resends are spent. The
  step survives a reload (ADR 0017), so someone who typed `sara@gmial.com` waits through three
  pointless resends. That person is already locked out, usually on a phone.
- **proposal:** always show a `link` button «استخدم بريدًا آخر» under the resend. It returns to the
  email form, which is the built `enterEmailAgain`; a new `forgot` ends the old recovery. Keep
  showing the address the server holds (masked) as «أُرسلت إلى s•••@gmial.com», so the typo is
  visible.
- **why:** the most common recovery mistake gets a one-tap fix, and nothing about accounts is
  revealed (the answer is the same for every address). **cost:** S, prototype and code.
- **rule:** ADR 0017 §4; security.md › Passwords (another link).

### AC-004 — The return from signing in forgets why the person signed in
- **type:** improvement · **level:** pattern (G1) · **impact:** medium
- **where:** 05 · *Back on the space · toast* —
  `…/Space details.html?id=focus&loc=none&auth=1&fav=1&toast=welcome` —
  `screens/05-auth-flow/03-3-back-on-the-space-toast.webp`
- **evidence:** `AC-004.png`
- **what is wrong:** the heart is filled, but the toast talks only about the account. A person who
  signed in from "Report" is not brought back to the report.
- **proposal:**
  - The pending action rides with `next` (`intent=favorite|report`). On return it runs once: the
    favourite is saved, or the report dialog opens.
  - One toast names both: «أهلًا سارة — حُفظت Focus Hub في المفضّلة».
  - If the save fails, the P8 failure toast with «إعادة المحاولة».
- **why:** the user finishes what they started, with no second tap. **cost:** M (web, with step 10)

### AC-005 — The forced change says the Masaha team made every temporary password
- **type:** defect · **level:** page · **impact:** medium
- **where:** 18 · *Forced change · empty* — `…/Change password.html?auth=1` —
  `screens/18-forced-password-change/02-forced-change-empty-phone-390.webp`
- **evidence:** `AC-005.png`
- **what is wrong:** «هذه كلمة مرور مؤقتة من فريق مساحة». The same words are in code
  (`users.passwordChange.description`). A reception account's temporary password comes from its
  **owner** (security.md › Passwords), so a receptionist reads something false. The session cannot
  tell who made it.
- **proposal:** «كلمة المرور التي دخلت بها مؤقتة، أُعطيت لك عند إنشاء حسابك. اختر كلمة مرور خاصة
  بك للمتابعة.» Also, after saving, land where the built `RequirePasswordChange` lands (the
  dashboard for an owner), not Home (prototype).
- **why:** true for all three cases (admin-created owner, owner-created receptionist, admin
  recovery). **cost:** S
- **rule:** security.md › Passwords.

### AC-006 — The Security card: two headings and a wall of empty password fields
- **type:** improvement · **level:** page · **impact:** medium
- **where:** 17 · *Settings · email account* — `…/Settings.html?auth=1` —
  `screens/17-settings/01-settings-email-account-desktop-1440.webp`
- **evidence:** `AC-006.png`
- **what is wrong:**
  - The card title «الأمان» and the inner h3 «تغيير كلمة المرور» have the same style, so there is
    no hierarchy (lens A3).
  - Two empty password fields and the rules are always open, on a page people mostly visit for
    their name or language.
- **proposal:**
  - One card «تسجيل الدخول», listing the sign-in methods as rows, each a label, a status and one
    action:
    - «Google» — `Badge` «مربوط»;
    - «كلمة المرور» — «تغيير», which opens the form in place (current, new, rules, «حفظ كلمة
      المرور», «رجوع»); for a Google-only account the row offers AC-001's link.
  - The G2 sentence sits under the form.
- **why:** progressive disclosure (lens B5); the card reads as "how I sign in" at a glance.
  **cost:** S

### AC-007 — Password change and Google link do not say they signed out other devices
- **type:** defect · **level:** pattern (G2) · **impact:** medium
- **where:** 06 · *After Google · accounts linked (toast)* — `…/Home.html?loc=none&toast=linked` —
  `screens/06-sign-in/10-after-google-accounts-linked-toast-phone-390.webp`; and 17 · Settings
  (password changed toast)
- **evidence:** `AC-007.png`
- **what is wrong:**
  - The prototype's «ربطنا حساب Google بحسابك» hides that the password was removed and the other
    sessions ended.
  - «تم تغيير كلمة المرور» hides that every other device was signed out (security.md).
  - Built code already says the first in `linkedDescription`. The second is not built yet.
- **proposal:** G2's lines. The linked toast stays until dismissed (Sonner `duration: Infinity`).
- **why:** a person who later finds their tablet signed out, or their password gone, knows why.
  **cost:** S
- **rule:** security.md › Sign-in methods; › Passwords.

### AC-008 — «لم تعد متاحة» for a space that left the directory
- **type:** defect · **level:** pattern (G4) · **impact:** medium
- **where:** 15 · *Favourites · saved spaces + one hidden* — `…/Favorites.html?auth=1&loc=none` —
  `screens/15-favourites/01-favourites-saved-spaces-one-hidden-desktop-1440.webp`
- **evidence:** `AC-008.png`
- **what is wrong:**
  - «متاح» is the live status «متاح الآن», so «هذه المساحة لم تعد متاحة» reads as "full now".
  - The muted card stretches to its neighbour's height, a large empty box.
  - My reports has no such state.
- **proposal:** G4: «لم تعد هذه المساحة معروضة في الدليل». The card sizes to its content
  (`items-start` on the grid, or a one-line row under the grid). **cost:** S
- **rule:** glossary (live status words); ADR 0008.

### AC-009 — The reply's author is guessed from today's verification
- **type:** defect · **level:** page · **impact:** medium
- **where:** 16 / 19 · *My reports · replies* — `…/Reports.html?auth=1` —
  `screens/16-my-reports/02-reports-list-phone-390.webp`
- **evidence:** `AC-009.png`
- **what is wrong:** the label «ردّ إدارة المساحة» / «ردّ فريق مساحة» comes from `s.verified` now.
  A report the admin answered before an owner joined would be shown as the space's reply. The data
  model stores the resolver (`DataReport.resolvedById`).
- **proposal:** `GET /me/reports` returns `repliedBy: "space" | "masaha"`, derived on the server from
  the resolver (an admin is «فريق مساحة», anyone linked to the space «إدارة المساحة»), and the card
  shows that.
- **why:** the person knows who really answered. **cost:** S (API field + web)
- **rule:** foundation §13 item 11; data-model › DataReport.

### AC-010 — One name for the account settings page; label the nav
- **type:** improvement · **level:** pattern (G3) · **impact:** low
- **where:** 17 · Settings · 1440 — `…/Settings.html?auth=1` —
  `screens/17-settings/01-settings-email-account-desktop-1440.webp`
- **evidence:** `AC-010.png`
- **what is wrong:** «الإعدادات» (nav, h1) vs «إعدادات حسابي» (menu, P4). For an owner it is also the
  dashboard's «الإعدادات». The start-side nav has no label.
- **proposal:** G3. **cost:** S

### AC-011 — A signed-out visitor gets a sentence inside the shell
- **type:** improvement · **level:** pattern (G3) · **impact:** low
- **where:** not a frame — `…/Favorites.html` (no `auth`)
- **evidence:** `AC-011.png`
- **what is wrong:** the account shell, its nav and an h1 render around «سجّل الدخول لعرض هذه
  الصفحة». Built code already has `RequireAuth`, which redirects to sign-in with a return URL.
- **proposal:** the design follows the code: `/me/*` routes redirect, and the inline state goes.
  **cost:** S

### AC-012 — The email shown as a disabled input, with an untrue promise
- **type:** defect · **level:** page · **impact:** low
- **where:** 17 · Settings · 390 — `…/Settings.html?auth=1` —
  `screens/17-settings/02-settings-email-account-phone-390.webp`
- **evidence:** `AC-012.png`
- **what is wrong:**
  - A read-only `Input` on `bg-muted` looks like a disabled field.
  - Its helper «لتغيير البريد تواصل معنا» links to `About.html#owners`, the owners' section.
  - No endpoint, admin action included, changes an email.
- **proposal:**
  - Show the email as text: a `label` plus the value `dir="ltr"`, with the caption «تسجّل الدخول بهذا
    البريد».
  - Drop the change promise. If the owner wants a manual path, link to `#contact` (U11) and add it
    to the admin's backlog.
- **why:** it doesn't invite an edit that can't happen, and it doesn't promise a service no one
  delivers. **cost:** S
- **rule:** foundation §13 item 9 (name, password, language, theme: no email).

### AC-013 — Preferences: the theme defaults to «فاتح», and neither choice says where it is kept
- **type:** defect · **level:** page · **impact:** low
- **where:** 17 · Settings — `…/Settings.html?auth=1`
- **evidence:** `AC-013.png`
- **what is wrong:**
  - Foundation §6 follows the system until the user chooses, but the toggle starts on «فاتح».
  - The language is saved to the account (`PATCH /me`); the theme lives on this device only. The
    card says only «تُطبَّق فورًا».
  - A failed language save has no state.
- **proposal:**
  - Preselect «حسب الجهاز» when no choice is stored.
  - Captions: language «تُحفظ في حسابك», theme «على هذا الجهاز».
  - A failed language save returns the toggle and raises the P8 failure toast. Per P8's exception,
    the change shows in place, so there is no success toast.
- **cost:** S · **rule:** foundation §6.

### AC-014 — Favourites shows distances with no sign that the location is in use
- **type:** improvement · **level:** page · **impact:** low
- **where:** 15 · *Favourites · location on* — `…/Favorites.html?auth=1&loc=granted` —
  `screens/15-favourites/04-favourites-location-on-phone-390.webp`
- **evidence:** `AC-014.png`
- **what is wrong:** «على بعد 0.7 كم تقريبًا» appears on each card, but there is no control, no
  `LocationStatus` line, no privacy line, and no distance order.
- **proposal:** apply U2 here: the «الأقرب إليّ» `Button` by the count, which sorts by distance when
  on, with its one state line. With it off, no distances.
- **why:** "which of my places is nearest and open" is the favourites question; it should be asked
  the same way as on the Directory. **cost:** S

### AC-015 — The account lists do not page
- **type:** defect · **level:** pattern (G3) · **impact:** low
- **where:** 16 · Reports · 1440 — `…/Reports.html?auth=1`; 15 · Favourites
- **evidence:** `AC-015.png`
- **what is wrong:** api-contract §4 pages every list. Neither page has `Pagination` or an order.
- **proposal:**
  - My reports: P6 (20 per page, newest first).
  - Favourites: newest saved first. Either P6, or an exception in §4 answered whole: a person
    saves a handful, and a grid that pages is awkward. The second needs the owner's yes and a §4
    line.
- **cost:** S · **rule:** api-contract §4.

### AC-016 — My reports: «عرض المزيد» with nothing hidden, «مغلقة» named nowhere else
- **type:** defect · **level:** page · **impact:** low
- **where:** 16 · *Reports · list* — `…/Reports.html?auth=1` —
  `screens/16-my-reports/01-reports-list-desktop-1440.webp`
- **evidence:** `AC-016.png`
- **what is wrong:**
  - At 1440, Golden Hub's message fits in two lines, yet «عرض المزيد» shows (a 90-character test,
    not an overflow test).
  - The filter's «مغلقة» names no badge («تم التصحيح», «لم يُعتمد»).
  - A report's message is optional (required only for «أخرى»), but the card has no form without
    one.
  - The user's text is not `dir="auto"` (§8).
- **proposal:**
  - Show the toggle only when the clamp cuts text.
  - Chips «الكل · قيد المراجعة · تمت المراجعة» (P5's ≤ 4 rule).
  - Without a message, the field group alone.
  - `dir="auto"` on the message.
- **cost:** S

### AC-017 — The sign-in card speaks only to visitors
- **type:** improvement · **level:** pattern (G1) · **impact:** low
- **where:** 06 · *Sign in · default* — `…/Sign in.html` —
  `screens/06-sign-in/02-sign-in-default-phone-390.webp`
- **evidence:** `AC-017.png`
- **what is wrong:** «سجّل الدخول لمتابعة مساحاتك المفضّلة والبلاغات…» (also in code). Owners,
  receptionists and the admin sign in here every day.
- **proposal:** «سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.» **cost:** S

### AC-018 — The sign-in dialog for reporting gives an untrue reason
- **type:** defect · **level:** page · **impact:** low
- **where:** 05 · *Heart → sign-in dialog* (its report variant) —
  `…/Space details.html?id=focus&loc=none` → «الإبلاغ عن معلومة غير صحيحة» —
  `screens/04-space-details-variants/14-signed-out-heart-sign-in-dialog-phone-390.webp`
- **evidence:** `AC-018.png`
- **what is wrong:** «نطلب تسجيل الدخول لنتابع البلاغ معك إن احتجنا توضيحًا». Masaha sends no
  messages (Not in v1); the real reason is that the reply appears in «بلاغاتي» (U10).
- **proposal:** «سجّل الدخول لتجد الردّ على بلاغك في «بلاغاتي».» **cost:** S
- **rule:** overview › Not in v1; U10.

### AC-019 — The reset form is a dead end
- **type:** improvement · **level:** pattern (G1) · **impact:** low
- **where:** 08 · *Reset · new password* — `…/Reset password.html?state=typing` —
  `screens/08-forgot-reset-password/08-reset-new-password-phone-390.webp`
- **evidence:** `AC-019.png`
- **what is wrong:** apart from the wordmark there is no way out. The person who opened the link on
  the wrong account, or changed their mind, has nowhere to go. The same holds in code.
- **proposal:** the card footer of the forgot page: «العودة إلى تسجيل الدخول». **cost:** S

### AC-020 — A password over 72 bytes ticks every rule
- **type:** defect · **level:** component (`PasswordRules`, `@shared/forms`) · **impact:** low
- **where:** 07 · Register — `…/Register.html` (44 Arabic letters typed)
- **evidence:** `AC-020.png`
- **what is wrong:** the policy caps a password at 72 bytes (36 Arabic letters). The rules list
  shows three ticks while the server will refuse it, and the error points to "the rules below",
  which are all met.
- **proposal:** a fourth rule shown only when broken, in `destructive`: «طويلة جدًا — اختصرها».
  No byte count shown. **cost:** S
- **rule:** security.md › Passwords (policy).

### AC-021 — The reset email: a copyable link (the built greeting is already right)
- **type:** improvement · **level:** page · **impact:** low
- **where:** 09 · *Reset email — phone 390* — `…/Reset email.html` —
  `screens/09-reset-email/02-reset-email-phone-390.webp`
- **evidence:** `AC-021.png`
- **what is wrong:**
  - The design greets «مرحبًا سارة»; security.md forbids greeting by name. Built code already says
    «مرحبًا،», so the design catches up.
  - Only a button carries the link, which fails in clients that strip styled links.
- **proposal:** one caption line under the button: «إن لم يعمل الزر، انسخ هذا الرابط:» and the URL
  `dir="ltr"`. The design drops the name. **cost:** S
- **rule:** security.md › Passwords (the email).

### AC-022 — Already better in code: the design catches up
- **type:** improvement · **level:** page · **impact:** low
- **where:** 06–08 · sign-in, register, forgot, reset — e.g. `…/Register.html?state=exists` —
  `screens/07-register/08-register-email-already-registered-phone-390.webp`
- **evidence:** `AC-022.png`
- **what is better in code:**
  - an `EMAIL_TAKEN` answer on the email field, with «سجّل الدخول بهذا البريد» under it, not a top
    Alert;
  - a 429 counting down from `Retry-After` («حاول بعد 0:42»), with submit disabled and the reason
    beside it (§10), not a fixed «15 دقيقة»;
  - Google's failures worded per code (`GOOGLE_LINK_NOT_ALLOWED`, `service_unavailable`), and no
    button without a client id;
  - the recovery's server-held steps (loading, unreachable, «فتحت رابط الاستعادة», check failed,
    resends spent), with the masked email from the server, not the typed one;
  - the m:ss resend clock;
  - the forced change landing where the role lands (AC-005).
- **proposal:** the prototype draws these states as built. **cost:** S

## 4. Rules in doubt

- **foundation §13, screen 9:** "a Google-only account can add one" reads as a form on Settings.
  security.md › Passwords allows it only through the reset email. Proposed wording: "…can add one,
  through the reset email (security.md)" (AC-001).
- **api-contract §4:** every list pages. A user's favourites may be better answered whole, like the
  directory's set (AC-015). This is the owner's call.

## 5. Not reviewed

- **The built screens live:** compared by reading their code and copy, not by running the app (two
  workers use the dev ports).
- **Email clients:** the reset email was seen only in Chrome.
- **Screen readers:** not run. Keyboard was checked by tab order and focus position only.
- **Roles' account menus:** settled by P4. **The toast above the bottom bar:** SH-012. **The auth
  card's h1:** SH-017.
