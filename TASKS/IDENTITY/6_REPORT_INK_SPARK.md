# IDENTITY — "ink + spark" trial, report (2026-11-11)

**Status: built, looked at and checked. Nothing committed, staged or pushed.** Both candidates the owner kept, slate-coral and slate-berry, pass every measured criterion. The owner removed warm charcoal ink + coral spark on 2026-11-11; it is gone from the stylesheet, the switch and the docs. Commit, push or PR only on the owner's word.

- **Worktree:** `C:\c\dev\masaha\app-identity`. That is the path git lists; the prompt's `C:\dev\masaha\app-identity` does not exist.
- **Branch:** `design/ink-spark`, from `7fb73c3c` (main).
- **Plan:** `5_PLAN_INK_SPARK.md`.

## Serve and look

```
cd C:\c\dev\masaha\app-identity\docs\design\prototype
python -m http.server 5402
```

(It is running now from this session, bound to 127.0.0.1.) Without `?identity=`, every page is *Sea*, unchanged. The parameter is carried on every link, like `lang` and `theme`.

| Candidate | Ready URLs (dark, English) |
|---|---|
| slate-coral | http://127.0.0.1:5402/Home.html?identity=slate-coral&theme=dark&lang=en · http://127.0.0.1:5402/Owner%20overview.html?identity=slate-coral&theme=dark&lang=en · http://127.0.0.1:5402/Directory.html?view=map&selected=focus&identity=slate-coral&theme=dark&lang=en |
| slate-berry | http://127.0.0.1:5402/Home.html?identity=slate-berry&theme=dark&lang=en · http://127.0.0.1:5402/Owner%20overview.html?identity=slate-berry&theme=dark&lang=en · http://127.0.0.1:5402/Directory.html?view=map&selected=focus&identity=slate-berry&theme=dark&lang=en |

## Measured numbers

The ramps come from the palette lab's own engine (`makeRamp`, `makeNeutral`). ΔE is OKLab distance. CVD is the Machado 2009 simulation at severity 1.0, and the CVD figure is the lower of protan and deutan.

Criteria:
- foundation §5's pairs on the remap, 66 per theme;
- ink against the destructive red: ΔE ≥ 0.10, and ≥ 0.08 under protan and deutan;
- the spark ≥ 3:1 on every ground it sits on;
- red-400's hue stays at 15–45° in dark.

| | slate-coral | slate-berry |
|---|---|---|
| Ink | neutral h255 c0.030 | neutral h250 c0.014 |
| Spark seed | #C2492F | #A149A0 (h328) |
| Ink, light / dark | #151F2C / #F7FBFF | #1A1F25 / #F7FBFF |
| Spark, light / dark | #D2573D (500) / #FEA793 (300) | #B55BB3 (500) / #D27ED0 (400) |
| §5 pairs, light · dark | 66/66 · 66/66 | 66/66 · 66/66 |
| Ink↔red ΔE, light (protan, deutan) | .353 (.193, .326) | .346 (.190, .319) |
| Ink↔red ΔE, dark (protan, deutan) | .329 (.365, .278) | .329 (.365, .278) |
| Spark's lowest contrast, light · dark | 3.63 · 7.00 | 3.70 · 4.77 |
| Text on spark fill (n-950), light · dark | 4.63 · 9.99 | 4.58 · 6.84 |
| Red-400 in dark | h25.0 c0.175 (unchanged) | same |
| **Result** | **PASS** | **PASS** |
| *Added:* spark↔red ΔE (CVD), light · dark | .099 (.089) · .121 (.096) | .191 (.184) · .156 (.154) |
| *Added:* spark tint↔destructive-subtle, dark (CVD) | **.079 (.077)** | .110 (.104) |

*Sea*, for comparison: its tint is 0.154 from destructive-subtle in dark (0.093 CVD).

Neither candidate failed a criterion.

## What was built (only `docs/design/`)

**`masaha/identity-ink-spark.css` (new).** It does nothing unless `<html data-identity>` is set.
- Per candidate it sets three ramps: the neutral ramp in the ink's hue, a spark ramp, and `brand-*` mapped to the spark ramp, so no Sea teal can be left over.
- Remap, both themes:
  - `primary`, `ring` and `sidebar-ring` = ink;
  - `accent` and `sidebar-accent` = a spark tint (50 / 900) with ink text;
  - `sidebar-primary` and `chart-1` = the spark.
- Destructive, success, warning, info and their subtle pairs are unchanged.

