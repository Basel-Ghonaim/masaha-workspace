# Review of #132 — R4: the public site and the account — git objects / read-only review
Head: a12c0790 · commits 15 · checks: green · head moved during the review: no
Verdict for my range: not mergeable

## Findings (verified defects only, most severe first)
### R4-F1 — should-fix · Password recovery drops `next` on the reset route (finding 232)
- Where: `apps/web/src/pages/site/auth/ForgotPasswordPage.tsx:45`, `apps/web/src/pages/site/auth/ResetPasswordPage.tsx:24,29` at a12c0790
- Seen in the code: the forgot page's “continue” link navigates to `/reset-password` without carrying `next`; both the reset page's “back to sign in” link and its post-success sign-in link navigate to `/login` without a query.
- Scenario: a guest starts at `/login?next=%2Fspaces%2Fspace-a`, opens “forgot password”, follows the sent-link flow to the reset page, then chooses “back to sign in” (or finishes the reset) → the sign-in page has no `next`, so successful sign-in lands by the default landing rule instead of returning to the requested page. This contradicts D9.4's kept way back and the required sign-in-flow behavior.
- Fix: preserve the validated `next` query through Forgot → Reset and on both reset-page sign-in links, using the existing `nextSearch`/`returnUrlOf` path rather than concatenating unvalidated input. · Belongs: a fix round on #132

