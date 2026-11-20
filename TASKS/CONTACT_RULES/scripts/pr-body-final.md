## Summary
Five planned findings are resolved in one PR: every phone reads Arabic-Indic and Eastern digits (217); websites require a real domain and Facebook links must identify a page or profile (218); a ghost control inside a hovered table row takes the ink wash (226); component teardown waits for toast removal timers (219); and four site test files warm their lazy routes (225). Finding 228 is fixed here too (the owner's decision C11): customers' search reads Arabic-Indic and Eastern phone suffixes as phone digits and searches the end of stored phones, and the desk's present search does the same.

## Scope
- C1 + C2: `toWesternDigits` moves from the web's `shared/lib` to `@masaha/shared/core`; `normalisePhone` and the `OTHER` number test use it. The forms +970, +972, 00970, 00972 and local 0 remain supported.
- C3 + C4: link hosts require a domain with a top-level domain; Facebook accepts a username, `profile.php?id=<digits>` or `/people/<name>/<id>`. The Sheet refuses invalid values before sending; the server refuses them too.
- C5: `Button`'s ghost variant inside `[data-slot=table-row]` uses `hover-on-muted` on hover and while its menu is open.
- C6: the component setup waits out a drawn toast's removal timer after the file's last test; four site test files warm their lazy modules.
- Finding 228 fixed: `customerSearch.ts` reads the term's digits through `toWesternDigits` before the digit test; `matchesPerson.ts` (the desk's present search) does the same; both are covered by unit tests.

## Acceptance criteria
- [x] Arabic-Indic and Eastern whole phones normalize to `+970599123456`; the contacts Sheet, desk edit dialog and contacts API accept their specified Arabic-Indic inputs.
- [x] Bare numbers, IPs, `localhost` and bare words are refused as websites; Facebook non-page/profile paths are refused while page and profile links are stored.
- [x] The Sheet reports invalid website/Facebook values on their rows without sending a request; the API returns `422 invalid_format` and writes nothing.
- [x] The ghost button has both row-scoped classes; token tests check `hover-on-muted` and foreground over hover in both themes; eight 1440px captures were visually checked.
- [x] The toast teardown test fails without the wait and passes with it; `waitOutToastRemoval` lives in `apps/web/src/test/toastRemoval.ts`; four lazy-route warm-ups are present.
- [x] A phone's last digits typed in Arabic-Indic or Eastern digits search the end of a stored phone (finding 228), in the customers' search and the desk's present search.
- [x] Read-only data counts are reported; no data was changed.
- [x] All local checks are green on head `23f79af37a7fd3932c3c3d2b75f8b8a04bfb742c`.

## Out of scope
No schema, migration, dependency, copy or data change. Stored contacts were not rewritten.

## Change type
fix (web, api, shared, design system, docs)

## Evidence
- Lint, typecheck, format:check, check:classes (1,990 files), check:links (2,784 links in 226 documents and 2,690 source files) and check:conflicts: passed.
- Production build and `check:build`: passed; emitted CSS contains the table-row-scoped rule.
- `test:unit`: shared 29 files / 384 tests, API 77 / 924, web 196 / 1,403 — all passed. `test:component`: 349 files / 2,152 tests passed. `test:api`: 126 files / 1,451 tests passed.
- First-failure evidence: each new test row passes only after its code; removing `search` from Facebook's paths fails the `/search/?q=x` row, removing `events` fails `/events`; removing `toWesternDigits` from `customerSearch.ts` fails the Arabic-Indic suffix rows, and from `matchesPerson.ts` fails `٠١`. All restored.
- Read-only `masaha_cr_dev` count: FACEBOOK 0 refused of 1 data contact; WEBSITE 0 refused of 1 data contact; self-tests: FACEBOOK 4/7 refused, OTHER 1/3, WEBSITE 4/6; mismatches 0 for every self-test row.
- Live API `/health` on port 3337 returned `status: ok`, `db: up`; server stopped by PID and port 3337 free. The headless showcase run printed no browser errors.
- Not run: release E2E smoke (outside this task); CI is running after this push.

## Screenshots
Eight captures at 1440px are saved in `C:\Users\basel\Downloads\contact-rules-shots\`: Arabic row hover, ghost hover and open menu in light and dark; English ghost hover in light and dark. The printed values show the ghost wash differs from the row in both themes; both menu captures have `aria-expanded=true`; Arabic is RTL and English LTR. The PNGs were opened and visually checked. Below 768px the rows are cards, not table rows.

## Definition of Done checklist
- [x] Acceptance criteria met; 38 files total (the plan's 37 plus the owner-directed finding 228).
- [x] Lint, typecheck and production build pass.
- [x] Owning test lanes pass; planned first failures and mutations are documented.
- [x] No user-facing copy changed.
- [x] RTL and LTR, light and dark, desktop captures checked.
- [x] Authorization is unchanged; shared validation is enforced by the server.
- [x] Documents updated; findings 217, 218, 219, 225, 226 and 228 resolved; index moved.
- [x] Claims name their test or command.
- [x] CI green on the pushed head and GitHub shows `CLEAN`.
- [x] Five-commit history pushed.

More than 25 files: a separate review conversation is required by workflow §2, phase 7.
