# Round 3 (design) — summary

> The design lead, 2026-11-14 (Opus 5.5, effort high), from `2_DESIGN_LEAD_PROMPT.md`, under the owner's R3-8 … R3-17.
> No repository edit, no git, nothing submitted on the live site. Everything is in `DESIGN\ROUND3\`.

## The diagnosis's headline

Masaha is correct, accessible and honest, but it has no point of view. It is shadcn/ui's default kit with ink and berry
dropped in:
- one white rounded card for everything (678 corners of 6/8 px on the measured frames);
- a timid type scale (13 px is the most used size; the auth pages' and the 404's h1 is 17 px);
- a template "Find X in Y" hero, and every section at the same weight;
- a spark that only paints the selected tint;
- the spaces' posters as the only imagery;
- a map that opens on the region, with Hebrew labels.

The copy and the truth rules are not the problem. Full text with the captures: `DIAGNOSIS.md`.

## The directions (`directions\`, open `index.html` first)

| | Idea | Learns from | Key overturns |
|---|---|---|---|
| **A «اللوحة» · The live board** | State first, in rows. An ink "board" with Gaza's clock, and the spark marks open now. | Google Maps lists, departure boards / Citymapper, Linear's density | §7 scale (font kept), U12 card → 64 px plate, Home's division, hours' today tint, OSM tiles, account side nav → tabs |
| **B «القطاع» · The Strip** | Place first. The Strip's silhouette is the identity's second mark: list and map side by side, Alexandria display. | Airbnb search, Apple Maps place cards, Google Travel | §9/U6 list-or-map → side by side, font (§7, §15), radius/density, filter sidebar → popover bar, U12, Home |
| **C «الدليل» · The guide** | Editorial. Governorates are chapters; each space has one sentence composed from its data, and an ink fact box. Amiri (Arabic) and Markazi Text (Latin) display over Plex. | Thmanyah, Monocle and Wallpaper* guides, FT fact boxes | font (§7, §15), U12, filter sidebar → refine panel + sentence, default order grouped by governorate, U8 page order, Home |

**All three keep** ink + berry, the logo, Arabic first, v1 and the truth rules. Each has a review panel with
«حالات تجريبية»: it shows the product's live states that today's data lacks, off by default. A builder's decisions are
under *Builder's notes* in its `DESIGN.md`; its account of the work is in its `REPORT.md`.

**Recommendation:** A as the base, with B's Strip drawing (the map, no-photo, 404, About) and C's composed sentence
(the space page's head). The reasons are in `FOR_THE_OWNER_AR.md`.

## How it was done

- **Phase 1, the before captures** (`before\`, 134 images + facts JSON):
  - public pages from the live site (paced, read only);
  - signed-in pages from app-dr (5336/3336, demo user; the forced change by rewriting the session answer's
    `mustChangePassword` in the browser, no DB write);
  - at 390 and 1440, in Arabic (English for the main ones), light and dark, viewport and full page;
  - tool: `tools\cap-before.mjs`.
  - The app-dr servers were stopped by PID afterwards; ports 3336/5336 are free.
- **Phase 2, the builds:**
  - Three sub-agents, one per direction, built from `directions\COMMON.md` + each `DESIGN.md` + `PROMPT.md`.
  - The data came from the live API: `data\`, copied to `directions\_shared\data`, plus `strip-outline.json`, the lead's
    schematic outline, with every space checked inside it.
  - Real photos and the logo are in `_shared\`.
  - Every Chrome run went through the grant script (`heavy.mjs`), one at a time; the capture-and-check tool is
    `tools\shoot.mjs`.
- **The quality gate:** I opened each direction's captures at 390/1440 (768 checked by the builders and the report), in
  Arabic and English, light and dark. `shoot.mjs` reports 0 overflow, 0 contrast failures, nothing under 12 px, no
  missing focus style and no console error on the final runs of all three. Each direction got one improvement round
  from my review:
  - **A:** the map outline, the empty location panel, the duplicated phone bar.
  - **B:** posters cropped into a wall of brands, so they now sit whole on a mat; the footer wrap.
  - **C:** its Arabic display face was silently falling back to Plex (Markazi's Arabic not served), so it switched to
    Amiri; the map was rotated, now north-up; the directory was too sparse.
  - I captured C's login, account, favourites and filters-open pages myself (`C\shots-lead\`, 48 frames, clean),
    because its round-2 run had replaced its folder.
- **Presentation:**
  - `directions\index.html`: each idea in two lines, the key screens at 1440 and 390, before/after for the directory,
    the map and sign-in, and links to every page. Captured clean at 390 and 1440, light and dark.
  - `FOR_THE_OWNER_AR.md`: the owner's summary in Arabic.

## Skills

- **Used, loaded with the Skill tool:**
  - `frontend-design`;
  - Vectorlab: `anti-slop`, `typography`, `spacing`, `surfaces`, `page-patterns`, `viewports`, `motion`.
- **The three R3-11 plugins** (Website Design, UI Design Review, Design) are **not in this session's skill list**,
  although the files are synced on disk. I read and applied them from disk: `landing-page`, `web-design-system`,
  `web-review`, `ui-review`, `ui-compare`, `ui-polish`, `design-critique`, `design-system`, `ux-copy`. The builders
  read `landing-page` and `ui-review` the same way.
- **Not used:** `brand-guidelines` was never used. UXKIN was not connected and was never asked for, so the comparisons
  name products from knowledge, no library.

## Not done, and why

- **The 5410 server.** The prompt's `python -m http.server 5410 …` was **refused by the session's safety classifier**,
  so I did not start it or work around it. The mock-ups were built to run from `file://` instead, and `index.html`
  works when opened directly. The owner can run the command himself (it is in `FOR_THE_OWNER_AR.md`).
- **Pages outside the eight mock-ups:** register, forgot/reset, the forced change and privacy have before captures
  only. In the mock-ups their links lead to a note or to the 404.
- **The map:**
  - Every map is a schematic SVG on an approximate outline, not survey data; its production equivalent is named in
    each `DESIGN.md`.
  - No governorate borders are drawn as fact.
- **Time of day:** the evening and after-hours states are coded from the real hours but were captured only in the
  afternoon (Gaza time).
- **Known nits left:**
  - A's dashed "no live status" bar is quiet on 7 of 13 rows today.
  - B's Gaza City pins cluster at whole-Strip zoom.
  - C's phone entries can break «30 ₪» across lines.
  - Some builders' early frames remain beside the final ones in their `shots\`; a builder's shell `rm` was refused, and
    I left them.
- **Next:** none of this is production code. The prototype and then the design system and pages follow the owner's
  choice, by later prompts.
