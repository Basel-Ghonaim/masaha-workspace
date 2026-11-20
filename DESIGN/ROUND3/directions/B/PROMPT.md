# Direction B — «القطاع» · The Strip: the builder's prompt

You are the builder of **direction B** in design round 3 for **Masaha (مساحة)**, a bilingual Arabic-first (RTL) /
English directory of coworking spaces in the Gaza Strip. A lead designer diagnosed the live site and wrote three
directions; you build this one as **real, interactive HTML/CSS mock-ups** for the owner to look at and choose from.
The owner's bar, in his words: **"a design I look at and am shocked by its quality and by the difference."**

## Read, in this order (all in `C:\dev\masaha\workspace\DESIGN\ROUND3\`)

1. `DIAGNOSIS.md` — what is wrong today and why it reads as AI-made (the "before" captures it cites are in `before\`;
   open a few: `home-1440-ar-light.full.jpg`, `spaces-1440-ar-light.full.jpg`, `space-1440-ar-light.full.jpg`,
   `map-1440-ar-light.jpg`, `home-390-ar-light.full.jpg`).
2. `directions\COMMON.md` — the fixed points (colours, the spark's rules, the logo, RTL, v1 scope, truth), the real
   content and where it is, the eight pages and their states, the technical rules (static, `file://`, no libraries),
   the quality gate and its capture tool, your limits, and your report.
3. `directions\B\DESIGN.md` — **your direction**: its idea, type, grid, surfaces, spark, imagery, icons, motion,
   density, components, every page's division, the decisions it overturns, its proposed copy. Build it faithfully.
   Where it leaves something open or you find a real problem in it, decide in its spirit and record what you decided
   and why in your report (and append it to the DESIGN.md under *Builder's notes*). Never cross COMMON.md's fixed
   points to do so.

## Skills (load them before you design; one that does not load — say so and go on)

Load with the Skill tool: `frontend-design:frontend-design`, `vectorlab-ux-skills:anti-slop`,
`vectorlab-ux-skills:typography`, `vectorlab-ux-skills:spacing`, `vectorlab-ux-skills:viewports`,
`vectorlab-ux-skills:motion`, `vectorlab-ux-skills:surfaces`. Read from disk (their plugin is not in every session's
skill list), under `C:\Users\basel\.claude\plugins\synced\a3277e10-26a7-4970-9a50-22644cf83ac0_a96b35c9-1b79-4362-a52a-df056bef17ac\`:
`1c733bea-1060-4a27-8c95-946337650cc0\skills\landing-page\SKILL.md` and
`3d633e8a-5eb0-4e7e-a7cc-826df3151b9c\skills\ui-review\SKILL.md`. **Never** `brand-guidelines`. No UXKIN (not
connected; never start its sign-in). A skill's advice that contradicts COMMON.md's fixed points or this direction's
DESIGN.md loses.

## Build, check, improve

1. Plan briefly (your tokens as CSS custom properties for both themes, the shared header/footer/review panel, the
   data file, the icon helper), then build all eight pages in `directions\B\`.
2. Check with the capture tool through the grant script, lane **`design-b`** (the command is in COMMON.md §4); Read
   the screenshots — at 390, 768 and 1440, Arabic and English, light and dark — and the report. Fix, re-check.
3. Before you report, do one honest pass as a senior designer with `ui-review` and `anti-slop`: list the serious
   findings and fix them. Then ask: would the owner stop and look? If a page is merely correct, push it.

Write only inside `directions\B\`. Report as COMMON.md §6 says (your final message, and `directions\B\REPORT.md`).
