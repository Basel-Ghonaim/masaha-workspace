## Summary

Adds the public space page's responsive photo gallery and accessible viewer, plus live occupancy status with visible-page polling.

## Scope / Acceptance criteria / Out of scope

- Shows up to five gallery photos with bilingual accessible names and a wrapping viewer.
- Reads `/spaces/:slug/occupancy`, renders verified/unset/unverified/error states, polls every 60 seconds while visible, and refreshes on focus.
- Carries the agreed fixes from #107.
- Out of scope: booking, payments, QR check-in, reviews, claiming, and dashboard work.

## Change type

Feature and carried review fixes for the public directory, with documentation and focused tests.

## Carried from #107

Items 1–10 were handled before the feature commits:

1. Footer clearance: `01289292`
2. Place-map touch scrolling: `074dafa2`
3. Frontend architecture wording/date: `c704d960`
4. Directory authority punctuation: `c704d960`
5. Unverified contact `none` wiring: `72ae561d`
6. Phone map live announcement: `04e25352`
7. Loading/failed page heading: `db19543d`
8. Escape comment: `04e25352`
9. Finding 131 evidence: `c704d960`
10. Unknown-shift price case checked; API validation prevents it, so no change.

## Evidence

- `npm run lint`: passed.
- `npm run typecheck`: passed.
- `npm run test:unit -w @masaha/web`: passed.
- Focused component tests: 3 files, 16 tests passed.
- Production build, `check:build`, `check:classes`, `format:check`, and `check:links`: passed.
- The broader scoped component command had 378 passing tests and 5 timing/state failures across 3 files; changed files were rerun directly and passed.
- Full component, API, shared-unit, and API test lanes are CI-only.
- Read-only inventory found all required data cases in `masaha_dev`.
- Real run covered the English dark 1440 gallery viewer and Arabic light 390/768, one-photo, no-photo, and unverified cases; a second visible `/occupancy` request was observed after approximately 60 seconds.

## Screenshots

- `PUBLIC/shots/pr3b/3b-photos-en-dark-1440.png`
- `PUBLIC/shots/pr3b/3b-photos-ar-light-390.png`
- `PUBLIC/shots/pr3b/3b-photos-ar-light-768.png`
- `PUBLIC/shots/pr3b/3b-one-photo-ar-light-390.png`
- `PUBLIC/shots/pr3b/3b-no-photo-ar-light-390.png`
- `PUBLIC/shots/pr3b/3b-unverified-ar-light-390.png`

## Definition of Done checklist

- [x] Carried fixes committed before feature commits.
- [x] Gallery and live status implemented with bilingual copy.
- [x] Focused tests and repository checks pass.
- [x] No data changed in `masaha_dev`.
- [x] Required data inventory and representative browser matrix completed.
- [ ] CI is pending.
