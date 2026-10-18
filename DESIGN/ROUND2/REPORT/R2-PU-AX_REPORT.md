# R2-PU-AX — Round 2 review: The public site · Accessibility and resilience

1. Commit SHAs

- `HEAD` = `5e8c979d7ece5193febedcae92db3e08510b2525`
- `origin/main` = `5e8c979d7ece5193febedcae92db3e08510b2525`

HEAD equals origin/main. Reviewed at the committed `main` (34a6c59 merged state noted in the prompt).

2. Verdict

The public site applies the settled accessibility patterns well (named controls, focus rings, map pin shapes, live regions, retry/offline states), but two applied patterns fail: the skip-to-content link has no target, and the filter sheet toggle exposes no open/closed state, so a screen-reader user cannot reach main content directly or know whether the filter sheet is open.

3. Five most important points

- Skip link «تخطَّ إلى المحتوى» points at `#main`, which no public page defines, so it goes nowhere.
- Directory filter sheet toggle button has no `aria-expanded`, so its open/closed state is not announced.
- Live-status pins use shape as well as colour (filled / bar / hollow / dashed), matching the legend — colour alone is not relied on.
- Every control carries a programmatic name (view switch sr-only label, pin names, heart `aria-label`, «الأقرب إليّ» `aria-pressed`).
- Skeletons, loading regions (`aria-busy`), error/offline retry, and the static space-page map (`role="img"`) are all present per P7 / PU-026.

4. Issues

## R2-PU-AX-001 — Skip link target missing

**type:** defect
**level:** page
**impact:** medium
**where:** Frame label "1 · Home" / "2 · Directory — list" / "4 · Space details" / "About «عن مساحة» / "404" — `Home.html`, `Directory.html`, `Space details.html`, `About.html`, `Error.html`, all at `http://127.0.0.1:5413/<page>`, width 390/768/1440, AR light/dark and EN light/dark. Screenshot in `docs/design/screens/01-flow/`, `03-directory-views-states/`, `04-space-details-variants/`, `10-about-error-pages/`.
**evidence:** `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-AX\R2-PU-AX-001.png` (Home page, 390×844, AR light; skip link is the first focusable element).
**what is wrong:** `SkipLink` (shared.jsx:276) renders `href="#main"` on every public page, but none of `Home.html`, `Directory.html`, `Space details.html`, `About.html`, `Error.html` gives its `<main>` an `id="main"`. Keyboard and screen-reader users activating «تخطَّ إلى المحتوى» are taken nowhere — the settled SH-018 pattern is applied but fails.
**proposal:** Add `id="main"` to the `<main>` element of each public page so the skip link reaches the page's main content.
**why:** A skip-to-content link that resolves nowhere fails WCAG 2.4.1 / foundation §10 (bypass blocks); it denies keyboard and screen-reader users a direct route to content on every public page.
**cost:** S
**rule:** SH-018 (settled: «تخطَّ إلى المحتوى» first in every shell, prototype); foundation §10 accessibility baseline.

## R2-PU-AX-002 — Filter sheet toggle exposes no open/closed state

**type:** defect
**level:** component
**impact:** medium
**where:** Frame label "2 · Directory — list" / "2 · Directory — map" — `Directory.html?loc=none` and `Directory.html?view=map&loc=none`, `http://127.0.0.1:5413/Directory.html`, width 390 (and map view at every width), AR light/dark and EN light/dark. Screenshot in `docs/design/screens/03-directory-views-states/`.
**evidence:** `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-AX\R2-PU-AX-002.png` (Directory page, 390×844, AR light; the «الفلاتر» button opens the bottom sheet).
**what is wrong:** The filter sheet toggle button (shared.jsx:607, `FilterSheet`) has no `aria-expanded`, so a screen-reader user cannot tell whether the filter sheet is open or closed. The button announces only «الفلاتر».
**proposal:** Add `aria-expanded={open}` to the filter toggle button so its expanded/collapsed state is announced.
**why:** An expandable control must expose its current state (WCAG 4.1.2, foundation §10 — every control has a programmatic label/state). Without it, the sheet's state is silent to assistive technology.
**cost:** S
**rule:** foundation §10 accessibility baseline; P5 one filter bar (settled, prototype) — applied but the toggle's state is not exposed.

5. Decisions in doubt

None. All applicable settled decisions (P1, P5, P7, P8, P9, U1–U12, PU-013, PU-024, PU-026, SH-018) were reviewed; the two defects above are failures in applying settled patterns, not disagreements with the decisions themselves.

6. What was not reviewed and why

- Flow length, visual hierarchy and spacing — reviewed under the VD prompt, not this axis.
- Favourites, My reports, Settings, sign-in/register/forgot/reset — account and auth pages are outside the PU public-site scope (Home, Directory, Space details, About, Error only).
- API truth, counts, location privacy, and the privacy-line wording change mandated by 2026-10-13 — reviewed under TR, not AX.
- The `<<<<<<< HEAD` stray line before INDEX.md § 54 — already recorded, not re-reported (prompt note).
- 768 tablet width was checked by code inspection for the public pages; the three public views (list/map at 390 and 1440) were rendered. Contrast values were not re-measured instrumentally — foundation §10 pairs are verified by the design system, and the prototype uses semantic roles only; where a page applies a role correctly it is not re-verified here.
- A screen reader was not available in this session; keyboard navigation and the accessibility tree were used instead.
