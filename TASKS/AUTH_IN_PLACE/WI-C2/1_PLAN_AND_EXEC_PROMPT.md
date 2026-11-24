# WI-C2 — sign in where the action is: the form inside the overlay

You are a **Claude Code worker** on **Masaha**, a bilingual Arabic RTL / English platform for coworking spaces in Gaza.
This is a fresh session, **Opus 5.5, effort high**, started in the worktree **`C:\dev\masaha\app-design`** (detached at
`main` = `e0f9f66a`, its own `.env`s: the API on **3323** against `masaha_dev`, tests on `masaha_design_test`; the web
on **5323**, as `C:\dev\masaha\app\.claude\launch.json`'s `api-before` / `web-before` run them). `main` is **live in
production**: every merge deploys.

**Another worker is running beside you:** WI-C1 in `C:\dev\masaha\app`, branch `feat/adaptive-dialog`, expected
**#155**: the layer's `AdaptiveDialog` (a dialog from 768 px, a full-screen panel below it, Back closing it, focus back
to the trigger) and `SignInPrompt` moved onto it. **Your work builds on it.** Its approved plan is
`C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\WI-C1\2_PLAN.md` (+ `2b_SUPERVISOR_REVIEW.md`): plan against that API.

## Two phases

1. **Now: read and plan only.** Save the plan to `C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\WI-C2\2_PLAN.md`, say in
   the conversation that it is saved, and **stop**. Do not wait inside plan mode for an answer: the approval comes
   later as a message in this same session. **Edit nothing in the repository in this phase, and touch nothing in
   `C:\dev\masaha\app`** (C1's folder) — read it only.
2. **After the owner's approval and once #155 has merged:** `git fetch`, cut your branch from the new `origin/main`
   (`git switch --no-track -c feat/sign-in-in-place origin/main`), check `AdaptiveDialog` is as C1's plan said (adapt
   where the merged code differs, and say so), then execute the plan to the end without stopping: local
   verification, the Chrome pass, the PR, green CI and `CLEAN`, then `4_REPORT.md` beside the plan. **Never merge.**

Follow the project's skills `start-work-item`, `write-plan`, `open-pr` and `final-report` (with the two phases
above in place of their stop-and-wait).

## Read first — binding

- `C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\0_OWNER_DECISIONS.md` (every entry);
- `C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\1_ANALYSIS.md` — all of it; **this Work Item is I1, I3–I6, I8–I10,
  I12, I14 and I15's content** (C1 built I15's shell);
