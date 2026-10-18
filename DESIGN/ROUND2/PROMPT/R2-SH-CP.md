> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-SH-CP — Round 2 review: The shared layer · Content and Arabic copy

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge shared words only (section 5). You
read Arabic fluently.

## 2. Where

- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory. Quote copy exactly as
  shown; give the URL and parameters where each string appears.

## 3. How to open the prototype

- Serve it on your own port **5439** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5439 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\design` as the working directory.
- Open pages as `http://127.0.0.1:5439/<Prototype URL>` with the parameters exactly as listed.
- Read the copy source `docs/design/prototype/masaha/i18n.js` (and `shared.jsx`'s string table) for
  the exact strings.
- You open other parts' pages **read-only for pattern comparison only**: report pattern-level copy
  issues here; page-level copy belongs to the parts, not to you.
- At the end: stop the server by its PID and check the port is free (`5439` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-SH-CP-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\SH-CP\` (create it if missing).

## 4. Scope: SH — the shared layer (CP angle)

**This part owns no pages.** It owns the recurring words: nav group labels, the switcher, top-bar
titles and «⋯», the drawer (theme, language, account head), the account menu, filter-bar and sheet
labels («عرض N نتيجة», «مسح الفلاتر», result counts «عرض 1–20 من N», chips), pagination («صفحة 1
من 16»), the states' lines (loading, empty, «تعذّر تحميل …» + «إعادة المحاولة», offline, 403, 404,
429 «محاولات كثيرة»), toasts and undo («تراجع»), dismiss («رجوع»), void («إلغاء»), confirm-or-undo
lines, the skip link («تخطَّ إلى المحتوى»), «تغييرات غير محفوظة».

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative; the list below is
the entry point, not a copy):** 11, 12, 41, 50, 51, 52. For pattern evidence, open the same
representative pages as the sibling SH scope in Arabic, then their full English mirror
(`?lang=en`).

**Roles:** all five — one menu, one set of states, one verb discipline for everyone.

**Widths and modes:** Arabic first at **390 and 1440**, then the English mirror of every chrome
string; light is enough unless a string differs in dark.

## 5. Your axis: CP — content and Arabic copy (of the shared patterns)

Judge the shared words through this axis only, deeply:

1. Wording that reads as a translation rather than Arabic said first (nav labels, state lines,
   sheet footers).
2. Terms against `docs/project/glossary.md` used identically in every shell.
3. One thing named two ways across shells (dashboard vs site: favourites, «بلاغاتي», settings,
   sign-out; «تراجع» vs «رجوع» vs «إلغاء» per P9 — audit every occurrence).
4. Labels that do not say what happens («⋯» neighbours, «عرض الكل», pagination summary, sheet
   footers with live counts).
5. Plurals and gender in counts («عرض 1–20 من 312», «صفحة 1 من 16», result counts).
6. Numbers and dates in LTR isolation (`Ltr`) and Arabic-digit reading.
7. The English mirror: same meaning, same place across all shells; no leftover Arabic (or vice
   versa).
8. Truth: a chrome line that promises what the product cannot keep. Boundary with the parts' TR:
   you judge what the *shared words* promise; parts judge their screens' data truth.

**Out of this prompt's axis (leave to the other SH prompts and the parts, do not report):** flow
opinions (UX — R2-SH-UX); layout and type choices (VD — R2-SH-VD); breakage and overflow (DF —
R2-SH-DF — but do report a shared string too long for its control *as a copy defect* with the
width where it breaks); removals (parts); focus/names/contrast (AX — R2-SH-AX); data-depth truth
(parts). Page-level copy belongs to the parts — report pattern-level only.

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (especially the P9 verb
  discipline, P5's sheet footer, P6's count line, P8's toast lines, SH-018's skip link).
- Settled wording is **not reported again**. A settled line applied where it does not fit is
  reported as a misapplication, with the decision named.
- If you believe a settled line makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.10–A.11), §4 (proposals: the better line in Arabic *and*
English, why it is better, cost S/M/L; **pattern-level proposals name every page they change**) and
the report shape in section 8 below. Known limits of the archive (lens §2) are not reported.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-CP_REPORT.md`. English, concise
(quote Arabic strings verbatim). In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-SH-CP-001`…), title,
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
