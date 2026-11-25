## Summary

A guest's heart or «الإبلاغ عن معلومة غير صحيحة» now opens the **sign-in itself over the page** ([ADR 0021](docs/architecture/decisions/0021-sign-in-where-the-action-is.md)), not two links to the pages. Sign in, register, Google and the request for a reset link happen there, each a view of the layer's `AdaptiveDialog` (#155). Signing in closes it: the page and its address stay, the held action runs at once, and the focus goes back to what was pressed, with no landing by role. The reset link's page signs in on its card once the password is set, and lands on the held action's page. The sign-in's code is a lazy chunk of its own, and `check:build` keeps it off the public pages.

Plan: `workspace/TASKS/AUTH_IN_PLACE/WI-C2/2_PLAN.md`, approved with D1 (the password's one line everywhere), D2 = B (no e-mail kept in the browser), D3–D8 and the design issues as recommended.

## Scope

- **The overlay's views:**
  - sign in (Google, «أو», e-mail, password, «نسيت كلمة المرور؟», «جديد على مساحة؟ إنشاء حساب»);
  - register (titled by the reason, the privacy policy in a new tab, «لديك حساب؟ تسجيل الدخول»);
  - the reset link's request and the link sent, with what completes after the reset;
  - A1: a reset completed in another tab brings the sign-in back, the e-mail filled and the password focused.
  - The e-mail carries between views; a password never leaves its form.
- **Every state:** wrong credentials, too many attempts, Google unavailable or refusing to join an account (with «نسيت كلمة المرور؟»), the e-mail taken (with «سجّل الدخول بهذا البريد»), and busy (no way of closing).
- **After a sign-in or register there:** the overlay closes and the action runs. A temporary password goes through the gate first, and the action waits for the change (`intentMayRun`).
- **The reset page:** with a held action, it says where it returns; once the password is set, its sign-in sits on the card (the e-mail empty, focused, `autocomplete="email"`) and lands on the action's page through `landingPath`, else its own `next`, else by role. It never signs in by itself.
- **The held intent:**
  - the report's carries the space's name;
  - it carries the mark of the tab that held it, and a sign-in confirms only its own (or a recovery's);
  - it is read back as `next` is (`returnUrlOf`), and the path that yields is the one followed;
  - a sign-out lets every hold go, in memory too;
  - a link request renews its 15 minutes;
  - `heldIntentPreview` reads it without taking it.
- **The password change's gate** redirects again when a move interrupts its redirect while the change page loads: Back from the overlay's entry after a temporary-password sign-in left the page blank before.
- **The password's condition** is one line everywhere it shows (A7, D1).
- **The `sign-in` chunk** and its `check:build` rule.
- **Documents:** architecture §2 (the landing's two cases), §3 (forms, the chunk) and §4 (the held intent, the `storage` event); `auth.md`, `favorites.md`, `data-reports.md`, `users.md`; finding 230.

## Acceptance criteria

- [x] The heart or the report opens the sign-in over the page, titled by the reason; the views and states above.
- [x] Signed in there, the overlay closes, the URL stays, and the action runs once, its toast in the welcome's place; the focus is back on the heart.
- [x] A temporary password: `/change-password?next=<page>` first, and the action only after the change.
- [x] Escape, the close button, the scrim and Back let the action go; nothing closes while a request is under way.
- [x] The pages `/login`, `/register`, `/forgot-password` are unchanged; the header's «تسجيل الدخول» stays a link.
- [x] The reset page's return line, its sign-in on the card, and its landing.
- [x] The password's one line.
- [x] The sign-in's code is out of every public page's and the shell's load; `check:build` was seen failing.
- [x] Both catalogues; the documents.

## Out of scope

The berry primary button (WI-B), the full pages' redesign (WI-C3), the dashboard's sign-in paths, GOOGLE_VERIFY. No API, schema, migration or dependency change. No design-system file is touched.

## Change type

Feature (web) · documents · a build check.

## Evidence

**Run locally on the head** (through the grant script):

| Check | Result |
|---|---|
| `format:check` · `check:classes` · `check:links` · `check:conflicts` | clean |
| `lint` · `typecheck` | clean |
| `test:unit` | 2,754 passed (web 1,446, API 924, shared 384) |
| `test:component` | 2,261 passed in 353 files |
| `build` (`NODE_ENV=production`) | clean; `sign-in` chunk 21.3 kB, 6.3 kB gzipped |
| `check:build` | clean, with its new line |

**Seen failing first.** Every new test failed under a named break, then the code was restored from a copy:
- **Unit** (13 failures): `intentMayRun` without the change clause; the old held-path check (S1); `renewHeldIntent` creating an intent; the preview taking it; the report's name dropped; `onRecoveryDoneElsewhere` without its key check; the generic register title; `check:build` without the page reach.
- **Component** (36 + 12 failures):
  - `useSignInBusy` never busy; Google's refusal slot not drawn; `FormFailure` without its action;
  - the password line stuck on "needs"; the e-mail report a no-op; the forms' `onRequested` / `onResent` and focus option removed;
  - the reset card's note dropped; the reset page landing without the intent;
  - A1's listener removed; the prompt not closed by the session; no renewal; the privacy link without `target`; no focus on a switch; the sent note never shown;
  - Google remounted per view, isolated: its test alone failed.
- **`check:build`:** a static `@features/auth` import in `SignInPrompt.tsx` failed the new rule on DirectoryPage, HomePage and SpacePage.
- **One break was caught at the hook level only** (R1's N-4, accepted): with `intentMayRun` broken, the overlay's temporary-password test still passes, because the gate also unmounts the site shell in the same render. The hook tests of the favourite and the report are what fail; the rule no longer depends on that render order.

**Tests rewritten by design** (they asserted what this item removes, D6): the prompt's links (`SignInPrompt.component.test.tsx`); the space page's report test's `/login` link; the reset page's «Sign in» link after the set; the reset card's slot name; the password checklist's assertions.

**Chrome** (headless, over CDP; API on 3323 and web on 5323 against `masaha_dev`; the demo owner):
- **Views:** 390 and 1440, Arabic and English, light and dark, the sign-in, register and forgot views each: the panel below 768 px and the dialog above it, the focus on the title at every opening and switch, and axe with no violation (24 views).
- **Flows** (390 Arabic and 1440 English):
  - Back and Escape close it, keep the page and let the action go;
  - a wrong password shows its alert;
  - a sign-in from the heart closes it, keeps the URL, saves the space with its toast and puts the focus back on the heart;
  - the report's dialog opens after a sign-in;
  - the link sent shows the masked address and its line;
  - A1 from a second tab fills the e-mail;
  - the reset page, opened from the e-mail's link, says it returns to the space.
  - axe is clean on each.
- **Google:**
  - Shift+Tab from the e-mail reaches Google's own button inside the trap, and Tab comes back;
  - Enter on it opens Google's window, which shows Google's OAuth error page because `localhost:5323` is not an authorised origin of the client id;
  - closing that window leaves the overlay open and shows nothing.
  - The credential's return is proven by the component test (`fakeGoogle`).

**The plan's Review Focus checks** (the fix round, in Chrome):
- **A temporary password's history:** after the gate fix, the change page shows within ~70 ms of the overlay's step back, and Back from it reaches the earlier page, which the gate redirects. Before the fix the page was left blank.
- **Home and the directory:** the overlay over a card's heart; signed in, the page stays, the heart is saved, and the focus is back on that heart after the grid re-renders, at 390 and 1440.
- **Slow 3G:** the overlay opens at once with its title and the loading line.
- **Offline:** the line and «Try again»; back online, «Try again» loads the forms, the focus on the title.

**The fix round's tests, each seen failing first:**
- S-1 (two hook tests);
- S-2 and N-2 (unit);
- N-1 (component);
- the focus on the link sent;
- the reset page's promise read again;
- the gate's interrupted redirect.

**Not run:**
- `test:api` (no API change; CI runs it).
- In Chrome: completing a registration, or completing a reset (it would change the demo account's password).
- In Chrome: a temporary password's sign-in; the component lane proves it.
- In Chrome: Google's real credential return, which needs an authorised origin and a Google account.

## Screenshots

Kept outside the repository in `Downloads\c2-shots\`:
- the sign-in, register and forgot views at 390 and 1440, Arabic and English, light and dark;
- wrong password, signed in and saved, the report open, the link sent and A1 at 390 Arabic and 1440 English;
- the reset form with its return line;
- Google's button at both widths.

## Definition of Done

- [x] Acceptance criteria met, scope kept
- [x] Lint and typecheck clean; build passes
- [x] Tests in the owning lanes, passing, each seen failing
- [x] No hardcoded text; both catalogues
- [x] RTL and LTR, light and dark, phone and desktop
- [x] Authorization stays on the server (no API change)
- [x] Triggered documentation updated; one home per fact
- [x] Every claim above names its test or command
- [x] Atomic history: four commits
