> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-AD-VD — Round 2 review: The admin's dashboard · Visual design and consistency

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

- Serve it on your own port **5416** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5416 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\design` as the working directory.
- Open pages as `http://127.0.0.1:5416/<Prototype URL>` with the parameters exactly as listed.
- At the end: stop the server by its PID and check the port is free (`5416` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-AD-VD-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AD-VD\` (create it if missing).

## 4. Scope: AD — the admin's dashboard

**Prototype pages (this part owns these files):** `Admin overview.html`, `Admin spaces.html`,
`Admin space add.html`, `Admin space edit.html`, `Admin owners.html`, `Admin reports.html`,
`Admin users.html`, `Admin lookups.html`, `Admin audit.html`, `Admin settings.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 42, 43, 44, 45, 46, 47, 48, 49.

**Key states to open:** the full AD state matrix from the sibling AD scope (status filters, link/
unlink dialogs, one-time-password dialog, role dialog, report resolve, lookups sheets, editor
`?demo=` limits, hours/prices/contacts edge states; read INDEX.md at run time).

**Roles:** admin only.

**Widths and modes:** all three widths **390, 768, 1440** (tables become cards below 768; the 768
rail and column priorities matter here); Arabic and English; light and dark. Narrow only with a
stated reason.

## 5. Your axis: VD — visual design and consistency

Judge this part through this axis only, deeply. Adapt these questions to the admin:

1. Hierarchy: one h1 per page; the editor's `h2` sections with chips navigation (current section
   marked at every width); the verified read-only page's alert and section order.
2. Layout and grid: data tables full width; row-managed lists (lookups) at reading width (AD-029);
   fixed price-table columns from 768, one card per price on the phone.
3. Spacing on the scale (foundation §5) across lists, dialogs, sheets, and editor groups.
4. Colour by semantic role and token: «ناقصة»/missing as `warning` everywhere; destructive red only
   per P9 (delete, suspend, unlink — hide is neutral); verification vs hidden as two facts (G3);
   deleted rows muted.
5. The same job done the same way on every page: filter bar + chips + count + pagination (P5/P6),
   link/unlink dialogs from either end, one-time-password handover, role dialog, resolve-with-note,
   add-sheets — name the pattern and every place it differs.

**Out of this prompt's axis (leave to the other AD prompts, do not report):** flow length and
feedback behaviour (UX); anything broken, overflowing, mis-mirrored, or console errors (DF);
removals of elements (EX); wording and translation (CP); focus, names, contrast, touch targets,
screen-reader order (AX); API/model/v1 truth and permissions (TR).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments).
- What these settle is **not reported again**. Report only how a page applies a settled pattern
  where that needs a choice (which columns survive at 768 per the SH-007 priority table in
  `CHANGES.md` › Batch 1).
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.1–A.4 and B.4), §4 (proposals from the design system's own
components and tokens — foundation §12 is the inventory; a proposal needing a new component says so
and why; cost S/M/L; pattern-level proposals name every page they change) and the report shape in
section 8 below. Known limits of the archive (lens §2) are not reported.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-VD_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-AD-VD-001`…), title,
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
