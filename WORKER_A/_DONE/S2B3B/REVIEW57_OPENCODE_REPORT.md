# Review — PR #57 (S2b-3b: add a space, with its pin on the map)

**Verdict:** No blocker. One should-fix (a commit subject over the 50-character limit) and five nits; the form, the map, the build checks, the design-system split, the tests and the documents otherwise hold up.

Head pinned to `36507590ff1783bb988883707318121c62b4a5ad`; base `49cd088`.

## Findings (most severe first)

### 1. should-fix — a commit subject is 52 characters (limit 50)
`df998c938652f94e8d8627436e316049027b4bb5` — `fix(design-system): keep the data table off the site` = 52 chars. The rule is `<type>(<scope>): <description>` — imperative, lowercase, no period, **≤ 50 chars** (`docs/development/workflow.md` §3, Commits). The other four are 33–46 and pass.
**Fix:** reword to ≤ 50, e.g. `fix(design-system): keep the table off the site` (47).

### 2. nit — `package-lock.json` clears the dev flag on five packages unrelated to this change
Entries `node_modules/ajv` (line 5850), `node_modules/fast-json-stable-stringify` (7555), `node_modules/json-schema-traverse` (8422), `node_modules/punycode` (9784), `node_modules/uri-js` (11194) each go `"dev": true` → `"devOptional": true`.
Scenario: these are the eslint `ajv@6` tree, not Leaflet. `@hookform/resolvers@5.9.1` (a prod dependency of `apps/web`) declares `ajv` among **optional** `peerDependencies`; re-resolving the tree (adding Leaflet) makes npm mark the already-hoisted `ajv@6` and its transitive deps `devOptional`. Result: a production install (`npm ci --omit=dev`) now keeps that eslint-only tree, where before it was omitted. Nothing in the changed files explains it, and no code reads `ajv`.
Fix: regenerate the lock with the CI's npm version and drop the unrelated flips (or state that they are accepted). Confirmed: the only other lock changes are the four Leaflet packages (`leaflet`, `react-leaflet`, `@react-leaflet/core`, `@types/leaflet`); no other version is added, removed or changed.

### 3. nit — the new finding takes number 46, but the next number is 49
`docs/architecture/findings/46-the-deployments-headers-must-let-the-maps-tiles-load.md` (added) and `docs/architecture/findings/README.md:37`.
Scenario: the rule is "A new finding takes the next number" (`docs/architecture/findings/README.md:10`); the base's highest is 48 (`48-db-up-...`), so the next number is **49**, not 46. Using 46 leaves 47 permanently unused while a later author following the rule takes 49, so the sequence never closes.
Possible, not certain: if 46/47 were deliberately reserved, 46 is correct — but nothing in the repository reserves them (`git grep` finds no other reference to 46/47). Plausible this should be 49.
Fix: rename to `49-...` and update the index, or record 46/47 as reserved next to the rule.

### 4. nit — `Last Updated` headers not bumped on two documents this PR changes
`docs/frontend/architecture.md:3` and `docs/frontend/design-system/foundation.md:7` both still read `**Last Updated:** 2026-10-07`, although the PR edits their content (architecture §3, §6, the built-layout paragraph; foundation §3's entries and stylesheet rule). The sibling capability documents this PR edits were bumped to `**Last Updated:** 2026-10-10` (`docs/features/spaces.md:3`, `docs/features/lookups.md:3`).
Scenario: the header is the document's date (the template's "last updated", `docs/architecture/documentation.md:66`), so a reader sees the changed architecture/design-system pages as older than the change that edited them. Plausible the bump is expected; the exact bump rule is not spelled out (documentation.md puts "each header has its date" under *Not adopted* and workflow §7 lists triggers, not dates).
Fix: bump both headers to 2026-10-10, or confirm the convention is not to bump.

### 5. nit — finding 46 is linked from nowhere that describes the affected area
`docs/features/spaces.md:133` (its *Open findings*, lines 135–136, list only 43 and 44) and `docs/frontend/architecture.md:270` (§6, Map).
Scenario: finding 46 is the map's CSP risk, reached by the add-space page, and the analogous finding 33 is linked from the capability document that uses it (`docs/features/auth.md:80`). Finding 46 appears only in the findings index, so a reader of the spaces or map documents never reaches it.
Fix: link `[46](../architecture/findings/46-...)` from `spaces.md`'s *Open findings* or architecture §6.

### 6. nit — `libraryChunkOf` is exported but only its unit test uses it
`apps/web/scripts/libraryChunks.ts:24` (used by `libraryChunks.unit.test.ts:2,16,25`).
Scenario: production code reads `LIBRARY_CHUNKS` directly — `vite.config.ts:37` maps it and `checkBuild.ts:172` maps `.name`. `libraryChunkOf` has no production caller, so it is a test-only helper, against the project's stance that code exist for its callers and not for its tests (cf. `docs/architecture/findings/39-...`).
Fix: delete `libraryChunkOf` and have the unit test assert the `LIBRARY_CHUNKS` regexes directly (the regexes themselves are exercised in production).

## Checked and fine

- **Form.** Blank optional texts are omitted in `profileInput.ts:22-24` so the schema reads them as absent; required blanks stay and fail `too_short`; `location` becomes a point or stays text (`:26-28`) so `out_of_range`/`invalid_format` land on the `location` field; the 422 lands per field with focus on the first (`useServerForm`), the 409 reads `failureLines.conflict` (`useAddSpaceForm.ts:67`), the 429 counts down and blocks. `onCreated()`/toast run only after `refresh()` settles (`useCreateSpace.ts:19-23`, `useAddSpaceForm.ts:61-64`).
- **Map.** Leaflet, React Leaflet and `leaflet.css` are behind `PointPicker`'s `lazy` import (`PointPicker.tsx`); no pin until `value`; click/drag/typed coordinates are one value (`useAddSpaceForm.ts:100-111`); tile failures before any tile loads and a failed code fetch both fall back to `MapFailed` (`useTileStatus.ts`, `PointPicker.tsx:11-16`); container is `dir="ltr"` with `role="application"`; no listeners or timers left on unmount; attribution always visible.
- **Build checks.** `libraryProblems` fails on a first-download library chunk **and** on a missing chunk; the CSS check refuses `.leaflet-container` in the first download; when the manifest is absent the script still fails. The `data-table` / `leaflet` groups hold the whole library trees (`includeDependenciesRecursively: false` is safe: every dependency is matched).
- **Design-system entry.** Only the six `DataTable` exports moved from `index.ts` to `data.ts`; every importer of `DataTable` (the showcase and `AdminSpacesList.tsx`) now uses `@shared/design-system/data`; lint/`layerEntries`/`mapImports` tests run the real ESLint config.
- **Tests.** No `vi.mock` in the added tests; lane-correct by suffix; the CSS/build/coordinate/parse tests assert real behaviour.
- **Text and styling.** Every new string is in both catalogues; `leaflet.css` lives in the design system and is imported only by `shared/map`; no colour or arbitrary value outside the layer.
