# Review — PR #57, merged from three reviewers (Copilot, OpenCode, Codex)

Head `36507590ff1783bb988883707318121c62b4a5ad`, base `49cd088`. Each finding names the reviewers who
raised it; duplicates are merged. Verification against the code follows in §3.

## 1. Findings

**R1 · should-fix · the list is not refetched after a creation** *(Copilot 1, Codex 1)*
`apps/web/src/features/spaces/hooks/add/useCreateSpace.ts:23–25`. On `/dashboard/admin/spaces/new`
the spaces page is unmounted, so its list query is inactive. `refresh()` invalidates `['admin']`,
and invalidation refetches only **active** queries by default: the awaited promise settles without
fetching the list, and the toast and the navigation run before the list is fresh. The form test keeps
a list query mounted beside the form (`useAddSpaceForm.component.test.tsx:125–140`), so it misses the
real route. **Fix:** refetch the admin list (inactive queries included, e.g. `refetchType: 'all'` or
an explicit refetch) and await it before the toast and the navigation; a test with no list mounted.

**R2 · should-fix · a tile failure after one tile loaded is hidden** *(Copilot 2 should-fix, Codex
nit)* `apps/web/src/shared/map/hooks/useTileStatus.ts:17–18`. Once any tile has loaded, `loaded`
suppresses every later `tileerror`, so a map left partly blank shows no failure line; the ref also
survives the language-keyed remount of the map. **Fix:** show the line on a tile failure whatever
loaded before (or once failures pass a threshold), and reset the status for each map lifecycle.

**R3 · should-fix · a commit subject is 52 characters** *(all three)*
`df998c9` `fix(design-system): keep the data table off the site`; the limit is 50 (workflow §3).
**Fix:** reword it, e.g. `fix(design-system): keep the table off the site` (47).

**R4 · should-fix (by the owner's rule) · a function only the tests call** *(OpenCode 6)*
`apps/web/scripts/libraryChunks.ts:24` exports `libraryChunkOf`, which no production code calls
(`vite.config.ts` and `checkBuild.ts` read `LIBRARY_CHUNKS`); only `libraryChunks.unit.test.ts`
uses it. **Fix:** remove it; test the `LIBRARY_CHUNKS` patterns directly.

**R5 · to verify · five lock-file entries changed from `dev` to `devOptional`** *(OpenCode 2 nit;
Copilot and Codex: acceptable)* `package-lock.json`: `ajv`, `fast-json-stable-stringify`,
`json-schema-traverse`, `punycode`, `uri-js`. OpenCode says a production install
(`npm ci --omit=dev`) now keeps this eslint-only tree, through `@hookform/resolvers`' optional peer
`ajv`; Codex says the flags alone add nothing to a production install; Copilot traces them to an
optional runtime chain. **The reviewers disagree;** §3 settles it. **Fix if real:** regenerate the
lock without the unrelated flips, or state them as accepted.

**R6 · nit · two documents' dates not bumped** *(OpenCode 4)*
`docs/frontend/architecture.md:3` and `docs/frontend/design-system/foundation.md:7` still say
`Last Updated: 2026-10-07`, though this PR edits them; the capability documents it edits were bumped.
**Fix:** 2026-10-10.

**R7 · nit · finding 46 is linked from no document of its area** *(OpenCode 5)*
`docs/features/spaces.md` (*Open findings* lists 43 and 44) and `docs/frontend/architecture.md` §6
don't link it, as `auth.md` links finding 33. **Fix:** link it from `spaces.md`'s *Open findings*.

**R8 · nit · finding 46's number against the index's rule** *(OpenCode 3)*
`docs/architecture/findings/README.md:10` says "A new finding takes the next number" (49 after 48),
but workflow §9 *Conflicts* gives each worker its own range (A: 46–47). The number is right by the
workflow; the index's sentence contradicts the workflow. **Fix:** the index's rule says numbers come
from each worker's range (workflow §9), and 46 stays.

## 2. Checked and fine (by at least two reviewers, none disagreeing)
The form's body, parsing and validation (Arabic digits, the Strip's box); 422 on fields with focus,
409, 429; the map lazy, its pin from tokens, `dir="ltr"`, the attribution, `leaflet.css` imported only
by `shared/map`; the build checks failing on a first-download library chunk, a missing chunk and
Leaflet's CSS; every `DataTable` importer on the new entry; no `vi.mock`; every new string in both
catalogues; findings 45 resolved, 46 added, 27 untouched; the other four commit subjects.

## 3. Verification against the code (two read-only subagents, at the pinned head)

- **R1 — PARTLY: the mechanism is right, the harm is narrower.** `useRefreshAdmin.ts:13` invalidates
  `['admin']` with the default `refetchType: 'active'` (query-core 5.104.1, `queryClient.ts:478–486`);
  on `/new` no `['admin', …]` query is active (`AreaSelect` reads `['public', …]`, the hold uses
  `skipToken`), so `refresh()` resolves at once and the toast and the navigation follow at once
  (`useCreateSpace.ts:22–25`, `AddSpacePage.tsx:46–48`). **The list is not left stale:** the
  invalidated query refetches on mount (`queryObserver.ts:847–856`); the admin briefly sees the old
  rows without the new space, then it appears. **The JSDoc** (`useCreateSpace.ts:13–15`,
  `useAddSpaceForm.ts:49–50`: "pending until the list has arrived again") **is false on the real
  route**, and the test mounts a list beside the form (`:50–58`, relied on at `:126–138`), so it
  proves a path the route never takes.
- **R2 — CONFIRMED.** `useTileStatus.ts:10,17–18`; the hook is called at `LeafletPointPicker.tsx:86`,
  outside the `MapContainer` keyed by language (`:108`), so the ref survives the remount. A naive
  "any `tileerror` shows the line" would flicker (each `tileload` clears it). Leaflet's `loading` and
  `load` events (GridLayer 1.9.4) mark one load cycle.
- **R3 — CONFIRMED.** Subjects 42, 33, 42, 46 and **52** (`df998c9`).
- **R4 — CONFIRMED.** `libraryChunkOf` is defined at `libraryChunks.ts:24` and called only by
  `libraryChunks.unit.test.ts:2,16,25`; its first-match lookup even skips the dashboard group that
  comes first in `vite.config.ts:30–34`, so it does not mirror the real chunking.
- **R5 — PARTLY: real, harmless, no fix.** The lock adds `leaflet`, `react-leaflet`,
  `@react-leaflet/core` (prod) and `@types/leaflet` (dev), nothing removed or re-versioned. The five
  flips come from `@hookform/resolvers`' optional peer `ajv` (already in the base lock): npm 11's flag
  calculation re-ran during the install; Leaflet did not cause it. `npm ci --omit=dev` would now
  install those five small packages, but nothing runs it (CI uses plain `npm ci`), nothing imports
  them, and Vite bundles nothing extra. Never hand-edit the lock (workflow §9).
- **R6 — CONFIRMED, and wider:** `docs/project/overview.md:3` (the PR edits its spaces line) also
  still says 2026-10-07, beside architecture and foundation.
- **R7 — CONFIRMED.** The index is finding 46's only link; the tile rule is the map's, so its home
  is architecture §6.
- **R8 — PARTLY.** The contradiction is real, but workflow §9 states no ranges itself: it says each
  prompt gives its worker a range, and A's prompt gave 46–47. **46 is correct**; the index's sentence
  ("the next number") is what needs the change.
