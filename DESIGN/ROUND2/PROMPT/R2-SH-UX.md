> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-SH-UX — Round 2 review: The shared layer · Experience and flow

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge shared flows and experience only
(section 5).

## 2. Where

- Read from `C:\dev\masaha\app-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5436** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5436 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\app-design` as the working directory.
- Open pages as `http://127.0.0.1:5436/<Prototype URL>` with the parameters exactly as listed.
- You open other parts' pages **read-only for pattern comparison only**: report pattern-level
  issues here; page-level issues belong to the parts, not to you.
- At the end: stop the server by its PID and check the port is free (`5436` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-SH-UX-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\SH-UX\` (create it if missing).

## 4. Scope: SH — the shared layer (UX angle)

**This part owns no pages.** It owns the recurrences: the shells (site and dashboard), navigation
and the space switcher, top bars and drawers, the account menu, page headers, toasts, dialogs and
sheets, the states (loading, empty, error, offline, 403, 404, 429), the filter bar and pagination —
as they recur across parts.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative; the list below is
the entry point, not a copy):** 11 Variants, 12 Variants phone 390, 41 Fix DS date picker,
50 Dashboard variants Arabic dark, 51 Dashboard variants English LTR, 52 Dashboard variants phone
390. For pattern evidence, open representative pages from every part: `Home.html`, `Directory.html`,
`Sign in.html`, `Desk.html?role=reception`, `Customers.html`, `Payments.html`,
`Admin spaces.html`, `Admin users.html`, `Owner overview.html`, `Finance.html` — with
`?state=offline|403|404|error|loading|ratelimit`, `?drawer=open` (phone), `?fail=<action>` where the
page has one.

**Roles:** guest, user, owner, reception, admin — the shells serve all five; judge each shell for
its roles (reception ungrouped nav per P3; admin's «م» rail mark per SH-006).

**Widths and modes:** primarily **390 and 768** (drawer, rail, bottom bars, sheets) in Arabic
light, plus **1440** for the sidebar groups and page-header actions; spot-check English and dark.
Say in the report which widths/modes each issue was seen in.

## 5. Your axis: UX — experience and flow (of the shared patterns)

Judge the shared layer through this axis only, deeply:

1. Can each role find its daily tasks first — owner grouped by task (P3: اليوم · المال · المساحة ·
   الفريق والإعدادات), admin grouped (المساحات · المنصة), reception ungrouped — on desktop, the 768
   rail, and the phone drawer (account at its head — DI-10)?
2. Is there one page header (P1): title with its actions from 768, «⋯» below it, the desk's
   «تسجيل زيارة» as the phone's only bottom bar, a list's add at the row's end at every width?
3. Is there one account menu everywhere (P4) with the same way between site and dashboard, and does
   the site's phone header show the avatar?
4. Is there one filter bar (P5: search always visible, labelled fields inline from 768, bottom
   sheet below with active-count badge and «عرض N نتيجة» / «مسح الفلاتر», count by the toolbar,
   chips for ≤4-choice status) and one pagination (P6: 20 a page, «عرض 1–20 من N», numbers from
   768)?
5. Do toasts sit above the desk's bottom bar, announce what changed (P8 — with the desk exception
   K7), and does every destructive action meet confirm-or-undo (P9: «تراجع» vs `AlertDialog` vs
   «رجوع»)?
6. Dialog vs sheet choice consistent for the job (link, warn, money, add-flows, phone sheets);
   sub-page h1 as the record's name with a `Breadcrumb` back (SH-016).

**Out of this prompt's axis (leave to the other SH prompts and the parts, do not report):** visual
polish, hierarchy and tokens (VD — R2-SH-VD); anything broken, overflowing, mis-mirrored or
erroring (DF — R2-SH-DF); removals as such (judged inside the parts — no SH-EX exists); wording
and translation quality (CP — R2-SH-CP); focus order, names, contrast, touch targets,
screen-reader order (AX — R2-SH-AX); API/model/v1 truth and permissions (judged inside the parts —
no SH-TR exists). Page-level issues belong to the parts — report pattern-level only.

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P1–P10 with all Amended notes
  — this prompt's home ground).
- What P1–P10 settle is **not reported again**. Report only where a page misapplies a settled
  pattern (which action is primary here; which of this page's actions is "felt by others") or a
  page where a settled pattern does not fit, with why.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially B.4 patterns across pages — name the pattern and where it
differs — B.6–B.8), §4 (proposals from the design system's own components and tokens; why it is
better; cost S/M/L; **pattern-level proposals name every page they change**) and the report shape
in section 8 below. Known limits of the archive (lens §2) are not reported. Every width (390, 768,
1440), the API contract's expectations (lens §2c), and the P9 classification apply throughout.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-UX_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-SH-UX-001`…), title,
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
