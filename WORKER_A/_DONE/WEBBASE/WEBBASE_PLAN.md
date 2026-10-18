# WEBBASE — plan: one browser-storage layer, page titles, and two unstable tests

Worker A · main folder · branch `refactor/web-storage-titles`.
- **Planned on** `d7d800e`. **Approved** by `WEBBASE_PLAN_REPLY.md`: §13's decisions 1, 2 and 4 as
  proposed, and decision 3 with its condition (D2b below).
- **The branch is cut from `068efc6`**, the latest `main` (#61 and #62 merged), after
  `git fetch --prune origin`. `findings/README.md` already holds #62's edits.
- **The amenities worker** may edit one fixture line of `dashboard/routes.component.test.tsx`; I keep
  to my own hunks.

## 1. Summary

Three pieces of web groundwork that no design decision touches:
- **`shared/storage`**: the one way to browser storage (Issue #37). The preferences and the last space
  go through it; lint keeps every other file away from `localStorage` and `sessionStorage`.
- **A document title on every page** (finding 35): each route declares its title, one place sets
  `document.title` (`{page} · Masaha` / `{page} · مساحة`), and the dashboard's top bar reads the same
  title. `index.html` gets a default title.
- **The two unstable tests** (findings 47, 42): the dashboard test waits for the chosen page's title,
  and the registration test's failure is reproduced, its cause found and fixed.

## 2. The contract

**Scope**
- `apps/web/src/shared/storage/` (new); the preferences and `lastSpace` moved onto it; `src/test`
  storage helpers; an ESLint rule.
- Route titles: `shared/routing` (the title's hook and setter), `RootLayout`, both groups' route
  definitions, the dashboard's `PageHeader`, its pages' calls to it, both `site` catalogues,
  `index.html`.
- The dashboard routes test (47); the registration test, and any test with the same cause (42).
- Documents: `frontend/architecture.md`, `frontend/localisation.md` (one sentence),
  `frontend/design-system/foundation.md` §10, `development/testing.md` (one sentence), findings 35,
  47, 42 and the index.

**Acceptance criteria**
- [ ] No file outside `shared/storage` reaches `localStorage` or `sessionStorage`; lint fails if one
  does (test files and `src/test` exempt).
- [ ] The stored keys keep their names: `masaha.language`, `masaha.theme`, `masaha.lastSpace.<userId>`.
- [ ] With storage throwing on every call, the app renders and its language and theme still change.
- [ ] Every page of the site and the dashboard has a title in both languages. The tab reads
  `{page} · Masaha` / `{page} · مساحة` and follows a language change. A route with no title gives
  the name alone. `index.html` has `<title>مساحة</title>`.
- [ ] The dashboard's top-bar title and the tab's title come from the route's one title.
- [ ] Finding 47 resolved: no test reads the top bar's title before the page it waits for has loaded.
- [ ] Finding 42 resolved, with its evidence (reproduction, cause, fix, the count of runs) or the count
  of clean full runs.
- [ ] Every local check passes on the head; a real run as §12 describes.
- [ ] PR `refactor(web): storage layer and page titles`, labels `refactor`, `area:web`, `area:docs`,
  assigned to the owner, `Closes #37`.

**Out of scope**: finding 27, the shell's redesign, design-system components, `sessionStorage`
(no use needs it), the session hint cookie, a title mechanism for record pages (D2b below), the API.

## 3. Reading done

- CLAUDE.md, workflow (all), the docs map, the findings index. Findings 35, 47, 42 in full; 28 and 6
  (resolved by a longer wait and by warming jsdom); 27 and 40 checked (not related).
- Issue #37.
- `frontend/architecture.md` (all), `frontend/localisation.md` (all), foundation §10, `testing.md`
  (all), `engineering-principles.md` (all).
- Code: `shared/preferences` (`platform.ts`, `preferences.ts`, its unit test),
  `shared/routing/landing/lastSpace.ts` and its test, `shared/session/repository/sessionHint.ts`,
  `src/test/` (`fakeStorage`, `fakePlatform`, `startPreferences`, `componentSetup`), `app/` (router,
  RootLayout, bootstrap, App and providers tests, `prePaint.unit.test.ts`), both groups' `routes.tsx`
  and `navigation.ts`, every site and dashboard page, `PageHeader` / `PageHeaderSlot` / `TopBar` /
  `DashboardLayout` / `PlaceholderPage`, `index.html`, the `site` / `dashboard` / `status` / `auth`
  catalogues, `eslint.config.js`, `dashboard/routes.component.test.tsx`,
  `useRegister.component.test.tsx` and `useRegister.ts`, Sonner 2.0.8's toast mount code and its
  injected CSS.
- Open PRs: #62 touches `shared/copy/*/errors.ts`, `findings/README.md` and `workflow.md`; #61 none of
  the web.

## 4. The settled decisions, as they will be built

### D1 — `shared/storage`

**Files (flat; one role):**
- `shared/storage/keys.ts`: `STORAGE_KEYS`, the one list of what the app keeps on a device:
  ```ts
  export const STORAGE_KEYS = {
    language: 'masaha.language',
    theme: 'masaha.theme',
    lastSpace: (userId: number) => `masaha.lastSpace.${String(userId)}` as const,
  } as const;
  export type StorageKey = 'masaha.language' | 'masaha.theme' | `masaha.lastSpace.${string}`;
  ```
  (`StorageKey` is derived from `STORAGE_KEYS` in the code.)
- `shared/storage/storage.ts`: `storage` with `read(key): string | null`, `write(key, value): void`
  and `remove(key): void`.
- `shared/storage/index.ts`: exports `storage`, `STORAGE_KEYS`, `type StorageKey`.

**What it knows:**
- `localStorage`, reached on each call as `globalThis.localStorage`, inside the guard. Chrome throws
  on reaching the property itself when site data is blocked, and Node has no such global.
- The guard: `read` gives `null` when nothing is stored or storage throws. `write` and `remove`
  do nothing when it throws (blocked, full). The page keeps working: a choice holds for this page.
- How a key is named: the `masaha.` prefix, and every key declared in `keys.ts`. The API takes only
  a `StorageKey`, so a key nobody declared fails the typecheck.

**What it does not know:**
- What a value means. Values are plain strings, and each owner checks what it reads: the preferences
  with `isLanguage` / `isTheme`, the landing by matching a link. Anything can write storage (another
  tab, an older version, the user), so the check belongs to the owner, which knows the domain.
  Typed values per key would bring the catalogues and the themes into the layer for no second use.
- The `storage` event. It is the window's, and only the preferences listen to it, so it stays in
  their `Platform.events`. Only the key's name comes from `STORAGE_KEYS`.
- `sessionStorage`. No use needs it; lint forbids it until a use adds it to the layer.

**The moves:**
- `preferences.ts`: `stored` and `persist` go. Reads and writes use `storage.read` / `write` /
  `remove` with `STORAGE_KEYS`. `PREFERENCE_KEYS` is removed from the module and its barrel.
  `Platform` loses `storage`. `browserPlatform` keeps `root`, `prefersDark` and `events`.
- `lastSpace.ts`: `rememberSpace` and `lastSpace` use the layer. Their own try/catch goes.
- `index.html`'s comment points at `shared/storage` as the owner of the keys; the script itself is
  unchanged. It runs before the bundle and stays the documented exception, held by
  `prePaint.unit.test.ts`.

**The seam:** tests stub the global `localStorage`, the way the layer reaches it. No `vi.mock`.
- `src/test/fakeStorage.ts`: `stubLocalStorage` and `blockLocalStorage` gain `removeItem`.
- `src/test/fakePlatform.ts`: keeps its `stored` / `storageThrows` options and `stored()` /
  `otherTabWrites`, now built on `fakeStorage`'s stub. Its callers (`preferences.unit.test.ts`,
  `session.unit.test.ts`, `prePaint.unit.test.ts`) add `vi.unstubAllGlobals()` where they lack it.

**The rule (lint),** in `eslint.config.js`, a block for `apps/web/src/**/*.{ts,tsx}`:
- `no-restricted-globals`: `localStorage` and `sessionStorage`;
- `no-restricted-properties`: `window` and `globalThis` with `.localStorage` and `.sessionStorage`;
- the message: "Browser storage goes through @shared/storage.";
- turned off for `apps/web/src/shared/storage/**`, `apps/web/src/test/**` and `**/*.test.{ts,tsx}`.
  Tests stand in for the browser, or read the raw key to prove its name.

**Kept as is:** the session hint stays the session's. It is a cookie the server sets and clears
beside the refresh cookie, not storage, and moving it gives nothing.

### D2 — the document title

- **The route says it.** A route's `handle` carries `title: (copy: Catalogue) => string`. The type
  is `TitledHandle` in `shared/routing/title/`. Every leaf route of `siteRoutes` and
  `dashboardRoutes` declares one:
  - home, the directory and about: `copy.site.links.*`;
  - sign-in, register, forgot password and reset password: their `copy.auth.*.title`;
  - the forced change: `copy.users.passwordChange.title`;
  - each 404 (`*`): `copy.status.notFound.title`;
  - each dashboard page: `copy.dashboard.pages[name]`, from its navigation item;
  - add space: `copy.dashboard.addSpace.title`;
  - the exception is `/dashboard`, a redirect that shows nothing of its own.
- **One hook reads it:** `usePageTitle()` in `shared/routing` returns the deepest matching route's
  title (`useMatches`) in the current language (`useCopy`), or `undefined`.
- **One place sets it:** `DocumentTitle`, in `shared/routing/title/` and mounted once in
  `RootLayout`, sets `document.title` in an effect:
  - with a title: `copy.site.documentTitle({ page })`, a new line in both catalogues beside
    `wordmark` (`` `${page} · Masaha` `` / `` `${page} · مساحة` ``);
  - with none: `copy.site.wordmark`.
  - It renders again when the language changes, so the tab follows it.
- **The dashboard's top bar reads the same title.** `PageHeader` drops its `title` prop and renders
  `usePageTitle()`. `PlaceholderPage` drops its `name` prop and becomes `<PageHeader />`.
  `SpacesPage`, `LookupsPage` and `AddSpacePage` drop the title they passed. The top bar and the tab
  cannot disagree.
- **`index.html`:** `<title>مساحة</title>`, matching the markup's fallback `lang="ar"`, shown until
  the bundle runs.
- **D2b — a page whose title is a record's name** (the space's edit screen, S2b-4, is next; the
  details page later): the rule is written down now and built with its first page, which is its
  first caller (engineering principles §1). *Approved, on a condition: the name must serve the top
  bar as well as the tab.*
  - **The rule:** the route's title shows while the record loads. Then the page gives the record's
    name to `usePageTitle`, the one place both the top bar (`PageHeader`) and `document.title`
    (`DocumentTitle`) read, never to either of them directly.
  - **Why the shape takes it without rework:** both readers already go through `usePageTitle()`.
    Adding the name changes that hook's body only, plus one small provider:
    - `RootLayout`, which already mounts `DocumentTitle` above the `Outlet`, hosts a context that
      holds a record title;
    - the page sets it with a hook (for example `usePageRecordTitle(name)`), which clears it in its
      effect's cleanup when the page unmounts;
    - `usePageTitle()` returns that title when one is set, else the route's.
    - `PageHeader` renders through a portal, and React context crosses portals, so it reads the same
      value.
  - **What does not change:** `DocumentTitle`, `PageHeader`, the routes' `handle` and the catalogue
    format. The plan builds `usePageTitle` as a hook from the start, never inlined in its two
    readers, so that this holds.
- Foundation §10 gains a line saying every page has a document title in the interface's language
  (WCAG 2.4.2), and links architecture §2 for how it is set.

### D3 — finding 47

`topBarTitle(name)` in `dashboard/routes.component.test.tsx` becomes
`within(await screen.findByRole('banner')).findByRole('heading', { level: 1, name })`, and every use
passes the name. The drawer test then waits for "Customers". The same race is in "closes the drawer
when another space is chosen in it" (line 372: the old space's shell stays on screen while the new
page loads), and the name-taking helper fixes it too (*Stronger decisions 1*).

