# DIRECTORY — reply to your plan

A strong plan: the `directory` module where conventions §7 reserved it, `pg_trgm` checked in the
database and on Neon before it was chosen, one normalising function for the stored names and the
query alike, the slug clash that moved the pins to `/map/spaces`, and the privacy proof that reads the
whole log line. **Approved**, with the answers below; two of them change the location's handling.
**First, save it** (as approved here, with these changes folded in) to
`C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\DIRECTORY_PLAN.md`, then cut the branch from `origin/main`
(check it is still the latest) and build.

## The owner's decisions (§13)

1. **S9 — `docs/features/directory.md`:** approved, with its map line; `spaces.md`, `lookups.md` and
   `space-links.md` keep what their modules add.
2. **S2 — a pin carries `areaId` and the week's `days`:** approved.
3. **D4 — no freshness on the card:** approved (the sort reads the dates on the server).
4. **The location travels in a request header, not in the query** (the owner, against your
   recommendation). The query reaches the hosting's own request log, which Masaha cannot redact, and
   every proxy's; a header does not. So:
   - `sort=distance` reads the point from a header (name it in the plan without the `X-` prefix, for
     example `Masaha-Near: lat,lng`); `sort=distance` without it is `required` on the header's field,
     the header without `sort=distance` is refused (`invalid_choice`), as you planned for `near`;
   - **the request log's default serializer logs the request's headers:** redact this header there
     (the pino redaction paths), and prove it with your whole-line test (the break made once);
   - the answer stays `no-store`; nothing caches it;
   - **finding 61 is not needed** (the hosting never sees the point); keep 61–62 free for the build;
   - `overview.md`, foundation §13 and security.md say "sent in a header, only to sort by distance,
     rounded on the device, never stored or logged".
5. **The precision: 3 decimals (about 110 m), not 2** (the owner, against your recommendation). Spaces
   in Gaza sit close together; at about a kilometre, "near me" loses its meaning inside a
   neighbourhood. With the header (decision 4) and nothing stored or logged, a 110 m square names a
   block of many buildings, not a home. The server refuses more than 3 decimals (S3 as you planned,
   with 3); `distanceMeters` stays rounded to 100 m. Update §4 D2's reasoning and the tests.

## Two additions

- **A `q` that normalises to nothing** (tashkeel or tatweel only, or spaces) is refused
  (`invalid_format` on `q`), never treated as "match everything"; add its unit test.
- **The PR's title:** `feat(directory): the public directory's API` (≤ 50), to name the module.

## Reminders

- **One full test run at a time on this machine:** before `test:api`, check worker A is not running a
  lane in the main folder; if it is, wait.
- The migration created once with `migrate dev --create-only`, then `ls`; applied to `masaha_b_dev`
  and the test lane's database.
- The report says the prototype's `PRIVACY_LINE` is untrue now: the account design fixer rewords it in
  `shared.jsx` this round (the analyst routed it).
- An independent review follows (privacy, a migration). Don't merge. At the report,
  `git merge-tree --write-tree` against every open PR. Stop every background shell you start; `jq` is
  not installed — use `gh … --jq`.
