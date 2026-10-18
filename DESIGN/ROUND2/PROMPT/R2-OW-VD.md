> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-OW-VD — Round 2 review: The owner's management · Visual design and consistency

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge visual design and consistency only
(section 5).

## 2. Where

- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5423** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5423 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\design` as the working directory.
- Open pages as `http://127.0.0.1:5423/<Prototype URL>` with the parameters exactly as listed.
- At the end: stop the server by its PID and check the port is free (`5423` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-OW-VD-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-VD\` (create it if missing).

## 4. Scope: OW — the owner's management

**Prototype pages (this part owns these files):** `Owner overview.html`, `Owner space profile.html`,
`Owner settings.html`, `Owner audit.html`, `Packages.html`, `Staff.html`, `Announcements.html`,
`Finance.html`, `Payments.html`, `Data reports.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 29, 30, 32, 33, 34, 35, 36,
37, 38, 39, 40, 55.

**Key states to open:** the full OW state matrix from the sibling OW scope (queue demos, editor
report carry, package sheet variants, announcement tabs/dialogs, staff sheet states, Finance tabs
and month, Payments range/voided/void, reports open/filter, settings card failures, audit;
read INDEX.md at run time).

**Roles:** owner; reception on `Announcements.html` only.

**Widths and modes:** all three widths **390, 768, 1440**; Arabic and English; light and dark.
Narrow only with a stated reason.

## 5. Your axis: VD — visual design and consistency

Judge this part through this axis only, deeply. Adapt these questions to the owner:

1. Hierarchy: the queue first on the overview (counts and links, no amounts — O3); one h1 per
   page; the editor's `h2` sections with chips nav; Finance's three tabs with counts as `Badge`s.
2. Layout and grid: the AD-008 price table with its own date and confirm on Packages; the package
   sheet's live summary; per-card save on Settings; voided payments struck with who/why in Payments
   and the customer file's «الدفعات».
3. Spacing on the scale (foundation §5) across queue rows, editor groups, sheets, and Finance cards.
4. Colour by semantic role and token: queue states, stale/missing badges, voided struck (excluded
   from cards — K4), destructive red only per P9/O4 (void, staff removal, extension, owing-archive).
5. The same job done the same way on every page: queue rows, «عرض الكل» links (Finance → Payments
   carrying the month — DI-36), sheets (package, announcement, staff), add-then-hand-over
   (password shown once), resolve-with-«تم التصحيح» — name the pattern and every place it differs.

**Out of this prompt's axis (leave to the other OW prompts, do not report):** flow length and
feedback behaviour (UX); anything broken, overflowing, mis-mirrored, or console errors (DF);
removals of elements (EX); wording and translation (CP); focus, names, contrast, touch targets,
screen-reader order (AX); API/model/v1 truth, money privacy, permissions (TR).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all notes).
- What these settle is **not reported again**. Report only how a page applies a settled pattern
  where that needs a choice.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.1–A.4 and B.4), §4 (proposals from the design system's own
components and tokens — foundation §12 is the inventory; a proposal needing a new component says so
and why; cost S/M/L; pattern-level proposals name every page they change) and the report shape in
section 8 below. Known limits of the archive (lens §2) are not reported.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-VD_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-OW-VD-001`…), title,
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