### D4 — finding 42

**Cause (to confirm):** Sonner draws a new toast with `opacity: 0` (`[data-sonner-toast]` in its
injected CSS). It turns it visible only on a second render, from a `useEffect` (`setMounted(true)`)
that runs after the toast is added inside `setTimeout` + `flushSync`, outside `act`.
`findByText` can resolve between the two renders, and `toBeVisible()` then fails at once. That
matches a failure after 761 ms, well inside the 3 s wait.

**Method:**
1. Reproduce on the branch before any change: run `useRegister.component.test.tsx` alone in a loop
   (50×), then under CPU load (24 busy loops on 12 cores, as finding 6), then the full lane. Keep
   every failure's message.
2. Confirm the cause from the message (`not visible … opacity: 0`) and from the toast's
   `data-mounted` at the moment `findByText` resolves.
3. Fix the test, not the toast: one helper in `src/test/`, `findToast(text)`, waits until the toast
   is visible (`waitFor` + `toBeVisible`). Every toast assertion of that shape uses it:
   `useRegister`, `useGoogleSignIn` (×2), `useChangePassword`, `providers` (`حُفظ`), and any other
   the grep finds (*Stronger decisions 2*).
4. Prove it: the same loops under load after the fix, and the full lane 5 times (§12).

If the cause cannot be reproduced after those runs, finding 42 is resolved by evidence: the counts,
under load and in full runs, written in its resolution. No code change rides on an unconfirmed
cause. If a different cause shows, it is fixed as found (systematic-debugging; stop after three
failed fixes, workflow §8).

