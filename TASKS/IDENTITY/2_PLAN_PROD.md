# IDENTITY — ink + berry and the logo in production — the plan

> **For:** a fresh executor session (Claude Code, Opus 5.5, effort xhigh) in `C:\dev\masaha\app-design`.
> **Planned:** 2026-11-12, on `main` `f0709d28`, with #143 (`feat/space-profile`, head `29a25054`) read as if merged.
> **Prompt:** `C:\dev\masaha\workspace\TASKS\IDENTITY\1_PLAN_PROMPT_PROD.md`. **Saved to:** `…\TASKS\IDENTITY\2_PLAN_PROD.md`.
> Every decision is taken here, except the `OD`s (§14), which the owner answers. What reading could not settle is an
> executor check (`EC`, §12). Nothing was built, rendered or run to write this plan.

---

## 1. Summary

The visual identity changes from *Sea* (a petrol teal that carried every role) to **ink + berry spark** (ADR 0019,
new): a dark **ink** (the neutral ramp's 900 / 50, in the ink's hue) carries actions, links, focus and structure; a
warm **berry spark** marks *what matters now* — sparingly, as fills, edges and marks, never as small text, never on an
action, never destructive. **Hover becomes a role of its own** (neutral), apart from **selected** (the spark's tint),
told apart by hue and, where the trial gives one, a second mark. The **logo** («مساحة» over "MASAHA", the ة's two dots
in the spark) replaces the text wordmark in the site's header, the phone menu, the focus shell, and the admin's
sidebar (the small mark on its rail); the browser gets a **favicon and a home-screen icon** for the first time; the
**reset e-mail** loses Sea's hexes; the **skeleton** and the photo grid's **«+N»** reach their contrast. One PR, so the
live site never shows half of each.

---

## 2. The contract

### Scope
1. **Tokens** (`apps/web/src/shared/design-system/tokens/`): the neutral ramp in the ink's hue; a `spark-*` ramp in
   place of `brand-*`; the remap (§5); new roles `hover`, `hover-foreground`, `hover-on-muted`, `primary-hover`,
   `spark`, `scrim`, `scrim-foreground`; a `skeleton` component token; their utilities; the token test extended.
2. **The layer's components** draw hover with `hover`, selected with `accent`, the selected's second mark and the
   other spark marks with `spark`, the primary's hover with `primary-hover`, and controls on a muted ground with
   `hover-on-muted`. Links in running text are underlined.
3. **Features and pages** follow the same rules (card hovers, links, #143's sortable marks, contact tiles, «+N»).
4. **The logo** as a layer component (`display/Logo`), shown in every shell but the owner's and reception's (OD3).
5. **The browser's icons**: `apps/web/public/` (new) with `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`; the
   links and `theme-color` in `apps/web/index.html`.
6. **The reset e-mail** (`apps/api/src/modules/auth/email/resetEmail.ts`) in ink + berry's neutrals.
7. **Documents:** `foundation.md` (§3, §4, §5, §11, §12, §15, a new §16 *The logo*), ADR 0019, the map,
   `setup.md` and `CLAUDE.md`'s line on `check:classes` (SD2), finding 219; the design archive if OD5 (a).
8. **The prototype** (OD5 (a)): berry becomes its default; Sea and coral stay behind `?identity=`.

### Acceptance criteria
- [ ] Every semantic role, old and new, resolves to a colour in both themes; key parity holds (T1–T3).
- [ ] The trial's measured pairs hold as tests, each failing below its threshold (T4–T9); the logo's colours are the
      tokens' (T10); the spark has no text utility (T11).
- [ ] No class in `apps/web/src` hovers or highlights with the selected tint (`check:classes`, T12 — SD2).
- [ ] No Sea value is left: no `brand-*` primitive (T3), no Sea hex in any computed colour of the visual pass (§13).
- [ ] Hover and selected differ on every surface the visual pass hovers, light and dark; a control on a muted ground
      shows its hover in dark (D1).
- [ ] Links in running text are underlined; the link Button is underlined at rest (T20).
- [ ] The logo: named «مساحة» / "Masaha" by the interface's language, decorative where its name is beside it, never
      mirrored, ink and spark per theme (T16); the right form per sidebar mode (T17); in each shell (T18, T19).
- [ ] `index.html` links the three icons, which exist at their sizes, the SVG switching with the browser's scheme;
      `theme-color` per scheme (T13–T15).
- [ ] The reset e-mail draws with exactly the ink + berry colour set, its links underlined (T22).
- [ ] The skeleton is ≥ 1.2:1 on its grounds (T6); «+N» keeps 4.5:1 over any photo (T4).
- [ ] `foundation.md` and ADR 0019 say what is built and nothing more; the map lists ADR 0019.
- [ ] Every local check and lane green, `NODE_ENV=production` build + `check:build` green, the visual pass done (§13).
- [ ] One PR, CI green on its pushed head, GitHub `CLEAN`.

### Out of scope
- Coral (`slate-coral`) in production; removing Sea or coral from the prototype.
- The README's screenshots (finding 219); the design archive's `screens/` (regenerated at the end of the fix phase,
  as `docs/design/README.md` says).
- A web app manifest, a PWA, a logo in the e-mail (PA3, PA7); optimising the logo's paths (PA4).
- The owner's and reception's sidebar head (unless OD3 (b) or (c)).
- Google Branding's upload (the owner's steps, §16) — no code.
- Any change of words, layout or behaviour beyond what the identity needs; finding 215 (the prototype's Home).
- No migration, no dependency, no change to `packages/shared` or the API contract.

---

## 3. The reading done

- `CLAUDE.md`; `docs/development/workflow.md` whole; `engineering-principles.md`; `testing.md`;
  `docs/architecture/documentation.md` (§5–§9); the map `docs/README.md`; the findings index (open titles; 5, 19, 215
  opened); ADR 0005, 0011 (style); `docs/frontend/design-system/foundation.md` **whole**; `docs/frontend/architecture.md`
  (§1–§2, the site and dashboard shells); `docs/design/README.md` (*Rules for implementing*), `docs/design/CHANGES.md`
  («Identity trial — ink + spark»), `INDEX.md`'s `?identity=` row, `SCREENS.md`; `docs/development/setup.md` (demo
  data, *Running a second folder*, the commands table); `docs/features/users.md` (the forced change's header).
- The prototype at `main`: `masaha/identity-ink-spark.css` (every rule), `masaha/i18n.js`, the `data-brand-mark` hooks
  (`shared.jsx`, `auth.jsx`, `admin.jsx`, `Change password.html`), `masaha/logo/` (each file's structure: the full
  logo is two paths, ink 13 166 chars + spark 1 150 chars, viewBox `263 45 2473 903`; the mark is the same ink path
  clipped twice — one copy mirrored inside the drawing, `translate(1158 0) scale(-1 1)` — and the dots moved 11.5;
  the app icon is the mark on a white `rx 170` tile).
- The workspace: `0_OWNER_DECISIONS.md`, `4_PLAN_INK_ACCENT.md`, `6_REPORT_INK_SPARK.md` (rounds 1–4),
  `7_REVIEW_FINAL.md`; `TASKS\LOGO\LOGO_NOTES.md` (Axes 3, 5, 6; from «The symbol dropped» on), `LOGO_DECISION.md`
  (rules of use only).
- The code at `main`: `tokens/*` (`primitives.css`, `semantic.css`, `tailwind.css`, `themes.ts`,
  `semantic.unit.test.ts`), `lib/cn.ts`, `leaflet.css` and its test; every use of `accent`, `sidebar-accent`,
  `primary`, `ring`, `sidebar-*`, `chart-1`, `color-mix` and `hover:` across `apps/web/src` (§7); Button, Calendar,
  DropdownMenu, Select, Combobox, Table, DataTable, Input, ToggleGroup, Tabs, SegmentedControl, Sidebar, FilterTag,
  Skeleton, Sortable; the shells (`SiteHeader`, `SiteMenu`, `FocusLayout`, `AdminLayout`, `SpaceLayout`, `SpaceHead`),
  every user of `copy.site.wordmark`; `apps/web/index.html` (no favicon, no `public/`); `vite.config.ts`;
  `scripts/checkBuild.ts`, `checkClasses.ts`, `contentSecurityPolicy.unit.test.ts`; `vercel.json` (CSP:
  `style-src 'self' 'unsafe-inline' …`, `img-src 'self' …`); the showcase (`registry.tsx`, `SidebarSection`,
  `SortableSection`, `ShowcaseNav`, `FieldSection`); the API's `resetEmail.ts` and its test.
- #143's diff (`git diff origin/main...origin/feat/space-profile`): its uses in `ContactsSheet`, `ContactsView`,
  `PhotosEdit`, `PhotosView`, `HoursView`, `AmenitiesSheet`, `ProfileHeader`; it takes finding 216 and changes
  `foundation.md` (§3 and the Sortable row), the icons and the layer's index, `architecture.md`, `routes.component.test.tsx`.
- Google's help page *Manage OAuth App Branding* (logo: square 120 × 120, ≤ 1 MB, JPG / PNG / BMP; a new logo on a
  production external app needs verification first; branding cannot be edited while it runs).
- Next free numbers: **ADR 0019**, **finding 219** (217 and 218 exist; #143 takes 216), **PR #144** (the last issue/PR
  is #143). Re-checked by EC1.

---

## 4. The owner's decisions — binding (word for word from the prompt)

- **I1 — ink + spark:** a dark **ink** for actions and structure, a warm **spark** for "what matters now", sparingly.
- **I4 — berry adopted:** `slate-berry` is the identity and the logo's colours. **Production gets berry only, in two
  themes** (light, dark). Coral stays **in the prototype only**, for a later comparison; Sea leaves production.
- **The values are the trial's, as the owner approved them after round 4** — the `slate-berry` block of
  `docs/design/prototype/masaha/identity-ink-spark.css` at `main`: the neutral ramp in the ink's hue, the spark ramp,
  the remap of `primary` / `ring` / `sidebar-ring` to ink, `accent` / `sidebar-accent` to the spark tint (light
  spark-100; dark spark-900 lifted 30 % toward spark-800), `sidebar-primary` and `chart-1` to the spark, **a hover
  role of its own** (light neutral-200, dark `muted`; an ink wash on muted tracks), status colours unchanged.
- **The spark's rules:** fills, large text and icons only (≥ 3:1 on its ground); **never on an action, never small
  text, never destructive**. Links in running text are ink and **underlined**. Hover and selected differ from each
  other (hue, plus a second mark where the trial gives one: the sidebar's 3 px bar, the chip's spark edge).
- **The logo** (round 3 of the trial; files already in `docs/design/prototype/masaha/logo/`, the `-berry` ones):
  «مساحة» as the hero with "MASAHA" under it, the ة's two dots in the spark; the **full logo** in the site's header,
  the phone menu and the sign-in / account pages (40 px tall), and in the admin's sidebar (replacing the «م» tile);
  the **small mark** (the ة + dots) in the collapsed rail and the browser tab; **never mirrored**, never cropped;
  its accessible name «مساحة» / "Masaha" in each language. The name «مساحة / Masaha» is kept.
- **Also in this task (the owner's list, 2026-11-11):** `foundation.md` **and an ADR** for the spark and hover roles;
  the berry tokens in `apps/web/src/shared/design-system/`; the logo in header / sidebar / auth; **favicon + app
  icon** in `apps/web/public/`; **the skeleton's fill** (today 1.11 on a card — give it the hover fill, ≈ 1.27) and
  **the photo strip's «+N» scrim** (white on a 55 % scrim, 3.64 — darken to ≈ 70 % for 4.5:1); **Google Branding**
  (the owner's steps, §3.7).
- **Pending — the owner's call, not yet given:** the owner / reception shell (its sidebar head is the space switcher)
  shows **no platform logo** — the supervisor recommends keeping none. Plan it as an `OD` with that recommendation.

### How each is built

| Decision | Built as |
|---|---|
| I1, I4 | §5's tables: ink = `neutral-900` / `neutral-50`; spark = `spark-500` / `spark-400`; no `brand-*`, no coral, no Sea |
| The values | Exactly the trial's `slate-berry` block, rewritten as `semantic.css` bindings (primitives, `color-mix` where the trial mixes); the prototype's CSS is a specification, never copied (`docs/design/README.md`, rule 1) |
| A hover role | `hover` / `hover-foreground` (light n-200 / n-900, dark n-800 / n-50) and `hover-on-muted` (ink at 10 % / 8 %) |
| The spark's rules | `spark` exposed as a fill, an edge, an outline and a mark only, never as a text colour (SD1); T5, T8, T11, T20 |
| Links underlined | The link Button and every link today marked by colour alone (§7.3) |
| Hover vs selected | Hover = `hover`; selected = `accent` + the sidebar's 3 px spark bar and the chip's spark edge; selected keeps its tint under the pointer |
| The logo | `Logo` (`form="full"` / `"mark"`), inline SVG on `foreground` and `spark`; 40 px in the site's headers and menu, 36 px in the admin's sidebar, the mark 36 px on its rail; favicon from the mark |
| Skeleton | Its own component token `skeleton` at the hover fill's steps (SD4) |
| «+N» | A `scrim` role at 70 % with its text pair, tested over any photo (SD5) |
| Google Branding | The owner's steps (§16) and a 120 px PNG the executor renders |
| Owner / reception shell | OD3, recommended: no logo |

---

## 5. The tokens — every value

### 5.1 Primitives (`primitives.css`)

`neutral` replaced; `brand` **removed** and `spark` added (SD7); `green`, `amber`, `red`, `blue`, `white`, radius,
shadow, motion and layers unchanged.

| Ramp | 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 950 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `neutral` (ink: OKLCH h 250, c 0.014) | #F7FBFF | #ECF4FC | #DDE5ED | #C9D0D7 | #9FA6AD | #767D84 | #5E646A | #484E54 | #2C3137 | **#1A1F25** | #0D1217 |
| `spark` (berry: seed #A149A0, h 328) | #FEF3FE | #FFE3FD | #FAC8F7 | #EBA5E8 | **#D27ED0** | **#B55BB3** | #934791 | #773A75 | #5A2A59 | #3F1B3E | #260D25 |

The file's header comment: "Palette (ink + berry, ADR 0019)". The shadows' `rgb(15 30 40 / …)` stay (the trial kept them).

### 5.2 Semantic roles (`semantic.css`) — `n` neutral, `s` spark; **bold** = changed binding

| Role | Light | Dark | Note |
|---|---|---|---|
| `background` / `foreground` | n-50 / n-900 | n-950 / n-50 | binding kept, ramp new |
| `card` / `card-foreground` | white / n-900 | n-900 / n-50 | kept |
| `popover` / `popover-foreground` | white / n-900 | n-900 / n-50 | kept |
| `muted` / `muted-foreground` | n-100 / n-600 | n-800 / n-400 | kept |
| `border` · `input` | n-200 · n-500 | n-800 · n-500 | kept |
| `ring` | **n-900** | **n-50** | ink |
| `primary` / `primary-foreground` | **n-900** / white | **n-50** / **n-950** | ink |
| `primary-hover` *(new)* | `color-mix(in oklch, var(--neutral-900), var(--neutral-50) 18%)` | `color-mix(in oklch, var(--neutral-50), var(--neutral-950) 18%)` | the trial's: primary mixed 18 % toward the background |
| `secondary` / `-foreground` | n-100 / n-900 | n-800 / n-100 | kept |
| `accent` / `accent-foreground` | **s-100** / **n-900** | **`color-mix(in oklab, var(--spark-800) 30%, var(--spark-900))`** / **n-50** | **selected**, the spark's tint |
| `hover` / `hover-foreground` *(new)* | n-200 / n-900 | n-800 / n-50 | never the spark; dark binds n-800 itself, not `muted` (coincidence is not identity) |
| `hover-on-muted` *(new)* | `color-mix(in oklab, var(--neutral-900) 10%, transparent)` | `color-mix(in oklab, var(--neutral-50) 8%, transparent)` | an ink wash on a muted ground |
| `spark` *(new)* | s-500 | s-400 | what matters now; carries no text |
| `scrim` / `scrim-foreground` *(new)* | `color-mix(in oklab, var(--neutral-900) 70%, transparent)` / n-50 | `color-mix(in oklab, var(--neutral-50) 70%, transparent)` / n-950 | text laid over a photo (SD5) |
| `destructive`, `success`, `warning`, `info` and their `-subtle` pairs | unchanged | unchanged | |
| `sidebar` / `sidebar-foreground` | white / n-700 | n-900 / n-300 | kept |
| `sidebar-primary` / `-foreground` | **s-500** / **n-950** | **s-400** / n-950 | the spark (the count badge) |
| `sidebar-accent` / `-foreground` | **s-100** / **n-900** | **the `accent` mix** / n-50 | selected (dark was n-800) |
| `sidebar-border` · `sidebar-ring` | n-200 · **n-900** | n-800 · **n-50** | ink ring |
| `chart-1` … `chart-5` | **s-500** · i-600 · a-500 · g-500 · n-500 | **s-400** · i-400 · a-400 · g-400 · n-500 | |
| `card-border` · `overlay-scrim` | n-200 · n-950 50 % | n-700 · n-950 70 % | kept |
| `skeleton` *(new component token)* | n-200 | n-800 | Skeleton only (SD4) |

Resolved hexes the tests write by hand: light `background` #F7FBFF, `foreground` #1A1F25, `spark` #B55BB3; dark
`background` #0D1217, `foreground` #F7FBFF, `spark` #D27ED0 — the logo files' and `theme-color`'s colours.

**A state takes its surface's text.** `primary-hover` (on primary: `primary-foreground`) and `hover-on-muted` (over
muted: the control's `foreground`) have no `-foreground`; `spark` carries no text (the badge on it is
`sidebar-primary`, whose foreground is verified). foundation §5's "every role with a surface has a matching
`-foreground`" gains that sentence.

### 5.3 Utilities (`tailwind.css`)

- `@theme inline` adds `--color-primary-hover`, `--color-hover`, `--color-hover-foreground`, `--color-hover-on-muted`,
  `--color-scrim`, `--color-scrim-foreground`.
- **The spark has no `--color-spark`** (SD1). Four static utilities instead, each on `var(--spark)`:
  `@utility bg-spark` (background-color), `border-spark` (border-color), `outline-spark` (outline-color),
  `fill-spark` (fill). There is no `text-spark`, so spark text cannot be written. (EC5, with its fallback.)
- `skeleton` stays a component token, bound inside the layer as `bg-(--skeleton)`.

### 5.4 The trial's numbers — the acceptance values (from `6_REPORT_INK_SPARK.md`)

| Pair | Light | Dark | Threshold |
|---|---|---|---|
| foundation §5's pairs | 66/66 | 66/66 | 4.5 / 3 |
| spark, lowest on its grounds | 3.70 | 4.77 | ≥ 3 |
| `sidebar-primary-foreground` on the spark | 4.58 | 6.84 | ≥ 4.5 |
| spark (the bar) on the selected tint | 3.45 | 4.92 | ≥ 3 |
| hover on card · on background | 1.27 · 1.22 | 1.26 · 1.44 | ≥ 1.2 (seen) |
| hover-on-muted over muted | 1.21 | 1.27 | ≥ 1.2 |
| selected on card | 1.19 | 1.23 | ≥ 1.15 (seen; a second mark or a word carries it) |
| selected on background (the chip, with its edge) | 1.14 | 1.39 | not tested (D5) |
| muted-foreground · sidebar-foreground on hover | 4.71 · 6.62 | — | ≥ 4.5 |
| foreground / muted-foreground on selected | 13.94 / 5.04 | 13.01 / 5.50 | ≥ 4.5 |
| foreground on hover-on-muted | 12.31 | 9.90 | ≥ 4.5 |
| input on card · on background | 4.17 · 4.01 | 3.98 · 4.51 | ≥ 3 |
| focus ring on every ground | 13.0–16.6 | 12.6–18.1 | ≥ 3 |
| ink ↔ red, OKLab ΔE (protan, deutan) | .346 (.190, .319) | .329 (.365, .278) | ≥ .10 (≥ .08) |
| spark ↔ red, ΔE (CVD) | .191 (.184) | .156 (.154) | ≥ .10 (≥ .08) |
| selected tint ↔ destructive-subtle, ΔE | .05 | .13 | dark ≥ .10 |
| red-400's hue in dark | — | h 25.0 | 15–45° |

---

## 6. Stronger decisions

Each strengthens a decision of the prompt or a document within scope; each is built only with the plan's approval.

- **SD1 — the spark has no text utility.** *What:* expose `spark` through four static utilities, not `--color-spark`.
  *Why:* "never small text" becomes impossible to write, not only reviewed; the token test holds it (T11). *Cost:*
  four `@utility` lines; a pattern unlike the other roles, said in foundation §5. `text-sidebar-primary` and
  `text-chart-1` (spark through other roles) stay possible: Review Focus. *Recommend:* yes.
- **SD2 — `check:classes` refuses the selected tint as a hover.** *What:* a third rule: `bg-accent`,
  `text-accent-foreground`, `bg-sidebar-accent`, `text-sidebar-accent-foreground` under a hover or highlight variant
  (`hover:`, `focus:`, `focus-visible:`, `aria-expanded:`, `data-open:`, `has-data-open:`, `data-[selected=true]:`,
  `data-highlighted:`, alone or compounded) fail anywhere in `apps/web/src`. *Why:* shadcn's copies default to
  `hover:bg-accent`; the next copied component would bring the old meaning back silently. *Cost:* the script, its unit
  test, `setup.md`'s commands row, `CLAUDE.md`'s commands line, foundation §3 *Enforcement*; a build-check change (the
  PR's review is a separate conversation anyway, > 25 files). *Recommend:* yes.
- **SD3 — `primary-hover` is a role.** *What:* the trial's arbitrary `hover:bg-[color-mix(…)]` becomes a token used by
  Button and Calendar. *Why:* the token test then proves its label keeps 4.5:1 (T4); today nothing proves it.
  *Cost:* one role, one utility. *Recommend:* yes.
- **SD4 — the skeleton's own token at the hover fill's steps.** *What:* `skeleton` = n-200 / n-800, not `bg-hover`.
  *Why:* foundation §4, "coincidence is not identity": a placeholder and a hover mean different things; the value is
  the owner's (≈ 1.27). *Cost:* one component token. *Recommend:* yes.
- **SD5 — «+N» on a `scrim` role.** *What:* `bg-scrim text-scrim-foreground` in place of `bg-foreground/60
  text-background`. *Why:* the 70 % is then a token the unit test proves over the worst photo pixel (white and black),
  instead of an opacity in a feature's class that no test sees. *Cost:* two roles, two utilities, one pair test.
  *Recommend:* yes. *Fallback if declined:* `bg-foreground/70`, proven by the visual pass only.
- **SD6 — controls on a muted ground hover with the wash.** *What:* the trial's dark `hover` equals `muted`, so a
  control drawn on `muted` or `secondary` loses its hover in dark; each such control takes `hover-on-muted` (D1).
  *Why:* the owner's complaint was an invisible hover; the trial fixed it on card and background, not on these.
  *Cost:* five small edits and EC10's search. *Recommend:* yes.
- **SD7 — `brand-*` removed, not aliased.** *What:* the ramp is `spark-*`; `brand` no longer exists. *Why:* the brand
  now has two roles; a `brand` ramp equal to the spark would mislead, and T3 then refuses a leftover. *Cost:* foundation
  §4's tier table. *Recommend:* yes.
- **SD8 — the trial's criteria become tests.** *What:* T5–T9: the spark ≥ 3:1 on each ground it sits on; the fills seen
  (≥ 1.2 hover-type, ≥ 1.15 selected); hover ≠ selected (OKLab ΔE ≥ 0.02, a just-noticeable difference); ink ↔ red and
  spark ↔ red ≥ 0.10 (≥ 0.08 protan and deutan — the trial's own proposal 2 for the spark); the dark tint ≥ 0.10 from
  destructive-subtle; red-400's hue 15–45°. *Why:* the measured identity cannot drift unseen. *Cost:* OKLab, OKLCH,
  `color-mix` and Machado's matrices in the test (EC3, EC4). The thresholds are the trial's criteria, or a JND, never
  fitted to the values. *Recommend:* yes.
- **SD9 — `SidebarHeader` takes `mark` (the rail's) and `logo` (expanded and the drawer), both required.** *Why:* the
  rail shows the mark, the rest the full logo; the sidebar alone knows its mode. *Cost:* the showcase and the test
  change with it. *Recommend:* yes.
- **SD10 — the logo's link takes the layer's one focus style** (`rounded-sm focus-visible:outline-2
  focus-visible:outline-offset-2 focus-visible:outline-ring`), in place of the browser's default. *Why:* foundation
  §11, one focus style; the element is rebuilt anyway. *Recommend:* yes.

**Rules of the documents this item bends — stated, not silent:**
- *No colours outside the layer* (CLAUDE.md, foundation §2): the browser's icons (`apps/web/public/`, `theme-color` in
  `index.html`) and the reset e-mail carry hexes. Neither can read a token: the icons are images the browser draws
  outside the page, the e-mail is read by mail clients (finding 19, accepted). foundation §16 records the exception;
  T10, T13, T14 and T22 hold the values by hand.
- *Admission test* (foundation §2.8): the logo enters the layer. It is the identity the tokens draw, not a domain
  concept; `LOGO_DECISION.md` §4 and the trial expected it there. Said in the §12 row.
- *Every role with a surface has a `-foreground`*: the two state roles and the spark (§5.2), said in foundation §5.

---

## 7. What changes, file by file

### 7.1 Inventory — every use of the changing roles (at `main` + #143)

**The layer's components**

| File | Today | Becomes | Commit |
|---|---|---|---|
| `components/actions/Button/Button.tsx` | primary `hover:bg-[color-mix(in_oklch,var(--primary),var(--foreground)_12%)]`; outline/ghost `hover:bg-accent hover:text-accent-foreground aria-expanded:bg-accent aria-expanded:text-accent-foreground`; link `text-primary underline-offset-4 hover:underline` | primary `hover:bg-primary-hover`; outline/ghost `hover:bg-hover hover:text-hover-foreground aria-expanded:bg-hover aria-expanded:text-hover-foreground`; link `text-primary underline underline-offset-4`; secondary and destructive unchanged; the comment rewritten | C2 · C3 |
| `components/fields/Calendar/Calendar.tsx` | `FILLED` hover mixes primary toward foreground; today's cell `bg-muted`, its ghost day hovering | `FILLED` `hover:bg-primary-hover hover:text-primary-foreground`; today's day when not filled `hover:bg-hover-on-muted`; the range's `bg-accent` kept (selected) | C2 |
| `components/actions/DropdownMenu/DropdownMenu.tsx` | items `focus:bg-accent focus:text-accent-foreground`; sub-trigger `data-open:bg-accent data-open:text-accent-foreground` | `focus:bg-hover focus:text-hover-foreground`; `data-open:bg-hover data-open:text-hover-foreground`; destructive item kept | C2 |
| `components/fields/Select/Select.tsx` | item `focus:bg-accent focus:text-accent-foreground` | `focus:bg-hover focus:text-hover-foreground` | C2 |
| `components/fields/Combobox/Combobox.tsx` | item `data-[selected=true]:bg-accent …accent-foreground` (cmdk's highlighted) | `data-[selected=true]:bg-hover …:text-hover-foreground`; the chosen keeps its check | C2 |
| `components/data/Table/Table.tsx` | row `hover:bg-accent has-data-open:bg-accent`; header keeps `muted` | `hover:bg-hover has-data-open:bg-hover`; header unchanged; comments | C2 |
| `components/data/DataTable/DataTable.tsx` | sort header `hover:bg-accent hover:text-accent-foreground`, on the muted header | `hover:bg-hover-on-muted hover:text-foreground` (D1) | C2 |
| `components/fields/Input/Input.tsx` | `InputAction` `hover:bg-accent hover:text-accent-foreground` | `hover:bg-hover hover:text-hover-foreground` | C2 |
| `components/fields/ToggleGroup/ToggleGroup.tsx` | `hover:bg-accent hover:text-accent-foreground … data-on:border-primary data-on:bg-accent data-on:text-accent-foreground` | `not-data-on:hover:bg-hover not-data-on:hover:text-hover-foreground … data-on:border-spark data-on:bg-accent data-on:text-accent-foreground`; the comment | C2 |
| `components/navigation/Tabs/Tabs.tsx` | pills `not-data-active:hover:bg-accent …accent-foreground`; md `md:not-data-active:hover:bg-transparent`; line `after:bg-primary` | `not-data-active:hover:bg-hover not-data-active:hover:text-hover-foreground`; md `md:not-data-active:hover:bg-hover-on-muted` (text to `foreground` kept); line `after:bg-spark`; the phone's active pill stays `primary` | C2 · C4 |
| `components/fields/SegmentedControl/SegmentedControl.tsx` | unchecked `hover:text-foreground` only | adds `data-unchecked:hover:bg-hover-on-muted` | C2 |
| `components/navigation/Sidebar/Sidebar.tsx` | item `hover:bg-sidebar-accent hover:text-sidebar-accent-foreground`, current `data-[active=true]:bg-sidebar-accent …`; `SidebarHeader` shows `mark` always | `not-data-[active=true]:hover:bg-hover not-data-[active=true]:hover:text-hover-foreground`; current keeps the tint and gets a 3 px spark bar at the inline start, as a logical pseudo-element (`relative overflow-hidden` + `data-[active=true]:before:absolute …before:inset-y-0 …before:start-0 …before:w-0.75 …before:bg-spark`), clipped by the item's radius as the trial's inset shadow; badge unchanged (`sidebar-primary` is now the spark); `SidebarHeader({ mark, logo })` (SD9) | C2 · C6 |
| `components/display/FilterTag/FilterTag.tsx` | remove button: a ghost Button on `secondary` | its `className` adds `hover:bg-hover-on-muted` (D1) | C2 |
| `components/feedback/Skeleton/Skeleton.tsx` | `bg-muted` | `bg-(--skeleton)` | C5 |
| `leaflet.css` | `.leaflet-bar a:hover` on the accent pair; `.map-mark-selected span` outlined `var(--primary)` | `var(--hover)` / `var(--hover-foreground)`; `outline: 3px solid var(--spark)` (the span keeps the light theme, finding 135, so the spark resolves light on the tiles); the selected-mark comment | C2 · C4 |
| `components/display/Logo/` *(new)* | — | `Logo.tsx`, `drawing.ts`, `index.ts`, `Logo.component.test.tsx` (§7.4) | C6 |
| `index.ts` (layer) | — | exports `Logo`, `type LogoProps` | C6 |

Unchanged in code, changed by the tokens: Badge `primary` (the tint, ink text), StatCard's icon tile (the tint), Meter
`primary` and Heatmap (ink), Checkbox, RadioGroup, Switch checked (ink), Toast's action (ink), Pagination (outline →
`hover`), BarChart (`chart-1` = spark).

**Features and pages**

| File | Today | Becomes | Commit |
|---|---|---|---|
| `features/directory/components/card/SpaceCard.tsx` | Card `hover:bg-accent` | `hover:bg-hover` | C2 |
| `features/directory/components/page/ContactList.tsx` | `hover:bg-accent` | `hover:bg-hover` | C2 |
| `features/finance/components/DebtsTab.tsx` | tile `hover:bg-accent` | `hover:bg-hover` | C2 |
| `features/overview/components/admin/PlatformTiles.tsx` · `owner/OwnerOverview.tsx` | `hover:bg-accent` | `hover:bg-hover` | C2 |
| `pages/site/public/home/AreaCards.tsx` | Card `hover:bg-accent` | `hover:bg-hover` | C2 |
| `features/spaces/components/contacts/ContactsSheet.tsx` (#143) | handle `hover:bg-accent`; lifted row `border-primary shadow-floating` | `hover:bg-hover`; `border-spark shadow-floating` | C2 · C4 |
| `features/spaces/components/contacts/ContactsView.tsx` (#143) | the `<a>` tile `bg-muted … hover:bg-accent` | the `<li>` holds `rounded-lg bg-muted`; the `<a>` keeps its layout, `rounded-lg hover:bg-hover-on-muted` (D1) | C2 |
| `features/spaces/components/photos/PhotosEdit.tsx` (#143) | lifted tile `outline-2 outline-primary` | `outline-2 outline-spark` | C4 |
| `features/spaces/components/photos/PhotosView.tsx` (#143) | «+N» `bg-foreground/60 … text-background` | `bg-scrim … text-scrim-foreground` | C5 |
| `pages/site/auth/RegisterPage.tsx` (2) · `pages/site/public/about/AboutPage.tsx` (the `#contact` link) · `pages/site/shell/SiteFooter.tsx` (4) | `className="text-primary"` | `text-primary underline underline-offset-4` | C3 |
| `features/spaces/components/editor/MissingChecklist.tsx` | `text-primary underline-offset-4 hover:underline` | `text-primary underline underline-offset-4` | C3 |

Left as they are, and why: the verified lines in `text-primary` (SpaceCard, SpaceSummary, SpaceHeader) become ink with
their icon; FavoriteButton's heart (an action's state: ink); HoursSection and #143's HoursView today rows (`bg-accent`:
selected); PackageOptions' chosen card (`border-primary`: an ink edge); SpaceCover's and SpaceHead's letter tiles
(`bg-primary`: ink tiles); AboutPage's and #143's icons in `text-primary`; the links already underlined (PackageSheet,
PricingCard, AmenitiesSection, OwnerHead, PricesSection, #143's AmenitiesSheet, ProfileHeader, HoursView); the names in
tables (`text-foreground … hover:underline`: a row's name, not running text); SkipLink; the public Gallery's pill
(`bg-background/90` with `foreground`: about 12:1 over any photo, no «+N» scrim). The production covers are photos or
the letter tile — the prototype's drawn covers and their OKLCH mix have no production counterpart.

**The rule while editing:** selected keeps its tint under the pointer — a hover class applies only when the item is
not selected (`not-data-on:`, `not-data-active:`, `not-data-[active=true]:`, or the caller's condition).

### 7.2 The shells (C7)

| File | Becomes |
|---|---|
| `pages/site/shell/SiteHeader.tsx` | the home `Link` holds `<Logo label={copy.site.wordmark} className="h-10" />`, with SD10's focus style |
| `pages/site/shell/SiteMenu.tsx` | the drawer's `<p>` wordmark becomes `<Logo label={copy.site.wordmark} className="h-10 self-start" />` (`self-start`: a stretched column would centre it — the trial's defect 3) |
| `pages/site/shell/FocusLayout.tsx` | as SiteHeader (sign in, register, forgot, reset, the forced change) |
| `pages/dashboard/shell/AdminLayout.tsx` | `SidebarHeader mark={<Logo form="mark" className="size-9" />} logo={<Logo className="h-9" />}`, both decorative; the children: `<span className="sr-only">{copy.site.wordmark}</span>` and the caption «إدارة المنصة», so the header is read «مساحة، إدارة المنصة» once |
| `SpaceLayout` / `SpaceHead` | unchanged (OD3 (a)) |

`copy.site.wordmark` stays the logo's name; no catalogue line changes. `PageHeader`'s and `DocumentTitle`'s fallback
text stay text.

### 7.3 The showcase

`ShowcaseNav.tsx` (hover → `hover`, the current entry keeps `accent`, its hover only when not current, C2);
`sections/fields/SortableSection.tsx` (handle hover → `hover`, C2; lifted → `border-spark`, C4);
`sections/fields/FieldSection.tsx` (its link underlined, C3); `sections/navigation/SidebarSection.tsx` (`mark` and
`logo`, C6); `sections/display/LogoSection.tsx` *(new)*, its `registry.tsx` entry and `fixtures.json` samples (both
forms, named and decorative, on the page and in a sidebar; C6).

### 7.4 The logo component (C6)

- **Files:** `components/display/Logo/Logo.tsx`; `drawing.ts` — the two `d` strings copied verbatim from
  `docs/design/prototype/masaha/logo/masaha-logo-berry.svg` (the owner's asset, not prototype code), the two viewBoxes
  and the mark's clip rectangles (`h`: 250 240 329 540; `d`: 400 50 380 200), each named; `index.ts`; the test.
- **API:** `LogoProps = Omit<ComponentProps<'svg'>, 'children'> & { form?: 'full' | 'mark'; label?: string }`.
  `form` defaults to `full`. With `label`: `role="img"` and `aria-label`; without: `aria-hidden` and
  `focusable="false"`. No word inside the layer (§2.5).
- **Drawing:** `full` — `<svg viewBox="263 45 2473 903">`, the words path `fill-foreground`, the dots path
  `fill-spark`, both `fill-rule="evenodd"`. `mark` — `<svg viewBox="190 17 778 778">`: the words path inside a nested
  `<svg>` whose viewport is rectangle `h` (a nested viewport clips, so no `id` is needed), the same again inside
  `translate(1158 0) scale(-1 1)` (the drawing's own symmetry, not RTL mirroring), and the dots inside rectangle `d`
  under `translate(-11.5 0)` — the file's clip paths reproduced (EC6).
- **Size:** by its height from the caller (`h-10`, `h-9`, `size-9`); the component sets `w-auto` and its viewBox's
  aspect ratio, so it never stretches. Nothing direction-dependent: no `rtl:` class, no icon wrapper.
- **Weight:** the words path is ~13 KB raw (about 5–6 KB compressed) in the site's first download; the mark reuses
  the same string. EC7 records it; `check:build` has no size budget.

### 7.5 The browser's icons (C8)

- `apps/web/public/` *(new; Vite copies it to `dist/` as is, served at the root, before the SPA rewrite)*:
  - `favicon.svg` — the berry mark, the words path defined once (`<defs>` + two `<use>`, ids are safe in a file of
    its own), classes `.ink` / `.spark` filled #1A1F25 / #B55BB3, and `@media (prefers-color-scheme: dark)` #F7FBFF /
    #D27ED0. The page's CSP allows its inline style (`style-src 'unsafe-inline'`). The browser's scheme, not the app's
    toggle, decides it: the tab is the browser's.
  - `favicon.ico` — 16, 32 and 48 px PNG entries of the app-icon art (the mark on its white tile, D3).
  - `apple-touch-icon.png` — 180 × 180, the mark on white, full bleed (D2).
- `apps/web/index.html`, after the stylesheet link:
  `<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48" />`,
  `<link rel="icon" href="/favicon.svg" type="image/svg+xml" />`,
  `<link rel="apple-touch-icon" href="/apple-touch-icon.png" />`,
  `<meta name="theme-color" content="#f7fbff" media="(prefers-color-scheme: light)" />`,
  `<meta name="theme-color" content="#0d1217" media="(prefers-color-scheme: dark)" />`. The inline scripts are
  untouched, so their CSP hashes hold (`contentSecurityPolicy.unit.test.ts`).
- **How the rasters are made (OD4 (a)):** in headless Chrome over CDP (already used for screenshots): each SVG at its
  pixel size, `Emulation.setDefaultBackgroundColorOverride` transparent (the .ico art) or white (180, 120), captured
  at device scale 1; the `.ico` packed by a ~30-line Node script in the session's scratchpad (ICONDIR, three entries,
  the PNGs). Nothing but the three files enters the repository. Also rendered, **not committed:** the 120 × 120 PNG
  for Google (§16) to `C:\dev\masaha\workspace\TASKS\IDENTITY\google\masaha-logo-120.png`.

### 7.6 The reset e-mail (C9)

`resetEmail.ts`'s `COLOR`: `page` #f7fbff (n-50), `card` #ffffff, `border` #dde5ed (n-200), `ink` #1a1f25 (the brand
line «مساحة», the button's fill, the links), `onInk` #ffffff, `text` #1a1f25 (n-900; kept apart from `ink`: same
value, different meaning), `muted` #5e646a (n-600). The English inline link gets `text-decoration:underline`; the link
written as text is ink. The comment names ADR 0019's values and finding 19. Every pair equals one the web verifies
(primary-foreground on primary, foreground and muted-foreground on card and background). No spark, no image.

### 7.7 The prototype (C10, OD5 (a))

- `masaha/i18n.js`: no `?identity=` gives `slate-berry`; `?identity=sea` gives today's bundle (no `data-identity`);
  `slate-coral` unchanged; links carry `identity` only when it is not the default; the tab's icon follows as now.
- `masaha/identity-ink-spark.css`: its header comment (foundation now takes berry, ADR 0019; Sea is `?identity=sea`).
- `Reset email.html`: its inline hexes to §7.6's.
- `CHANGES.md`: a section «Berry, the default (date)»; `INDEX.md`'s `?identity=` row; `SCREENS.md`'s line on
  `Wordmark.html` (option A superseded by the logo, foundation §16).
- Checks: `node docs/design/scripts/check-parse.mjs`, `node docs/design/scripts/check-classes.mjs`.

### 7.8 Documents

| Document | Change | Commit |
|---|---|---|
| `foundation.md` Status + Last Updated | the values are ink + berry (ADR 0019); Sea was direction 1a's | C1 |
| §4 | tier table `spark-50…950`; *Primitive palette (ink + berry, ADR 0019)*: the two ramps (§5.1), "the brand has two roles: the ink `neutral-900` / `neutral-50` and the spark `spark-500` / `spark-400`"; component tokens: `skeleton` | C1 |
| §5 | roles tables: `primary` (ink: actions, links, checked and active controls), `accent` (selected, what matters now, as a tint), new rows `primary-hover`, `hover` / `hover-foreground`, `hover-on-muted`, `spark`, `scrim` / `scrim-foreground`; the `-foreground` sentence (§5.2); *Values (ink + berry)* = §5.2; *Verified* rewritten with T4–T9's pairs and criteria; usage rules: the spark's rules, text over a photo on `scrim` | C1 |
| §5 usage rules | hover vs selected (hue + a second mark; selected keeps its tint under the pointer; a control on a muted ground takes the wash) | C2 |
| §3 *Enforcement* · §11 | (e) the selected tint is never a hover (`check:classes`); "A hover never fades a fill" rewritten: secondary and destructive mix toward the foreground, the ink's hover is `primary-hover`, outline / ghost / items hover with `hover`, never `accent` | C2 |
| §12 rows | Table, DataTable (sort header), Select / Combobox (highlighted item), ToggleGroup (hover; on: the tint, a spark edge, the check), SegmentedControl (the wash on hover), Sidebar (hover; current: tint + spark bar; `SidebarHeader` mark and logo in C6), Calendar (filled days' hover) · Button (link underlined, C3) · Tabs (`line`: a spark indicator), Sortable's callers' lifted mark (C4) · Skeleton (C5) · Logo row in `display` (C6) | C2–C6 |
| §5 usage rules | links in running text are underlined | C3 |
| §15 | row 1 → *Settled — ink + berry spark (ADR 0019)*; row 5 → *Settled — the logo (§16)*; the closing line keeps Sea as the first direction | C1 · C6 |
| §16 *The logo* (new) | the forms; where each shows; sizes (40 px headers and menu, 36 px sidebar, the mark 36 px rail; never under 36 px tall — the smallest the owner saw; the mark from 16 px); clear space 20 % of its height (8 px in the 56 px header); never mirrored, cropped, stretched, recoloured or set on a photo without a plain ground; its name; the source files (`docs/design/prototype/masaha/logo/`); the browser's icons and the e-mail as stated exceptions, held by tests | C6 · C7 · C8 |
| ADR 0019 *The brand: an ink for actions and a spark for what matters now* (new, `docs/architecture/decisions/0019-ink-and-spark-brand.md`) | short and decision-level, no file names or code: **Context** — Sea's one teal carried actions, links, hover and selected alike; the owner wanted a warm colour, and every warm primary failed beside the destructive red (hue apart only, the same under colour blindness); a measured trial, and the logo drawn with it. **Decision** — two roles: an ink for actions, links (underlined), focus and structure; a berry spark, sparingly, for what matters now, never small text, an action or destructive; hover a neutral role of its own, selected the spark's tint, told apart by hue and a second mark; the neutrals in the ink's hue; status colours unchanged; one brand in two themes; the logo «مساحة» over "MASAHA" in ink with the ة's dots in the spark; the name kept. **Alternatives** — keep Sea; a warm primary (coral, the sea sunset): rejected; slate-coral: equal by the numbers, berry chosen with the logo, coral kept in the design for a later comparison; a third, coral dark theme: rejected; hover as before (`muted`): rejected, unseen. **Consequences** — every screen changes at once; links carry underlines; the values that live outside the page (the browser's icons, the e-mail) carry the identity by hand, held to it by tests; the measured criteria are tests, so a later spark must pass them | C1 |
| `docs/README.md` | the ADR's line; foundation's line names the logo | C1 · C6 |
| `docs/development/setup.md` (commands row) · `CLAUDE.md` (commands line) | `check:classes`' third rule (SD2) | C2 |
| finding 219 + index | §8 | C11 |
| Design archive | §7.7 | C10 |

`docs/frontend/architecture.md` and `docs/features/users.md` say "the wordmark": the logo is a wordmark, so they stay
true; no change. No capability document changes (no behaviour changes); no *Deferred documents* trigger is met (no
endpoint).

### 7.9 Files shared with another open item

None once #143 merges (EC1). `foundation.md`, the layer's `index.ts` and `routes.component.test.tsx` are #143's too;
this item edits them only after it is in `main`.

---

## 8. Related findings

| Finding | Fold? | Why · cost |
|---|---|---|
| 19 — the reset e-mail's colours outside the layer (Accepted) | No change | Its acceptance says a palette change is carried by hand; C9 does that, and T22 holds it |
| 5 — dark destructive badge louder (Accepted) | No | Status colours unchanged; T8 keeps the spark's tint apart from destructive-subtle |
| 135 — the map's marks take the light theme | No | The selected mark's spark resolves in that light span, as its tones do |
| 215 — the prototype's Home disagrees with production | No | Not the identity; C10 touches `i18n.js` only |
| **219 (new) — the README's screenshots show Sea** | Record (C11) | `docs/assets/readme/*.webp` and `masaha.gif` show Sea; resolves when they are re-shot under ink + berry, in a README task. Range for any other finding this item records: **219–224** |

---

## 9. Design issues — built only once approved

- **D1 — in dark, `hover` equals `muted`, so a control on a muted ground shows no hover.** Found: DataTable's sort
  headers (the muted header row), the calendar's today, FilterTag's remove button (on `secondary`), #143's contact
  tiles (the tile is `muted`). Each takes `hover-on-muted`, the trial's wash for its tracks; the contact tile moves its
  `muted` fill to the `<li>` so the anchor's translucent hover lies over it. EC10 searches for more.
- **D2 — the 180 px home-screen icon is full bleed.** iOS rounds the corners itself and turns transparent corners
  black, so the app icon's own rounded tile is squared for this file (the mark and its white ground unchanged).
- **D3 — the `.ico` draws the mark on its white tile.** It cannot switch with the scheme; without the tile the ink
  mark is dark on a dark tab bar in a browser that ignores the SVG favicon. The SVG keeps the owner's "no background"
  (Axis 3).
- **D4 — Google's 120 px logo:** the mark on white with clear space all round, so a round crop never cuts the dots.
- **D5 — the selected chip on the page background is 1.14** (light): accepted, as the trial did — its spark edge and
  its check carry the state. Not a test pair.

---

## 10. Tests — the matrix

Lanes per `testing.md`. "Seen failing" is how the executor sees each red before the change that turns it green.

| # | Lane · file | Proves | The break it catches | Seen failing |
|---|---|---|---|---|
| T1 | unit · `tokens/semantic.unit.test.ts` | key parity; every role and themed token of §5.2 in both themes (ROLES, THEMED_TOKENS extended) | a new role missing in one theme | before `semantic.css` has the new roles |
| T2 | unit · same | every role resolves to a colour, `color-mix` (oklab, oklch, `transparent`) included; a translucent result composited over its named ground | a typo in a mix; a mix the resolver mis-reads | resolver first, against today's tokens' `overlay-scrim` (not resolvable today) |
| T3 | unit · same | the primitives are exactly `spark`, `neutral`, `green`, `amber`, `red`, `blue` × 11 steps + `white` | a leftover `brand-*`; a missing step | today's file (has `brand`, lacks `spark`) |
| T4 | unit · same | text ≥ 4.5: §5's verified pairs + muted-foreground and sidebar-foreground on `hover`; foreground and muted-foreground on `accent` and `sidebar-accent`; `primary-foreground` on `primary-hover`; foreground on `hover-on-muted` over muted; `scrim-foreground` on `scrim` over #ffffff and over #000000 | a value moved below 4.5; the scrim back to 60 % (4.21 over white) | the new pairs fail on today's tokens (missing roles) |
| T5 | unit · same | non-text ≥ 3: `spark` on background, card, popover, sidebar, accent, sidebar-accent; `ring` on muted, accent, hover, sidebar-accent; the existing non-text pairs | a paler spark step; a ring that vanishes on the tint | missing roles today |
| T6 | unit · same | fills seen: `hover` on card, background, popover, sidebar ≥ 1.2; `hover-on-muted` over muted ≥ 1.2; `skeleton` on card and background ≥ 1.2; `accent` on card and `sidebar-accent` on sidebar ≥ 1.15 | the hover back to `muted` (1.11); the tint back to spark-50 (1.08) | today: `skeleton` missing; with `skeleton: n-100` it reads 1.11 |
| T7 | unit · same | hover is not selected: OKLab ΔE(`hover`, `accent`) and (`hover`, `sidebar-accent`) ≥ 0.02, both themes | hover set to the tint | a temporary `--hover: var(--accent)` |
| T8 | unit · same | the brand never reads as an error: ΔE(`primary`, `destructive`) and ΔE(`spark`, `destructive`) ≥ 0.10, ≥ 0.08 under protan and deutan (Machado 2009, severity 1); dark ΔE(`accent`, `destructive-subtle`) ≥ 0.10; dark `destructive`'s OKLCH hue 15–45° | a coral spark (#EF7B62 measured 0.036); a reddish tint | a temporary coral `spark` |
| T9 | unit · same | the measures are right: contrast (existing); OKLab of #ffffff = (1, 0, 0) and of #ff0000 ≈ (0.628, 0.225, 0.126); `color-mix(in oklab, #ffffff, #000000)` = #636363; each Machado row sums to 1 | a wrong constant or transfer function | written before the helpers |
| T10 | unit · same | the identity's resolved hexes: light background #f7fbff, foreground #1a1f25, spark #b55bb3; dark #0d1217, #f7fbff, #d27ed0 (the logo files', `theme-color`'s and the favicon's) | a step moved off the logo's colours | today's Sea values |
| T11 | unit · same (reads `tailwind.css`) | the spark is offered only as `bg-`, `border-`, `outline-`, `fill-spark`; no `--color-spark` | someone exposes spark text | before `tailwind.css` changes |
| T12 | unit · `scripts/checkClasses.unit.test.ts` | `check:classes` refuses the tint under each hover / highlight variant (compounded too), and allows `bg-accent`, `data-on:bg-accent`, `data-[active=true]:bg-sidebar-accent` | the rule removed or narrowed; a shadcn copy's `hover:bg-accent` | before the rule (SD2) |
| T13 | unit · `apps/web/scripts/browserIcons.unit.test.ts` *(new)* | `index.html` links `/favicon.ico`, `/favicon.svg` (`image/svg+xml`), `/apple-touch-icon.png`, each present in `public/`; `theme-color` #f7fbff light, #0d1217 dark | a link or file renamed or dropped | before `public/` exists |
| T14 | unit · same | `favicon.svg` fills ink #1a1f25 / spark #b55bb3, and #f7fbff / #d27ed0 under `prefers-color-scheme: dark` | the dark rule lost; a colour off | same |
| T15 | unit · same | `apple-touch-icon.png` is 180 × 180 (PNG header); `favicon.ico` holds 16, 32 and 48 entries | a wrong export | same |
| T16 | component · `Logo.component.test.tsx` *(new)* | named by `label` as an image («مساحة», "Masaha"); hidden from assistive technology without one; both forms draw `fill-foreground` and `fill-spark`; the same markup under `DirectionProvider` rtl and ltr (never mirrored) with no `rtl:` or scale class; axe clean | the name dropped; a mirroring class; a fill on another role | before the component exists |
| T17 | component · `Sidebar.component.test.tsx` | the rail shows `mark` and not `logo`; desktop and the phone drawer show `logo` and not `mark` | the mode branch swapped | before SD9 |
| T18 | component · `SiteLayout.component.test.tsx`, `changePasswordPage.component.test.tsx` | the header's home link is named «Masaha» by the logo's image; the phone menu holds the logo; the focus shell's header too | the text wordmark kept; the logo unnamed | before C7 |
| T19 | component · `pages/dashboard/routes.component.test.tsx` | the admin's sidebar header: the decorative logo, the name for assistive technology, the caption; no «م» tile | the tile back; the name read twice | before C7 |
| T20 | component · `Button.component.test.tsx` | the link variant is underlined at rest; no variant's class names the spark | `hover:underline` back; a spark on an action | before C3 |
| T21 | component · existing axe tests of the touched components | still clean (jsdom: no colour contrast — that is EC11's) | an aria regression from the restructures (ContactsView, AdminLayout) | n/a (existing) |
| T22 | unit (api) · `resetEmail.unit.test.ts` | the HTML's colours are exactly {#f7fbff, #ffffff, #dde5ed, #1a1f25, #5e646a}; the button cell `background:#1a1f25` with a `#ffffff` label; the English link underlined | a Sea hex left; the underline removed | before C9 |
| T23 | manual · the visual pass (§13) | hover vs selected seen, focus rings, no Sea, contrast of painted text, axe in Chrome, the logo, RTL, 360 px | anything visual | n/a |
| T24 | prototype scripts | `check-parse`, `check-classes` after C10 | a broken prototype page | n/a |

The test helpers (OKLab, OKLCH, `color-mix`, compositing, Machado) live inside `semantic.unit.test.ts`; no production
code serves a test. The thresholds are §5.4's criteria; a red test is fixed in the values, never in the threshold.

---

## 11. Review Focus — inputs no planned test exercises

- Which class each component hovers with (visual; T23 and SD2's rule are the guards).
- Spark through other roles: `text-sidebar-primary`, `text-chart-1` remain writable.
- The mark's inner `scale(-1 1)` is the drawing's symmetry; T16 compares directions, not transforms.
- Hover classes guarded by `not-…:` on selected items: the order of Tailwind's variants is not relied on.
- The destructive and secondary hovers still mix in OKLCH toward the new ink (PA6).
- The heatmap and the occupancy meter in dark: ink is near-white there.
- `theme-color` follows the device's scheme, not the app's toggle; Safari without SVG favicons gets the `.ico`.
- The CSP for the favicon's inline style; the SPA rewrite never answering `/favicon.*` (EC8, after deploy).
- ContactsView's `<li>`/`<a>` restructure: the focus ring still on the anchor, the wash over the `<li>`.
- The first download's growth (EC7); the 360 px header (EC14).
- `color-mix` in the test against Chrome's painted result (EC3).

---

## 12. Executor checks (`EC…`)

- **EC1 — the start.** `git fetch origin`; #143 is in `origin/main` (if not: stop and report). Next numbers: the last
  ADR (0018 → 0019), the last finding (→ 219), the last issue/PR (`gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number'`
  → 143, so #144). Re-run the inventory on the real `main`:
  `grep -rnE "(bg|text|border|outline|ring|fill|after:bg)-(accent|primary|sidebar|chart-1)|var\(--(primary|accent|ring|brand|sidebar)|color-mix|hover:bg-" apps/web/src --include=*.tsx --include=*.ts --include=*.css`
  and compare with §7.1; a file the plan does not list takes the same rule and is named in the report.
- **EC2 — databases and ports.** This folder: API 3323, web 5323, `TEST_DATABASE_URL` `masaha_design_test`,
  `DATABASE_URL` `masaha_dev`. **Never `db:seed` `masaha_dev`.** The visual pass reads its demo set as it is: check
  the directory lists the demo spaces (`masaha-demo` and the 24); sign in as `demo-owner@example.com`,
  `demo-reception@example.com` and the seeded admin with the passwords in `apps/api/.env`, never printed. If the demo
  set is missing: stop and ask the owner (a `masaha_design_dev` of its own, created, migrated and seeded with
  `SEED_DEMO=true`, is his call). `test:api` uses `masaha_design_test`; if it does not exist in the shared container,
  create it as setup › *Running a second folder* says (a test database only; nothing else is created or seeded).
- **EC3 — colour maths.** The test's OKLab/OKLCH/`color-mix` reproduce T9's references, §5.4's trial numbers (± 0.02),
  and Chrome's painted dark `accent`, `primary-hover` and `hover-on-muted` over muted (± 1/255 a channel, from a
  screenshot pixel). A mismatch: find the cause (workflow §8); never move a threshold.
- **EC4 — CVD.** Machado 2009, severity 1.0, protan and deutan, on linear RGB, reproduce the trial's ink ↔ red and
  spark ↔ red CVD figures (± 0.005). If not: keep the normal-vision checks, drop the CVD ones, report why.
- **EC5 — the spark's utilities.** `bg-spark`, `border-spark`, `outline-spark`, `fill-spark` generate rules with their
  variants (`data-on:border-spark`, `after:bg-spark`, `data-[active=true]:before:bg-spark`) in the dev server and the
  production build (grep the built CSS), and `cn` keeps them beside other colour classes. Fallback: `--color-spark`
  in `@theme`, and SD2's rule also refuses `text-spark`; T11 then asserts that rule instead.
- **EC6 — the logo's form.** At `h-10` it measures 110 × 40 (± 1), at `h-9` 99 × 36, the mark at `size-9` 36 × 36; in
  the drawer's column it sits at the inline start in both directions; the component's mark at 64 px matches
  `masaha-mark-berry.svg` at 64 px (≤ 1 % of pixels differing by more than 8/255). Fallback: clip paths with `useId`
  ids, escaped for `url(#…)`.
- **EC7 — the first download.** Record its compressed JS size from the production build's output before C6 and
  after C7; report the difference; `check:build` passes.
- **EC8 — the icons, served.** In the dev server and `vite preview` of the build: `/favicon.svg`, `/favicon.ico`,
  `/apple-touch-icon.png` answer with their types; Chrome takes the SVG and switches it under
  `Emulation.setEmulatedMedia` prefers-color-scheme. After the merge (the owner or the supervisor): production's
  `/favicon.svg` answers `image/svg+xml`, not `index.html`.
- **EC9 — the rasters.** Made as §7.5 says; T15 reads them; each opened in Chrome and looked at (16 px legible as "a
  room with two people", the 180 px square, the 120 px with clear space).
- **EC10 — muted grounds.** Search features and pages for a ghost or outline Button, or a `hover:` class, inside a
  `bg-muted` / `bg-secondary` container; each takes `hover-on-muted` as D1; list them.
- **EC11 — axe in Chrome.** Inject `node_modules/axe-core/axe.min.js` (present; no dependency) into each visual-pass
  page, light and dark; report every violation, colour contrast included.
- **EC12 — Google's facts on the day.** Re-read *Manage OAuth App Branding* before the owner uploads (§16).
- **EC13 — the prototype beside production.** Serve `docs/design/prototype` (`python -m http.server <free port>`),
  the same screens at 1440, light and dark; the primary button, the sidebar's current item, a chip on, a hover:
  computed colours equal.
- **EC14 — 360 px.** The site's header (menu, logo, language, avatar) fits at 360 with no overflow, in both languages.

---

## 13. Verification (phase 4) and the visual pass

**Order, one heavy run at a time** (1–3 GB free): `npm run lint` · `typecheck` · `format:check` · `check:classes` ·
`check:links` · `check:conflicts` · `test:unit` · `test:component` · `test:api` · `NODE_ENV=production npm run build`
(this folder's `apps/web/.env` sets `NODE_ENV=development`) · `check:build` · the prototype's two checks · the visual
pass. **A lane killed for memory: retry once when the machine is quieter; killed again — record it, carry on, and CI
on the pushed head judges** (said in the PR and the report). Lint and typecheck on every commit.

**The visual pass (T23).** API and web from this folder (3323, 5323; browse `http://localhost:5323`, not `[::1]`),
the prototype on a free port. One headless Chrome at a time over CDP (a scratchpad script, as the earlier tasks did:
a random debug port, `about:blank` between loads, sign in per run via `/login?next=…`, at most ~25 reloads per 15
minutes, RTL captured by the viewport only, Radix menus opened by Enter, a loading state by holding a request with
`Fetch.enable`, «+N» by adding photos to a response with `Fetch.fulfillRequest` if the demo has fewer than six).
- **Screens:** Home; the directory (cards, the subscription choice and filters set); its map with a mark selected; a
  space's page (gallery, contacts, today's hours); sign in, register, forgot; `/me` and the favourites; the phone menu
  open; the desk (owner) with the check-in dialog; Payments with «إلغاء الدفعة» open; the owner's overview; the
  owner's space profile (a Sheet open, the photos with «+N», a contact lifted by the keyboard); Finance (charts,
  heatmap); a date picker open (a range); the admin's overview, spaces and a space's editor; a loading state; the 404;
  the owner's rail and the admin's rail (768) and drawer (390).
- **At** 390, 768 and 1440, Arabic and English, light and dark; the header also at 360 (EC14).
- **Each load checked:** console errors; a computed-colour scan of every element (colour, background, border,
  outline, fill, stroke, shadow) for Sea's 22 values (its `brand` and `neutral` ramps, §4 at `main`); no element with
  the spark as its text colour; no button with the spark; every visible text against its painted ground; the focus
  ring after three Tabs, on the page, a card, the sidebar, a Sheet and a dialog; overflow; the logo (file, size,
  `transform: none`, its name); the status colours sampled (light #BE222A #137D41 #B27406 #1F6CB0, dark #FC6E68
  #63B77C #D6912B #64A6E9); axe (EC11).
- **Hover vs selected, with a real pointer** (`Input.dispatchMouseEvent`), 1440, light and dark: a desk row, a
  sidebar item beside the current, an outline button, a menu item, a chip beside a chip on, the subscription choice,
  the desktop tabs, a sort header, FilterTag's remove, today in the calendar, a contact tile, a space card.
- **The prototype beside it** (EC13). The icons (EC8, EC9).
- **Screenshots:** curated to `C:\Users\basel\Downloads\identity-prod-shots\` (about 30: each screen once light-ar-390
  and dark-en-1440, the hover set, the rails and drawers, the logo close up); never committed.
- **Afterwards:** every server stopped by its PID; ports 3323, 5323 and the prototype's free.

---

## 14. Decisions for the owner (`OD…`)

### 14.0 The size, estimated before the shape

| Area | Files | New | Commits |
|---|---|---|---|
| Tokens (`primitives`, `semantic`, `tailwind`, the token test) | 4 | — | C1 |
| The layer's components (Button + test, Calendar, DropdownMenu, Select, Combobox, Table, DataTable, Input, ToggleGroup, Tabs, SegmentedControl, Sidebar + test, FilterTag, Skeleton, `leaflet.css`, Logo × 4, the index) | 22 | 4 | C2–C6 |
| The build check (`checkClasses.ts` + test) | 2 | — | C2 |
| Features and pages (six card hovers, four #143 files, four link files) | 14 | — | C2–C5 |
| Shells (four) and their tests (three) | 7 | — | C7 |
| Showcase | 7 | 1 | C2–C6 |
| The browser's icons (three files, `index.html`, the test) | 5 | 4 | C8 |
| The API's e-mail and its test | 2 | — | C9 |
| Documents (foundation, ADR 0019, the map, `setup.md`, `CLAUDE.md`, finding 219, the index) | 7 | 2 | C1–C8, C11 |
| The prototype (OD5 (a)) | 6 | — | C10 |
| **Total** | **76** | **11** | **11** |

Ten test files (two new); 24 tests in the matrix. **Verification:** every check and the four lanes once each, the
production build and `check:build`, the prototype's checks, three rasters, and the visual pass — about 20 states ×
3 widths × 2 languages × 2 themes (≈ 240 loads), plus ≈ 25 hover shots, the rails and drawers, ≈ 20 prototype loads:
about 300 loads, one Chrome at a time. The code is roughly half the work, the verification the other half.

- **OD1 — how it executes.**
  - **(a) One executor session builds it all, in commit order** — *recommended.* The edits are many but small (most
    1–5 lines) and one rule set must be applied the same way everywhere; the heavy part — the lanes, the build and a
    ~300-load visual pass — is serial on this machine whatever the shape; lanes would all need `foundation.md`'s rows
    and the tokens (the lead's), so the lead would write every document anyway and review every lane's diff; three
    sub-agents' briefs and joins cost back most of the time they save.
  - **(b) A lead and three sub-agents** — if the owner wants it faster. The lead builds and commits **C1 and C6**
    (tokens, roles, utilities, the token test, the logo and `SidebarHeader`'s API, foundation §3–§5 and §16, ADR 0019,
    the map), runs lint, typecheck, `test:unit` and the build green, then:

    | Lane | Commits | Files | Tests and breaks | May not touch |
    |---|---|---|---|---|
    | A — components | C2, C3, C4 | the layer's components but Skeleton and Logo, `leaflet.css`, `checkClasses.ts` + test, the features' hovers and links, #143's ContactsSheet, ContactsView, PhotosEdit, the showcase's Nav, Sortable and Field sections | T12, T20; `test:component` of its files only | tokens, `foundation.md`, `setup.md`, `CLAUDE.md` (the lead folds their lines into A's commits), shells |
    | B — shells and fixes | C5, C7 | Skeleton, #143's PhotosView, SiteHeader, SiteMenu, FocusLayout, AdminLayout and their tests | T18, T19; their files' tests | the layer but Skeleton, tokens, documents |
    | C — outside the web's source | C8, C9, C10, C11 | `apps/web/public/`, `index.html`, `browserIcons.unit.test.ts`, the API's e-mail, the prototype, finding 219 | T13–T15, T22, T24 | `apps/web/src`, `foundation.md` (§16's icon lines are the lead's) |

    Each lane's prompt is written by the lead, self-contained; at most three sub-agents (the prompt's cap, workflow
    §10); the full lanes, builds and the visual pass are the lead's, one at a time; the lead joins A, B, C by rebase
    in that order, folds a fix into its commit, and keeps the commits of §15.
- **OD2 — the PRs.**
  - **(a) One PR** — *recommended:* every merge deploys; the identity, the logo, the icons and the e-mail change
    together; the prototype's commit is docs only and rides along.
  - (b) Two: the identity PR, then a docs-only PR for the prototype (C10) — a smaller review, no effect on the site.
  - (c) More — rejected: any split of the web or the e-mail leaves the live site half Sea.
- **OD3 — the owner's and reception's shell.**
  - **(a) No platform logo** — *recommended (the supervisor's):* its head is the space's own (the switcher, the
    space's initial); the tab icon and the site's header carry Masaha.
  - (b) The small mark at the sidebar's foot, beside «الصفحة العامة».
  - (c) The full logo above the switcher (changes that shell's layout).
- **OD4 — the raster icons.**
  - **(a) The executor renders them in headless Chrome and packs the `.ico` with a scratchpad script** —
    *recommended:* reproducible from the committed SVG, no dependency, no wait; the owner looks at them in the PR.
  - (b) The owner exports them in Figma (Axis 6) and hands them over before execution.
  - (c) No `.ico`: the SVG favicon and the 180 px PNG only (older browsers and `/favicon.ico` requests get nothing).
- **OD5 — the prototype after production.**
  - **(a) Berry becomes its default; `?identity=sea` and `?identity=slate-coral` compare** — *recommended:* the
    prototype is the living design features are built from; left on Sea, the next feature would read a look
    production no longer has. Files: §7.7.
  - (b) Sea stays the default; a line in `CHANGES.md` says production is berry.
- **The stronger decisions SD1–SD10 and the design issues D1–D5** are approved with the plan, or struck one by one.

---

## 15. Commits

On `feat/ink-berry-identity`, cut with `git switch --no-track -c feat/ink-berry-identity origin/main`. Staged by path,
`git status` before each; no tool attribution; `#PRNUM` in documents, replaced just before the push (§17).

1. **`feat(design-system): adopt ink and berry identity`** — primitives (neutral, spark; `brand` removed), the remap
   and the new roles, the `skeleton` token, the utilities, the token test (T1–T11), foundation Status, §4, §5 (values,
   roles, verified, the spark's rules, the scrim), §15 row 1, ADR 0019, the map. *Body:* why two roles, why hover is
   its own, the trial's numbers now tests.
2. **`feat(design-system): tell hover from selected`** — §7.1's C2 rows (the layer, the features' card hovers, #143's
   handle and tiles, the showcase's nav and handle), `check:classes`' rule (T12), foundation §3, §5 rule, §11, §12
   rows, `setup.md`, `CLAUDE.md`. *Body:* the tint meant both; the wash for muted grounds; the rule for future copies.
3. **`feat(web): underline links in running text`** — the link Button, RegisterPage, AboutPage, SiteFooter,
   MissingChecklist, FieldSection, T20, foundation's Button row and rule. *Body:* ink links read as text unless underlined.
4. **`feat(design-system): mark what matters in spark`** — Tabs' line indicator, the map's selected mark, the lifted
   item (ContactsSheet, PhotosEdit, SortableSection), §12 rows. *Body:* where the spark shows and why only there.
5. **`fix(web): raise the skeleton and photo count`** — Skeleton on `skeleton`, PhotosView on `scrim`, §12's
   Skeleton row. *Body:* 1.11 → 1.27; 3.64 → ≥ 4.5 over any photo.
6. **`feat(design-system): add the logo`** — `display/Logo` (T16), the index, `SidebarHeader`'s mark and logo (T17),
   the showcase's Logo section and SidebarSection, foundation §3's category row, §12's Logo row, §15 row 5, §16 (the
   forms, sizes, rules of use), the map's foundation line. *Body:* inline, on the tokens, so it follows the theme.
7. **`feat(web): show the logo in every shell`** — SiteHeader, SiteMenu, FocusLayout, AdminLayout (T18, T19), §16's
   "where it shows". *Body:* the owner's places; OD3's answer.
8. **`feat(web): add the favicon and home-screen icon`** — `apps/web/public/`, `index.html`, T13–T15, §16's lines on
   the browser's icons. *Body:* none before; how they were made; why the hexes live there.
9. **`feat(auth): draw the reset email in ink`** — `resetEmail.ts`, T22. *Body:* finding 19's "carried by hand".
10. **`docs(design): make berry the prototype's default`** — §7.7 (OD5 (a)). *Body:* the design source matches
    production; Sea and coral stay to compare.
11. **`docs(findings): record the readme's sea shots`** — finding 219 and the index.

Eleven commits for ~75 files: each a unit with its code, tests and documents (workflow §3).

---

## 16. Google Branding — the owner's steps (no code)

After the PR merges, so the site already shows the logo:
1. Google Cloud console → *Google Auth Platform* → *Branding*: upload `masaha-logo-120.png` (square 120 × 120, under
   1 MB; JPG, PNG or BMP accepted) from `C:\dev\masaha\workspace\TASKS\IDENTITY\google\`.
2. Check the page's other fields: the app's name as the site shows it, the home page, the privacy policy (`/privacy`,
   the same address the home page links), the authorised domains.
3. The app is external and in production, so **a new logo goes through Google's verification first**: Google's page
   says branding cannot be edited while it runs, and that without verification only the app's domain is shown.
   Sign-in with Google keeps working meanwhile.
4. Verification needs the domain verified in Google Search Console — whether the site's current address can be is the
   owner's check (EC12). If Google refuses, its message names what to fix.

---

## 17. The PR, the report, the limits

- **PR** (`open-pr`): title = commit 1's subject; assigned to the owner; labels `feat`, `area:web`,
  `area:design-system`, `area:api`, `area:docs`, `area:ci` (SD2); the description per workflow §3 (Summary, Scope /
  Acceptance criteria / Out of scope, Change type, Evidence naming each command and what was not run, Screenshots from
  the Downloads folder attached by the owner, the DoD checklist). Over 25 files and a build check: a separate review
  conversation (workflow §2, phase 7).
- **`#PRNUM`:** just before the push, read the last issue/PR number (issues share the sequence), replace it in every
  commit's tree (`git filter-branch --tree-filter "sed -i 's/#PRNUM/#144/g' <files>" origin/main..HEAD`, then delete
  `refs/original/`), grep it to zero, push (`git push -u origin feat/ink-berry-identity`) and `gh pr create` at once;
  confirm the number it got.
- **Report** (`final-report`), once CI is green on the pushed head and GitHub shows `CLEAN`: to the file the execution
  prompt names (suggested `TASKS\IDENTITY\3_REPORT_PROD.md`); the head and commits, what ran and what did not, the
  breaks made, problems and their solutions, anything unexpected, the file count, EC results, `git merge-tree` against
  any other open PR, departures from this plan.
- **Limits:** no migration; no dependency; **never `db:seed` `masaha_dev`**; stage by path, never `git add -A` / `.`;
  no push to `main`, no merge, no force-push of another branch, no secret printed; never stop on file count — report
  it; review fixes fold into their commits (`backup/*` first); public text never names hosting providers, free plans
  or session durations.

---

## 18. Risks

| Risk | Mitigation |
|---|---|
| A missed accent-as-hover in a feature | SD2's rule fails the build; EC1's inventory |
| More controls on muted grounds than D1 lists | EC10; the dark hover set of §13 |
| The test's colour maths wrong, so the tests prove nothing | T9's references, EC3 against Chrome, EC4 |
| Custom spark utilities not generated | EC5 and its fallback |
| #143 changes or is late | EC1 stops the start |
| A lane killed for memory | the retry-once rule; CI judges |
| Google's verification holds the branding | the owner's steps after merge; sign-in unaffected |
| The logo's paths weigh on the first download | EC7 measures; PA4 optimises later |
| A screen outside the matrix looks wrong | the token-level guarantees (every role passes in both themes); findings for what the pass sees |

---

## 19. Proposed alternatives (challenges — none built without approval)

- **PA1 — keep the trial's dark hover (`muted`) but fix the muted grounds** (SD6/D1), rather than a lighter dark
  hover: the owner's value stands.
- **PA2 — the skeleton on its own token at the hover's steps** (SD4) rather than `bg-hover` literally.
- **PA3 — a web app manifest with 192 / 512 px icons:** not now (no PWA in v1; the touch icon covers iOS).
- **PA4 — optimise the logo's paths** (an SVGOMG pass at precision 1–2, by the owner): could halve its weight in the
  first download and the favicon; later, after looking at the result large.
- **PA5 — `theme-color` from the app's own theme:** needs the pre-paint script and its CSP hash; not now.
- **PA6 — mix the destructive hover in OKLab:** its OKLCH path toward the new ink bends the red slightly toward
  magenta; *recommend keeping* the trial's look, approved by the owner; the visual pass looks, and if it reads pink
  it is one class.
- **PA7 — a logo in the reset e-mail:** not recommended (images blocked by default in many clients; a hosted image ties
  the e-mail to the site's address).
- **PA8 — the lifted mark drawn by the layer's Sortable** (two callers now draw it): a follow-up, not here.
- **PA9 — the trial's "wordmark in spark":** obsolete; the logo's dots carry the spark.
- **The trial's own items, answered:** *two fixes* → `primary-hover` (SD3); production has no drawn covers, and its
  mixes keep OKLab where hues differ. *Defects fixed* → the chip's edge (`data-on:border-spark`), hover ≠ selected
  (C2), the drawer's logo (`self-start`, EC6). *For the owner* → skeleton and «+N» (C5), coral's tint (not in
  production), the map drawing (production has a real map), the shell (OD3). *Proposed alternatives* → hover role
  (adopted), dark tint at 900 + 30 % (adopted), spark ↔ red criterion (T8), wordmark in spark (PA9).

---

## 20. What changes on the merge day

- **Visitors (the public site, signed out or in):** teal gives way to ink: buttons, links (now underlined in running
  text), the map's single pin and the visitor's dot; neutrals turn a cool slate instead of a teal-grey, light and dark;
  the header, the phone menu and the sign-in, register, forgot and reset pages show the logo («مساحة» over "MASAHA",
  berry dots) in place of the teal word — in English too; the browser tab gets an icon for the first time, and an iPhone
  "add to home screen" its square icon; hover fills are grey and plainly visible; a filter on or a selected map mark
  carries berry; loading placeholders are darker; the space's verified line is ink with its icon.
- **Owners and reception:** the sidebar's current page is a berry tint with a 3 px berry bar on its inline start; its
  counts are berry; primary buttons and checked boxes are ink; the line tabs' indicator berry; the first chart series
  berry, the heatmap and the occupancy meter in ink; hovering a row, a menu item or a card shows grey, never the tint;
  the profile's «+N» is darker and a dragged photo or contact has a berry edge; their sidebar head is unchanged (OD3).
- **The admin:** the same, and the sidebar shows the logo in place of the «م» tile, the small mark on the tablet rail.
- **The reset e-mail** (sent after the merge): ink button, ink text, no teal.
- **Unchanged:** the status colours (green, amber, red, blue), every word, layout and behaviour; Google's consent screen
  until the owner's branding passes; the README's screenshots (finding 219); the design archive's `screens/`.
