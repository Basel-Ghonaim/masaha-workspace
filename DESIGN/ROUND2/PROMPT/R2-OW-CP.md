> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-OW-CP — Round 2 review: The owner's management · Content and Arabic copy

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge words only (section 5). You read
Arabic fluently.

## 2. Where

- Read from `C:\Users\basel\masaha-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory. Quote copy exactly as
  shown; give the URL and parameters where each string appears.

## 3. How to open the prototype

- Serve it on your own port **5426** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5426 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\Users\basel\masaha-design` as the working directory.
- Open pages as `http://127.0.0.1:5426/<Prototype URL>` with the parameters exactly as listed.
- Read the prototype's copy source `docs/design/prototype/masaha/i18n.js` (and `owner-data.js` /
  `desk-data.js` sample lines that stand in for server text) for the exact strings.
- At the end: stop the server by its PID and check the port is free (`5426` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-OW-CP-001.png`) in
  `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-CP\` (create it if missing).

## 4. Scope: OW — the owner's management

**Prototype pages (this part owns these files):** `Owner overview.html`, `Owner space profile.html`,
`Owner settings.html`, `Owner audit.html`, `Packages.html`, `Staff.html`, `Announcements.html`,
`Finance.html`, `Payments.html`, `Data reports.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 29, 30, 32, 33, 34, 35, 36,
37, 38, 39, 40, 55.

**Copy to cover:** the queue rows («كل شيء على ما يرام», «بلا حالة مباشرة», «لم تُضف بعد»); counts
in tabs as badges; package validity/limit/billing lines and the repeated-name line; announcement
lines with no title (O9) and the closure's «مغلق الآن» line; the extension dialog (who moves, how
many days); the staff password shown once and its delivery method; Finance tab names and empty
lines; void reasons («ألغاها أحمد: …»); report rows with the reporter as «زائر» (O12); settings
attendance lines (capacity, auto check-out rules); audit lines.

**Roles:** owner; reception on announcements.

**Widths and modes:** Arabic first at **1440 and 390**, then the full English mirror (`?lang=en`)
of every page at **1440** (and 390 for dialogs/sheets); light is enough unless a string differs in
dark.

## 5. Your axis: CP — content and Arabic copy

Judge this part through this axis only, deeply:

1. Wording that reads as a translation rather than Arabic said first.
2. Terms against `docs/project/glossary.md` (package vs subscription vs custom, balance vs credit,
   void, announcement vs closure, queue, data report).
3. One thing named two ways (packages/prices/subscriptions across profile, Packages and Finance;
   «مؤرشف»/«محذوف»/«مخفية» nowhere confused; void vs cancel vs «إلغاء»).
4. Labels that do not say what happens («إنهاء الآن», «تمديد», «عرض الكل», «حفظ واستلام» amounts on
   submits, dialog actions repeating the verb per P9/O4).
5. Plurals and gender (O5: counted nouns through the plural forms; tabs with counts; addressed
   owner).
6. Numbers and dates (months, «34 اليوم · 27 الآن», money, durations).
7. The English mirror: same meaning, same place, no leftover Arabic (or vice versa).
8. Truth: a promise the product cannot keep (what the extension really moves, what «عرض الكل»
   really opens, what the void really keeps). Boundary with TR: you judge what the *words* promise;
   TR judges whether screens show things the API/model/v1 cannot hold.

**Out of this prompt's axis (leave to the other OW prompts, do not report):** flow and steps (UX);
layout and type choices (VD); breakage and overflow (DF — but do report a string too long for its
control *as a copy defect* with the width where it breaks); removals (EX); focus/names/contrast
(AX); permissions and data-depth truth beyond the words' promises (TR).

## 6. What is settled — do not report again

- Read `D:\masahaWorkspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes, including the
  P9 verb discipline) and `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O1–O13 with all
  notes, including O5 plurals and O9's no-title announcements).
- Settled wording is **not reported again**. A settled line applied where it does not fit is
  reported as a misapplication, with the decision named.
- If you believe a settled line makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.10–A.11), §4 (proposals: the better line in Arabic *and*
English, why it is better, cost S/M/L; pattern-level proposals name every page they change) and the
report shape in section 8 below. Known limits of the archive (lens §2) are not reported.

## 8. The report

Save it to `D:\masahaWorkspace\DESIGN\ROUND2\REPORT\R2-OW-CP_REPORT.md`. English, concise
(quote Arabic strings verbatim). In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-OW-CP-001`…), title,
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
