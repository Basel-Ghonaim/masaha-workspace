# IDENTITY — the owner's decisions (2026-11-05)

The visual identity: a new colour identity, decided together with the logo. Runs in parallel with refactor round 1
(DIRECTORY_FILTERS), on separate files.

## The owner's lean (2026-11-05)

The lab built (`design/palette-lab` in app-b, 37e7bca7, not yet reported). **The owner's favourite: Sea sunset**
(brand 600 `#AB432D`, blue-grey neutrals). All 38 contrast pairs pass in both themes; the lab warns it may be
confused with red (destructive). Next: a status-clash check in the lab (primary beside destructive), a tuned variant,
the "copy values" bug (it prints a literal `\n`), then the logo in the chosen colours.

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
