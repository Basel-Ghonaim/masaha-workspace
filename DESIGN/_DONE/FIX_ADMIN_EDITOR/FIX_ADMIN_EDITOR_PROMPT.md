# Design fix 2a — the admin's space editor and its creation form, in the prototype

**The design-fix worker** · worktree `C:\Users\basel\masaha-design`, detached at `origin/main`
(`d7d800e`) · branch `design/admin-editor`, cut with `git fetch --prune origin`, then
`git switch --no-track -c design/admin-editor origin/main`. Serve the prototype on **port 5346** with
`npx serve` from `docs/design/prototype` (its `serve.json` keeps the `?…` parameters) or
`python -m http.server 5346`. No `npm ci`, no database, no `.env`: you edit static files.

**Model:** Opus 5.5, effort high. **Size cap:** at most 2 subagents, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_ADMIN_EDITOR_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_ADMIN_EDITOR_REPORT.md` (`final-report`).
**Before/after images:** `C:\Users\basel\Downloads\design-fix-admin-editor\` (not committed).
Follow the skills: `start-work-item` (you are a third worker; your folder is the one above),
`write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

Batch 2 (the admin's dashboard) is decided and is built in two items. **This is the first: the space
editor** — the screen worker A builds next (S2b-4) — and the form that creates a space. Apply the
decisions below to the prototype. The second item (the lists, owners, users, overview, reports,
lookups, audit, settings) follows; touch none of its pages' own content.

## 2. Read first

1. **The decisions:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` — its *Amended* note,
   then **The space edit screen** (A1, A2, Hours, Prices, Contacts, the verified space's page) and
   **AD-002** under *Already better in code*. Apply only what is marked **prototype**.
2. **Already settled, which the editor follows:** `DECISIONS_SHARED.md` (P1 as amended, P8, P9, P10);
   `DECISIONS_OWNER.md` **O1** (the owner's profile *is* this editor, differing only by its
   permissions) and **O7** (photos are immediate actions).
3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_ADMIN_REPORT.md`
   (AD-001 … AD-012, with frames, URLs and evidence).
4. **What the code already built,** which the creation form catches up with: `docs/features/spaces.md`
   › *Adding a space on the web* and its *Web decisions*; `docs/features/lookups.md` › *The area
   field*.
5. `docs/design/README.md`, `CHANGES.md`, `INDEX.md`; `docs/frontend/design-system/foundation.md`
   §5, §7–§10, §12; `docs/project/glossary.md`; `docs/api/api-contract.md` › *Spaces (the admin)* (each
   group's fields and limits) and `docs/architecture/data-model.md` › *Spaces* (what a space holds).
6. The prototype's source: `Admin space edit.html`, `Admin spaces.html` (its «إضافة مساحة» only),
   `Owner space profile.html`, `masaha/profile-a.jsx`, `profile-b.jsx`, `admin.jsx`, `shared.jsx`.

## 3. The settled decisions (review them in "Stronger decisions")

- **E1 — the editor (A1):** one «المساحة» section (the basics and the location as two
  `Separator`-ed blocks, one footer, one date, one confirm), then ساعات العمل, الأسعار, المرافق,
  التواصل, then الصور. A group never saved says «لم تُضف بعد» and offers **Save only**. Section
  titles `h2`; the side navigation becomes a scrolling row of chips below `lg`, the current section
  marked at every width, one name per section in both places. **No capacity section** on the admin's
  editor.
- **E2 — the creation form (AD-002, #57):** «إضافة مساحة» leads to a creation form as the code built
  it — one form, *Basics* and *Location*, the grouped area field, «اختياري» on every optional field,
  both landmarks, the pin with its coordinates field, one «إضافة مساحة». Not the editor in a "new"
  mode. Settle in the plan whether it is a page of its own or a state of an existing page, and keep
  `INDEX.md`'s URLs working.
- **E3 — after a creation (A2):** the new space's editor, headed by the «ما زال ناقصًا» checklist (the
  five groups, each «لم تُضف بعد» or «تمّت», each linking its section); the same checklist heads any
  space with missing groups. (The built code still returns to the list; worker A changes it in S2b-4.)
- **E4 — hours, prices, contacts:** as the decision file says (the two labelled `Field`s, a shift
  checked against each open day and its error naming the day, «نسخ إلى كل الأيام», «24 ساعة»; the
  prices' small table and phone cards, «الوردية» from the section's own shifts, the limit's reason, a
  duplicate on its field; the contract's seven contact types, «هاتف» with the carrier derived from the
  prefix, each helper showing the stored form).
- **E5 — the verified space's page (AD-012):** its Alert's two links, «عرض في الموقع», the owner
  named, no section list below `lg`.
- **E6 — the gallery (A1, O7):** no date, no «المعلومات ما زالت صحيحة», no «حفظ»; uploads on choose,
  per-tile progress and failure with retry, removal by `AlertDialog`, reorder and cover at once.
- **E7 — the owner's page shares the editor (O1).** What you change in the shared editor reaches
  `Owner space profile.html`; that is intended. The owner's own differences (prices as a link row,
  capacity moved to Settings, no hide or delete) are batch 5's: leave its page's own content as it is,
  and list in the report what it inherited.
- **E8 — your check scripts are committed** (the owner's decision): the Babel parse and the class
  check you run go into `docs/design/scripts/`, in a commit of their own, with one paragraph in
  `docs/design/README.md` on how to run them and **what they cannot see** (a layout drawn twice, a
  gap, a misplaced block — F2 of fix 1). No CI wiring, no new dependency (use what the prototype
  vendors or Node's own). `docs/design/` is outside Prettier.

## 4. Stay alert: new design issues

You will see the editor more closely than the review did. **Any new defect or better design** is
reported, never silently fixed or ignored: in the plan's **"Design issues"** (`write-plan`), or, once
building, in the report's **"New design issues"**, each with the frame, what is wrong, the better
solution from the design system, and its level (prototype / design system / pattern). Build none
unless the reply approves it.

## 4b. The owner's additions

A change **inside** a decision you apply (a spacing, a word, an icon's place) — make it. A **new**
change (a page or section the decisions don't touch, another batch's page, a rule) — say it goes to
the analyst first. List every addition in the report's **"Owner's additions"**.

## 5. Risks

- **The shared editor:** `profile-a.jsx` / `profile-b.jsx` serve two pages; open both after each
  change. Fix 1's F1 (the form's gap inside a `Card`) must hold.
- **Breaking a page:** one syntax error blanks it. Parse every file you touch and open every page you
  touched, in both languages, before each commit.
- **Your checks' limit:** the scripts and a load matrix see blanks and errors, not layout. Look at
  every changed section with your own eyes at 390, **768** and 1440.
- **The repository:** touch nothing outside `docs/design/`. Workers A and B build in their folders.

## 6. Phase 4 and the pull request

- **Checks:** `format:check` and `npm run check:links`; your two scripts. No test lanes, no build.
- **Real run:** every page you changed, at 390, 768 and 1440, Arabic and English, light and dark;
  before/after pairs in the images folder, named after the decision (`E1-editor-768.png`). Servers
  and browsers stopped and the ports checked free at the end. Stop every background shell you start;
  `jq` is not installed — use `gh … --jq`.
- **The archive's documents:** a *Batch 2a* section in `docs/design/CHANGES.md`, one line per applied
  decision; `INDEX.md` for any URL or parameter you add or rename.
- **PR:** title `design: the admin's space editor` (≤ 50), labels `docs`, `area:docs`, assigned to
  the owner; commits grouped by decision (≤ 50 characters each — count them). The owner reviews it on
  the served prototype. Don't merge.
