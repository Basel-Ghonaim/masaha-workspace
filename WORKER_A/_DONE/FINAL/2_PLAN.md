# FINAL — every screen of Masaha v1 complete, every open finding closed — the plan

> **Approved 2026-10-29 by the supervisor on the owner's behalf (the owner delegated it: "the rest as your
> recommendation") — binding on every executor of this plan; it wins where the plan below differs:**
> - **§13 OD1–OD12 as recommended:** 22, 112, 115 accepted (OD1 (b), OD2 (a), OD3); OD4 (b) the size guide revised;
>   OD5 (a); **OD6 (a)** — finding 91 by S1's narrow rule; **OD7 (a)** — migration M2; OD8 yes (`public.ts` entries);
>   OD9 yes (the index moved once at the end, this PR only); OD10 the six supersessions approved, each recorded where it
>   lives; OD11 (a) the reclamation job built; **OD12 — DI1–DI33 as recommended.** PA1–PA7 not taken.
> - **The migrations M1 and M2 only** (F3); any other need for a migration is SERIOUS (the execution prompt's rule).
> - **§10.5's "retried once, then CI judges" is overridden:** nothing reaches CI untested — a run killed for memory is
>   re-run, then run in parts, until every file has run green locally.
> - **§9.4's lanes are a proposal:** the execution prompt (`3_EXEC_PROMPT_LEAD.md`) decides the lanes, the
>   concurrency and the test databases; it wins over §9.4 and §10.5 where they differ.
> - Every decision logged in `C:\dev\masaha\workspace\WORKER_A\FINAL\SUPERVISOR_DECISIONS.md`.

> Worker A's plan for the project's last build mission: **one PR**, executed by a lead with sub-agents. It stands
> alone: it never sends its reader to another plan, prompt or report. The repository's own documents (named by
> path at `origin/main`) are the source of truth for what exists. Everything here is numbered so the supervisor,
> the owner and the executor can point at it: **§** sections, **D** decisions (per unit, `D5.3`), **S** stronger
> decisions, **PA** proposed alternatives, **DI** design issues, **T** tests (each with its break **B**, same
> number), **EC** executor checks, **OD** decisions for the owner, **M** migrations, **C** commits (per unit,
> `C5.3`), **U** units, **L** lanes.

## §1. Header

