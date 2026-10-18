# Design fix 1 — apply the shared layer's decisions to the prototype

**The design-fix worker** (one-off, named after its task) · worktree `C:\Users\basel\masaha-design`,
detached at `origin/main` · branch `design/shared`, cut with `git fetch --prune origin`, then
`git switch --no-track -c design/shared origin/main`. Serve the prototype on **port 5343**. No
`npm ci`, no database, no `.env`: you edit static files.

**Size cap:** at most 2 subagents, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_SHARED_PLAN.md` (`write-plan`).
**Report:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_SHARED_REPORT.md` (`final-report`).
**Before/after images:** `C:\Users\basel\Downloads\design-fix-shared\` (not committed).
Follow the skills: `start-work-item` (you are a third worker; your folder is the one above),
`write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

Masaha's design archive (`docs/design/`) becomes the **living design**: Claude Design is no longer
available, so the prototype is fixed and improved by hand (the original is tagged
`design-2026-09-29`). Six reviews take it apart; the first, the shared layer, is decided. Apply its
decisions to the prototype — every item marked **prototype** — so every page inherits them.

## 2. Read first

1. **The decisions:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_SHARED.md` — your scope, item by
   item. Apply only those marked **prototype**; the **design system** and **docs** items are other
   workers'.
2. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_SHARED_REPORT.md`
   (each issue's frames, URLs and evidence) and `C:\Users\basel\Downloads\design-review-shared\`.
3. `docs/design/README.md`, `INDEX.md`, `prototype/BRIEF.md`; `docs/frontend/design-system/foundation.md`
   §5, §7–§10, §12; `docs/project/glossary.md`.
4. The prototype's source: `prototype/masaha/*.jsx`, `masaha.css`, and the pages that use what you
   change.

## 3. How to build it

- **Shared parts first:** the shells and shared components (`shared.jsx`, `owner.jsx`, `admin.jsx`,
  `account.jsx`, `auth.jsx`, `masaha.css`), then each page that needs its own change (P1's actions,
  P5's filters, P6's pagination, P7's states, P8's feedback, P9's dialogs), page by page.
- **Only the design system's components and tokens** (the vendored bundle in `prototype/_ds/`); no
  new colour, size or font. If a decision cannot be built with them, stop and say so.
- **Every change checked** in Arabic and English, light and dark, at 390, **768** and 1440.
- **Screenshots in `docs/design/screens/` are not regenerated in this item** — they are regenerated
  once, at the end of the design phase. Instead, for each change, a **before/after pair** (same page,
  width, language, theme) in the images folder above, named after its decision (`P1-desk-390.png`).
- **The archive's documents:** `docs/design/README.md` says the prototype is now the living design
  (the original at the tag; the screenshots from before until their regeneration), and a new
  `docs/design/CHANGES.md` lists each applied decision in one line (what changed, where, the date).
- Keep `INDEX.md`'s URLs working: a state parameter you rename is renamed there too.

## 4. Stay alert: new design issues

You will see the prototype more closely than the review did. **Any new defect or better design you
find** — in what you change or around it — is reported, never silently fixed or ignored:
- **found while planning:** in the plan's **"Design issues"** section (`write-plan`), each with the
  frame, what is wrong, the better solution from the design system, and its level (prototype / design
  system / pattern);
- **found while working:** in the report's section **"New design issues"**, in the same shape.

Build none of them unless the reply approves it; the analyst routes each to its batch or decision.

## 4b. The owner's additions

The owner may ask you for changes while you work. **A change inside a decision you are applying**
(a spacing, a word, an icon's place) — make it. **A new change** (a new component, a page or section
the decisions do not touch, a different decision, another batch's page, a rule) — don't make it:
say that it goes to the analyst first. Either way, list every addition the owner asked for in the
report's section **"Owner's additions"**, with where it went.

## 5. Risks

- **Scope:** the next reviews (admin, public) are reading the original meanwhile; change a page's own
  content only where a decision says so.
- **Breaking a page:** the prototype is React with in-browser Babel; one syntax error blanks a page.
  Open every page you touched, in both languages, before you commit.
- **The repository:** touch nothing outside `docs/design/`. Workers A and B build in their folders.
- **Weight:** the before/after images stay outside the repository.

## 6. Phase 4 and the pull request

- **Checks:** this item has no code in the product: `format:check` and the link check (by hand, or
  `npm run check:links` if it has reached `main`). No test lanes, no build.
- **Real run:** every page you changed, served on 5343, at the three widths, both languages and
  themes; servers stopped and the port checked free at the end.
- **PR:** title `design: apply the shared layer's decisions` (≤ 50), labels `docs`, `area:docs`,
  assigned to the owner; commits grouped by decision (shells, navigation and menus; header and
  actions; lists and filters; states and feedback; confirmations; words). The analyst reviews it.
  Don't merge.
