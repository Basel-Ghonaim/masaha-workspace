## Summary

The audit reader, on the API. The space's owner reads the space's audit log: every entry of the space, the admin shown as **Masaha**. The admin reads the platform's events only, by a default-deny list. Both logs are paged, cover the last 30 days or all time, are searched by the target's name and filtered by actor and action.

**Carried from #123** (its review; the first three commits):
- **Item 1, finding 151** (the owner's option A): a closure's extension now also moves each covered subscription's renewal chain that has not started. That is a renewal starting after today and not ended early, and that renewal's own renewal too. Start and end move by the same days. The chain is locked with the covered rows in one statement, by id. Each renewal is linked and counted by the preview, and the audit names them apart (`renewalIds`). Finding 151 is written and resolved here.
- **Item 2:** a key that extended another space's closure is a `conflict` (409, no code), checked before anything is answered.
- **Item 3:** `data-model.md` line 23: the extension's key is unique on its own.
- **Item 4:** `subscriptions.md`'s API history now has `#123` below `#118`.

## Scope / Acceptance criteria / Out of scope

**Scope**
1. Carried from #123: items 1–4 above.
2. `@masaha/shared/audit`: the actions and entity types, the two queries, `AuditEntry`, `PlatformAuditEntry`, `AuditMeta`.
3. The `audit` module (L5, a read model; it writes nothing):
   - `GET /manage/spaces/:spaceId/audit-log` (🏢, `requireCan('space.auditLog.read')`);
   - `GET /admin/audit-log` (🛡).
4. The admin's allowlist (`audit/platformEvents.ts`, pure; the SQL is built from the same lists).
5. Documents: `features/audit.md` (new), the contract's *Audit log*, conventions §6–§7, security, the data model, v1-mvp, the overview, the docs map. Finding 151 (resolved) and finding 152 (open, §13 Q10).

**Acceptance criteria**
- [x] An extension moves every covered subscription's end, and each of their renewals not started, start and end, by the same days, with one link each and audited `renewalIds`. The review's scenario: S ends 12-03, R runs 12-04 → 2027-01-02 (T-C1).
- [x] A renewal already started, or ended early, is not moved. The preview counts what the extension moves (T-C2, T-C3), and a renewal sold while the extension waits moves too (T-C4).
- [x] A key that extended another space's closure is a `conflict`, answering nothing of it (T5).
- [x] The owner reads every entry of the space, newest first, paged; another space's never. The admin is `MASAHA` with no id or name; a staff member is named, also after their link ended; the system is `SYSTEM` (T1, T2).
- [x] Each entry carries its action, time, actor, target (type, id, current name, deleted) and `before`/`after` as stored (T3).
- [x] Filters, each applied before the page is cut, with the total right (T4–T7):
  - `period` `LAST_30_DAYS` (the default, from the Gaza midnight 29 days back) or `ALL`;
  - `q` (Arabic folded);
  - `actor`; `actor=<an admin's id>` finds nothing;
  - `actions`;
  - `meta.actors` lists the period's actors.
- [x] Reception gets 403 before the query is read. A stranger, another space's owner and the admin get `not_found` (T8). A bad query gets 422 on its field (T9).
- [x] The admin reads the platform's events of every space and of none. Never a space's customers, subscriptions, check-ins, visits, payments, packages, announcements, extensions, capacity, override, settings or staff (T10). An account's event that names a space is the space's (T11).
- [x] The admin's `q` also finds a space's entries by its name, and each entry carries its space (T12). `actor` narrows (T13). The `/admin` guard refuses others (T14).

**Out of scope:** the screens (worker A's later items: screens 31 and the owner's audit screen, finding 14); the platform settings (PR 2); finance (PR 3); a retention job (decision 10, finding 152); a free date range (§13 Q8).

## Change type

feat (with fixes and docs carried from #123): API code, the shared contract, tests and documents. No migration, no web change, no dependency.

## New error codes

None.

## Decisions taken without the owner (the autonomy rule; each in the report with its undo)

- **The target's names are read by joins, not a lateral subquery** (a departure from D5's sketch). On a generated year (§12.2 check 4), PostgreSQL wrapped the lateral `UNION ALL` in a `Memoize` node that missed on every row. A search over all time took 2.5–8.4 s for the owner and 4.3–4.7 s for the admin. One `LEFT JOIN` per target type gives the same answers (T3, T5, T12) and is 10–30× faster on `q`.
- **Four reads stay over 150 ms; they are recorded, not indexed** (your Q5 rule). They are all `q` over **all time**: the owner's page and count at 280 / 220 ms, the admin's page and count at 1,082 / 179 ms, on a busy machine (133 / 114 / 582 / 114 ms when quieter). Everything without `q`, and `q` over the default 30 days (72 ms), is under. An index on `(action, created_at)` or a trigram index is yours to decide.
- **T-C2's "started" renewal** uses an ended closure on the test file's own clock, instead of the plan's second clock.
- **`actions` repeated count once** (as the directory's area list). **An actor id out of bounds is `out_of_range`.**
- **The carried real-run case was not performed**: the demo space has no closure left to extend and no renewal starting after today. T-C1–T-C4 prove it.
- **`OPEN_DECISIONS.md` is not appended**: the exec prompt allows only the report. The line for point 2 is in the report.

## Evidence

- `lint`, `typecheck`: each commit and the head, exit 0.
- `test:unit`: 263, 879 and 989 tests passed.
- `test:api`: 97 files, 1245 tests passed (643 s).
- `format:check`, `check:links` (2907 links), `check:conflicts`, `build -w @masaha/shared`: all green on the head.
- Seen failing first:
  - T-C1–T-C4: 5 failed of 15, e.g. `expected '2026-12-01 → 2026-12-30' to be '2026-12-03 → 2027-01-01'`.
  - T5's new line: `expected 201 to be 409`.
  - U1–U3: each against a stub.
  - T1–T9 and T10–T13: 404s before the routes existed.
  - T14 passed before its route existed (the `/admin` guard answers first); B18 is its break.
- Deliberate breaks, 25 in all, each red, restored from a backup (SHA-256 the same) and green again:
  - the carried items, B-C1–B-C6;
  - the allowlist, B1–B2, B13–B15;
  - the period, B3 and B8;
  - the query, B4;
  - privacy, B5–B6 and B10;
  - targets and search, B7, B9 and B16;
  - actors, B11 and B17;
  - access, B12, B12a and B18.
- Measured on a generated year (337,000 entries): the table is in the report.
- Real run on 3321: the owner's log 200 (13 entries, equal to SQL); reception 403; the directory owner 404; the admin's log 200 (17 rows, each on the list, equal to SQL by the same list); after the admin hid and showed the demo space (1) and Tuffah Place (10) — the run's only writes, entries 52–55 — the admin's log shows the four with their names, the owner's the demo space's two as `MASAHA`, and `q=Demo Space` finds them. One check of the script was its own defect (it matched the target's id, not the actor's) and was re-judged read-only: ALL PASS. The carried case was not performed (no closure left to extend in the demo data).
- Not run: `test:component`, the web's `build`, `check:build`, `check:classes`. No web file changes; CI runs them.

## Screenshots

None: API and documents only.

## Definition of Done checklist

- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes and data only).
- [x] Authorization on the server (`requireCan`, the boundary, `/admin`'s guard; the admin's allowlist).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