**`masaha/i18n.js`.** Reads `?identity=` against the list of two, sets `data-identity` and carries it on links. No value, or an unknown one, gives *Sea*.

**Pages.** The stylesheet is linked last on the 38 app pages and the 5 `_*head.txt` templates. Four pages load neither `i18n.js` nor `masaha.css` and stay out: the two iframe boards, the reset e-mail and the Wordmark sheet.

**`data-brand-mark`.** Added to the header word in `shared.jsx` (2), `auth.jsx` and `Change password.html`, and to the admin's «م» tile in `admin.jsx`. These are data attributes, so no new class is needed.

**Where the spark shows:**
- the sidebar's current item (tint, plus a 3px bar at the inline start) and its count badge;
- a selected filter chip (tint and a spark edge);
- the line tabs' indicator;
- `primary` badges and today's row;
- the selected map pin's ring;
- the sortable item while dragged over or lifted (checked live: `#B55BB3`, 2px and 3px);
- `tone-primary` covers;
- the brand mark: the word stays ink with a spark dot, and the «م» tile is a spark fill.

**Where it never shows:**
- action buttons: the primary is ink, and the hover tint inside any button or action menu is re-scoped to neutral (the count badge inside «Filters» is neutral for the same reason);
- small text: there is no spark text anywhere;
- destructive.

Links in running text are ink and underlined.

**Two fixes the remap needed:**
- The bundle's primary hover mixes `primary` with `foreground`. Under ink those are the same colour, so the hover disappeared. Under the trial the hover mixes toward `background`; text on it stays at 4.5:1 or better in both themes.
- In dark slate-coral the drawn covers turned purple. `masaha.css` mixes the tones in OKLCH, and the hue path from peach (h≈35) to the slate-blue card (h≈255) runs through violet. Under the trial the covers mix in OKLab.

**Docs:** `CHANGES.md` has «Identity trial — ink + spark (2026-11-11)», marked as a trial that is not adopted. `INDEX.md` has a row for `?identity=`.

## Look and check

**Matrix:** for the two candidates, 10 screens × 390/1440 × ar/en × light/dark = 160 shots. Each shot was checked automatically:
- console errors and exceptions;
- any Sea-teal computed colour, shadow or fill;
- `data-identity` present and carried by `carryParams`;
- page overflow;
- the focus outline after three real Tab presses, ≥ 3:1 against its ground.

The 10 screens: Home, Directory (cards with chips selected), map with a selected pin, Space details, Desk, a check-in warning dialog, the «إلغاء الدفعة» void dialog on `Payments.html` (owner, row «⋯»), Owner overview, Owner space profile, Admin spaces.

**Sea control:** 24 shots of Home, Owner overview and the map without the parameter. It shows teal everywhere and no `data-identity`, which proves both that the detector works and that the default is untouched.

**Result:** 0 findings caused by the trial.

**Re-shot screens:**
- The first Home shots got `ERR_CONNECTION_REFUSED`: four Chromes started at once against Python's server. Re-shot with staggered starts.
- The void shots are re-shot with a retry until the alert dialog is open (all 16 opened).
- Dir, details and profile are re-shot after the OKLab cover fix.

