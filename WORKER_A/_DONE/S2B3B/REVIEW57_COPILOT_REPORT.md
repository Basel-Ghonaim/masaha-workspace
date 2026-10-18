Verdict: Changes requested — two should-fix issues and one commit-subject nit.

## Findings

1. **should-fix — `apps/web/src/features/spaces/hooks/add/useCreateSpace.ts:23–25`** — After creating a space from `/dashboard/admin/spaces/new`, the spaces-list query is inactive because the list page has been replaced. `refresh()` only invalidates `['admin']`; TanStack Query's default invalidation refetches active queries, so the awaited promise can resolve without refreshing the cached list. The success toast then appears and navigation begins before the list fetches on mount. The form test keeps a list query active alongside the form (`useAddSpaceForm.component.test.tsx:125–140`), so it does not cover this route scenario. **Fix:** explicitly refetch the cached admin spaces query (including inactive queries), and await that fetch before showing the toast or navigating.

2. **should-fix — `apps/web/src/shared/map/hooks/useTileStatus.ts:17–18`** — A tile error is ignored after any tile has loaded. If an initial tile succeeds but another fails, the map can remain partially blank without the required failure line. The `loaded` ref also survives the language-keyed map remount, so later tile failures can be suppressed. **Fix:** surface tile errors after partial loads and reset/track tile status for each map-layer lifecycle.

3. **nit — `git log: df998c9`** — The subject `fix(design-system): keep the data table off the site` is 52 characters, exceeding the stated 50-character limit by two. **Fix:** shorten the subject.

## Checked and fine

- Blank optional fields are omitted; coordinate parsing accepts Arabic digits, and the schema rejects malformed/out-of-bounds points. The 422 field-error mapping and 409/429 refusal paths are wired.
- The area selector uses the public catalogue; the map is lazy, uses a custom token-based pin, and imports its stylesheet only from `shared/map`. The build guard checks the first-download manifest for library chunks and Leaflet CSS.
- `DataTable` consumers use the separate design-system data entry; the main barrel no longer exports it. No added tests use `vi.mock`.
- The lockfile's five `dev` → `devOptional` changes are `ajv`, `fast-json-stable-stringify`, `json-schema-traverse`, `punycode`, and `uri-js`. They follow the optional runtime dependency chain through `@prisma/streams-local`/Ajv; these are not purely dev-only packages, though an install may include them via that optional production path. No other lockfile changes were present beyond the Leaflet packages and dependencies.
- The edited feature/build documentation matches the code; finding 45 is resolved, finding 46 is added, and finding 27 is untouched. Four commit subjects meet the limit; `df998c9` does not.
