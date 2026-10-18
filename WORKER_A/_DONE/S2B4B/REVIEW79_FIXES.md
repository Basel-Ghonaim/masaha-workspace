# S2b-4b — review fix for PR #79 (one small round)

The independent review (`REPORT\REVIEW79_OPENCODE_REPORT.md` — read it) passed everything but one
should-fix, which the analyst checked in the code: it holds, and it is about money.

## The fix

`apps/web/src/features/spaces/services/pricesForm.ts` › `agorotOf`: an amount with **more than two
decimals** is sent as `shekels * 100`, which is a whole number whenever the extra digits are zeros —
so `12.500` becomes 1,250 agorot and, worse, **`1,000` (an admin typing one thousand with a thousands
separator) becomes 100 agorot, 1 ₪, accepted silently.** The function's own comment says such an
amount is refused; the code does not refuse it.

- **More than two decimals → hand back the text as typed**, so the contract's schema refuses it on its
  field as `invalid_format`, exactly as an unreadable amount is. Up to two decimals is unchanged.
- **Unit tests** in the file's test: `1,000`, `12.500` and `٣٫٠٠٠` are refused (returned as typed);
  `12.5`, `12,50` and `١٢٫٥` still give 1,250; the break (the old `shekels * 100` branch) seen failing.
- **A new commit of its own** (the owner's stated exception to workflow §3's "fold review fixes"):
  `fix(spaces): refuse an amount past two decimals` (47), on top of the branch. No rebase, no
  force-push.

## Then

- **Run only what the fix touches** (the owner: no full round for a small fix): the one unit test file
  (`npm run test:unit -w @masaha/web -- <path to the pricesForm test>`), seen failing with the old
  branch and passing with the fix; then `npm run lint` and `npm run typecheck`. **No full lane
  locally:** CI runs every lane on the push.
- `git push` (a plain push: the new commit sits on top); wait for CI on the pushed head and `CLEAN`.
- One **"Review fixes"** comment on #79; a "Review fixes" section in `REPORT\S2B4B_REPORT.md`. Don't
  merge. Stop every background shell you start.
