> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-SH-DF — Round 2 review: The shared layer · Design defects

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge what is broken in the shared
patterns only (section 5).

## 2. Where

- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5438** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5438 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\design` as the working directory.
- Open pages as `http://127.0.0.1:5438/<Prototype URL>` with the parameters exactly as listed.
- Keep the browser console open on every page; report console errors with the page and parameters.
- You open other parts' pages **read-only for pattern comparison only**: report pattern-level
  breakage here; page-level breakage belongs to the parts, not to you.
- At the end: stop the server by its PID and check the port is free (`5438` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-SH-DF-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\SH-DF\` (create it if missing).

## 4. Scope: SH — the shared layer (DF angle)

**This part owns no pages.** It owns the recurrences listed in the sibling SH scope.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative; the list below is
the entry point, not a copy):** 11, 12, 41, 50, 51, 52. For pattern evidence, open the same
representative pages as the sibling SH scope, every one with `?state=offline|403|404|error|
loading`, settings pages with `?state=ratelimit`, list pages with `?state=loading`,
`?drawer=open` on dashboards (phone), and `?fail=<action>` where the page has one.

**Roles:** all five.

**Widths and modes:** every shell at **390, 768 and 1440** (768 is where shells break — look
hardest there); Arabic and English; light and dark. A defect seen in only some combination says
which.

## 5. Your axis: DF — design defects (of the shared patterns)

Judge the shared layer through this axis only, deeply. What is broken across pages:

1. Shells overflowing, cut or overlapping at any width (top bar with title + «⋯» + state control +
   account at 390; the 768 rail; drawer contents; bottom bars covering content or toasts).
2. A wrong component or variant recurring (sheet vs dialog vs popover for the same job; the public-
   state control mounted twice — P2 as settled, flag recurrences).
3. A missing or wrong state recurring: route states inside the shell (`?state=offline|403|404`
   with no actions, sidebar as the way on — P7), load errors with retry, skeletons, 429 lines; a
   state that says nothing useful on more than one page.
4. Broken RTL/LTR recurring: unmirrored shells, always-LTR values breaking mid-number (SH-007's
   `Ltr`/`nowrap` as settled — flag cells it misses), icons pointing the wrong way, mixed-direction
   text (foundation §8).
5. Dark mode recurring breakage across the §50–§52 frames.
6. Console errors and blank frames on any shell/state combination (with page and parameters).

**Out of this prompt's axis (leave to the other SH prompts and the parts, do not report):** flow
opinions (UX — R2-SH-UX); consistent-but-unbroken visual choices (VD — R2-SH-VD); removals
(parts); wording quality (CP — R2-SH-CP); focus visibility/order, control names, contrast ratios,
touch-target sizes, screen-reader order except where content is visually broken too (AX —
R2-SH-AX); API/model/v1 truth (parts). Page-level breakage belongs to the parts — report
pattern-level only (a flaw *in* a component takes **level: design system**).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P1–P10 with all Amended
  notes, SH-007/SH-018/SH-020, DI-2/DI-4/DI-5/DI-6/DI-7/DI-27 as fixed).
- What these settle is **not reported again**. A settled pattern applied so it breaks is a defect in
  the application — report it as such, naming every page it breaks on.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.5–A.8 and §2c), §4 (proposals from the design system's own
components and tokens; cost S/M/L; **pattern-level proposals name every page they change**) and the
report shape in section 8 below. Known limits of the archive (lens §2) are not reported.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-DF_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-SH-DF-001`…), title,
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