## 5. Stronger decisions

1. **The top-bar helper requires the title's name** (D3).
   - **What:** every use waits for the page it expects, not only the drawer test.
   - **Why:** the same race sits at line 372, and a helper that can read any title invites it again.
   - **Cost:** about 10 changed lines in one test file.
   - **Recommendation:** do it.
2. **One `findToast` helper for every toast test of that shape** (D4), if the cause is confirmed.
   - **Why:** the same race sits in at least 4 other tests; fixing one leaves the flake for later.
   - **Cost:** one helper file and about 6 test lines in 4–5 files (`features/auth`,
     `features/users`, `app`), none in `features/lookups`.
   - **Recommendation:** do it.
3. **`PageHeader` reads the route's title, with no `title` prop** (D2).
   - **What:** this goes further than "where they can". The page can no longer pass a title that
     differs from the tab's.
   - **Cost:** `PageHeader` depends on the route's match. A record page will need its own way in
     (D2b).
   - **Recommendation:** do it.
4. **A unit test that every page route has a title in both languages.**
   - **What:** `app/pageTitles.unit.test.ts` walks `siteRoutes` and `dashboardRoutes`. It lives in
     `app/` because only the app may import both groups.
   - **Why:** "every built page gets one" becomes a check, not a review item. A new route without a
     title fails.
   - **Cost:** one test; it moves to the component lane if loading the route modules needs a DOM
     (said in the report).
   - **Recommendation:** do it.
