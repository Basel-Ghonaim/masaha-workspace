## Review fixes

Folded into their commits (head 23f79af37a7fd3932c3c3d2b75f8b8a04bfb742c):

- F1 — finding 217's quoted number corrected (docs: resolve findings…): `٠٥٩٩٧٧٧٧٨٨٨` → `٠٥٩٩٧٧٧٨٨٨` (ten digits, matching what the Sheet types) in `docs/architecture/findings/217-contacts-and-every-phone-refuse-arabic-indic-digits.md`.
- F2 — the untested link rows tested: `WEBSITE javascript:alert(1)`; `FACEBOOK facebook.com/search/?q.x`, `facebook.com/events`, `facebook.com/share`, `facebook.com/reels`, `facebook.com/videos`, `facebook.com/posts`; `facebook.com/masaha/about`, `facebook.com/profile.php`, `notfacebook.com/masaha` — added to the refusal tests in `packages/shared/src/spaces/contacts.unit.test.ts` (fix(spaces): accept only real links in contacts).
- Phone rows tested: `00972599123456` → `+970599123456`, `022981234` → `+97022981234`, `+1 202 555 0100` refused, `abc` refused — added to `packages/shared/src/core/phone.unit.test.ts` (fix(shared): read Arabic-Indic digits in phones).
- F3 — finding 219's test now fails without the wait: moved the wait into `waitOutToastRemoval` in a new support file `apps/web/src/test/toastRemoval.ts`, rewrote `apps/web/src/test/toastTeardown.component.test.tsx` to dismiss a toast then assert it is gone from the document after the wait, proved it fails when the helper resolves at once, and updated finding 219's Resolution (test(web): wait out toast timers, warm lazy routes; finding 219's resolution updated).
- Finding 228 fixed (the owner's decision): `customerSearch.ts` reads the term's digits through `toWesternDigits` before the digit test, so Arabic-Indic/Eastern suffix digits search the end of a phone; the desk's present search changed — `matchesPerson.ts` reads the term through `toWesternDigits` too (fix(shared): read Arabic-Indic digits in phones).

Verification: lint ✓; typecheck ✓; format:check ✓; check:classes 1,990 files ✓; check:links 2,784 links in 226 documents and 2,690 source files ✓; check:conflicts ✓; build ✓; check:build ✓; test:unit shared 29 files / 384 tests, API 77 / 924, web 196 / 1,403 ✓; test:component 349 / 2,152 ✓; test:api 126 / 1,451 ✓.