- **Base:** `origin/main` = **`ce671b376b96dd307345de7a6f2cd53a60b326b9`** (`ce671b37`, the merge of #131: finance,
  the two overviews, `GET`/`PATCH /me`, `GET …/visits`, finding 167's filter, the `payments` totals). Read only from
  its commit objects (`git show origin/main:…`, `git grep … origin/main`); the working tree, branch and `HEAD` of
  `C:\dev\masaha\app` were not touched.
- **What was read:** `CLAUDE.md`; the owner's decisions for this mission; the carried public-site fixes from #111 and
  the review they came from; the design decisions batches (shared, admin, account, desk, owner) and the review lens;
  at `origin/main`: `docs/design/SCREENS.md`, `README.md`, `CHANGES.md` (in part), every prototype page of the seven
  missing screens and their modules (`Owner overview.html`, `Finance.html` + `masaha/finance.jsx`, `Owner audit.html`,
  `Admin overview.html`, `Admin audit.html`, `Admin settings.html`, `Settings.html`, `masaha/owner.jsx`,
  `masaha/admin.jsx`, `masaha/account.jsx`, `masaha/shared.jsx` in part); `foundation.md` whole; `architecture.md`
  whole; `api-contract.md` §1–§4 and the sections *Me*, *Managed spaces*, *Subscriptions*, *Front desk*, *Finance*,
  *Audit log*, *Overview*, *Internal*, *Spaces (the admin)*, *Platform settings*, §6; `v1-mvp.md` whole;
  `overview.md` whole; `docs/README.md` whole; the findings index and **every one of the 67 open findings' files**;
  `features/audit.md`, `features/overview.md`; the web's shells, navigation, routes, copy registration and the code
  each finding names; the API code each finding names (sessions, staff, owners, jobs, storage, env, the
  `subscription_usage` migration, the schema's `User`, `Subscription`, `SpaceManager`). **The 24 built screens were
  checked against their prototypes by five read-only sub-agents** (screens 1–8; 13 and 16; 10, 11, 14, 15, 17, 18;
  20–24; 26–30), each reading the prototype and the code at `origin/main`; their gaps are copied into §4 and planned
  in §5. Radix's menu was read in the installed `node_modules/@radix-ui/react-menu` (finding 105): a `disabled` item
  is skipped by the arrow keys (`focusable: !disabled`) and by typeahead.
- **What could not be proven by reading** (→ executor checks, §14): the build's chunk graph after a new code-splitting
  group (EC5), Docker Compose's version for inline `configs` (EC6), Cloudinary's resource listing (EC8), the
  rendering at 390 / 768 / 1440 and in dark of every changed screen (the real run, §11), the exact field names some
  audit entries store (EC12), whether the installed Radix equals the lockfile's (EC4), and the rest listed in §14.
- **Size (estimates):** 11 units, 8 lanes plus the lead, **121 commits**, **≈ 420 files** (≈ 160 added, ≈ 250
  modified, ≈ 10 deleted), **2 migrations** (M1, M2), **1 new error code**, **3 new routes**, **3 new timed jobs**
  and **≈ 16 changed requests or answers** on the API.
- **Finding numbers:** this plan records none of its own. **200–219 are reserved for the executor** (a defect found
  while building that this PR does not fix), **220–239 for the reviewers.**
- **Screens at the base** (foundation §13's 32): **1 complete (18), 25 partial, 6 missing (9, 12, 19, 25, 31, 32)**;
  and the owner's audit (O13), missing, which this plan builds inside screen 31's line (DI1). **Gaps on the built
  screens and the shells: 108** (§4.1: 102 screen gaps, GX.1 included, and 6 shell gaps), besides the open findings
  that touch them.
- **Findings at the base:** 67 open. **Built: 55** (98 among them: a document change either way, OD4) · **accepted:
  6** (84, 187, 193 by the owner; 22, 112, 115 recommended, OD1–OD3) · **to the deployment item: 6** (23, 33, 46, 64,
  65, 152).
- **Decisions needed from the owner:** OD1–OD12 · **design issues:** DI1–DI33 · **executor checks:** EC1–EC26 ·
  **proposed alternatives:** PA1–PA7 · **tests:** 267 (numbered T1–T298 by unit, each with its break B).

---

## §2. The owner's decisions — binding (verbatim)

*Copied word for word from the owner's decisions for this mission (2026-10-29).*

### The mission

- **Close everything:** after it, **every one of the 32 screens is complete, with no gap**, and every open finding
  below is closed — built, or accepted by the owner.
- **The screens missing or partial on `main` (2026-10-29):** 9 (the name and language — `GET`/`PATCH /me`, built by
  B's BACKEND_FINAL); 12 (the owner's overview); 19 (finance); the owner's audit (O13, `Owner audit.html`, finding
  14); 25 (the admin's overview); 31 (the admin's audit log); 32 (the platform settings). Gaps on built screens that
  B's new routes close: finding 161's visits of a day, finding 167's filter on screen 28. Plus every gap the planner
  finds by checking each screen against its prototype and `foundation.md` §13.
- **The home-page review is cancelled;** a full review of the whole project follows this mission.

### The framework

- **F1 — scope (a):** every open finding is in, **except** (1) those B's BACKEND_FINAL closes — 97, 153, 161, 167,
  170 — and (2) those only deployment or a measurement there can close — **23** (a per-address ceiling), **33, 46,
  64** (the deployment's headers), **65** (the reset wait measured), **152** (the audit's retention) — which go to the
  deployment item. `0_CARRIED_FROM_111.md` (the public site's small fixes) is in.
- **F2 — one PR may change `apps/web`, `apps/api`, `packages/shared` and `docs` together.** The web/API split between
  the workers is lifted for this mission (the owner: the project's end; speed matters).
- **F3 — migrations (a):** allowed when the approved plan names each; its SQL read at the review; no PR number in
  SQL.
- **F4 — one PR (a)**, the reviews split by lanes.
- **Planner:** Opus 5.5 at **xhigh** effort. **It starts once worker B's BACKEND_FINAL PR has merged.**
- **Execution:** as #129 and B's lead run — a lead with sub-agents (the lead decides how many), a test database per
  API lane, heavy runs scheduled on the memory, the complete verification and the real run before the PR, no stop.

### The findings that needed the owner

**Built** (each as its finding's *Resolves when* says):
- **14** — the owner's audit screen (design O13), with its place in the owner's navigation.
- **21** — a refresh token replayed within the grace returns the same successor, derived deterministically (an HMAC of
  the presented token under a server key).
- **32** — the Google sign-in's answer says the account was created (`created` beside `linked`); a first Google
  sign-in is welcomed as registration is.
- **83** — `ALREADY_OWNER`'s 409 names the account (a contract change).
- **89** — the person search reads a larger page or an exact email filter; a failed read is worded as such.
- **92** — deactivating a reception link ends that person's sessions only when no other active link remains.
- **99** — the owner's checklist names the retired amenities the space holds, marked, until a save leaves them out.
- **160** — a visit's check-in may take its customer (`customerId`), and the desk sends it.
- **162** — the statement names who recorded and who voided each payment.
- **163** — the subscription's corrections get a place: its card in the customer's file, on the routes as they are
  (the planner designs it in the layer; its DIs go to the owner).
- **164** — a read lists a space's written-off visits (reason, who, when) and a screen offers their undo there.
- **165** — the dashboard's navigation grouped by task (`SPACE_NAV`, `ADMIN_NAV` with groups; labels hidden on the
  rail).
- **166** — the ledger's staff filter names the space's other owners.
- **168** — a guest's held action survives a password recovery in a short-lived, same-origin store the session
  confirms, never in the address.
- **171 (a)** — the desk sends the published price it showed (`published.amountAgorot`); the server compares and
  answers 409 when it differs (a new error code, both catalogues).
- **91 (a)** — creating an account with the address of a pending account whose temporary password expired replaces
  that pending account.

**Accepted (closed without code; each finding moved to *Accepted* with the owner's line):**
- **84** — v1 needs no linking of an existing account to a second front desk (close to in-app claiming, *Not in v1*).
- **187** — no undo after «إزالة» of a space that left the directory (the owner's DI-58 (a), 2026-10-28).

**Added 2026-10-29, after #131 merged (`main` = `ce671b37`, the API of v1 complete):**
- **193 — accepted:** finance's «غير محصّلة» stays the desk's list (equal to what the overview's tile links to); the
  documents already say owed and uncollected are never added. Moved to *Accepted* with the owner's line.
- **158** (the admin's spaces list's second schema for "editable", left by #131 for screen 25) — **in**: screen 25's
  «عرض الكل» uses it, and the planner closes it as its *Resolves when* says.
- **97, 153, 161, 167, 170** are resolved on `main` (#131).

**The run (the owner, 2026-10-29):** the plan is written by **a planning session of worker A's own (in
`C:\dev\masaha\app`, read-only, from `origin/main`'s commit objects)**; worker A executes in **a second, clean session
in the same folder** that waits for the execution prompt. The supervisor reviews the plan, **settles every open point on the owner's behalf** (the safest recommendation,
each logged in `WORKER_A\FINAL\SUPERVISOR_DECISIONS.md`), writes the approval note and the execution prompt, then
creates `WORKER_A\FINAL\READY`; worker A's waiting script starts the run on it. #125 closed (2026-10-29).

**Every other open finding** (≈ 40: tests, performance, accessibility, documents, tooling) — **built** as its own
*Resolves when* says; where a finding offers "or the owner accepts", the planner recommends one and lists it for the
owner's approval note.

### The public site's carried fixes (from #111's review, decided by the owner 2026-10-24) — copied in full

The owner's decision (2026-10-24): #111 merged; its review found no blocker. Every fix waits for the owner's
in-person review of the whole public site and goes into **one fix PR** — **this PR** (the home-page review is
cancelled, above). **These are its first commits in their lane, each code fix red first, then green.** The review's
file, line and scenario for each item are copied under it (*Context*). Review items 9 and 13 are findings 137 and
138 (in, §7); 11b (`lookups.md`'s scope) and 11c (`architecture.md`'s date) **merged with #113** (verified at
`origin/main`: `lookups.md`'s *Scope* names Home; `architecture.md` §2's status-states bullet carries
"(2026-10-24, #111)") and are not repeated.

**Decided by the owner (2026-10-24), as the supervisor recommended:**

1. **A link to a section focuses that section** (review 1; changes S8's rule "not when only the hash changes",
   approved): arriving at `/about#owners` or `/about#contact` — from another page or from About itself — moves
   the focus to the named section's heading (`tabIndex={-1}`), not to `main`; no hash → `main` as today. A routes
   test for each case; break: the old rule → red.
   *Context:* `apps/web/src/pages/site/shell/useMainFocus.ts:17-21` focuses `#main` on every path change, then
   `ScrollRestoration` scrolls to the hash; a screen reader starts at «عن مساحة», the next Tab goes to the intro's
   «تصفّح المساحات» at the top; pressed on About itself (only the hash changes) the focus stays in the footer.
2. **«تواصل معنا» once** (review 2): the freshness note's last sentence becomes the link itself: «إن وجدت معلومة
   خاطئة، تواصل معنا.» with «تواصل معنا» linking `#contact` (design issue 41), the rest of the note word for word.
   *Context:* `site.about.source.note` (both catalogues) ends «… إن وجدت معلومة خاطئة، تواصل معنا.», and
   `AboutPage.tsx:50-55` adds a link with the same words (`words.contact.title`): «… تواصل معنا. تواصل معنا» /
   "…contact us. Contact us". Split the note: `note` without its last sentence, then `wrong` «إن وجدت معلومة خاطئة،» +
   the link «تواصل معنا» + «.»; English "If you find wrong information, " + "contact us" + ".".
3. **Home's owners' card** (review 3): «تواصل معنا لإضافة مساحتك، وإدارة ساعاتها وأسعارها، وتظهر حالتها المباشرة
   تلقائيًا من تسجيل الحضور.» / "Contact us to add your space and manage its hours and prices; its live status
   shows automatically from the check-ins."
   *Context:* `site.home.owners.text` (both catalogues).
4. **Home's title waits for its answer** (review 4): keep the previous title while the list shows placeholder
   data (or show skeletons when available ↔ nearest changes); a test.
   *Context:* `useHomeSpaces.ts` sets `title` from `nearest` (≈ line 64) while `useDirectoryQuery` keeps the previous
   key's answer (`keepPreviousData`): keep the previous title while `query.isPlaceholderData`.
5. **A second retry while offline is announced** (review 5): the status line re-announces on each press; test
   80 presses twice.
   *Context:* `shared/routing/states/RetryState.tsx` (`retry` ≈ 38-41; the `role="status"` line ≈ 61-63) sets
   `stillOffline` to `true`, which it already is: clear the line, then set it again on the next frame (or key it by a
   press count).
6. **The phone's single tile names «عرض كل الصور (n)»** (review 6): its accessible name or description carries
   the pill when `more` is set; a test.
   *Context:* `Gallery.tsx:32` gives each tile `aria-label={tile.view.label}` («عرض الصورة 1»), replacing the pill
   (45-49) and the alt; on the first tile, when `more` is set, use `more.label` as its name or point
   `aria-describedby` at the pill.
7. **The page's live badge through `statusViewOf`** (review 7): one mapping of status → word and tone.
   *Context:* `useSpacePage.ts` (≈ 96-124, the `live` badge) maps `AVAILABLE`/`FULL`/`CLOSED` by hand: use
   `statusViewOf(liveQuery.data.status, copy)`.
8. **Three tests** (review 8): the footer's room given back on leaving a space page; «اختر منطقتك» scrolls to and
   focuses the areas' heading; «حدّد موقعي على الخريطة» starts the pick and opens `/spaces?view=map`.
   *Context:* (a) `footerRoom.ts:15-20`'s cleanup has no test: a space with a bar, then «الرئيسية» → no `pb-24`;
   (b) and (c) one Home test each.
9. **Documents** (review 11a, 11d, 11e): `directory.md`'s *Authority* names Home's spaces and counts and About's
   legend; `overview.md`'s Directory line leaves the contact to `platform-settings`; `SiteFooter.tsx`'s JSDoc
   within 100 characters.
10. **`maxLength` from the shared constant** (review 12): `HomeSearch` and `DirectorySearch` read
    `SPACE_NAME_MAX_LENGTH` from `@masaha/shared/spaces`.
11. **The two slow site tests** (review 10, plausible): record them under finding 87 (the cold lazy import inside
    a 3 s `findBy`), with the fix it names; no change to the timeout. **Add (from #116, 2026-10-25):**
    `App.component.test.tsx` › "renders the main landmark" and `router.component.test.tsx` › "shows the
    root's general error…" missed 3 s the same way locally (the site's lazy shell), passed alone and in CI.
    **And (from #117):** `routes.component.test.tsx` › "lists reception's four pages".
    **And the owner's own find (2026-10-25):** changing a page of the Directory makes the screen jump twice —
    `ScrollRestoration` resets to the top on the pushed address, then `DirectoryResults.tsx:39`'s
    `scrollIntoView` runs before the new page arrives. **Fix:** `preventScrollReset` on `ListPagination`'s three
    links (`shared/lists/components/ListPagination.tsx` 29, 41, 54), and the results' scroll and focus moved to
    after the new page has arrived (`isPlaceholderData` false); a test that no scroll happens while the old page
    still shows.
    *Context:* the slow tests are "shows the Directory under its title" (`routes.component.test.tsx:152`) and "marks
    the current page's link" (`SiteLayout.component.test.tsx:95`), each the first in its file to open `/spaces`; the
    lazy import pulls the whole `directory` feature through Vitest's on-demand transform inside a `findBy` limited
    by `asyncUtilTimeout: 3_000`. Finding 87 closes here (D4.3), not by a record only.

**Not carried:** review 14 (the report's "21 areas" sentence) — the report only.

Every item is done in this PR; one that proves larger than this section says is decided by the executor under the
autonomy rule (§9.7), recorded, never silently dropped.

---

## §3. Scope, acceptance criteria, out of scope

### §3.1 Part one — the screens

**In:** the seven missing screens built (9, 12, 19, the owner's audit, 25, 31, 32); every gap of §4.1 closed on the
25 built screens; the shells' gaps (§4.1, *Shells*). Each screen's acceptance criterion is one line, **"complete, no
gap"**, broken into these testable lines, all of which hold for it:

- **AC-S1** each of its gaps in §4.1 closed as its decision in §5 says, with the test §10 names (or, for a pure
  layout or word change, the real-run case of §11 that shows it);
- **AC-S2** its states: loading (skeletons or `DataTable loading`), empty, a load error (destructive `Alert` with
  «إعادة المحاولة» / "Try again"), offline (P7's own state), 403 and 404 inside its shell, and the 429 warning on
  every action that can be refused one;
- **AC-S3** every word through the copy catalogue, in both languages, counted nouns through the plural forms (all
  six Arabic categories), values isolated (`<bdi>` / `dir="ltr"`); `catalogues.unit.test.ts` green;
- **AC-S4** its layout at 390, 768 and 1440 as its prototype and foundation §9 draw it, in light and dark, Arabic and
  English, seen in the real run (§11);
- **AC-S5** accessibility: one `h1` (the top bar's, in the dashboard), section titles `h2`, every control named, the
  focus visible and moved where the decision says, `axe` clean in its component tests;
- **AC-S6** the routes it reads and writes are the contract's, and the contract says them (§12).

| Screen | AC | Gaps it closes (§4.1) |
|---|---|---|
| 1 Home | AC-S1–S6 | G1.1–G1.2, carried 3, 4, 8b, 8c, 10 |
| 2 Directory | AC-S1–S6 | G2.1–G2.3, findings 132–136, carried 11 |
| 3 Space details | AC-S1–S6 | G3.1–G3.4, finding 138, carried 6, 7, 8a |
| 4 About | AC-S1–S6 | G4.1–G4.4, carried 1, 2, 9 |
| 5 Sign in | AC-S1–S6 | G5.1–G5.6, finding 32 |
| 6 Register | AC-S1–S6 | G6.1–G6.3 |
| 7 Forgot / reset (+ email) | AC-S1–S6 | G7.1–G7.4, finding 168 |
| 8 404 / error / offline | AC-S1–S6 | G8.1–G8.2, carried 5 |
| 9 Profile & settings | AC-S1–S6 | missing → built (D9.2) |
| 10 Favourites | AC-S1–S6 | G10.1–G10.3 |
| 11 My reports | AC-S1–S6 | GX.1 (the lists' range) |
| 12 Owner's overview | AC-S1–S6, **no amount anywhere (T-test)** | missing → built (D5.1) |
| 13 Front desk | AC-S1–S6 | G13.1–G13.24, findings 160, 164, 172 |
| 14 Customers | AC-S1–S6 | G14.1–G14.4, GX.1, finding 126 |
| 15 Customer details | AC-S1–S6 | G15.1–G15.7, findings 162, 163 |
| 16 New / renew subscription | AC-S1–S6 | G16.1–G16.5, finding 171 |
| 17 Payments | AC-S1–S6 | G17.1, GX.1, finding 166 |
| 18 Announcements | AC-S1–S6 | (none beyond the shells') |
| 19 Finance | AC-S1–S6, the owner's alone | missing → built (D5.3–D5.5) |
| 20 Space profile | AC-S1–S6 | G20.1–G20.2, findings 73, 99, 184 |
| 21 Prices & packages | AC-S1–S6 | G21.1–G21.3, finding 102 |
| 22 Staff | AC-S1–S6 | G22.1–G22.3, findings 92, 104, 105, 106 |
| 23 Data reports (owner) | AC-S1–S6 | G23.1–G23.2 |
| 24 Settings (owner) | AC-S1–S6 | G24.1–G24.3, finding 106 |
| Owner's audit (O13) | AC-S1–S6, the owner's alone | missing → built (D6.1) |
| 25 Admin's overview | AC-S1–S6 | missing → built (D5.2), finding 158 |
| 26 Spaces | AC-S1–S6 | G26.1–G26.8, findings 73, 74, 158 |
| 27 Space owners | AC-S1–S6 | G27.1–G27.5, findings 83, 89 |
| 28 Data reports (all) | AC-S1–S6 | G28.1–G28.4 (167's filter) |
| 29 Users | AC-S1–S6 | G29.1, findings 94, 104, 105 |
| 30 Lookups | AC-S1–S6 | G30.1–G30.4 |
| 31 Admin's audit log | AC-S1–S6 | missing → built (D6.2) |
| 32 Platform settings | AC-S1–S6 | missing → built (D6.3) |
| Shells (all) | AC-S1–S6 | GSH.1–GSH.6, findings 130, 165 |

### §3.2 Part two — the findings

**In:** every open finding but F1's deployment six. **AC-F** for each: *closed* — **built** (its *Resolves when*
met, a test that its removal turns red where code changed, its file's status line `Resolved` with a *Resolution*
line, §7) or **accepted** (status `Accepted` with the owner's line); the findings index lists it under its new group.
At the end the index's *Open* group holds **exactly 23, 33, 46, 64, 65, 152**.

### §3.3 Part three — the documents

**AC-D** at the end: every step of `docs/plans/v1-mvp.md`'s build map reads **Built** (screens included); every
screen of foundation §13 is built; `overview.md`'s *Built* names each screen's capability; the contract names every
route and answer this PR adds or changes; each capability document changed by a unit says what it built
(*Behaviour*, *Decisions*, *Code map*, *History*); no document claims what is not built.

### §3.4 Out of scope

- F1's six findings (23, 33, 46, 64, 65, 152) and anything only the deployment can do (headers, a measurement online).
- *Not in v1*: online payment, QR check-in, in-app claiming (84 accepted), booking, reviews; no new export route
  (finance's CSV is built in the browser).
- The full review of the whole project that follows this mission (the owner) — not this PR's.
- A new design for a screen: every screen follows its prototype and the decisions; a point neither settles is a DI
  (§6), decided by the supervisor before the run.
- The archive's screenshots (`docs/design/screens/`) are not regenerated (the README's rule: once, at the end of the
  fix phase — the owner's, outside this PR); the **prototype** is corrected where a finding asks it (74) or a decision
  of this plan changes what it draws (D10.3).

---

## §4. The reading done

### §4.1 The screens: state and gaps

States at `origin/main`: **built** = no gap found; **partial** = built with gaps; **missing** = no screen (a
placeholder or no route). Each gap: its id, what, where, and the unit that closes it. "(p)" = verified by the
sub-agent in both the prototype and the code; "(me)" = found by the planner. Gaps an open finding already records
are listed under that finding (§4.2) and named here only by number.

| # | Screen | State | Gaps | Unit |
|---|---|---|---|---|
| 1 | Home | partial | **G1.1** (p) on a phone the site header shows the theme and puts the language in the menu; SH-005: the language in the header at every width, the theme in the menu (`SiteHeader.tsx:44-45`, `SiteMenu.tsx`; every site page) · **G1.2** (p) no avatar in the phone header (P4): `AccountMenu` is `hidden md:inline-flex` (`SiteHeader.tsx:51`) · carried 3, 4, 8b, 8c, 10 | U0 (G1.1, G1.2), U9 |
| 2 | Directory | partial | **G2.1** (p) the map view has no result count (`DirectoryView.tsx:57-61`) · **G2.2** (p) on a phone the map view stacks the search and «الفلاتر» (U6: one row) (`DirectoryView.tsx:45`) · **G2.3** (p) the chosen space on the map has no distance «على بعد … كم» (`SpaceSummary.tsx`) · 132, 133, 134, 135, 136, carried 11 | U9, U3 (carried 11) |
| 3 | Space details | partial | **G3.1** (p) the status panel vanishes with no hours and no near point (`SpaceDetails.tsx:89,121,137`, `panelShown = today ‖ distance`) · **G3.2** (p) today's line ignores a running closure: «مغلقة مؤقتًا اليوم» (`useSpacePage.ts:169`) · **G3.3** (p) the location map never shows the visitor's point (`LocationSection.tsx:14`) · **G3.4** (p) «الاتجاهات» sits under the address, not as the section's header action · 138, carried 6, 7, 8a | U9 |
| 4 | About | partial | **G4.1** (p) the contact comes from `VITE_CONTACT_*`, not `GET /settings/public` (`platformContact.ts:31-35`): a contact the admin saves never reaches the site · **G4.2** (p) «تصفّح المساحات» is outline and `self-start`; the design: primary, full width on a phone · **G4.3** (p) the verified card has no `CircleCheckIcon` in its title · **G4.4** (p) the contact section's sentence differs from the design (DI14) · carried 1, 2, 9 | U6 (G4.1), U9 |
| 5 | Sign in | partial | **G5.1** (p) the description does not speak to owners and reception (C4) · **G5.2** (p) the way out ignores `next`: always «تصفّح المساحات بدون حساب» → `/spaces` (AC-017/019) · **G5.3** (p) `next` is lost to the forgot page and back · **G5.4** (p) no «أهلًا بعودتك» toast after an email sign-in · **G5.5** (p) the Google "linked" toast closes after 10 s; C5: it stays until closed · **G5.6** the focus shell has no skip link (130) · 32 | U9, U0 (G5.6) |
| 6 | Register | partial | **G6.1** (p) the card has no way out (C4) · **G6.2** (p) the owner note links `#contact`; the design: «تواصل معنا» → `/about#owners` · **G6.3** (p) the fourth password rule «طويلة جدًا — اختصرها», shown only when broken (AC-020), is missing (also the reset form) | U9 |
| 7 | Forgot / reset (+ email) | partial | **G7.1** (p) «استخدم بريدًا آخر» shows only once the resends are spent (C3) · **G7.2** (p) the reset card has no «العودة إلى تسجيل الدخول» (C4) · **G7.3** (p) «لا يمكنك الوصول إلى بريدك؟ تواصل معنا» leads to `/about#contact`, not to WhatsApp (foundation §13 #7) · **G7.4** (p) the reset email has no copyable link (AC-021) · 168 | U9, U1 (G7.4) |
| 8 | 404 / error / offline | partial | **G8.1** (p) the general error's «إعادة المحاولة» only reloads and never says «ما زال الخطأ قائمًا. حاول بعد قليل.» (PU-024) · **G8.2** (p) the bare 403 (a non-admin at `/dashboard/admin`) has no way on and reads «هذه الصفحة غير متاحة لحسابك.»; the design adds «إن كنت تظن أن هذا خطأ، تواصل معنا.» and «الرئيسية» · carried 5 | U9 |
| 9 | Profile & settings | **missing** | no route `/me`; the account navigation and menu have no «إعدادات حسابي»; the forced change is built | U9 (+ U0 route, U1 `MyAccount`) |
| 10 | Favourites | partial | **G10.1** (p) the count, «الأقرب إليّ» and the location line show while loading, after a failure and with nothing saved (`FavoritesView.tsx:61-78`) · **G10.2** (p) the empty state has no card and an outline «تصفّح المساحات» (the design: a `Card`, the default variant) · **G10.3** (p) «اختر منطقتك» lands on the Directory with its filters closed | U9 |
| 11 | My reports | partial | **GX.1** the «عرض 1–20 من N» summary (cross-screen, below) | U3 |
| 12 | Owner's overview | **missing** | a `PlaceholderPage` | U5 |
| 13 | Front desk | partial | **G13.1** (p) no «السجل» (K8): «الآن \| السجل» tabs, a day, the log's rows (`GET …/visits` + `GET …/check-ins?from&to`) — finding 161's screen · **G13.2** (p) the phone's order reads search → present → uncollected; K1: search → uncollected → present (`DeskPage.tsx:232-239`) · **G13.3** (p) the empty «غير محصّل» card always shows, and says it twice · **G13.4** (p) a usage-based subscriber's check-out is one tap; the design's dialog shows the due so far (DI10) · **G13.5** (p) names are not links to «ملف الزبون» (present rows, the search's present rows, uncollected rows with a customer, the search cards) · **G13.6** (p) the kind badge: a subscriber's «اشتراك» neutral (the design: the subscription's name, `primary`); a student visit cannot read «زيارة · طالب» (no `audience` on a visit's `PresentPerson`) · **G13.7** (p) no «تجديد» / «اشتراك جديد» from the desk's card and pre-check-in choice · **G13.8** (p) the search card has no progress lines («هذا الأسبوع 3 من 3») and no «غير حاضر» (`CustomerRow.current` has no progress) · **G13.9** (p) the visit dialog's "full" reads the status, not the count, and its alert lacks «27/40» (`DeskPage.tsx:80`) · **G13.10** (p) «طالب» is a `Checkbox` (the design: `Switch`); «الوردية» a `Select` (the design: deselectable `ToggleGroup` chips) · **G13.11** (p) the check-out's calculation line names no rate and no amount, and has no day-price-only line · **G13.12** (p) no live «يُضاف إلى ملف {name}» when a typed phone is a known customer's · **G13.13** (p) a 429 in a money dialog does not say nothing was recorded · **G13.14** (p) the phone fields have no «+970 59 000 0000» placeholder · **G13.15** (p) icons missing: «تسجيل زيارة», «خروج», «حضور»; the empty states' `UsersIcon`/`SearchXIcon`; the status control's chevron from 768 · **G13.16** (p) the search field is not large (the layer's `Input` has no `size`) · **G13.17** (p) words: the «منذ» cell repeats «منذ»; the «إجراءات» header visible; «ساعتان» → «ساعتين»; «ملاحظة» without «اختياري» in «استلام دفعة» and «تحصيل» · **G13.18** (p) the check-out dialog has no description; the money block stacks from 768 · **G13.19** (p) offline is the destructive load failure, not P7's offline state · **G13.24** (p) `visits.md`'s *Authority* still says "no web screen" · 160, 164, 172, 130, 132 | U7 |
| 14 | Customers | partial | **G14.1** (p) the type filter has no «شهري» / «أسبوعي» (foundation §13 #14), and a week or month sold from a published price filters as «مخصّص» · **G14.2** (p) a row's «⋯» lacks the state's actions: «حضور»/«خروج», «استلام {المبلغ}», «تجديد» (DK-013) · **G14.3** (p) "no customers yet" has no icon and no «زبون جديد» · **G14.4** (p) «زبون جديد» sits in the top bar, not in the row above the list beside the count (P1 amended) · GX.1 · 126 | U8, U2 (G14.1) |
| 15 | Customer details | partial | **G15.1** (p) the header holds only «⋯»: no «حضور»/«خروج», «استلام {المبلغ}», state-gated «تجديد» · **G15.2** (p) «تذكير على واتساب» and «يفتح واتساب برسالة جاهزة، وترسلها أنت.» are absent; reception cannot read the template · **G15.3** (p) the owner has no «لن يُحصَّل…» on the file's unpaid visits · **G15.4** (p) the unpaid-visits card lacks «تُحسب في رصيده.» · **G15.5** (p) «هذا الزبون يأتي بزيارات فقط.» shows even with unpaid visits, without its icon (K4) · **G15.6** (p) «حاضر الآن» (success) instead of «حاضر منذ {time}» (info) · **G15.7** (p) «تجديد» on every latest subscription; DK-013: only while ending soon or expired · 162, 163, 164 | U8, U2 (G15.2) |
| 16 | New / renew subscription | partial | **G16.1** (p) native date inputs, not the layer's `DatePicker` · **G16.2** (p) the custom end note ignores a set total (DK-008) · **G16.3** (p) the earlier debt is not a warning `Alert`, the money block's `calc` is empty and its due «المستحق», not «المجموع» with its parts · **G16.4** (p) a usage-based custom has no «يُحسب من الحضور: …» line and no rate prefilled «من السعر المنشور» · **G16.5** (p) «باقات المساحة — لا تظهر للزوار» → «خاصة بالمكتب — لا تظهر للزوار», a «خاصة» badge per row · 171 | U7 |
| 17 | Payments | partial | **G17.1** (p) the empty states lack their icons (the ledger's `CircleCheckIcon`/`SearchXIcon`, «دفعاتي اليوم»'s `CircleCheckIcon`) · GX.1 · 166 | U8 |
| 18 | Announcements | **built** | — (the shells' gaps only) | — |
| 19 | Finance | **missing** | a `PlaceholderPage` | U5 |
| 20 | Space profile | partial | **G20.1** (p) no open-report notice above its section (O12/A8) · **G20.2** (p) a section's header action («نسخ إلى كل الأيام») stays beside the title on a phone; the design leads the content with it (`SectionCard.tsx:41-46`, the shared editor) · 73, 99, 184 | U6 |
| 21 | Prices & packages | partial | **G21.1** (p) the desk's words dropped while the desk was not built (packages design issue 4): five lines (D5.9) · **G21.2** (p) a row's price under the terms in `body-sm`; the design: `label` weight in the end group (`PackageRow.tsx:23`) · **G21.3** (p) no report notice above «الأسعار المعلنة» · 102 | U5 (G21.1–2), U6 (G21.3) |
| 22 | Staff | partial | **G22.1** (p) no «مقبوضاته هذا الشهر» column / card line, each linking to the ledger · **G22.2** (p) no «عرض مقبوضاته» menu item · **G22.3** (p) no «أُضيف في» (`StaffMember` has no date) · 92, 104, 105, 106 | U5, U1 (G22.3) |
| 23 | Data reports (owner) | partial | **G23.1** (p) «تعديل الحقل» does not carry the report (`?report=<id>#report`) and the list cannot open one from `?open=<id>` · **G23.2** (p) the sidebar's «بلاغات البيانات» has no count of new reports | U6, U0 (G23.2) |
| 24 | Settings (owner) | partial | **G24.1** (p) the «حسابي» card is missing (dropped while `/me` was not built) · **G24.2** (p) the auto check-out's helper does not say where unpaid visits go · **G24.3** (p) the reminder's description does not say where it opens · 106 | U5 |
| O13 | Owner's audit | **missing** | no route, no item in the navigation (finding 14) | U6 (+ U0 route and item) |
| 25 | Admin's overview | **missing** | a `PlaceholderPage` | U5 |
| 26 | Spaces | partial | **G26.1** (p) a verified row's menu says «تعديل»; the design «عرض (يعدّلها المالك)» · **G26.2** (p) the hide/show toast has no «تراجع» (P9) · **G26.3** (p) the delete dialog's dismiss says «إلغاء» / "Cancel"; P9: «رجوع» · **G26.4** (p) the phone's filter sheet lacks the primary «عرض N نتيجة»; its clear is outline and never disabled (P5) · **G26.5** (p) the missing badge says «غير مُدخلة:» beside the chip «قديمة أو ناقصة» → «ناقصة: …» · **G26.7** (p) the editor shows no report notice · **G26.8** (p) a verified space's notice has no «بلاغات {space}» link and no «لتصحيح معلومة:» · 73, 74, 158 (G26.6) | U6 |
| 27 | Space owners | partial | **G27.1** (p) the «إجراءات» header is visible (also the users list) · **G27.2** (p) the empty state has no «إضافة مالك» · **G27.3** (p) `ACCOUNT_SUSPENDED` in the add sheet has no way out («استرجعه أولًا» → the users page) · **G27.4** (p) «مالك جديد بلا حساب؟» lands without opening the add sheet (`?sheet=add`) · 83 (G27.5), 89 | U6 |
| 28 | Data reports (all) | partial | **G28.1** (p) the sheet's title does not name the space («{space} · {field}») · **G28.2** (p) no `?open=<reportId>` · **G28.3** (p) no sidebar badge of the reports awaiting the admin · **G28.4** (me) **finding 167's filter is not offered** («يعالجه»: the owner's mission names it; supersedes data-reports' DI-39) | U6, U0 (G28.3) |
| 29 | Users | partial | **G29.1** (p) «انضم» drops the year when it is this year · G27.1 · 94, 104, 105 | U6 |
| 30 | Lookups | partial | **G30.1** (p) the edit sheets still hold the active switch (AD-025) · **G30.2** (p) no «الترتيب» position field past ten rows (AD-026) · **G30.3** (p) the arrows' names lack «… — {i} من {n}» and no live region announces a move · **G30.4** (p) the amenities tab shows the governorates' hint | U6 |
| 31 | Admin's audit log | **missing** | a `PlaceholderPage` | U6 |
| 32 | Platform settings | **missing** | a `PlaceholderPage`, named «الإعدادات» in the sidebar (AD-029: «إعدادات المنصة») | U6 (+ U0 name) |

**Cross-screen (GX):** **GX.1** (p) the lists' footer «عرض 1–20 من N» is absent (customers, the ledger, «دفعاتي
اليوم», «بلاغاتي»), and a one-page list drops its page steps; P6: a short list keeps its steps, `aria-disabled`
(`paginationView.ts` returns `null` when `total ≤ 1`; screen 18 keeps DI-26's exception) — U3 (the rule) and each
list's lane (passing the summary).

**Shells (GSH, me):** **GSH.1** the dashboard's navigation is one flat list (165) · **GSH.2** no skip link and no
focus on a page change in the dashboard's shells and the focus shell (130) · **GSH.3** on a phone the dashboard's top
bar holds the theme and the avatar; DI-10: the account heads the drawer, SH-005: the theme and the language in the
drawer's foot (`TopBar.tsx`, `DashboardLayout.tsx`) · **GSH.4** the account menu (P4): no role beside the name, no
«إعدادات حسابي», and in the dashboard «لوحة التحكم» where P4 says «الموقع العام» (`AccountMenuContent.tsx`) ·
**GSH.5** the admin's settings item reads «الإعدادات»; AD-029: «إعدادات المنصة» in the sidebar and the page ·
**GSH.6** the owner's audit has no place in the navigation (14) — all U0.

**Count:** of foundation §13's 32 — 6 missing, 25 partial, 1 built (18); the owner's audit (O13) missing besides.
**Gaps: 108** — 102 on the screens (GX.1 included) and 6 on the shells; the carried items and the open findings that
touch a screen are counted under §2 and §4.2, not again here.

### §4.2 The open findings: state at the base

Each: its fix's kind (W web, A API, S shared, D documents, T tests, B build/tooling, M migration), its size, its
unit, and its outcome. "→ OD" = its *Resolves when* offers the owner's acceptance; the recommendation is in §13.

| # | Title (short) | Fix | Size | Unit | Outcome |
|---|---|---|---|---|---|
| 14 | owner's audit has no design | W (O13 built), D | M | U6 | built |
| 17 | expired counters and sessions never swept | A (a timed job) | S | U1 | built |
| 21 | a token replayed in the grace branches | A | S | U1 | built (owner) |
| 22 | the reset email's words outside the catalogue | D | S | U1 | → OD1: accepted (rec.) |
| 23 | no per-address ceiling | — | — | — | deployment (F1) |
| 27 | two dashboard chunks import each other | B | M | U4 | built |
| 32 | Google's answer says nothing of a creation | A, S, W | S | U1, U9 | built (owner) |
| 33 | headers for Google | — | — | — | deployment (F1) |
| 46 | headers for the tiles | — | — | — | deployment (F1) |
| 48 | `db:up` recreates the container | B, D | S | U4 | built |
| 55 | a lazy shell's first wait on a busy machine | T | S | U4 | built |
| 63 | a photo's files can outlive it | A (a timed job), storage port | M | U2 | built |
| 64 | headers for Cloudinary | — | — | — | deployment (F1) |
| 65 | the reset wait measured | — | — | — | deployment (F1) |
| 69 | the owners endpoint's code for a deleted space | D, T | S | U1 | built |
| 73 | the gallery's per-tile progress | W (layer `Meter`) | S | U3, U6 | built |
| 74 | the design's gallery copy | prototype | S | U6 | built |
| 77 | the race helper and Vitest's timeout | T | S | U1 | built |
| 78 | the owners' names test | T | S | U1 | built |
| 79 | the names reader's optional transaction | A | S | U1 | built |
| 82 | the users feature keeps operations flat | W (moves) | S | U9 | built (rec. over accepting) |
| 83 | `ALREADY_OWNER` names no account | A, S, W, D | M | U0, U1, U6 | built (owner) |
| 84 | two front desks for one person | D | — | U10 | accepted (owner) |
| 87 | the owner's shell cold-loads space-links | T | S | U4 | built |
| 89 | «تحقّق من البريد» for three causes | A, S, W | S | U1, U6 | built (owner) |
| 91 | an expired pending account locks its address | A, D | M | U1 | built (owner), S1 |
| 92 | an owner ends another owner's sessions | A, D | S | U1 | built (owner) |
| 93 | three staff refusals untested | T | S | U1 | built |
| 94 | the person search calls a receptionist a user | W | S | U6 | built |
| 95 | a link words the space from the editor's read | W | S | U6 | built (rec.) |
| 98 | the capability documents outgrow their guide | D | S | U4 | → OD4 |
| 99 | the owner's checklist and a retired amenity | A, S, W | S | U2, U6 | built (owner) |
| 102 | the package summary announced per keystroke | W | S | U5 | built |
| 103 | Arabic-Indic digits read by five helpers | W | S | U3 | built |
| 104 | the staff menu's triggers copy the admin's | W | S | U3, U5, U6 | built |
| 105 | a held menu item unreachable by keyboard | W (layer) | S | U3, U5, U6 | built (Radix verified: it skips them) |
| 106 | two owner lines miss a case / label in name | A, W | S | U1, U5 | built |
| 112 | a key that closed a visit unpaid | — | — | — | → OD2: accepted (rec.) |
| 115 | a write-off and its undo carry no key | D | — | U10 | → OD3: accepted (rec.; the condition holds) |
| 120 | two zone databases | T | S | U2 | built |
| 121 | the auto check-out can stall | A | S | U2 | built |
| 122 | `subscription_usage` overflows | M | S | U2 | built (M1) |
| 126 | a whole phone one way only | A | S | U2 | built (rec. over accepting) |
| 127 | the dated check-ins filter on an expression | A | S | U2 | built |
| 130 | no skip link in the dashboard's shells | W | S | U0 | built |
| 132 | no sign of the next page loading | W (shared/lists) | S | U3 | built (DI4) |
| 133 | the place filter has no cap | W | S | U9 | built |
| 134 | the map rebuilds every marker | W | S | U9 | built (+ measured, §11) |
| 135 | dark marks disagree with the legend | W (layer css) | S | U9 | built (OD5) |
| 136 | near me's wait counts the prompt | W | S | U9 | built (rec. over accepting) |
| 137 | Home's counts past 1,000 spaces | W | S | U9 | built |
| 138 | a failed refresh still reads live | W | S | U9 | built (rec. over accepting) |
| 152 | audit retention | — | — | — | deployment (F1) |
| 158 | the spaces list and `editable` | S, W | S | U6 | built (owner) |
| 160 | a visit's check-in cannot name its customer | A, S, W | M | U2, U7 | built (owner) |
| 162 | no route names a space's staff to reception | A, S, W | S | U2, U8 | built (owner) |
| 163 | a subscription's corrections have no screen | W | M | U8 | built (owner), DI11–DI13 |
| 164 | a written-off visit is listed nowhere | A, S, W | M | U2, U7 | built (owner) |
| 165 | the navigation is not grouped | W | S | U0 | built (owner) |
| 166 | the staff filter cannot name the other owners | W | S | U8 | built (owner; no API: EC10) |
| 168 | a guest's intent and a password recovery | W | M | U9 | built (owner) |
| 171 | a published price changed silently | A, S, W | S | U0, U2, U7 | built (owner) |
| 172 | the write-off's reason not focused first | W | S | U7 | built |
| 180 | a site page's chunk reaches the libraries | B, W | M | U4 | built (rec. over accepting) |
| 184 | «تعديل الحقل» may not scroll | W | S | U6 | built |
| 187 | a favourite removed cannot be saved again | D | — | U10 | accepted (owner) |
| 193 | a visit left to a customer, debt and uncollected | D | — | U10 | accepted (owner) |

**Totals:** 67 open · **built 55** (98's either outcome is a document change, counted built) · **accepted 6** (84,
187, 193 by the owner; 22, 112, 115 by OD1–OD3) · **deployment 6**. **Migrations 2:** M1 (122), M2 (G14.1).

**Deferred documents** (`docs/README.md`): one trigger, "*Endpoints* in api-contract.md — each endpoint is built" —
met by every route and answer this PR adds or changes; each unit writes its own contract entries (§12).
**`v1-mvp.md`:** steps 1–12 each name a screen still planned (9; 19, 24 partly, 31, 32; 12, 25; the desk's and the
lists' steps say "the screens remain"); U10 rewrites each to *Built*. **`overview.md`:** *Built* lacks the screens of
finance, overview, audit, platform settings and the account's settings; U10 adds them.

---

## §5. Decisions as built

Each decision: what is built, then **Why** (one line) and **Undo** (one line). Words are given in both languages,
Arabic first, verbatim; a line marked *(existing)* is already in the catalogue and is reused by its key. Counted
lines give the six Arabic forms in the order zero · one · two · few · many · other.

### §5.0 U0 — the lead's foundations (first; every lane builds on them)

**D0.1 — A refusal may name the record it is about (83, contract §2).** The error envelope gains `details`:
```ts
ErrorEnvelope.error.details?: ErrorDetails          // packages/shared/src/core/envelope.ts
ErrorDetails = { userId: number }                   // today only ALREADY_OWNER carries it (D1.7)
```
The API's `AppError` takes an optional `details` (a fifth constructor argument and `AppError.conflict(code, message,
errors?, details?)`), and `errorHandler` writes it into the envelope when set. The web's `AppError`
(`shared/errors`) keeps it (`toAppError` copies `error.details`), typed `ErrorDetails | undefined`. Contract §2 shows
the field; §5 *Owners (the admin)* says which refusal carries it. Tests T1, T2.
*Why:* the client can act on the record the refusal names without a second, uncertain search. *Undo:* drop the field;
the add sheet keeps its row line.

**D0.2 — A new domain code, `PUBLISHED_PRICE_CHANGED` (171), by the `add-error-code` skill's steps:**
`packages/shared/src/core/errors.ts`'s list (after `FAVORITES_LIMIT_REACHED`), both catalogues' `errors.ts`:
- ar «تغيّر هذا السعر منذ فتحت النافذة. راجع المبلغ الجديد، ثم أكّد.»
- en "This price changed since the sheet opened. Check the new amount, then confirm."
Contract §6: "`PUBLISHED_PRICE_CHANGED` (409: a subscribe from a published price whose amount the desk showed differs
from the price now, 2026-10-29, #PRNUM)". The API's use is D2.8, the desk's D7.4. Test T3 (both catalogues name it).
*Why:* the owner's 171 (a). *Undo:* remove the code; the subscribe charges the price now, as before.

**D0.3 — The dashboard's navigation, grouped by task (165, 14, GSH.1, GSH.5, GSH.6, P3).**
- `pages/dashboard/navigation.ts`: `NavItem` gains `group?: NavGroup` (`'today' | 'money' | 'space' | 'team' |
  'spaces' | 'platform'`); an item without one heads the list. `SPACE_NAV`, in order: `overview` · **today:** `desk`,
  `customers`, `payments`, `myPayments` · **money:** `finance`, `packages` · **space:** `profile`, `announcements`,
  `dataReports` · **team:** `staff`, **`audit`** (new: segment `audit`, `OWNER` only — finding 14's place), `settings`.
  `ADMIN_NAV`: `overview` · **spaces:** `spaces`, `owners`, `dataReports` · **platform:** `users`, `lookups`,
  `audit`, **`platformSettings`** (renamed from `settings`; segment `settings` unchanged, so its address stays
  `/dashboard/admin/settings`).
- `DashboardNavigation` draws one `SidebarGroup` per run of items with the same group, its `SidebarGroupLabel` the
  group's name (`role="group"`, `aria-labelledby` the label), **only when `grouped`**: the owner's and the admin's
  shells pass `grouped`; reception's four pages are drawn ungrouped (P3). On the rail (768–1023) the labels are kept
  for assistive technology only and a `SidebarSeparator`-like border divides the groups (EC1: the layer's
  `SidebarGroupLabel` in rail form; if it shows, the layer hides it there — a layer change in this commit).
- Copy (`dashboard.ts`, both catalogues): `groups` — ar `today: 'اليوم'`, `money: 'المال'`, `space: 'المساحة'`,
  `team: 'الفريق والإعدادات'`, `spaces: 'المساحات'`, `platform: 'المنصة'`; en `'Today'`, `'Money'`, `'The space'`,
  `'Team & settings'`, `'Spaces'`, `'The platform'`. `pages.platformSettings` — ar «إعدادات المنصة», en "Platform
  settings". `NAVIGATION_ICONS.platformSettings = SettingsIcon`; the owner's `audit` takes `ScrollTextIcon` (existing).
- **Badges** (G23.2, G28.3): `NavigationItem` takes an optional `badge: { count: number; label: string }`, drawn
  through `SidebarMenuButton`'s `badge` / `badgeLabel` only when `count > 0`. The shells compute them:
  `SpaceLayout`, for an owner only, from `data-reports`' new hook `useOpenReportsCount(spaceId)` (`GET
  /manage/spaces/:spaceId/data-reports?status=OPEN&limit=1` → `meta.totalRecords`, key `['space', spaceId,
  'data-reports', 'count', 'open']`); `AdminLayout` from `useAdminReportsCount()` (`GET
  /admin/data-reports?status=OPEN&handledBy=ADMIN&limit=1`, key `['admin', 'data-reports', 'count', 'admin']`).
  Labels — ar «بلاغات جديدة» / «بلاغات بانتظار الإدارة», en "new reports" / "reports waiting for the admin". Both keys
  sit under their scope's `data-reports` prefix, so every decision's invalidation refreshes them; read on mount and on
  window focus, never polled.
- Tests T4–T8.
*Why:* the owner's 165 and P3; 14's place is O13's «الفريق والإعدادات». *Undo:* drop `group`; one flat list.

**D0.4 — A skip link and the focus on a page change in every shell (130, G5.6, carried 1).**
`SkipLink` and `useMainFocus` move from `pages/site/shell/` to `shared/routing/focus/` (exported by
`@shared/routing`; their tests move with them). Every shell renders `SkipLink` first: `SiteLayout`, `FocusLayout`
(both of its routes) and `DashboardLayout` (before the sidebar). Each shell's `main` is `id="main"` and
`tabIndex={-1}`. **The rule** (`useMainFocus`):
1. the document's **first page** keeps the focus where the browser leaves it, whichever shell shows it and however it
   arrived (a guard's `replace` on load included): a module-level flag in `shared/routing/focus/firstPage.ts`, set
   once the first page has shown;
2. after it, **every change of path** moves the focus to `main`, a browser Back or Forward included (so returning from
   the focus shell by Back focuses the site's `main`);
3. **a hash that names an element** on the page moves the focus to that element instead (carried 1), also when only
   the hash changes; the named sections carry `tabIndex={-1}` on their heading (About's `#owners`, `#contact`; the
   space editor's cards for D6.10's anchors);
4. a change of the search alone moves nothing; the scroll stays `ScrollRestoration`'s.
Words: `site.skipToContent` *(existing)* — «تخطَّ إلى المحتوى» / "Skip to content". Tests T9–T13.
*Why:* SH-018; 130's three notes; the owner's carried item 1. *Undo:* the site-only hook, as before.

**D0.5 — The account where each shell has room for it (GSH.3, GSH.4, G1.1, G1.2; DI-10, SH-005, P4).**
- **Dashboard, below 768:** the top bar holds the drawer's trigger and the page's header (title and the page's
  controls) only; the language, the theme and the account show from 768 (`hidden md:flex`). The drawer opens with the
  **account first** (`DrawerAccount`, in `pages/dashboard/shell/`): a full-width button — the avatar, «{name} · {role}»
  on one line, the email (`dir="ltr"`) under it, a `ChevronsUpDownIcon` at the end — opening the account menu without
  the theme and language items; then the switcher (space) or the wordmark (admin); the drawer's foot holds the public
  page's link (space), then the language **and the theme** toggles (`md:hidden`).
- **The account menu** (`features/users` › `AccountMenuContent`): the label «{name} · {role}» when the shell passes
  a role (`role?: string`), the email under it; then, **on the site:** «لوحة التحكم» (for those with one) *(existing)*,
  then the account's links in their navigation order (المفضّلة، بلاغاتي، **إعدادات حسابي**); **in the dashboard:**
  «الموقع العام» → `/` and «إعدادات حسابي» → `/me`, in place of «لوحة التحكم»; then sign-out *(existing)*. The shells
  pass the role word: the space shell the role at the space in the URL, the admin shell «أدمن»; the site none.
  Words (`users.ts`): `roles` — ar `OWNER: 'صاحب المساحة'`, `RECEPTION: 'موظف استقبال'`, `ADMIN: 'أدمن'`; en `'Owner'`,
  `'Reception'`, `'Admin'`; `publicSite` — «الموقع العام» / "Public site"; `account.links.settings` — «إعدادات حسابي» /
  "Account settings".
- **Site header, below 768** (G1.1, G1.2): the language toggle in the header at every width; the theme toggle in the
  header from 768 and in the phone's menu below it; a signed-in user's account trigger is the avatar alone below 768
  (named «قائمة الحساب — {name}» *(existing `users.menu`)*), the name beside it from 768. (`SiteHeader.tsx`,
  `SiteMenu.tsx`.)
- Architecture §2's two shell bullets say it. Tests T14–T18.
*Why:* DI-10, SH-005 and P4, settled; the account was out of reach on a site phone. *Undo:* the bar as it was.

**D0.6 — Every screen still to come has its route now (so no lane edits the route tables).**
- `pages/dashboard/routes.tsx`: `SPACE_PAGES` gains `overview` → `./space/overview/OverviewPage`, `finance` →
  `./space/finance/FinancePage`, `audit` → `./space/audit/AuditPage`; `ADMIN_PAGES` gains `overview` →
  `./admin/overview/OverviewPage`, `audit` → `./admin/audit/AuditPage`, `platformSettings` →
  `./admin/settings/SettingsPage`. Each file is created here as a stub that renders `PageHeader` and
  `PlaceholderPage`'s body, with a JSDoc naming the unit that fills it; the lanes replace its body only.
- `pages/site`: `SITE_PATHS.mySettings = '/me'`; a route under `AccountLayout`, `RequireAuth`, titled
  `copy.users.settings.title` («إعدادات حسابي» / "Account settings"), lazily loading
  `./account/settings/AccountSettingsPage` (a stub here, D9.2's); `ACCOUNT_LINKS` gains `{ key: 'settings', to:
  SITE_PATHS.mySettings }` after `reports`; `site.account.settings` — «إعدادات حسابي» / "Account settings".
- The copy registers three new sections, empty, for their lanes: `overview`, `finance`, `audit` (`english/<name>.ts`
  `as const`, `arabic/<name>.ts` `satisfies Catalogue['<name>']`, both `index.ts`). `pageTitles.unit.test.ts` covers
  the new routes (T19).
*Why:* the route tables, the navigation and the copy indexes are the files every lane would otherwise touch at once.
*Undo:* none needed; each stub is replaced by its lane.

### §5.1 U1 — the API: identity, accounts, staff and owners (lane A1)

**D1.1 — A replayed token within the grace returns the same successor (21).** `sessions/tokens.ts` gains
`successorOf(token, key): string` = `base64url(HMAC-SHA256(key, token))`. The key is derived once at start-up from
`JWT_SECRET` by HKDF-SHA256 (`node:crypto` `hkdfSync('sha256', JWT_SECRET, '', 'masaha refresh successor', 32)`),
handed to `createSessionsService` as a dependency (`successorKey`). `rotate`:
- **first presentation** (`rotatedAt` null): the successor is `successorOf(token)`, its row inserted as today, the
  presented one marked rotated;
- **within the grace** (rotated ≤ 30 s ago): the successor is `successorOf(token)` again; its row is found by its
  hash and **returned as it is** — no new row, the family's activity carried as today; a successor row that no longer
  exists (its family ended) answers `invalid`;
- **after the grace:** `reused`, the family ended, as today.
`security.md` › *Tokens and cookies* says it. Tests T20–T22. (S7: no new environment variable.)
*Why:* the owner's 21 — a copy replayed within the window gains nothing it can keep apart. *Undo:* `newToken()` for
every successor, as before.

**D1.2 — Expired counters and tokens are swept by a timed job (17).** Two jobs join `app.ts`'s list, after the auto
check-outs, each run every 5 minutes with them and answering its counts in `done`:
- `sessions.sweepExpired` → `{ refreshTokens, resetTokens, recoveries }`: deletes refresh tokens past `expires_at`
  or past `session_ends_at`, reset tokens past `expires_at`, recoveries past `expires_at`;
- `rateLimits.sweepExpired` → `{ counters }`: deletes the `rate_limits` rows whose window has ended.
Each deletes at most 5,000 rows a table a run, oldest id first (`DELETE … WHERE id IN (SELECT id … ORDER BY id LIMIT
5000)`), so a run stays within the function's time. Contract *Internal* lists them; `security.md` › *Rate limits* and
`data-model.md` › *Operations* say the rows are swept. Tests T23–T25. EC2 (the rate-limit table's window column).
*Why:* finding 17's first clause. *Undo:* remove the two jobs.

**D1.3 — Google's answer says it created the account (32).** `POST /auth/google` answers `Session & { linked:
boolean, created: boolean }`; `created` is `true` exactly when this sign-in created the account (a new `USER`
without a password, D1.4's replacement included). `@masaha/shared/auth` names the type (`GoogleSession`). The web's
welcome is D9.3. Contract updated. Test T26.
*Why:* the owner's 32. *Undo:* drop `created`; no welcome.

**D1.4 — An expired pending account's address is freed when its holder creates an account (91 (a), with S1).**
- **Replaceable** (S1): an account whose temporary password is pending **and expired**
  (`must_change_password AND temporary_password_expires_at <= now`), with no Google subject, holding **no active
  `OWNER` link**, that **never acted**: no audit entry with it as actor, no favourite, no data report it wrote.
- **Where:** `POST /auth/register` and `POST /auth/google` (when it would create an account), in their transaction,
  under the old account's lock, before the new account is created:
  1. each of its active reception links is deactivated, audited `space.staffDeactivated` (the link's space, no actor:
     the owner's log shows «النظام»);
  2. its sessions are ended (`revokeAll`), it is suspended, and its email becomes `replaced-{id}@replaced.invalid`
     (`.invalid` is reserved, RFC 2606);
  3. audited **`user.replaced`** (a new action: entity the old account, no space, `before: { email }`, `after: {
     replacedById }`) — on `AUDIT_ACTIONS` and on the admin's account events (`PLATFORM_ACCOUNT_ACTIONS`);
  4. the new account is created as today (register: a `USER` with its password; Google: a Google-only `USER`,
     `created: true`).
- **Otherwise unchanged:** register answers `EMAIL_TAKEN`, Google `GOOGLE_LINK_NOT_ALLOWED`; a reset sends no email
  while a temporary password is pending; the owner's staff add and the admin's owner add create for a free address
  only.
- `security.md` › *Passwords*, `users.md`, contract *register* and *google*. Tests T27–T32. EC3 (how register meets a
  taken email today).
*Why:* the owner's 91 (a), narrowed so a real account (an owner, or one recovered after use) is never taken by a
stranger who types its address (S1). *Undo:* remove the step; the admin frees an address as before.

**D1.5 — The reset email prints its link (G7.4, AC-021).** Under the button, both parts (HTML and text):
- ar «إن لم يعمل الزر، انسخ هذا الرابط:» then the link as text (`dir="ltr"`, breaking anywhere);
- en "If the button doesn't work, copy this link:" then the link.
In `apps/api/src/modules/auth/email/resetEmail.copy.ts` (its shape test covers the new line) and `resetEmail.ts`.
Test T33. **Finding 22 → OD1** (recommended: the email's words accepted as a second home in `localisation.md`).
*Why:* AC-021; mail clients that strip buttons. *Undo:* remove the line.

**D1.6 — `MyAccount` says how the account signs in (screen 9).** `GET`/`PATCH /me` answer `MyAccount & {
hasPassword: boolean, hasGoogle: boolean }` (`passwordHash` not null; `googleSubject` not null). Contract *Me*;
`@masaha/shared/users`. Test T34.
*Why:* the settings' «تسجيل الدخول» card names the methods (the design's Google row «مربوط»). *Undo:* drop both.

**D1.7 — `ALREADY_OWNER` names the owner (83).** `adminOwners.service.ts`'s `upgrade` throws it with `details: {
userId: account.id }` (D0.1). Contract *Owners (the admin)* › `POST /admin/owners`: "`conflict` (409)
`ALREADY_OWNER`, with `details.userId`, the owner's account, to link instead". Test T35.
*Why:* the owner's 83. *Undo:* drop the details.

**D1.8 — The users list finds an account by its exact email (89).** `adminUsersQuerySchema` gains `email:
emailSchema.optional()` (trimmed, lowercased, ≤ 254): `GET /admin/users?email=` keeps the one account whose stored
email equals it, alone or with the other filters. Contract *Users (the admin)*. Test T36.
*Why:* the owner's 89 — a right email always reads as found. *Undo:* drop `email`.

**D1.9 — A deactivation ends sessions only when no other link remains (92).** `staff.service.ts` › `setActive(…,
false)`: the reception link is deactivated as today; `users.endSessions(userId)` runs only when
`countOtherActiveLinks(userId, space.id) === 0`. Access to this space ends at once anyway: the space boundary reads the
links on every request. Contract *Staff (managed)* › `PATCH`; `space-links.md`. Tests T37, T38.
*Why:* the owner's 92. *Undo:* end the sessions always.

**D1.10 — An admin's account refused as an admin's on the re-issue (106).** `issueTemporaryPassword` checks
`account.role === 'ADMIN'` first → 409 `ACCOUNT_IS_ADMIN`; then `role !== 'USER' || other active links` →
`ACCOUNT_HAS_LINKS`. Contract *Staff (managed)*. Test T39 (and T41's case). The words are D5.10's.
*Why:* 106's first clause offers "the API gives the admin's its own code". *Undo:* one code.

**D1.11 — Each reception link has its date (G22.3).** `StaffMember` gains `addedAt: string` (the link's
`created_at`, ISO 8601). Contract *Staff (managed)*. Test T40.
*Why:* OW-018's «أُضيف في». *Undo:* drop the field.

**D1.12 — Three staff refusals and the expiry's second check get tests of their own (93):** T41–T44 (the re-issue's
`role !== 'USER'` half with an `OWNER`-role account holding no link here; the 404 for a deactivated reception link on
the re-issue and on the handover; `ACCOUNT_IS_ADMIN` on a re-activation; the sign-in's `confirm` refusing an expiry
that passed between the password check and the lock).
*Why:* 93's *Resolves when*. *Undo:* —.

**D1.13 — The owners endpoints' type check is named by the contract (69).** Contract *Owners (the admin)*: "a
`spaceId` that is not a positive whole JSON number answers `validation` (422) `invalid_format` on `spaceId`, before the
space is read; a soft-deleted space `invalid_choice`". Test T45 pins both answers.
*Why:* 69's second option: one answer per cause, both named. *Undo:* —.

**D1.14 — The race helper names its table, and its reach sits well under its test's limit (77).**
`apps/api/test/locks.ts`: `waitingOnLock` requires `on` (a table, matched through `pg_locks.relation`); `whileHeld`
passes it; every race test names its table (EC9: the call sites); `REACH_MS` becomes 8,000 and a `RACE_TIMEOUT_MS =
20_000` is exported for the race tests' own timeout (`it(title, fn, RACE_TIMEOUT_MS)`). Test T46.
*Why:* 77. *Undo:* —.

**D1.15 — The owners' names test finds the names' own query (78).** `space.api.test.ts` › "reads the owners' names
on the read's own connection, inside its transaction" identifies the waiting backend by its statement
(`pg_stat_activity.query` holding the names' `SELECT … FROM "users"`), not only by its pid. Test T47.
*Why:* 78. *Undo:* —.

**D1.16 — The names reader's transaction is explicit (79).** `users.namesFor(ids, tx: Tx | undefined)` and its
repository's `findNames(ids, tx: Tx | undefined)` take it as required; each caller says which it means (the admin's
spaces list passes `undefined`). Typecheck proves it (T48: a `@ts-expect-error` call without the argument).
*Why:* 79's first option. *Undo:* —.

**D1.17 — One schema of the admin's space statuses (158, its shared and API part).** `packages/shared/src/space-links/
requests.ts`: `SPACE_STATUSES` becomes `['verified', 'unverified', 'hidden', 'deleted', 'editable']`;
`adminSpacesQuerySchema` takes them; `ADMIN_SPACES_STATUSES` and `adminSpacesListQuerySchema` are removed and every
reader (the API's `listingQuery.ts`, the admin's overview) uses the one schema. The web's choice and its words are
D6.4. Contract *Spaces (the admin)* › `status` drops "the list screen does not offer it yet". Test T49.
*Why:* 158: "the two shared schemas become one". *Undo:* the second schema back.

### §5.2 U2 — the API: the desk, the money, the data reports and the spaces (lane A2)

**D2.1 — `subscription_usage` computes the due in `bigint` (122) — migration M1.** Prisma models no function, so
the migration is written by hand (§5.2.M). Its readers convert the column with `Number()` where they map it (EC11:
`subscriptions.repository.ts`, `payments.repository.ts`, the customers list; a `sum` of it was already `bigint`).
Within the price's bound (10,000,000 agorot) and any count of days or minutes, the due stays below 2⁵³, so `Number`
is exact. `data-model.md` › *Derived values* says it. Tests T50, T51.
*Why:* 122's first option; a bound on the price cannot help a per-day subscription without an end. *Undo:* a
migration restoring `integer`.

**D2.2 — PostgreSQL's Gaza dates pinned at a transition (120).** An API test (`src/db/gazaZone.api.test.ts`) finds,
with Node's zone data (`gazaClockOf`), every instant of 2026 where Gaza's offset changes, and for each instant
`t − 1 h`, `t`, `t + 1 h` asserts that `(t AT TIME ZONE 'Asia/Gaza')::date` in PostgreSQL equals Node's Gaza date.
Test T52. *Why:* 120's second option, with no hard-coded decree. *Undo:* —.

**D2.3 — The dated check-ins filter by the two Gaza midnights as instants (127).** `subscriptions.repository.ts`'s
dated list: `checked_in_at >= {Gaza midnight of from} AND checked_in_at < {Gaza midnight of to + 1 day}`, the
instants from the shared calendar (`@masaha/shared/core` gazaTime; EC12: the helper's name — finance's windows
already compute one), which the `(space_id, checked_in_at)` index serves. `GET …/visits` (#131) is checked for the same
expression and moved too if it filters by one (EC12). The existing edge tests stay green; T53 adds the plan's
`EXPLAIN` shape (an index range scan, not a sequential one, on a generated space).
*Why:* 127, decided with 120: the dates come from Node, as everywhere else. *Undo:* the expression.

**D2.4 — A run whose failures fill its batch answers 500 (121).** `visits.autoCheckOut` and
`subscriptions.autoCheckOut` answer `stalled: true` in `done` when they closed nothing and their failures equal the
batch they took; `shared/jobs` answers `server` (500) for a run with a stalled job (the others still run) and logs
`job stalled` with the job's name and count. Contract *Internal*. Tests T54, T55.
*Why:* 121's third option, stateless (a function has no memory between calls). *Undo:* 200 always.

**D2.5 — Files no photo holds are reclaimed (63).** The storage port gains `list(prefix): AsyncIterable<{ key:
string; createdAt: Date }>`: locally a walk of `apps/api/.storage/<prefix>` (each file's mtime); on Cloudinary the
Admin API's `GET /resources/image/upload?prefix={folder}/{prefix}&max_results=500&next_cursor=…` with basic
authentication (`api_key:api_secret`), each `public_id` (the folder dropped) plus `.{format}` as the key and
`created_at` its date (EC8). A new job, **`photos.reclaimOrphans`**, in `app.ts`'s list: it acts only during the
Gaza hour 03:00–03:59 (the clock's; other runs answer `{ skipped: true }`), lists `spaces/`, and removes each file
`spaces/{k}/{size}.webp` whose `{k}` no `space_photos.path` holds and that is older than one hour, at most 200 a run;
it answers `{ removed, kept }` and logs each removed key `[storage:reclaimed]`. Contract *Internal*; `conventions.md`
§12 (the port); `spaces.md` › *Photos*. Tests T56–T58.
*Why:* 63's first option; the hour keeps Cloudinary's Admin API calls to a dozen a day. *Undo:* remove the job.

**D2.6 — A whole phone finds a number stored under either code (126).** `customerSearch.ts`: a whole phone typed in
any form is matched by its **national digits without the trunk 0** (at least nine: `591234567`), against the end of
the stored phones' digits; so `+970…` and `+972…` find each other both ways. Contract *Customers (managed)* › `q`.
Tests T59, T60.
*Why:* 126's first option. *Undo:* the trunk-0 rule.

**D2.7 — A visit's check-in may name its customer (160).** `checkInVisitSchema` gains `customerId?` (a positive id).
With it, the desk service checks, in its transaction: a customer of the space (`invalid_choice` on `customerId`
otherwise), not archived (409 `CUSTOMER_ARCHIVED`), not present (409 `MEMBER_ALREADY_CHECKED_IN`: an open check-in or
an open visit is theirs); the visit is created with its `customer_id`; `visitorName` stays required (the desk sends
the customer's name). Audit `visit.checkedIn`'s `after` gains `customerId`. At its check-out the visit keeps its
customer (the existing rule: no phone asked). Contract *Front desk* › `POST …/visits`. Tests T61–T63.
*Why:* the owner's 160. *Undo:* drop the field.

**D2.8 — A published price that changed is refused (171 (a)).** The subscribe's `published` gains `amountAgorot?`
(1–10,000,000). Under the space's lock, the service compares it with the standard price it reads: different → 409
`PUBLISHED_PRICE_CHANGED`, writing nothing; absent → as today. Contract *Subscriptions (managed)*. Tests T64, T65.
*Why:* the owner's 171 (a). *Undo:* ignore the field.

**D2.9 — The statement names who recorded and who voided (162).** `ItemPayment` becomes
`VisitPayment & { recordedBy: { id: number; name: string }; voided: { at: string; by: { id: number; name: string };
reason: string } | null }` (`recordedById` kept, `voided.byId` replaced by `voided.by`), answered by
`GET …/subscriptions/:id` and the file's `unpaidVisits[].payments`; a name is the account's, a link of any state.
Contract (*Customers* and *Subscriptions*). Test T66.
*Why:* the owner's 162 (the first option: no staff route for reception). *Undo:* ids only.

**D2.10 — The space's written-off visits are listed (164).** **`GET /manage/spaces/:spaceId/written-off-visits` ·
🏢** (`visits.writeOff`; reception `forbidden` (403) before the query): a page of
```ts
WrittenOffVisit = { visit: DeskVisit, writtenOffBy: { id: number, name: string },
                    paidAgorot: number, writtenOffAgorot: number }   // the rest written off: charge − paid, voids left out
```
the latest written off first, then by id; `meta` the pagination. `@masaha/shared/visits`. Contract *Front desk*;
`visits.md`. Tests T67, T68.
*Why:* the owner's 164. *Undo:* remove the route.

**D2.11 — A subscription keeps its published period (G14.1) — migration M2.** `Subscription.publishedPeriod
PricePeriod? @map("published_period")`, set to `WEEK` or `MONTH` by a subscribe from `published`, and a `CHECK` (M2).
`SubscriptionState` gains `publishedPeriod: 'WEEK' | 'MONTH' | null`. `customersQuerySchema`'s `kind` gains `WEEK`
and `MONTH` (the current subscription's published period); `PACKAGE` unchanged; **`CUSTOM` narrows** to no package and
no published period; `NONE` unchanged. Existing rows stay `NULL` (nothing is deployed; the demo's published ones read
as custom until the seed makes new ones — the seed's demo sets the period, EC13). Contract *Customers* and
*Subscriptions*; `data-model.md`. Tests T69–T71. **OD7** offers the no-migration alternative.
*Why:* foundation §13 #14 names «شهري» and «أسبوعي»; the period is not derivable (a custom 7-day subscription looks the
same). *Undo:* M2 reverted; the filter loses two choices.

**D2.12 — The file carries the space's reminder (G15.2).** `CustomerFile` gains `reminderTemplate: string | null`
(the space's; `null`: the catalogue's default), read by the staff, so reception can send «تذكير على واتساب». Contract
*Customers (managed)*. Test T72.
*Why:* `GET …/settings` is the owner's; the reminder is a staff action on the file. *Undo:* drop the field.

**D2.13 — The desk's reads say more of who is there and of the current subscription (G13.6, G13.8).**
Occupancy's `PresentPerson` of kind `VISIT` gains `audience: 'GENERAL' | 'STUDENT'`; `CustomerRow.current` gains
`progress` (as `SubscriptionState.progress`) and `totalDays`, `daysPerWeek`, `hoursPerDay`, `totalHours` (the list
already computes `subscription_usage` for each row). Contract *Occupancy (managed)* and *Customers (managed)*.
Tests T73, T74.
*Why:* the design's «زيارة · طالب» and the card's «هذا الأسبوع 3 من 3». *Undo:* drop the fields.

**D2.14 — One report is read by its id (G20.1, G23.1, G26.7, G28.2).** **`GET
/manage/spaces/:spaceId/data-reports/:reportId` · 🏢** answers the owner's row (`SpaceReport`, the reporter
anonymous as in the list); **`GET /admin/data-reports/:reportId` · 🛡** the admin's (`AdminReport`). `not_found`
(404) for another space's report or an unknown one. Contract *Data reports*. Tests T75, T76.
*Why:* the report notice opens one report from the address; a search of the list's first page could miss it (S5).
*Undo:* remove both.

**D2.15 — The space names the retired amenities it holds (99).** `AdminSpace` (the admin's and the managed reads)
gains `retiredAmenities: { id: number; nameAr: string; nameEn: string; iconKey: string }[]` — the amenities among
`amenityIds` the platform hid, in the platform's order. Contract *Spaces (the admin)*. Test T77. The checklist is D6.13.
*Why:* the owner's 99 ("a managed read … names the retired amenities a space holds"). *Undo:* drop the field.

**§5.2.M — The migrations, their SQL in full and their procedure.** Both live under
`apps/api/prisma/migrations/`, each in its own folder made by **one** `npx prisma migrate dev --create-only --name
<name>` (run once, then `ls` the folder: a second run applies the migration to the folder's dev database; in the
lane's own worktree databases, `masaha_<lane>_dev` / `_test`), then edited; or `npx prisma migrate diff --script`
when the command is non-interactive. **No PR number in SQL** (F3).

**M1 — `<timestamp>_subscription_usage_bigint`** (122; no schema change: the folder is created empty and filled):
```sql
-- Raw SQL: Prisma models no function. The amount due in bigint, so no price within its bound overflows
-- (docs/architecture/data-model.md › Derived values). The return type changes, so the function is dropped and
-- created again; nothing else depends on it (src/db/subscriptions.api.test.ts proves the rows it answers).
DROP FUNCTION "subscription_usage"(integer, integer, date, date);

CREATE FUNCTION "subscription_usage"(p_space_id integer, p_customer_id integer, p_today date, p_week_start date)
RETURNS TABLE ("subscription_id" integer, "customer_id" integer, "usage_based" boolean,
               "days_used" integer, "days_this_week" integer, "minutes_used" integer,
               "minutes_today" integer, "due_agorot" bigint)
LANGUAGE sql STABLE AS $$
  SELECT s."id", s."customer_id", s."billing" <> 'FIXED',
         count(DISTINCT c.day)::integer,
         count(DISTINCT c.day) FILTER (WHERE c.day >= p_week_start AND c.day <= p_today)::integer,
         coalesce(sum(c.minutes), 0)::integer,
         coalesce(sum(c.minutes) FILTER (WHERE c.day = p_today), 0)::integer,
         CASE s."billing"
           WHEN 'FIXED' THEN s."price_agorot"::bigint
           WHEN 'PER_DAY' THEN count(DISTINCT c.day) * s."price_agorot"::bigint
           ELSE round(coalesce(sum(c.minutes), 0) * s."price_agorot"::bigint / 60.0)::bigint
         END
  FROM "subscriptions" s
  LEFT JOIN LATERAL (
    SELECT ("ci"."checked_in_at" AT TIME ZONE 'Asia/Gaza')::date AS day,
           CASE WHEN "ci"."checked_out_at" IS NULL THEN NULL
                ELSE floor(extract(epoch FROM "ci"."checked_out_at" - "ci"."checked_in_at") / 60)::integer
           END AS minutes
    FROM "check_ins" "ci" WHERE "ci"."subscription_id" = s."id"
  ) c ON true
  WHERE s."space_id" = p_space_id AND (p_customer_id IS NULL OR s."customer_id" = p_customer_id)
  GROUP BY s."id";
$$;
```
(EC11: `git grep subscription_usage -- apps/api/prisma` shows the function in one migration only, and no view or
function depends on it; if one does, it is dropped and created again in M1 too.)

**M2 — `<timestamp>_subscription_published_period`** (G14.1; the schema gains `publishedPeriod`; Prisma writes the
`ALTER TABLE … ADD COLUMN`, the `CHECK` is added by hand below it):
```sql
-- AlterTable
ALTER TABLE "subscriptions" ADD COLUMN "published_period" "PricePeriod";

-- A subscription sold from a published price keeps its period, so the customers list can filter the weekly and
-- the monthly ones (foundation §13 #14): only a week or a month, never with a package.
ALTER TABLE "subscriptions" ADD CONSTRAINT "subscriptions_published_period_check"
  CHECK ("published_period" IS NULL OR ("published_period" IN ('WEEK', 'MONTH') AND "package_id" IS NULL));
```
At review the SQL is read (F3). Test T71 proves the `CHECK` (a package with a period is refused by the database).

### §5.3 U3 — the layer and the web's shared modules (lane L)

**D3.1 — `Meter`, a bar for a share of a whole (display).** `components/display/Meter/`: props `value`, `max`,
`label` (its accessible name), `kind: 'meter' | 'progress'` (`role="meter"` or `"progressbar"`, with
`aria-valuemin/max/now` and an optional `valueText`), `tone: 'primary' | 'warning'`. A `muted` track 12 px high
(`h-3`), `radius-pill`, the fill `primary` or `warning`, its width set inside the layer. foundation §12 (`display`)
gains its row; the showcase a section. Tests T80, T81.
*Why:* the overview's occupancy meter (D5.1) and the gallery's per-tile progress (73) need a bar no class outside the
layer may draw; a hand-built one brings no Radix dependency (73's ruling). *Undo:* the spinner and no meter.

**D3.2 — Two charts, `BarChart` and `Heatmap` (data).** `components/data/BarChart/` and `components/data/Heatmap/`,
hand-built, no library, in the layer's main entry:
- `BarChart`: `title` (a `figcaption`, visually hidden), `series: { name: string; tone: 1 | 2 | 3 | 4 | 5 }[]` (the
  `chart-*` roles), `data: { label: string; tick?: string; values: number[] }[]` (stacked, in series order),
  `format: (n: number) => string`, `size: 'md' | 'sm'` (200 / 120 px, a component token), `periodLabel` (the hidden
  table's first header). A legend when there is more than one series; ticks under the bars (`tick`, else the label);
  bars `aria-hidden`; a visually hidden `<table>` (caption, headers, one row per datum) carries every value.
- `Heatmap`: `title`, `unit`, `columns: string[]`, `rows: { label: string; values: number[] }[]`, `fewer`, `more`
  (the legend's words), `dayLabel` (the table's first header). Five steps of `primary` over `muted`
  (opacity 0.12 · 0.3 · 0.5 · 0.72 · 1, a component token list); the legend «أقل … أكثر»; the same hidden table.
foundation §12 (`data`) gains both rows; the showcase a section each. Tests T82–T84.
*Why:* foundation §5's `chart-1…5` and finance's charts (screen 19); no chart library is worth its weight for four
charts. *Undo:* —.

**D3.3 — A held menu item stays reachable by the keyboard (105).** Radix's menu skips a `disabled` item in its arrow
keys and typeahead (`focusable: !disabled`, read in `@radix-ui/react-menu`'s source). `DropdownMenuItem` gains `held?:
boolean`: `aria-disabled="true"`, `data-held`, the disabled look (50%), its `onSelect` prevented — **not** `disabled`,
so the roving focus and typeahead reach it and its reason, which stays inside the item, is read. foundation §12's
DropdownMenu row says it. Tests T85, T86. The consumers switch in D5.11 and D6.15.
*Why:* foundation §10, "every disabled action stays reachable with its reason". *Undo:* `disabled`.

**D3.4 — `Input` takes `size="lg"` (G13.16):** a component token `control-height-lg`, 48 px (52 on touch), the value
text `body`. foundation §12's Input row. Test T87.
*Why:* the desk's search, the page's main field. *Undo:* —.

**D3.5 — A list shows its range, and a one-page list keeps its steps (GX.1, P6).** `shared/lists`:
`rangeSummary(meta, words)` → ar «عرض {from}–{to} من {total}», en "Showing {from}–{to} of {total}" (numbers isolated);
`paginationView` answers a view for any `total ≥ 1`, its Previous / Next `aria-disabled` on a single page (screen 18
keeps DI-26: it passes `onlyPastOne`). Each paged `DataTable` passes `summary` (the lists are U8's and U9's).
Tests T88, T89.
*Why:* P6. *Undo:* —.

**D3.6 — A paged list says the next page is coming (132, DI4).** `ListPagination` marks **the page asked** (read from
the address) current at once, `aria-current="page"`, while the answer for it loads; `DataTable` takes `refreshing`
(`aria-busy`, its rows or cards dimmed by the layer's `refreshing` token, 60%); a new layer wrapper
`components/feedback/Refreshing/` does the same for a list that is not a table (the Directory's and the favourites'
cards). Every paged list passes `refreshing={isPlaceholderData}`. foundation §12 rows. Tests T90, T91.
*Why:* 132, the design's quiet sign. *Undo:* `aria-busy` alone.

**D3.7 — One reader of Arabic-Indic digits (103).** `shared/lib/numbers/westernDigits.ts` `toWesternDigits(text)`
(U+0660–U+0669 and U+06F0–U+06F9 → 0–9); `wholeNumberOf`, `countOf` (packages), the clock times (spaces), `agorotOf`
and the coordinates call it, each keeping its own rule. Test T92.
*Why:* 103. *Undo:* —.

**D3.8 — One home for the row menus' triggers (104).** `shared/lists/hooks/useRowTriggers.ts` (the admin's, moved);
the users page and the staff list use it; `features/staff/hooks/menu/useMenuTriggers.ts` and
`pages/dashboard/admin/useRowTriggers.ts` are deleted. Test T93 (moved with it).
*Why:* 104. *Undo:* —.

**D3.9 — A CSV built in the browser.** `shared/lib/csv/csvOf(header, rows)` (RFC 4180: a value with `"`, `,`, CR
or LF quoted, `"` doubled; rows joined by `\r\n`; a UTF-8 BOM first, so Excel reads Arabic) and
`shared/lib/csv/downloadFile(name, text)` (a `Blob` `text/csv;charset=utf-8`, an object URL, an anchor clicked, the
URL revoked). Test T94.
*Why:* the owner's decision 5 (no export route); finance's three exports (D5.3–D5.5). *Undo:* —.

**D3.10 — A page change of a list no longer jumps (carried 11, the scroll part in `shared/lists`).**
`ListPagination`'s three links take `preventScrollReset`. (The Directory's own scroll is D9.8.) Test T95.

**D3.11 — One filler of the debt reminder, and a WhatsApp link.** `packages/shared/src/space-settings/
reminderTemplate.ts` gains `fillReminder(text, { name, amount, space })` (every placeholder, every time it appears;
pure), which the settings' preview (`reminderPreview.ts`) now calls, and finance (D5.4) and the file (D8.2) use;
`shared/lib/phone/whatsappLink(phone, text)` → `https://wa.me/{the E.164 digits without +}?text={encoded}`. The name
filled is the customer's first word (DI28), the amount the money text («45 ₪»), the space its name in the interface's
language. Tests T79, T130.
*Why:* three places fill one template; one rule. *Undo:* —.

### §5.4 U4 — the build and the tooling (lane T)

**D4.1 — What only the dashboard uses gets a chunk that never imports the dashboard's back (27).** In
`vite.config.ts`, a second code-splitting group, `dashboard-shared`, holds the modules the dashboard's chunk imports
that the site never does (TanStack Query's `useQuery` and `publicSpacePath` today), with a priority below
`dashboard`'s; `check:build` gains a rule: **no chunk the `dashboard` chunk imports statically imports the
`dashboard` chunk** (a cycle), read from the manifest, and its unit test a case with a cycle. EC5 (the group that
achieves it; the executor proves it by the manifest). Tests T96, T97.
*Why:* 27's first option, proven by the manifest. *Undo:* the group removed; the cycle rule kept as a guard.

**D4.2 — A site page's chunk reaches neither the table's nor the calendar's library (180; OD8).** `data-reports`,
`announcements` and `platform-settings` gain a second entry, **`public.ts`**, holding what the site draws
(`ReportAction`, `MyReportsList`; the space page's announcements; `PlatformContact` and its query); their `index.ts`
keeps the dashboard's parts. The site's pages import only `@features/<cap>/public`; `eslint.config.js`'s boundaries
allow that entry beside the index (as the layer's `data` and `calendar` entries). `check:build` gains: **every chunk a
site page loads, with its static imports, reaches neither `data-table` nor `calendar`** (and `leaflet` only from the
Directory, the space page and the account's favourites, which draw a map — EC14). Architecture §3 states the rule.
Tests T98, T99.
*Why:* 180's first option, as the layer's heavy entries did (45, 169). *Undo:* the one entry; the cost accepted.

**D4.3 — The lazy shells' first load is paid before the tests wait (55, 87, carried 11's tests).** A helper
`apps/web/test/warmLazy.ts` (`warm(...loaders)`, awaiting each lazy module once); each route test file calls it in a
`beforeAll` with a 60 s timeout for the shells and first pages its tests open: `pages/dashboard/routes.component.test.tsx`,
`pages/site/routes.component.test.tsx`, `SiteLayout.component.test.tsx`, `authPages.component.test.tsx`,
`App.component.test.tsx`, `router.component.test.tsx` (EC15: the files). No timeout is raised. The report records
the CI run's slowest of these files (55's measurement). Test T100 (the helper).
*Why:* 55's second option and 87's "the shell's imports leave a margin". *Undo:* remove the warm-up.

**D4.4 — The database container no longer depends on the folder that started it (48).** `docker-compose.yml`:
the init script becomes an inline config —
```yaml
configs:
  create-test-database:
    content: |
      -- The API test lane's database; test:api migrates and truncates it, never masaha_dev.
      CREATE DATABASE masaha_test;
services:
  postgres:
    # … as today, its bind mount of ./docker/postgres/… removed:
    configs:
      - source: create-test-database
        target: /docker-entrypoint-initdb.d/create-test-database.sql
```
`docker/postgres/create-test-database.sql` is deleted; `setup.md` › *Database* and *Running a second folder* say a
second folder's `db:up` now leaves the container as it is. EC6 (Compose 2.23.1 or later; the existing container is
recreated once, its volume kept). Test: the real run's `docker compose config` from two folders shows one
configuration (§11, R40).
*Why:* 48. *Undo:* the bind mount.

**D4.5 — The capability documents' size guide (98) → OD4** (recommended (b): the guide revised, text in OD4).

### §5.5 U5 — the owner's screens: the two overviews, finance, and the owner's gaps (lane W1)

**D5.1 — Screen 12, the owner's overview (OV1–OV3, O3, P1 amended: no bottom bar).**
- **Route** `/dashboard/spaces/:spaceId` (segment `''`), `OWNER` only (the guard's; reception lands on the desk,
  OV3). **Reads** `GET /manage/spaces/:spaceId/overview` (`OwnerOverview`) — nothing else.
- **Feature** `features/overview` (new, dashboard-only): `repository/overviewRepository.ts` (`owner(spaceId)`,
  `admin()`), `hooks/queryKeys.ts` (`['space', spaceId, 'overview']`, `['admin', 'overview']`),
  `hooks/owner/useOwnerOverviewQuery.ts` and `hooks/owner/useOwnerOverview.ts` (the view model),
  `components/owner/{OwnerOverview,AttentionCard,PresentCard,EndingCard}.tsx`, `services/attentionRows.ts` (pure: the
  rows from the answer, in order). Exports `OwnerOverview` and `AdminOverview`. **Not polled** (OV7): refetched on
  mount (`refetchOnMount: 'always'`) and on window focus. Every link is a prop the page passes (features know no
  routes): `OwnerOverviewLinks = { group(g), reports, desk, deskUnpriced, debts, announcements, capacity,
  presentNow, endingAll, customer(id) }`.
- **Page** `pages/dashboard/space/overview/OverviewPage.tsx`: `PageHeader` (the title «نظرة عامة» and the public
  state control `LiveStatusControl` beside it, as the desk's top bar holds it — P2), then `OwnerOverview`.
- **Layout** (`flex flex-col gap-6`): ① the attention card, full width; ② a grid `lg:grid-cols-3`: the present card
  `lg:col-span-2`, the announcements tile; ③ the ending card, full width. One column below 1024.
- **① «يحتاج انتباهك» / "Needs your attention"** — a `Card`, its title an `h2`; one row per item, in this order, each
  `flex-col` below 768 and a row from it: the title (`label`) with its badge, a caption (`caption`, muted), an
  `outline sm` link button at the end.
  1. each fact group in `groups.missing` (profile, hours, prices, amenities, contacts order): title the group's
     name (`spaces` copy *(existing)*: «المساحة»، «ساعات العمل»، «الأسعار»، «المرافق»، «التواصل» / "The space",
     "Opening hours", "Prices", "Amenities", "Contacts"), badge `warning` «لم تُضف بعد» / "Not added yet", caption
     «لم يُحفظ هذا القسم بعد، فلا يراه الزوار.» / "This section was never saved, so visitors don’t see it.", action
     «مراجعة» / "Review" → prices: Packages & prices `#prices`; the others: the space profile `#<group>`;
  2. each group in `groups.stale`: badge `warning` «قديمة» / "Out of date", caption «آخر تحديث» + the days counted:
     ar zero «اليوم» · one «قبل يوم واحد» · two «قبل يومين» · few «قبل {n} أيام» · many «قبل {n} يومًا» · other
     «قبل {n} يوم»; en one "{n} day ago" · other "{n} days ago" ("Updated " before it); action as 1;
  3. `openReports > 0`: title counted — ar zero «لا بلاغات جديدة» · one «بلاغ جديد» · two «بلاغان جديدان» · few
     «{n} بلاغات جديدة» · many «{n} بلاغًا جديدًا» · other «{n} بلاغ جديد»; en "{n} new report" / "{n} new reports";
     caption «من زوار، عن معلومات في صفحة المساحة» / "From visitors, about facts on the space page"; action «مراجعة» →
     the data reports `?status=open`;
  4. `uncollectedVisits > 0` (DI3: no «اليوم»): ar zero «لا زيارات غير محصّلة» · one «زيارة واحدة لم تُحصَّل» · two
     «زيارتان لم تُحصَّلا» · few «{n} زيارات لم تُحصَّل» · many «{n} زيارة لم تُحصَّل» · other «{n} زيارة لم
     تُحصَّل»; en "{n} visit not collected" / "{n} visits not collected"; caption «خرجت بلا دفع، أو سُجّل خروجها
     تلقائيًا» / "Left without paying, or checked out automatically"; action «فتح المكتب» / "Open the desk" → the desk
     `#uncollected`;
  5. `unpricedVisits > 0` (DI2): ar zero «لا زيارات بلا سعر» · one «زيارة واحدة بلا سعر» · two «زيارتان بلا سعر» ·
     few «{n} زيارات بلا سعر» · many «{n} زيارة بلا سعر» · other «{n} زيارة بلا سعر»; en "{n} visit with no price" /
     "{n} visits with no price"; caption «أُغلقت بلا سعر؛ حدّد سعرها من المكتب.» / "Closed with no price; set it at
     the desk."; action «فتح المكتب» → the desk `#unpriced`;
  6. `customersOwing > 0` (OV2, a count only): ar zero «لا زبائن عليهم مبالغ» · one «زبون واحد عليه مبلغ» · two
     «زبونان عليهما مبالغ» · few «{n} زبائن عليهم مبالغ» · many «{n} زبونًا عليهم مبالغ» · other «{n} زبون عليهم
     مبالغ»; en "{n} customer owes money" / "{n} customers owe money"; caption «المبالغ في المالية › الديون» / "The
     amounts are in Finance › Debts"; action «عرض» / "View" → finance `?tab=debts`;
  7. `closuresAwaitingExtension > 0` (DI6): ar zero «لا إغلاقات بانتظار التمديد» · one «إغلاق لم تُمدَّد اشتراكاته» ·
     two «إغلاقان لم تُمدَّد اشتراكاتهما» · few «{n} إغلاقات لم تُمدَّد اشتراكاتها» · many «{n} إغلاقًا لم تُمدَّد
     اشتراكاته» · other «{n} إغلاق لم تُمدَّد اشتراكاته»; en "{n} closure whose subscriptions are not extended" /
     "{n} closures whose subscriptions are not extended"; caption «مدّد اشتراكات من شملهم الإغلاق، مرة واحدة.» /
     "Extend the subscriptions it covered, once."; action «مراجعة» → the announcements page;
  8. `capacitySet === false`: «لم تُحدَّد السعة» / "Capacity is not set", caption «بدونها لا تظهر حالة مباشرة
     للزوار.» / "Without it visitors see no live status.", action «تحديد السعة» / "Set the capacity" → settings
     `#attendance`.
  No row: the card's content is one line, a `CircleCheckIcon` and «كل شيء على ما يرام» / "All is in order".
- **② «الحاضرون الآن» / "Present now"** — a `Card`: description the title's word; title `text-display`, `dir="ltr"`
  «{total} / {capacity}» (or «{total}» without a capacity); action `outline sm` «عرض الحاضرين» / "View who’s here" →
  the desk; content: the layer's `Meter` (D3.1, `kind="meter"`, label «نسبة الإشغال» / "Occupancy", tone `warning` when
  `total ≥ capacity`) when a capacity is set; the line «الآن: {members} و{visits}» / "Now: {members} and {visits}"
  (DI5), counted — members: ar zero «لا مشتركين» · one «مشترك واحد» · two «مشتركان» · few «{n} مشتركين» · many «{n}
  مشتركًا» · other «{n} مشترك», en "{n} subscriber" / "{n} subscribers"; visits: ar zero «لا زيارات» · one «زيارة
  واحدة» · two «زيارتان» · few «{n} زيارات» · many «{n} زيارة» · other «{n} زيارة», en "{n} visit" / "{n} visits";
  then a row: the state badge «يظهر للزوار: {state}» / "Visitors see: {state}" (`occupancy`'s live status words and
  tones *(existing)*; `status: null` → «بلا حالة مباشرة» / "No live status", neutral) and its line — no capacity:
  «حدّد السعة في الإعدادات لتظهر حالة مباشرة.» / "Set the capacity in Settings for a live status."; full: «وصلت إلى
  السعة، فتظهر المساحة «ممتلئ».» / "At capacity, so the space shows «Full»."; otherwise: «السعة لا تظهر للزوار، فقط
  الحالة.» / "Visitors never see capacity, only the state.".
- **The announcements tile** — a link wrapping a `StatCard` (every tile a link, OW-003): label «إعلانات نشطة» /
  "Active announcements", value `running`, helper the running types' words joined by «، » / ", " (`announcements`'
  type words *(existing)*), → the announcements page.
- **③ «اشتراكات تنتهي هذا الأسبوع» / "Subscriptions ending this week"** — a `Card`: description counted — ar zero
  «لا اشتراكات» · one «اشتراك واحد» · two «اشتراكان» · few «{n} اشتراكات» · many «{n} اشتراكًا» · other «{n} اشتراك»;
  en "{n} subscription" / "{n} subscriptions"; action `link sm` «عرض الكل» / "View all" → customers
  `?status=ENDING_SOON`; up to five rows: the customer's name, a link to their file (`label`); under it «{subscription}
  · {ends}» — ends: today «ينتهي اليوم» / "Ends today", tomorrow «ينتهي غدًا» / "Ends tomorrow", else «ينتهي» + ar
  two «بعد يومين» · few «بعد {n} أيام» · many «بعد {n} يومًا» · other «بعد {n} يوم» (zero and one never reached: today
  and tomorrow) / en "Ends in {n} days"; `endsOn: null` → the name alone; at the row's end `outline sm` «تجديد» /
  "Renew" → the customer's file (DI26). None: one line «لا اشتراكات تنتهي هذا الأسبوع.» / "No subscription ends this
  week.".
- **States:** loading — three `Skeleton` blocks in the layout's places; a failure — a destructive `Alert` «تعذّر
  تحميل النظرة العامة» / "Couldn’t load the overview" with «إعادة المحاولة» / "Try again"; offline — P7's offline
  state; 403 for reception, 404 for another space: the guard's.
- **No amount anywhere:** the answer holds none; a component test renders a full overview and asserts the page's text
  holds no `₪`, no "ILS" and no number of agorot (T110).
- Tests T110–T116.
*Why:* OV1–OV3, O3 as amended, the prototype. *Undo:* the placeholder.

**D5.2 — Screen 25, the admin's overview (OV4–OV7, A8).**
- **Route** `/dashboard/admin` (segment `''`), the admin's branch. **Reads** `GET /admin/overview`
  (`AdminOverview`).
- **Feature** `features/overview`: `hooks/admin/useAdminOverviewQuery.ts`, `useAdminOverview.ts`,
  `components/admin/{AdminOverview,PlatformTiles,CompletenessCard}.tsx`. Links passed by the page:
  `AdminOverviewLinks = { spaces, reportsOpen, stale, unverified, users, space(id), completenessAll }`.
- **Page** `pages/dashboard/admin/overview/OverviewPage.tsx`.
- **Tiles** — a `section` named «ملخص المنصة» / "Platform summary", `grid gap-4 md:grid-cols-2 lg:grid-cols-3
  xl:grid-cols-5` (DI7), each a link wrapping a `StatCard`:
  1. «المساحات» / "Spaces": value verified + unverified + hidden; helper «{v} موثّقة · {u} غير موثّقة · {h} مخفية» /
     "{v} verified · {u} unverified · {h} hidden" → the spaces list;
  2. «بلاغات مفتوحة» / "Open data reports": `reports.open`; helper «{a} بانتظار الإدارة · {o} بانتظار المالكين» /
     "{a} waiting for the admin · {o} waiting for owners" → reports `?status=open`;
  3. «بيانات قديمة أو ناقصة» / "Stale or missing data": `spaces.staleOrMissing`; helper «حسب حدود الحداثة في إعدادات
     المنصة، أو لم تُضف بعد» / "By the platform’s freshness limits, or not added yet" (DI8) → spaces `?stale=true`;
  4. «مساحات غير موثّقة بلا مالك» / "Unverified spaces, no owner": `spaces.unverifiedNoOwner`; helper «تعدّلها الإدارة
     حتى يُربط مالكها» / "The admin edits them until an owner is linked" → spaces `?status=unverified`;
  5. «مستخدمون جدد» / "New users": `newUsers`; helper «آخر 30 يومًا» / "Last 30 days" → the users list (DI7).
- **«اكتمال البيانات» / "Data completeness"** — a `Card`: description «المساحات التي تعدّلها الإدارة — غير الموثّقة،
  والمخفية منها — وينقصها شيء أو فيها بيانات قديمة. الموثّقة يحدّثها مالكوها.» / "The spaces the admin edits — the
  unverified ones, hidden ones included — that miss something or hold stale data. Verified spaces are their owners’ to
  update."; up to five rows: the space's name (the interface's language, `spaceName`, marked with its language), the
  badge «غير موثّقة» and «مخفية» when hidden (the list's badges *(existing)*); then one `warning` badge per missing
  group «{group} · لم تُضف بعد» / "{group} · not added yet" and per stale group «{group} · {days}» with the days
  counted (ar zero «اليوم» · one «يوم واحد» · two «يومان» · few «{n} أيام» · many «{n} يومًا» · other «{n} يوم»; en
  "{n} day" / "{n} days"), missing is `warning`, never `destructive` (A8); at the end `outline sm` «تعديل» / "Edit" →
  the space's editor. The footer: «عرض الكل» / "View all", with «({total})» when `total > 5` → spaces
  `?status=editable&stale=true` (158, D6.5). None: «لا مساحات ينقصها شيء.» / "No space misses anything.".
- **The privacy note** under it (`bg-muted` text block): «بيانات تشغيل المساحة خاصة بإدارتها — الزبائن والزيارات
  والاشتراكات والدفعات والمالية.» / "A space’s operating data is private to its management — customers, visits,
  subscriptions, payments and finance.".
- **States** as D5.1's (the failure «تعذّر تحميل النظرة العامة»). Not polled.
- Tests T117–T120.
*Why:* OV4–OV7, A8. *Undo:* the placeholder.

**D5.3 — Screen 19, Finance: the page and its income (the owner's decisions 2–6, OW-015).**
- **Route** `/dashboard/spaces/:spaceId/finance`, `OWNER` only. **Address** `?tab=income|debts|occupancy&month=
  YYYY-MM` (the defaults — income, the current Gaza month — never written; a month outside the 24 falls back to the
  current one). **Feature** `features/finance` (new, dashboard-only): `repository/financeRepository.ts` (four reads),
  `hooks/queryKeys.ts` (`['space', spaceId, 'finance', '<read>', …]`), one query hook per read, `useFinanceTabs`
  (the address), `services/{months,monthLabel,stayText,incomeCsv,debtsCsv,occupancyCsv}.ts` (pure),
  `components/{IncomeTab,DebtsTab,OccupancyTab,MonthField,CollectionsTable,DebtorRow}.tsx`. Exports
  `FinanceScreen` (the tabs, the month and the export, given the links) and `useMonthCollections(spaceId)` (D5.6).
- **Page** `pages/dashboard/space/finance/FinancePage.tsx`: `PageHeader` holding the export (`outline`, on a phone in
  «⋯», P1): «تصدير الدخل (CSV)» / "Export income (CSV)", «تصدير الديون (CSV)» / "Export debts (CSV)», «تصدير الإشغال
  (CSV)» / "Export occupancy (CSV)" by the tab; then `FinanceScreen`.
- **Toolbar:** `Tabs` (named «التقارير» / "Reports"): «الدخل» / "Income", «الديون» / "Debts", «الإشغال» /
  "Occupancy"; beside them, from 1024 at the end, `Field` «الشهر» / "Month" holding a `Select` (`md:w-48`) of the
  current Gaza month and the 23 before it (`FINANCE_MONTHS_BACK`), newest first, each «{month} {year}» in the
  interface's language with Western digits (`Intl.DateTimeFormat` with `numberingSystem: 'latn'`, «أكتوبر 2026» /
  "October 2026"). The month applies to every block that counts by month; the charts keep their fixed windows, named.
- **Income tab** (`GET …/finance/income?month`): first the line «الدخل = المبالغ المقبوضة فعليًا، بدون الدفعات
  الملغاة.» / "Income = amounts actually collected, excluding voided payments." (`caption`, muted); then
  - three `StatCard`s (`md:grid-cols-3`): «اليوم» / "Today" — `today.totalAgorot`, helper «حتى {time}» / "Up to
    {time}" (the Gaza time the answer was read); the month's label — `income.totalAgorot`, helper (when the month
    before has income) «{sign}{n}٪ عن {previous}» → written with Western digits «+12% عن سبتمبر 2026» / "+12% vs
    September 2026" (`n` rounded; no helper when the month before had none); «منذ البداية» / "All time" —
    `allTime.totalAgorot`, helper «منذ {since month}» / "Since {month}", or «لا دفعات بعد» / "No payments yet";
  - a `Card` «الدخل حسب الشهر» / "Income by month", description «آخر 12 شهرًا» / "Last 12 months": `BarChart`
    (`size="md"`), series «اشتراكات» / "Subscriptions" (tone 1) and «زيارات» / "Visits" (tone 2), one bar per
    `months[]` (label the short month name), `format` the money text; title «الدخل حسب الشهر، آخر 12 شهرًا» / "Income
    by month, last 12 months";
  - a `Card` «دخل الزيارات يوميًا» / "Visit income per day", description «آخر 30 يومًا» / "Last 30 days": `BarChart`
    (`size="sm"`), one series «زيارات» (tone 2), `visitsByDay`, a tick under every fifth day counted back from today
    (the day of the month), title «دخل الزيارات يوميًا، آخر 30 يومًا» / "Visit income per day, last 30 days";
  - a `Card` «التحصيل حسب الموظف» / "Collections by staff member", description the month's label: a `DataTable` (a
    card per person below 768) — «الموظف» / "Staff", «العدد» / "Count", «المجموع» / "Total" (`label`), «نقدًا» /
    "Cash", «تحويل» / "Transfer" (the payments copy's method words *(existing)*); none: «لا تحصيل في هذا الشهر.» /
    "No collections this month.".
- **Export (income):** `masaha-income-{YYYY-MM}.csv`, header «الشهر، اشتراكات، زيارات، المجموع» / "Month,
  Subscriptions, Visits, Total" (the interface's language), one row per month of `months[]` (`YYYY-MM`, the amounts in
  shekels with two decimals and a dot, no symbol), built by `csvOf` and saved by `downloadFile` (D3.9); then the toast
  «نُزّل الملف» / "File downloaded" with the file's name as its description.
- **States** (each tab): loading — `Skeleton` stat cards and chart blocks; a failure — destructive `Alert`
  «تعذّر تحميل المالية» / "Couldn’t load finance" with «إعادة المحاولة»; offline — P7's; 403 for reception (the guard).
- Tests T121–T127.
*Why:* the owner's finance decisions (cash collected, Gaza months, server aggregates, CSV in the browser, the owner's
alone). *Undo:* the placeholder.

**D5.4 — Finance › Debts (`GET …/finance/debts`, `…/payers`; 193 accepted).**
- Four `StatCard`s (`md:grid-cols-2 lg:grid-cols-4`): «مجموع الديون» / "Total owed" — `totals.owed.agorot`, helper
  the customers counted (ar zero «لا زبائن» · one «زبون واحد» · two «زبونان» · few «{n} زبائن» · many «{n} زبونًا» ·
  other «{n} زبون»; en "{n} customer" / "{n} customers"); «أرصدة للزبائن» / "Customer credit" —
  `totals.credit.agorot`, helper «{customers} دفعوا مقدمًا» / "{customers} paid in advance"; «دفعوا في {month}» /
  "Paid in {month}" — the payers' `meta.totalRecords`, counted as customers; **«زيارات غير محصّلة» / "Uncollected
  visits" (DI9)** — `totals.uncollected.visits` counted as visits (D5.1's forms), helper «{owedAgorot} · لا تُجمع مع
  الديون» / "{owedAgorot} · never added to the debts", and when `unpriced > 0` « · {n} بلا سعر» / " · {n} with no
  price"; the tile links to the desk `#uncollected`.
- A `Card` «عليهم مبالغ» / "Customers who owe", description «الأكبر أولًا» / "Largest first", `state=OWES` paged by
  20 (`ListPagination` with D3.5's range): each row — the name, a link to the file, «مؤرشف» / "Archived" (neutral
  badge) when archived; under it «منذ {date} · أقدم بند: {item}» / "Since {date} · oldest item: {item}" (`oldestItem.since`
  as a Gaza date; `oldestItem.name`, else «زيارة» / «اشتراك»); at the end the badge `warning` «عليه {amount}» / "Owes
  {amount}", then **«تذكير على واتساب» / "WhatsApp reminder"** (`ghost sm`, only with a phone; a link to `wa.me/{digits}`
  with the reminder filled — D3.11 —, `target="_blank" rel="noopener"`), then «استلام دفعة» / "Receive payment"
  (`outline sm`) → the customer's file, where «استلام {المبلغ}» is (DI15). None: `EmptyState` (`CircleCheckIcon`)
  «لا توجد ديون» / "No one owes anything".
- A grid `lg:grid-cols-2`: a `Card` «لهم رصيد» / "In credit", description «دفعوا مقدمًا أكثر مما استخدموا» / "Paid in
  advance beyond their use" — `state=CREDIT`, paged by 20: the name (link) and the `success` badge «له {amount}» / "In
  credit {amount}"; none: «لا أرصدة للزبائن.» / "No one is in credit."; and a `Card` «دفعوا في {month}» / "Paid in
  {month}" — `GET …/finance/payers?month&limit=5`: the name (link) and «{paid} · آخر دفعة {date}» / "{paid} · last
  paid {date}" (DI14); when the total is over five, the action `link sm` «عرض الكل» / "View all" → the ledger
  `?from={month's first day}&to={its last day, or today}`; none: «لم يدفع أحد في هذا الشهر.» / "No one paid this
  month.".
- **Export (debts):** reads every page of `debts?state=OWES&limit=50` in turn (the button `loading`), then
  `masaha-debts-{YYYY-MM-DD}.csv`, header «الاسم، الهاتف، المبلغ، منذ، أقدم بند، مؤرشف» / "Name, Phone, Amount,
  Since, Oldest item, Archived", one row per debtor (the phone as stored; archived «نعم» / "Yes" or empty). A failed
  page: the toast error «تعذّر تصدير الديون» / "Couldn’t export the debts" with «إعادة المحاولة»; nothing saved. (The
  phones leave the device only by the owner's own download, the owner's decision 5.)
- Tests T128–T133.

**D5.5 — Finance › Occupancy (`GET …/finance/occupancy?month`).**
- Three `StatCard`s: «متوسط مدة الجلوس» / "Average stay" — `averageStayMinutes.all` as «{h}:{mm} س» / "{h}:{mm} h"
  (the API answers whole minutes; the web writes them), helper «المشتركون {m} · الزيارات {v} · {month}» / "Members {m} · visits {v} · {month}" (each `h:mm`,
  «—» when `null`); «ساعة الذروة» / "Peak hour" — «{h}:00–{h+1}:00» (`dir="ltr"`), helper the month; «متوسط الحضور
  اليومي» / "Average daily attendance" — one decimal, helper the month. A `null` value shows «—» and the helper «لا جلسات
  مغلقة في {month}» / "No closed stays in {month}".
- A `Card` «ساعات الذروة» / "Peak hours", description «متوسط الحاضرين لكل ساعة · آخر 4 أسابيع» / "Average people
  present per hour · last 4 weeks": `Heatmap` — rows the weekdays in the week's order of the language (Arabic from
  Saturday, English from Sunday, as the calendar), a weekday whose 24 values are all zero left out; columns from the
  first to the last hour holding a value above zero in any row, labelled «08» … (DI16); title «متوسط الحاضرين حسب
  اليوم والساعة» / "Average people present by day and hour", unit «أشخاص» / "people", legend «أقل» / "Fewer», «أكثر» /
  "More"; all zero: `EmptyState` «لا جلسات مغلقة في آخر 4 أسابيع» / "No closed stays in the last 4 weeks"; the card's
  content scrolls sideways below 768 (`overflow-x-auto`).
- A `Card` «الزيارات والمشتركون يوميًا» / "Visits and members per day", description «آخر 14 يومًا» / "Last 14 days":
  `BarChart` series «مشتركون» / "Members" (tone 1) and «زيارات» / "Visits" (tone 2), `byDay`, a tick every second
  day; title «الزيارات والمشتركون يوميًا، آخر 14 يومًا» / "Visits and members per day, last 14 days".
- **Export (occupancy):** `masaha-occupancy-{YYYY-MM-DD}.csv`, header «اليوم» / "Day" then «00» … «23», one row per
  weekday (its name) with its 24 averages.
- Tests T134–T137.

**D5.6 — Screen 22, Staff: the month's collections, the date added, «عرض مقبوضاته» (G22.1–G22.3).**
Columns, in order: «الاسم» / "Name", «الحالة» / "Status", **«أُضيف في» / "Added"** (`addedAt` as a Gaza date with its
year, D1.11), **«مقبوضاته هذا الشهر» / "Collected this month"** (the person's `totalAgorot` in this month's
`collections` — `finance`'s `useMonthCollections(spaceId)`, composed by the page; none → «0 ₪»; the read failed →
«—»), and the sr-only «إجراءات»; the amount is a link to the ledger `?staff={userId}&from={month's first day}&to={today}`
(EC16: the ledger's address names). On a phone the card adds «أُضيف في {date}» and «هذا الشهر {amount}» / "This
month {amount}". The row's menu gains **«عرض مقبوضاته» / "View collections"** → the same ledger address. The page
(`StaffPage.tsx`) composes `staff`'s list with the collections through a `collectedOf(userId)` prop. Tests T138–T140.
*Why:* OW-018; staff design issue 9 deferred these to the payments step, now built (superseded, with the owner's
approval in this plan). *Undo:* the columns removed.

**D5.7 — Screen 24, Settings: the account card and two helpers (G24.1–G24.3).**
- A last card «حسابي» / "My account": «الاسم وكلمة المرور واللغة والمظهر.» / "Your name, password, language and
  theme.", its action `outline` «الإعدادات الشخصية» / "Personal settings" → `/me` (supersedes space-settings design
  issue 13).
- The auto check-out's helper: «يُسجَّل خروج من بقي عند موعد الإغلاق. الزيارات غير المدفوعة تظهر في «غير محصّل».» /
  "Whoever is still in is checked out at closing. Unpaid visits show under «Uncollected».".
- The reminder's description: «رسالة واتساب جاهزة لتذكير زبون بدينه، تُفتح من ملف الزبون ومن المالية، وترسلها أنت.»
  / "A ready WhatsApp message reminding a customer of their debt; it opens from the customer’s file and from Finance,
  and you send it.".
Test T141.

**D5.8 — Screen 21, Prices & packages: the desk's words, the row's price (G21.1, G21.2).** The five lines restored
(`packages.ts`, both catalogues):
- the page's line, at its top: «أسعار الأسبوع والشهر تُختار أيضًا في المكتب عند إنشاء اشتراك.» / "Week and month
  prices are also chosen at the desk when creating a subscription.";
- the private packages section's line: «لا تظهر للزوار · تُختار في المكتب عند إنشاء اشتراك» / "Never shown to visitors
  · chosen at the desk when creating a subscription";
- the row's switch: «متاحة في المكتب» / "Available at the desk";
- the sheet's line: «باقة خاصة — لا تظهر للزوار، وتُختار في مكتب الاستقبال.» / "Private — never shown to visitors;
  chosen at the front desk.";
- the empty state: «لا توجد باقات خاصة» / "No private packages", «أنشئ باقة مثل «10 أيام» أو «20 ساعة» لتختارها في
  المكتب.» / "Create a package like «10 days» or «20 hours» to pick at the desk.".
A row's price moves into its end group beside the switch, in `label` weight (`PackageRow.tsx`). Supersedes packages
design issue 4. Test T142.

**D5.9 — The package sheet announces what the owner does not type (102).** The summary's polite live region holds
only the terms and the price; the name is outside it (`PackageSheet.tsx`). Test T143.

**D5.10 — Two owner lines, both cases and the label in the name (106).**
- `staff.refusals.ACCOUNT_HAS_LINKS` keeps «صار لهذا الحساب مساحة أخرى؛ يستعيد كلمة مروره من فريق مساحة.» *(existing)*
  for its one cause now (D1.10); `staff.refusals.ACCOUNT_IS_ADMIN` on the re-issue: «هذا الحساب حساب أدمن؛ لا يُصدر له
  رمز مؤقت من هنا.» / "This is an admin’s account; no temporary password is issued for it here." (EC17: the key exists for
  the re-activation; the same line serves both);
- the reminder's insert buttons are named with their token: «إدراج {الاسم}», «إدراج {المبلغ}», «إدراج {المساحة}» /
  "Insert {الاسم}", "Insert {المبلغ}", "Insert {المساحة}" (`insertNamed`), so the visible token is inside the name
  (WCAG 2.5.3). Tests T144, T145.

**D5.11 — The staff menu's held item and its triggers (105, 104 — the staff side).** `StaffActionsMenu`'s
«كلمة مرور مؤقتة جديدة» uses `held` (D3.3), not `disabled`; the list's triggers come from `shared/lists`'s
`useRowTriggers` (D3.8). Test T146.

### §5.6 U6 — the admin's screens, both audit logs, the platform settings, the report notice (lane W2)

**D6.1 — The audit logs: one feature, two screens (14 / O13, 31).**
- **Feature** `features/audit` (new, dashboard-only): `repository/auditRepository.ts` (`space(spaceId, query)`,
  `platform(query)`), `hooks/queryKeys.ts` (`['space', spaceId, 'audit', query]`, `['admin', 'audit', query]`),
  `hooks/useAuditLog.ts` (the address ↔ the query, the page's view), `services/{actionWords,actionGroups,detailsOf,
  targetOf,auditQueryOf}.ts` (pure), `components/{AuditLog,AuditFilters,AuditRow,AuditCard}.tsx`. Exports `AuditLog`
  (props: `scope: 'space' | 'platform'`, `spaceId?`, `spaceName?`, and `linkOf(target)` the page passes).
- **Address:** `?q=&period=all&actor=&type=<group>&page=` (`period` absent = the last 30 days; `type` one group of
  actions, sent as `actions=` its list, ≤ 30 by construction; `actor` an id, `masaha` or `system`).
- **Layout** (both): an intro line (`body-sm`, muted) — the owner's «كل ما جرى في {space}: مَن فعل ماذا، ومتى.» /
  "Everything done at {space}: who did what, and when."; the admin's «أحداث المنصة فقط. أحداث تشغيل المساحات (الزبائن
  والدفعات) يراها مالك المساحة فقط.» / "Platform events only. Space operations events (customers and payments) are
  seen only by the space owner."; then a `DataTable` (a table at 768 too — A7; cards below 768) named «سجل التدقيق» /
  "Audit log":
  - **toolbar:** `Field` «بحث في الهدف» / "Search the target" (`role="searchbox"`, placeholder — owner «دفعة، شخص،
    إعلان…» / "A payment, a person, an announcement…"; admin «مساحة، شخص، قائمة…» / "A space, a person, a lookup…",
    1–80 characters, paused search of `shared/lists`); the filter bar (P5: inline from 768, `FilterSheet` below it with
    its active count, «عرض N نتيجة», «مسح الفلاتر»): «الفترة» / "Period" — «آخر 30 يومًا» / "Last 30 days", «كل
    الفترة» / "All time" (DI17: no third choice); «المنفّذ» / "Actor" — only when `meta.actors` holds more than one:
    «الكل» / "All", then each actor's word; «نوع الإجراء» / "Action type" — «كل الإجراءات» / "All actions", then the
    scope's groups (below); the count «الأحداث: {n}» / "Events: {n}" (`totalRecords`).
  - **columns:** «الوقت» / "Time" (the Gaza date with its year · the time, `dir="ltr"`), «المنفّذ» / "Actor», «الإجراء»
    / "Action" (a `Badge`, `neutral`; `destructive` for the acts whose confirmation is destructive, AD-028 as amended:
    the owner's `payment.voided`, `space.staffDeactivated`, `closure.subscriptionsExtended`, `space.photoRemoved`; the
    admin's `space.deleted`, `user.suspended`, `space.ownerUnlinked`), «الهدف» / "Target" (its name, a link where the
    target has a page — below; the admin's adds «في {space}» / "at {space}" under it when the entry names a space;
    the details under it until 1024), «التفاصيل» / "Details" (from 1024). The card (below 768): the badge and the
    time on one line, the target, the details, the actor.
  - **The actor's word:** a person — their name (`<bdi>`); `MASAHA` (the owner's log only) — «فريق مساحة» / "The
    Masaha team"; `SYSTEM` — «النظام» / "The system".
  - **The target:** its current name in the interface's language (a space's or a lookup's `nameAr ?? name`); with
    none, the type's word — ar payment «دفعة», announcement «إعلان», dataReport «بلاغ», platformSettings «إعدادات
    المنصة», visit «زيارة», checkIn «حضور مشترك» / en "A payment", "An announcement", "A report", "Platform
    settings", "A visit", "A subscriber's check-in"; `deleted` → «{name} (محذوفة)» / "{name} (deleted)", never a link.
    Links (the page's `linkOf`): owner — customer → the file; space → the profile; package → Packages & prices;
    announcement → the announcements page; payment → the ledger; dataReport → the reports `?open={id}`; others none;
    admin — space → its editor (a deleted one → spaces `?status=deleted`); user → users `?q={name}`;
    governorate/area → lookups; amenity → lookups `?tab=amenities`; dataReport → reports `?open={id}`;
    platformSettings → the settings page.
  - **Empty:** with filters «لا توجد أحداث تطابق الفلاتر» / "No events match the filters" (`SearchXIcon`); with none
    «لا أحداث بعد» / "No events yet". Loading, failure («تعذّر تحميل سجل التدقيق» / "Couldn’t load the audit log",
    «إعادة المحاولة»), offline: P7.
- **The action groups** (`actionGroups.ts`; DI17):
  - owner — payments «الدفعات» / "Payments": `payment.*`; visits «الزيارات» / "Visits": `visit.*`; checkIns «حضور
    المشتركين» / "Subscriber check-ins": `checkIn.*`; customers «الزبائن» / "Customers": `customer.*`; subscriptions
    «الاشتراكات» / "Subscriptions": `subscription.*`, `closure.subscriptionsExtended`; packages «الباقات» /
    "Packages": `package.*`; announcements «الإعلانات» / "Announcements": `announcement.*`; space «بيانات المساحة
    وصورها» / "The space's facts and photos": `space.created`, every `space.*Edited` / `*Confirmed` of a fact group,
    `space.photo*`, `space.hidden`, `unhidden`, `deleted`, `restored`, `ownerLinked`, `ownerUnlinked`; staff
    «الموظفون» / "Staff": `space.staff*`, `user.created`, `user.temporaryPassword*`, `user.emailChanged`; settings
    «الإعدادات والحالة» / "Settings and status": `space.settingsEdited`, `space.capacityEdited`,
    `space.statusOverridden`, `space.statusOverrideCleared`; reports «بلاغات البيانات» / "Data reports":
    `dataReport.*`;
  - admin — spaces «المساحات» / "Spaces" (the space's facts, photos, creation, hiding, deletion, restoring); owners
    «أصحاب المساحات» / "Space owners": `space.ownerLinked`, `space.ownerUnlinked`; accounts «الحسابات» / "Accounts":
    `user.*` but `profileEdited`; lookups «القوائم» / "Lookups": `governorate.*`, `area.*`, `amenity.*`; reports
    «بلاغات البيانات»: `dataReport.*`; settings «إعدادات المنصة» / "Platform settings": `platformSettings.*`.
- **The action words** (`actionWords.ts`, both catalogues' `audit.ts`; an action the web does not know shows as stored,
  `dir="ltr"`, neutral):

  | Action | ar | en |
  |---|---|---|
  | `amenity.added` · `edited` · `hidden` · `restored` | إضافة مرفق · تعديل مرفق · إخفاء مرفق · إظهار مرفق | Amenity added · edited · hidden · shown again |
  | `area.*` (the same four) | إضافة منطقة · تعديل منطقة · إخفاء منطقة · إظهار منطقة | Area added · edited · hidden · shown again |
  | `governorate.*` (the same four) | إضافة محافظة · تعديل محافظة · إخفاء محافظة · إظهار محافظة | Governorate added · edited · hidden · shown again |
  | `announcement.created` · `edited` · `ended` · `started` · `deleted` | نشر إعلان · تعديل إعلان · إنهاء إعلان · بدء إعلان · حذف إعلان | Announcement posted · edited · ended · started · deleted |
  | `checkIn.checkedIn` · `checkedOut` · `autoCheckedOut` | حضور مشترك · خروج مشترك · خروج تلقائي لمشترك | Subscriber checked in · checked out · checked out automatically |
  | `closure.subscriptionsExtended` | تمديد الاشتراكات | Subscriptions extended |
  | `customer.created` · `edited` · `archived` · `restored` | زبون جديد · تعديل زبون · أرشفة زبون · استرجاع زبون | New customer · Customer edited · archived · restored |
  | `dataReport.resolved` · `dismissed` | بلاغ تمّت مراجعته · بلاغ لم يُعتمد | Report resolved · Report not accepted |
  | `package.created` · `edited` | باقة جديدة · تعديل باقة | New package · Package edited |
  | `payment.recorded` · `voided` | تسجيل دفعة · إلغاء دفعة | Payment recorded · Payment voided |
  | `platformSettings.contactEdited` · `newSpaceDefaultsEdited` · `stalenessEdited` | تعديل تواصل المنصة · تعديل إعدادات المساحات الجديدة · تعديل حداثة البيانات | Platform contact edited · New-space defaults edited · Data freshness edited |
  | `space.created` · `hidden` · `unhidden` · `deleted` · `restored` | إضافة مساحة · إخفاء مساحة · إظهار مساحة · حذف مساحة · استرجاع مساحة | Space added · hidden · shown · deleted · restored |
  | `space.profileEdited` · `hoursEdited` · `pricesEdited` · `amenitiesEdited` · `contactsEdited` | حفظ بيانات المساحة · حفظ ساعات العمل · حفظ الأسعار · حفظ المرافق · حفظ التواصل | Space details saved · Opening hours saved · Prices saved · Amenities saved · Contacts saved |
  | the five `…Confirmed` | تأكيد بيانات المساحة · تأكيد ساعات العمل · تأكيد الأسعار · تأكيد المرافق · تأكيد التواصل | Space details confirmed · Opening hours confirmed · Prices confirmed · Amenities confirmed · Contacts confirmed |
  | `space.photoAdded` · `photoRemoved` · `photosReordered` | إضافة صورة · حذف صورة · ترتيب الصور | Photo added · Photo deleted · Photos reordered |
  | `space.ownerLinked` · `ownerUnlinked` | ربط مالك · فك ربط مالك | Owner linked · Owner unlinked |
  | `space.staffAdded` · `staffDeactivated` · `staffReactivated` | إضافة موظف · إيقاف وصول · إعادة وصول | Staff member added · Access removed · Access given back |
  | `space.settingsEdited` · `capacityEdited` · `statusOverridden` · `statusOverrideCleared` | تغيير الإعدادات · تعديل السعة · ضبط الحالة يدويًا · العودة للحالة التلقائية | Settings changed · Capacity edited · Status set by hand · Back to the automatic status |
  | `subscription.created` · `corrected` · `priceCorrected` · `ended` | اشتراك جديد · تصحيح اشتراك · تصحيح سعر اشتراك · إنهاء اشتراك | New subscription · Subscription corrected · Subscription price corrected · Subscription ended |
  | `user.created` · `roleChanged` · `suspended` · `unsuspended` · `emailChanged` · `profileEdited` · `replaced` | حساب جديد · تغيير دور · إيقاف حساب · استرجاع حساب · تصحيح بريد · تعديل الحساب · استبدال حساب منتهٍ | Account created · Role changed · Account suspended · Account restored · Email corrected · Account edited · Expired account replaced |
  | `user.temporaryPasswordIssued` · `temporaryPasswordHandedOver` | كلمة مرور مؤقتة · تسليم كلمة مرور مؤقتة | Temporary password issued · Temporary password handed over |
  | `visit.checkedIn` · `checkedOut` · `autoCheckedOut` · `priced` · `leftToCustomer` · `writtenOff` · `writeOffUndone` | تسجيل زيارة · خروج زيارة · خروج تلقائي · تسعير زيارة · تسجيل دين · لن يُحصَّل · تراجع عن «لن يُحصَّل» | Visit checked in · Visit checked out · Automatic check-out · Visit priced · Left to a customer · Written off · Write-off undone |

- **The details** (`detailsOf.ts`, DI18): a line only where the stored values say something a person needs, else none —
  `payment.recorded`: «{amount} · {method}»; `payment.voided`: «{amount} · {method} · السبب: {reason}» / "… · reason:
  {reason}"; `visit.checkedOut` / `visit.autoCheckedOut`: «{charge}» when charged; `visit.writtenOff`: «{balance} ·
  {reason}»; `visit.priced`: «{charge} · {reason}»; `subscription.priceCorrected`: «من {before} إلى {after} ·
  {reason}» / "from {before} to {after} · {reason}"; `subscription.ended`: «انتهى في {date}» / "Ended on {date}";
  `closure.subscriptionsExtended`: the subscriptions counted and the days («{n} اشتراكات · {d} أيام», the D5.1 forms);
  `user.roleChanged`: «من {before} إلى {after}» (the role words of D0.5, «مستخدم» / "User" for `USER`);
  `space.statusOverridden`: «{state} · حتى {time}» / "{state} · until {time}"; `space.capacityEdited`: «{before} ←
  {after}» written as «من {before} إلى {after}»; `dataReport.dismissed`: «{note}». EC12: each stored field name is
  read from its writer and pinned by the formatter's unit test.
- **Pages:** `pages/dashboard/space/audit/AuditPage.tsx` (the owner's: `scope="space"`, the space's name from the
  switcher's read) and `pages/dashboard/admin/audit/AuditPage.tsx` (`scope="platform"`). Tests T150–T158.
*Why:* finding 14 (O13: «سجل التدقيق» in «الفريق والإعدادات», the admin's page scoped to the space) and screen 31
(AD-028); the contract's two periods only (the owner's decision 9). *Undo:* the placeholders.

**D6.2 — Screen 32, the platform settings (AD-029).**
- **Route** `/dashboard/admin/settings`, titled «إعدادات المنصة» (D0.3). **Feature** `platform-settings`: its admin
  cards in `index.ts` (dashboard); the public contact in `public.ts` (D4.2): `repository/platformSettingsRepository.ts`
  (the three `GET`/`PUT` pairs and the public read), `hooks/admin/{useContactCard,useStalenessCard,useDefaultsCard}.ts`
  (each `useServerForm` over its shared schema), `components/admin/{ContactCard,StalenessCard,DefaultsCard,
  SettingsCardShell}.tsx`. Keys `['admin', 'platform-settings', '<card>']`; a contact save also invalidates the public
  contact's key.
- **Page** `pages/dashboard/admin/settings/SettingsPage.tsx`: one column `max-w-3xl`, the three cards in this order:
  1. **«التواصل مع المنصة» / "Platform contact"**, «يظهر في «عن مساحة» و«تواصل معنا».» / "Shown in «About Masaha» and
     «Contact us».": «البريد الإلكتروني» / "Email" (`type="email"`, `dir="ltr"`), «واتساب» / "WhatsApp" (`type="tel"`,
     `dir="ltr"`, placeholder «+970 59 000 0000»); a field left empty sends `null` (helper «اتركه فارغًا ليختفي من
     الموقع.» / "Leave it empty to hide it from the site."); errors `invalid_format` — «أدخل بريدًا صحيحًا» / "Enter a
     valid email"; «رقم غير صالح، مثل +970 59 000 0000» / "Not a valid number, e.g. +970 59 000 0000";
  2. **«حداثة البيانات» / "Data freshness"**, «بعدها يرى الزوار «قد يكون تغيّر» أو يُخفى السعر في المساحات غير
     الموثّقة.» / "After this visitors see «may have changed», or the price is hidden on unverified spaces.": two fields
     side by side from 768 — «الأسعار (أيام)» / "Prices (days)" (`priceStalenessDays`), «باقي البيانات (أيام)» / "Other
     data (days)" (`stalenessDays`), `inputMode="numeric"`, `dir="ltr"`, Arabic-Indic digits read (D3.7); errors:
     `required` «أدخل عدد الأيام» / "Enter the number of days", `out_of_range` «من 1 إلى 365 يومًا» / "From 1 to 365
     days", `invalid_format` «عدد أيام صحيح» / "A whole number of days";
  3. **«الإعدادات الافتراضية للمساحات الجديدة» / "Defaults for new spaces"**, «يغيّرها كل مالك لاحقًا من إعدادات
     مساحته.» / "Each owner can change them later in their space settings.": `Switch` «تسجيل خروج تلقائي عند الإغلاق»
     / "Automatic check-out at closing"; `RadioGroup` «تقريب الزيارات» / "Visit rounding" — «تقريب لأعلى بعد عدد من
     الدقائق» / "Round up after a number of minutes" (with, when chosen, the field «بعد (دقائق)» / "After (minutes)",
     `visitRoundingMinutes`, its bounds and errors the owner's settings' own — EC18), «لأقرب نصف ساعة» / "To the
     nearest half hour", «بالدقيقة» / "By the minute"; `Switch` «لا يتجاوز سعر اليوم» / "Never more than the day price".
  Each card: read by its own `GET` (its own `Skeleton`, its own failure with «إعادة المحاولة»); «حفظ» / "Save" always
  enabled (P10); while it differs from the saved values, the `warning` badge «تغييرات غير محفوظة» / "Unsaved changes" in
  the header and the `ghost` «تجاهل التغييرات» / "Discard changes" in the footer; a refusal inside its card only
  (`FormFailure`, the 429 included); success — the toast «حُفظت الإعدادات» / "Settings saved".
- Tests T159–T163.
*Why:* AD-029 (each card its own error, one name, a form's reading width). *Undo:* the placeholder.

**D6.3 — The site reads the platform's contact from the API (G4.1).** `platform-settings/public.ts`'s
`usePlatformContact()` reads `GET /settings/public` (`['public', 'platform-settings', 'contact']`, `staleTime` 5
minutes, as the server's cache); `PlatformContact` draws the channels it answers, WhatsApp first; while it loads,
nothing (DI31); when none is set or the read fails, the caller's line, as today. `VITE_CONTACT_EMAIL` and
`VITE_CONTACT_WHATSAPP` are removed (`platformContact.ts`'s env reads, `apps/web/.env.example`, the setup document);
architecture §3's platform-settings paragraph is rewritten. Tests T164, T165.
*Why:* a contact the admin saves must reach About, the footer and the unverified dialog. *Undo:* the env reads.

**D6.4 — The spaces list lands `editable` (158; G26.6).** One shared schema (D1.17): `SPACE_STATUSES` holds
`editable`; the web's `filtersOf` and the status filter offer it as a fifth choice, «تعدّلها الإدارة» / "Kept by the
admin" (DI30), so the overview's «عرض الكل» lands on `?status=editable&stale=true` with its chip «قديمة أو ناقصة» on.
Test T166.

**D6.5 — The owners page: the owner `ALREADY_OWNER` names, and the exact email (83, 89; G27.5).**
- `ALREADY_OWNER` with `details.userId`: the email field's error «هذا البريد لمالك مسبقًا.» / "This email is already
  an owner’s." and, under it, the `link` button «اربطه بالمساحة» / "Link them to the space", which opens the owners
  page's link dialog for that person and the chosen space (its address `?link={userId}&space={spaceId}`, EC19). The
  old line `refusals.ALREADY_OWNER` is replaced.
- `useEmailAccount` reads `GET /admin/users?email=` (D1.8): `found` / `notFound` as today; a failed read is its own
  state — «تعذّر التحقق من هذا البريد الآن.» / "Couldn’t check this email right now." with «إعادة المحاولة» (a
  refetch); `accountUnconfirmed` is removed.
- Tests T167–T169.

**D6.6 — The person search names a person's front desks (94).** The link dialog's person option reads «مستخدم ·
استقبال {spaces}» / "User · reception at {spaces}" for a person with reception spaces (`AdminUserRow.receptionSpaces`);
the line before the act adds «يعمل في استقبال {spaces}، ويبقى رابطه هناك.» / "Works the front desk at {spaces}; that
link stays." (`spaces` joined by «، »). Test T170.

**D6.7 — A link from a space words the space from a fresh read (95).** The dialog opened from a space's editor reads
`GET /admin/spaces/:spaceId` when it opens (its own query, `staleTime: 0`); with no active owner it says «تصبح موثّقة
ويعدّلها مالكها» *(existing)* and its toast «المساحة موثّقة الآن» *(existing)*; with owners, «يُضاف مالكًا آخر لهذه
المساحة.» / "They become another owner of this space." and the toast «أُضيف مالك للمساحة» / "An owner was added to the
space". While it reads, the submit waits (`loading`). Test T171.

**D6.8 — The report notice beside its field, and the reports' deep links (G20.1, G21.3, G23.1, G26.7, G28.2, 184).**
- `data-reports` exports `ReportNotice` and `useReportNotice(scope, reportId)` (D2.14's single reads; the owner's or
  the admin's). The owner's profile and Packages & prices, and the admin's editor, read `?report=<id>`; the notice draws
  above the section the report's field names (`location`, `other` → the profile's «المساحة»; `hours`; `prices`;
  `amenities`; `contacts`) through a new slot of `SpaceEditor` (`noticeFor(group)`) and above `SpacePricesEditor`; an
  info `Alert` with `id="report"`:
  - title «بلاغ مفتوح على {field}» / "An open report on {field}" (the field's words *(existing)*);
  - the report's words in quotes, «“{message}” — زائر، {date}» for the owner (O12: anonymous) / «— {name}، {date}» for
    the admin; en "“{message}” — a visitor, {date}" / "— {name}, {date}";
  - `primary sm` «تم التصحيح» / "Corrected" (`PATCH` `RESOLVED`, no note), and the link «فتح البلاغ للرد» / "Open the
    report to reply" → the reports list `?open={id}`;
  - once decided: «عُلّم «تم التصحيح»» / "Marked «Corrected»" with the link «العودة إلى البلاغات» / "Back to the
    reports". A report decided already, or not found, draws nothing.
- The sheets' «تعديل الحقل» carry the report: `?report={id}#{group}` (`fieldSections.ts`).
- Both reports lists read `?open={id}` and open that report's sheet, reading it by its id when it is not on the page
  (`?open` removed when the sheet closes).
- **184:** the space editor, once its cards have drawn, scrolls to and focuses the element the address's hash names
  (`spaces`' `useHashLanding`, run when the read has answered; the cards' headings `tabIndex={-1}`); D0.4 handles a later
  hash change.
- Tests T172–T177.
*Why:* O12 and A8 («تعديل الحقل» carries the report to the edit screen, «تم التصحيح» in place); 184. *Undo:* the
plain field link.

**D6.9 — Screen 28: the handler filter, the title, the badge (G28.1, G28.4; 167's screen).** The admin's reports gain
the chips «يعالجه» / "Handled by" — «الكل» / "All", «الإدارة» / "The admin", «المالك» / "The owner" (`?handledBy=admin|owner`
→ `ADMIN | OWNER`), inline from 768 and in the sheet below it (supersedes data-reports' DI-39, by the owner's mission);
the sheet's title «{space} · {field}» (the space's name marked with its language). (The badge is D0.3's.) Test T178.

**D6.10 — Screen 26's gaps (G26.1–G26.5, G26.8, G20.2).**
- A verified row's menu reads «عرض (يعدّلها المالك)» / "View (its owner edits it)" (`menu.view`); an unverified's
  «تعديل» *(existing)*.
- Hide and show: the toast gains «تراجع» / "Undo", which sends the opposite (P9: reversible, no one else affected).
- The delete dialog's dismiss: «رجوع» / "Back" (P9).
- The phone's filter sheet: the primary, full-width «عرض {n} نتيجة» closing it (the reports sheet's words and forms
  *(existing)*, EC20), and the clear `ghost`, disabled with no filter on.
- The missing badge: «ناقصة: {groups}» / "Missing: {groups}".
- A verified space's notice adds «لتصحيح معلومة:» / "To correct a fact:" and the link «بلاغات {space}» / "{space}’s
  reports" → the admin's reports `?space={id}`.
- The shared editor's `SectionCard`: below 768 the header's action («نسخ إلى كل الأيام») leads the content instead of
  sitting beside the title (G20.2).
- Tests T179–T182.

**D6.11 — Screens 27 and 29's gaps (G27.1–G27.4, G29.1).** The «إجراءات» header visually hidden (owners and users
lists); the owners' empty state offers «إضافة مالك» *(existing words)*; the add sheet's `ACCOUNT_SUSPENDED`: «الحساب
موقوف — استرجعه أولًا.» / "The account is suspended — restore it first." with «استرجعه أولًا» a link to the users list
`?q={email}`; the owners page opens its add sheet on `?sheet=add` (removed on close), which the editor's «مالك جديد بلا
حساب؟» link uses; «انضم {date}» always with its year. Tests T183, T184.

**D6.12 — Screen 30's gaps (G30.1–G30.4; AD-025, AD-026).** The edit sheets keep the names and an amenity's icon only
(the active switch and its copy removed); a list of more than ten rows gives its sheet «الترتيب» / "Position" (1–n,
Arabic digits read, helper «من 1 إلى {n}» / "From 1 to {n}"), saved through the list's order route after the names (EC21);
each arrow is named «تحريك لأعلى: {name} — {i} من {n}» / "Move up: {name} — {i} of {n}" (and down), the row keeps the
focus, and a polite live region says «{name}: {j} من {n}» / "{name}: {j} of {n}" after a move; each tab its own hint —
the amenities' «غير النشط لا يظهر في النماذج، وتحتفظ به المساحات التي لديها. الترتيب هنا هو ترتيب الظهور.» / "An
inactive amenity is offered in no form; the spaces that have it keep it. The order here is the order shown.".
Tests T185–T187.

**D6.13 — The owner's checklist names the retired amenities (99).** The owner's profile passes `retiredAmenities`
(D2.15) to `lookups`' amenities field: each is listed with the others, ticked, with the neutral badge «لم يعد في
قائمة المنصة» / "No longer on the platform’s list"; unticking it leaves it out of the next save; the count line
(«يبقى مرفق واحد لم يعد في قائمة المنصة مرتبطًا بالمساحة.») is removed. Test T188.

**D6.14 — The gallery's per-tile progress is a bar (73), and the design says the contract's limits (74).** Each
uploading tile shows the layer's `Meter` (`kind="progress"`, label «جارٍ رفع الصورة {n}» / "Uploading photo {n}",
`valueText` «{p}٪» / "{p}%") with the percentage as its caption, in place of the spinner. The prototype's
`Admin space edit.html` gallery line becomes «حتى 10 صور · JPEG أو PNG أو WebP · حتى 4 ميغابايت للصورة» / "Up to 10
photos · JPEG, PNG or WebP · up to 4 MB each", and its upload tile draws the bar; `docs/design/CHANGES.md` gains the
row. Test T189.

**D6.15 — The admin's held items and triggers (105, 104 — the admin side).** `MenuActionItem` uses `held`; the users
page's triggers come from `shared/lists`. Test T190.

### §5.7 U7 — the front desk and the subscription sheet (lane W3a)

**D7.1 — «السجل», the day's log beside who is here (G13.1; 161's screen; K8).** Beside the «الحاضرون الآن» heading,
`Tabs` (`line`): «الآن» / "Now" (the present list, as today) and «السجل» / "Log". The log:
- **the day:** the owner chooses one (`DatePicker`, single, today by default, no day after today); reception reads
  today's only (the contract's rule), with the line «اليوم» / "Today" in place of the picker;
- **the read** (DI24, S6): the day's visits (`GET …/visits?from={d}&to={d}`) and the day's subscriber check-ins
  (`GET …/check-ins?from={d}&to={d}`), each read whole page after page (`limit=50`) — a day is bounded —, merged
  latest check-in first, then shown 20 to a page with D3.5's range;
- **a row** (a `DataTable`, cards below 768): the name (a link to the file when there is a customer) · the kind —
  the subscription's name (`primary` badge) or «زيارة» / "Visit" (`neutral`), «زيارة · طالب» / "Visit · student" for a
  student · «دخل» / "In" the time · «خرج» / "Out" the time or «—» while present · «المدة» / "Duration" «{h}:{mm}» · how
  it ended — «تلقائي» / "Automatic" for `AUTO`, «يدوي» / "Manual" for `MANUAL`, nothing while open; a written-off visit
  carries the neutral badge «لن يُحصَّل» / "Written off";
- **empty:** «لا يوجد حضور في هذا اليوم» / "No one came on this day"; loading, failure («تعذّر تحميل السجل» /
  "Couldn’t load the log", «إعادة المحاولة»), offline (P7);
- `desk`'s `components/log/`, `hooks/log/`, `services/logRows.ts` (pure merge). Tests T200–T203.
*Why:* K8 («the log a paged read by day»); 161 resolved its route, the screen was still owed. *Undo:* the tabs removed.

**D7.2 — The owner lists and undoes the written-off visits (164, DI19).** The uncollected card, for the owner, gains
a second view by a `ToggleGroup` (single) under its title: «غير محصّل» / "Uncollected" *(existing title)* and «لن
تُحصَّل» / "Written off" (`GET …/written-off-visits`, D2.10, paged): each row — the visitor's name (a link when a
customer) and its date; «لن يُحصَّل {amount} · {reason}» / "Written off {amount} · {reason}»; «كتبها {name} في {date}»
/ "Written off by {name} on {date}"; at the end `outline sm` «تراجع» / "Undo" (`DELETE …/write-off`, sent once, **never
retried by itself** — 115's condition), its success the toast «عادت الزيارة إلى غير المحصّل» / "The visit is
uncollected again" and both views refreshed; none: «لا زيارات شُطبت.» / "No visit was written off.". Reception never
sees the view. Tests T204–T206.
*Why:* the owner's 164 ("a screen offers their undo there"). *Undo:* the toast's undo only.

**D7.3 — «تسجيل كزيارة» checks the customer in as their visit (160, G13.20; DK-020).** The pre-check-in choice sends
`customerId` with the customer's name (D2.7); the line saying the visit is not added to the file is removed; the toast
*(existing)* names the visit; at check-out the visit is the customer's (no phone asked). Desk DI-14 is superseded.
Test T207.

**D7.4 — The sheet sends the price it showed (171 (a)).** A subscribe from a published price sends
`published.amountAgorot` = the amount the sheet showed. On `PUBLISHED_PRICE_CHANGED` the sheet stays open with what
was typed, reads the prices again, shows the new amount, and says D0.2's line in its failure area; the payment's amount
is refilled with the new due only when the desk had not edited it. Test T208.

**D7.5 — The write-off's reason takes the focus first (172).** `WriteOffDialog` places the focus itself on opening
(`onOpenAutoFocus` → the reason's `Textarea`), as the void's does; `autoFocus` removed. Test T209 asserts the handler
moves the focus to the reason (and fails with `autoFocus` alone, the handler removed).

**D7.6 — The phone's order, the empty uncollected card, offline (G13.2, G13.3, G13.19).** The DOM reads search →
uncollected → present (the grid places them from `xl`); an empty uncollected card is hidden below `xl` and, from it,
keeps its title «غير محصّل» with one line, a `CircleCheckIcon` and «لا توجد مبالغ غير محصّلة.» *(existing)* (the
second empty line removed); a `network` failure of the present list, the uncollected card or the search draws P7's
offline state *(existing words)*, not the destructive load failure. Tests T210, T211.

**D7.7 — Names lead to the file; who is here is worded fully (G13.5, G13.6, G13.17).** The present rows, the
search's present rows, an uncollected row with a customer, and a search card's title link to «ملف الزبون». The kind:
a subscriber's badge is their subscription's name (`primary`, from the open check-ins' read); a visit's «زيارة» or
«زيارة · طالب» (`neutral`, D2.13's `audience`). The «منذ» cell shows the time alone; the «إجراءات» header is visually
hidden; the override's durations read «ساعتين» / "2 hours"; «ملاحظة» in «استلام دفعة» and «تحصيل» carries «اختياري» /
"optional" (the `Field`'s optional marker). Tests T212, T213.

**D7.8 — Renew or subscribe from the desk; the card's progress (G13.7, G13.8).** A search card shows its current
subscription's progress lines (`progressLines` from D2.13's `current.progress`, «هذا الأسبوع 3 من 3» / "This week 3
of 3" *(existing forms)*) and the neutral badge «غير حاضر» / "Not here" when the customer is not present; it offers
«تجديد» / "Renew" while the current subscription is `ENDING_SOON` or `EXPIRED` (the sheet opened to renew it, the
subscription's state read first by its statement). The pre-check-in choice adds «تجديد» for an expired subscription
and «اشتراك جديد» / "New subscription" for none. Tests T214, T215.

**D7.9 — A full space by its count; the visit dialog's controls; the check-out's lines (G13.9–G13.11, G13.18).**
- "Full" is `present.total ≥ capacity` from the state now (not the status), its alert «المساحة ممتلئة {total}/{capacity}»
  / "The space is full {total}/{capacity}" (`dir="ltr"` for the ratio).
- «طالب» / "Student" is a `Switch`; «الوردية» / "Shift" a single `ToggleGroup` one may deselect (none chosen: no
  shift; the «بدون وردية» choice removed).
- The check-out's calculation lines (display only: the amount is the quote's, the web never prices): «{h} س × {rate} = {amount}
  · {rounding}» / "{h} h × {rate} = {amount} · {rounding}"; with the cap «السقف: سعر اليوم {day}» / "Cap: the day
  price {day}"; with no hourly rate «لا يوجد سعر بالساعة — سعر اليوم {day}» / "No hourly price — the day price {day}".
- The check-out dialog's description names the kind («زيارة · طالب»); in the money block «المستلم الآن» and
  «الطريقة» sit side by side from 768.
- Tests T216–T218.

**D7.10 — A typed phone names the file it adds to (G13.12).** In the check-out's unpaid part and in «تسجيل دين», once
the typed phone is valid, a debounced (400 ms) `GET …/customers?q={phone}&limit=2`: one match → «يُضاف إلى ملف
{name}» / "Added to {name}’s file"; none → «زبون جديد بهذا الرقم» / "A new customer with this number"; while reading,
nothing. Test T219.

**D7.11 — Money refusals, placeholders, icons, the large search (G13.13–G13.16).** A 429 in a money dialog (the visit
check-in and check-out, «تحصيل», «استلام دفعة», the sheet) adds «لم يُسجَّل شيء. إعادة المحاولة بعد ذلك لن تسجّله
مرتين.» / "Nothing was recorded. Trying again after that won’t record it twice."; every phone field takes the
placeholder «+970 59 000 0000»; «تسجيل زيارة» and «حضور» take `LogInIcon`, «خروج» `LogOutIcon`; the present list's
empty state `UsersIcon`, the search's none `SearchXIcon`; the status control its `ChevronDownIcon` from 768; the desk's
search is `Input size="lg"` (D3.4). Test T220.

**D7.12 — A usage-based subscriber's check-out says what is due (G13.4, DI10).** A fixed-price subscriber stays one
tap with its toast. A usage-based one is checked out by the tap, then a dialog opens from the answer
(`CheckInCheckOut`): title «خرج {name}» / "{name} checked out"; «اليوم {h}:{mm} · المدفوع {paid}» / "Today {h}:{mm} ·
paid {paid}"; «يبقى على اشتراك {subscription}: {balance}» / "Left on {subscription}: {balance}" (no line when nothing
is owed); the money block filled with the balance; «استلام {amount}» / "Receive {amount}" and `ghost` «لاحقًا» /
"Later". Tests T221, T222.
*Why:* the design's dialog shows the due; no quote exists for an open check-in, so it is said after the close, from
the server's answer (the web never prices). *Undo:* the one tap and its toast.

**D7.13 — The subscription sheet's gaps (G16.1–G16.5).**
- «من» and «إلى» are the layer's `DatePicker`s; a package's end is shown as text (not a disabled input).
- The custom end note by the limits set: no end and no total — «بلا تاريخ نهاية · يبقى نشطًا حتى يُنهى» *(existing)*;
  a total and no end — «بلا تاريخ نهاية · ينتهي عند استهلاك {limit}» / "No end date · ends once {limit} are used"; an
  end and a total — «ينتهي في {date} أو عند استهلاك {limit}، أيهما أسبق» / "Ends on {date} or once {limit} are used,
  whichever comes first"; `{limit}` counted — days: ar zero «لا أيام» · one «يوم واحد» · two «يومين» · few «{n} أيام» ·
  many «{n} يومًا» · other «{n} يوم», en "{n} day" / "{n} days"; hours: ar zero «لا ساعات» · one «ساعة واحدة» · two
  «ساعتين» · few «{n} ساعات» · many «{n} ساعة» · other «{n} ساعة», en "{n} hour" / "{n} hours".
- The earlier debt is a warning `Alert` (its words *(existing)*); the money block's `calc` lists each earlier item
  «{item}: {balance}» and «{التجديد | الاشتراك}: {name} {price}» / "{Renewal | Subscription}: {name} {price}", and its
  due is labelled «المجموع» / "Total".
- A usage-based custom subscription's rate is prefilled from the published hour or day price, helper «من السعر
  المنشور» / "From the published price", and the line «يُحسب من الحضور: {rate} للساعة» / "Charged by attendance:
  {rate} an hour" (or «لليوم» / "a day").
- The packages' group heading «خاصة بالمكتب — لا تظهر للزوار» / "For the desk only — never shown to visitors", each
  package row a «خاصة» / "Private" badge.
- Tests T223–T225.

**D7.14 — `visits.md`'s *Authority* names the desk's screen (G13.24).** Documents only.

### §5.8 U8 — customers, the customer's file, payments (lane W3b)

**D8.1 — A customer's actions by their state, in the list and in the file (G14.2, G15.1, G15.7; DK-013).**
`desk` gains `components/customer-actions/CustomerActions.tsx` (and its hook), used by the list's row «⋯» and the
file's header:
- present → «خروج» / "Check out" (the desk's check-out of their stay); not present, with a subscription that can be
  used → «حضور» / "Check in";
- owing → «استلام {amount}» / "Receive {amount}": the **oldest owing item's** balance, paid through the pay dialog on
  that item, whose description names it («أقدم بند: {item}» / "Oldest item: {item}") (DI32: a payment pays one item);
- the current subscription `ENDING_SOON` or `EXPIRED` → «تجديد» / "Renew".
In the row's menu these come first, then the existing items; in the file's header they are buttons (the first
`primary`, the others `outline`), then «⋯». On the file's subscription cards, «تجديد» shows only while that
subscription is `ENDING_SOON` or `EXPIRED`. Tests T230–T232.

**D8.2 — «تذكير على واتساب» from the file (G15.2).** In the file's header, while `debtAgorot > 0` and the customer
has a phone: `outline sm` «تذكير على واتساب» / "WhatsApp reminder", a link (`target="_blank" rel="noopener"`) built by
D3.11 from `reminderTemplate` (D2.12; the default text when `null`) with the debt, the customer's first name and the
space's name; its caption «يفتح واتساب برسالة جاهزة، وترسلها أنت.» / "Opens WhatsApp with a ready message; you send
it.". Test T233.

**D8.3 — The statement names who recorded and who voided (162).** Each payment row of a statement and of the file's
unpaid visits: «سجّلها {name}» / "Recorded by {name}"; a void: «ألغاها {name}: {reason}» *(existing line)*. Supersedes
desk DI-48. Test T234.

**D8.4 — A subscription's corrections, from its card (163; DI11–DI13).** The file's subscription card's «⋯» gains
«تصحيح الاشتراك» / "Correct the subscription" (the staff's; `held` with «انتهى الاشتراك مبكرًا» / "Ended early" on an
ended one). It opens a `Sheet side="end"` titled «تصحيح {name}» / "Correct {name}":
- **«الاسم والتواريخ والحدود» / "Name, dates and limits"** (`PATCH …/subscriptions/:id`): «الاسم» / "Name"; «من» /
  "From" and «إلى» / "To" (`DatePicker`s; «إلى» clearable — «بلا تاريخ نهاية» / "No end date"); «مجموع الأيام» /
  "Total days", «أيام في الأسبوع» / "Days a week", «ساعات في اليوم» / "Hours a day", «مجموع الساعات» / "Total hours"
  (each clearable: «بلا حد» / "No limit"); only the changed fields are sent;
- **«السعر» / "The price"** — the owner's only (`PUT …/price`): «طريقة الاحتساب» / "Billing" *(existing words: «سعر
  ثابت · بالساعة · باليوم»)*, «السعر» / "Price", «سبب التصحيح» / "Why it is corrected" (required, 1–200);
- the footer «حفظ التصحيح» / "Save the correction" (sends the changed part or both, the dates and limits first, each
  its own outcome) and «رجوع» / "Back"; success — the toast «صُحّح الاشتراك» / "The subscription was corrected", the
  file refreshed; refusals inside the sheet: `SUBSCRIPTION_ENDED` — «انتهى هذا الاشتراك مبكرًا؛ لا يُصحَّح.» / "This
  subscription was ended early; it can’t be corrected."; `PRICE_BELOW_PAID` — «السعر أقل مما دُفع عليه.» / "The price
  is below what was paid on it."; `out_of_range` on `endsOn` — «النهاية قبل البداية» / "The end is before the start";
  the 429.
- `desk`'s `components/correct/`, `hooks/correct/`. Tests T235–T238.
*Why:* the owner's 163 (the routes as they are; the card is its place). *Undo:* the item removed.

**D8.5 — The type filter: monthly and weekly (G14.1).** The customers list's «النوع» / "Type": «شهري» / "Monthly"
(`MONTH`), «أسبوعي» / "Weekly" (`WEEK`), «باقة» / "Package", «مخصّص» / "Custom", «بدون اشتراك» / "No subscription"
(the last three *(existing)*), in foundation §13's order. Test T239.

**D8.6 — The lists' and the file's smaller gaps (G14.3, G14.4, G15.3–G15.6, G17.1, GX.1).**
- Customers: "no customers yet" — `UsersIcon`, «لا زبائن بعد» *(existing)* and «زبون جديد»; «زبون جديد» moves from the
  top bar into the row above the list, at its end, beside the count (P1 amended; desk.md's screen-16 bullet rewritten);
  the footer's range (D3.5).
- The file: the owner's «لن يُحصَّل…» on each unpaid visit's «⋯» (the desk's write-off dialog); the unpaid card's
  description «تُحسب في رصيده.» / "They count in their balance."; «هذا الزبون يأتي بزيارات فقط.» *(existing)* only when
  there is no unpaid visit, with `UsersIcon`; the presence badge `info` «حاضر منذ {time}» / "Here since {time}"
  (`present.since`).
- Payments: the ledger's empty states `CircleCheckIcon` (none) and `SearchXIcon` (no match), «دفعاتي اليوم»'s
  `CircleCheckIcon`; both lists' range (D3.5).
- Tests T240–T243.

**D8.7 — The ledger's staff filter names the space's other owners (166).** `spaces` exports
`useSpaceOwners(spaceId)` (the active owners of `GET /manage/spaces/:spaceId`, which `AdminSpace.owners` answers to
its staff — EC10); `PaymentsPage` lists the owner signed in, then the other owners, each «{name} · صاحب المساحة» /
"{name} · owner", then the reception accounts. No API change. Test T244.
*Why:* the owner's 166; the route already exists. *Undo:* the owner and reception only.

### §5.9 U9 — the public site and the account (lane W4)

**D9.1 — The users feature, one folder per operation (82), first, with no change of behaviour:** `hooks/account/
useAccount.ts`, `hooks/password-change/useChangePassword.ts`, `hooks/forced-change/useForcedPasswordChangeForm.ts`,
`hooks/sign-out/useSignOutAction.ts`; `components/account-menu/{AccountMenu,AccountMenuContent,AccountMenuSection,
CompactAccountMenu}.tsx`, `components/forced-change/ForcedPasswordChangeForm.tsx`, `components/sign-out/{SignOutButton,
SignOutFailure}.tsx`; tests moved beside them; `index.ts`'s exports unchanged. (D0.5 edits `AccountMenuContent` before
this move: U9 starts after U0, so the move carries U0's version.)
*Why:* 82's first option; screen 9 adds four operations to the feature. *Undo:* —.

**D9.2 — Screen 9, «إعدادات حسابي» (C1, C2, C6, AC-012, AC-013).**
- **Route** `/me` (D0.6), in the account's layout, signed-in only. **Reads** `GET /me` (`['me', 'account']`);
  **writes** `PATCH /me`, `POST /me/password`, `POST /auth/password/forgot`. `features/users` gains
  `repository` calls, `hooks/settings/{useMyAccountQuery,useProfileForm,useLanguageChoice,useThemeChoice,
  usePasswordChangeForm,useSetPasswordLink}.ts`, `components/settings/{ProfileCard,PreferencesCard,SignInCard,
  PasswordChangeForm}.tsx`; `shared/session` gains `accountEdited(userId, { name?, language? })`, which updates the
  held user's name and language (as `passwordChanged` does its token), so the account menu shows the new name at once.
- **Page** `pages/site/account/settings/AccountSettingsPage.tsx`: its `h1` «إعدادات حسابي» / "Account settings"
  (`heading-1`), then one column `max-w-3xl` of three cards:
  1. **«الملف الشخصي» / "Profile"**: `Field` «الاسم» / "Name" (`autoComplete="name"`, the registration's rule); the
     email as text — «البريد الإلكتروني» / "Email", the address `dir="ltr"`, and «تسجّل الدخول بهذا البريد» / "You sign
     in with this email" (no change offered); «حفظ» / "Save"; success — the toast «حُفظت التغييرات» / "Changes saved".
  2. **«التفضيلات» / "Preferences"**, «تُطبَّق فورًا.» / "Applied right away.": «اللغة» / "Language" — a single
     `ToggleGroup` «العربية» (`lang="ar"`) · «English» (`lang="en"`), helper «تُحفظ في حسابك» / "Saved to your
     account": a choice applies at once (the preferences) and sends `PATCH /me { language }`; its failure puts the
     choice back and toasts «تعذّر حفظ اللغة» / "Couldn’t save the language" with «إعادة المحاولة» (P8's exception:
     the success shows in place); «المظهر» / "Theme" — «فاتح» / "Light" · «داكن» / "Dark" · «حسب الجهاز» / "Device
     setting", helper «على هذا الجهاز» / "On this device" (the stored choice, `system` by default). The headers'
     toggles stay this device's only (DI20).
  3. **«تسجيل الدخول» / "Signing in"**, «الطرق التي تدخل بها إلى حسابك.» / "The ways you sign in to your account.":
     with `hasGoogle`, the row «Google» — «تسجّل الدخول باستخدام Google · {email}» / "You sign in with Google ·
     {email}" — and the `success` badge «مربوط» / "Linked", then a `Separator`; the row «كلمة المرور» / "Password":
     - **with a password:** «تسجّل الدخول ببريدك وكلمة المرور» / "You sign in with your email and password" and
       `outline sm` «تغيير» / "Change" (`aria-expanded`, `aria-controls` the form), which opens the form below it, the
       focus in its first field: «كلمة المرور الحالية» / "Current password", «كلمة المرور الجديدة» / "New password" (the
       rules' checklist), the line «تغيير كلمة المرور يسجّل خروجك من كل الأجهزة الأخرى» / "Changing your password signs
       you out on all your other devices" (C2), «حفظ كلمة المرور» / "Save password" and `ghost` «رجوع» / "Back"
       (closes it, the focus back on «تغيير»); success — the toast «تم تغيير كلمة المرور، وسُجّل خروجك من الأجهزة
       الأخرى» / "Password changed, and you were signed out on your other devices", the session renewed
       (`passwordChanged`), the form closed; `CURRENT_PASSWORD_INCORRECT` on its field *(existing line)*; the 429's
       countdown;
     - **without one (Google only, C1):** «لم تُعيَّن بعد» / "Not set yet", «لتسجيل الدخول بالبريد وكلمة مرور أيضًا،
       نرسل رابطًا إلى بريدك» / "To also sign in with your email and a password, we send a link to your email", and
       `outline` «أرسل رابط تعيين كلمة المرور» / "Send a link to set a password" (`POST /auth/password/forgot` with
       the account's email); then the link-sent block of `auth` *(existing component)* with «أرسلنا إلى بريدك رابطًا
       لتعيين كلمة المرور. الرابط صالح لمدة ساعة. تفقّد مجلد الرسائل غير المرغوب فيها.» / "We sent a link to set your
       password to your email. The link is valid for one hour. Check your spam folder." and its resend countdown.
- **States:** each card's `Skeleton` while `GET /me` loads; its failure — destructive `Alert` «تعذّر تحميل حسابك» /
  "Couldn’t load your account" with «إعادة المحاولة»; offline P7.
- Tests T250–T256.
*Why:* foundation §13 #9, C1, C2, C6. *Undo:* the stub.

**D9.3 — Google's first sign-in is welcomed (32); its "linked" toast stays (G5.5, C5).** `useGoogleSignIn`: `created`
→ the toast `auth.register.welcome({ name })` *(existing: «أهلًا {name}، تم إنشاء حسابك»)*, worded once the session
is set (the account's language); `linked` → its toast with `duration: Infinity` and a close button. Tests T257, T258.

**D9.4 — Sign in, register, forgot and reset: the way back and `next` (G5.1–G5.4, G6.1, G6.2, G7.1–G7.3; C3, C4).**
- The sign-in card's description: «سجّل الدخول لحفظ مساحاتك المفضّلة ومتابعة بلاغاتك، أو لإدارة مساحتك.» / "Sign in
  to save your favourite spaces and follow your reports, or to run your space.".
- **The way back** (`AuthWayBack`, `pages/site/auth/`), on sign-in and register: with a safe `next` — «العودة إلى
  {space}» / "Back to {space}" when `next` is a space's page whose name the directory's cached read holds
  (`directory`'s `useCachedSpaceName(slug)`), else «العودة إلى الصفحة السابقة» / "Back to the previous page"; without
  `next` — «العودة إلى الرئيسية» / "Back to home" (DI33).
- `next` travels with «نسيت كلمة المرور؟» to the forgot page and back with its «العودة إلى تسجيل الدخول».
- After a sign-in with a password, the toast «أهلًا بعودتك» / "Welcome back" (a held action's toast, when one runs,
  takes its place, C4).
- Register's owner note links «تواصل معنا» to `/about#owners`.
- The sent step always offers «استخدم بريدًا آخر» / "Use another email" under the resend (C3), which opens the empty
  form with the focus in it.
- The reset card's footer «العودة إلى تسجيل الدخول» / "Back to sign in", except after success.
- «لا يمكنك الوصول إلى بريدك؟ تواصل معنا» opens the platform's WhatsApp (`wa.me/{digits}`, from D6.3's contact) when
  it is set, else `/about#contact`.
- Tests T259–T264.

**D9.5 — The fourth password rule (G6.3, AC-020).** `packages/shared/src/users/passwordPolicy.ts`'s `PASSWORD_RULES`
gains `{ id: 'bytes', onlyBroken: true }` (at most 72 bytes in UTF-8, the policy's own bound); `usePasswordRules` shows
it only while broken: «طويلة جدًا — اختصرها» / "Too long — shorten it" (register, reset, the settings' change). Tests
T265, T266.

**D9.6 — A guest's held action survives a password recovery (168).** `shared/storage` declares
`STORAGE_KEYS.heldIntent` (`masaha.heldIntent`, in `localStorage`, so the reset link's new tab reads it):
`{ kind: 'favorite' | 'report', spaceId: number, slug: string, path: string, at: number }`. `shared/routing`'s guest
module (`guest/heldIntent.ts`) writes it when a guest presses a held action, alongside the memory it holds today; it
is **cleared** when it runs, when the guest lands on another site page (the S14 rule, `noteSitePage`), on any
sign-out, and when older than **15 minutes**. **The session confirms it:** only a session established by a sign-in in
this browser (`onSessionEstablished`, source `signIn`, a Google sign-in included) consumes it within its life — the app
goes to its `path` when elsewhere (a `replace`), then `favorites` saves the space (with its toast) or `data-reports`
opens the report's dialog; a restore or a refresh never runs it. **Never in the address.** Architecture §4 (*Where
state lives*) gains the line. Tests T267–T270.
*Why:* the owner's 168. *Undo:* the memory only.

**D9.7 — Home and About (carried 2, 3, 4, 9, 10; G4.2–G4.4).** As the carried items say; About's «تصفّح المساحات» is
the default (primary) variant, full width below 768 (`w-full md:w-auto`); the verified card's title takes a
`CircleCheckIcon` (`text-primary`); the contact section's sentence becomes the design's (DI14): «اكتب لنا بسؤال، أو
عن بلاغ لم يصلك ردّه، أو عن خطأ في الموقع.» / "Write to us with a question, about a report that got no reply, or about
a mistake on the site.". Tests T271–T275 (carried 4, 8b, 8c, 10; G4).

**D9.8 — The Directory (G2.1–G2.3, carried 11, 133, 134).**
- The map view shows its result count, the list's words *(existing)*, beside «الأقرب إليّ»; on a phone its search and
  «الفلاتر» share one row.
- The chosen space on the map (the card from 768, the phone's sheet) shows its distance «على بعد {km} كم» *(existing
  card words)* when a near point is set (`straightLine.ts`).
- The results' scroll and focus run once the new page has arrived (`isPlaceholderData` false), not before (carried 11).
- **133:** the place filter stops at `DIRECTORY_AREAS_MAX` (50): once 50 are chosen, the others are disabled and the
  line «يمكن اختيار 50 منطقة على الأكثر.» / "You can choose at most 50 areas." shows (`lookups`' `AreaFilter`).
- **134:** the map's marks are memoised on the answer and the language (`useDirectoryMap`), and `MarkerMap` gives each
  mark stable handlers (one `useCallback` per handler, read by id), so a key typed in the map's search rebuilds no mark;
  measured in the real run (R27).
- Tests T276–T280.

**D9.9 — The map's marks on its light tiles (135, OD5 (a)).** `leaflet.css`: inside `.leaflet-container`, the marks'
fills and edges take the light theme's values in both themes (the tiles are always light), and `MapMarkSample` draws a
legend's mark on a light swatch, so the legend and the map agree in dark. A layer change. Test T281 (the stylesheet's
rule); the real run's dark shot (R26).

**D9.10 — Near me waits once the permission is known (136).** `useNearMe`: where the Permissions API answers, `granted`
starts the 15 s at once; `prompt` starts them when the state becomes `granted` (its `change` event) or a position
arrives; `denied` ends at once as denied; without the API, from the press, as today. Tests T282, T283.

**D9.11 — Home's areas show no number past the pins' ceiling (137).** While the pins answer `truncated`, the area
cards and «كل المناطق» show their names without counts. Test T284.

**D9.12 — The space page (G3.1–G3.4, carried 6, 7, 8a, 138).** The status panel is always drawn (its live part
always says something: the state or «لا تتوفر حالة مباشرة» *(existing)*); today's line reads «مغلقة مؤقتًا اليوم» /
"Temporarily closed today" while a closure runs today; the location map shows near me's point (`PlaceMap`'s user
mark); «الاتجاهات» is the location section's header action. **138:** once a refresh fails and the last status read is
older than 3 minutes, «الحالة مباشرة الآن» becomes «آخر تحديث» + counted — ar zero «الآن» · one «قبل دقيقة واحدة» ·
two «قبل دقيقتين» · few «قبل {n} دقائق» · many «قبل {n} دقيقة» · other «قبل {n} دقيقة»; en "Updated {n} minute ago" /
"Updated {n} minutes ago" — and the badge turns `neutral`; a later success restores it. Tests T285–T290.

**D9.13 — The error states (G8.1, G8.2, carried 5).** `RetryState`'s «إعادة المحاولة» re-runs the route (revalidates
in place) for the general error, and reloads only when the page's code failed to load; a second failure in a row adds
«ما زال الخطأ قائمًا. حاول بعد قليل.» / "The error is still there. Try again in a little while."; the offline line is
announced on each press (carried 5). The bare 403 of `/dashboard/admin` for a non-admin says «هذه الصفحة غير متاحة
لحسابك.» *(existing)* and «إن كنت تظن أن هذا خطأ، تواصل معنا.» / "If you think this is a mistake, contact us.", with
«الرئيسية» / "Home" and «تواصل معنا» / "Contact us" (→ `/about#contact`) (DI21); a 403 inside a shell keeps none (the
sidebar is the way on). Tests T291–T293.

**D9.14 — Favourites (G10.1–G10.3).** The count, «الأقرب إليّ» and the location line show only once the list has
answered with at least one space; the empty state sits in a `Card` with the default «تصفّح المساحات»; «اختر منطقتك»
leads to `/spaces?filters=open`, on which the Directory opens its filter sheet below 1024 or focuses its place field
from 1024, then removes `filters` from the address. Tests T294, T295.

**D9.15 — «بلاغاتي»'s range (GX.1)** and **carried 8a–8c's tests** (the footer's room given back; «اختر منطقتك»'s
scroll and focus; «حدّد موقعي على الخريطة» starting the pick on `/spaces?view=map`). Tests T296–T298.

### §5.10 U10 — the closing documents (the lead, last)

**D10.1 — The findings.** Each built finding's file gets `Resolved` and its *Resolution* line (§7) in the commit that
builds it; the accepted ones (84, 187, 193; 22, 112, 115 by OD1–OD3) get `Accepted` with the owner's line in U10. **The
index moves every entry once, in U10** (S2). At the end *Open* holds 23, 33, 46, 64, 65, 152.
**D10.2 — The build map and the scope.** `v1-mvp.md`: steps 1–12 each end "*Built*" with the screens it names (and #PRNUM);
the *Planned API surface*'s managed and admin tables name every route as built; `overview.md`'s *Built* adds the
screens: Finance, Overview, Audit, Platform settings, Users (the account's settings), the desk's log and written-off
visits, the corrections; foundation §13's screen 31 line names the owner's log (DI1) and screen 24's the account card.
**D10.3 — The design archive.** `SCREENS.md`: the owner's audit moves from *Also in the archive* to screen 31's row
(«`Admin audit.html`, `Owner audit.html` (O13)»); `CHANGES.md` gains D6.14's row (74).
**D10.4 — `PlaceholderPage`** is deleted once no route uses it (EC22), with its test.
**D10.5 — Architecture §2's *Built so far*** names every page; §3's table and the dashboard-only list unchanged.

### §5.11 Stronger decisions (S)

- **S1 — 91's replacement only for a never-used account** (D1.4): no active owner link, no audit entry as actor, no
  favourite, no data report. *Why:* registration verifies no email, so the literal rule would let a stranger retire a
  real account (an owner whose admin-issued password expired, unverifying their space). *Undo:* the plain rule (OD6).
- **S2 — The findings index is moved once, by the lead, at the end** (an override of "a change of status … moves it …
  in the same commit", stated here): each finding's own file changes in its fixing commit; nine lanes moving entries in
  one list would collide at every merge. *Undo:* each commit moves its entry.
- **S3 — Each lane writes its capability documents in its own commits; the shared documents are integrated by the
  lead** (the contract's sections by the API lanes, each in its own section; `v1-mvp.md`, `overview.md`, `SCREENS.md`,
  the index by U10).
- **S4 — The owner's audit is not a 33rd screen:** foundation §13 keeps 32; screen 31's line names the owner's log
  (O13 is "the admin's audit page scoped to the space") (DI1).
- **S5 — One report is read by its id** (D2.14), never searched for in a list's first page.
- **S6 — The desk's log reads one day whole and pages it in the browser** (D7.1): a day is bounded, and two paged
  routes cannot be merged page by page.
- **S7 — 21's key derived from `JWT_SECRET`** (HKDF, its own label), so the deployment adds no variable.
- **S8 — No new screen departs from its prototype silently:** every departure is a DI of §6.
- **S9 — Each lane's first commit is its red test of its first fix** where a fix has one (the carried items' rule,
  extended): no code without its failing test first.

### §5.12 Proposed alternatives (argued, not applied)

- **PA1 — 83 without a contract change:** on `ALREADY_OWNER`, the sheet looks the owner up by 89's exact email (D1.8)
  and opens the link dialog. Cheaper, but the owner chose "a contract change".
- **PA2 — 63 by a measurement** at the deployment (as F1's six): no job, no port method. Not applied: 63 offers the job
  first, and the job is small.
- **PA3 — 122 by a lower bound on usage-based prices:** no migration, but a per-day subscription without an end still
  overflows; not applied.
- **PA4 — 164 as a filter of `GET …/visits` (`writtenOff=only`):** one route fewer, but the visits list requires a range
  of days and a written-off visit may be months old; not applied.
- **PA5 — 180 by lazy components inside the features** (`React.lazy` for the dashboard's lists): no new entry, but a
  feature would hold loading states that belong to the page; not applied.
- **PA6 — G14.1 by deriving the period** (fixed, no package, no limits, 7 or 30 days): no migration, but a custom
  subscription of the same terms reads as weekly; not applied.
- **PA7 — The desk's log from one new composed route** (`GET …/attendance?date`, the visits and check-ins merged and
  paged on the server): cleaner for the browser, one more read model on the API; not applied (S6 suffices).

---

## §6. Design issues (DI) — each with its recommendation

A screen detail no prototype or decision settles. The supervisor settles each on the owner's behalf before the run;
the recommendation is what §5 builds.

- **DI1 — Where the owner's audit sits among foundation §13's screens.** (a) inside screen 31's line («Audit log — the
  admin's; the owner's, scoped to the space, O13») · (b) a 33rd screen. **Rec. (a)** (S4): O13 is defined as the
  admin's page scoped to the space; the count of 32 stays true.
- **DI2 — The owner's overview names the unpriced visits** (the API counts them; the prototype has no row). **Rec.:**
  a row after the uncollected, to the desk's «بدون سعر» card (D5.1 item 5); the owner's open decision of #97 asked that «يحتاج انتباهك» count the unpriced and the uncollected visits.
- **DI3 — «لم تُحصَّل اليوم»:** the count has no day. **Rec.:** the line drops «اليوم» (D5.1 item 4).
- **DI4 — The paged lists' quiet sign (132):** (a) the asked page marked at once and the rows dimmed while it loads ·
  (b) a spinner by the count · (c) nothing but `aria-busy`. **Rec. (a)** (D3.6): it answers the tap where the eye is,
  and the list never blanks (S13 and the admin lists' rule kept).
- **DI5 — «اليوم: {present + left today}»** has no field. **Rec.:** «الآن: {members} و{visits}» only (D5.1 ②).
- **DI6 — The closures awaiting their extension** are a count, not a list. **Rec.:** one counted row to the
  announcements page (its tabs' badges lead on) (D5.1 item 7).
- **DI7 — The admin's fifth tile «مستخدمون جدد»** (OV4) is not in the prototype. **Rec.:** a fifth tile linking to the
  users list (newest first; the list has no date filter, so it shows the list, not the 30 days), the grid at five
  from 1280 (D5.2).
- **DI8 — The stale tile's helper** names the prototype's constants (30 / 60 days). **Rec.:** «حسب حدود الحداثة في
  إعدادات المنصة، أو لم تُضف بعد» (OV6: never a constant on screen).
- **DI9 — Finance shows «غير محصّلة»** (193 accepted: the desk's list, never added). **Rec.:** a fourth debts tile
  with its count, its amount and «لا تُجمع مع الديون», linking to the desk (D5.4).
- **DI10 — A usage-based subscriber's check-out dialog** (G13.4): (a) after the tap, from the answer (D7.12) · (b) an
  API quote for an open check-in, then the design's dialog before the close · (c) the one tap kept, decided. **Rec. (a):**
  it shows the true due with no new route, and the web never prices.
- **DI11 — Where the corrections open (163):** **Rec.:** «تصحيح الاشتراك» in the subscription card's «⋯» (the
  card is the place the owner named), opening an end sheet.
- **DI12 — One sheet or two for the terms and the price:** **Rec.:** one sheet, two sections, the price section the
  owner's only, one «حفظ التصحيح» that sends each changed part (D8.4).
- **DI13 — An ended subscription:** **Rec.:** the item held with «انتهى الاشتراك مبكرًا» (the API refuses
  `SUBSCRIPTION_ENDED`); an expired one (its end passed) may still be corrected (the API allows it).
- **DI14 — About's contact sentence:** the built «راسلنا إن كان لديك سؤال، أو مشكلة في الموقع الإلكتروني.» against the
  design's «اكتب لنا بسؤال، أو عن بلاغ لم يصلك ردّه، أو عن خطأ في الموقع.». **Rec.:** the design's (it names the
  reports' case).
- **DI15 — Finance's «استلام دفعة»:** (a) a link to the customer's file · (b) the desk's pay dialog inline. **Rec. (a):**
  the file has «استلام {amount}» (D8.1); finance stays a read, and no lane waits on another.
- **DI16 — The heatmap's rows and columns:** **Rec.:** weekdays in the language's week order, a weekday with no
  presence left out; hours from the first to the last with any presence (the prototype's 08–17 was its sample).
- **DI17 — The audit logs' period and action filter:** the prototype offers «فترة محدّدة»; the contract has two
  periods only (the owner's decision 9). **Rec.:** two choices; the action type a group of actions (the shared
  schema's comment: "a group of the web's action types").
- **DI18 — The audit's details:** **Rec.:** a line only where the stored values say something (amounts, reasons,
  from → to); none otherwise (D6.1).
- **DI19 — Where the written-off visits are listed:** (a) the uncollected card's second view (owner) · (b) the log's
  rows only · (c) Finance › Debts. **Rec. (a):** the write-off is made there, and its undo belongs beside it.
- **DI20 — The language toggles in the headers:** (a) this device's only · (b) also saved to the account. **Rec. (a):**
  the settings' choice is the account's (C6 «تُحفظ في حسابك»), the quick toggle the device's, as today.
- **DI21 — The bare 403 at `/dashboard/admin`:** **Rec.:** no shell (the architecture's rule), but its ways on and the
  design's sentence (D9.13).
- **DI22 — Favourites' «اختر منطقتك»:** **Rec.:** `/spaces?filters=open` (D9.14): the sheet below 1024, the place
  field's focus from it.
- **DI23 — The desk's log for reception:** **Rec.:** today only, no picker (the contract refuses another day).
- **DI24 — The log's paging:** **Rec.:** the day read whole and paged by 20 in the browser (S6).
- **DI25 — The customers' «زبون جديد»:** **Rec.:** in the row above the list, at its end (P1 amended), as the design.
- **DI26 — The overview's «تجديد»:** **Rec.:** to the customer's file, where «تجديد» opens the sheet (no address opens
  it today).
- **DI27 — The account menu's role words:** **Rec.:** the role at the space in the URL (owner / reception), «أدمن» in
  the admin's shell, none on the site.
- **DI28 — The reminder's {الاسم}:** **Rec.:** the customer's first name (the first word), as the prototype's.
- **DI29 — Finance's address:** **Rec.:** `?tab=` and `?month=`, defaults left out (S8 of the lists).
- **DI30 — `editable` in the spaces list (158):** (a) a fifth choice «تعدّلها الإدارة» · (b) read only, not offered.
  **Rec. (a):** an address one cannot see in the filters cannot be cleared from them.
- **DI31 — The site's contact while it loads:** **Rec.:** nothing drawn until it answers (5 minutes' cache), then the
  channels or the caller's line.
- **DI32 — The customer's «استلام {amount}»:** **Rec.:** the oldest owing item's balance, paid through that item (a
  payment pays one item, ADR 0010); the dialog names the item.
- **DI33 — The auth card's way back with `next`:** **Rec.:** «العودة إلى {space}» from the directory's cached read,
  else «العودة إلى الصفحة السابقة».

---

## §7. Related findings — each closed or accepted, with its *Resolution* line

Each built finding's file: `**Status:** Resolved · **Date:** … · **Resolved:** 2026-10-29` and a last paragraph
`**Resolution (#PRNUM):** …` with the line below. The accepted ones: `**Status:** Accepted` and `**Accepted (the
owner, 2026-10-29):** …`.

| # | Outcome | *Resolution* / *Accepted* line |
|---|---|---|
| 14 | Resolved | The owner's audit screen is built from O13 (`Owner audit.html`): «سجل التدقيق» in «الفريق والإعدادات», the admin's audit page scoped to the space (D6.1). |
| 17 | Resolved | Two timed jobs sweep the expired refresh tokens, reset tokens, recoveries and rate-limit counters, 5,000 rows a table a run (D1.2). |
| 21 | Resolved | A token presented again within the grace gets the same successor, an HMAC of it under a key derived from `JWT_SECRET` (D1.1). |
| 22 | Accepted (OD1) | The reset email's words stay in `resetEmail.copy.ts`, held to one shape in both languages by its test; `localisation.md` names this second home. |
| 27 | Resolved | What only the dashboard uses has a chunk that never imports the dashboard's back; `check:build` refuses such a cycle (D4.1). |
| 32 | Resolved | `POST /auth/google` answers `created`; a first Google sign-in is welcomed as registration is (D1.3, D9.3). |
| 48 | Resolved | The init script is an inline Compose config, so the container depends on no folder (D4.4). |
| 55 | Resolved | Each route test file pays its lazy shells' first transform before its tests wait; CI's slowest is recorded (D4.3). |
| 63 | Resolved | A daily job removes the stored files that no photo holds and that are older than an hour (D2.5). |
| 69 | Resolved | The contract names `invalid_format` for an id of the wrong JSON type and `invalid_choice` for a deleted space; a test pins both (D1.13). |
| 73 | Resolved | The layer's `Meter` draws each tile's progress (D3.1, D6.14). |
| 74 | Resolved | The prototype's gallery line says the contract's limits (D6.14). |
| 77 | Resolved | Every race names its table, and the reach (8 s) sits well under the race tests' 20 s (D1.14). |
| 78 | Resolved | The test identifies the names' own query by its statement (D1.15). |
| 79 | Resolved | `namesFor` takes `tx` as a required `Tx | undefined` (D1.16). |
| 82 | Resolved | The users feature keeps one folder per operation (D9.1). |
| 83 | Resolved | `ALREADY_OWNER` carries `details.userId`, and the add sheet links that owner (D0.1, D1.7, D6.5). |
| 84 | Accepted (owner) | v1 needs no linking of an existing account to a second front desk (close to in-app claiming, *Not in v1*). |
| 87 | Resolved | The route tests pay the shell's first load before their waits (D4.3). |
| 89 | Resolved | The add sheet reads the account by its exact email; a failed read is worded apart, with a retry (D1.8, D6.5). |
| 91 | Resolved | An expired pending account that never acted and owns no space is replaced by the account its address's holder creates (D1.4, S1). |
| 92 | Resolved | A deactivation ends the person's sessions only when no other active link remains (D1.9). |
| 93 | Resolved | Each of the three refusals and the expiry's second check has a test its removal turns red (D1.12). |
| 94 | Resolved | The person option and the line before the act name the front desks a person works at (D6.6). |
| 95 | Resolved | The link dialog reads the space's owners when it opens from a space, and words the line and the toast from it (D6.7). |
| 98 | Resolved | (By OD4's outcome; recommended:) documentation §5's guide is revised: … (OD4's text). |
| 99 | Resolved | The space's reads name its retired amenities; the owner's checklist shows each, marked, until a save leaves it out (D2.15, D6.13). |
| 102 | Resolved | The live region holds only the terms and the price (D5.9). |
| 103 | Resolved | One reader of Arabic-Indic digits in `shared/lib` serves the five (D3.7). |
| 104 | Resolved | `useRowTriggers` lives in `shared/lists`; both lists use it (D3.8). |
| 105 | Resolved | Radix skips a disabled item; a held item is `aria-disabled`, stays in the roving focus, and is read with its reason (D3.3). |
| 106 | Resolved | An admin's account is refused `ACCOUNT_IS_ADMIN` on the re-issue; the insert buttons' names hold their tokens (D1.10, D5.10). |
| 112 | Accepted (OD2) | The web holds one key per intent and never reuses one across two visits, so the case does not arise from the desk; the rule stays. |
| 115 | Accepted (OD3) | The desk never retries the write-off or its undo by itself (test 41 of #117, and D7.2's undo), the condition the owner set. |
| 120 | Resolved | A test pins every 2026 transition: PostgreSQL's Gaza dates equal Node's (D2.2). |
| 121 | Resolved | A run whose failures fill its batch answers 500, named in the log (D2.4). |
| 122 | Resolved | `subscription_usage` computes the due in `bigint` (M1). |
| 126 | Resolved | A whole phone matches on its national digits without the trunk, so both codes find each other (D2.6). |
| 127 | Resolved | The dated list bounds `checked_in_at` by the two Gaza midnights, which the index serves (D2.3). |
| 130 | Resolved | Every shell has its skip link, and the focus moves on a page change after the first (D0.4). |
| 132 | Resolved | A paged list marks the asked page at once and dims its rows until the answer (D3.6). |
| 133 | Resolved | The place filter stops at 50 areas and says so (D9.8). |
| 134 | Resolved | The marks are memoised with stable handlers; typing on the map was measured (D9.8, R27). |
| 135 | Resolved | The marks take the light values on the always-light tiles, the legend the same (D9.9). |
| 136 | Resolved | Near me's wait starts once the permission is known (D9.10). |
| 137 | Resolved | Home shows no count while the pins are truncated (D9.11). |
| 138 | Resolved | A status older than three minutes after a failed refresh reads «آخر تحديث قبل …» (D9.12). |
| 158 | Resolved | One shared schema with `editable`; the list offers it and lands the overview's «عرض الكل» (D1.17, D6.4). |
| 160 | Resolved | A visit's check-in takes `customerId`; «تسجيل كزيارة» sends it (D2.7, D7.3). |
| 162 | Resolved | The statement names who recorded and who voided each payment, and the file shows them (D2.9, D8.3). |
| 163 | Resolved | The subscription's card offers «تصحيح الاشتراك» on the routes as they are (D8.4). |
| 164 | Resolved | `GET …/written-off-visits` lists them; the desk's «لن تُحصَّل» view offers their undo (D2.10, D7.2). |
| 165 | Resolved | `SPACE_NAV` and `ADMIN_NAV` carry their groups; the sidebar draws them, labels hidden on the rail (D0.3). |
| 166 | Resolved | The ledger's staff filter names the space's other owners from the managed space read (D8.7). |
| 168 | Resolved | The held action is kept 15 minutes in the browser's storage and run only after a sign-in (D9.6). |
| 171 | Resolved | The desk sends `published.amountAgorot`; a changed price answers 409 `PUBLISHED_PRICE_CHANGED` (D0.2, D2.8, D7.4). |
| 172 | Resolved | The write-off's dialog focuses its reason on opening (D7.5). |
| 180 | Resolved | The site draws three capabilities through their `public` entries; `check:build` refuses a site page reaching the table's or the calendar's library (D4.2). |
| 184 | Resolved | The editor scrolls to and focuses the card its hash names once drawn (D6.8). |
| 187 | Accepted (owner) | No undo after «إزالة» of a space that left the directory (the owner's DI-58 (a), 2026-10-28). |
| 193 | Accepted (owner) | Finance's «غير محصّلة» stays the desk's list (equal to what the overview's tile links to); owed and uncollected are never added. |

F1's six (23, 33, 46, 64, 65, 152) stay *Open*, each gaining the line "**To the deployment item** (the owner's F1,
2026-10-29)." in its file.

---

## §8. The files (A = added, M = modified, D = deleted), by unit

Paths from the repository's root; "+test" = the test beside it (added or modified). Each unit's documents are §12's.

**U0 (lead).** M `packages/shared/src/core/{envelope.ts,errors.ts,index.ts}` +test · M
`apps/api/src/shared/errors/{appError.ts,errorHandler.ts}` +test · M `apps/web/src/shared/errors/{AppError.ts,toAppError.ts}`
(EC23: the files' names) +test · M `apps/web/src/shared/copy/{arabic,english}/{errors,dashboard,users,site,index}.ts`,
A `…/{arabic,english}/{overview,finance,audit}.ts` · M `apps/web/src/pages/dashboard/{navigation.ts,routes.tsx}`,
M `pages/dashboard/shell/{DashboardNavigation,NavigationItem,navigationIcons,DashboardLayout,TopBar,SpaceLayout,
AdminLayout}.tsx|ts` +tests, A `pages/dashboard/shell/DrawerAccount.tsx` +test · A
`pages/dashboard/space/{overview/OverviewPage,finance/FinancePage,audit/AuditPage}.tsx`, A
`pages/dashboard/admin/{overview/OverviewPage,audit/AuditPage,settings/SettingsPage}.tsx` (stubs) · A
`apps/web/src/shared/routing/focus/{SkipLink.tsx,useMainFocus.ts,firstPage.ts}` +tests, M `shared/routing/index.ts`,
D `pages/site/shell/{SkipLink.tsx,useMainFocus.ts}` (moved) · M `pages/site/shell/{SiteLayout,FocusLayout,SiteHeader,
SiteMenu}.tsx` +tests · M `pages/site/{navigation.ts,routes.tsx}`, A `pages/site/account/settings/AccountSettingsPage.tsx`
(stub) · M `features/users/components/{AccountMenuContent,AccountMenu,CompactAccountMenu}.tsx`,
`features/users/hooks/useAccount.ts` +tests · A `features/data-reports/hooks/count/{useOpenReportsCount,
useAdminReportsCount}.ts` +test, M `features/data-reports/{index.ts,hooks/queryKeys.ts}` ·
M `apps/web/src/app/pageTitles.unit.test.ts` · (if EC1) M `shared/design-system/components/navigation/Sidebar/Sidebar.tsx`.

**U1 (A1).** M `apps/api/src/modules/sessions/{tokens.ts,sessions.service.ts,sessions.repository.ts,index.ts}` +tests,
M `apps/api/src/config/env.ts` (the derived key), M `apps/api/src/app.ts` (the jobs, the key) · M
`apps/api/src/shared/rate-limit/counter.ts` (the sweep) +test · M `apps/api/src/modules/auth/{auth.service.ts,
auth.controller.ts}` +tests, M `modules/auth/email/{resetEmail.ts,resetEmail.copy.ts}` +test · M
`apps/api/src/modules/users/{users.service.ts,users.repository.ts,users.mapper.ts}` +tests · M
`apps/api/src/modules/audit/platformEvents.ts` +test · M `packages/shared/src/audit/actions.ts` · M
`packages/shared/src/auth/responses.ts`, `packages/shared/src/users/responses.ts` · M
`packages/shared/src/space-links/{requests.ts,responses.ts}` (89, 158, `addedAt`) +test · M
`apps/api/src/modules/space-links/{admin-owners/adminOwners.service.ts,admin-users/adminUsers.service.ts,
admin-spaces/listingQuery.ts,admin-spaces/adminSpaces.service.ts,staff/staff.service.ts,staff/staff.mapper.ts,
space-links.repository.ts}` +tests · M `apps/api/src/modules/spaces/space/space.api.test.ts` (78) · M
`apps/api/test/locks.ts` +test and the race tests that call it (EC9) · M `apps/api/src/shared/jobs/*` (if the sweep
needs the runner's shape).

**U2 (A2).** A `apps/api/prisma/migrations/<ts>_subscription_usage_bigint/migration.sql` (M1), A
`…/<ts>_subscription_published_period/migration.sql` (M2), M `apps/api/prisma/schema.prisma` · M
`apps/api/src/modules/subscriptions/{subscriptions.repository.ts,subscriptions.service.ts,subscriptions.mapper.ts}`
+tests · M `apps/api/src/modules/payments/{payments.repository.ts,payments.service.ts}` +tests · A
`apps/api/src/db/gazaZone.api.test.ts` · M `apps/api/src/modules/visits/{visits.service.ts,visits.repository.ts,
visits.controller.ts,visits.manage.routes.ts,visits.mapper.ts}` +tests · M
`apps/api/src/modules/desk/desk.service.ts` +tests · M `apps/api/src/shared/jobs/jobs.ts` +test · M
`apps/api/src/shared/storage/{storage.ts,localStorage.ts,cloudinaryStorage.ts}` +tests · M
`apps/api/src/modules/spaces/photos/{photos.service.ts,photos.repository.ts}` +test · M
`apps/api/src/modules/customers/{customerSearch.ts,customers.repository.ts,customers.service.ts,customers.mapper.ts}`
+tests · M `apps/api/src/modules/occupancy/{present.ts,occupancy.mapper?}` (EC24) +test · M
`apps/api/src/modules/data-reports/{data-reports.controller.ts,data-reports.service.ts,data-reports.repository.ts,
data-reports.manage.routes.ts,data-reports.admin.routes.ts}` +tests · M `apps/api/src/modules/spaces/space/
{space.service.ts,space.mapper.ts,spaceView.ts}` +tests · M `packages/shared/src/{visits,subscriptions,payments,desk,
customers,occupancy,data-reports,spaces}/{requests,responses}.ts` +tests · M `apps/api/src/db/seed/demo.ts` (EC13) ·
M `apps/api/src/app.ts` (the reclaim job — integrated with U1's change by the lead).

**U3 (L).** A `apps/web/src/shared/design-system/components/display/Meter/{Meter.tsx,index.ts}`,
`…/data/BarChart/`, `…/data/Heatmap/`, `…/feedback/Refreshing/` +tests · M `…/actions/DropdownMenu/DropdownMenu.tsx`,
`…/fields/Input/Input.tsx`, `…/data/DataTable/DataTable.tsx` +tests · M `shared/design-system/index.ts`,
`tokens/{semantic.css,tailwind.css}` (component tokens) · A `pages/showcase/sections/{display/MeterSection,
data/ChartsSection,feedback/RefreshingSection}.tsx`, M `pages/showcase/registry.tsx` · A
`apps/web/src/shared/lib/numbers/westernDigits.ts`, `shared/lib/csv/{csvOf.ts,downloadFile.ts}`,
`shared/lib/phone/whatsappLink.ts` +tests, M `shared/lib/index.ts`, M the five digit helpers (`wholeNumber.ts`,
`features/packages/services/packageValues.ts`, `features/spaces/services/clockTime.ts`, `shared/lib/money/shekels.ts`,
`shared/map/services/coordinates.ts`) · M `packages/shared/src/space-settings/reminderTemplate.ts` (`fillReminder`)
+test, M `features/space-settings/services/reminderPreview.ts` · A `shared/lists/hooks/useRowTriggers.ts` (moved),
`shared/lists/services/rangeSummary.ts` +tests, M `shared/lists/{services/paginationView.ts,
components/ListPagination.tsx,index.ts}` +tests, D `features/staff/hooks/menu/useMenuTriggers.ts`,
`pages/dashboard/admin/useRowTriggers.ts` · M `shared/copy/{arabic,english}/forms.ts` (the range words).

**U4 (T).** M `apps/web/vite.config.ts`, `apps/web/scripts/{checkBuild.ts,checkBuild.unit.test.ts}` · A
`apps/web/src/features/{data-reports,announcements,platform-settings}/public.ts`, M their `index.ts` · M every
`pages/site/**` import of those three · M `eslint.config.js` · A `apps/web/test/warmLazy.ts` +test, M the six route
test files (EC15) · M `docker-compose.yml`, D `docker/postgres/create-test-database.sql` · M
`docs/development/setup.md`, `docs/architecture/documentation.md` (OD4).

**U5 (W1).** A `apps/web/src/features/overview/**` (repository, hooks, components, services; +tests) · A
`apps/web/src/features/finance/**` (+tests) · M `pages/dashboard/space/overview/OverviewPage.tsx`,
`pages/dashboard/space/finance/FinancePage.tsx`, `pages/dashboard/admin/overview/OverviewPage.tsx` +tests · M
`features/staff/{components/StaffList.tsx,hooks/access/useStaffActions.ts,components/StaffActionsMenu.tsx,index.ts}`
+tests, M `pages/dashboard/space/StaffPage.tsx` · M `pages/dashboard/space/SettingsPage.tsx` · M
`features/packages/components/{list/PackageRow.tsx,sheet/PackageSheet.tsx}`, `pages/dashboard/space/PackagesPage.tsx`
+tests · M `features/space-settings/components/reminder/ReminderCard.tsx` +test · M
`shared/copy/{arabic,english}/{overview,finance,staff,packages,spaceSettings}.ts`.

**U6 (W2).** A `apps/web/src/features/audit/**` (+tests) · M `pages/dashboard/space/audit/AuditPage.tsx`,
`pages/dashboard/admin/audit/AuditPage.tsx` · A `features/platform-settings/{repository,hooks/admin,components/admin}/**`
+tests, M `features/platform-settings/{services/platformContact.ts,components/PlatformContact.tsx,index.ts,public.ts}`,
M `apps/web/.env.example` · M `pages/dashboard/admin/settings/SettingsPage.tsx` · M
`features/space-links/{services/filtersOf.ts,components/admin-list/FiltersSheet.tsx,components/owners-list/OwnersList.tsx,
components/users-list/UsersList.tsx,components/ListState.tsx,hooks/add-owner/{useEmailAccount.ts,useAddOwnerForm.ts},
components/add-owner/*,components/link/*,hooks/link/*,services/userRowView.ts}` +tests · M
`features/spaces/{components/menu/SpaceActionsMenu.tsx,hooks/hide/useSetSpaceHidden.ts,components/editor/{SpaceEditor,
SectionCard,VerifiedNotice}.tsx,hooks/editor/useHashLanding.ts (A),components/gallery/*}` +tests · A
`features/data-reports/{components/notice/ReportNotice.tsx,hooks/notice/useReportNotice.ts}` +tests, M
`features/data-reports/{services/reportsQueryOf.ts,services/adminReportsQueryOf.ts,hooks/decide/useDecideSheet.ts,
repository/*}` +tests · M `pages/dashboard/{fieldSections.ts,space/ProfilePage.tsx,space/PackagesPage.tsx,
space/reports/DataReportsPage.tsx,admin/{SpaceEditPage,SpacesPage,OwnersPage,UsersPage,DataReportsPage,LookupsPage,
MenuActionItem,UserActionsMenu}.tsx}` · M `features/lookups/components/{sheet/LookupForm.tsx,sheet/AmenityForm.tsx,
*/AmenitiesField*.tsx}` +tests · M `shared/copy/{arabic,english}/{audit,platformSettings,spaceLinks,spaces,
dataReports,lookups}.ts` · M `docs/design/prototype/Admin space edit.html` (74).

**U7 (W3a).** M `features/desk/**` — A `components/log/`, `hooks/log/`, `services/logRows.ts`,
`components/written-off/`, `hooks/written-off/`, `components/usage-out/`; M `components/{present,uncollected,
search,check-out,subscriber,visit,write-off,money,sheet,pay,collect,debt}/**`, `hooks/{…}`, `repository/deskRepository.ts`
+tests · M `features/occupancy/components/LiveStatusControl.tsx`, `features/occupancy/hooks/usePresentList.ts` (EC24)
+tests · M `pages/dashboard/space/desk/DeskPage.tsx`, `pages/dashboard/space/SubscriptionSheetSlot.tsx` · M
`shared/copy/{arabic,english}/{desk,occupancy}.ts`.

**U8 (W3b).** A `features/desk/{components/customer-actions,hooks/customer-actions,components/correct,hooks/correct}/**`
+tests · M `features/desk/components/{customers,file,menu,statement}/**`, `hooks/{customers,file}/**`,
`services/customersQueryOf.ts` +tests · M `features/payments/components/{ledger/PaymentsLedger,mine/MyPaymentsToday}.tsx`
+tests · M `features/spaces/{hooks/owners/useSpaceOwners.ts (A),index.ts}` · M
`pages/dashboard/space/{customers/CustomersPage,customers/CustomerPage,payments/PaymentsPage}.tsx` · M
`shared/copy/{arabic,english}/{desk,payments}.ts`.

**U9 (W4).** M `features/users/**` (D9.1's moves; A `hooks/settings/*`, `components/settings/*`) +tests · M
`shared/session/{session.ts,index.ts}` (`accountEdited`) +test · M `pages/site/account/settings/AccountSettingsPage.tsx`
· M `features/auth/{hooks/google-sign-in/useGoogleSignIn.ts,hooks/sign-in/useSignIn.ts,components/forgot-password/
LinkSent.tsx,components/reset-password/ResetPasswordCard.tsx}` +tests · A `pages/site/auth/AuthWayBack.tsx`, M
`pages/site/auth/{SignInPage,RegisterPage,ForgotPasswordPage,nextSearch}.tsx|ts` +tests · M
`packages/shared/src/users/passwordPolicy.ts` +test, `shared/forms/hooks/usePasswordRules.ts` +test · A
`shared/routing/guest/heldIntent.ts` +test, M `shared/routing/guest/guestLeaving.ts`, `shared/storage/keys.ts`,
`features/{favorites,data-reports}/hooks/**` (the held actions) · M `pages/site/public/{home/*,about/AboutPage.tsx,
directory/DirectoryPage.tsx,space/SpacePage.tsx}` · M `features/directory/**` (Home's title and counts, the map view,
the results' scroll, near me, the map's marks, the space page's panel, today, location, the live line; favourites'
view; `useCachedSpaceName`) +tests · M `features/lookups/components/AreaFilter*.tsx` +test · M
`shared/map/components/{MarkerMap,MapMarkSample}.tsx` +test, `shared/design-system/leaflet.css` · M
`shared/routing/states/{RetryState,ForbiddenState}.tsx` +tests · M `pages/site/shell/SiteFooter.tsx` (carried 9) ·
M `shared/copy/{arabic,english}/{site,auth,users,directory,favorites,status}.ts`.

**U10 (lead).** M `docs/architecture/findings/README.md` and every finding file of §7 not changed in its unit
(the accepted ones; F1's six) · M `docs/plans/v1-mvp.md`, `docs/project/overview.md`,
`docs/frontend/design-system/foundation.md` (§12 rows by U3; §13 here), `docs/design/{SCREENS.md,CHANGES.md}`,
`docs/frontend/architecture.md` (§2 *Built so far*) · D `apps/web/src/pages/dashboard/PlaceholderPage.tsx` +test (EC22).

**Count:** ≈ 160 added, ≈ 250 modified, ≈ 10 deleted — **≈ 420 files**.

---

## §9. Units, commits and lanes

### §9.1 The commits (subject ≤ 50 characters, Conventional Commits; each with its tests and its documents)

**U0 — lead (first, in this order):**
- C0.1 `feat(shared): carry a refusal's details` — D0.1; T1, T2; contract §2.
- C0.2 `feat(shared): refuse a published price changed` — D0.2 (the code and its words only); T3; contract §6.
- C0.3 `feat(web): group the dashboard's navigation` — D0.3; T4–T8; architecture §2.
- C0.4 `feat(web): skip to the content in every shell` — D0.4 (with carried 1); T9–T13; architecture §2.
- C0.5 `feat(web): give the account its place on a phone` — D0.5; T14–T18; architecture §2.
- C0.6 `feat(web): route the screens still to come` — D0.6; T19.

**U1 — A1:**
- C1.1 `feat(sessions): give a replay its successor` — D1.1; T20–T22; security.md.
- C1.2 `feat(jobs): sweep expired counters and tokens` — D1.2; T23–T25; contract *Internal*, security, data-model.
- C1.3 `feat(auth): say a Google sign-in made the account` — D1.3; T26; contract.
- C1.4 `feat(auth): free an expired account's address` — D1.4; T27–T32; security, users.md, contract.
- C1.5 `feat(auth): print the reset link in the email` — D1.5; T33; (OD1's localisation.md line).
- C1.6 `feat(users): say how an account signs in` — D1.6; T34; contract *Me*.
- C1.7 `feat(space-links): name the owner in ALREADY_OWNER` — D1.7; T35; contract.
- C1.8 `feat(space-links): find an account by exact email` — D1.8; T36; contract.
- C1.9 `feat(space-links): one schema of space statuses` — D1.17 (158's shared part); T49; contract.
- C1.10 `fix(staff): keep sessions held by another link` — D1.9; T37, T38; contract, space-links.md.
- C1.11 `fix(staff): refuse an admin's account by its code` — D1.10; T39; contract.
- C1.12 `feat(staff): date each reception link` — D1.11; T40; contract.
- C1.13 `test(staff): pin three refusals and the expiry` — D1.12; T41–T44.
- C1.14 `docs(api): name the owners' type-check code` — D1.13; T45.
- C1.15 `test(api): aim the race helper at its own wait` — D1.14; T46.
- C1.16 `test(spaces): find the names' own query` — D1.15; T47.
- C1.17 `refactor(users): require the names' transaction` — D1.16; T48.

**U2 — A2:**
- C2.1 `feat(db): compute a subscription's due in bigint` — D2.1, M1; T50, T51; data-model.
- C2.2 `test(db): pin Gaza's transitions in PostgreSQL` — D2.2; T52.
- C2.3 `perf(subscriptions): bound check-ins by midnights` — D2.3; T53.
- C2.4 `fix(jobs): answer 500 when failures fill a batch` — D2.4; T54, T55; contract.
- C2.5 `feat(jobs): reclaim the files no photo holds` — D2.5; T56–T58; contract, conventions §12, spaces.md.
- C2.6 `fix(customers): match a phone under either code` — D2.6; T59, T60; contract.
- C2.7 `feat(visits): check a visit in for its customer` — D2.7; T61–T63; contract, visits.md.
- C2.8 `feat(subscriptions): refuse a changed price` — D2.8; T64, T65; contract.
- C2.9 `feat(subscriptions): name who recorded and voided` — D2.9; T66; contract.
- C2.10 `feat(visits): list a space's written-off visits` — D2.10; T67, T68; contract, visits.md.
- C2.11 `feat(db): keep a subscription's published period` — D2.11, M2; T69–T71; contract, data-model.
- C2.12 `feat(customers): carry the reminder in the file` — D2.12; T72; contract.
- C2.13 `feat(desk): say more of who is there and of plans` — D2.13; T73, T74; contract.
- C2.14 `feat(data-reports): read one report by its id` — D2.14; T75, T76; contract.
- C2.15 `feat(spaces): name the retired amenities held` — D2.15; T77; contract.

**U3 — L:**
- C3.1 `feat(design-system): add a meter` — D3.1; T80, T81; foundation §12.
- C3.2 `feat(design-system): draw bar charts and a heatmap` — D3.2; T82–T84; foundation §12.
- C3.3 `feat(design-system): reach a held menu item` — D3.3; T85, T86.
- C3.4 `feat(design-system): size a large input` — D3.4; T87.
- C3.5 `feat(lists): show a list's range and its steps` — D3.5; T88, T89.
- C3.6 `feat(lists): mark the page asked while it loads` — D3.6; T90, T91.
- C3.7 `fix(lists): keep the scroll on a page change` — D3.10 (carried 11, its `shared/lists` part); T95.
- C3.8 `refactor(lib): read Arabic-Indic digits once` — D3.7; T92.
- C3.9 `refactor(lists): share the row menus' triggers` — D3.8; T93.
- C3.10 `feat(lib): build a CSV and a WhatsApp link` — D3.9, D3.11; T94, T79.

**U4 — T:**
- C4.1 `build(web): serve the site's parts by their entry` — D4.2 (first: the other lanes then import the entries);
  T98, T99; architecture §3.
- C4.2 `build(web): keep dashboard-only code acyclic` — D4.1; T96, T97.
- C4.3 `test(web): load the lazy shells before waiting` — D4.3; T100.
- C4.4 `build(db): hold the test database's script inline` — D4.4; setup.md.
- C4.5 `docs: settle the capability documents' size` — D4.5 / OD4.

**U5 — W1:**
- C5.1 `feat(overview): show the owner's work queue` — D5.1; T110–T116; overview.md (the feature's web part).
- C5.2 `feat(overview): show the platform at a glance` — D5.2; T117–T120.
- C5.3 `feat(finance): show a month's income` — D5.3; T121–T127; finance.md.
- C5.4 `feat(finance): show who owes and who paid` — D5.4; T128–T133.
- C5.5 `feat(finance): show the space's occupancy` — D5.5; T134–T137.
- C5.6 `feat(staff): show each person's month and start` — D5.6; T138–T140; space-links.md.
- C5.7 `feat(space-settings): link the personal settings` — D5.7; T141; space-settings.md.
- C5.8 `fix(packages): say the desk sells these prices` — D5.8; T142; packages.md.
- C5.9 `fix(packages): announce the terms, not the name` — D5.9; T143.
- C5.10 `fix(staff): word both cases and name the tokens` — D5.10; T144, T145.
- C5.11 `fix(staff): reach the held item by the keyboard` — D5.11; T146.

**U6 — W2:**
- C6.1 `feat(audit): show a space's audit log` — D6.1 (feature + the owner's page); T150–T155; audit.md.
- C6.2 `feat(audit): show the platform's audit log` — D6.1 (the admin's page); T156–T158.
- C6.3 `feat(platform-settings): edit the settings` — D6.2; T159–T163; platform-settings.md.
- C6.4 `feat(platform-settings): read the public contact` — D6.3; T164, T165; architecture §3.
- C6.5 `feat(space-links): land the spaces the admin keeps` — D6.4; T166.
- C6.6 `feat(space-links): link the owner a refusal names` — D6.5 (83); T167.
- C6.7 `fix(space-links): read the email's account exactly` — D6.5 (89); T168, T169.
- C6.8 `fix(space-links): name a person's front desks` — D6.6; T170.
- C6.9 `fix(space-links): word a link from a fresh read` — D6.7; T171.
- C6.10 `feat(data-reports): open a report beside its field` — D6.8; T172–T177; data-reports.md, spaces.md.
- C6.11 `feat(data-reports): filter by who handles them` — D6.9; T178.
- C6.12 `fix(spaces): finish the spaces list and editor` — D6.10; T179–T182.
- C6.13 `fix(space-links): finish the owners and users` — D6.11; T183, T184.
- C6.14 `fix(lookups): keep switches in rows, add positions` — D6.12; T185–T187; lookups.md.
- C6.15 `feat(lookups): name the retired amenities kept` — D6.13; T188.
- C6.16 `feat(spaces): show a photo's upload as a bar` — D6.14; T189; prototype, CHANGES.md.
- C6.17 `fix(admin): reach a held user action by keyboard` — D6.15; T190.

**U7 — W3a:**
- C7.1 `fix(desk): focus the write-off's reason first` — D7.5 (first: red test); T209.
- C7.2 `feat(desk): show a day's log beside who is here` — D7.1; T200–T203; desk.md.
- C7.3 `feat(desk): list and undo the written-off visits` — D7.2; T204–T206.
- C7.4 `feat(desk): check a customer in as their visit` — D7.3; T207.
- C7.5 `feat(desk): send the price the sheet showed` — D7.4; T208.
- C7.6 `fix(desk): order the phone's desk and its states` — D7.6; T210, T211.
- C7.7 `feat(desk): link names and word who is here` — D7.7; T212, T213.
- C7.8 `feat(desk): renew or subscribe from the desk` — D7.8; T214, T215.
- C7.9 `fix(desk): count a full space and show the rates` — D7.9; T216–T218.
- C7.10 `feat(desk): name the file a phone adds to` — D7.10; T219.
- C7.11 `fix(desk): say a refused payment recorded nothing` — D7.11; T220.
- C7.12 `feat(desk): say a usage subscriber's due at out` — D7.12; T221, T222.
- C7.13 `fix(desk): finish the subscription sheet` — D7.13; T223–T225.
- C7.14 `docs(visits): name the desk's screen` — D7.14.

**U8 — W3b:**
- C8.1 `feat(desk): offer a customer's actions by state` — D8.1; T230–T232; desk.md.
- C8.2 `feat(desk): remind a customer on WhatsApp` — D8.2; T233.
- C8.3 `feat(desk): name who recorded and voided` — D8.3; T234.
- C8.4 `feat(desk): correct a subscription from its card` — D8.4; T235–T238; subscriptions.md.
- C8.5 `feat(desk): filter customers by week and month` — D8.5; T239.
- C8.6 `fix(desk): finish the customers list and file` — D8.6; T240–T243.
- C8.7 `feat(payments): name the space's other owners` — D8.7; T244; payments.md.

**U9 — W4:**
- C9.1 `refactor(users): one folder per operation` — D9.1 (no behaviour change).
- C9.2 `feat(users): edit one's own account` — D9.2; T250–T256; users.md.
- C9.3 `feat(auth): welcome a first Google sign-in` — D9.3; T257, T258; auth.md.
- C9.4 `fix(auth): keep next and the way back` — D9.4; T259–T264.
- C9.5 `feat(forms): say when a password is too long` — D9.5; T265, T266.
- C9.6 `feat(auth): keep a guest's action through a reset` — D9.6; T267–T270; architecture §4.
- C9.7 `fix(site): announce a second retry while offline` — carried 5 (first: red test); T291.
- C9.8 `fix(site): finish Home and About` — D9.7 (carried 1's About sections focusable, 2, 3, 4, 9, 10); T271–T275.
- C9.9 `fix(directory): finish the map and the results` — D9.8; T276–T280.
- C9.10 `fix(directory): draw the marks as on light tiles` — D9.9; T281.
- C9.11 `fix(directory): wait for near me once permitted` — D9.10; T282, T283.
- C9.12 `fix(directory): hide area counts past the pins` — D9.11; T284.
- C9.13 `fix(directory): finish the space page` — D9.12 (carried 6, 7, 8a, 138); T285–T290.
- C9.14 `fix(site): retry the route and give the 403 a way` — D9.13; T292, T293.
- C9.15 `fix(favorites): show the list's line once ready` — D9.14; T294, T295.
- C9.16 `test(site): pin the footer, the areas and the pick` — D9.15 (carried 8; «بلاغاتي»'s range); T296–T298.

**U10 — lead (last):**
- C10.1 `docs: close the findings v1 resolves` — D10.1 (index, accepted findings, F1's line).
- C10.2 `docs: record every screen of v1 as built` — D10.2–D10.5.
- C10.3 `refactor(web): remove the placeholder page` — D10.4 (EC22).

**Total: 121 commits** (U0 6 · U1 17 · U2 15 · U3 10 · U4 5 · U5 11 · U6 17 · U7 14 · U8 7 · U9 16 · U10 3), each
`#PRNUM` replaced by the PR's number before the push (§12.3).

### §9.2 Dependencies — what must come first

1. **U0 before every web lane** (the routes, the navigation, the copy sections, the account menu, the shells), and
   **C0.1–C0.2 before U1 and U2** (the envelope's `details`, the new code).
2. **C4.1 (the `public` entries) early in U4**, before U6 edits `platform-settings`' and `data-reports`' entries and
   U9 the site's imports; the lead merges U4's C4.1 right after U0.
3. **U3's C3.1–C3.2 (meter, charts)** before U5's C5.1 (meter) and C5.3–C5.5 (charts); **C3.3** before C5.11 and
   C6.17; **C3.5–C3.6** before U8's and U9's lists; **C3.9** before C5.3's export; **C3.10** (`fillReminder`,
   `whatsappLink`) before C5.4 and C8.2; **C3.4** before C7.11.
4. **U1 → U6 and U9:** C1.7 → C6.6; C1.8 → C6.7; C1.9 → C6.5; C1.6 → C9.2; C1.3 → C9.3; C1.12 → C5.6.
5. **U2 → U5, U6, U7, U8:** C2.7 → C7.4; C2.8 → C7.5; C2.9 → C8.3; C2.10 → C7.3; C2.11 → C8.5; C2.12 → C8.2;
   C2.13 → C7.7, C7.8; C2.14 → C6.10; C2.15 → C6.15.
6. **Within U7 and U8** (both in `features/desk`): U7 first through C7.1, then both run; each keeps to its own folders
   and its own sub-objects of `desk.ts`'s copy (§9.3).
7. **U10 last**, after every lane is merged and green.

A web commit that needs an API change codes against its shared types once the API lane's shared commit is merged into
the PR branch; until then the web lane works on its other commits (the order in §9.1 puts the independent ones first).

### §9.3 The shared files, and how lanes add to them without colliding

| File | Who changes it | The rule |
|---|---|---|
| `pages/dashboard/routes.tsx`, `navigation.ts`, `pages/site/routes.tsx`, `navigation.ts` | U0 only | every route exists after U0; lanes fill their page files |
| `shared/copy/{arabic,english}/index.ts`, `shape.ts` | U0 only | the three new sections registered empty |
| a section file (`desk.ts`, `site.ts`, …) | its lane(s) | each lane edits only its own sub-objects; `desk.ts` is U7's (`page`, `log`, `writtenOff`, `sheet`, `visit`, `checkOut`) and U8's (`customers`, `file`, `actions`, `correct`) |
| `shared/design-system/index.ts`, `tokens/*`, `foundation.md` §12 | U3 (and U0's EC1, U9's `leaflet.css`) | U3 lands its components first; U9's stylesheet change is its own rule block |
| `shared/lists/*`, `shared/lib/*` | U3 | other lanes only call them |
| `packages/shared/src/core/*` | U0 | — |
| `packages/shared/src/<cap>/*` | the API lane of that capability (U1: auth, users, audit, space-links; U2: the rest) | U3's `fillReminder` is the one exception (`space-settings/reminderTemplate.ts`, no API lane touches it); U9's `passwordPolicy.ts` likewise |
| `apps/api/src/app.ts` | U1 (jobs, key) and U2 (the reclaim job) | each adds its lines in its own block; the lead merges both |
| `docs/api/api-contract.md` | U0, U1, U2 | each edits only the sections of its routes; §6's codes list U0 only |
| `docs/backend/security.md` | U1 | — |
| `docs/frontend/architecture.md` | U0 (§2), U4 (§3), U6 (§3 contact), U9 (§4), U10 (§2 *Built so far*) | distinct paragraphs |
| `docs/features/<cap>.md` | the lane of that capability (S3) | `desk.md`: U7's and U8's sections apart; *History* lines added by each, conflicts resolved by the lead |
| `docs/architecture/findings/*.md` | the fixing lane (its finding's file) | the index by U10 only (S2) |
| `v1-mvp.md`, `overview.md`, `SCREENS.md`, `CHANGES.md` | U10 (CHANGES.md also U6's one row) | — |
| `eslint.config.js`, `vite.config.ts`, `checkBuild.ts` | U4 | — |

### §9.4 Lanes proposed (the execution prompt decides)

| Lane | Units | Kind | Needs |
|---|---|---|---|
| **lead** | U0, then integration, U10 | web + shared + docs | — |
| **A1** | U1 | API + shared | its own test database (`masaha_a1_test`) |
| **A2** | U2 | API + shared + migrations | its own databases (`masaha_a2_dev`, `masaha_a2_test`) |
| **L** | U3 | web layer + shared web | — |
| **T** | U4 | build, tooling, docs | C4.1 right after U0 |
| **W1** | U5 | web | U3's C3.1–C3.2, C3.9, C3.10 |
| **W2** | U6 | web | U1's C1.7–C1.9, U2's C2.14–C2.15, U4's C4.1 |
| **W3** | U7 then U8 (one lane, `features/desk`) | web | U2's desk commits |
| **W4** | U9 | web | U1's C1.3, C1.6; U3's lists; U4's C4.1 |

**Proposed: 8 lanes and the lead, at most 6 running at once** (two API lanes' full test runs fit beside the web
lanes' unit runs; a third full `test:api` waits — the memory rule): first U0 (lead) and U1, U2 (start at once after
C0.2), L, T; then W1, W2, W3, W4 as their needs land. Every lane: its commits red-then-green where a fix has a test
(S9), its touched tests while working, its lane's full test file set before handing back; the lead runs the complete
verification (§10.5) on the integrated branch.

### §9.5 The autonomy rule (copied from the owner's practice in #131)

No stop until ready for review; each "stop and ask" of this plan becomes *decide, record under "Decisions taken without
the owner" in the report, continue* — within the hard limits: never a change on the *Not in v1* list, never a migration
not named here (M1, M2), never a force-push of `main`, never a merge. No stop for the file count.

---

## §10. Tests

Each: **T#** · lane (`unit` = `*.unit.test.ts`, `comp` = `*.component.test.tsx`, `api` = `*.api.test.ts`) · its
title · **B#**, the break that must turn it red. A test is written red first (S9) and its break run once by the
executor (each break is a temporary edit, reverted; the report lists them).

### §10.1 U0
- T1 api · "a refusal that names a record carries its details in the envelope" — B1: the handler drops `details`.
- T2 unit (web) · "toAppError keeps an envelope's details" — B2: `toAppError` ignores `error.details`.
- T3 unit · "both catalogues word PUBLISHED_PRICE_CHANGED" — B3: the Arabic line removed (the parity test).
- T4 comp · "the owner's sidebar draws five groups with their labels, the overview first" — B4: one flat group.
- T5 comp · "reception's four pages are drawn without group labels" — B5: `grouped` always true.
- T6 comp · "on the rail the group labels are read, not shown" — B6: the label without its rail rule.
- T7 comp · "the owner's «سجل التدقيق» sits under «الفريق والإعدادات», reception never has it" — B7: roles `BOTH`.
- T8 comp · "the data reports item shows the open reports' count, named «بلاغات جديدة»; none at zero" — B8: the badge
  drawn at 0.
- T9 comp · "the first page keeps the focus where it is, also after a guard's replace" — B9: the flag never set.
- T10 comp · "a later page moves the focus to main, in the dashboard too" — B10: `useMainFocus` not mounted in
  `DashboardLayout`.
- T11 comp · "Back from the focus shell focuses the site's main" — B11: a pop treated as a load.
- T12 comp · "a hash naming a section focuses its heading, also when only the hash changes (/about#owners)" — B12: the
  old rule (main on a path change only).
- T13 comp · "each shell's first focusable is «تخطَّ إلى المحتوى», leading to main" — B13: `SkipLink` after the header.
- T14 comp · "on a phone the dashboard's bar holds no avatar or theme; the drawer opens with the account" — B14: the
  avatar left in the bar.
- T15 comp · "the drawer's foot holds the language and the theme below 768" — B15: the theme removed from the foot.
- T16 comp · "the dashboard's account menu offers «الموقع العام» and «إعدادات حسابي», not «لوحة التحكم»" — B16: the site's
  items.
- T17 comp · "the account menu's label names the role at the space" — B17: no role passed.
- T18 comp · "on a phone the site header shows the language and the avatar; the theme is in the menu" — B18: the theme
  in the header.
- T19 unit · "every page has a title in each language" (extended to the new routes) — B19: a new route without a handle.

### §10.2 U1
- T20 api · "a token presented twice within the grace gets one successor, the same token" — B20: `newToken()` for the
  successor.
- T21 api · "a replay after the grace ends the session" (kept) — B21: the grace check removed.
- T22 unit · "the successor key is derived from the secret and its label" — B22: the label dropped (another key).
- T23 api · "a sweep deletes expired refresh tokens and sessions past their end, keeping live ones" — B23: `<=`
  becomes `<` on `session_ends_at`.
- T24 api · "a sweep deletes expired reset tokens and recoveries" — B24: the recoveries' delete removed.
- T25 api · "a sweep deletes ended rate-limit windows, at most 5,000 a run" — B25: no `LIMIT`.
- T26 api · "Google's answer says created for a new account, not for a linked one" — B26: `created` always false.
- T27 api · "registering an expired pending account's address replaces it and creates the new one" — B27: the step
  removed (`EMAIL_TAKEN`).
- T28 api · "the replaced account loses its links and sessions, is suspended, and its email freed" — B28: the links kept.
- T29 api · "an account that acted, or owns a space, is not replaced" — B29: the footprint check removed.
- T30 api · "a pending account not yet expired is not replaced" — B30: the expiry check removed.
- T31 api · "Google's first sign-in at such an address replaces it, answering created" — B31: Google path not wired.
- T32 api · "the replacement is audited user.replaced, and the space's log shows the link ended by no one" — B32: no
  entry.
- T33 unit · "the reset email holds the link as text in both parts and languages" — B33: the text part without it.
- T34 api · "GET /me answers hasPassword and hasGoogle" — B34: `hasGoogle` from the password.
- T35 api · "ALREADY_OWNER carries the owner's id" — B35: no details.
- T36 api · "the users list's email filter keeps the exact account only" — B36: `email` read as `q` (contains).
- T37 api · "deactivating a link of a person with another active link keeps their sessions" — B37: `endSessions`
  always.
- T38 api · "deactivating a person's last link ends their sessions" (kept) — B38: `endSessions` never.
- T39 api · "the re-issue refuses an admin's account with ACCOUNT_IS_ADMIN" — B39: the admin check after the links'.
- T40 api · "a staff member is answered with the date their link was made" — B40: `updatedAt` instead.
- T41 api · "the re-issue refuses an OWNER-role account with no link here: ACCOUNT_HAS_LINKS" — B41: `role !== 'USER'`
  removed.
- T42 api · "the re-issue and the handover answer 404 for a deactivated reception link" — B42: the active check removed.
- T43 api · "a re-activation refuses an admin: ACCOUNT_IS_ADMIN" — B43: the check removed.
- T44 api · "a temporary password that expires between the check and the lock is refused at confirm" — B44: the second
  check removed.
- T45 api · "the add-owner names invalid_format for a string id and invalid_choice for a deleted space" — B45: the
  schema coerces.
- T46 unit · "waitingOnLock needs its table, and counts only that table's waiters" — B46: `on` optional again.
- T47 api · "the owners' names are read on the read's own connection" (by the statement) — B47: the names read on
  another connection.
- T48 unit · (typecheck) "namesFor without its transaction does not compile" (`@ts-expect-error`) — B48: `tx?` again.
- T49 unit · "the spaces list's schema takes editable and the five others" — B49: `editable` removed.

### §10.3 U2
- T50 api · "a per-day subscription's due past the integer's range is answered exactly" — B50: M1's `bigint` back to
  `integer`.
- T51 api · "the customers list answers with such a subscription" (no 500) — B51: the mapper without `Number()`.
- T52 api · "PostgreSQL's Gaza date equals Node's around every 2026 transition" — B52: the zone name changed in the
  query.
- T53 api · "the dated check-ins' first and last Gaza day are both in, the day after out" (kept) + "the plan is an index
  range" — B53: the midnight off by an hour.
- T54 api · "a run whose failures fill the batch answers 500" — B54: `stalled` never set.
- T55 unit · "a run with one stalled job still runs the others" — B55: the runner stops at the first.
- T56 unit · "the local store lists its files under a prefix with their dates" — B56: the prefix ignored.
- T57 unit · "Cloudinary's listing follows next_cursor and maps public ids to keys" — B57: one page only.
- T58 api · "the reclaim removes only files no row holds and older than an hour, in its hour" — B58: the age check removed.
- T59 api · "+970… typed finds a phone stored as +972…" — B59: the trunk rule back.
- T60 api · "+972… typed finds +970…" — B60: as B59.
- T61 api · "a visit checked in with customerId is that customer's" — B61: the id ignored.
- T62 api · "an archived customer's visit check-in is refused CUSTOMER_ARCHIVED" — B62: the check removed.
- T63 api · "a present customer's visit check-in is refused MEMBER_ALREADY_CHECKED_IN" — B63: the check removed.
- T64 api · "a published amount that differs answers PUBLISHED_PRICE_CHANGED, writing nothing" — B64: the comparison
  removed.
- T65 api · "an equal amount, or none, subscribes as before" — B65: an absent amount refused.
- T66 api · "the statement names who recorded and who voided each payment" — B66: `voided.by` without its name.
- T67 api · "the written-off list names who wrote off, the amount and the reason, newest first" — B67: oldest first.
- T68 api · "reception is refused the written-off list before the query" — B68: the `can()` removed.
- T69 api · "a subscription sold from a month's price is filtered MONTH, a custom one CUSTOM" — B69: `published_period`
  not set.
- T70 unit · "the customers query takes WEEK and MONTH" — B70: the enum unchanged.
- T71 api · "the database refuses a published period with a package" — B71: M2's CHECK removed.
- T72 api · "the customer's file carries the space's reminder, null for the default" — B72: the field always null.
- T73 api · "a present student visit says its audience" — B73: the field dropped.
- T74 api · "a customer row's current subscription carries its progress" — B74: progress omitted.
- T75 api · "the owner reads one report by its id; another space's is 404" — B75: the space check removed.
- T76 api · "the admin reads one report by its id" — B76: the route not mounted.
- T77 api · "a space's read names its retired amenities" — B77: inactive ones filtered out.

### §10.4 U3–U9 (web)
- T79 unit · "whatsappLink makes a wa.me link of a phone's digits with the text encoded" — B79: the `+` kept.
- T80 comp · "Meter is a named meter with its value" — B80: `role` missing.
- T81 comp · "Meter as progress is a progressbar" — B81: the kind ignored.
- T82 comp · "BarChart's hidden table holds every value of every series" — B82: the table without the second series.
- T83 comp · "BarChart draws a legend only for more than one series" — B83: always.
- T84 comp · "Heatmap's table holds every cell, its caption the unit" — B84: a row skipped.
- T85 comp · "a held item is reached by the arrow keys and typeahead, its reason read" — B85: `disabled` instead.
- T86 comp · "selecting a held item does nothing" — B86: `onSelect` not prevented.
- T87 comp · "Input size lg is the large control" — B87: the size ignored.
- T88 unit · "rangeSummary says 1–20 of 312" — B88: off by one.
- T89 comp · "a one-page list keeps its steps, both disabled" — B89: `null` at one page.
- T90 comp · "a tap on page 2 marks it current at once and dims the rows until it arrives" — B90: the answer's page.
- T91 comp · "Refreshing marks its list busy and dimmed" — B91: no `aria-busy`.
- T92 unit · "toWesternDigits reads both Arabic-Indic sets" — B92: the extended set dropped.
- T93 comp · "the row's trigger takes the focus back when its dialog closes" (moved) — B93: the trigger not registered.
- T94 unit · "csvOf quotes commas, quotes and line breaks, and starts with a BOM" — B94: no doubling of `"`.
- T95 comp · "a page link keeps the scroll where it is" — B95: no `preventScrollReset`.
- T96 unit · "check:build refuses a chunk the dashboard imports that imports it back" — B96: the rule removed.
- T97 (build) · `check:build` passes on the PR's build (CI) — B97: the group removed (the cycle returns, EC5).
- T98 unit · "check:build refuses a site page reaching data-table or calendar" — B98: the rule removed.
- T99 (build) · the PR's build passes it — B99: the space page importing `@features/data-reports` again.
- T100 unit · "warm awaits every loader once" — B100: not awaited.
- T110 comp · "the overview shows no amount anywhere" — B110: a debt amount rendered (a fixture's `owed`).
- T111 comp · "the attention rows come in order, each with its link" — B111: two rows swapped.
- T112 comp · "a stale group says its days with the right plural (2 → «قبل يومين»)" — B112: `other` always.
- T113 comp · "nothing to attend: «كل شيء على ما يرام»" — B113: the card empty.
- T114 comp · "present now shows the meter and the ratio only with a capacity" — B114: the meter without one.
- T115 comp · "ending soon lists five, «ينتهي غدًا», and «عرض الكل»" — B115: six listed.
- T116 comp · "a failure offers «إعادة المحاولة»; reception gets the 403" — B116: the retry not wired.
- T117 comp · "the admin's five tiles, each a link with its helper" — B117: the new users tile missing.
- T118 comp · "the completeness card lists five, missing as warning, and «عرض الكل (n)» to editable&stale" — B118:
  `destructive`.
- T119 comp · "«عرض الكل» lands on ?status=editable&stale=true" — B119: `stale=1`.
- T120 comp · "the privacy note is shown" — B120: removed.
- T121 unit · "months lists the current Gaza month and the 23 before it" — B121: 24 before.
- T122 unit · "the month's helper says +12% vs the month before, none when it had none" — B122: divide by zero shown.
- T123 comp · "income's three tiles, two charts and the collections table" — B123: the all-time tile reads the month.
- T124 comp · "the month in the address changes every month-bound block, not the fixed windows" — B124: the 30 days
  re-read by month.
- T125 unit · "the income CSV has one row per month in shekels with a dot" — B125: agorot written.
- T126 comp · "the export downloads and says «نُزّل الملف»" — B126: no toast.
- T127 comp · "reception gets the 403 on finance" — B127: the route's roles `BOTH`.
- T128 comp · "debts' four tiles, the uncollected one linking to the desk and not added" — B128: owed + uncollected
  summed.
- T129 comp · "a debtor row: since, oldest item, the amount, WhatsApp only with a phone" — B129: WhatsApp without a
  phone.
- T130 unit · "the reminder is filled with the first name, the amount and the space" — B130: the full name.
- T131 comp · "the debts' CSV reads every page before saving" — B131: the first page only.
- T132 comp · "a failed page of the export saves nothing and offers a retry" — B132: a partial file saved.
- T133 comp · "paid in the month: five, «عرض الكل» to the ledger's range" — B133: a range past the month.
- T134 unit · "stayText writes 252 minutes as 4:12" — B134: minutes as decimals.
- T135 comp · "the heatmap leaves out the weekdays and hours with no presence" — B135: all 24 hours.
- T136 comp · "occupancy's nulls show «—» and their line" — B136: «0».
- T137 unit · "the occupancy CSV has a row per weekday with 24 values" — B137: 23 values.
- T138 comp · "staff shows «أُضيف في» and «مقبوضاته هذا الشهر», a link to the ledger" — B138: the collections not
  matched by id.
- T139 comp · "a failed collections read shows «—»" — B139: «0 ₪».
- T140 comp · "the menu's «عرض مقبوضاته» opens the ledger for that person" — B140: the item missing.
- T141 comp · "settings' «حسابي» card links /me; the helpers' new words" — B141: the card missing.
- T142 comp · "Packages & prices shows the desk's five lines and the row's price at its end" — B142: a line missing.
- T143 comp · "typing the package's name changes nothing in the live region" — B143: the name inside it.
- T144 comp · "the re-issue's ACCOUNT_IS_ADMIN reads as an admin's account" — B144: the links line.
- T145 comp · "the insert buttons are named with their tokens" — B145: «إدراج الاسم».
- T146 comp · "the staff menu's held item is reached by the keyboard" — B146: `disabled`.
- T150 unit · "every AUDIT_ACTIONS action has a word in both languages" — B150: one removed.
- T151 unit · "each group holds at most 30 actions, each known" — B151: a group of 31.
- T152 unit · "detailsOf words a void's amount, method and reason" — B152: the reason dropped.
- T153 comp · "the owner's log: Masaha as «فريق مساحة», the system as «النظام»" — B153: the admin named.
- T154 comp · "the actor filter shows only with more than one actor" — B154: always.
- T155 comp · "a void, a staff deactivation, an extension and a photo removal are red; the rest neutral" — B155: all
  neutral.
- T156 comp · "the admin's log names the entry's space under the target" — B156: omitted.
- T157 comp · "a deleted target is marked and not a link" — B157: linked.
- T158 comp · "the filters are in the address and survive a reload" — B158: state only.
- T159 comp · "each settings card loads, saves and fails on its own" — B159: one shared error.
- T160 comp · "an empty contact field sends null" — B160: an empty string.
- T161 comp · "freshness refuses 0 and 366 with its words" — B161: no bound.
- T162 comp · "the rounding minutes field shows only for «تقريب لأعلى…»" — B162: always.
- T163 comp · "«تغييرات غير محفوظة» and «تجاهل التغييرات» while a card differs" — B163: the badge never.
- T164 comp · "the site's contact comes from GET /settings/public" — B164: the env read.
- T165 comp · "no contact set: the caller's line" — B165: nothing drawn.
- T166 comp · "?status=editable selects «تعدّلها الإدارة»" — B166: falls back to all.
- T167 comp · "ALREADY_OWNER offers «اربطه بالمساحة» opening the link dialog for that owner" — B167: the old line.
- T168 comp · "an exact email is found even beyond the first page" — B168: `q` read.
- T169 comp · "a failed read says so and retries" — B169: `notFound`.
- T170 comp · "a receptionist's option reads «مستخدم · استقبال {spaces}»" — B170: «مستخدم».
- T171 comp · "a space linked meanwhile is worded as another owner" — B171: the editor's read.
- T172 comp · "a report in the address shows its notice above its section" — B172: above the page.
- T173 comp · "«تم التصحيح» resolves it in place" — B173: the PATCH not sent.
- T174 comp · "the owner's notice says «زائر», the admin's the name" — B174: the owner sees a name.
- T175 comp · "«تعديل الحقل» carries ?report=" — B175: the plain link.
- T176 comp · "?open= opens that report's sheet" — B176: ignored.
- T177 comp · "the editor scrolls to and focuses the card its hash names once drawn" — B177: before the read.
- T178 comp · "«يعالجه» filters by ADMIN or OWNER; the title names the space" — B178: the chip not sent.
- T179 comp · "a verified row's menu reads «عرض (يعدّلها المالك)»" — B179: «تعديل».
- T180 comp · "hiding offers «تراجع» that shows it again" — B180: no action.
- T181 comp · "the phone's sheet closes on «عرض N نتيجة»; clear is disabled with none" — B181: enabled.
- T182 comp · "a section's header action leads its content below 768" — B182: beside the title.
- T183 comp · "?sheet=add opens the add sheet" — B183: ignored.
- T184 comp · "ACCOUNT_SUSPENDED links the users page searched by the email" — B184: plain text.
- T185 comp · "the edit sheet has no active switch" — B185: kept.
- T186 comp · "a list of 11 offers «الترتيب» and moves the row there" — B186: offered at 10.
- T187 comp · "an arrow's name holds its position; a move is announced" — B187: no live region.
- T188 comp · "the owner's checklist names a retired amenity, marked, and drops it when unticked" — B188: not listed.
- T189 comp · "an uploading tile shows a progressbar with its percentage" — B189: the spinner.
- T190 comp · "the users page's held items are reached by the keyboard" — B190: `disabled`.
- T200 unit · "logRows merges visits and check-ins latest first" — B200: visits first.
- T201 comp · "the owner's log reads a chosen day; reception's today without a picker" — B201: reception's picker.
- T202 comp · "a log row names its kind, times, duration and how it ended" — B202: the method missing.
- T203 comp · "an empty day says «لا يوجد حضور في هذا اليوم»" — B203: blank.
- T204 comp · "the owner's «لن تُحصَّل» view lists who, when, how much and why" — B204: no `writtenOffBy`.
- T205 comp · "«تراجع» undoes once and is never re-sent by itself" — B205: a key/retry added.
- T206 comp · "reception has no «لن تُحصَّل» view" — B206: shown.
- T207 comp · "«تسجيل كزيارة» sends the customer's id" — B207: by name only.
- T208 comp · "a changed price keeps the sheet open with the new amount" — B208: closes.
- T209 comp · "the write-off's dialog focuses its reason on opening" (the handler) — B209: `onOpenAutoFocus` removed.
- T210 comp · "below xl the uncollected card comes before who is here, and hides when empty" — B210: the old order.
- T211 comp · "a network failure shows the offline state" — B211: the destructive alert.
- T212 comp · "present names link to their files; a subscriber's badge is its plan's name" — B212: «اشتراك».
- T213 comp · "a student visit reads «زيارة · طالب»" — B213: «زيارة».
- T214 comp · "a search card shows its progress and «غير حاضر»" — B214: none.
- T215 comp · "«تجديد» opens the sheet to renew; the pre-check-in offers «اشتراك جديد» with none" — B215: missing.
- T216 comp · "full is by the count, not by a manual «ممتلئ»" — B216: the status.
- T217 comp · "the shift chips may be deselected; «طالب» is a switch" — B217: a select.
- T218 comp · "the check-out's line names the rate and the amount" — B218: «مدة محسوبة» only.
- T219 comp · "a known phone says «يُضاف إلى ملف {name}»" — B219: no lookup.
- T220 comp · "a 429 in a money dialog says nothing was recorded" — B220: the plain 429.
- T221 comp · "a usage-based subscriber's check-out opens the due dialog" — B221: one tap only.
- T222 comp · "a fixed subscriber stays one tap" — B222: the dialog for every one.
- T223 comp · "the sheet's dates are date pickers" — B223: native inputs.
- T224 unit · "the end note words a total and an end" — B224: always «بلا تاريخ نهاية».
- T225 comp · "the earlier debt is a warning with its calc, «المجموع»" — B225: «المستحق».
- T230 comp · "a present customer's menu offers «خروج», an owing one «استلام {amount}»" — B230: missing.
- T231 comp · "the file's header holds the state's buttons" — B231: «⋯» only.
- T232 comp · "«تجديد» only while ending soon or expired" — B232: always.
- T233 comp · "the file's reminder link holds the filled template" — B233: the default always.
- T234 comp · "a statement row says «سجّلها {name}»" — B234: none.
- T235 comp · "the correction sends only the changed fields" — B235: the whole body.
- T236 comp · "reception sees no price section" — B236: shown.
- T237 comp · "PRICE_BELOW_PAID is said in the sheet" — B237: a toast.
- T238 comp · "an ended subscription's item is held with its reason" — B238: enabled.
- T239 comp · "the type filter offers monthly and weekly first" — B239: missing.
- T240 comp · "the customers' empty state offers «زبون جديد»; the add sits by the count" — B240: the top bar.
- T241 comp · "the owner's unpaid visit offers «لن يُحصَّل…»" — B241: `more: null`.
- T242 comp · "«حاضر منذ {time}», info" — B242: «حاضر الآن».
- T243 comp · "the ledger's lists show their range" — B243: no summary.
- T244 comp · "the staff filter names the space's other owners" — B244: owner and reception only.
- T250 comp · "the profile saves the name and the menu shows it at once" — B250: the session not updated.
- T251 comp · "choosing English applies at once and saves it to the account" — B251: no PATCH.
- T252 comp · "a failed language save puts the choice back with a retry" — B252: kept.
- T253 comp · "the theme offers «حسب الجهاز», stored on the device only" — B253: sent to the API.
- T254 comp · "a Google account shows «مربوط»; a password account «تغيير»" — B254: Google from the password.
- T255 comp · "the password change closes, says it signed out the others, and focuses «تغيير»" — B255: focus lost.
- T256 comp · "a Google-only account sends the set-password link and shows its block" — B256: the change form.
- T257 comp · "a first Google sign-in is welcomed by name" — B257: no toast.
- T258 comp · "the linked toast stays until closed" — B258: 10 s.
- T259 comp · "the sign-in card's way back names the space next points to" — B259: «تصفّح المساحات».
- T260 comp · "next survives the forgot page and back" — B260: dropped.
- T261 comp · "a password sign-in toasts «أهلًا بعودتك»" — B261: none.
- T262 comp · "«استخدم بريدًا آخر» is offered on the sent step at once" — B262: only when spent.
- T263 comp · "the reset card offers «العودة إلى تسجيل الدخول»" — B263: none.
- T264 comp · "«لا يمكنك الوصول إلى بريدك؟» opens WhatsApp when set" — B264: #contact always.
- T265 unit · "the policy's fourth rule breaks past 72 bytes" — B265: counted in characters.
- T266 comp · "«طويلة جدًا — اختصرها» shows only when broken" — B266: always.
- T267 unit · "a held intent older than 15 minutes is dropped" — B267: no age check.
- T268 comp · "a favourite pressed as a guest is saved after a sign-in in a new page" — B268: memory only.
- T269 comp · "a restore never runs a held intent" — B269: any session runs it.
- T270 comp · "landing on another site page lets it go" — B270: kept.
- T271 comp · "About's note says «تواصل معنا» once, as its link" — B271: twice.
- T272 comp · "Home's title waits for its answer" — B272: from `nearest`.
- T273 comp · "the owners' card says the status shows automatically" — B273: the old words.
- T274 comp · "the search fields' maxLength is the shared constant" — B274: 80 literal.
- T275 comp · "About's verified card has its icon; its button is the primary" — B275: outline.
- T276 comp · "the map view shows its count" — B276: none.
- T277 comp · "the chosen space shows its distance with a near point" — B277: none.
- T278 comp · "the results do not scroll while the old page shows" — B278: scroll before arrival.
- T279 comp · "the place filter stops at 50 and says so" — B279: no cap.
- T280 comp · "typing in the map's search rebuilds no mark" — B280: a new `eventHandlers` each render.
- T281 unit · "inside the map, marks take the light values in dark" — B281: the rule removed.
- T282 comp · "near me's 15 s start once the permission is granted" — B282: from the press.
- T283 comp · "without the Permissions API, from the press" — B283: never starts.
- T284 comp · "truncated pins show no counts" — B284: counts shown.
- T285 comp · "the status panel is drawn with no hours and no near point" — B285: hidden.
- T286 comp · "a running closure says «مغلقة مؤقتًا اليوم»" — B286: today's hours.
- T287 comp · "the location map shows the visitor's point" — B287: none.
- T288 comp · "«الاتجاهات» is the section's action" — B288: under the address.
- T289 comp · "a status older than 3 minutes after a failure reads «آخر تحديث قبل …»" — B289: «مباشرة الآن».
- T290 comp · "the page's live badge comes from statusViewOf; the single tile names «عرض كل الصور (n)»" — B290: by hand.
- T291 comp · "a second retry while offline is announced" — B291: the same text kept.
- T292 comp · "a second general failure says «ما زال الخطأ قائمًا…»" — B292: reload.
- T293 comp · "the bare 403 offers «الرئيسية» and «تواصل معنا»" — B293: none.
- T294 comp · "favourites' line shows only once ready with spaces" — B294: while loading.
- T295 comp · "?filters=open opens the Directory's filters" — B295: ignored.
- T296 comp · "leaving a page with a bar gives the footer its room back" — B296: the cleanup removed.
- T297 comp · "«اختر منطقتك» scrolls to and focuses the areas' heading" — B297: no focus.
- T298 comp · "«حدّد موقعي على الخريطة» starts the pick on /spaces?view=map" — B298: the list view.

### §10.5 The complete verification (the lead, before the PR)

`npm ci` · `npm run format:check` · `npm run lint` · `npm run typecheck` · `npm run check:classes` · `npm run
check:links` · `npm run check:conflicts` · `npm run test:unit` · `npm run test:component` (whole) · `npm run
test:api` (whole, on the lead's test database) · `NODE_ENV=production npm run build` then `npm run check:build` ·
`node docs/design/scripts/check-parse.mjs` and `check-classes.mjs` (74's prototype edit) · the real run (§11).
Heavy runs one at a time beside at most one other (the memory); a lane killed for memory is retried once, then CI
judges.

### §10.6 Not tested, and said

- **Rendering at 390 / 768 / 1440 and in dark** — the real run's (§11), not a test lane's (jsdom has no layout).
- **Cloudinary's real listing** — mocked `fetch` only (T57); the deployment's first run shows it (EC8).
- **The 2027 transitions and beyond** — T52 pins 2026's; a new decree is a data update of both runtimes.
- **The heatmap's colours' contrast** — the layer's tokens (`primary` steps) are not in the contrast test; the real run
  looks at them in both themes.
- **A real screen reader** on the held items and the charts' tables — the tests prove the roles and names only.

### §10.7 Review focus (inputs no test exercises)

- 21: a family whose successor row was deleted between the two presentations (the second answers `invalid`).
- 91: an account replaced while its old holder is mid-request with a valid access token (refused at once by the
  session version).
- 63: a photo uploaded at 03:00 exactly (its file is younger than an hour, kept).
- 171: an owner editing prices while three desks subscribe (each compares under the lock).
- The audit's details of an action written later (unknown to `detailsOf`): no line, the action as stored.
- The finance CSV of a month with 0 payments (a header only).
- The desk's log of a day with more than 200 stays (read whole, paged in the browser).

---

## §11. The real run

**Set-up:** the web on 5320 and the API on 3320 against `masaha_dev`, seeded with `SEED_DEMO=true` (the demo space
with its owner, its reception, packages, subscriptions, visits and payments; the directory's 24 spaces); headless
Chrome over CDP (the project's script), browsing `http://localhost:5320` (never the API's port: CORS); each shot
saved, curated, never pushed. **Roles:** guest; a user (registered in the run: R1); the demo owner; the demo
reception; the seeded admin. **Variants:** Arabic light and English dark at 390, 768 and 1440 where a layout changes
(marked ◻︎ 3 widths); elsewhere 390 and 1440 in Arabic light, one English dark at 1440. **The network log** of each
case is kept; every write is named and, where it can be, put back (✎ = a write; ↺ = how it is put back; ✗ = cannot
be put back, named in the report). The dev server is stopped by PID after the run and its port checked free.

| R | Screen · role | What is looked at | Writes |
|---|---|---|---|
| R1 | 6 · guest | register a user «Run User»; the fourth rule past 72 bytes; the way back; the owner note to `#owners` | ✎ an account (✗, kept as the run's user) |
| R2 | 5 · guest | sign in with `next` from a space; «العودة إلى {space}»; `next` to the forgot page and back; «أهلًا بعودتك» | — |
| R3 | 7 · guest | forgot: «استخدم بريدًا آخر» at once; the reset card's way back; «لا يمكنك الوصول…» → WhatsApp (the seed's contact); the reset email's printed link (the log email mode) | ✎ a recovery (expires) |
| R4 | 8 · guest, user | 404; offline (the network off in CDP) and two presses announced; the general error's second line (a forced 500 via the proxy); the bare 403 at `/dashboard/admin` for the user with «الرئيسية» and «تواصل معنا» | — |
| R5 | shells · all ◻︎ | the skip link first (Tab once) in the site, the focus shell and the dashboard; the focus on `main` after a page change and on Back from sign-in; `/about#owners` focuses its heading | — |
| R6 | 1 · guest ◻︎ | phone header: language in the bar, theme in the menu, avatar once signed in; the owners' card's words; the title waits (near me via CDP's geolocation); no counts when truncated (lacks: >1,000 pins — not seen, T284) | — |
| R7 | 2 · guest ◻︎ | map view: the count, one row on a phone, the chosen space's distance; a page change with no jump; the place filter's cap (lacks: >50 areas — not reached, T279); typing on the map with CPU ×4 throttling (134's measure, 24 pins: the demo lacks 1,000) | — |
| R8 | 2 · guest, dark | the marks on the light tiles and the legend agree (135) | — |
| R9 | 3 · guest ◻︎ | the status panel always; «مغلقة مؤقتًا اليوم» (needs a running closure: R30 makes one); the visitor's point on the location map; «الاتجاهات» in the header; a refresh failing past 3 minutes (CDP offline, the clock advanced) → «آخر تحديث قبل …»; the single tile's name | — |
| R10 | 4 · guest ◻︎ | the contact from `GET /settings/public` (the network log); the note's one link; the design's sentence; the primary button full width on a phone | — |
| R11 | guest → reset | a guest's heart on a space, then a password recovered in a new tab, then signed in: the favourite saved and said (168) | ✎ a favourite ↺ removed |
| R12 | 9 · user ◻︎ | profile name saved and shown in the menu; language saved (the network shows `PATCH /me`) and its failure (CDP blocks the request) put back; the theme's three; the password change closing with its toast; | ✎ name ↺ restored; ✎ language ↺ Arabic; ✎ password ✗ (the run's user only) |
| R13 | 9 · Google-only | lacks (no Google client id locally): the Google row and the set-password link seen with a fixture account only in tests (T254, T256) | — |
| R14 | 10, 11 · user ◻︎ | favourites: the line only once ready; the empty card; «اختر منطقتك» opens the Directory's filters; «بلاغاتي»'s range | ✎ favourite ↺ |
| R15 | dashboard shells · owner, reception, admin ◻︎ | the groups and their labels; the rail at 768 (labels hidden, read by the accessibility tree); reception's four ungrouped; the drawer's account, the foot's toggles; the account menu's role, «الموقع العام», «إعدادات حسابي»; the badges | — |
| R16 | 12 · owner ◻︎ | every attention row the demo holds (the run checks which ones it lacks: a missing group — the demo's profile may hold all, then lacks; capacity set — lacks «لم تُحدَّد السعة»); present now with the meter; ending soon; **no amount anywhere** (the page's text searched for ₪); reception → the desk | — |
| R17 | 19 · owner ◻︎ | the three tabs, the month select in the address, the charts (both themes), the collections table to cards at 390, the debts' four tiles (the uncollected not added), the reminder link (opened, not sent), the three CSVs downloaded and opened (BOM, Arabic, the debts' pages); reception's 403 | ✎ none (reads only) |
| R18 | owner's audit · owner ◻︎ | the log of the run's own writes; Masaha's and the system's actors (the auto check-out's entries); the filters and the address; the red badges | — |
| R19 | 13 · reception, owner ◻︎ | the phone's order; the empty uncollected card hidden below xl; names as links; the kind badges; the log tab (owner: yesterday; reception: today only); offline state | ✎ a visit checked in and out (✗ kept: the desk's own record) |
| R20 | 13 · owner | the write-off with its reason focused (focus seen in the browser, 172), then «لن تُحصَّل» listing it, then «تراجع» | ✎ write-off ↺ undone |
| R21 | 13 · reception | «تسجيل كزيارة» for a customer with an expired subscription; the visit in their file; «تجديد» and «اشتراك جديد» from the desk; the usage-based subscriber's due dialog (the demo's usage-based subscriber, or lacks — then a custom one per hour made in R22); a known phone's «يُضاف إلى ملف» | ✎ visits ✗ kept |
| R22 | 16 · owner | the sheet's date pickers, the end note with a total, the warning for an earlier debt, the usage rate prefilled; a published price changed in another tab before confirming → the 409's line and the new amount | ✎ a subscription ✗ kept; ✎ the price ↺ restored |
| R23 | 14, 15 · owner, reception ◻︎ | the type filter (monthly from R22's sale); the row's state actions; the file's header buttons; «تذكير على واتساب» for reception (opened, not sent); «سجّلها»/«ألغاها»; «حاضر منذ»; the owner's «لن يُحصَّل…» from the file | ✎ a payment ✗ kept |
| R24 | 15 · owner | «تصحيح الاشتراك»: dates and limits saved; the price corrected with a reason; reception sees no price section; an ended one held | ✎ corrections ↺ corrected back |
| R25 | 17 · owner, reception ◻︎ | the ledger's staff filter with the other owners (lacks: the demo space has one owner — then a second owner linked by the admin in R34, ↺ unlinked); the range; the icons; «دفعاتي اليوم» | — |
| R26 | 20, 21 · owner ◻︎ | a report's notice above its section from «تعديل الحقل» (a report made by the run's user, R1), «تم التصحيح»; the scroll and focus to the card; the retired amenity listed (an amenity hidden by the admin, R35); the desk's words on Packages; the gallery's progress bar (a photo uploaded and removed) | ✎ report resolved ✗; ✎ photo ↺ removed |
| R27 | 22, 24 · owner ◻︎ | «أُضيف في», «مقبوضاته هذا الشهر» and «عرض مقبوضاته»; the held item by the keyboard; settings' «حسابي» card and helpers; the insert buttons' names | — |
| R28 | 23 · owner | `?open=` opens a report; the badge counts the open ones | — |
| R29 | 18 · owner | (no change; the shells' gaps only) | — |
| R30 | 18 · owner | a closure posted and started (for R9), then ended and deleted | ✎ ↺ deleted |
| R31 | 25 · admin ◻︎ | five tiles and their links; «اكتمال البيانات»; «عرض الكل» landing on editable & stale; the privacy note | — |
| R32 | 26 · admin ◻︎ | the verified row's «عرض»; hide with «تراجع»; delete's «رجوع»; the phone's sheet primary; «ناقصة:»; the editor's report notice; the verified notice's link; `editable` in the filter | ✎ hide ↺ shown |
| R33 | 27, 29 · admin ◻︎ | the sr-only actions header; the empty state's add (a search with no match); `?sheet=add`; ALREADY_OWNER → «اربطه بالمساحة» (the demo owner's email on another space); the exact email found; a receptionist's option «مستخدم · استقبال …»; «انضم» with its year; the held items by the keyboard | ✎ a link ↺ unlinked |
| R34 | 27 · admin | a second owner linked to the demo space for R25, then unlinked | ✎ ↺ |
| R35 | 30 · admin ◻︎ | no switch in the sheets; «الترتيب» on a governorate of more than ten areas (the seed's Gaza City); the arrows' names and the announcement; each tab's hint; an amenity hidden for R26, then shown | ✎ ↺ |
| R36 | 28 · admin ◻︎ | «يعالجه»; the title with the space; `?open=`; the badge | — |
| R37 | 31 · admin ◻︎ | the platform's log of the run's admin writes; the space under the target; no space operation listed | — |
| R38 | 32 · admin ◻︎ | each card loads and saves alone; a refusal in one card only; the unsaved badge and discard; the contact saved and seen on About (R10) | ✎ each ↺ restored |
| R39 | the build | `check:build` output: no site page reaching `data-table`/`calendar`; no cycle with `dashboard` | — |
| R40 | the database | `docker compose config` from this folder and from a second one: one configuration; `db:up` from the second leaves the container | — |

**What the demo data lacks** (never changed through the app to fake it; named in the report): over 1,000 pins (137),
over 50 areas (133), a Google account (13, 32), an expired pending account (91 — proven by T27–T31 only), a stalled
auto check-out (121), an orphan photo file older than an hour at 03:00 (63 — T58), a second owner of the demo space
(made and undone in R34).

---

## §12. Documents

### §12.1 By unit (each in the commit that changes what it describes)

- **U0:** `api-contract.md` §2 (`details`), §6 (`PUBLISHED_PRICE_CHANGED`); `frontend/architecture.md` §2 (the
  navigation's groups and badges; the skip link and the focus rule in every shell; the phone's drawer and the account
  menu; the new routes; `SkipLink`/`useMainFocus` in `shared/routing`); `localisation.md` if the role words need its
  *Formatting* line (no).
- **U1:** `api-contract.md` (*Session* › `POST /auth/google`, `POST /auth/register`; *Me*; *Staff (managed)*;
  *Owners (the admin)*; *Users (the admin)*; *Spaces (the admin)* › `status`; *Internal*); `backend/security.md`
  (*Tokens and cookies*: the successor; *Passwords*: the replacement; *Rate limits*: the sweep); `data-model.md` ›
  *Operations* (the swept rows); `features/{auth,users,space-links,audit}.md` (Behaviour, Decisions, History);
  `frontend/localisation.md` (OD1: the reset email's second home).
- **U2:** `api-contract.md` (*Front desk* › visits' `customerId`, the written-off list; *Subscriptions* ›
  `published.amountAgorot`, `publishedPeriod`; *Customers* › `q`, `kind`, `CustomerFile.reminderTemplate`,
  `CustomerRow.current`; *Occupancy* › `audience`; *Data reports* › the single reads; *Spaces (the admin)* ›
  `retiredAmenities`; `ItemPayment`; *Internal* › the stall and the reclaim); `data-model.md` (*Derived values*: the
  due in bigint; *Front desk and money*: the published period); `backend/conventions.md` §12 (the port's `list`);
  `features/{visits,subscriptions,customers,payments,desk,occupancy,data-reports,spaces}.md`.
- **U3:** `foundation.md` §12 (Meter, BarChart, Heatmap, Refreshing; DropdownMenu's `held`; Input's `size`;
  DataTable's `refreshing`); architecture §1 (`shared/lib`'s csv, digits and WhatsApp link; `shared/lists`' range,
  triggers).
- **U4:** architecture §3 (the `public` entries; `check:build`'s two rules); `development/setup.md` (*Database*,
  *Running a second folder*; the warm-up's note under *Tests*); `development/testing.md` (the warm-up); 
  `architecture/documentation.md` §5 (OD4).
- **U5:** `features/{overview,finance}.md` (their web parts: *Who uses it*, *Behaviour*, *Web decisions*, *Code map*,
  *History*); `features/{space-links,space-settings,packages}.md` (the staff columns; the account card; the desk's
  words — superseding their design issues 9, 13 and 4 with this plan's approval).
- **U6:** `features/{audit,platform-settings,space-links,spaces,data-reports,lookups}.md`; architecture §3 (the
  contact from the API); `docs/design/CHANGES.md` (74's row); the prototype `Admin space edit.html`.
- **U7, U8:** `features/{desk,visits,subscriptions,payments,occupancy}.md` (the log, the written-off view, the
  corrections, the state actions; desk DI-14 and DI-48 superseded).
- **U9:** `features/{users,auth,directory,favorites,data-reports,lookups}.md`; architecture §4 (the held intent in
  the browser's storage; `sessionStorage` not used); `features/directory.md`'s *Authority* (carried 9), `overview.md`'s
  Directory line (carried 9).
- **U10:** the findings (§7, index); `plans/v1-mvp.md` (every step *Built*; the planned surface built);
  `project/overview.md` (*Built*); `foundation.md` §13 (screen 31's line with O13; screen 24's account; screen 9's
  methods); `design/SCREENS.md`; architecture §2's *Built so far*; `README.md` (root) unchanged (it presents the
  design, never the build state).

### §12.2 `#PRNUM`

Every new dated line in a document reads "(2026-10-29, #PRNUM)" or "#PRNUM"; never in SQL. Just before the push the
lead checks the next PR number (`gh pr list --state all --limit 1`) and replaces `#PRNUM` in each commit's tree
(`git filter-branch --tree-filter` over the PR's range), then verifies none is left (`git grep '#PRNUM' HEAD`).

### §12.3 At the end

- `v1-mvp.md`: steps 1–12 each *Built* (screens included); the *Planned API surface* lists nothing planned.
- foundation §13: every screen built.
- The findings index: *Open* = 23, 33, 46, 64, 65, 152 (each with "To the deployment item"); every other finding
  *Resolved* or *Accepted*.
- `overview.md`'s *Built*: every capability's screens named.

---

## §13. Decisions needed from the owner (OD) — options and a recommendation each

- **OD1 — Finding 22, the reset email's words:** (a) move them into a catalogue both apps read (`packages/shared`) ·
  (b) accept this second home in `localisation.md`. **Rec. (b):** the web never shows them; they are held to one shape
  in both languages by their own test; moving UI words into the shared contract package mixes its roles. → 22
  *Accepted*.
- **OD2 — Finding 112, a check-out key that recorded no payment:** (a) accept the rule as it is · (b) remember every
  check-out's key (a column on visits, a third migration). **Rec. (a):** the web holds one key per intent and never
  reuses one across two visits (#117's evidence), so the case cannot arise from the desk. → *Accepted*.
- **OD3 — Finding 115, a write-off and its undo carry no key:** move it to *Accepted* — the owner's condition (no
  automatic retry) holds and is tested (test 41 of #117; D7.2's undo sends once). **Rec.:** yes.
- **OD4 — Finding 98, the capability documents' size guide:** (a) a documentation item that brings the documents back
  under 1,200 words · (b) revise the guide. **Rec. (b)**, documentation §5's sentence becomes: "A capability
  document holds the decisions as they hold today and links rather than restates; it has no word ceiling, but a part
  that a change to the capability need not read (its *History*, a superseded decision's record) moves below its
  *Code map*, so the part read before a change stays short." → 98 *Resolved* by the revision.
- **OD5 — Finding 135, the map's marks in dark:** (a) the light theme's mark values inside the map, the legend's
  samples on a light swatch · (b) keep them as they are. **Rec. (a)** (D9.9): the tiles are always light, so the
  marks must read on light.
- **OD6 — Finding 91's replacement, narrowed (S1):** (a) as S1 (only a never-used account, no owner link) · (b) the
  literal rule (any expired pending account). **Rec. (a):** (b) lets a stranger who types an owner's address retire
  that owner's account and unverify their space.
- **OD7 — G14.1, «شهري» and «أسبوعي» in the customers' filter:** (a) M2's column (D2.11) · (b) no migration: the two
  folded into one choice «من سعر معلن» derived from the absence of package and typed price · (c) record a decision that
  the filter keeps three kinds. **Rec. (a):** foundation §13 #14 names both, and only a stored period tells them
  apart.
- **OD8 — Finding 180's second entries (an architecture rule, D4.2):** a capability the site draws may have a
  `public.ts` entry beside its `index.ts`, lint allowing it as it allows the layer's entries. **Rec.:** yes — the
  layer's own precedent (45, 169).
- **OD9 — The findings index moved once at the end (S2),** overriding "in the same commit". **Rec.:** yes, for this PR
  only.
- **OD10 — Supersessions this plan makes of earlier recorded decisions** (each listed so none is silent): packages
  design issue 4 (the desk's words, D5.8); staff design issue 9 (D5.6); space-settings design issue 13 (D5.7);
  data-reports DI-39 (the handler filter, D6.9, by the mission's own words); desk DI-14 (D7.3) and DI-48 (D8.3).
  **Rec.:** approve all six.
- **OD11 — Finding 63, the reclamation job:** (a) build it (D2.5) · (b) leave it to the deployment item as "a
  measurement" (PA2). **Rec. (a):** its first option is buildable here and small.
- **OD12 — The design issues DI1–DI33** (§6): **Rec.:** each as recommended.

---

## §14. Executor checks (EC) — what to check, and what to do if it fails

- **EC1** — the layer's `SidebarGroupLabel` on the rail: is it hidden visually and kept for assistive technology? If
  not, add the rail rule in the layer (D0.3's commit).
- **EC2** — the `rate_limits` table's column that ends a window (`window_ends_at` or a start plus the policy's
  length): sweep by it; if only the start is stored, delete rows whose start is older than the longest policy window
  (24 h), and say so in security.md.
- **EC3** — how `register` meets a taken email today (a unique violation caught, or a read first): put the replacement
  check before the insert in the same transaction, under the old account's lock; if a read-then-insert race exists, the
  unique violation still answers `EMAIL_TAKEN`.
- **EC4** — the installed `@radix-ui/react-menu` equals the lockfile's: if a newer one stops skipping disabled items,
  `held` still holds (it never uses `disabled`).
- **EC5** — the code-splitting group that breaks 27's cycle: try (1) a `dashboard-shared` group with `test` matching the
  modules the dashboard alone imports (TanStack Query's `useQuery` module, `shared/routing`'s `publicSpacePath`
  file) and a priority below `dashboard`'s; (2) if Rolldown still places them in the `SpaceLayout` chunk, move the
  dashboard group's `includeDependenciesRecursively` for those named modules only. Prove it by the manifest and
  `check:build`'s cycle rule. If no option works in two hours, keep the cycle rule as a failing guard only for a
  *load-time* use (a module-level import from the cycle) and record the measured graph in the report — then 27 stays
  open with a new note (record, never silently).
- **EC6** — `docker compose version` ≥ 2.23.1 (inline `configs.content`): if older, write the script with `command`'s
  `-c` init through a one-line entrypoint, or keep the bind mount and record 48 open with the version as its cause.
- **EC7** — the existing container recreated once after D4.4: its volume and both databases (and the worktree
  databases) still there (`\l`); if not, stop and restore from the volume (it is named, never removed by `up`).
- **EC8** — Cloudinary's Admin API resource listing (fields `public_id`, `format`, `created_at`, `next_cursor`) against
  its documentation; the unit test's fixture is its documented shape. The local adapter is what the run proves.
- **EC9** — every caller of `waitingOnLock` / `whileHeld` (`git grep`): each passes its table; a race whose request
  waits on two tables names the one it is proven by.
- **EC10** — `GET /manage/spaces/:spaceId` answers `owners` to the owner (the contract says "including … active
  owners"): if it does not, 166 needs a route (`GET …/owners`, 🏢) added in U2 — decide and record.
- **EC11** — `subscription_usage`'s readers: each `due_agorot` mapped through `Number()`; no view or other function
  depends on the function (else drop and recreate it in M1).
- **EC12** — the stored `before`/`after` fields of each audit action `detailsOf` words, and the Gaza-midnight helper's
  name in `@masaha/shared/core` (finance's windows); a field that differs is read as stored and pinned by T152's
  fixtures.
- **EC13** — the demo seed's published subscriptions: set `publishedPeriod` in the seed so R23's filter has rows; if the
  seed sells none from a published price, add none (the run makes one, R22).
- **EC14** — which site pages draw a map (Directory, the space page, favourites' near me?): the `leaflet` allowance of
  D4.2's rule names exactly those.
- **EC15** — the route test files that wait for lazy shells (`git grep findBy -- '*routes*.component.test.tsx'`, the
  auth pages', `App`'s, `router`'s): each gets the warm-up.
- **EC16** — the ledger's address names for its staff and range (`ledgerQueryOf.ts`: `staff`, `from`, `to`): the
  staff page's and the payers' links use them.
- **EC17** — `staff.refusals.ACCOUNT_IS_ADMIN` exists (the re-activation's): reuse it for the re-issue, its words
  checked to fit both.
- **EC18** — `newSpaceDefaultsSchema`'s `visitRoundingMinutes` bounds and the owner's pricing card's error words: the
  admin's card uses the same bounds and words.
- **EC19** — the owners page's link dialog address (`?link=<user>&space=<id>`): if it differs, use the page's own; if the
  dialog opens only from a row, the page gains that address.
- **EC20** — the reports sheet's «عرض N نتيجة» words and forms: the spaces sheet reuses them by key.
- **EC21** — the lookups' order route body (`PUT /admin/governorates/:id/areas/order`, `…/order`): the position field
  sends the whole order with the row moved.
- **EC22** — no route uses `PlaceholderPage` after U5 and U6 (`git grep PlaceholderPage`): delete it; if one does, keep
  it and name the page left.
- **EC23** — the web's `AppError` and `toAppError` files' names in `shared/errors`.
- **EC24** — where occupancy's `PresentPerson` is built (`present.ts`) and read on the web (`usePresentList.ts`).
- **EC25** — each new route's `requireCan` action exists in `can()` (`visits.writeOff`, `space.dataReports.read`, the
  admin's guard): add none without the owner, reuse the existing ones; record any gap.
- **EC26** — the next PR number before `#PRNUM`'s replacement (§12.2), and CI green on the pushed head before the
  report.
