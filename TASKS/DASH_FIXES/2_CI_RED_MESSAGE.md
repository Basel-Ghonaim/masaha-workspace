# DASH_FIXES — CI red on #146 (the message to paste to OpenCode)

```
Supervisor's message (relayed by the owner). #146's CI is red on 63415cbf: typecheck fails with two errors —
  apps/web/src/features/directory/hooks/page/useSpacePage.ts(240,21): TS2304 Cannot find name 'knownAmenityIcon' (no import).
  apps/web/src/features/spaces/components/editor/SpaceEditorActions.component.test.tsx(159,13): TS2304 Cannot find name 'refused' (no import).
Fix each in the commit that introduced it (the first in 9ed98383 "guard unknown amenity icons", the second in c282a58d "hide actions for gone space"): a backup/dash-fixes-pre-ci branch first, then --fixup + autosquash — no fix commits.
Run `npm run typecheck` through the grant script now (node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs dash npm run typecheck) — this one is required before the push; then the two touched test files alone.
Push with --force-with-lease (your branch only), wait for every check green and CLEAN, then write 4_REPORT.md and stop. Never merge.
```
