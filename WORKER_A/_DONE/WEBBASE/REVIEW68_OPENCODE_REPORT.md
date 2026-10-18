# Review — PR #68 (WEBBASE)

Head: `9cb6382a3a7ff6d106ddef26b234cd13408a8a7d` (branch `refactor/web-storage-titles`). Base: `068efc6407c490d315192ad0db4c02bb2ced6728` (`git merge-base origin/main <head>`). Read via `git show <head>:<file>` and `git diff <base>...<head>` only.

Verdict: accept — no blockers, one nit below.

## Findings

### Nit — `PageHeader` renders an empty `h1` on an untitled route

- **Severity:** nit (latent — no current route reaches it; plausible rather than observed).
- **File:** `apps/web/src/pages/dashboard/shell/PageHeader.tsx:18` (`<h1 className="text-heading-3">{title}</h1>`, `title` from `usePageTitle()`, `string | undefined`).
- **Scenario:** a route with no `handle.title` that renders `PageHeader` shows an empty heading while `DocumentTitle` falls back to the wordmark alone, so the top bar is an empty `h1` where the tab shows `Masaha` / `مساحة`. Today every leaf that renders `PageHeader` carries a title (`pageTitles.unit.test.ts` enforces it; `/dashboard` renders no `PageHeader`), so nothing fails now; a future untitled page (or a D2b record page in a state with neither route nor record title) would hit it.
- **Fix:** render the wordmark fallback as `DocumentTitle` does, or render no `h1` when `title` is `undefined`, e.g. read the same `copy.site.wordmark` `DocumentTitle` uses, keeping the two readers on the one source.

## Checked and fine

- Storage guard (`shared/storage/storage.ts`): reaching `globalThis.localStorage`, `getItem`, `setItem` (quota included), `removeItem` all inside `guarded`; no module-load capture; `read` → `null`, writes harmless on throw.
- Lint rule (`eslint.config.js` storage block): `no-restricted-globals` for bare `localStorage`/`sessionStorage`, `no-restricted-properties` for `window`/`globalThis`/`self` × both properties; ignores only `shared/storage/**`, `src/test/**`, `**/*.test.{ts,tsx}`. No non-exempt storage reach remains outside the layer (verified via `git grep` on the head).
- Key names/values unchanged: `masaha.language`, `masaha.theme`, ``masaha.lastSpace.${userId}`` identical to base (`PREFERENCE_KEYS`, `keyFor`); plain-string values with owner-side validation (`isLanguage`/`isTheme`, strict `String(spaceId)` match); pre-paint script reads the same literals, diff is comment + `<title>` only.
- Titles: every site leaf (9) and dashboard leaf (admin 8 + add-space + 2 × 404 + space 12) carries `handle.title` as `(copy) => copy.…`; `DocumentTitle` mounted once in `RootLayout`, `{page} · Masaha` / `{page} · مساحة` with wordmark-alone fallback, effect on `[title]` so language and navigation update it; `PageHeader` prop-less, reading the same `usePageTitle()`; `index.html` default `<title>مساحة</title>`; `pageTitles.unit.test.ts` walks all leaves (31 pages, `>20` guard) in both languages.
- D2b record-name rule (architecture §2): both readers go through `usePageTitle()`, so a `RootLayout`-held context preferred by that hook reaches tab and top bar without touching `DocumentTitle`/`PageHeader`/handles; portal crossing is ordinary React context behaviour. Plausible without rework, as claimed.
- First download: route files import no copy/catalogue and no dashboard modules (titles are lambdas over the handed catalogue; dashboard pages all lazy except shared `NotFoundState`); architecture §3 sentence matches this.
- Tests: `findToast` waits for visibility (`waitFor` + `getByText` + `toBeVisible`), used by all 7 toast files; `topBarTitle(name)` requires the name at all 10 call sites; no `vi.mock` in the touched tests; seam is the stubbed/blocked global (`fakeStorage`), `fakePlatform` shares the one `Map` with the stub; worker's run counts (42: 50/50, 20/20 probe, 0/80, 2/200, 200/200; 47: 4/5 repro, 5/5 fixed, main 2/2 fail vs branch 7/7 pass) match findings 42/47 resolutions exactly.
- Documents: architecture §4 (storage + rule), §2 (titles + D2b), §3 (first-download sentence), localisation mechanism sentence, foundation §10 line, testing seam sentence, findings 35/42/47 resolved with 55 new, index moves — each true to the code, single home with links.
- Scope: web + docs only (`apps/web`, `docs`, `eslint.config.js`); no `apps/api` or `packages/shared` hunks; session hint untouched.
- Commits: four — `bb603ce` (52 chars, over, permitted as first), `2f96377` (43), `ccf30b0` (43), `9cb6382` (37).

Head re-checked at end: `gh pr view 68 --json headRefOid` still `9cb6382a3a7ff6d106ddef26b234cd13408a8a7d`.