5. **Keys typed as `StorageKey`** (D1).
   - **What:** the typecheck refuses a key nobody declared, beside lint's refusal of the global.
   - **Cost:** none.
   - **Recommendation:** do it.
6. **A rule this item changes:** architecture §3 says the route definitions in the site's first
   download "hold paths, guards and lazy imports only". They will also hold titles: small functions
   of the catalogue they are handed, with a type-only import of `Catalogue` and no copy in the
   download. The sentence is updated. **Cost:** a few hundred bytes in the first download.
   `check:build` still passes, because the dashboard's chunk and the libraries stay out of it.
7. **`testing.md`, one sentence** in *A feature, layer by layer*.
   - **What:** browser storage's seam is the global `localStorage` the layer reaches
     (`fakeStorage`), as the cookie's is `document`.
   - **Why:** D1 sets the seam, and testing owns where seams are named.
   - **Recommendation:** add it.

## 6. Related findings

- **35, 47, 42: folded** (the prompt). Each is resolved in its commit, with its status line, a
  resolution, and its move in the index.
- **27: not folded** (the owner leaves it open). The titles add no dashboard import to the first
  download.
- **28, 6: resolved;** read for method only.
- **40, 22: not related.**
- No other open finding touches storage, titles or these tests.
- New findings, if any, take 55–56.

