> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-OW-AX — Round 2 review: The owner's management · Accessibility and resilience

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge accessibility and resilience only
(section 5).

## 2. Where

- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5427** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5427 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\Users\basel\masaha-design` as the working directory.
- Open pages as `http://127.0.0.1:5427/<Prototype URL>` with the parameters exactly as listed.
- Drive every page by keyboard alone at least once; where you can, check with a screen reader.
- At the end: stop the server by its PID and check the port is free (`5427` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-OW-AX-001.png`) in
  `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\` (create it if missing).

## 4. Scope: OW — the owner's management

**Prototype pages (this part owns these files):** `Owner overview.html`, `Owner space profile.html`,
`Owner settings.html`, `Owner audit.html`, `Packages.html`, `Staff.html`, `Announcements.html`,
`Finance.html`, `Payments.html`, `Data reports.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 29, 30, 32, 33, 34, 35, 36,
37, 38, 39, 40, 55.

**Roles:** owner; reception on announcements.

**Widths and modes:** **390, 768, 1440**; Arabic and English; light and dark. Keyboard and
screen-reader order are checked in Arabic (RTL) first, then English (LTR).

## 5. Your axis: AX — accessibility and resilience

Judge this part through this axis only, deeply:

1. Focus visible on every control and in a sensible order (queue links, editor chips nav with
   `aria-current`, package/announcement/staff sheets, per-card saves, Finance tabs, Payments row
   «⋯» menus, void dialogs, drawer on the phone).
2. A name for every control (row menus, icon buttons, switches, the month picker, «⋯» menus).
3. Information not by colour alone (queue states, stale/missing badges, voided struck *with*
   who/why text, destructive verbs not just red).
4. Contrast (foundation §10) in light and dark, including badges, helpers, struck voided rows.
5. Touch targets of at least 44 × 44 (queue links, chips, row menus, pagination, drawer items).
6. Screen-reader order: overview queue before money, editor sections in order, tables vs their phone
   cards, sheets and dialogs announced with their purpose, toasts announced.
7. The states a weak connection meets: skeletons, per-card save failures, sheet save failures with
   retry, load error with «إعادة المحاولة», offline/403/404 inside the shell, 429 per card and on
   settings.

**Out of this prompt's axis (leave to the other OW prompts, do not report):** flow length (UX);
visual hierarchy and spacing (VD); non-accessibility breakage or console errors (DF — but do report
where breakage *causes* an access failure); removals (EX); wording quality (CP); API truth, money
privacy, permissions (TR).

## 6. What is settled — do not report again

- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,
  P8 feedback/429) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all
  notes).
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

Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-OW-AX_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-OW-AX-001`…), title,
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