**Screenshots:** 39 curated, in `C:\Users\basel\Downloads\identity-shots\`:
- 18 per candidate, one folder each;
- 3 in `sea-control`.

The removed candidate's 18 shots are still in their own folder there; I did not delete them, and will on the owner's word.

The full matrix is in the session's scratchpad: `…\scratchpad\shots`, `shots2` and `shots3`. Nothing is in the repository.

**Checks:**

```
node docs/design/scripts/check-parse.mjs     → 52/52 blocks parsed, from 42 pages and the modules
node docs/design/scripts/check-classes.mjs   → 361 classes used, 5 dead uses (all known), 0 new
check:links (apps/api/scripts/checkLinks.ts) → 3260 links in 215 documents and 2623 source files all resolve.
check:conflicts                              → No conflict markers found.
```

## Findings (recorded, not acted on)

1. **Coral's tint in dark reads as the error tint.** The spark-900 tint is ΔE 0.079 from destructive-subtle, against Sea's 0.154. In dark, «شهري» and «الغلاف» badges and the current sidebar item look like a red badge; the words still say what they are (status is never colour alone). In light every 50-step tint is near-white (Sea's own is 0.029), so the badge text carries the difference there. This affects slate-coral; berry is clear at 0.110. If the owner chooses coral, I propose a desaturated dark tint, such as spark-900 mixed toward neutral-800.
2. **Coral spark vs red** is 0.099 in light (0.089 CVD), just under the 0.10 used for ink. That is acceptable only because the spark never marks an action or a state. Dark coral had to use step 300: step 400 measured 0.036 from red-400 (0.005 CVD), which is the same colour.
3. **Pre-existing, not the trial:** on the Directory's map at 390, the first Tab lands on a `span` with no visible focus outline. Sea does the same (seen in the control).
4. **The map drawing** mixes `primary` into its land and blocks. Under ink, the dark map's blocks are light grey, not tinted. It is a stand-in drawing, so it is left as is.

## Proposed alternatives

1. **Wordmark in spark.** WCAG exempts logotypes, but heading-3 is 17px/600, so "never small text" wins here. The logo step could make a spark word at 24px or larger.
2. **Spark↔red as a recorded criterion**, ≥ 0.08 under CVD, for any spark. That guard is what set dark coral to step 300.
3. **A separate neutral `hover` role in production**, with `accent` kept for selections. The trial re-scopes `accent` inside buttons and menus to get the same result.
4. **Dark accent at spark-900, not 950.** The plan named 950, but 950 is barely visible on n-950. 900 matches what Sea does with `b-900`, and both pass.

## Next (the owner)

The owner chooses slate-coral or slate-berry, or rejects the idea. If one is chosen, the next steps are, in order:
1. a `foundation.md` change (a new spark role), for approval;
2. the logo in ink + spark;
3. the production tokens.

The commit, when asked for, is one Conventional commit staged by path, for example `feat(design): try an ink + spark identity in the prototype`.

## Round 3 — the logo (2026-11-11)

**Files.** The owner's 10 SVGs are copied unchanged from `TASKS\LOGO\wordmark\final-trace\` into `docs/design/prototype/masaha/logo/`, five per identity. Before copying, I checked that they contain only paths: no script, image, text or external link. Their colours are exactly each candidate's ink and spark. The app icons are copied but not used: nothing in the prototype shows an app icon.

**Where the logo shows** (only with `?identity=`; *Sea* is untouched):
- **Site header, phone drawer title, Sign in and the other auth pages:** the full logo, 40 px tall (110 × 40), light or dark by theme. The words «مساحة» / "Masaha" stay inside the element, transparent, so the element keeps its name for screen readers in each language.
- **Admin sidebar:** the full logo replaces the «م» tile (99 × 36). The word «مساحة» beside the tile is now `data-brand-mark="name"`: hidden on screen, kept for screen readers. The caption «إدارة المنصة» stays.
- **The 768 rail:** the small mark (36 × 36).
- **Phone drawer:** the full logo.
- **Browser tab:** the identity's small mark, chosen in `i18n.js`. It follows the browser's own colour scheme, light or dark, not the page's theme, because the tab is the browser's.

**Hooks.** Everything goes through `data-brand-mark`. There is one new value, `name`, and no new class; the layout is in `identity-ink-spark.css`.

**Not changed, for the owner to decide.** Desk and Owner overview use the owner/reception shell, whose sidebar header is the space switcher (SH-006). It has no platform brand mark to replace, so it shows no logo. Adding one would change that shell's layout, so I did not do it without a decision.

**Look and check.** 128 shots, one Chrome at a time (the machine had about 1 GB of memory free):
- **Main set:** Home, Directory, Desk, Owner overview and Sign in, for both identities, at 390 and 1440, in Arabic and English, light and dark: 80 shots.
- **Admin spaces:** at 390, 768 and 1440: 24 shots.
- **Sea control:** 24 shots.

**Results:**
- No errors, no leftover teal, focus rings fine, no overflow.
- Every page with a brand mark shows the right file for its identity and theme.
- One Sign in shot was read before the logo had drawn; its screenshot shows the logo.
- The control shows `favicon.svg` and no logo.
- The admin's phone drawer, opened, shows the full logo.

**Checks:**
- `check-parse`: 52/52 blocks parsed.
- `check-classes`: 0 new.
- Links: 3260 resolve.

**Screenshots:** 25 more, in `Downloads\identity-shots\`:
- `logo-slate-coral`: 11
- `logo-slate-berry`: 12, including the open phone drawer
- `logo-sea-control`: 2

**Ready URLs** (`python -m http.server 5402` in `docs/design/prototype`):
- slate-coral:
  - http://127.0.0.1:5402/Home.html?identity=slate-coral&theme=dark&lang=en
  - http://127.0.0.1:5402/Sign%20in.html?identity=slate-coral&theme=dark&lang=en
  - http://127.0.0.1:5402/Admin%20spaces.html?identity=slate-coral&theme=dark&lang=en
- slate-berry:
  - http://127.0.0.1:5402/Home.html?identity=slate-berry&theme=dark&lang=en
  - http://127.0.0.1:5402/Sign%20in.html?identity=slate-berry&theme=dark&lang=en
  - http://127.0.0.1:5402/Admin%20spaces.html?identity=slate-berry&theme=dark&lang=en

## Round 4 — the final review (2026-11-11)

**Status: done; nothing committed, staged or pushed.** Berry (`slate-berry`, adopted as I4) came first. Coral got the same rules and a lighter look at the pages. Everything changed is under `docs/design/`, and the trial is still 51 paths in `git status`, the same as before.

### Part A — light mode and hover

**What changed** (only in `identity-ink-spark.css`, and only under `html[data-identity]`):
- **Hover is its own role.** A new trial token, `--hover`, is never the spark:
  - light: `neutral-200`;
  - dark: `muted`, unchanged.
- **Hover on a muted track.** `--hover-on-muted` is an ink wash, 10% in light and 8% in dark. It is used where an opaque fill would vanish: the desktop tabs (the bundle gave them no hover fill) and the Directory's subscription choice.
- **Where `--hover` now applies.** Every hover the bundle draws with `accent` or `sidebar-accent` takes it:
  - buttons, including their open state;
  - menu, select and combobox items;
  - table rows, including the row whose menu is open;
  - cards, chips, the phone's tab pills, sort headers and input actions;
  - sidebar items and the owner's switchers.
- **Selected keeps its tint under the pointer.** That covers a chip that is on, today's row and the current sidebar item.
- **Selected (the spark tint, `accent` / `sidebar-accent`):**
  - light: `spark-100`;
  - dark: `spark-900` lifted 30% toward `spark-800`.
- The 3 px spark bar on the current sidebar item stays.

**Before → after.** WCAG contrast of the fill against its ground, light / dark. Measured from the tokens, then checked live with a real mouse hover in headless Chrome: the painted values matched.

| Pair | berry before → after | coral before → after |
|---|---|---|
| hover on card, light | 1.11 → **1.27** | 1.12 → **1.28** |
| hover on background, light | 1.07 → **1.22** | 1.08 → **1.23** |
| hover on a muted track, light (tabs, subscription) | 1.00 → **1.21** | 1.00 → **1.21** |
| hover on card / background, dark | 1.26 / 1.44, unchanged | 1.26 / 1.43, unchanged |
| hover on a muted track, dark | 1.00 → **1.27** | 1.00 → **1.27** |
| selected on card, light | 1.08 → **1.19** | 1.07 → **1.18** |
| selected on background, light (the chip, which also has its spark edge) | 1.04 → 1.14 | 1.03 → 1.14 |
| selected on card, dark | 1.14 → **1.23** | 1.14 → **1.24** |
| selected on background, dark | 1.29 → 1.39 | 1.29 → 1.40 |
| hover vs selected, light (they also differ by hue: grey vs tint) | 1.03 → 1.07 | 1.04 → 1.08 |
| hover vs selected, dark | 1.11 → 1.03 (same lightness, different hue) | 1.10 → 1.02 |
| foreground on hover, light | 14.93 → 13.03 | 14.86 → 13.01 |
| muted-foreground on hover, light (the space card's text) | 5.39 → **4.71** | 5.37 → **4.71** |
| sidebar-foreground on hover, light | 7.59 → 6.62 | 7.55 → 6.62 |
| foreground / muted-fg on selected, light | 15.37 / 5.55 → 13.94 / 5.04 | 15.47 / 5.60 → 14.06 / 5.08 |
| foreground / muted-fg on selected, dark | 14.05 / 5.93 → 13.01 / 5.50 | 13.97 / 5.87 → 12.93 / 5.44 |
| foreground on hover-on-muted, light · dark | — → 12.31 · 9.90 | — → 12.25 · 9.94 |
| spark bar on the selected tint, light · dark (≥ 3) | 3.81 · 5.31 → 3.45 · 4.92 | 3.78 · 7.72 → 3.44 · 7.15 |
| selected tint vs destructive-subtle, dark (OKLab ΔE) | 0.11 → 0.13 | **0.079 → 0.10** |
| selected tint vs destructive-subtle, light (ΔE) | 0.02 → 0.05 | 0.00 → 0.03 |

Every hover now lands at 1.21–1.28 on every surface in light. Every text pair on it keeps 4.5:1 or better; the lowest is muted-foreground at 4.71.

Hover and selected are told apart by:
- **hue:** a neutral grey against the berry tint, ΔE 0.05 in light and 0.08 in dark;
- **a second mark:** the sidebar bar or the chip's spark edge.

Today's row and the `primary` badges carry the tint alone. That is acceptable, because they are never hovered as actions.

**The light pass (A.4)**, same in both candidates within 0.02:

| Pair | light | dark |
|---|---|---|
| border / divider on card | 1.27 | 1.26 |
| card border on background | 1.22 | 2.23 |
| card fill on background (the border and the raised shadow carry it, as in Sea) | 1.04 | 1.13 |
| input border on card · background (≥ 3) | 4.17 · 4.01 | 3.98 · 4.51 |
| disabled text and buttons (50%) on card | 3.24 | 4.96 |
| focus ring (ink) on background, card, muted, selected tint, hover | 13.0–16.6 | 12.6–18.1 |

Inputs show focus as a 2 px ink outline on their group (checked live, with a screenshot). The input element itself has no outline, so my matrix's "no outline" flags on inputs were false.

**Hover shots** (1440, light, Arabic; berry and coral; 12 files) are in `Downloads\identity-shots\hover-*`:
- the Desk table row;
- a sidebar item, beside the current one;
- an outline button;
- a menu item;
- the Directory's chip, with the selected chip beside it;
- the segmented tabs.

The Directory's only chips are the list/map toggle; its filters are checkboxes and the subscription choice.

### Part B — the review

**How it was looked at:**
- **berry:** all 38 app pages, plus 8 states (the map with a pin selected, the Desk's check-in dialog, the «إلغاء الدفعة» dialog `Payments.html?void=1`, the profile's Sheet `?sheet=hours`, the admin's Sheet, signed-in Home, a loading table, reception's Desk), at 390, 768 and 1440, in Arabic and English, light and dark: **552 loads**;
- **coral:** the same at 390 and 1440: **368 loads**.

Each load checked:
- errors;
- the identity and its carry on links;
- leftover Sea teal;
- page overflow;
- the contrast of every visible text against its painted ground (45,047 text elements in berry);
- spark-coloured text;
- the spark on any action;
- the side of the sidebar's bar;
- the logo (file, size, transform, name);
- the status colours;
- the focus ring after three Tabs.

Then I looked at about 25 screenshots by eye. Separately:
- the phone drawers, the 768 rail and the tab's icon got their own probe;
- for Sea, 7 pages × 3 views were compared pixel by pixel against `main`'s prototype.

| # | Check | Result |
|---|---|---|
| 1 | Colour roles | **Passed.** Ink on every action. No spark text anywhere (0 in 920 loads). No spark on any action (0). No Sea teal left (0). Status colours identical in every load: light `#BE222A #137D41 #B27406 #1F6CB0`, dark `#FC6E68 #63B77C #D6912B #64A6E9`. The spark is on the current item and its bar, the count badge, the selected chip and its edge, `primary` badges, today's row, the selected pin, the line tabs and the covers. **Fixed:** the selected chip's spark edge was dead (below). |
| 2 | Contrast | **Passed.** The pairs are in the tables above. In the page scan nothing fails because of the trial. The scan flagged two things, both outside the trial: the photo strip's «+1» (white on a 55% scrim over a photo, 3.64; identical pixels in Sea, so it predates the trial; *for the owner*), and disabled pagination and «إضافة سعر» at 3.21–3.26 in light (disabled controls are exempt; still readable). |
| 3 | States | **Fixed** hover and selected (part A). Focus-visible is ≥ 12.6 on every surface. Inputs have a 2 px outline. Active/pressed are distinct: an ink pill or a raised card on the segmented control, a tint plus spark edge on chips. Disabled is 50%. Loading: the skeleton is `muted` on the card, 1.11, as faint as hover was. It is identical in Sea, so it is *for the owner* (below). |
| 4 | The logo | **Passed; fixed one.** The right file in every load, per identity and theme: header, auth pages, the site drawer, the admin's sidebar and drawer (99 × 36), and the 768 rail (the 36 × 36 mark). The tab's icon follows the browser's own scheme. Logos are never mirrored (`transform: none`), never cropped. The accessible name is «مساحة» / "Masaha" (the element's own text, transparent; the admin's name is kept visually hidden). **Fixed:** in the phone drawer the logo was centred in a stretched title while the items start at the inline start (below). Clear space in the 56 px header is 8 px above and below; the viewBox is tight to the drawing. |
| 5 | Layout and RTL | **Passed.** 0 overflow in 920 loads. The sidebar's bar is at the inline start in every load (right in Arabic, left in English). Chevrons and arrows are mirrored. The logo is not. |
| 6 | Today's identity untouched | **Passed.** Without `?identity=`, 20 of 21 views are pixel-identical to `main`'s prototype (main has no prototype change since this branch). The 21st, Sign in at 1440, differed by 667 pixels on the first load only: the font loading, which is identical when loaded again. |
| 7 | The code | **Fixed.** Every rule is under `html[data-identity…]`, and every selector exists in the markup or the bundle. There are no new classes (0 new). Changes: the dead `[data-on]` selector; the new hover rules, which use the bundle's real states (`[data-state=on/active/open]`); the drawer logo; and comments saying why. `CHANGES.md`, `INDEX.md` and the stylesheet's header now say that berry is adopted and coral is kept to compare; `CHANGES.md` has a row for round 4's hover and selected. |

