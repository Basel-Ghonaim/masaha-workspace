# Review — PUBLIC PR 1a (#101, `feat/directory-list`)

**Head:** `e50d92225efef87f8687c32d6aee95b5c9960a5e` (unchanged at the end of the review) · base `origin/main`
`2c4d78f9` · `gh pr checks 101`: all nine green (build, check:classes, check:links, format:check, lint,
test:api, test:component, test:unit, typecheck; CodeRabbit) · `mergeStateStatus: CLEAN`.

**Verdict: mergeable — no blocker.** Seven findings are should-fix, each small. Under the owner's rule they
go into PUBLIC PR 1b's first commit through `0_CARRIED_FROM_101.md`. The other four are nits or findings to
record.

What I saw and what I only read: I read the code, the tests, the documents and the commit messages through
commit objects only. I ran no test and no build, opened no server and viewed no screenshot. The real run,
the widths 390 / 768 / 1440, every break being red, the first download's sizes and the manifest behind
finding 27 come **from the executor's report only**. CI being green I saw myself.

---

## The five most important findings

### 1. The focus jumps to the results whenever the shown page number changes, including in the middle of a search — should-fix
- **Where:** `apps/web/src/features/directory/components/list/DirectoryResults.tsx:30` (the effect keyed on
  `page`). `page` is `answer?.meta.currentPage ?? filters.page` (`useDirectoryList.ts`).
- **Scenario (seen in the code):** a visitor on `/spaces?page=2` types «Palm» in the search. After the
  400 ms pause, `useDirectoryFilters` writes `q` with `page: 1`, which replaces the address. When the answer
  arrives, `currentPage` goes from 2 to 1, so the effect focuses the visually hidden `h2` and scrolls to it.
  - The focus leaves the search field while the visitor is still typing: the next keys are lost, and on a
    phone the keyboard closes.
  - On a weak connection the answer comes seconds later, so the jump is more likely to land mid-typing.
  - The same happens when the visitor picks an order in «الترتيب» from page 2 or later.
  - It also happens on a first load of a pasted link past the last page (`?page=5` → replaced by 2): focus
    and scroll move with no action from the visitor.
  - Test 28 covers only a click on «الصفحة 2».
- **Fix:** move the focus only for a page the visitor chose: the pages are `Link` pushes, while filter
  writes and `replacePage` are `replace: true`. So `useNavigationType() === 'PUSH'` (or `!== 'REPLACE'`)
  alongside the page change is enough. Add a test: on page 2, type a search; the field keeps the focus and
  the heading does not take it.
- **Where the fix belongs:** small → **PR 1b's first commit**. This is the most visible of the defects; the
  owner may prefer a fix round.

### 2. After a rate-limit refusal, the list goes blank with no retry once the countdown ends — should-fix
- **Where:** `useDirectoryList.ts:41` (`failureOf` returns `null` when `view.view === null`) together with
  `components/list/ResultsState.tsx:18` (`'failed'` draws `results.failure !== null && …`).
- **Scenario (seen in the code):**
  - The API's general guest limit (1,200 per window by IP, `apps/api/src/app.ts:176`) sends `Retry-After`.
    Many visitors behind one carrier IP can reach it.
  - On a 429 for the first page, `useRefusalView` shows the countdown with the retry disabled. When the count
    ends it returns `view: null` (`shared/forms/hooks/useRefusalView.ts:41-44`).
  - From then on the state stays `'failed'` (no answer) but `failure` is `null`. Under the search and the
    order the visitor sees nothing: no cards, no line, no «إعادة المحاولة», and an empty count. Only a reload
    gets out.
  - `space-links`' admin list keeps its failure block and its retry in the same case
    (`useAdminSpacesList.ts`, `failure` is always built).
- **Fix:** keep the failure with its title and retry when the view is gone. The line can be empty or
  `errors.rate_limit`, as the admin list does. Add a test: 429 with `Retry-After: 1`, advance the clock, and
  the retry is offered and asks again. This also gives the untested `blocked` path its test.
- **Where:** small → **PR 1b's first commit**.

### 3. A hand-edited budget with `min` above `max` reaches the server, and the 422 replaces the list with a failure — should-fix
- **Where:** `features/directory/services/filtersOf.ts:54-55`. Each bound is read alone, then `requestOf`
  sends both.