## 7. Files

All of them are in the web layer and the documents; no licence in the API is needed.
- **New:**
  - `shared/storage/{index,keys,storage}.ts` and `storage.unit.test.ts`;
  - `shared/routing/title/{usePageTitle.ts,DocumentTitle.tsx,titledHandle.ts}` and
    `DocumentTitle.component.test.tsx`;
  - `app/pageTitles.unit.test.ts`;
  - `src/test/findToast.ts`.
- **Changed:**
  - `shared/preferences/{platform,preferences,index}.ts` and `preferences.unit.test.ts`;
  - `shared/routing/landing/lastSpace.ts`, `shared/routing/index.ts`;
  - `app/RootLayout.tsx`, `app/App.component.test.tsx`, `app/session.unit.test.ts`,
    `app/prePaint.unit.test.ts` (teardown only), `app/providers.component.test.tsx` (toast);
  - `pages/site/routes.tsx`, `pages/dashboard/{routes.tsx,PlaceholderPage.tsx}`,
    `pages/dashboard/shell/PageHeader.tsx`,
    `pages/dashboard/admin/{SpacesPage,LookupsPage,AddSpacePage}.tsx`,
    `pages/dashboard/routes.component.test.tsx`;
  - the toast tests: `features/auth/hooks/{register,google-sign-in}/…component.test.tsx`,
    `features/users/hooks/useChangePassword.component.test.tsx`;
  - `shared/copy/{english,arabic}/site.ts`;
  - `src/test/{fakeStorage,fakePlatform}.ts`;
  - `apps/web/index.html`, `eslint.config.js`;
  - the documents in §2.