**Defects fixed:**
1. **The selected chip's spark edge never showed.** The rule used `[data-on]`, but the bundle compiles `data-on:` to `[data-state=on]`, so the edge stayed ink. It now shows (seen in the shots).
2. **Hover and selected were the same colour almost everywhere.** Table rows, cards, chips, the phone's tab pills and select or combobox items hovered with the spark tint (`accent`), so a hovered row looked selected. They now take the neutral hover fill.
3. **The phone drawer's logo was centred.** A stretched title drew it in the middle while the items start at the inline start. The word mark's width is now capped at the logo's own (110 px), so it sits at the start.

**For the owner:**
1. **The skeleton (loading) is faint**: 1.11 on the card in light, the same weakness as hover had. It is identical in Sea. One line would give it `--hover` (1.27). I did not change it, because it is Sea's own look, not the trial's.
2. **The photo strip's «+1»** is white on a 55% scrim over the photo: 3.64 at 17 px, which needs 4.5. Pixels are identical in Sea, so it predates the trial. A darker scrim, about 70%, would fix it; it lives in `masaha.css`.
3. **Coral only: its dark tint is still close to the error tint.** It is now ΔE 0.10, up from 0.079, but the current item and the «شهري» badges still read rust-red in dark (see `final-slate-coral/01`). Berry is 0.13.
4. **The map drawing's land is tinted by the spark** (pink in berry). It is a stand-in drawing, so I left it. Production uses a real map.
5. **The owner and reception shell still has no platform logo** (round 3, SH-006). It is unchanged and needs a decision.

