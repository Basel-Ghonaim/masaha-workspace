# WEBBASE — report

## 1. The pull request

[#68 `refactor(web): storage layer and page titles`](https://github.com/Basel-Ghonaim/masaha/pull/68):
- **Head:** `9cb6382`, on branch `refactor/web-storage-titles`, cut from `068efc6`.
- **State:** CI run 38294707500 passed on `9cb6382`, every check green (`test:component` included), and GitHub shows `CLEAN`.
- **Labels and description:** `refactor`, `area:web`, `area:docs`; assigned to the owner; `Closes #37`.
- **Review:** the PR touches **49 files**. That is above workflow phase 7's ~25-file threshold, so it calls for a separate review conversation rather than the analyst alone.

## 2. The commits

1. `bb603ce` refactor(web): one storage layer for browser storage
   - `shared/storage`: the guarded `localStorage` and every key in `STORAGE_KEYS`.
   - The preferences and the last space now go through it.
   - The lint rule, and the test helpers on the global seam.
   - The App test with storage blocked.
   - Documents: architecture §1–§4, and one sentence each in localisation and testing.
2. `2f96377` feat(web): give every page a document title
   - Route handles; `usePageTitle` and `DocumentTitle`, mounted in `RootLayout`.
   - `PageHeader` reads the route's title.
   - `site.documentTitle` in both catalogues; `index.html`'s `<title>`.
   - Tests: `pageTitles.unit.test.ts` and `DocumentTitle.component.test.tsx`.
   - Documents: architecture §2–§3, foundation §10, and finding 35 resolved.
3. `ccf30b0` test(web): wait for the chosen page's title
   - `topBarTitle(name)`, with all 10 uses passing a name.
   - Finding 47 resolved; finding 55 recorded.
4. `9cb6382` test(web): read a toast once it shows
   - The `findToast` helper, used in 7 test files.
   - Finding 42 resolved.

Lint and the web's typecheck passed on each of the first three commits (checked in a temporary worktree at each commit), and on the head.

## 3. What was run

**On the head, once each, one at a time:**
- `test:unit`: web 732/732, api 660/660, shared 158/158.
- `test:component`: **790/791.** The one failure is "lists the owner's eleven pages" (`Unable to find role="navigation" and name "Space dashboard"`), which is finding 55 (§6). The run took 348 s while worker B's component lane ran beside it; `main` fails this test the same way under the same conditions. **The owner chose to open the PR and let CI decide; CI passed `test:component`.**
- `NODE_ENV=production npm run build`, then `check:build`: no showcase in 37 files, no dashboard code, and no data-table or Leaflet in the site's first download.
- `lint`, `typecheck`, `check:classes` (700 files), `format:check`, and `check:links` (1931 links): clean.

**The unstable tests, before and after:**
- **Finding 42:**
  - The registration test file alone passed 50 of 50 runs, unloaded, before any change.
  - Probes repeating its pattern found the toast unmounted at opacity 0 when its text first appeared, in 20 of 20.
  - After `findByText`, the toast was invisible in 0 of 80 finds unloaded, and in 2 of 200 with 24 busy loops on 12 cores.
  - With `findToast`, it was visible in 200 of 200 under the same load.
- **Finding 47:**
  - With 12 busy loops, the original test read "Overview" in 4 of 5 runs; the fixed test passed 5 of 5.
- **Full component runs on the busy machine:** 9 in all, 5 + 2 on the branch and 2 on `main` at `068efc6`, each taking 400–570 s.
  - `main` failed 47's test in 2 of 2; the branch passed it in 7 of 7.
  - No toast test failed in any of the 9.
  - The branch's failures in those runs were all finding 55's kind, or a lost worker (§6).

**Real run** (web on 5320, API on 3320 with `masaha_dev`, local headless Chrome over CDP):
- **Titles:** every site, focus-shell and admin page shows `{page} · Masaha` / `{page} · مساحة`, the 404s included, and the top bar matches it.
  - Site pages: `/`, `/spaces`, `/about`, a 404, `/login`, `/register`, `/forgot-password`.
  - Admin pages: overview, spaces, add space, lookups, a 404.
- **A language change:** the title switches live, on the site and in the dashboard.
- **A reload** keeps the language and the theme.
- **Site data blocked** (`localStorage` throws `SecurityError`): the page renders, both toggles work, and a reload forgets them.
- **Records:** screenshots and `realrun-results.txt` are in `Downloads\webbase-shots`.
- **Afterwards:** the servers were stopped by PID (tsx, server, pino, Vite and the npm processes), and ports 3320 and 5320 are free.

**Not run:**
- `test:api`, because nothing in the API changed.
- The real run of the space branch (`/dashboard/spaces/...`): see §6.

## 4. The breaks made and the tests seen failing first

Each break was made once in the code, the test was seen failing, and the code was restored:
- `storage.unit.test.ts`:
  - reading another key;
  - JSON-wrapping a value;
  - `remove` writing `''`;
  - the guard dropped (the blocked and full-storage tests);
  - `localStorage` captured at module load.
- Each stored key renamed once in `STORAGE_KEYS`:
  - the language and the theme fail `prePaint.unit.test.ts`;
  - the last space fails `lastSpace.unit.test.ts`.
- `DocumentTitle.component.test.tsx`:
  - the shallowest title taken instead of the deepest (3 tests);
  - the effect run once (3);
  - no fallback (1).
- `App.component.test.tsx`: the guard dropped; `DocumentTitle` not mounted.
- `pageTitles.unit.test.ts`: the add-space route's title removed (the failure names `/dashboard/admin/spaces/new`).
- The lint rule: `localStorage`, `window.sessionStorage` and `globalThis.localStorage` outside the layer each fail `eslint`.
- Finding 47: with "Customers" pointed at the front desk, the drawer test fails with `Unable to find role="heading" and name "Customers"`.
- Finding 42: the old pattern was caught under load by the probe (2 of 200); `findToast`, in the same probe, never was.

## 5. Problems met, and how each was solved

- **Headless Chrome prefers dark,** so the theme toggle offered "Light theme". The script flips whichever theme is shown.
- **The Chrome extension couldn't reach the local servers**, at `localhost`, `127.0.0.1` or `[::1]`. The real run used local headless Chrome over CDP, as the memory note describes.
- **The first finding-47 comparison, at 24 busy loops,** only reproduced the lazy-shell wait (finding 55). It was stopped, along with every process it had started; the other worker's processes were left untouched. It was rerun at 12 busy loops.
- **Two sessions ended mid-run.** On each restart, I checked the logs and the leftover processes, then reran.
- **The intermediate commits mix files.** `architecture.md`, `index.html`, the App test and the findings index each carry two commits' hunks. Each commit's version was built from `HEAD` and staged through the index, so the working tree the test runs read stayed untouched. The commits were then checked in a temporary worktree, which was removed afterwards (its `node_modules` junctions were unlinked first).

## 6. What behaved unexpectedly

- **The component lane is not stable on this machine when other folders run their lanes.**
  - Of 9 full runs, only 1 passed.
  - "Lists the owner's eleven pages" missed the first wait for the lazy space shell in 7 runs, and "/login shows its page" did in 3. These are finding 28's two tests.
  - Two tests ran past 5 s.
  - One run lost a Vitest worker at start, with Windows exit code `0xC0000142`.
  - `main` fails the same way.
  - **Recorded as finding 55, open;** CI passed.
- **Finding 55 nearly had a twin.** At my first conflict check, worker B's #67 carried a finding 57 for the same failure, and its index line conflicted with mine. At the report's check, #67's head (`c309164`) holds neither the finding nor the line, so both the conflict and the duplicate are gone. If 57 comes back, the PR that merges second should drop its own finding and point to the other.
- **The dev database's demo owner no longer signs in** with `SEED_DEMO_PASSWORD` from `apps/api/.env`. The seed skips the demo data once its space exists, so a later change to that variable never reached the account. I left the data untouched, so the real run did not reach the space branch; the component lane covers those titles.
- **A command meant to mask passwords did not.** It printed the seed admin's credentials from `apps/api/.env` into this session's tool output. They were not written to any file, commit or PR, and the real-run script reads them from `.env` without printing them.

## 7. The early conflict check

`git merge-tree --write-tree` of `9cb6382` against each open PR's head, after `git fetch`:
- **#67** `feat/admin-deleted-spaces` (`c309164`): **clean.** The earlier check had a conflict in `docs/architecture/findings/README.md`, both sides appending to the Open list; see §6.
- **#66** `design/admin-rest` (`15039cb`): clean.
- **#65** `design/public` (`51685d0`): clean.
- **#64** `feat/space-own-amenities` (`2e4aa4d`): clean, the shared `routes.component.test.tsx` included.

## 8. Departures from the prompt

- **The head's local component lane was not green** (790/791). The cause is machine load, and `main` fails the same way. The owner chose to let CI decide, and CI passed.
- **The real run did not reach the space branch**, because of the demo account's password (§6).
- **The real run used local headless Chrome over CDP**, because the Chrome extension could not reach the local servers.
- **The screenshots cover:**
  - the site home: Arabic, English, and English with storage blocked;
  - sign-in, on a phone;
  - the admin's lookups, Arabic and English.

  No screen's look changed, so a full RTL/LTR × light/dark × phone/desktop set was not taken.
- **Finding 55 is new, not folded** (§6), in the prompt's range 55–56.
- **D2b (the record-name title) is written as a rule** in architecture §2, *Titles*. It reaches the top bar and the tab through `usePageTitle`, as the reply's condition asked. It is built with its first page.
- **Beyond the plan:**
  - the toast fix also covers the three `features/spaces` tests that read a toast's title (Stronger decision 2, approved);
  - `topBarTitle(name)` also fixes the race at the space-switch test (Stronger decision 1, approved).
