# PR #49 — last round: rebase, two doc lines, two screenshots

Verified on `095bbbb`: all five fixes hold in the code; thank you. PR #48 has merged (`main` =
`e1f51f8`), so #49 is now `DIRTY`. This round is small: no code changes, no test lanes, no
subagents. ONE push at the end (`--force-with-lease`).

## 1. Rebase
Rebase on `origin/main`. The only conflict is `docs/project/overview.md` (adjacent lines): keep both.
Then run `npx prisma generate` in `apps/api` (#48 changed the schema; your `masaha_b_dev` already has
its migration).

## 2. Two doc lines, folded into the commits that last touched them
- `docs/features/lookups.md`, the decision "**A row's failure stays in its card** … no toasts, the
  amenities' included" now reads against the next one ("An amenity's failure shows in its row").
  Narrow it: "**A governorate's or an area's failure stays in its card** until the next action there;
  a 409 on an order fetches the list again; no toasts, the amenities' included."
- `docs/frontend/architecture.md`, the header's "a placeholder for each page (§2)" is no longer true:
  "a placeholder for each page not built yet (§2)". In the tab commit, beside your §2 correction.

## 3. Retake the row-failure screenshots
`Downloads\s2a3-shots\06-row-failure-*.png` were taken before the fix and still show the old alert
above the list. Retake both (`ar-light-1440`, `en-dark-390`) with **two rows failed at once**, so the
shots show each failure under its row. If the phone shot shows a layout problem, stop and report it
before changing anything.

## Checks
- Lint and typecheck once on the head, after the rebase (your commits change only two doc lines and
  the base under them). No test lanes, no build: CI runs everything.
- Add a short "Second round" note to the same "Review fixes" comment (rebase, the two lines, the
  shots). Report once CI is green and GitHub shows `CLEAN`: the head and the shots' paths. Don't merge.