**Left as is, with reasons:**
- **Light hover vs selected differ by 1.07 in contrast.** The difference is hue plus a second mark; a stronger tint (spark-200) would drop muted-foreground on it to 4.18.
- **The map's first Tab lands on a `span` with no outline.** It is pre-existing, as round 1 found.
- **Sea's own 1.11 hover** is untouched, because Sea must stay as it is.

**Screenshots** in `C:\Users\basel\Downloads\identity-shots\`:
- `hover-*`: 12;
- `final-slate-berry`: 25, including the fixed drawer, the admin's drawer and the focused input;
- `final-slate-coral`: 6, where coral differs;
- `final-sea-control`: 3.

The full matrix (920 + 21 shots and their JSON) is in this session's scratchpad (`…\ae7581d8-…\scratchpad\mB`, `mC`, `seaC`). Nothing is in the repository.

**Checks:**
- `check-parse`: 52/52 blocks parsed.
- `check-classes`: 361 used, 5 dead (all known), 0 new.
- `check:links`: 3260 resolve.
- `check:conflicts`: none.

**Ready URLs** (run `python -m http.server 5402` in `docs/design/prototype`; I stopped my server):
- berry:
  - http://127.0.0.1:5402/Desk.html?role=reception&identity=slate-berry
  - http://127.0.0.1:5402/Directory.html?loc=none&identity=slate-berry
  - http://127.0.0.1:5402/Owner%20overview.html?identity=slate-berry&theme=dark
- coral:
  - http://127.0.0.1:5402/Desk.html?role=reception&identity=slate-coral&theme=dark
