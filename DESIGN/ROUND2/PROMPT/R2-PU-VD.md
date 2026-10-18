> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-PU-VD — Round 2 review: The public site · Visual design and consistency

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge visual design and consistency only
(section 5).

## 2. Where

- Read from `C:\dev\masaha\app-design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5409** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5409 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\app-design` as the working directory.
- Open pages as `http://127.0.0.1:5409/<Prototype URL>` with the parameters exactly as listed.
- At the end: stop the server by its PID and check the port is free (`5409` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-PU-VD-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\PU-VD\` (create it if missing).

## 4. Scope: PU — the public site

**Prototype pages (this part owns these files):** `Home.html`, `Directory.html`,
`Space details.html`, `About.html`, `Error.html`.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative for frame labels,
URLs and parameters; the list below is the entry point, not a copy):** 01 Flow, 02 Home states,
03 Directory views & states, 04 Space details variants, 10 About & error pages, 53 Batch 3 — the
public site.

**Key states to open:** every `?loc=`, `?view=`, `?demo=`, `?sheet=`, `?state=`, `?dialog=`,
`?auth=`, `?photos=`, `?area=`/`?period=`/`?priceMin=`/`?priceMax=`, `?fail=` variant above (same
pages and sections as the sibling PU scope; read INDEX.md at run time). Include all five space
variants (focus, branch, golden, numberone, white, zm), the map's marker-tapped frames, and the
error/offline frames.

**Roles:** guest; signed-in visitor (`?auth=1`).

**Widths and modes:** all three widths **390, 768, 1440**; Arabic and English (`?lang=en`); light
and dark (`?theme=dark`). Visual consistency must hold in every combination — narrow only with a
stated reason.

## 5. Your axis: VD — visual design and consistency

Judge this part through this axis only, deeply. Adapt these questions to the public site:

1. Hierarchy: one h1 per page; the card's order (photo → name → area → state → hours → distance);
   the space page's section order with no competing primary headings; About's title as
   `text-heading-1`.
2. Layout and grid: three result columns from `xl` on Directory and Favourites alike (PU-025); the
   map legend inside the map at every width; the aside's behaviour below `lg`.
3. Spacing on the scale (foundation §5): card internals, list gaps, section rhythm on the space
   page.
4. Colour by semantic role and token: live-state marks (filled / filled-with-bar / hollow / dashed
   hollow) as shapes *and* colours, identical in the legend; no price louder than content; dark
   theme a full resolution, not an inversion.
5. The same job done the same way on every page: cards (U12 — photo frame 2:1 phone, 16:9 from
   768; mark for no-photo), pins, the heart (`HeartButton`), freshness lines (U4), per-audience
   price grids (U9), location states — name the pattern and every place it differs.

**Out of this prompt's axis (leave to the other PU prompts, do not report):** flow length, dead
ends and feedback behaviour (UX); anything broken, overflowing, mis-mirrored, or console errors
(DF); removals of elements (EX); wording and translation (CP); focus, names, contrast, touch
targets, screen-reader order (AX); API/model/v1 truth, counts, and location privacy (TR).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` (with its Amended notes) and
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_PUBLIC.md` (U1–U12, H2–H5, the 2026-10-12
  amendments including the striking priceless card, and the 2026-10-13 Changed note).
- What these settle is **not reported again**. Report only how a page applies a settled pattern
  where that needs a choice (e.g. which price grid leads for this space).
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (what to look for — especially A.1–A.4 and B.4 patterns across pages),
§4 (proposals built from the design system's own components and tokens — foundation §12 is the
inventory; a proposal needing a new component says so and why; cost S/M/L; pattern-level proposals
name every page they change) and the report shape in section 8 below. Known limits of the archive
(lens §2: the card covers are drawn stand-ins, not artwork to build) are not reported. Tokens, type
and responsive rules: `docs/frontend/design-system/foundation.md`.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-PU-VD_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-PU-VD-001`…), title,
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