- **Scenario (seen in the code):** someone pastes `/spaces?min=50&max=10`.
  - `filtersOf` keeps both, so the request carries `period=DAY&priceMin=5000&priceMax=1000`.
  - `directoryQuerySchema`'s `checkPrice` refuses `priceMin > priceMax`
    (`packages/shared/src/directory/requests.ts:106`), so the answer is 422.
  - The list shows «تعذّر تحميل المساحات» with a reference.
  - This contradicts S5 ("a value the server would refuse falls back to its default and never reaches the
    request"), test 10's title, and `docs/features/directory.md:79`, which states that rule as built.
- **Fix:** in `filtersOf`, drop `max` when it is below `min`. That is the same rule as commit 6's `priceBounds`
  (`belowMin` on the maximum, which is then left out). Add `min=50&max=10` to test 10.
- **Where:** small, and PR 1b rewrites the price path anyway → **PR 1b's first commit**.

### 4. `lookups.md` says the site's Directory filters by `AreaFilter`; on this head nothing sets it — should-fix
- **Where:** `docs/features/lookups.md:18` («on the site's Directory, through its page, the area filter and a
  card's area name») and `:104` («The site's Directory filters by `lookups`' `AreaFilter` … both set by the
  page»). Commit 4's body says the same («The site's Directory filters by place»).
- **Scenario (seen in the code):** `DirectoryPage.tsx` sets only `spaceLink` and `areaName`. `DirectorySlots`
  has no `placeFilter`, and `AreaFilter` is imported by nothing but its own test.
  - The approval note's rule is "Each PR's documents say only what it built", and CLAUDE.md says "Claim only
    what is true".
  - `directory.md`'s own decision line (S7, the area name only) is correct.
- **Fix:** say that `AreaFilter` is offered for the Directory's place filter, and that the page sets only
  `AreaName` for now. PR 1b's wiring commit then restores the two lines as they stand.
- **Where:** two lines → **PR 1b's first commit**. The commit body is history: no action unless a fix round
  folds commit 4 anyway.

### 5. Arriving on the site's shell from the focus shell (after signing in) leaves the focus nowhere — should-fix, plausible in the browser
- **Where:** `pages/site/shell/useMainFocus.ts:12`. `placed = useRef(pathname)` is per mount.
- **Scenario:**
  - **Seen in the code:**
    - `SiteLayout` and `FocusLayout` are sibling lazy layouts (`pages/site/routes.tsx`).
    - Signing in navigates to `/spaces` or the landing path (`authPages.component.test.tsx`), which mounts a
      fresh `SiteLayout`. Its ref starts at the new path, so the hook treats a client-side navigation as the
      first load and does not move the focus.
    - The submit button that held the focus is gone.
  - **Not observed:** that the focus then falls to `body`. This is how browsers behave, but I did not run it.
  - S8's own reason ("a client-side navigation that leaves the focus on a removed link") applies here. The
    same is true for the focus shell, which has no focus move of its own and no skip link.
- **Fix:** tell a real first load from a mount reached by navigation. For example: on mount, `useNavigationType()`
  is `'POP'` on a first load or reload and `'PUSH'`/`'REPLACE'` after `navigate`. Add a test: sign in from
  the focus shell, and the site's `main` has the focus. The focus shell's own case can be added to finding 130.
- **Where:** the hook → **PR 1b's first commit**. The focus shell → **record** in finding 130.

---

## The rest