- **Shared with others, edited minimally:**
  - `pages/dashboard/admin/LookupsPage.tsx`: one line, the `PageHeader` call. The amenities worker
    owns `features/lookups/` only, but may touch this page; a conflict keeps both sides.
  - `docs/architecture/findings/README.md`: PR #62 edits it too. I move only lines 35, 42 and 47.
  - Not touched: `shared/copy/*/errors.ts` (#62), `features/lookups/`, `docs/design/`.

## 8. Design issues

None. No screen's look changes. The top bar shows the same title from a different source, and the
tab's title is not part of the designs.

## 9. Tests: lane, test, the break it catches

| Behaviour | Lane | Test | Break it catches |
|---|---|---|---|
| The layer reads the value stored at a key, and `null` for none | Unit | `storage.unit.test.ts` | reading another key, or `undefined` for none |
| It writes and removes the plain string at the key | Unit | same | JSON-wrapping a value; `remove` that writes `''` |
| Storage that throws: `read` is `null`; `write` and `remove` are harmless | Unit | same (`blockLocalStorage`) | dropping the guard |
| No `localStorage` at all (reaching it throws) | Unit | same (Node, no stub) | capturing `localStorage` once at module load, outside the guard |
| The preferences and the last space through the layer: unchanged behaviour, the same keys | Unit | existing `preferences.unit.test.ts`, `lastSpace.unit.test.ts`, `prePaint.unit.test.ts` (each made to fail once by renaming a key in `STORAGE_KEYS`) | a renamed key |
| With storage blocked the app renders, and its language toggle works | Component | `App.component.test.tsx`, new case: block, bootstrap, render, click "English", `h1` "Home" | a storage path outside the guard that throws at start or on a toggle |
| Every page route has a title in `ar` and `en`, never empty | Unit | `app/pageTitles.unit.test.ts` | a route added without a title |
| The tab reads `{page} · Masaha` from the deepest titled route | Component | `DocumentTitle.component.test.tsx` | the shallowest match taken, or the format changed |
| It follows a language change (`… · مساحة`) and a navigation | Component | same | copy read once; the effect not re-run |
| A route with no title gives the name alone | Component | same | a stale title, or "undefined · Masaha" |
| The setter is mounted in the app | Component | `App.component.test.tsx`: `document.title` "Home · Masaha" after the toggle | `DocumentTitle` not mounted in `RootLayout` |
| The top bar shows the route's title | Component | existing dashboard tests (`topBarTitle(name)`), now that the title comes from the route | `PageHeader` reading the wrong match |
| 47: the drawer test waits for "Customers" | Component | the test itself; seen failing by pointing the drawer's link at the overview once | — |
| 42: a toast is asserted only once it is visible | Component | `findToast`; seen failing by asserting before the mount (a direct `getByText` + `toBeVisible` right after `findByText`, under load) | — |

Every new test is seen failing before its code (testing §3 rule 5). Lint's rule is proven by adding a
`localStorage.getItem` outside the layer once and seeing `npm run lint` fail.

## 10. Review Focus (inputs no planned test exercises)

- A toggle in another tab while storage is blocked: no `storage` event fires, so the tabs drift
  apart. That is expected; nothing persists.
- Reaching `localStorage` throwing in the component lane: jsdom's getter does not throw, so only the
  unit lane covers that shape.
- An error boundary or a guard's 403 / 404 inside a titled route: the tab keeps the page's title.
  When a shell itself fails, `RootError` leaves the last title.
- `/dashboard` while the session is restored shows the name alone.
- The showcase (development only) has no titles; it shows the name alone.
- A language change while a lazy page is loading: the tab changes once the new route has matched.

## 11. Commits

1. `refactor(web): one storage layer for browser storage`: `shared/storage`, the preferences and
   the last space on it, the test helpers, the lint rule, the App test with blocked storage, the
   `index.html` comment, and architecture §1 (the `shared` list, the class line) / §2 (the last
   space) / §3 (*Where state lives*) / §4 (a `shared/storage` bullet), localisation's key sentence
   and testing's seam sentence.
2. `feat(web): give every page a document title`: titles in the routes, `usePageTitle`,
   `DocumentTitle`, `PageHeader`, the catalogues, `index.html`'s `<title>`, the tests,
   architecture §2 / §3, foundation §10, and finding 35 resolved with the index.
3. `test(web): wait for the chosen page's title`: finding 47 resolved, with the index.
4. `test(web): read a toast once it shows`: finding 42 resolved with its evidence, and the index. If
   it is not reproduced: `docs(findings): resolve the registration test's failure`, evidence only.

Lint and typecheck run on each commit; the lanes run once, on the head.

## 12. Verification (phase 4)

- **On the head, one at a time:**
  - `test:unit`, `test:component`;
  - `NODE_ENV=production npm run build`, then `check:build`;
  - `lint`, `typecheck`, `check:classes`, `format:check`, `check:links`.
- **Not run:** `test:api`, because nothing in the API changes.
- **The unstable tests:**
  - before the fixes: the two files alone, in loops, unloaded and under load (24 busy loops);
  - after: the same loops, and 5 consecutive full `test:component` runs;
  - the counts and results go in each finding's resolution and the report.
- **A real run** on 5320, with the API on 3320 (`masaha_dev`):
  - `document.title` read on each page group (site, focus shell, dashboard admin, dashboard space)
    in Arabic and English, and after a toggle;
  - the language and theme kept after a reload;
  - with site data blocked for `localhost` in Chrome's settings: the page renders, the toggles
    work, and a reload forgets them;
  - screenshots in `C:\Users\basel\Downloads\webbase-shots\`; the tab strip is shown where the tool
    can capture it, and the titles read are recorded either way;
  - the servers stopped by PID, and ports 3320 and 5320 checked free.
- **At the report:** `git merge-tree --write-tree` against every open PR (the amenities worker's
  `feat/space-own-amenities`, the design fixer's `design/admin-rest`).

## 13. Decisions needed from the owner

1. Stronger decisions 1–5 and 7 (the named top-bar helper, `findToast` across the toast tests,
   `PageHeader` without a title prop, the titles unit test, the typed keys, testing's seam sentence).
2. The lint rule's exemptions: `shared/storage`, `src/test`, and test files.
3. D2b: the record-name title is written as a rule and built with its first page, not now.
4. Architecture §3's first-download sentence widened to include titles (Stronger decisions 6).
