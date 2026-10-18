# PR #42 — review fixes (one list)

An independent review ran on `4e525c3` (no blockers); the analyst verified items 1 and 2 in the code,
and the owner tested the real Google flow by hand: sign-in, linking, the linked toast in the
account's language and the admin's landing all work. Fold each fix into the commit it corrects
(fixup + autosquash, `--force-with-lease`); no "fix" commits. Then post ONE "Review fixes" comment
and update the PR description (say the real Google flow was checked by the owner). No subagents.

**Keep this round tight:** only these items, the smallest change that closes each. Add only the
tests an item names. If an item turns out bigger than described, stop and report.

## Must fix

1. **The Google ID token stays in the mutation cache.** `useGoogleSignIn`'s mutation keeps
   `{ idToken, language }` as its variables, and a failure keeps it in `error.cause.config.data`, for
   the default 5 minutes; a sign-in clears nothing, and the API doesn't make the token single-use. Set
   `gcTime: 0` on that mutation, as `useCheckResetLink` already does, and say why in its comment.
   Extend an existing `useGoogleSignIn` test to show the cache holds no token after an answer.
   **Record a finding** (number 34): `useSignIn`, `useRegister` and `useChangePassword` keep passwords
   in the mutation cache the same way; resolves when each sets `gcTime: 0` (not fixed here).

2. **The showcase shows every toast twice:** the root Toaster now wraps the showcase routes, and
   `pages/showcase/ShowcasePreview.tsx` still mounts its own. Remove the preview's Toaster (and its
   copy lines if nothing else uses them), so the root one serves the showcase too. Fold into
   `feat(app): mount the toaster with two toasts`.

3. **Nothing proves the credential handler's life cycle.** Add one test to the `useGoogleButton`
   (or `googleIdentity`) tests: mount, unmount, mount again — `initialize` runs once, exactly one
   handler is live, and a credential delivered after the unmount is dropped (no request sent).

## Google's button language (the owner's test)

4. **Google draws the button in the Google account's language, not ours.** With the owner's real
   client id, on an English page, the button reads «المواصلة باستخدام Google», and the Arabic text
   breaks inside the left-to-right button. Our code passes `locale: 'en'` correctly; Google ignores
   it, most likely in favour of the signed-in Google account's or the browser's language.
   - **Investigate, time-boxed** (about 30 minutes): a locale format such as `en_US`; loading the
     script with the page's language (`?hl=`) and reloading it when the language changes; whether the
     Google account's language is what decides. If one works, fix it in `feat(auth): add Google
     sign-in`, with a test where one fits.
   - **If none works, stop and report** what you tried and what decides the language. **Don't build
     a workaround** (for example our own button with Google's official one transparent on top): that
     needs the owner's approval first.

## Cheap fixes

5. **Cap the width inside the resize observer** (`useGoogleButton.ts:59` stores the raw width,
   `:77` caps it at 400), so a resize above the cap doesn't redraw Google's frame for nothing.
6. **Two stale lines in architecture.md:** `:177` `AuthRepository { login, register }` gains
   `google`; `:193` the toast bullet names `useGoogleSignIn`'s linked toast too.
7. **Two findings to record or extend** (in `docs(project): record Google sign-in as built` or the
   commit that already holds findings):
   - extend **finding 29**'s evidence: on 2026-10-06 dev servers left over from earlier runs (a
     `tsx watch` that survived Ctrl+C on Windows, and a Vite started for screenshots) kept ports 5320
     and 3320, so a fresh `npm run dev` failed or reached a stale API with an old environment;
   - **a new finding** (number 35): the web sets no document title — `index.html` has no `<title>` and
     no page sets one — so every tab shows the URL (WCAG 2.4.2, page titled). Resolves when each page
     has a title in both languages.

**Left as they are:** the review's nit 4 (the extra tests for the 422 line, the width cap and the
register toast's language).

## Checks — don't re-run what already passed

- Lint and typecheck on each rewritten commit.
- On the head, once: `test:component` and `test:unit` (web code changed), and `check:classes`.
  Skip `test:api` locally (no API change); CI runs every lane on the pushed head. The four known
  lazy-page timeouts (finding 28) may fail locally; say so if they do.
- Report once CI is green: the head, what changed per item, item 4's outcome, the counts. Don't merge.
