> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-AD-AX — Round 2 review: The admin's dashboard · Accessibility and resilience

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge accessibility and resilience only
(section 5).

## 2. Where

- Read from `C:\dev\masaha\app-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5420** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5420 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\app-design` as the working directory.
- Open pages as `http://127.0.0.1:5420/<Prototype URL>` with the parameters exactly as listed.
- Drive every page by keyboard alone at least once; where you can, check with a screen reader.
- At the end: stop the server by its PID and check the port is free (`5420` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-AD-AX-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AD-AX\` (create it if missing).

## 4. Scope: AD — the admin's dashboard

**Prototype pages (this part owns these files):** `Admin overview.html`, `Admin spaces.html`,
`Admin space add.html`, `Admin space edit.html`, `Admin owners.html`, `Admin reports.html`,
`Admin users.html`, `Admin lookups.html`, `Admin audit.html`, `Admin settings.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 42, 43, 44, 45, 46, 47, 48, 49.

**Roles:** admin only.

**Widths and modes:** **390, 768, 1440**; Arabic and English; light and dark. Keyboard and
screen-reader order are checked in Arabic (RTL) first, then English (LTR).

## 5. Your axis: AX — accessibility and resilience

Judge this part through this axis only, deeply:

1. Focus visible on every control and in a sensible order (tables and their row menus, link/unlink
   dialogs, the `Combobox` person/space pickers, editor sections and chips nav, lookups switches,
   pagination).
2. A name for every control (row «⋯» menus, switches with their state beside them — «مفتوحة» /
   «مغلقة» — icon buttons, the one-time-password copy button).
3. Information not by colour alone (verification/hidden/deleted states with words, «ناقصة» with
   text, destructive actions with verbs not just red).
4. Contrast (foundation §10) in light and dark, including muted deleted rows, helpers, badges.
5. Touch targets of at least 44 × 44 (row menus, chips nav scrolling sideways, pagination, sheet
   controls on the phone).
6. Screen-reader order: editor section nav with `aria-current`, tables vs their phone cards, dialogs
   trapping focus (the one-time-password dialog: no X, Escape and outside-click do nothing — is the
   keyboard path still sane?), toasts announced.
7. The states a weak connection meets: skeletons, load error with «إعادة المحاولة», offline/403/
   404 inside the shell, 429 on settings and in dialogs, photo-upload failure with retry on its
   tile (`?fail=upload`).

**Out of this prompt's axis (leave to the other AD prompts, do not report):** flow length (UX);
visual hierarchy and spacing (VD); non-accessibility breakage or console errors (DF — but do report
where breakage *causes* an access failure); removals (EX); wording quality (CP); API truth and
permissions (TR).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,
  P8 feedback/429) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all
  amendments, including the one-time-password no-dismiss rules).
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

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-AX_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-AD-AX-001`…), title,
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