### 6. The page-past-the-last rule is a copy of `space-links`' `usePageInRange` — should-fix
- **Where:** `useDirectoryList.ts:57-67`, line for line `features/space-links/hooks/usePageInRange.ts`.
- `usePageInRange` imports only `@shared/api`'s `Page` type and React. Nothing ties it to `space-links`, and
  it is the same "second instance" S2 gave as its reason to move the other five pieces (engineering principles
  §1). A later fix to one copy (for example, finding 1's past-last focus) will not reach the other.
- **Fix:** `git mv` it to `shared/lists/hooks/usePageInRange.ts`, export it from the barrel, and have its two
  `space-links` importers and `useDirectoryList` use it. There is no behaviour change, and existing tests
  cover it.
- **Where:** small refactor → **PR 1b's first commit**.

### 7. A card's details may never reach a screen reader — should-fix, plausible
- **Where:** `components/card/SpaceCard.tsx:34`. The whole card is one `<a aria-labelledby={nameId}>`.
- **Why I am unsure:** the link's accessible name is only the space's name. VoiceOver on iOS and TalkBack
  typically read a labelled link as one element: its name only. NVDA and JAWS often replace a link's content
  with its label. So the live status «متاح»/«مغلق الآن», «موثّقة», today's hours and the area may be
  skipped. The "status by word" rule would then hold for the eye only.
  - **Not observed:** I did not try a screen reader. The plan asks for the name as the link's name, and
    test 27 asserts it.
- **Fix:** keep the name and add `aria-describedby` pointing at the area and details block. The name stays
  short and the details are read after it. Or check with TalkBack and VoiceOver in the real run.
- **Where:** small → **PR 1b's first commit**, or record if the real run shows it is read.

### 8. The count announces a wrong line while the next answer loads — nit
- **Where:** `useDirectoryList.ts` (`count`) with `DirectoryList.tsx`'s `aria-live="polite"`.
- **Scenario:** with no filter, typing a search makes `anyApplied` true at once, while the shown answer is
  still the placeholder. The live region then announces «35 مساحة مطابقة», which is false, before the real
  count.
- **Fix:** word the count only from an answer that is not a placeholder (keep the last line while
  `isPlaceholderData`).
- **Where:** **PR 1b's first commit** with finding 1, or record.

### 9. No visible sign that the next page or filter is loading — finding to record
- `busy` is `aria-busy` only, and `ListPagination` still marks the old page as current until the answer
  comes (it reads the placeholder's `currentPage`). On a weak connection, a tap on «2» changes nothing on
  screen for seconds, which invites a second tap.
- This is consistent with the admin lists and with S13 as written, so it is a design point, not a defect of
  this PR.
- **Where:** **record a finding** (owner's call: a subdued state on the cards or the pages).

### 10. Two states with no test — nit
- `refreshFailure` (a failed refetch over shown cards, `FailureAlert` above the grid) and the rate-limit
  countdown's `blocked` retry have no test. Finding 2's test covers the second.
- **Where:** **PR 1b's first commit**, with finding 2.

### 11. Words that repeat — nit, recorded only
- For an empty directory, the count line («لا توجد مساحات في قطاع غزة بعد») sits right above the
  `EmptyState` («لا توجد مساحات في الدليل بعد»).
- For no match, «لا توجد مساحات مطابقة» sits above «لا توجد مساحات تطابق ما اخترت».
- Both are §9's approved words, so this is for the owner: a count of zero could draw nothing.

---

## The executor's departures, judged
- **The split of commit 5:** clean. On this head:
  - the repository has no `near` argument, the keys have no point and no `hasNear`;
  - there is no `distanceText`, no `card.distance`, no `distance` order word and no `placeFilter` slot;
  - nothing is half-wired.
  - The one piece exported and unused is `AreaFilter`/`useAreaFilter` with `lookups.areaFilter`. That is
    commit 4 as the plan cuts it, waiting for 1b, but its documents claim it is in use (finding 4).
  - Tests 17, 31–43 and the privacy half of 14 are rightly 1b's.
- **S6 left to 1b:** correct. Plan §7/§9 put `useMediaQuery`'s export and foundation §3 in commit 6. The
  execution prompt's sentence that S6 is in 1a was the error, and the `area:design-system` label still holds
  for foundation §5.
- **The `h3` inside `CardTitle`, and the name's `lang`/`dir` on a `span` inside it:** fine. `CardTitle` is a
  `div`, the heading order is h1 → h2 (results) → h3 (cards and empty states), and an English name no longer
  floats left in an Arabic card.
- **The page-past-last rule inline:** it should have moved (finding 6).
- **`useMainFocus` comparing paths:** right for StrictMode, but it resets on each mount of the shell
  (finding 5).
- **The four existing tests changed:** not weakened. `SiteLayout` gains a query wrapper and an empty fake
  directory. Three tests change their heading `Spaces` → `Workspaces` (the plan's `h1`). `routes` only adds
  test 44 and `restoreTransport`.
- **Tests written after their code** (repository, `useDirectoryList`): the breaks the report lists would
  prove them. That they were red is from the report only.
- **Finding 27 left open:** follows the approval note's (10). The evidence (both builds keep a two-way import)
  is from the report only.
- **99 files against ≈ 63:** everything is in scope. The extra files are:
  - the importers `git grep` found (`useReadOnlyHours`, `hoursForm`);
  - `FailureAlert`, `DirectoryListView` and `DirectoryRequest`;
  - the four tests.
  There is no drive-by change. The estimate was low.

## Checked and fine
- **The refactors:**
  - `shared/lists` (four exports, `pageItems` internal) and `shared/lib`'s `spaceNameOf`, `SpaceNameView` and
    `clockOf` are byte-identical moves. `clockOf`'s test case moved unchanged.
  - Every importer reads the barrels, and nothing in `shared/` imports `@features`.
  - `space-links`' own `SpaceNameView` is left as it was (Review Focus).
- **`lookups` (S7):** `AreaName` and `useAreaName` take a required `source`.
  - `admin` still reads `useGovernoratesQuery` only, so its behaviour is unchanged for `SpaceEditPage`, the
    one caller.
  - `public` reads the catalogue only, and the test proves the admin's lists are never asked for.
  - `AreaFilter` groups areas by governorate, leaves out a governorate with no area, searches both names, and
    shows its summary, loading, and failure with a retry.
- **The URL state:**
  - every S5 key is read and written, with no default written;
  - `relevance` is dropped without `q`, and `page` is a whole number of at least 1;
  - `area` is all-or-nothing and at most 50;
  - a search of tashkeel or tatweel only stays in the field with its line, and stays off the address and the
    request;
  - filter writes replace the address and return to page 1; the pages are links (push), so Back and reload
    work, and a copied link carries everything;
  - a page past the last is replaced by the last.
  - Exception: finding 3.
- **The states:** skeletons on the first load; the failure with its reference and retry; offline worded by
  `useRefusalView`; an empty directory against no match with «مسح الفلاتر»; the cards kept with `aria-busy`
  while the next page loads (S13); the results heading focused on a page choice; a live count. Exceptions:
  findings 1, 2 and 8.
- **The card:**
  - one link to `publicSpacePath(slug)`, showing the cover or the mark, the mark also when the cover fails;
  - the status by word with its role (FULL `warning`, CLOSED `neutral` = `bg-secondary`) or «لا تتوفر حالة
    مباشرة»;
  - «موثّقة»;
  - today's hours on Gaza's calendar (`gazaClockOf().dayOfWeek`, Sunday 0 as `days` is), isolated, open
    around the clock, closed today, or nothing when hours were never saved;
  - **no price**.
- **The shell:** «تخطَّ إلى المحتوى» is the first focusable element with `href="#main"`, inside
  `<main id="main" tabIndex={-1}>`. The focus moves on a change of path, not on the first load, and not on a
  change of search or hash. `ScrollRestoration` is in `RootLayout`.
- **Design system and copy:**
  - semantic tokens and logical classes only; no colour or CSS outside the layer;
  - every string in both catalogues, Arabic `satisfies Catalogue[...]`;
  - Arabic plurals with all six forms (`count.all`, `count.matching`, `areaFilter.chosen`);
  - §9's words as approved.
- **Boundaries and the first download:**
  - `features/directory` imports only `shared` and `@masaha/shared`;
  - `lookups` is not dashboard-only, so the page may compose it;
  - `check:build` holds the entry and its static imports. The new code is reached only through the
    Directory's lazy route, and lint guards the rest.
  - The first-download sizes are from the report only.
- **The documents:** `directory.md` (web header, list, decisions, code map, history), `architecture.md`
  (§1 `lists`, §2 shell and Directory, §7 polling), foundation §5's roles, the `overview.md` and
  `docs/README.md` lines, and finding 130 with its index line are true to the code. Exceptions: findings 3
  and 4.
- **Scope:** `apps/web` and `docs` only. The five commits are atomic, each with its own docs. Subjects are
  45, 48, 47, 49 and 45 characters. Each body says why. There is no tool attribution.
