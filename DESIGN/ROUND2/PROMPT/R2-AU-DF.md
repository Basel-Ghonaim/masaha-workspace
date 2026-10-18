> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-AU-DF — Round 2 review: Signing in and the account · Design defects

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge what is broken only (section 5).

## 2. Where

- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, or install anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5403** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5403 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\design` as the working directory.
- Open pages as `http://127.0.0.1:5403/<Prototype URL>` with the parameters exactly as listed.
- Keep the browser console open on every page; report console errors with the page and parameters.
- At the end: stop the server by its PID and check the port is free (`5403` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-AU-DF-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AU-DF\` (create it if missing).

## 4. Scope: AU — signing in and the account

**Prototype pages (this part owns these files):** `Sign in.html`, `Sign in - board.html`,
`Register.html`, `Forgot password.html`, `Reset password.html`, `Reset email.html`,
`Change password.html`, `Settings.html`, `Favorites.html`, `Reports.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 05 Auth flow, 06 Sign in,
07 Register, 08 Forgot & reset password, 09 Reset email, 13 Register polish, 14 Account signed-in
header, 15 Favourites, 16 My reports, 17 Settings, 18 Forced password change, 19 Account batch-2
fixes, 54 Batch 4 — the account.

**Defect matrix — open every combination:** all `?state=` values (typing, errors, exists,
ratelimit, network, loading, filled, toolong, sent, linkopen, spent, unreachable, checkfailed,
invalid, success, wrongpw, linksent, empty, error), all `?google=` values (error, notallowed,
unavailable, off), `?fail=setlink|language|fav`, `?auth=0|1|google|linked`, `?pw=open`,
`?role=owner|reception|admin|user`, `?demo=pages&tab=open|closed`, `?toast=linked|welcomefav|welcome`,
`?dialog=signin-report`.

**Roles:** guest, user; forced-change landings per role.

**Widths and modes:** every page at **390, 768 and 1440** (the board has no 768 frame — look anyway);
Arabic and English; light and dark. A defect seen in only some combination says which.

## 5. Your axis: DF — design defects

Judge this part through this axis only, deeply. What is broken on the account's pages:

1. Overflow, cut or overlapping content at any of the three widths (long emails, masked addresses,
   password-rule lines, reply rows, countdown text).
2. A wrong component or variant (a select for three choices, a dialog for a long form, a control
   drawn in a state it cannot be in — e.g. an enabled submit during 429).
3. A missing or wrong state: every state in the matrix above must exist and say something useful;
   a blank frame, a state that shows nothing, a toast that never appears.
4. Broken RTL/LTR: numbers, masked emails, phone-like strings, Latin names, icons pointing the
   wrong way, mixed-direction text (foundation §8).
5. Dark mode: unreadable text, lost borders, inverted meaning (`?theme=dark` on every page).
6. Console errors and blank frames on any page/parameter combination.

**Out of this prompt's axis (leave to the other AU prompts, do not report):** flow length and
feedback design (UX); consistent-but-unbroken visual choices (VD); removals (EX); wording quality
(CP); focus visibility/order, control names, contrast ratios, touch-target sizes, screen-reader
order except where content is visually broken too (AX); API/model/v1 truth and permissions (TR).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment).
- What these settle is **not reported again**. A settled pattern applied so it breaks (overflow,
  wrong state, blank frame) is a defect in the application, not the decision — report it as such.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (what to look for — especially A.5–A.8 components, direction,
responsive, states, and §2c: every width, the API contract's failure/429 expectations,
confirm-or-undo), §4 (proposals built from the design system's own components and tokens; cost
S/M/L; pattern-level proposals name every page they change) and the report shape in section 8
below. Known limits of the archive (lens §2) are not reported.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-DF_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-AU-DF-001`…), title,
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
