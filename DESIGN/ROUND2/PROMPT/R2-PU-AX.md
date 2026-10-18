> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-PU-AX — Round 2 review: The public site · Accessibility and resilience

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

- Serve it on your own port **5413** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5413 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\app-design` as the working directory.
- Open pages as `http://127.0.0.1:5413/<Prototype URL>` with the parameters exactly as listed.
- Drive every page by keyboard alone at least once; where you can, check with a screen reader.
- At the end: stop the server by its PID and check the port is free (`5413` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-PU-AX-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\PU-AX\` (create it if missing).

## 4. Scope: PU — the public site

**Prototype pages (this part owns these files):** `Home.html`, `Directory.html`,
`Space details.html`, `About.html`, `Error.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 01 Flow, 02 Home states,
03 Directory views & states, 04 Space details variants, 10 About & error pages, 53 Batch 3 — the
public site.

**Roles:** guest; signed-in visitor.

**Widths and modes:** **390, 768, 1440**; Arabic and English; light and dark. Keyboard and
screen-reader order are checked in Arabic (RTL) first, then English (LTR).

## 5. Your axis: AX — accessibility and resilience

Judge this part through this axis only, deeply:

1. Focus visible on every control and in a sensible order (search, filters, sort, view switch,
   cards, hearts, map pins, the picking crosshair region, price tabs, contacts, report controls).
2. A name for every control (the view switch's screen-reader-only label, pin names, hearts,
   «الأقرب إليّ» `aria-pressed`, icon-only map buttons).
3. Information not by colour alone: live-state pin shapes (U6 — filled / bar / hollow / dashed),
   the legend matching the pins, error text with errors, freshness with words not tint.
4. Contrast (foundation §10) in light and dark, including map pins, badges, helpers, distances.
5. Touch targets of at least 44 × 44 (pins are 24 px boxes with 44 × 44 touch; hearts, chips,
   pagination, bottom-bar call/WhatsApp).
6. Screen-reader order: the map's alternative (list), the static space-page map as `role="img"`
   (PU-026), card content order, the phone sheet announced without trapping the map behind it.
7. The states a weak connection meets: skeletons with the card's own frame, photos loading/failed
   (`?photos=`), the map while tiles load, offline/error pages with retry and the failed-retry
   line, 429 where the site can answer it.

**Out of this prompt's axis (leave to the other PU prompts, do not report):** flow length (UX);
visual hierarchy and spacing (VD); non-accessibility breakage or console errors (DF — but do report
where breakage *causes* an access failure); removals (EX); wording quality (CP); API truth,
counts, and location privacy (TR).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes — P7 states,
  P8 feedback) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U6–U7, U12, PU-013,
  PU-026, and the 2026-10-13 Changed note).
- What these settle is **not reported again**. A settled accessible pattern applied so it fails
  (unnamed control, untrapped focus, silent state) is a defect in the application — report it.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.9 and foundation §10), §4 (proposals from the design
system's own components and tokens; why it is better; cost S/M/L; pattern-level proposals name
every page they change) and the report shape in section 8 below. Known limits of the archive
(lens §2) are not reported.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-PU-AX_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-PU-AX-001`…), title,
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
