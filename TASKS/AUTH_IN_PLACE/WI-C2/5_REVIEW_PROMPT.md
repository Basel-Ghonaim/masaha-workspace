# WI-C2 — the targeted review of PR #157 (read-only)

You are a **read-only reviewer** of a pull request in Masaha (bilingual Arabic RTL / English, React 19 + Vite web,
Express API). **PR #157**, branch `feat/sign-in-in-place`, head `305c5d3f39fd133e94f0a14b36c6a12914346fde`, base
`main`. The checkout `C:\dev\masaha\app-design` is at that head: read it there, with `git` (e.g.
`git diff origin/main...HEAD`, `git show <sha>`), `gh pr view 157`, Read, Grep and Glob. **Edit nothing in the
repository; run no build, test or server.** Write only your review file (below).

**Your role is given in the launch line: R1 (security) or R2 (experience, accessibility and the whole PR).** Review
only your role's requirements in depth; note anything grave outside it in one line at the end.

## Read first
- `C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\0_OWNER_DECISIONS.md` (every entry) and `1_ANALYSIS.md` (I1–I15);
- `WI-C2\2_PLAN.md` (the approved plan) and `2b_SUPERVISOR_REVIEW.md` (the approval: D2 = B, store no e-mail);
- `WI-C2\4_REPORT.md` (the worker's claims — verify them, do not trust them);
- ADR 0021 in the repository; `docs/backend/security.md` (tokens, cookies, passwords); `docs/frontend/architecture.md`
  §2 (landing and guards, the held intent) as changed by the PR.

**The owner's condition for this work: no security risk and no user-experience risk; the experience as comfortable
as possible.** Judge every requirement against it.

## R1 — security (role R1)
- **R1.1** No credential (password, access token, reset token, recovery key) in a URL, `localStorage`,
  `sessionStorage`, the held intent, a log, an error report or the query cache. Trace every value the overlay, the
  reset page and the held intent store or send.
- **R1.2** D2 = B: **no e-mail is stored** in the browser's storage (the held intent included). The A1 tab fills it
  from memory only.
- **R1.3** Every return path (`next`, the held intent's path, the reset page's landing) passes `returnUrlOf`'s rule;
  `/\host`, `//host`, `/.//host`, full URLs and `javascript:` are refused (S1). Find any path read without it.
- **R1.4** The held action runs only in the cases ADR 0021 / I6 / I10 allow: a sign-in in the tab that held it, or the
  sign-in after a reset completed in this browser; never on a restore; never while `mustChangePassword` is true
  (`intentMayRun`); once only; let go on Escape / Back / close / sign-out / leaving the page / 15 minutes.
- **R1.5** A1 (`onRecoveryDoneElsewhere`): the `storage` event carries no secret; a forged event from another tab of
  the same origin cannot sign anyone in or run an action by itself.
- **R1.6** Google in the overlay: the one-button credential handler cannot receive a token meant for another button;
  `GOOGLE_LINK_NOT_ALLOWED`, `GOOGLE_TOKEN_INVALID`, 503 and a failed script are shown, never retried silently.
- **R1.7** Rate limits (429 with `Retry-After`) and every error code reach the user as the pictures / production
  patterns show; nothing is retried behind the user's back; busy blocks double submits.
- **R1.8** The lazy chunk and its `check:build` rule: no auth code in a public page's static imports; the rule can
  fail (its break is real).
- **R1.9** No new dependency, no API change, no cookie or CORS change, no weakened test (compare deleted or loosened
  assertions in the diff).

## R2 — experience, accessibility and the PR as a whole (role R2)
- **R2.1** The flows match the approved pictures and decisions: the heart and the report open the sign-in in place;
  register and the reset request in place; the link sent with its NEW line; A1; the reset page's sign-in landing on
  the space with the action done; the header link and `RequireAuth` still go to the pages (I3).
- **R2.2** Focus: the title on opening and on each view switch; the password where planned (A1, «سجّل الدخول بهذا
  البريد»); back on the trigger after closing; nothing left focused on a removed node.
- **R2.3** Back, Escape, the close button and busy behave as `AdaptiveDialog` (#155) built them; the views do not break
  them.
- **R2.4** Every user-facing string through the catalogue, in both languages, with the NEW words as approved; Arabic
  first; logical classes only; semantic tokens only; the design system untouched except where the plan said.
- **R2.5** The tests: every new test can fail (a named break in the report — check a sample of five against the code);
  the rewritten tests (D6) still prove what they proved; nothing deleted without a replacement.
- **R2.6** Scope: the 90 files are the plan's (list any outside it); no drive-by change; commits Conventional, subject
  ≤ 50, a body, no attribution, no `fixup!`, `#PRNUM` replaced.
- **R2.7** Documents: architecture §2–§4, `auth.md`, `favorites.md`, `data-reports.md`, `users.md`, finding 230 — true
  of the code, one home per fact, nothing claimed that is not built.
- **R2.8** The report's claims (Chrome results, sizes, runs) are consistent with the code and the CI.

## Output
Write `C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\WI-C2\6_REVIEW_<ROLE>.md` (`6_REVIEW_R1.md` or `6_REVIEW_R2.md`):
1. **Verdict** in one line: *mergeable*, *mergeable after a fix round*, or *not mergeable*.
2. **Each requirement of your role:** PASS / WEAK / FAIL, with `file:line` evidence and, for WEAK / FAIL, the concrete
   failure (input → wrong result) and the smallest fix.
3. **Findings ranked:** blocker / should-fix / nit.
Be precise and brief. Do not restate the plan. Then stop.