- ADR 0021 (`docs/architecture/decisions/0021-sign-in-where-the-action-is.md`);
- **The approved pictures** (masaha-prototype, public: `https://github.com/Basel-Ghonaim/masaha-prototype`):
  `prototype/variants/Space details/inplace.jsx` + `.css` (the overlay's views and states) and
  `prototype/variants/Reset password/inplace.jsx` (the reset page's last step), described in
  `decisions/Space details.md`; captures in `C:\dev\masaha\workspace\DESIGN\AUTH\inplace-P2\` (28) and `inplace-P1\`.
  Their words are production's catalogue's, except the ones marked NEW in the files.

## The owner's condition for this Work Item

**No security risk and no user-experience risk; the experience as comfortable as it can possibly be.** A Claude review
with security and UX requirements follows your PR. Plan for it: name, in the plan, how each of these holds:
- no credential in a URL, in `localStorage` / `sessionStorage`, in the held action, in a log or in the query cache
  (the existing rules: mutations with a credential keep nothing in the cache);
- `next` stays validated by `returnUrlOf` everywhere it is read; the overlay adds no new return path;
- the held action holds no secret, runs once, and only in the cases ADR 0021 and I6 / I10 allow;
- Google's popup inside the trapped overlay: keyboard reach, the popup's return, the one-button handler;
- rate limits and every error answer shown as the pictures show them; nothing retried behind the user's back;
- the focus, Back, Escape, the scrim and busy behave as C1 built them; nothing in your views defeats them.

## The work (the plan settles the details)

1. **The overlay holds the form** (`SignInPrompt` grows into the in-place sign-in; its name is yours to keep or change,
   said in the plan). Its views: **sign in** (Google, or, e-mail, password, «نسيت كلمة المرور؟», the primary action,
   «جديد على مساحة؟ إنشاء حساب»); **register** (its title keeps the reason, NEW; name, e-mail, password with the
   password's condition, the privacy policy **opening in a new tab** so the held action stays; «لديك حساب؟ تسجيل الدخول»);
   **the reset link's request** (the e-mail carried over) and **the link sent** (masked address, the resend clock,
   «استخدم بريدًا آخر», and the NEW line that the action completes after the reset); **the password changed elsewhere**
   (A1: when the reset completes in another tab of this browser, the waiting overlay turns into the sign-in with a
   success notice and the e-mail filled, the focus in the password). «العودة إلى تسجيل الدخول» above the title in the
   sub-views. Every state of the pictures: wrong credentials, too many attempts (the clock, the action off), Google
   unavailable, Google's address taken, the e-mail taken (with «سجّل الدخول بهذا البريد»), busy.
2. **After an in-place sign-in or register:** the overlay closes, the user stays on the page, the held action runs
   at once (the heart filled / the report dialog open), its toast says it; **no landing by role** (I4). A temporary
   password: the existing gate takes over and **the held action waits** for the change (I6).
3. **Reuse, do not fork:** the existing `features/auth` forms, hooks, repositories and `establishSession` drive the
   overlay; the pages `/login`, `/register`, `/forgot-password` keep working unchanged for direct visits, the
   header's «تسجيل الدخول» stays a link to the page (I3), `RequireAuth`'s redirects stay.
4. **The reset link's page** (`/reset-password`): when the recovery carries a `next` from the overlay, it says where it
   returns (NEW), and once the password is set it signs in **right there** (the e-mail filled, the focus in the
   password) and lands on `next`, where the held action runs (`masaha.recoveredAt`, today's rule). Never a sign-in by
   itself (ADR 0021 point 4).
5. **The password's condition:** the owner chose, for the auth pages (A7), one line — «8 أحرف على الأقل، فيها حرف
   ورقم» before typing, only what is missing while typing, «✓ كلمة المرور مناسبة» once met. Production shows a list
   of three rules today. Propose in the plan where the change lands (the shared component everywhere it shows, or the
   overlay and the reset page only), with its reason; the owner decides.
6. **Performance (I8):** the overlay's form code (the forms, the schemas, the auth hooks, Google's loader) is not in
   any site page's load; it loads when the overlay first opens, with a short loading state inside it; prefetching on
   the heart's hover / focus is your call. **Add a `check:build` rule** that it never reaches the first download.
7. **Not here:** the berry primary button (WI-B), the full pages' redesign (WI-C3), the dashboard's sign-in paths,
   GOOGLE_VERIFY.
8. **Tests (I12):** component lane — from the heart (sign in → saved → focus back), from the report (sign in → its
   dialog reopens), register in place, Google in place (`fakeGoogle`), wrong credentials, 429, the temporary password
   (the action waits), Escape / Back let the action go, the reset request and the link sent, A1 (a `storage` event),
   the reset page's sign-in landing on `next`; unit lane — the intent's runner and anything pure you add. Existing
   page tests stay green unchanged. Each new test seen failing by a named break.
9. **Documents:** `docs/frontend/architecture.md` §2 (the landing's two cases, the intent's run), `docs/features/auth.md`
   (the overlay, Google's place), `favorites.md` and `data-reports.md` (a guest's press now signs in in place), the
   copy catalogue in both languages; claim only what is built; one home per fact. Record anything else you find as a
   finding (the next free number is in the findings index).

## Hard limits

- Web and docs only: no API code, schema, migration, new dependency or database write. No secret printed.
- Touch only what this Work Item needs. Stage by path, never `git add -A` / `git add .`. No drive-by refactoring.
- The design system's rules hold (semantic tokens, logical classes, the catalogue for every string, both languages).
- Never weaken a test. No production code only a test uses.
- Commits: Conventional, **subject ≤ 50 characters, with a body**; no tool attribution; no `fixup!` left. `#PRNUM` in
  documents, replaced just before the push (expect **#156**; check the PR and Issue lists, since C1 is #155).
- Never push to `main`, never merge, never force-push a branch that is not yours.
- **Heavy commands** (lint, typecheck, build, a test lane, headless Chrome) through the grant script from the
  worktree's root: `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs c2 <command…>` — **C1 runs beside
  you, so expect to wait for its slot.** A run killed for memory: retry once, then CI judges, and say so. If the memory
  guard stops your servers, restart them once at ≥ 4 GB free; if that fails, skip the Chrome pass and say so.
- **Ports 3323 / 5323 only** (3320 / 5320 are C1's). Stop your servers by PID and check the ports are free.

## Verification (phase 2)

- On the head: `format:check`, `lint`, `typecheck`, `check:classes`, `check:links`, `check:conflicts`, `test:unit`,
  `test:component`, a production build (`NODE_ENV=production`), then `check:build` (with your new rule seen failing
  once). `test:api` is left to CI (no API change).
- **Chrome** (the browser pane shown before any layout or axe check): as a guest on a space page, at 390 and 1440,
  Arabic and English, light and dark — the heart → sign in → saved and focus back; the report → sign in → its dialog;
  register in place; the reset request → the link sent; A1 with a second tab; wrong password; Back and Escape; axe on
  each view. Shots to `C:\Users\basel\Downloads\c2-shots\`, curated, never in the repository.
- Push, open the PR with `open-pr`, wait for `gh pr checks` green on the pushed head and `CLEAN`, then `4_REPORT.md`
  with `final-report`: PR number and full head sha, commits, each requirement with its test and the break seen
  failing, the security conditions above one by one, the Chrome results, what ran locally and what CI judged, your
  decisions, anything left.

## Proposed alternatives

If a decision here or in the analysis is wrong, say so in the plan's "Proposed alternatives" with the reason. Build
nothing alternative before the owner's answer.
