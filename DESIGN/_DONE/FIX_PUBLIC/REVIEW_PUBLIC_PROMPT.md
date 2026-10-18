# Design review 3 — the public site

**The design-review-public worker** (a one-off reviewer, named after its task). **Read-only:** you
write nothing in the repository, run no git command that changes anything, and touch no worker's
folder.

**Size cap:** at most 2 subagents, no workflow; the whole review under 500,000 tokens.
**Report:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_PUBLIC_REPORT.md`.
**Evidence images:** `C:\Users\basel\Downloads\design-review-public\` (create it).

## 1. The task in brief

The third of six design reviews. The shared layer is reviewed and **decided**; this review takes
**the public site's pages themselves** — what a visitor (a student, a freelancer, on a phone, in
Arabic, on a weak connection) needs to find a space, judge it and reach it — and the better design
for each. The public directory is the build's next big step (step 3), and the product's face.

## 2. Read first

1. **The lens:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REVIEW_LENS.md`; follow it exactly.
2. **What is settled:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_SHARED.md`. Don't report it
   again (lens §2b).
3. `docs/design/README.md`, `docs/design/SCREENS.md` (public rows 1–4 and 8), `docs/design/INDEX.md`,
   `docs/design/prototype/BRIEF.md`.
4. `docs/frontend/design-system/foundation.md` §5, §7–§10, §12, §13 (*Public site*, *Near me* above
   all); `docs/project/overview.md` (the public v1 scope and *Not in v1*); `docs/project/glossary.md`;
   ADR 0008 (live status is a state, never a count); `docs/architecture/data-model.md` › *Derived
   values* (publicly listed, live status, stale); `docs/plans/v1-mvp.md` › *Planned API surface* ›
   *Public directory* (what the API will answer: one unpaginated set, no location sent).
5. The prototype's source: `masaha/shared.jsx` (the space card and its parts), `space-parts.jsx`,
   `map.jsx`, `location.jsx`, `data.js`, `details-data.js`, and `Home.html`, `Directory.html`,
   `Space details.html`, `About.html`, `Error.html`.

## 3. Your scope

The public screens and their frames, board sections **01–04**, **10**, **11–12** (the public
variants):
- **1 Home** (search, quick areas, «الأقرب إليك» with and without a location),
- **2 Directory** (list **or** map, the filters, sorting, near me and its fallbacks: denied,
  imprecise, outside the Strip, an area or a pin instead),
- **3 Space details** (photos, live status and its absence, prices, hours and shifts, amenities,
  contacts, location, announcements, freshness, the report and favourite actions),
- **4 About / Contact**, **8 404 / error / offline** (their content; the states' pattern is settled).

**The map:** the prototype's map is an illustration; the product's will be OpenStreetMap through
`shared/map` (being built now). Judge the map's **behaviour and layout** (pins, the selected card,
the legend, near me), not its drawing.

**Issue IDs:** `PU-001`, `PU-002`, …

## 4. How to look

- **Serve a copy, never the repository's folder:** extract the archive from `origin/main` to a short
  path and serve it on **port 5342**:
  `git archive origin/main docs/design | tar -x -C C:\Users\basel\design-review-public` (create the
  folder), then serve `C:\Users\basel\design-review-public\docs\design\prototype` on 5342.
- Every page in Arabic and English, light and dark, at 390, 768 and 1440, with the keyboard; evidence
  by headless Chrome (a script in your scratchpad, never committed).
- Read the source of each page, so a proposal names what really changes.
- At the end: stop the server, delete `C:\Users\basel\design-review-public`, check port 5342 is free.

## 5. Risks

- **Writing anything** in the repository or in `masaha`, `masaha-b`.
- **Reporting settled decisions** again, or the archive's known limits.
- **Breaking a product rule:** a seat count, the device's location sent anywhere, anything on
  *Not in v1* (booking, reviews, online payment), a field the data model has not.
- **A proposal outside the design system.**
- **Many small items, no big picture:** lead with the *Patterns* (site-wide) and the directory's and
  the space page's structure.

## 6. When you finish

Save the report; summarise it here in ten lines at most: the five most important points, the counts
by level and impact, and the proposals for the directory and the space page. Change nothing else.
