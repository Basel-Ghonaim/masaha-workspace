> **Update 2026-10-14 (the analyst) — read this first.** PR #80 (the desk batch) has **merged into `main`** (`34a6c59`), and the branch `origin/design/desk` no longer exists. **Ignore every instruction below about `origin/design/desk`** (its SHA, `git show` or `git archive` from it, a second source): read the desk's pages and `INDEX.md` § 56 from the folder at `origin/main`, like every other page, one source only. Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54 — a leftover of a merge, already recorded; do not report it.

# R2-DK-AX — Round 2 review: The front desk and reception · Accessibility and resilience

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge accessibility and resilience only
(section 5).

## 2. Where

- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write the `origin/main` SHA at the top
  of the report — **and** the `origin/design/desk` SHA (`git rev-parse origin/design/desk`), because
  this part also reviews the about-to-merge desk batch (section 4b).
- Never edit, commit, check out, install, or move anything in that directory. For the desk branch, use
  only read-only `git show` / `git archive` as section 4b describes — never check it out.

## 3. How to open the prototype

- Serve it on your own port **5434** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5434 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\Users\basel\masaha-design` as the working directory.
- Open pages as `http://127.0.0.1:5434/<Prototype URL>` with the parameters exactly as listed.
- Drive every page by keyboard alone at least once — the desk is a keyboard job at rush hour; where
  you can, check with a screen reader.
- For desk-branch frames (section 4b): extract read-only with
  `git archive origin/design/desk docs/design/prototype | tar -x -C <empty temp dir>` (under your
  TEMP, outside the repo), serve that copy on the same port after stopping the first server, and
  say in each issue which source (`main` or `design/desk`) it was seen in. Delete the temp copy at
  the end.
- At the end: stop every server by its PID and check the port is free (`5434` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-DK-AX-001.png`) in
  `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-AX\` (create it if missing).

## 4. Scope: DK — the front desk and reception

**Prototype pages (this part owns these files):** `Desk.html`, `Customers.html`,
`Customer file.html`, `My payments.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters on `main`; the list below is the entry point, not a copy):** 20, 21, 22, 23,
24, 25, 26, 27, 28, 31.

**Roles:** reception and owner.

**Widths and modes:** **390, 768, 1440**; Arabic and English; light and dark. Keyboard and
screen-reader order are checked in Arabic (RTL) first, then English (LTR).

### 4b. The desk batch (PR #80, branch `origin/design/desk`) — also in scope

PR #80 (the desk batch) is about to merge, so this review covers its new state too: read the desk
branch's DK pages read-only and its `docs/design/INDEX.md` **section 56 · Batch 6** plus the
**Batch 6 parameters** (full list in the sibling DK scope). Judge the §56 state where it supersedes
`main`, including the money block's keyboard path, the one-tap checkout, and the sheet's
saved-but-unpaid retry. Touches outside DK pages are OW cross-references, not reviewed here.

## 5. Your axis: AX — accessibility and resilience

Judge this part through this axis only, deeply:

1. Focus visible on every control and in a sensible order — at rush speed: search → results →
   dialog fields → submit; row «⋯» menus; the one-tap checkout's focus after the tap; sheet steps;
   file tabs; drawer on the phone.
2. A name for every control (search, «⋯» menus, «خروج» per row, void/write-off menu items, the
   handover's figures, icon buttons).
3. Information not by colour alone (warn vs error dialogs with words, debt/change lines with words,
   voided struck *with* who/why, status chips with text).
4. Contrast (foundation §10) in light and dark, including money figures, badges, struck rows.
5. Touch targets of at least 44 × 44 (search results, «خروج», row menus, bottom-bar «تسجيل زيارة»,
   sheet controls on the phone).
6. Screen-reader order: desk regions in order, dialogs/sheets announced with purpose and trapped,
   toasts (amount, item, method) announced, the present count announced.
7. The states a weak connection meets — the desk's money safety: loading buttons that block double
   taps (P8), failures that keep input with retry, the retry-is-safe line (DK-018), the 429 dialog
   line saying nothing was recorded, offline/403/404 inside the shell.

**Out of this prompt's axis (leave to the other DK prompts, do not report):** flow length (UX);
visual hierarchy and spacing (VD); non-accessibility breakage or console errors (DF — but do report
where breakage *causes* an access failure); removals (EX); wording quality (CP); API truth,
money/role privacy (TR).

## 6. What is settled — do not report again

- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,
  P8 feedback/429 with the desk exception) and
  `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023, DK-018's retry
  safety).
- What these settle is **not reported again**. A settled state that is unreachable, unnamed, or
  unusable by keyboard is a defect in the application — report it as such.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.9 and foundation §10), §4 (proposals from the design
system's own components and tokens; why it is better; cost S/M/L; pattern-level proposals name
every page they change) and the report shape in section 8 below. Known limits of the archive
(lens §2) are not reported.

## 8. The report

Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-DK-AX_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2 (main and `design/desk`).
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-DK-AX-001`…), title,
   **type** (defect | improvement), **level** (design system | pattern | component | page),
   **impact** (high | medium | low, for the user), **where** (frame label from INDEX.md — on main
   or §56 on the desk branch — prototype URL with parameters on your local server, width and mode,
   screenshot path in `docs/design/screens/`), **evidence** (the capture's path), what is wrong /
   what could be better, **proposal**, **why** it is better, **cost** (S/M/L),
   **rule** (the document and section it applies or puts in doubt, if any).
5. Decisions in doubt (if any).
6. What was not reviewed and why.

## 9. Cap

At most 25 issues, the most important first. No praise. One issue per problem.
