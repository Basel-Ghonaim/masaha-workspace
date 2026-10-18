# PR #40 — review fixes (one list)

**Keep this round tight:** fix these six items only, with the smallest change that closes each. Add
or change only the tests each item names; no extra test sweeps, no refactor beyond the item, no new
abstractions unless item 3 truly needs one. If an item turns out bigger than described, stop and
report instead of expanding it.

An independent review ran on `c5faa76`; the analyst verified items 1–3 in the code. Fold each fix
into the commit it corrects (fixup + autosquash, `--force-with-lease`); no "fix" commits. Then post
ONE "Review fixes" comment on the PR listing what changed. No subagents.

## Must fix

1. **A refused check keeps the token in React state** (`hooks/reset-password/useResetPasswordFlow.ts`,
   `setAnswered(error)` at :33/:46–50). The stored `AppError`'s `cause` is the Axios error, whose
   `config.data` is `{"token":"…"}`. After a 429 or a 5xx a still-valid token stays in component state
   while the page is mounted, which breaks "the check holds the token only until a verdict" (D4).
   - Fix: store only what the screen needs from the verdict (`type`, `code`, `requestId`,
     `retryAfterSeconds`), or the view built from it; never the `AppError` itself. Check that no other
     place in the flow keeps an error or variables carrying the token after an answer.
   - The test at `useResetPasswordFlow.component.test.tsx:126` ("…drops the token") checks only the
     mutation cache, so it passes today. Make it prove the decision: after a refused check (a 429 and
     a 5xx), nothing the hook returns or holds contains the token (for example, serialise the
     result, and the refused view, and assert the token string is absent). Keep the title honest.
   - Correct 4b960a3's commit message if it still claims more than the code does.

2. **A link opened on a reset page that is already showing is ignored** (`carriesLink` read once at
   :29; the effect at :58–64 does not depend on the hash). Pasting a new emailed link into the same
   tab changes only the fragment: no reload, the effect does not re-run, the token stays in the
   address bar and in history, and the page keeps its old screen.
   - Fix: re-run the take-and-check when the location's hash changes, and hold "a link is pending"
     in state that the effect sets, instead of a value read once at mount.
   - Test: navigate the mounted page to `#token=…` and prove the token leaves the address before the
     check is sent, and that the check runs.

3. **A 429 on the link check shows no m:ss countdown** (`useResetPasswordFlow.ts:93–104` rebuilds the
   form failure's "refused" view by hand). A 429 with `Retry-After` shows "wait a moment" and a
   reference line, against the decision that a 429 counts down m:ss.
   - Fix: give the check's failure the same view the forms give a 429, through the shared clock and
     the shared failure-view logic in `shared/forms`, so failure wording keeps one owner. If
     `useFormFailure` can't serve a failure that isn't a form's, propose in your report the smallest
     shared helper (no test-only parameter), and use it.
   - Update the test at `:162–178`, which expects the generic wording, to expect the countdown.

## Should fix (cheap)

4. **The gate's exemption is narrower than route matching** (`PasswordChangeGate.tsx:17–18` compares
   the path exactly; the router also accepts a trailing slash and any letter case). A hand-edited
   `/reset-password/#token=…` would have its token copied into `next`. Match the exemption the way
   the router matches the route (`matchPath`), and add the trailing-slash case to its test. Fold into
   3a9c693.

5. **`useForgotPassword` is named like a write** (architecture.md §3: `useX` is a write). It is the
   forgot page's screen hook; the write is `useRequestLink`. Rename it `useForgotPasswordFlow`, to
   mirror `useResetPasswordFlow`. Fold into d8a862e.

6. **An intermediate commit links to a missing route:** at d8a862e and 3a9c693 the forgot page's
   "Set a new password" link points to `/reset-password`, which exists only from 4b960a3. Move that
   link into 4b960a3, so each commit works on its own.

## Checks and report

- Lint and typecheck on each rewritten commit; the full lanes (check:classes, unit, component, api,
  build + check:build) once on the head, one at a time.
- Report once CI is green on the new head: the head, what changed per item, the counts. Don't merge.
