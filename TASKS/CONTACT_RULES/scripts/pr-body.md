## Summary
Five planned findings are resolved in one PR: every phone reads Arabic-Indic and Eastern digits (217); websites require a real domain and Facebook links must identify a page or profile (218); a ghost control inside a hovered table row takes the ink wash (226); component teardown waits for toast removal timers (219); and four site test files warm their lazy routes (225). Finding 228 is also recorded in its own file as Open: customers' search treats Arabic-Indic phone suffixes as a name. The search behavior is not changed here.

## Scope
- C1 + C2: `toWesternDigits` moves from the web's `shared/lib` to `@masaha/shared/core`; `normalisePhone` and the `OTHER` number test use it. The forms +970, +972, 00970, 00972 and local 0 remain supported.
- C3 + C4: link hosts require a domain with a top-level domain; Facebook accepts a username, `profile.php?id=<digits>` or `/people/<name>/<id>`. The Sheet refuses invalid values before sending; the server refuses them too.
- C5: `Button`'s ghost variant inside `[data-slot=table-row]` uses `hover-on-muted` on hover and while its menu is open.
- C6: the component setup waits out a drawn toast's removal timer after the file's last test; four site test files warm their lazy modules.
- Finding 228: recorded Open in `docs/architecture/findings/228-customers-search-reads-a-phones-arabic-indic-last-digits-as-a-name.md` and indexed; no search fix is included.

## Acceptance criteria
- [x] Arabic-Indic and Eastern whole phones normalize to `+970599123456`; the contacts Sheet, desk edit dialog and contacts API accept their specified Arabic-Indic inputs.
- [x] Bare numbers, IPs, `localhost` and bare words are refused as websites; Facebook non-page/profile paths are refused while page and profile links are stored.
- [x] The Sheet reports invalid website/Facebook values on their rows without sending a request; the API returns `422 invalid_format` and writes nothing.
- [x] The ghost button has both row-scoped classes; token tests check `hover-on-muted` and foreground over hover in both themes; eight 1440px captures were visually checked.
- [x] The toast teardown test and four lazy-route warm-ups are present. The teardown race did not reproduce in three isolated pre-fix runs; the test remains and the setup waits out the timer.
- [x] Read-only data counts are reported; no data was changed.
- [x] All local checks are green, including the owner's full API rerun; GitHub CI is green and `CLEAN` on head `a28f74dfce93bfc5900db2ccbdbfdde96ac4f976`.

## Out of scope
No schema, migration, dependency, copy or data change. Stored contacts were not rewritten. Finding 228's search behavior is recorded only.

## Change type
fix (web, api, shared, design system, docs)

## Evidence
- Lint, typecheck, format:check, check:classes, check:links and check:conflicts: passed. The number-only Markdown rewrite was followed by passing format:check and check:links again.
- Production build and `check:build`: passed; emitted CSS contains the table-row-scoped rule.
- `test:unit`: 302 files / 2,698 tests passed. `test:component`: 349 files / 2,152 tests passed. `test:api`: 126 files / 1,451 tests passed on code head `792ece8c5a77f070f14f40dc04686b44a4b1fb77`, with no code changes since.
- API environment incident: my initial full API run had 7 PostgreSQL-related failures while Postgres was under memory pressure; the retry repeated the directory open-hours failures and I stopped under the plan's twice-failed rule. After Docker restarted, the owner reran the two affected files on this branch and on main (37 tests passed each), then reran the full API lane on this branch through `heavy.mjs` (126 files / 1,451 tests passed, exit 0). Logs are `diag-branch.log`, `diag-main.log` and `diag-full-api.log` in the task folder.
- First-failure evidence: commit 1's phone and OTHER normalization cases failed before the code; commit 2's invalid domain/Facebook cases failed in shared, browser and API tests before the code; commit 3's new ghost-class assertion failed before the Button change. Commit 4's toast race did not reproduce locally; a temporary missing warm-up import was rejected by Vite and TypeScript, then restored. The detailed test and mutation log is in `4_REPORT.md`.
- Read-only `masaha_cr_dev` count: FACEBOOK 0 refused of 1 data contact; WEBSITE 0 refused of 1 data contact; self-tests: FACEBOOK 4/7 refused, OTHER 1/3, WEBSITE 4/6; mismatches 0 for every self-test row.
- Live API `/health` on port 3337 returned `status: ok`, `db: up`; server PID 20984 was stopped and port 3337 is free. The headless showcase run printed no browser errors.
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
- [x] Documents updated; findings 217, 218, 219, 225 and 226 resolved; finding 228 recorded Open with its index line.
- [x] Claims name their test or command.
- [x] CI green on the pushed head and GitHub shows `CLEAN` at `a28f74dfce93bfc5900db2ccbdbfdde96ac4f976`.
- [x] Five-commit history pushed.

More than 25 files: a separate review conversation is required by workflow §2, phase 7.
