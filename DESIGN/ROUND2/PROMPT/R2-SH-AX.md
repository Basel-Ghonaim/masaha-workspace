> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-SH-AX — Round 2 review: The shared layer · Accessibility and resilience

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge shared accessibility and resilience
only (section 5).

## 2. Where

- Read from `C:\dev\masaha\app-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5440** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5440 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\app-design` as the working directory.
- Open pages as `http://127.0.0.1:5440/<Prototype URL>` with the parameters exactly as listed.
- Drive every shell by keyboard alone at least once; where you can, check with a screen reader.
- You open other parts' pages **read-only for pattern comparison only**: report pattern-level
  issues here; page-level issues belong to the parts, not to you.
- At the end: stop the server by its PID and check the port is free (`5440` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-SH-AX-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\SH-AX\` (create it if missing).

## 4. Scope: SH — the shared layer (AX angle)

**This part owns no pages.** It owns the recurrences listed in the sibling SH scope.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative; the list below is
the entry point, not a copy):** 11, 12, 41, 50, 51, 52. For pattern evidence, open the same
representative pages as the sibling SH scope, every one with `?state=offline|403|404|error|
loading|ratelimit` where applicable, `?drawer=open` (phone), and dialogs/sheets open.

**Roles:** all five.

**Widths and modes:** **390, 768, 1440**; Arabic and English; light and dark. Keyboard and
screen-reader order are checked in Arabic (RTL) first, then English (LTR).

## 5. Your axis: AX — accessibility and resilience (of the shared patterns)

Judge the shared layer through this axis only, deeply:

1. The «تخطَّ إلى المحتوى» skip link first in every shell, seen on focus, leading to `main`
   (SH-018 as settled — flag shells that miss it).
2. Focus visible on every shell control and in a sensible order (sidebar/rail, switcher with its
   «تبديل المساحة — …» name and tooltip, top-bar «⋯», drawer, filter bar, pagination, dialogs,
   sheets, toasts' actions).
3. A name for every shared control (rail marks, icon buttons, «⋯» menus, sheet close, toast
   actions).
4. Information not by colour alone across shells; contrast (foundation §10) in both themes —
   compare the §50–§52 dark frames against light.
5. Touch targets of at least 44 × 44 (rail, drawer items, «⋯», pagination, sheet footers, toast
   actions on the phone).
6. Screen-reader order across shells (nav groups announced grouped, dialogs/sheets trapped and
   named, toasts announced, route states announced as the page).
7. The states a weak connection meets as one resilient pattern: skeletons, load error with retry,
   offline/403/404 inside the shell with the sidebar as the way on, 429 with countdown and safe
   retry — identical on every dashboard page.

**Out of this prompt's axis (leave to the other SH prompts and the parts, do not report):** flow
opinions (UX — R2-SH-UX); visual hierarchy and spacing (VD — R2-SH-VD); non-accessibility breakage
or console errors (DF — R2-SH-DF — but do report where breakage *causes* an access failure);
removals (parts); wording quality (CP — R2-SH-CP); data-depth truth (parts). Page-level issues
belong to the parts — report pattern-level only (a flaw *in* a component takes **level: design
system**).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P7 states, P8 feedback/429,
  SH-006/SH-018/SH-020).
- What these settle is **not reported again**. A settled state that is unreachable, unnamed, or
  unusable by keyboard on more than one page is a defect in the application — report it as such,
  naming every page.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.9 and foundation §10), §4 (proposals from the design
system's own components and tokens; why it is better; cost S/M/L; **pattern-level proposals name
every page they change**) and the report shape in section 8 below. Known limits of the archive
(lens §2) are not reported.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-AX_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-SH-AX-001`…), title,
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
