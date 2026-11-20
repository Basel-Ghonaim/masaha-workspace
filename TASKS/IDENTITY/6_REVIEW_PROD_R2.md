# Review of #144 (R2 — the logo and the rest) — Claude Code, Opus 5.5
Head: 4cff26c7de4ea1b4b8454ad48f1f440b9a0ae84b · commits 12 · files 81 · checks: green (run 43440252687: ten jobs pass, CodeRabbit skipped; GitHub `CLEAN`) · head moved: no (re-read at the end: same head, `CLEAN`, open)
Verdict (my role): **mergeable** — five nits, none serious. They can go into the next PR's first commit (named in its description), or be folded into their commits if R1's findings open a fix round.

## Findings (verified defects only, most severe first)

### F1 — nit · T14 checks the favicon's stylesheet, but not that its shapes use those classes
- **Where:**
  - `apps/web/scripts/browserIcons.unit.test.ts:65-78` (T14);
  - `apps/web/public/favicon.svg:8-10` (the two `<use … class="ink">` and the dots' `<path class="spark">`).
- **Seen in the code.**
- **Scenario:**
  - Drop `class="ink"` from either `<use>`, or `class="spark"` from the dots. That shape falls back to the SVG default fill, black, in both schemes, so it is black on a dark tab bar.
  - T14 still passes. `fills()` reads only the `<style>` rules. The "no colour but these four" set cannot see a default fill, because no hex is written for it.
  - The test's title, "the SVG favicon draws ink #1a1f25 and spark #b55bb3 …", claims more than the test proves (testing §3 rule 6).
  - Only the visual pass's pixel match (EC9) guards against this today.
- **Fix:** T14 also asserts that each drawn shape names its class:
  - both `<use>` carry `class="ink"`;
  - the dots' `<path>` carries `class="spark"`;
  - no `<use>` or `<path>` outside `<defs>` is left without a class.
- **Belongs:** the next PR's first commit, or folded into `b4cf3236`.

### F2 — nit · No test proves which logo form the admin shell gives each sidebar mode
- **Where:**
  - `apps/web/src/pages/dashboard/shell/AdminLayout.tsx:23-24`;
  - T19, `apps/web/src/pages/dashboard/routes.component.test.tsx:377-393`.
- **Seen in the code.**
- **Scenario:** swap AdminLayout's `mark` and `logo` props, or drop `form="mark"`.
  - The 64 px rail (`w-16`) then draws the 99 × 36 full logo, which overflows it. The expanded sidebar draws the square mark instead of the full logo.
  - Every test stays green:
    - T17 proves only the Sidebar's own branch, with placeholders;
    - T19 runs at 1280 and checks `aria-hidden`, the name and the caption, never the form.
  - testing §2 gives "dashboard wiring" to the component lane. Lane B named this gap (`REPORT_B.md`, «Found, not fixed»), and the lead's report does not carry it.
- **Fix:** T19 asserts the header's logo has the full form's `viewBox` (`263 45 2473 903`) at 1280, and a second case at 800 asserts the mark's (`190 17 778 778`).
- **Belongs:** the next PR's first commit, or folded into `4c732ea5`.

### F3 — nit · The prototype's reset e-mail still shows Sea's tab icon
- **Where:** `docs/design/prototype/Reset email.html:5` links `masaha/favicon.svg`: a `#02787d` tile with «م».
- **Seen in the code.**
- **Scenario:**
  - This PR redrew the page in ink (C10), and berry is now the prototype's default (OD5 (a)). Its tab still shows Sea's teal tile.
  - The page loads no `i18n.js`, so the swap to the identity's mark never runs.
  - Lane C reported it («Not changed (outside the brief)»), and the lead's report lists it as "Noted". It was neither fixed nor recorded (workflow §8: an observation is recorded).
  - It is the design archive, not production, so it is not a blocker.
- **Fix:** link `masaha/logo/masaha-mark-berry.svg`. The page declares `color-scheme: light`, so the light mark is enough.
- **Belongs:** folded into `1111a22f`, or the next PR's first commit, or finding **226**.

### F4 — nit · The PR description gives the layer chunk's growth as the first download's
- **Where:** PR #144's description, *Evidence*: "The first download grows by 15,672 bytes (+8,079 compressed)".
- **Only in a report** (the PR body, `runs\pr-body.md:111`).
- **Scenario:**
  - The measurement (`runs\ec7-after.txt`; `LEAD_LOG.md:171-173`) gives the first download at 1,121,394 B (gzip 334,832), against `main`'s 1,105,713 B (gzip 326,759). That is +15,681 B, +8,073 compressed, as `4_REPORT_PROD.md`'s EC7 says.
  - 15,672 and 8,079 are the `design-system` chunk's growth (293,137 → 308,809; gzip 84,458 → 92,537).
  - So the PR and the report disagree, and the PR's figure names the wrong thing.
- **Fix:** write +15,681 / +8,073, or say "the layer's chunk grows by".
- **Belongs:** the PR description (no commit).

### F5 — nit · foundation §16 lists a dark app icon that does not exist
- **Where:** `docs/frontend/design-system/foundation.md:562`, «(`*-berry.svg`: the full logo, the mark and the app icon, light and dark)».
- **Seen in the code:**
  - `docs/design/prototype/masaha/logo/` holds `masaha-logo-berry`, `-logo-dark-berry`, `-mark-berry` and `-mark-dark-berry`;
  - it holds one app icon, `masaha-app-icon-berry.svg`, and no dark app icon.
- **Fix:** «the full logo and the mark, light and dark, and the app icon».
- **Belongs:** the next PR's first commit, or folded into `199f9da8`.

No defect found outside my role.

## The test matrix rows of my role (present / missing / weaker · would it fail on its break?)

| # | State | Would it fail on its break? |
|---|---|---|
| T10 | present (`semantic.unit.test.ts:179-183`, by hand) | yes: a step moved off the logo's, favicon's or `theme-color`'s hexes. The colour maths is R1's |
| T13 | present (adds the links' order) | yes: a link dropped or renamed, a file missing (break made: the SVG link dropped) |
| T14 | **weaker than its title** (F1) | yes for its planned breaks: the dark rule lost (made), a colour off. No for a shape that loses its class |
| T15 | present | yes: a 32-only `.ico` (made), a wrong PNG size. The 180's opaque ground is seen only in EC9 |
| T16 | present (7 tests) | yes: name dropped, not hidden, `rtl:-scale-x-100`, the dots on `fill-primary`, a cropped frame (all made). A mirror that does not depend on direction would pass. EC6's pixel match covers it (0 of 4096 px) |
| T17 | present (3 tests) | yes: the mode branch swapped (made; 3 red) |
| T18 | present: header in both languages, phone menu, focus shell | yes: the text wordmark back, the logo without `label` (both made) |
| T19 | present, **weaker than the wiring it heads** (F2) | yes: the «م» tile back, the name read twice (both made). No for the forms swapped |
| T21 | present: Logo's axe test; lane B's 10 files, including axe-clean Home and About with the header | n/a. No axe test renders the admin's header; T19's assertions stand in |
| T22 | present | yes: a Sea hex, the underline removed (both made), the button cell and its label |
| T23 (my parts) | done — **only in a report**: EC6, EC8, EC9, EC14, and the re-check of F3 | n/a |
| T24 | present: `check-parse` 52/52, `check-classes` 0 new | ran on `4bf65b66`. `git diff 4bf65b66 <HEAD> -- docs/design` is empty, so it stands for the head |

The Logo's drawing is the owner's, checked by hash at `<HEAD>`:
- `WORDS` and `DOTS` in `drawing.ts` equal `masaha-logo-berry.svg`'s two paths (git blob `2438c109…`, `d920bfa8…`);
- `favicon.svg`'s words and dots equal them too;
- the mark's viewBox, the clips `h` (250 240 329 540) and `d` (400 50 380 200), `translate(1158 0) scale(-1 1)` and `translate(-11.5 0)` equal `masaha-mark-berry.svg`'s.

## Decisions, ODs, SDs and Ds of my role (built / departed, judged)

**The owner's decisions**
- **I4, the logo:** built.
  - Full logo, 40 px, named, as the link home in the site's header (`SiteHeader.tsx:26-31`) and the focus shell (`FocusLayout.tsx:25-30`).
  - At the head of the phone menu (`SiteMenu.tsx:51`, `self-start`).
  - In the admin's sidebar in place of the «م» tile: full logo 36 px expanded and in the drawer, mark 36 px on the rail, both decorative beside a `sr-only` name.
  - The browser tab: the mark.
  - Never mirrored: no `rtl:` class, no icon wrapper, and no mirroring rule anywhere in the layer's CSS (searched).
  - Named «مساحة» / "Masaha" by `copy.site.wordmark`, so it follows the language.
- **OD1 (b):** built (lanes A–C, then a fourth sub-agent for the visual pass once they had ended). Sound.
- **OD2 (a):** one PR. Built.
- **OD3 (a):** built. `SidebarHeader`'s only production caller is `AdminLayout`; the owner's and reception's head is unchanged.
- **OD4 (a):** built. The rasters were made in headless Chrome and packed by a scratch script, and no dependency was added (no manifest or lock file in the diff).
- **OD5 (a):** built.
  - `i18n.js`: no `?identity=`, or an unknown one, gives berry; `sea` gives the bundle's own Sea; `slate-coral` gives coral.
  - A link carries the identity only when it is not the default.
  - One page is left behind: F3.
- **The no-conflict rule:** only in the report. The history was rewritten after #143's merge, so it cannot be checked now.

**SDs**
- **SD9:** built. `SidebarHeader({ mark, logo })`, both required; the rail shows `mark`, desktop and the drawer `logo`.
- **SD10:** built. The logo's link takes the layer's focus classes exactly, with `rounded-sm`.
- **SD2's document lines** (`setup.md`, `CLAUDE.md`, in `e1cc1a7f`): present. The rule itself is R1's.

**Ds**
- **D2:** built. The 180 is the mark on opaque white, full bleed; I viewed it, and its margins match the owner's app-icon framing.
- **D3:** built, per lane C and EC9. The `.ico` is the app icon on its white tile, with transparent corners. The `.ico` itself was not viewed by me.
- **D4:** built and not committed (`google\masaha-logo-120.png`, viewed). The mark at 96 px is centred on white, with clear space for a round crop.

**Stated exceptions:** the hexes in the icons, `theme-color` and the e-mail are written in foundation §16 and in ADR 0019's consequences, and held by T10, T13, T14 and T22. As the plan said.

**Plan §7.6, the e-mail:** built. Its colour set is exactly {#f7fbff, #ffffff, #dde5ed, #1a1f25, #5e646a}, with `text` and `ink` kept apart. The English link is underlined; the "link as text" paragraphs are ink; there is no spark and no image.

## The report's deviations, judged (all)

**The prompt's own (1–6):** sound, as instructed. 220 replaced 219, and the commits keep the plan's units with C1 and C6 first.

**The owner's and supervisor's updates**
- **C11 records 220 and 221:** sound. Both were checked against the code at `<HEAD>`, and `useSpaceEditorActions` does return nothing only while `query.data` is `undefined`.
- **Commits 10–12 accepted by docs-only proof:** sound.
  - `git diff 37ef1039 <HEAD> -- . ':!docs'` is empty.
  - `eslint.config.js:249` ignores `docs/design/`.

**The lead's (LEAD-D…)**
- **A twelfth commit (222–225):** sound. The plan's six numbers are kept, shifted (220–225). Each finding was checked at `<HEAD>`:
  - `PhotoTile.tsx:32` `overflow-hidden`;
  - `Heatmap.tsx:88` `<table className="sr-only">`;
  - `LeafletMarkerMap.tsx:217` `<Tooltip>`;
  - `PhotosView.tsx:44` `overflow-x-auto`;
  - none of the four test files calls `warm`.
- **OKLab for `primary-hover`, `overlay-scrim`, the secondary hover and the prototype's primary hover (D4):** sound. EC3 measured the cause in Chrome; the reason is written in foundation §5, CHANGES and the commit; destructive stays OKLCH, with its reason. The maths is R1's to judge.
- **SiteMenu and LiveStatusControl beyond §7.1 (F3, F4 of the visual pass):** sound. Both serve the plan's own acceptance criterion, hover ≠ selected.
  - SiteMenu's `matchPath` agrees with NavLink's current page for all three `SITE_LINKS`: home has `end: true`, the other two are prefixes.
  - `variant={null}` drops cva's default variant, as intended.
  - LiveStatusControl's neutral trigger losing its open-state fill is acceptable, and it is listed under Review Focus.
- **The lifted photo's edge drawn inside the picture (F2):** acceptable. Inside is the only place the frame's `overflow-hidden` leaves visible. It was never seen over a real photo, because the photos answer 404 locally; R1 can weigh it.
- **T8 covers `sidebar-accent` too (D3):** sound (stronger).
- **Lane C renders the rasters inside C8 (D2):** sound. It owns `public/` and T15.
- **One known red between C6's two parts (D1):** acceptable. It is not in the final history: `199f9da8` carries the index export, the registry entry and the Logo section together.
- **The visual pass by a fourth sub-agent, and its re-check:** sound. The prompt allowed it.
- **EC2's `pal-hub` instead of `masaha-demo`:** acceptable. The demo set was present, and the substitution is recorded.
- **The prototype checks reused at the head:** sound. Their tree has the same `docs/design` as `<HEAD>`.
- **The grant script's changes (D8):** outside the repository. Acceptable.

**Also judged**
- **Per-commit lint and typecheck ran on the pre-rewrite chain `502e2ca3…5fa394d3`:** sound. Each of the nine commits has the same tree as its counterpart at `<HEAD>` outside `docs/` (`git diff --stat` empty for all nine pairs).
- **`test:unit` and `test:component` ran at `5e8a3b7b`:** acceptable. It differs from the head by `#PRNUM` → `#144` only, and CI ran every lane on `<HEAD>`.
- **EC7 above the plan's estimate** (+8,073 B compressed, against 5–6 KB): acceptable. It is fixed path data with no library, recorded, and `check:build` has no budget; PA4 (optimising the paths) is the owner's later call. The PR states the figure wrongly (F4).
- **EC13 not re-measured after F1:** acceptable (R1's area).
- **The lanes' own decisions:** sound. Lane B wrote T19 in Arabic and strengthened T18 in place. Lane C made an unknown `?identity=` give berry, used SVG 2's `href` on `<use>`, and added extra assertions.

## Documents
- **foundation §16:** true to the code: the forms, where each shows, the sizes (`h-10`, `h-9`, `size-9`), the clear space (8 px measured in the 56 px header and at 360) and the two stated exceptions. The one error is F5.
- **foundation §3, §12, §15:** §3's `display` row and §12's Logo and Sidebar (`SidebarHeader`) rows match the code. §15 row 5 is settled.
- **ADR 0019:** short and decision-level, with no file names or code (*Context · Decision · Alternatives · Consequences*).
- **The map:** lists ADR 0019, and foundation's line names the logo.
- **Findings 220–225:** in 219's format and appended to the index, with their evidence checked at `<HEAD>` as above.
- **The design archive:** the CHANGES section, the INDEX row and the SCREENS line are right. INDEX keeps the heading «Identity trial — ink + spark» above a row that now names production's default; this was lane C's decision, and is acceptable.
- **«The wordmark»:** `docs/frontend/architecture.md:85,90` and `docs/features/users.md:50,99` still say it. The logo is a wordmark, so they stay true, as the plan said.
- **The PR description:** complete per workflow §3, except F4.

## Scope and commits (R2)
- **The commits:** 12, the plan's eleven units plus the findings commit.
  - Each carries its code, its tests and its documents. The joins put foundation's lines in the right commits (§16's parts in C6, C7, C8 and C9), and `CLAUDE.md` and `setup.md` in `e1cc1a7f`.
  - Subjects are ≤ 50 characters. There are no trailers and no tool attribution (bodies searched).
- **The files:** 81, every one a plan row or a recorded deviation.
  - Nothing outside the scope: no dependency, migration, `packages/shared` or API contract change.
  - `MissingChecklist` is gone with #143, as EC1 says.
- **Placeholders and numbers:** no `#PRNUM` left; `#144` appears in two documents.
- **No Sea in production:** none of Sea's 22 primitive hexes is anywhere in `apps/`, `packages/`, the e-mail's design or the logo files.
- **No private or provider names:** the diff names no private name, hosting provider or plan.
- **The conflict check:** #144 is the only open PR, so there is nothing to `merge-tree` against.
- **The PR itself:** labels `feat`, `area:web`, `area:api`, `area:design-system`, `area:docs`, `area:ci`; assigned to the owner; titled with commit 1's subject.

## Not checked, and why
- **Nothing run** (no test, build, server or browser; the rules). Every visual fact comes from the reports only: EC6, EC8, EC9, EC14, and F1–F4's re-check.
- **The `.ico`** was not viewed. Its directory is held by T15, its pixels by lane C and EC9. I viewed the 180 and the Google 120.
- **The mark's clipping** was read, not rendered. The paths match by hash, and EC6 reports a 0-pixel difference at 64 px.
- **R1's areas** were not reviewed: the tokens and their maths, `check:classes`' rule, the hovers, the links, the spark marks, the skeleton and «+N». I read only the deviations that touch them.
- **The no-conflict rule** before #143's merge: only in the report, because the history was rewritten.
- **The lanes' and backup branches** were not inspected.
- **The production check after the merge** (`/favicon.svg` served as `image/svg+xml`) and **Google Branding** are the owner's, after the merge.
- **The logo in forced-colours (high-contrast) mode** is in neither the plan nor any pass.
