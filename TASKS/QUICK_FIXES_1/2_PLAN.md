# Plan — QUICK_FIXES_1

## Files changed
- `apps/web/src/shared/lists/components/ListPagination.tsx` — return `null` when both steps are unavailable (one page or none), so the bar is hidden.
- `apps/web/src/pages/site/public/privacy/PrivacyPage.tsx` — drop the trailing `{words.end}` dot.
- `apps/web/src/shared/copy/english/site.ts`, `apps/web/src/shared/copy/arabic/site.ts` — remove the now-unused `end` entry.
- Tests: `ListPagination.component.test.tsx`, `AdminSpacesList.component.test.tsx`, `PrivacyPage.component.test.tsx`.

## Tests added/updated
- Component: one page → no bar; two pages → bar (shared `ListPagination`), plus AdminSpacesList witness.
- Privacy: expected text without trailing dot.
