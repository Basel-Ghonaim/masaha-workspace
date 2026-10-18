> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-OW-DF — Round 2 review: The owner's management · Design defects

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge what is broken only (section 5).

## 2. Where

- Read from `C:\dev\masaha\app-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5424** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5424 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\app-design` as the working directory.
- Open pages as `http://127.0.0.1:5424/<Prototype URL>` with the parameters exactly as listed.
- Keep the browser console open on every page; report console errors with the page and parameters.
- At the end: stop the server by its PID and check the port is free (`5424` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-OW-DF-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-DF\` (create it if missing).

## 4. Scope: OW — the owner's management

**Prototype pages (this part owns these files):** `Owner overview.html`, `Owner space profile.html`,
`Owner settings.html`, `Owner audit.html`, `Packages.html`, `Staff.html`, `Announcements.html`,
`Finance.html`, `Payments.html`, `Data reports.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 29, 30, 32, 33, 34, 35, 36,
37, 38, 39, 40, 55.

**Defect matrix — open every combination:** the full OW state list from the sibling OW scope
(queue demos incl. `demo=missing,nocapacity`, `?drawer=open`, report carries, sheet variants,
`?fail=` per card/sheet, `?month=2026-08`, tabs, void flows, every dashboard `?state=`), plus
`Announcements.html?role=reception` in both roles.

**Roles:** owner; reception on announcements.

**Widths and modes:** every page at **390, 768 and 1440** (the board has no 768 frame — look anyway);
Arabic and English; light and dark. A defect seen in only some combination says which.

## 5. Your axis: DF — design defects

Judge this part through this axis only, deeply. What is broken on the owner's pages:

1. Overflow, cut or overlapping content at any width (queue rows, editor groups on the phone,
   price-table columns at 768, package-sheet summary, Finance cards, staff rows, announcement
   sheets, the phone drawer with `?drawer=open`).
2. A wrong component or variant (tabs where chips belong and vice versa, a dialog for a long form,
   a control drawn in a state it cannot be in).
3. A missing or wrong state: every state in the matrix must exist and say something useful; blank
   frames; «عرض الكل» landing without the month; void dialogs on the wrong payment; per-card
   failures contained to their card.
4. Broken RTL/LTR: amounts, phone numbers, Latin names, dates, icons pointing the wrong way
   (foundation §8).
5. Dark mode on every page (`?theme=dark`, including Finance's three tabs).
6. Console errors and blank frames on any page/parameter combination.

**Out of this prompt's axis (leave to the other OW prompts, do not report):** flow opinions (UX);
consistent-but-unbroken visual choices (VD); removals (EX); wording quality (CP); focus
visibility/order, control names, contrast ratios, touch-target sizes, screen-reader order except
where content is visually broken too (AX); API/model/v1 truth, money privacy, permissions (TR).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all notes).
- What these settle is **not reported again**. A settled pattern applied so it breaks is a defect in
  the application — report it as such.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.5–A.8 and §2c), §4 (proposals from the design system's own
components and tokens; cost S/M/L; pattern-level proposals name every page they change) and the
report shape in section 8 below. Known limits of the archive (lens §2) are not reported.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-DF_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-OW-DF-001`…), title,
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
