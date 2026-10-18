Verdict: Changes requested — reviewed PR head `28275b226047780f666008c9cf7f9a1a199099b3`.

## Findings

1. **should-fix** — `apps/api/src/modules/directory/directory.controller.ts:13-17` — If a request supplies a valid `Masaha-Near` point but another list field is invalid, validation fails before the controller runs; likewise, a directory error before `directory.list()` resolves skips `cachePrivately`. The error handler then returns an answer without `Cache-Control: no-store`, contrary to the requirement that every answer to a location-bearing request is not cached. Set `no-store` as soon as the location header is present, before validation, so validation and downstream errors retain it.
2. **plausible should-fix** — `apps/api/src/modules/directory/directory.service.ts:143-144` — `linksAt()` reads verification before `publicSpace.read()` opens its transaction and locks the space. If the active OWNER link is deactivated between those operations, `verified` remains `true` while `read()` evaluates current facts; an unverified space with stale prices can therefore return those prices. Read verification and facts under the same transaction/lock (or otherwise make the status and facts consistent); the gap between the two calls makes this race plausible.

## Checked and fine

- The point is accepted from the header only; the request logger redacts its normalized header, the proof test inspects the full serialized log line, and validation responses map issues to field codes rather than echoing values.
- Raw listing/search SQL binds dynamic values; filter-before-page, ID tie-breaks, stale-price filtering, batched week reads, and the map’s 1,001-row truncation check are present.
- The migration uses `CREATE EXTENSION IF NOT EXISTS pg_trgm` and creates the normalizer and score functions without schema tables; Neon’s build enables ICU and its extension reference lists `pg_trgm` for supported PostgreSQL versions ([Neon build](https://github.com/neondatabase/neon/blob/fa504217c61bbcaf5c512d75830564541f917f8f/Makefile#L60), [Neon extensions](https://neon.com/docs/extensions/pg-extensions.md)); PostgreSQL documents the ICU `-x-icu` locale naming ([PostgreSQL collation docs](https://www.postgresql.org/docs/current/collation.html#COLLATION-MANAGING-PREDEFINED-ICU)).
- Endpoint tests cover filtering/search, distance order, page 404s, cache revalidation, pins and truncation. The diff adds no `apps/web` changes or dependency-manifest changes; the three commit subjects are 45–47 characters.