### R4-F2 — should-fix · A password recovery can apply a held guest action to a different account (finding 233)
- Where: `apps/web/src/shared/routing/guest/heldIntent.ts:12-14,106-109` at a12c0790
- Seen in the code: the stored union contains only the action, path and timestamp; on every session established with `source === 'signIn'`, the code consumes it and sets `returnTo`, with no account, recovery-flow or initiating-session binding.
- Scenario: guest A presses Favorite or Report, starts recovery, then signs in with account B (for example by using a different account's recovery email or switching credentials) → the stored intent is consumed and the favorite is saved for B or B is taken to the report dialog. The requirement explicitly says the action cannot fire into another account.
- Fix: bind the held action to the account/recovery transaction that initiated the recovery and consume it only when the newly established session matches that binding; otherwise clear it without running. · Belongs: a fix round on #132

### R4-F3 — should-fix · A held action can survive a later visit in a new tab (finding 234)
- Where: `apps/web/src/pages/site/shell/useGuestIntents.ts:21`, `apps/web/src/shared/routing/guest/heldIntent.ts:106-109` at a12c0790
- Seen in the code: the “left the site page” guard depends on the module-local `shown` value inside `guestLeaving.ts`; a new tab starts with `shown === null`, while the held action is read from shared `localStorage` and is consumed by any later `source === 'signIn'`.
- Scenario: a guest presses a held action, closes the tab or completes recovery in another tab without consuming it, later opens a different site page in a fresh tab, and signs in within 15 minutes → the fresh tab never observes the original page transition, so the old local-storage intent is consumed and runs on the later visit. This violates D9.6's “or later visit” bound.
- Fix: store and validate the originating site-page/session nonce with the held intent, and clear it when a new tab/session observes a different page or when the recovery round trip is no longer the one that created it; do not let a fresh tab consume an orphaned intent solely because the timestamp is still young. · Belongs: a fix round on #132

## The checklist (lines 1–7, each answered)
1. **Every commit of my range read:** `79d8bdcd` keep `next` and the way back; `20869f1b` password-too-long rule; `7e2d442a` second offline retry announcement; `95ea07af` Home/About; `1f1ce675` directory map/results; `2048fdc4` light-tile map marks; `43e69574` near-me permission wait; `36c88ec3` area-count ceiling; `c611a7ad` space page; `b8eb7ff5` route retry and bare 403; `167dcd70` favourites readiness line; `974ab466` site/footer/areas/pick tests; `8f804bad` first Google welcome; `00017140` account editing; `f91b34cf` held guest action through reset.
2. **Plan decisions for U9:** D9.1–D9.15 are present in the head's U9 implementation, including the account `PATCH /me` path, immediate language/session update, password byte rule, same-site `next` validation, held-intent storage, completed public pages, directory/map fixes, retry/403 states and favourites. D9.4 and D9.6 are not built completely: the reset links lose `next`, and the held-intent implementation lacks account and fresh-tab/later-visit binding (R4-F1–F3).
3. **Money, roles, privacy, keys and locks in my range:** no money computation or key/lock change. The held-intent defects can save a favourite for the wrong signed-in account or open a private report action in that account; R4-F2 is therefore a real account-isolation defect. The bare 403 remains role-gated in the code read.
4. **Planned tests and breaks:** T250–T298 are reported as present, with their listed red breaks run by lane W4; the lead reports the integrated W4 component run green after the documented finding-87 timeout exception. The coverage is weaker than the requirement for R4-F1–F3: the reported T260 only covers the forgot-page back path, not the reset-page links; T267–T270 cover age, sign-in, restore and same-tab leaving, but do not prove account mismatch or a fresh-tab later visit.
5. **Screens in range:** the code and prototypes/planned gaps cover Home, Directory, Space details, About, Sign in, Register, Forgot/Reset, 404/error/offline, Profile & settings, and Favourites in both catalogue directions and responsive shell variants. The lane/lead reports state the component checks and real-run coverage; the real run did not perform the write cases, and it explicitly lacked the Google-only account in the local environment. The reset navigation gap and held-intent lifecycle gaps remain named above.
6. **Findings closed in range:** 32's web half (first Google welcome), 82, 133–138 and 168 are implemented as described in the lead/lane reports. Finding 168 is not fully resolved because the code does not enforce its “not another account” and “not a later visit” constraints (R4-F2–F3).
7. **Documents changed in range:** the changed auth, users, directory, favourites, data-reports, architecture and design-system documents generally describe the implemented surfaces. The auth and architecture descriptions overclaim D9.4/D9.6 by describing preserved recovery/held-intent behavior without the three code paths above; those facts need correction with the fix round.

## Decisions taken without the owner in my range, judged
- **LW4-D1 — defer the WhatsApp contact line until W2 joined:** sound and subsequently completed in the folded `C9.4` fixup; the head uses the configured WhatsApp link and falls back to About.
- **LW4-D2 — held-intent union with a favorite name or report slug:** acceptable as a transport shape, but insufficient without the account/recovery binding required by R4-F2.
- **LW4-D3 — a held-action toast replaces “Welcome back” by one toast id:** acceptable; it preserves one user-facing result.
- **LW4-D4 — route retry uses a replaced same-address navigation marker:** acceptable for the intended one-retry behavior.
- **LW4-D5 — carried directory scroll behavior needs no additional production change:** acceptable; the test pins the post-page-arrival behavior.
- **LW4-D6 — empty favourites focus falls back to “Browse spaces”:** acceptable and consistent with the focus rule.
- **LW4-D7 — set-password link has no resend countdown; current-password errors stay on the form:** acceptable for the planned account surface.
- **LW4-D8 — stale status age is measured from the last failed try:** acceptable and matches the stated freshness behavior.
- **LW4-D9 — permission-prompt timing waits for `granted` or a position:** acceptable.
- **LW4-D10 — bare 403 owns the home/contact paths in shared routing:** acceptable; these are route constants, not user-facing copy.
- **LW4-D11 — About/Home tests warm their lazy modules:** acceptable as a test-lane stabilization measure; it does not prove the unperformed real-run write cases.

## Outside my range
- API-only portions of findings 32 and 168, all dashboard/desk/finance/admin implementations, and the deployment findings 23, 33, 46, 64, 65 and 152.
- Lane W4's reported finding-87 cold-import timing misses in untouched dashboard route files are outside this review's defect findings.

## Not checked, and why
- No package installation, server, database, test, build, checkout, switch, reset or GitHub comment was run, per the read-only commit-object review rules.
- Visual rendering at every exact 390/768/1440 viewport and dark/RTL combination was not independently reproduced; the lead's real-run report was read, including its stated omissions.
