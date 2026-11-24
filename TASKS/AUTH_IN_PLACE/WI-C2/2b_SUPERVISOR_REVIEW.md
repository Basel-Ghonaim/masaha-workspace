# WI-C2 — the supervisor's review of `2_PLAN.md` (2026-11-24)

**Verdict: sound; recommend approval, with D2 answered B (store nothing).** The plan reuses `features/auth` instead of
forking it, keeps the shell light and the forms lazy with a `check:build` rule, turns two accidents of today's code
into stated rules with tests (the action waiting for a forced change; the held path checked as `next`), and corrects
the prompt where the API makes it impossible (the reset link carries no `next`). Checked by the supervisor: nothing in
`pages/site/shell`, `pages/site/public` or `app/` imports `features/auth` today (one comment in `sessionRepository`),
so the chunk rule can hold.

## On the owner's decisions
- **D1 — the one-line condition everywhere** (register, the reset, the forced change, the account's change): agree.
- **D2 — the reset page's e-mail: recommend B, not the worker's A.** A keeps the e-mail the guest typed in
  `localStorage` for up to 15 minutes. It is not a credential, but it is personal data on a device that, for this
  product, is often shared (a coworking space's computer), and anything stored there is readable by any script of the
  origin. The owner's condition is "no security risk"; the gain of A is one typed field that the browser's own
  autofill (`autocomplete="username"` / `email`) usually fills anyway. A1's waiting tab still fills it from memory.
- **D3 — keep the names:** agree. **D4 — the title as the first focus at both widths:** agree (the lazy body and
  Google's iframe make any other first target unreliable). **D5 — renew the held intent at a link request:** agree.
  **D6 — the listed tests rewritten by design:** agree. **D7 — the held path checked as `next`:** agree.
  **D8 — no prefetch:** agree.
- **Design issues 1–7:** agree with every recommendation (production's patterns for rate limit, Google's refusal and
  the register's toasts; «جديد على مساحة؟» as a new line; the hidden "(opens in a new tab)"; the link sent's link).
- **The NEW words:** approve as listed in §13; the review checks them in both languages in the PR.

## For phase 2
- The executor's Google checks (§4.4) come first, before anything else is built on them; a failure is reported, not
  worked around.
- The Claude review after the PR will hold the owner's condition item by item (§ "The owner's condition" of the
  prompt).

## The approval message (sent with `--resume` in the worker's session once the owner says so **and #155 has merged**)

> APPROVED by the owner: D1 (the one line everywhere), **D2 = B** (store no e-mail: the reset page's sign-in opens with
> the e-mail empty, `autocomplete` set, the focus in it; A1's tab fills it from memory), D3–D8 as recommended, design
> issues 1–7 as recommended, the NEW words as listed. #155 has merged: `git fetch`, cut `feat/sign-in-in-place` from
> the new `origin/main`, check `AdaptiveDialog` against C1's plan (say where it differs), then execute to the end
> without stopping: the Google checks first, local verification, the Chrome pass, the PR, green CI and CLEAN, then
> `4_REPORT.md`. Never merge.
