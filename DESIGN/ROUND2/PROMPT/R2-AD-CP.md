> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-AD-CP — Round 2 review: The admin's dashboard · Content and Arabic copy

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge words only (section 5). You read
Arabic fluently.

## 2. Where

- Read from `C:\dev\masaha\app-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory. Quote copy exactly as
  shown; give the URL and parameters where each string appears.

## 3. How to open the prototype

- Serve it on your own port **5419** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5419 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\app-design` as the working directory.
- Open pages as `http://127.0.0.1:5419/<Prototype URL>` with the parameters exactly as listed.
- Read the prototype's copy source `docs/design/prototype/masaha/i18n.js` (and `admin-data.js`
  sample lines that stand in for server text) for the exact strings.
- At the end: stop the server by its PID and check the port is free (`5419` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-AD-CP-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\AD-CP\` (create it if missing).

## 4. Scope: AD — the admin's dashboard

**Prototype pages (this part owns these files):** `Admin overview.html`, `Admin spaces.html`,
`Admin space add.html`, `Admin space edit.html`, `Admin owners.html`, `Admin reports.html`,
`Admin users.html`, `Admin lookups.html`, `Admin audit.html`, `Admin settings.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 42, 43, 44, 45, 46, 47, 48, 49.

**Copy to cover:** link/unlink consequence lines («تصبح … موثّقة…», last-link lines, Rima's deleted
case); the add-owner sheet and its server-answer lines (`EMAIL_HAS_ACCOUNT`, `ALREADY_OWNER`,
`ACCOUNT_IS_ADMIN`, `ACCOUNT_SUSPENDED`); the one-time-password handover (no-dismiss, «انسخها
أولًا», delivery method); role-dialog lines and disabled-reason lines («دوره يتبع روابطه…»,
«أنت»); suspend/restore lines; state filter names (verified/unverified/hidden/deleted); staleness
and «ما زال ناقصًا»/«لم تُضف بعد»/«ناقصة» lines; hours/shift/price/contact errors and limit lines;
lookups hiding lines (area vs amenity); report resolve lines.

**Roles:** admin only.

**Widths and modes:** Arabic first at **1440 and 390**, then the full English mirror (`?lang=en`)
of every page at **1440** (and 390 for dialogs/sheets); light is enough unless a string differs in
dark.

## 5. Your axis: CP — content and Arabic copy

Judge this part through this axis only, deeply:

1. Wording that reads as a translation rather than Arabic said first.
2. Terms against `docs/project/glossary.md` (verified/unverified/hidden/deleted, owner link,
   suspension, lookup, area/governorate, amenity/own amenity).
3. One thing named two ways (unlink vs remove vs «فك ربط»; delete vs hide vs archive; the space's
   state across list, editor and overview).
4. Labels that do not say what happens («ربط», «ترقية وربط», «استرجاع», «استرجاع الحساب», dialog
   actions repeating the verb per P9).
5. Plurals and gender (spaces, owners, reports, prices, days addressed to the admin).
6. Numbers and dates (counts, «محذوفة · 14 أغسطس», limits, thresholds).
7. The English mirror: same meaning, same place, no leftover Arabic (or vice versa).
8. Truth: a promise the product cannot keep (what linking/unlinking/restoring really does, what the
   one-time password really requires). Boundary with TR: you judge what the *words* promise; TR
   judges whether screens show things the API/model/v1 cannot hold.

**Out of this prompt's axis (leave to the other AD prompts, do not report):** flow and steps (UX);
layout and type choices (VD); breakage and overflow (DF — but do report a string too long for its
control *as a copy defect* with the width where it breaks); removals (EX); focus/names/contrast
(AX); permissions and data-depth truth beyond the words' promises (TR).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the
  P9 verb discipline: dismiss «رجوع», void «إلغاء») and
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (with all amendments).
- Settled wording is **not reported again**. A settled line applied where it does not fit is
  reported as a misapplication, with the decision named.
- If you believe a settled line makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.10–A.11), §4 (proposals: the better line in Arabic *and*
English, why it is better, cost S/M/L; pattern-level proposals name every page they change) and the
report shape in section 8 below. Known limits of the archive (lens §2) are not reported.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-AD-CP_REPORT.md`. English, concise
(quote Arabic strings verbatim). In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-AD-CP-001`…), title,
   **type** (defect | improvement), **level** (design system | pattern | component | page),
   **impact** (high | medium | low, for the user), **where** (frame label from INDEX.md, prototype
   URL with parameters on your local server, width and mode, screenshot path in
   `docs/design/screens/`), **evidence** (the capture's path), what is wrong / what could be better,
   **proposal** (the replacement lines, AR and EN), **why** it is better, **cost** (S/M/L),
   **rule** (the document and section it applies or puts in doubt, if any — glossary entry where
   relevant).
5. Decisions in doubt (if any).
6. What was not reviewed and why.

## 9. Cap

At most 25 issues, the most important first. No praise. One issue per problem.
