> **Update 2026-10-14 (the analyst) — read this first.** PR #80 (the desk batch) has **merged into `main`** (`34a6c59`), and the branch `origin/design/desk` no longer exists. **Ignore every instruction below about `origin/design/desk`** (its SHA, `git show` or `git archive` from it, a second source): read the desk's pages and `INDEX.md` § 56 from the folder at `origin/main`, like every other page, one source only. Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54 — a leftover of a merge, already recorded; do not report it.

# R2-DK-VD — Round 2 review: The front desk and reception · Visual design and consistency

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge visual design and consistency only
(section 5).

## 2. Where

- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write the `origin/main` SHA at the top
  of the report — **and** the `origin/design/desk` SHA (`git rev-parse origin/design/desk`), because
  this part also reviews the about-to-merge desk batch (section 4b).
- Never edit, commit, check out, or install anything in that directory. For the desk branch, use
  only read-only `git show` / `git archive` as section 4b describes — never check it out.

## 3. How to open the prototype

- Serve it on your own port **5430** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5430 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\Users\basel\masaha-design` as the working directory.
- Open pages as `http://127.0.0.1:5430/<Prototype URL>` with the parameters exactly as listed.
- For desk-branch frames (section 4b): extract read-only with
  `git archive origin/design/desk docs/design/prototype | tar -x -C <empty temp dir>` (under your
  TEMP, outside the repo), serve that copy on the same port after stopping the first server, and
  say in each issue which source (`main` or `design/desk`) it was seen in. Delete the temp copy at
  the end.
- At the end: stop every server by its PID and check the port is free (`5430` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-DK-VD-001.png`) in
  `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\DK-VD\` (create it if missing).

## 4. Scope: DK — the front desk and reception

**Prototype pages (this part owns these files):** `Desk.html`, `Customers.html`,
`Customer file.html`, `My payments.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters on `main`; the list below is the entry point, not a copy):** 20, 21, 22, 23,
24, 25, 26, 27, 28, 31.

**Key states to open on `main`:** the full DK state matrix from the sibling DK scope (search,
warn/checkout/pay/sheet dialogs, uncollected, customer file tabs, void flows, handover; read
INDEX.md at run time).

**Roles:** reception first, owner second.

**Widths and modes:** all three widths **390, 768, 1440**; Arabic and English; light and dark.
Narrow only with a stated reason.

### 4b. The desk batch (PR #80, branch `origin/design/desk`) — also in scope

PR #80 (the desk batch) is about to merge, so this review covers its new state too:

- Read the desk branch's pages read-only (`git show origin/design/desk:docs/design/prototype/…`)
  and the desk branch's `docs/design/INDEX.md` **section 56 · Batch 6 — the front desk** plus its
  **Batch 6 parameters** (see the sibling DK scope for the full list).
- Review every §56 frame through this prompt's axis; where a §56 frame supersedes a main frame,
  judge the §56 state and say so.
- Note the desk batch's touches outside DK pages as cross-references for OW — do not review them here.

## 5. Your axis: VD — visual design and consistency

Judge this part through this axis only, deeply. Adapt these questions to the front desk:

1. Hierarchy: the desk's order (search → uncollected → present on the phone; side column from
   1280); one h1 per page; the customer file's own name as h1 (P1/SH-016 as settled).
2. Layout and grid: the money block identical in every dialog (check-out, pay, sheet); the compact
   uncollected card («4 زيارات غير محصّلة · 36 ₪», three rows + «عرض الكل»); five columns from 768
   on Customers and Payments (DK-017); the handover's one card on the phone.
3. Spacing on the scale (foundation §5) across desk cards, dialogs, sheets, and file tabs.
4. Colour by semantic role and token: voided struck with who/why (excluded from figures — K4);
   warnings vs errors in check-in warnings and renewal alerts; destructive red only per P9 (void,
   write-off is owner-only — check its treatment).
5. The same job done the same way on every page: money block, customer actions by state in one
   order (DK-013), void in the row's «⋯» (DK-016), status chips (DK-022), «⋯» menus — name the
   pattern and every place it differs (desk card vs file header vs Customers row).

**Out of this prompt's axis (leave to the other DK prompts, do not report):** flow length and
feedback behaviour (UX); anything broken, overflowing, mis-mirrored, or console errors (DF);
removals of elements (EX); wording and translation (CP); focus, names, contrast, touch targets,
screen-reader order (AX); API/model/v1 truth, money/role privacy (TR).

## 6. What is settled — do not report again

- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and
  `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-003–DK-023).
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

Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-DK-VD_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2 (main and `design/desk`).
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-DK-VD-001`…), title,
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
