## Summary

The visual identity changes from *Sea* (one petrol teal for every role) to **ink + berry spark** ([ADR 0019](docs/architecture/decisions/0019-ink-and-spark-brand.md)):

- **The ink.** A dark slate (the neutral ramp's 900 / 50, in the ink's hue) carries actions, links, focus and structure.
- **The spark.** A berry marks what matters now, sparingly: as fills, edges and marks only, never text, never an action, never destructive.
- **Hover and selected.** Hover becomes a neutral role of its own, apart from selected, which is the spark's tint. A selected item keeps its tint under the pointer.
- **The logo.** «مساحة» over "MASAHA", the ة's dots in the spark, replaces the text wordmark in the site's header, the phone menu, the focus shell and the admin's sidebar.
- **Outside the page.** The browser gets a favicon and a home-screen icon for the first time, and the reset e-mail is drawn in ink.

One PR, so the live site never shows half of each.

The trial's measured criteria are now tests in the token test: contrast on every ground, the fills seen, hover apart from selected, and the brand apart from the destructive red with and without colour blindness. `check:classes` refuses the selected tint used as a hover.

## Scope / Acceptance criteria / Out of scope

**Scope**
- **Tokens:** the neutral ramp in the ink's hue; `spark-*` in place of `brand-*`; the remap; the new roles `primary-hover`, `hover` / `hover-foreground`, `hover-on-muted`, `spark`, `scrim` / `scrim-foreground`; the `skeleton` component token; their utilities (the spark only as `bg-`, `border-`, `outline-` and `fill-spark`); the token test.
- **Components, features and pages:** hover with `hover`, selected with the tint (plus a second mark: the sidebar's 3 px spark bar, the chip's spark edge), controls on a muted ground with the wash, links in running text underlined, the spark marks (the line tabs, the map's selected mark, a lifted item), the skeleton and the photo count.
- **The logo:** a layer component (`display/Logo`), shown in every shell but the owner's and reception's. `SidebarHeader` takes the rail's mark and the full logo.
- **The browser's icons:** `apps/web/public/` (`favicon.svg`, `favicon.ico`, `apple-touch-icon.png`), and their links and `theme-color` in `index.html`.
- **The reset e-mail:** drawn in ink + berry's neutrals.
- **Documents:** `foundation.md` (§3, §4, §5, §11, §12, §15, a new §16 *The logo*), ADR 0019, the map, `setup.md` and `CLAUDE.md` (`check:classes`' third rule), findings 220–225.
- **The prototype:** berry becomes its default; Sea and coral stay behind `?identity=`.

**Acceptance criteria**
- [x] Every role, old and new, resolves in both themes, with key parity (T1–T3).
- [x] The trial's measured pairs hold as tests (T4–T9); the logo's colours are the tokens' (T10); the spark has no text utility (T11).
- [x] No class in `apps/web/src` hovers or highlights with the selected tint (`check:classes`, T12).
- [x] No Sea value is left: no `brand-*` primitive (T3), and no Sea hex in any computed colour of the visual pass.
- [x] Hover and selected differ on every surface the visual pass hovered, light and dark; a control on a muted ground shows its hover in dark.
- [x] Links in running text are underlined; the link Button is underlined at rest (T20).
- [x] The logo is named by the interface's language, decorative where its name is beside it, never mirrored, and ink and spark per theme (T16). It takes the right form per sidebar mode (T17) and appears in each shell (T18, T19).
- [x] `index.html` links the three icons, which exist at their sizes; the SVG switches with the browser's scheme; `theme-color` is set per scheme (T13–T15).
- [x] The reset e-mail draws with exactly the ink + berry colour set, its links underlined (T22).
- [x] The skeleton is ≥ 1.2:1 on its grounds (T6); «+N» keeps 4.5:1 over any photo (T4).
- [x] `foundation.md` and ADR 0019 say what is built; the map lists ADR 0019.
- [x] Every local check and lane is green, the production build and `check:build` are green, and the visual pass is done.

**Out of scope**
- Coral in production; removing Sea or coral from the prototype.
- The README's screenshots (finding 221) and the design archive's `screens/`.
- A web app manifest or PWA; a logo in the e-mail; optimising the logo's paths.
- The owner's and reception's sidebar head (no platform logo there: the owner's decision).
- Google Branding's upload: the owner's steps, after the merge.
- Any change of words, layout or behaviour beyond what the identity needs. No migration, no dependency, no change to `packages/shared` or the API contract.

## Change type

`feat`: the identity, the logo and the browser's icons (web, design system, API e-mail, docs, a build check).

## Evidence — what was run (lint, typecheck, which test lanes) and what was NOT run

Run on the head before the push. Every heavy run went through the item's grant script, one at a time while under 8 GB was free.

**Checks**

| Command | Result |
|---|---|
| `npm run lint` · `npm run typecheck` | Exit 0 on each of commits 1–9. Commits 10–12 change only `docs/`: `git diff --name-only 37ef1039 HEAD -- . ':!docs'` is empty, and neither eslint nor tsc reads `docs/` (their runs were also 0) |
| `npm run format:check` · `check:classes` · `check:links` · `check:conflicts` | 0 · 0 (1989 files) · 0 (3296 links, 226 documents) · 0 |
| `npm run test:unit` | web 197 files / 1385 tests, shared 77 / 924, api 28 / 323, all passed |
| `npm run test:component` | 348 files / 2120 tests, all passed |
| `npm run test:api` (its own test database) | 125 files / 1432 tests, all passed |
| `NODE_ENV=production npm run build` · `npm run check:build` | 0 · 0 |
| The prototype's `check-parse.mjs` · `check-classes.mjs` | 52/52 blocks parsed · 0 new classes. The run was made after the prototype's last change; `docs/design/` is unchanged since |

**Seen failing first, each in its lane**

| Test | Before the change |
|---|---|
| The token test (T1–T11) | 66 failed on *Sea*'s tokens |
| `check:classes`' third rule (T12) | 23 failed before the rule |
| The browser's icons (T13–T15) | 5 failed before `public/` |
| Logo (T16) | Failed to import before the component |
| SidebarHeader (T17) | 2 failed |
| The shells (T18, T19) | 4 failed |
| The link Button (T20) | 1 failed |
| The reset e-mail (T22) | 3 failed |
| The resolver refusing an OKLCH mix | 4 failed on the old `primary-hover` |

**Breaks made, each red, then restored by copy**
- **Tokens:** a wrong transfer function; a hex-only resolver; hover set to the tint; a coral spark; the skeleton on `n-100`; the scrim at 60 %; a paler spark; a leftover `brand-*`; `--color-spark`; a `text-spark` utility; a role missing in dark.
- **Logo:** its name dropped; not hidden; mirrored; the dots on another role; a cropped frame.
- **SidebarHeader:** the mode branch swapped.
- **`check:classes`:** the rule removed; narrowed to `hover:`.
- **Button:** `hover:underline` back; the spark on the outline variant.
- **Shells:** the text wordmark back; the logo unnamed; the «م» tile back; the name read twice.
- **Icons:** a link dropped; the dark rule lost; a 32-only `.ico`.
- **E-mail:** a *Sea* hex; the underline removed.

**The real run: the visual pass in headless Chrome**
- **Coverage:** 390 / 768 / 1440 px, Arabic and English, light and dark. Home, the directory and its map, a space's page, sign-in, register, forgot, the 404, `/me` and the favourites, the phone menu, the desk with its dialogs, Payments, the owner's overview and profile, Finance, the admin's overview, spaces and editor, the rails and drawers, a loading state.
- **No *Sea* value** in any computed colour of any element, pseudo-element or stylesheet.
- **The spark:** no spark text, and no button in the spark except chips that are on (their designed edge).
- **Contrast:** no failure on any painted text.
- **Focus:** the ring visible on the page, a card, the sidebar, a Sheet and a dialog.
- **Hover vs selected:** told apart on every surface hovered with a real pointer, light and dark; selected keeps its tint under the pointer.
- **The logo:** 110 × 40 / 99 × 36 / 36 × 36, untransformed, named once. Its mark at 64 px matches the owner's file pixel for pixel.
- **The 360 px header** fits in both languages.
- **The icons:** served with their types in the dev server and in `vite preview` of the build; Chrome takes the SVG, and it switches with the browser's scheme.
- **The prototype** (berry by default) paints the same colours as production.
- **The status colours** are unchanged.
- **Fixed after the pass, each folded into its commit and re-checked in the browser:**
  - The ink's and the secondary button's hovers mix in OKLab: in OKLCH, Chrome drops a near-grey's hue and painted them warm. The token test now refuses OKLCH.
  - A lifted photo's spark edge is drawn inside the picture, which the tile's frame clipped.
  - The phone menu's current page takes the selected tint, apart from the hover.
  - The neutral live-status trigger gets a hover that shows in dark.
- **Recorded as findings:** the older defects it met (222–224) and a test-timing gap (225).

**The first download** grows by 15,672 bytes (+8,079 compressed), the logo's paths in the layer's chunk, against `main`'s 1,105,713 (`check:build` has no size budget).

**Not run, and why**
- **E2E smoke:** an end-of-project lane.
- **Touch-sized controls:** the 390 px pass used a desktop pointer.
- **The demo photos** answer 404 in this folder's local storage, so photo grounds were placeholders (the «+N» scrim is proven by the token test over white and black).
- **The production check after the merge,** that the deployed `/favicon.svg` answers `image/svg+xml`, is the owner's.
- **Interruptions:**
  - The first full `test:api` was cut by the machine's restart; the re-run above is green.
  - A per-commit loop was stopped once for low memory; it is accounted for above.

## Screenshots — for UI changes: RTL and LTR, light and dark, phone and desktop

The visual pass's curated shots (RTL and LTR, light and dark, 390 / 768 / 1440, the hover set, the rails and drawers, the logo close up, the icons, and each finding's before and after) are in the owner's `Downloads\identity-prod-shots\` folder, to be attached by the owner. They are not committed.

## Definition of Done checklist

- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean on every commit; build passes.
- [x] Tests added in the owning lane (unit: tokens, `check:classes`, the browser's icons, the e-mail; component: Logo, Sidebar, Button, the shells), each seen failing first and its break made.
- [x] No hardcoded user-facing text: no catalogue line changed; the showcase's samples are in both languages.
- [x] UI checked in RTL and LTR, light and dark, phone and desktop (the visual pass, in headless Chrome).
- [x] Authorization: no protected action is touched.
- [x] Triggered documentation updated in this PR (`foundation.md`, ADR 0019, the map, `setup.md`, `CLAUDE.md`, the findings, the design archive). No deferred document's trigger is met.
- [x] Each fact has one home; nothing claimed that is not built.
- [x] Every claim names the test or command that proves it (Evidence).
- [x] Atomic history (12 commits, 81 files), pushed, description complete.

This PR touches more than 25 files and changes a build check (`check:classes`), so its review is a separate conversation (workflow §2, phase 7).
