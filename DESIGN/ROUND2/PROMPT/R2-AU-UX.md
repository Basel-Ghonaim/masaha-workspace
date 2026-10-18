> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-AU-UX — Round 2 review: Signing in and the account · Experience and flow

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge flows and experience only (section 5).

## 2. Where

- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, or install anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5401** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5401 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\design` as the working directory.
- Open pages as `http://127.0.0.1:5401/<Prototype URL>` with the parameters exactly as listed.
- At the end: stop the server by its PID and check the port is free (`5401` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-AU-UX-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AU-UX\` (create it if missing).

## 4. Scope: AU — signing in and the account

**Prototype pages (this part owns these files):** `Sign in.html`, `Sign in - board.html`,
`Register.html`, `Forgot password.html`, `Reset password.html`, `Reset email.html`,
`Change password.html`, `Settings.html`, `Favorites.html`, `Reports.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 05 Auth flow, 06 Sign in,
07 Register, 08 Forgot & reset password, 09 Reset email, 13 Register polish, 14 Account signed-in
header, 15 Favourites, 16 My reports, 17 Settings, 18 Forced password change, 19 Account batch-2
fixes, 54 Batch 4 — the account.

**Key states to open (from the INDEX preamble, Batch 4):** `Sign in.html` with `?state=ratelimit`,
`?google=error|notallowed|unavailable|off`, `?state=error`; `Register.html` with
`?state=typing|errors|exists|ratelimit|network|loading|filled|toolong`, `?google=error`;
`Forgot password.html` with `?state=sent|ratelimit|loading|unreachable|linkopen|spent`
(`?state=sent&email=<address>`); `Reset password.html` with
`?state=typing|invalid|success|loading|unreachable|checkfailed`; `Settings.html` with
`?auth=1|google|linked`, `?pw=open`, `?state=wrongpw|ratelimit|linksent`, `?fail=setlink|language`;
`Change password.html` with `?auth=1&state=typing`, `?role=owner|reception|admin|user`;
`Favorites.html` / `Reports.html` / `Settings.html` with `?auth=0` (signed-out routing) and
`?state=empty|loading|error`; `Reports.html?demo=pages&tab=open|closed`;
`Space details.html?id=focus&loc=none&auth=1&fav=1&toast=welcomefav` and
`?dialog=signin-report` and `?fail=fav` (the return from signing in — AU judges the account side of
these frames, not the space page itself); `Home.html?loc=none&toast=linked`.

**Roles:** guest (sign-in, register, recovery), user (settings, favourites, reports); owner,
reception and admin only as the forced-change landing (`?role=`).

**Widths and modes:** primarily phone **390** in Arabic light (the account is a phone-first flow);
spot-check **768** and **1440**, English (`?lang=en`), and dark (`?theme=dark`) on the default frame
of each page. Say in the report which widths/modes each issue was seen in.

## 5. Your axis: UX — experience and flow

Judge this part through this axis only, deeply. Adapt these questions to the account:

1. Can a guest finish signing in, registering, and recovering a password in the fewest steps, with
   no dead end and a way back on every card (including the reset form)?
2. Does getting in keep the intent — the action that led to sign-in (saving a favourite, filing a
   report) runs on return and the toast names it; is the way back to the space obvious?
3. Is the forced password change one short path that lands where the role lands, and does it say
   what it did on other devices?
4. After each action is there feedback (what happened, what to do next) — sent steps, countdowns,
   failures with retry — and is nothing asked twice (email re-typed, password rules re-met)?
5. Do the account lists (Favourites, My reports) let a signed-in user reach their goal directly,
   including when a space left the directory or the list pages?
6. Arabic first, phone first, a weak connection in Gaza: thumb reach, short Arabic labels in order,
   no step that assumes a fast network.

**Out of this prompt's axis (leave to the other AU prompts, do not report):** visual polish,
hierarchy and tokens (VD); anything broken, overflowing, mis-mirrored or erroring (DF); removals
and merges of elements (EX — you may reorder steps, but proposing to delete an element is EX);
wording and translation quality (CP); focus order, control names, touch targets, screen-reader
order (AX); whether the API, data model or v1 can hold what is shown, and role permissions (TR).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes: P1, P4–P9 as
  they touch the account) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ACCOUNT.md` (C1–C8 and
  the 2026-10-13 amendment to C5's forced-change line; the prototype's `shared.jsx` belongs to this
  batch while batch 5 runs in parallel).
- What these settle (one account menu, `RequireAuth` signed-out routing, the sent step with masked
  address, intent kept on return, no sign-out-all-devices in v1, vertical account nav, favourites
  answered whole, reports paged) is **not reported again**.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (what to look for — especially B.2 the primary action, B.3 the flow,
B.7 navigation, B.8 Arabic/phone first), §4 (proposals built from the design system's own
components and tokens, why it is better, cost S/M/L; pattern-level proposals name every page they
change) and §5 as modified by section 8 below. Known limits of the archive (lens §2: placeholder
navigation icons, illustrative sample data, the Google font offline) are not reported. Every width
(390, 768, 1440), the API contract's pagination/failure/429 expectations (lens §2c), and the P9
confirm-or-undo classification apply to every page you open.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AU-UX_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-AU-UX-001`…), title,
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
