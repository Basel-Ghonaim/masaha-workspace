> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-AU-AX — Round 2 review: Signing in and the account · Accessibility and resilience

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge accessibility and resilience only
(section 5).

## 2. Where

- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, or install anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5406** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5406 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\Users\basel\masaha-design` as the working directory.
- Open pages as `http://127.0.0.1:5406/<Prototype URL>` with the parameters exactly as listed.
- Drive every page by keyboard alone at least once; where you can, check with a screen reader.
- At the end: stop the server by its PID and check the port is free (`5406` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-AU-AX-001.png`) in
  `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AU-AX\` (create it if missing).

## 4. Scope: AU — signing in and the account

**Prototype pages (this part owns these files):** `Sign in.html`, `Sign in - board.html`,
`Register.html`, `Forgot password.html`, `Reset password.html`, `Reset email.html`,
`Change password.html`, `Settings.html`, `Favorites.html`, `Reports.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 05 Auth flow, 06 Sign in,
07 Register, 08 Forgot & reset password, 09 Reset email, 13 Register polish, 14 Account signed-in
header, 15 Favourites, 16 My reports, 17 Settings, 18 Forced password change, 19 Account batch-2
fixes, 54 Batch 4 — the account.

**Roles:** guest, user; forced-change landings per role.

**Widths and modes:** **390, 768, 1440**; Arabic and English; light and dark. Keyboard and
screen-reader order are checked in Arabic (RTL) first, then English (LTR).

## 5. Your axis: AX — accessibility and resilience

Judge this part through this axis only, deeply:

1. Focus visible on every control and in a sensible order (auth fields, password toggles, Google
   button, way-back links, list rows and their actions, pagination on reports).
2. A name for every control (fields, password visibility toggles, rules announced as rules, icon
   buttons such as hearts and copies).
3. Information not by colour alone (field errors with text, sent confirmations, reply states).
4. Contrast (foundation §10) in light and dark, including helpers, masked addresses, countdowns.
5. Touch targets of at least 44 × 44 (hearts, toggles, pagination, way-back links on the phone).
6. Screen-reader order: card title → fields → errors → submit; toasts announced; countdown/loading
   not a silent trap.
7. The states a weak connection meets: loading, network failure with retry, 429 with its countdown
   and disabled submit, unreachable recovery states, photos still loading/failed on cards
   (`?photos=loading|failed`).

**Out of this prompt's axis (leave to the other AU prompts, do not report):** flow length (UX);
visual hierarchy and spacing (VD); non-accessibility breakage such as overflow or console errors
(DF — but do report where breakage *causes* an access failure); removals (EX); wording quality
(CP); API truth and permissions (TR).

## 6. What is settled — do not report again

- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,
  P8 feedback/429, P10 save enabled) and
  `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8, especially AC-022's 429
  countdown and the 2026-10-13 amendment).
- What these settle is **not reported again**. A settled state that is unreachable, unnamed, or
  unusable by keyboard is a defect in the application — report it as such.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (what to look for — especially A.9 accessibility, A.8 states, and
foundation §10), §4 (proposals built from the design system's own components and tokens; why it is
better; cost S/M/L; pattern-level proposals name every page they change) and the report shape in
section 8 below. Known limits of the archive (lens §2) are not reported.

## 8. The report

Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AU-AX_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-AU-AX-001`…), title,
   **type** (defect | improvement), **level** (design system | pattern | component | page),
   **impact** (high | medium | low, for the user), **where** (frame label from INDEX.md, prototype
   URL with parameters on your local server, width and mode, screenshot path in
   `docs/design/screens/`), **evidence** (the capture's path), what is wrong / what could be better,
   **proposal**, **why** it is better, **cost** (S/M/L),
   **rule** (the document and section it applies or puts in doubt, if any).
5. Decisions in doubt (if any).
6. What was not reviewed and why.

## 9. Cap

At most 25 issues, the most important first. No praise. One issue per problem.
