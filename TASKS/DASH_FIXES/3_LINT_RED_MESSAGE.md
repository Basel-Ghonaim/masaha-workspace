# DASH_FIXES — CI red again on #146 (lint) — the message to paste to OpenCode

```
Supervisor's message (relayed by the owner). #146 is red again on 800fb5b3 — typecheck now passes, lint fails (all in 227's commit, "guard unknown amenity icons"):
- boundaries/dependencies: directory's AmenitiesSection.tsx and useSpacePage.ts, and spaces' useAmenitiesSection.ts import lookups' `services/amenityIcon.ts` — a feature never imports a sibling feature. Move the one helper to where every caller already reaches: `packages/shared/src/lookups/amenityIcons.ts`, beside `AMENITY_ICON_KEYS` (e.g. `amenityIconOf(key: string): AmenityIconKey | null`), exported through `@masaha/shared/lookups`; delete `apps/web/src/features/lookups/services/amenityIcon.ts`; every caller imports it from `@masaha/shared/lookups`. Then `npm run build -w @masaha/shared` before the web's checks.
- AmenitiesSection.tsx:23 forbidden non-null assertion; useAmenityChecklist.ts:85 and AmenitiesView.tsx:20 unnecessary type assertions; AmenityChecklist.tsx:1 unused CircleCheckIcon — fix each without an eslint-disable.
Fold everything into that commit (backup/dash-fixes-pre-lint first; --fixup + autosquash).
Before the push, these are REQUIRED this time (two red rounds), each through the grant script, which waits for memory: `npm run lint`, `npm run typecheck`, then the touched test files alone (add a unit test for the moved helper in packages/shared if none covers it).
Push with --force-with-lease (your branch only), wait for every check green and CLEAN, write 4_REPORT.md (say both red rounds and what they were), stop. Never merge.
```
