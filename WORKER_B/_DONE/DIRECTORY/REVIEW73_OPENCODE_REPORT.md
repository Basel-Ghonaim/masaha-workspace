# Review — PR #73: the public directory's API

Head `28275b226047780f666008c9cf7f9a1a199099b3` (expected `28275b2`; rechecked at the end). Base `e30a86c9ef8b03998516263090570fb341345e62`.

Verdict: no blocker; one should-fix (the tie-break tests cannot fail) and two nits.

## Findings

### 1. should-fix — the tie-break tests pass even with the tie-break removed

- `apps/api/src/modules/directory/near.api.test.ts:48`, `apps/api/src/modules/directory/list.api.test.ts:104` against `apps/api/src/modules/spaces/public/publicListing.repository.ts:134-146`.
- Scenario: delete `, id` from any `ORDER BY` in `orderOf` (or from the default `last_updated DESC, id`). Both tests still pass: every row is freshly inserted, so heap order equals id order and the pages come out identical with or without the tie-break. The code is correct (every order ends with `id`), but the guarantee "ties keep their places across pages" is unproven — a future edit dropping a tie-break would go uncaught and pages could repeat or skip rows under ties. The worker's report admits this for the default order; the distance test (`limit=1&page=2` over two equidistant rows) is claimed as proof but suffers the identical masking.
- Fix: shuffle physical order away from id order before asserting — e.g. `UPDATE` a non-ordered column of the earliest row (a new heap version sorts last without the tie-break) — then assert the id-ordered page. Without `, id` the moved row sorts last and the test fails; with it, it passes.

### 2. nit — the contract promises `invalid_format` for a spaces-only `q`; the code answers `too_short`

- `docs/api/api-contract.md:201` against `packages/shared/src/directory/requests.ts:56` (`searchText`) and `:42` (`NOT_SEARCHABLE`).
- Scenario: `GET /spaces?q=%20%20`. `textSchema` trims to `""`, so `min(1)` fails first and the errors carry `too_short` (the unit test asserts `toContain('too_short')`), while the contract says a `q` of "tashkeel, tatweel or spaces" is `invalid_format`. If Zod also runs the `:42` refinement, `invalid_format` is appended and the contract holds; otherwise it overstates. Safe either way — the request is refused, never match-everything — but the exact code for the all-spaces case is undocumented.
- Fix: one clause in the contract naming the all-spaces code (or normalise before the length check so all three cases answer `invalid_format`).

### 3. nit — security.md says the distance answer labels the distance; it carries a bare number

- `docs/backend/security.md:116` against `packages/shared/src/directory/responses.ts` (`distanceMeters?: number`).
- Scenario: read the sentence against the payload — a JSON number cannot carry a label. The labelling is the screen's (foundation §13 already places "labelled approximate" on the screen).
- Fix: "…to the nearest 100 m; the screen labels it approximate."

## Checked and fine

- Privacy end to end: the point travels only in `Masaha-Near` (`listQuery.ts` reads header + query together, keeps the parsed point in `res.locals`, never on `req`); `?near=` is stripped by the schema and refused (`required`, test-proven); a duplicated header fails the regex (refused, never used); case-insensitive read is the same channel. Redaction path `req.headers["masaha-near"]` matches pino-http's header logging, including the 4xx `warn` line and the refused-point line. Validation errors carry codes only (`toFieldErrors` never echoes values). No point in any body beyond `distanceMeters`; distance answers are `no-store`; error answers carry no cacheable body. Reads write nothing (counters stay address-keyed); the point reaches the database only as a bound parameter, so a 5xx `err` log holds placeholders, not values (plausible — Prisma parameterises `$queryRaw`). The whole-line proof test fails when the redaction path is removed (break made).
- Migration: `pg_trgm` + two functions, no table change. `IMMUTABLE` truthful on both (`lower`/`regexp_replace`/`translate`/`btrim`/`strpos`/`word_similarity`); `STRICT` correct on the normaliser and correctly absent on the scorer (its `target IS NULL` branch); one rule for stored names and query; empty-database safe. `ar-x-icu`/`en-x-icu` exist on Neon — Neon's compatibility docs give the `icu` provider with a full predefined icu locale series, name `ar-x-icu` explicitly, and document the per-expression `COLLATE "xx-x-icu"` pattern (neon.com/docs/reference/compatibility); this closes the worker's open question. The `\uXXXX` sequences in the file are ASCII escapes the Postgres regex engine interprets — proven by the passing tashkeel/tatweel/hamza tests plus the worker's direct `psql` probe.
- SQL: every input via `Prisma.sql` parameters (period as a cast parameter, arrays as parameters, `ORDER BY` from fixed fragments); total and page under each sort with the id tie-break in code; price filter reads `GENERAL` of the period with inclusive, open bounds (period-alone documented in the contract), stale-unverified excluded via `pricesShown` (NULL-safe: missing prices match nothing); publicly-listed exactly as the data model defines it in list, pins (`listedAreaIds` intersection, inactive narrows to nothing) and page (`findShownBySlug` + `isActiveArea` + share-lock recheck, verified race disclosed and accepted). No N+1 (one `weeksFor`, one `areaNamesFor`, one amenity query per read).
- Levels and boundaries: `directory` imports lower modules only through their `index.ts`; the `spaces/public`, `lookups` and `space-links` additions sit by their rules (verified stays resolved by `space-links`); nothing in `apps/web`; `packages/shared/src/directory/` with its `index.ts`.
- Cache: `public, max-age=30` with ETag/304 on list, pins and page; `no-store` on distance answers; nothing user-specific cached.
- Tests: hand-written expectations throughout; distance order with 0/1100/3300 m rounding, typo/hamza/area search with exact-vs-typo ranking, truncation boundaries (1,000 → false, 1,001 → first-by-id + true), all five 404 cases, and exact-shape tests proving no capacity/price/count keys — each break made failed its test.
- Documents: contract §4 pins exception, §5 *Directory (public)* and the prices line naming both refusals; `directory.md` follows the §5 template (1,262 whitespace tokens including the standard header — approximately at the ~1,200 guideline); `spaces.md`/`lookups.md`/`space-links.md` bullets, history lines and code maps; data-model search + widened stale prices; security *Location* + redaction; conventions §9 bullet; overview *Built* + dated *Near me* change; foundation §13 dated change; plan rows (built work in *Built*, `availableNow` and announcements kept as future rows); README map line. One home per fact preserved.
- Commits: three; subjects 47 / 45 / 47 characters (counted, all ≤ 50). #69 alone in commit 1 (contract file only, `Closes #69` in its body); the distance work whole in commit 3. PR title, labels, assignee and `Closes #69` as required.

Head rechecked at the end: `28275b226047780f666008c9cf7f9a1a199099b3`.
