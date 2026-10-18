> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-AD-TR — Round 2 review: The admin's dashboard · Truth to the product, the data and the API

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge truth to the product, data and API
only (section 5).

## 2. Where

- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5421** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5421 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\Users\basel\masaha-design` as the working directory.
- Open pages as `http://127.0.0.1:5421/<Prototype URL>` with the parameters exactly as listed.
- At the end: stop the server by its PID and check the port is free (`5421` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-AD-TR-001.png`) in
  `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AD-TR\` (create it if missing).

## 4. Scope: AD — the admin's dashboard

**Prototype pages (this part owns these files):** `Admin overview.html`, `Admin spaces.html`,
`Admin space add.html`, `Admin space edit.html`, `Admin owners.html`, `Admin reports.html`,
`Admin users.html`, `Admin lookups.html`, `Admin audit.html`, `Admin settings.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 42, 43, 44, 45, 46, 47, 48, 49.

**Rules to judge by (read at run time):** `docs/project/overview.md` (v1 and *Not in v1*),
`docs/architecture/data-model.md` (Spaces, SpaceManager links, verification, soft delete, lookups,
audit), `docs/api/api-contract.md` (admin spaces/users/owners/reports/lookups endpoints, filters,
failure codes incl. `RECEPTION_LINK_ACTIVE`, `ACCOUNT_HAS_LINKS`, `EMAIL_HAS_ACCOUNT`,
`ALREADY_OWNER`, pagination), `docs/features/users.md` and `space-links.md`, ADR 0007 (soft
delete), ADR 0009 (roles — including the Revised line on customer edit/archive).

**Roles:** admin only — flag anything an admin can do here that the contract reserves otherwise,
and anything shown (e.g. reception links the users row cannot show) that the role should not see.

**Widths and modes:** desktop **1440** and phone **390** in Arabic light are enough; add English or
dark only where the truth differs (it should not).

## 5. Your axis: TR — truth to the product, the data and the API

Judge this part through this axis only, deeply:

1. Nothing on screen the API, the data model or v1 cannot hold: every field shown or sent exists in
   the contract and the model; every list follows pagination; the owners page is a view of users
   (`role=owner`); lookups match the catalogue the API serves.
2. Link/unlink truth: the role follows the links (#62 as built); last-unlink consequences; Rima's
   all-deleted case; suspended owners; `RECEPTION_LINK_ACTIVE` and `ACCOUNT_HAS_LINKS` refusals
   drawn where the contract raises them.
3. State truth: verification vs hidden as two facts; deleted as its own list with restore-then-
   undo semantics (finding 44); stale/missing groups per thresholds; the verified page's three ways
   on.
4. *Not in v1* (overview.md): flag anything the admin screens promise or imply along these lines
   (online payment, QR, booking, reviews, claiming, notifications beyond the reset email).
5. Privacy: reporter names where the admin may see them (and only there — compare OW's anonymous
   view); coordinates shown to the admin only; no account data leaked into the wrong list.

**Out of this prompt's axis (leave to the other AD prompts, do not report):** flow length (UX);
visual choices (VD); breakage (DF); removals (EX); wording quality except where words promise
something untrue — that boundary belongs to CP (CP); keyboard and resilience mechanics (AX).

## 6. What is settled — do not report again

- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and
  `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments, including role-
  as-built and the two-item build).
- What these settle is **not reported again**. Where the prototype contradicts the contract, the
  model, or an ADR, report the contradiction precisely (endpoint/field/rule).
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.11 and §2c: against the API contract), §4 (proposals from
the design system's own components and tokens; why it is better; cost S/M/L; pattern-level
proposals name every page they change) and the report shape in section 8 below. Known limits of the
archive (lens §2) are not reported.

## 8. The report

Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-AD-TR_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-AD-TR-001`…), title,
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
