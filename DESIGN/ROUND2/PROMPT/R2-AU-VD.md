> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-AU-VD — Round 2 review: Signing in and the account · Visual design and consistency

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge visual design and consistency only
(section 5).

## 2. Where

- Read from `C:\dev\masaha\app-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, or install anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5402** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5402 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\app-design` as the working directory.
- Open pages as `http://127.0.0.1:5402/<Prototype URL>` with the parameters exactly as listed.
- At the end: stop the server by its PID and check the port is free (`5402` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-AU-VD-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AU-VD\` (create it if missing).

## 4. Scope: AU — signing in and the account

**Prototype pages (this part owns these files):** `Sign in.html`, `Sign in - board.html`,
`Register.html`, `Forgot password.html`, `Reset password.html`, `Reset email.html`,
`Change password.html`, `Settings.html`, `Favorites.html`, `Reports.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 05 Auth flow, 06 Sign in,
07 Register, 08 Forgot & reset password, 09 Reset email, 13 Register polish, 14 Account signed-in
header, 15 Favourites, 16 My reports, 17 Settings, 18 Forced password change, 19 Account batch-2
fixes, 54 Batch 4 — the account.

**Key states to open:** every `?state=` / `?google=` / `?fail=` / `?auth=` variant listed for AU in
`R2-AU-UX` §4's sibling scope (same pages and sections; read INDEX.md at run time for the exact
frame URLs). Include the password-rules ticking states (`Register.html?state=typing|filled`), the
Google error frames, the 429 countdown frames, and the reply rows on `Reports.html`.

**Roles:** guest, user; owner/reception/admin only as the forced-change landing.

**Widths and modes:** all three widths **390, 768, 1440**; Arabic and English (`?lang=en`); light
and dark (`?theme=dark`). Visual consistency must hold in every combination — narrow only with a
stated reason.

## 5. Your axis: VD — visual design and consistency

Judge this part through this axis only, deeply. Adapt these questions to the account:

1. Hierarchy: one primary heading per card/page; no repeated titles; the right type styles
   (foundation §7) for auth cards, settings cards, and account lists.
2. Layout and grid: auth cards centred and aligned; settings `max-w-3xl` vs full-width lists (C6);
   edges and baselines lining up across the auth pages.
3. Spacing on the scale (foundation §5): equal gaps between twin fields, cards, and list rows.
4. Colour by semantic role and token: no raw palette values; destructive/warning/success used for
   what they mean (field errors, 429, sent confirmations); nothing that survives only in one theme.
5. The same job done the same way on every page: auth cards, password rules, Google button and its
   failures, sent/success blocks, the way back, favourites/report rows, settings cards — name the
   pattern and every place it differs.

**Out of this prompt's axis (leave to the other AU prompts, do not report):** flow length, dead
ends and feedback behaviour (UX); anything broken, overflowing, mis-mirrored, or console errors
(DF); removals of elements (EX); wording and translation (CP); focus, names, contrast, touch
targets, screen-reader order (AX); API/model/v1 truth and permissions (TR).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and the 2026-10-13 amendment).
- What these settle is **not reported again** (one account menu and its phone avatar, the auth card
  shape with its way back, the sent step, the vertical account nav, settings width vs list width).
  Report only how a page applies a settled pattern where that needs a choice.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (what to look for — especially A.1–A.4 alignment, spacing, hierarchy,
colour/tokens, and B.4 patterns across pages), §4 (proposals built from the design system's own
components and tokens — foundation §12 is the inventory; a proposal needing a new component says so
and why; cost S/M/L; pattern-level proposals name every page they change) and the report shape in
section 8 below. Known limits of the archive (lens §2) are not reported. Rules of visual truth:
`docs/frontend/design-system/foundation.md` (tokens, type, direction, responsive).

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-VD_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-AU-VD-001`…), title,
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
