# IDENTITY — the owner's decisions (2026-11-05)

The visual identity: a new colour identity, decided together with the logo. Runs in parallel with refactor round 1
(DIRECTORY_FILTERS), on separate files.

## The owner's lean (2026-11-05)

The lab built (`design/palette-lab` in app-b, 37e7bca7, not yet reported). **The owner's favourite: Sea sunset**
(brand 600 `#AB432D`, blue-grey neutrals). All 38 contrast pairs pass in both themes; the lab warns it may be
confused with red (destructive). Next: a status-clash check in the lab (primary beside destructive), a tuned variant,
the "copy values" bug (it prints a literal `\n`), then the logo in the chosen colours.

## Ink + spark (2026-11-11)

- **I1 — the direction:** the brand takes two roles, a dark **ink** for actions and structure and a warm **spark** for
  "what matters now" (the idea taken from Oyoun Academy's design system — an idea, not its values). Every coral /
  orange / earthy colour failed as the primary (it differs from the destructive red by hue only; under colour
  blindness they look the same).
- **I2 — the finalists (the owner, 2026-11-11):** **`slate-coral`** (slate-blue ink + coral spark) and
  **`slate-berry`** (slate ink + berry spark), beside **today's Sea** for comparison. `charcoal-coral` is removed from
  the trial. The owner likes both equally: **the logo decides** — the mark is drawn in both, and colour and logo are
  chosen together. If coral wins, its dark tint is desaturated (the error-tint resemblance, report §130) and the
  sidebar count badge is ink.
- **I3 — next:** the logo plan (`TASKS\LOGO\`).
- **I4 — BERRY ADOPTED officially (the owner, 2026-11-11):** `slate-berry` is the identity (ink + berry spark) and the
  logo's colours (`final-trace/*-berry.svg`). The coral design is **kept for now** (not deleted): once berry is in
  production, people's opinion is gathered and compared. The owner's idea of a coral dark mode as a third mode was
  answered no by the supervisor (dark is exactly where coral resembles the error colour; one brand, two themes).

## The production plan (2026-11-12)

`2_PLAN_PROD.md` (from `1_PLAN_PROMPT_PROD.md`, planner in app-design, Opus xhigh) — **approved by the owner with
its recommendations:** OD2 (a) one PR; OD3 (a) no platform logo in the owner / reception shell; OD4 (a) the raster
icons rendered by the executor in headless Chrome, the `.ico` packed by a scratchpad script (no dependency); OD5 (a)
berry becomes the prototype's default, Sea and coral behind `?identity=`; SD1–SD10 and D1–D5 as written.
**OD1 (how it executes) — reopened by the owner:** "if the task is big, why not a lead with sub-agents?" (the plan
recommended one executor). **Settled: OD1 (b) — a lead with sub-agents** (the supervisor's revised recommendation:
it protects the lead's context, which ran out on #143's first executor; the owner frees the disk for it). Each lane in
a worktree of its own when the disk allows (≈ 1 GB a lane), else the same folder on disjoint files with the lead
committing; at most 3 sub-agents at once; the heavy runs and the visual pass scheduled by the lead.
**The owner's no-conflict rule (2026-11-12):** the lead may start before #143 merges, but edits **no file #143
changes** until it has merged (today `foundation.md` and the layer's `index.ts`); the sub-agents start only after the
merge, once the lead has rebased and finished the shared layer on the merged `main`. Execution starts only after #143 merges (the owner, 2026-11-12). Its finding becomes
**220** (#143's fix round takes 219).

## Step 1 — the palette lab (approved 2026-11-05)

1. **A palette lab page in the prototype** to choose the colours by eye on real screens: one click swaps the whole
   identity, in light and dark at once.
2. **Why it works:** every colour of the site comes from two 11-step ramps, `brand` and `neutral` (foundation §4); the
   semantic roles map to their steps by a fixed table in both themes (§5). The prototype's bundle wires the semantic
   tokens through `var(--brand-*)` / `var(--neutral-*)`, so overriding the two ramps restyles a page in both themes.
   The mapping table is kept; only the ramps change.
3. **Both ramps change together:** the "AI-made" feel comes from the teal *and* its cool teal-cast greys.
4. **What the lab shows:** palette buttons (the current Sea for comparison, clay & stone (recommended), olive & ink,
   sea sunset, and a few more), light/dark side by side, real prototype screens (Home, the directory, a space's page,
   the desk, the owner's overview), a free colour mode (pick any colour, the ramps are built from it), and a contrast
   check of foundation §5's verified pairs in both themes (✓/✗), plus a warning when the brand's hue sits close to a
   status colour (success green, warning amber, destructive red, info blue).
5. **Worker:** an OpenCode worker in `C:\dev\masaha\app-b`, branch `design/palette-lab`, commits, **no PR, no push**.
   New files only (no edit to any existing file), so it never meets the DIRECTORY_FILTERS worker. Checks: the
   prototype's two scripts only.
6. **After the lab:** the owner narrows to two or three directions; the main supervisor draws the logo (SVG) in their
   colours (`TASKS\LOGO`), the lab gains a logo preview; the owner decides colour and logo together. Then the chosen
   ramps go into `foundation.md`, the prototype's tokens and the web's tokens (`apps/web/src/shared/design-system/`),
   and the logo to Google Branding. Whether the lab itself lands in the repository is decided then.
