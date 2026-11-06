# Palette lab plan

## Summary
Build a standalone, Arabic-first palette comparison lab for the design prototype.

## Contract
- Scope: add `Palette lab.html` and `masaha/palette-lab.js` only.
- Acceptance: seven palettes, live OKLCH ramps, iframe screen previews, light/dark/both modes,
  screen/device selection, contrast report, hue warning, copy output, and URL state.
- Out of scope: existing prototype edits, production code, dependencies, tests/build/lint, push, PR.

## Reading
Read `CLAUDE.md`, workflow, documentation map, findings index, design README, SCREENS.md,
design-system foundation, and the complete execution prompt.

## Settled decisions
Use the prompt's exact Sea baseline; generate other brand/neutral ramps in local OKLCH with
gamut clamping; apply only brand/neutral inline variables to same-origin iframe roots; keep
status ramps unchanged; use semantic-token chrome and existing bundle utilities.

## Stronger decisions
None: the prompt fixes palette inputs, screen list, URL contract, and verification behavior.

## Related findings
No open finding concerns this standalone design prototype; none folded.

## Files and parallel ownership
Create only the two named prototype files. No other-layer or shared-file edits.

## Design issues
None identified for the lab itself; use existing semantic tokens, controls, and responsive layout.

## Tests and review focus
The prompt assigns no test lane. Run the two prototype parse/class checks; manually exercise
every palette, theme, screen, device, copy action, URL state, and iframe navigation. Review URL
encoding, free-colour persistence, gamut edge cases, contrast pair coverage, and iframe load races.

## Commits
One Conventional Commit: `feat(design): add palette lab`.

## Verification
Run both prototype checks, serve on port 5401, browser-check all required matrix paths, and save
the requested screenshots outside the repository. Do not run npm ci, build, lint, or test lanes.

## Owner decisions
None required; all behavior is settled by the execution prompt.
