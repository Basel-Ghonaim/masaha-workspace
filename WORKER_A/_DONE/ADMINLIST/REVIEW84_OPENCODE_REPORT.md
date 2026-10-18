# REVIEW84 — independent post-merge review

**Merge SHA reviewed:** `93f152fe70f0b17e3e26a76fd7fa7fd7546ba75f` (merge of PR #84 into `main`, 2026-10-16), carrying `0c062c7f` and `60b2236c` on base `72ceb0474e91441495d1c270e050810384fb8a83`.
**Read:** commit objects only, from `C:\Users\basel\masaha-design-b`. No test was run; every test below was judged by reading it.

**Verdict.** The screen does what the plan said, and A3, A7, A8, the fourth status, the restore-only action and findings 44/50's resolutions are all really in the code; four should-fix items sit around it — the phone sheet still counts and clears the chip it no longer holds, the delete confirmation still says "undo right after", the chip's Arabic words are not the design's, and `space-links.md` still lists finding 50 as open — and the three open questions the prompt reserved numbers 69–70 for were never recorded as findings.

---

## Findings

### R84-001 — The phone's Filters sheet counts and clears the stale chip it no longer holds
**Severity:** should-fix · **verified** — read in the code, in the tests and against the design.
**Where:** `apps/web/src/features/space-links/hooks/admin-list/useAdminSpacesFilters.ts:85-92`; `apps/web/src/features/space-links/hooks/admin-list/useAdminSpacesList.ts:141-152`; asserted as correct by `apps/web/src/features/space-links/components/admin-list/AdminSpacesList.component.test.tsx:467-478` and `apps/web/src/features/space-links/hooks/admin-list/useAdminSpacesList.component.test.tsx:273-281`.

A7 moved the stale filter out of the sheet into a chip, so the sheet holds two fields. `applied` is still computed as `[filters.place !== null, filters.status !== undefined, filters.stale]` and `clearFilters` still writes `stale: false`. The design is explicit — `docs/design/prototype/Admin spaces.html:87` counts `active={[gov !== 'all', status !== 'all']}` and its `onClear` resets only those two.

**Failing scenarios.**
- `?stale=true` alone on a phone: the sheet's button reads «الفلاتر»/`Filters` with no badge (`FiltersSheet.tsx:35-39`), although a filter is applied and the chip above is on. `docs/features/space-links.md:67` says the button "counts them".
- `?status=hidden&stale=true` on a phone: the button reads «الفلاتر، المطبّق منها: 2» and shows a badge `2`, for a sheet in which one field applies. The test at `AdminSpacesList.component.test.tsx:472` asserts that string.
- Inside the sheet, «مسح الفلاتر»/`Clear filters` silently turns off the chip above the sheet, which the sheet never showed.
- The same test then asserts `search` becomes `''` (`:477`), so the wrong behaviour is pinned by a test.

**Fix.** Count and clear only the sheet's filters: `applied` from `place` and `status`; `clearFilters` writing `{ place: null, status: undefined }` and keeping the search. Keep `anyApplied` and `clearAll` counting and clearing everything, since the no-match state's «مسح الفلاتر» means all filters. Update the two tests: «Filters, 1 applied» and `count: 1`, and `?status=deleted`-style addresses keeping `stale=true` after the sheet's clear.

**Where the fix belongs:** the next branch touching `apps/web/src/features/space-links/hooks/admin-list/useAdminSpacesFilters.ts` (the admin list's filters), together with the line at `docs/features/space-links.md:67`.

---

### R84-002 — The delete confirmation still promises only the ten-second Undo, and the document calls that line true
**Severity:** should-fix · **verified** — read in both catalogues, in the capability document and in the design's record.
**Where:** `apps/web/src/shared/copy/english/spaces.ts` (`deleteDialog.description`), `apps/web/src/shared/copy/arabic/spaces.ts` (the same key); `docs/features/spaces.md:167`.

The built line is still `It leaves the site and this list. You can undo it right after.` / «تختفي من الموقع ومن هذه القائمة، ويمكنك التراجع فور الحذف.». The settled design changed it with this screen — `docs/design/CHANGES.md:154` (G3): «The delete dialog now says what is true — «وتجدها في «محذوفة» لاسترجاعها» — and keeps its «تراجع»», and `docs/design/prototype/Admin spaces.html:122` carries that Arabic. The decision at `docs/features/spaces.md:167` asserts the line "says only what is true", which stopped being true when this PR added the place a deleted space goes to; the PR touched the sentences around it and left it.

**Failing scenario.** An admin deletes a space, the ten seconds pass, and nothing in the dialog, the toast or the list has told them the space is under «محذوفة». The one screen that can bring it back is never mentioned at the moment of deletion.

**Fix.** Replace the description in both catalogues with the design's line («وتجدها في «محذوفة» لاسترجاعها» / "It leaves the site and this list; you'll find it under «Deleted» to restore it."), and amend the decision at `spaces.md:167` with the new wording and this PR's date.

**Where the fix belongs:** the next branch touching the delete dialog copy, or `docs/features/spaces.md`'s decisions. Note the plan put "changing the existing delete Undo flow" out of scope; the fix is a copy line and a decision line, which is why it should be taken explicitly rather than left.

---

### R84-003 — The chip's Arabic words are not the design's «قديمة أو ناقصة»
**Severity:** should-fix · **verified** — the design record, the prototype and the catalogue all read, and the document quotes the design.
**Where:** `apps/web/src/shared/copy/arabic/spaceLinks.ts` (`adminList.staleOrMissing`); the plan's copy table, which carried the same words.

`docs/design/CHANGES.md:158` (G5 · A8, **DI-26**, the owner's amendment) settles the words: "so its chip says so — **«قديمة أو ناقصة»**, A7's «بيانات قديمة فقط» amended", and `docs/design/prototype/Admin spaces.html:97` renders `tr('قديمة أو ناقصة', 'Stale or missing')`. The English catalogue matches ('Stale or missing'); the Arabic catalogue reads «بيانات قديمة أو ناقصة». `docs/features/space-links.md:69` quotes «قديمة أو ناقصة», which is the design's words — so the screen and its own capability document disagree.

**Failing scenario.** Every admin using Arabic sees a chip the owner did not word, and the string a reader checks in the document is not the string in the product.

**Fix.** Set `staleOrMissing` in the Arabic catalogue to «قديمة أو ناقصة»; correct the plan's copy table so the words are not carried again.

**Where the fix belongs:** the next branch touching `apps/web/src/shared/copy/arabic/spaceLinks.ts`. The catalogue change needs a matching assertion in `AdminSpacesList.component.test.tsx` only if a test names the Arabic chip; today the chip's label is asserted in English (`useAdminSpacesList.component.test.tsx:268-271`).

---

### R84-004 — `space-links.md` still lists finding 50 as open
**Severity:** should-fix · **verified** — three documents read against each other.
**Where:** `docs/features/space-links.md:138`.

The finding itself is `Status: Resolved` with a dated resolution (`docs/architecture/findings/50-an-owner-whose-only-spaces-are-deleted-stays-an-owner.md:3`, `:9`) and the index moved it to *Resolved* (`docs/architecture/findings/README.md`). The capability document's *Open findings* list still carries it. `docs/features/spaces.md:223-229` did drop 44 from its own list, so the two documents disagree with each other as well.

**Failing scenario.** A reader looking for what is still open finds 50 in the document an owner would read first, and finds it resolved two files away. `docs/architecture/documentation.md:8` gives each fact one home; `§5.9` makes *Open findings* a list of links, not a second status.

**Fix.** Remove the line from `docs/features/space-links.md`'s *Open findings*.

**Where the fix belongs:** the next branch touching `docs/features/space-links.md` (R84-007 and R84-008 land in the same file).

---

### R84-005 — The three open questions the prompt reserved numbers for were never recorded as findings
**Severity:** should-fix · **verified** — the plan's reading, the free numbers in the folder, and the three observations' only homes.
**Where:** the plan's §6 and §7; `docs/architecture/findings/`; the three observations in `…\MASAHA_WORKER_A\REPORT\ADMINLIST_REPORT.md` §7.4 and §8, and `…\ADMINLIST_BROWSER_ROUND2_REPORT.md` §10.

The prompt said "New findings: **69–70**". The plan read them as the GitHub issues `#69`/`#70`, already closed, and folded nothing (`ADMINLIST_PLAN.md` §6, §7). The findings folder ends at 67, so 69–70 are free numbers this item was given. Three observations therefore stayed in a report, and `docs/development/workflow.md:122` and `:179` require them to be findings:

1. **A deleted row keeps its freshness badges** (`ADMINLIST_REPORT.md` §7.4). The design draws a dash for a deleted row (`docs/design/prototype/Admin spaces.html:47`, `:107`) and CHANGES.md:154 lists the deleted row's facts as «محذوفة · 14 أغسطس». `docs/architecture/documentation.md:38` makes a design/code divergence a finding. The report offers it to the owner instead of recording it.
2. **Space 41 rendered verified with no owner link** (`ADMINLIST_REPORT.md` §8). The report calls it "an API finding, not a screen one" and leaves it unrecorded — "Record, never absorb" (`workflow.md:179`).
3. **`spaceId: invalid_format` on the owners endpoint** (`ADMINLIST_BROWSER_ROUND2_REPORT.md` §10). The contract says `validation` `errors.spaceId = ["invalid_choice"]` for a soft-deleted space (`docs/api/api-contract.md:553`) and the code throws `invalid_choice` (`apps/api/src/modules/space-links/admin-owners/adminOwners.service.ts:41-46`); `POST /admin/spaces/:spaceId/owners` answers 404 for one (`api-contract.md:562`). The observed code matches none of the three, and the observation is recorded nowhere as a question.

**Failing scenario.** Each of the three is a divergence a reader cannot find: the design and the screen differ on a deleted row's facts, a data anomaly that may be an API defect, and a contract/code/undefined gap in one error code. Only the report that happened to be written holds them.

**Fix.** Create three finding files (69, 70, 71, or as the owner numbers them), each with its evidence and its "Resolves when" — for (1) "the deleted row's freshness matches the design, or the design's line is amended"; for (2) "a verified space always has an active owner link, or the row explains it"; for (3) "the refusal code for a soft-deleted space on the owners endpoints is one the contract names".

**Where the fix belongs:** a finding to record — records are exempt from the one-home rule (`documentation.md:20`), so a records-only change is enough, and it needs no code. Offer it in the next branch that touches `space-links`, `spaces` or the owners endpoints.
---

### R84-006 — A deleted row shows badges where the design shows one muted line
**Severity:** should-fix, or an owner decision · **verified as a divergence** — the design record, the prototype and the row view all read.
**Where:** `apps/web/src/features/space-links/services/rowView.ts:39-51`, asserted by `rowView.unit.test.ts:93-104` and `AdminSpacesList.component.test.tsx:207-227`.

The design draws a deleted row's status cell as one muted line — «محذوفة · 14 أغسطس» (`docs/design/prototype/Admin spaces.html:53`, `docs/design/CHANGES.md:154`) — with no verification badge and no freshness on either width (`:47`, `:107`). The row view puts up to three badges (`موثّقة` `success`, `مخفية` `warning`, `محذوفة` `neutral`) plus the freshness badges, so a deleted verified space shows a green verification badge and a space that is gone warns about facts nobody will fill.

The prompt's A3 ("each row shows its verification badge always") and the plan's criterion 3 pull the other way, so the code is defensible and the divergence is real. The report declared only the freshness half (`ADMINLIST_REPORT.md` §7.4) and left the verification half undeclared.

**Failing scenario.** The deleted list is the noisiest screen in the admin: a badge pair that says a space that no longer exists is verified, on a row the design marks as gone. Nothing in the documents records the choice.

**Fix.** Either follow the design for deleted rows only (`rowView.ts` returns one muted «محذوفة · date» line and no verification badge when `deletedAt !== null`, keeping A3 whole for live rows), or keep the badges and record the design change as a finding with the report's freshness question beside it.

**Where the fix belongs:** a decision for the owner (see Decisions §4); then the next branch touching `rowView.ts`, with `rowView.unit.test.ts:93-104` and the two component tests updated together.

---

### R84-007 — Four documents still call the filter "stale only", and one quotes the chip wrongly
**Severity:** nit · **verified** by grep across `docs/` and the sources.
**Where:** `docs/features/space-links.md:102`; `docs/features/spaces.md:84`, `spaces.md:120`; `docs/architecture/data-model.md:85`; the source comments at `apps/web/src/features/space-links/hooks/admin-list/useAdminSpacesFilters.ts:85` and the test title at `AdminSpacesList.component.test.tsx:325`.

The contract's `stale` already keeps missing groups (`docs/api/api-contract.md`, `GET /admin/spaces`: "`stale`: `true` keeps the spaces with at least one stale or missing fact group"), and this PR's new bullet says so (`space-links.md:69`). Four sentences still name the filter «بيانات قديمة فقط»/"stale only" — inside `space-links.md` itself, which now contradicts itself one line apart. `data-model.md:85` is a platform document restating a UI label.

**Fix.** Say "stale or missing" (or link `space-links.md` for the label) in those four places and in the two source comments; retitle the test.

**Where the fix belongs:** the next branch touching these documents or the admin list's filters.

---

### R84-008 — The new decisions and history lines carry no PR
**Severity:** nit · **verified**.
**Where:** `docs/features/space-links.md:125-128`, `space-links.md:163`; `docs/features/spaces.md:211-213`, `spaces.md:252`; the two findings' resolutions (`…/44-….md:9`, `…/50-….md:9`).

Every new decision ends "2026-10-15, the deleted-spaces screen" and every new history line reads "The deleted-spaces screen — …". `docs/architecture/documentation.md:72` requires each decision to carry "its reason, its date and its PR", and `:75` makes *History* "the PRs". The form "the deleted-spaces item" already in both files is the existing precedent for items that never had a PR; this one has #84.

**Fix.** Write `2026-10-15, #84` on the four decisions and the two history lines.

**Where the fix belongs:** the next branch touching either capability document.

---

### R84-009 — Two document sentences do not match what they describe
**Severity:** nit · **verified**.
**Where:** `docs/features/spaces.md:211` ("The design drew it as a button beside the row's name"); `docs/features/space-links.md:117` ("**Freshness shows what is stale on a warning badge and what is missing on a warning badge,**").

The design puts the restore button in the row's Actions cell, not beside the name (`docs/design/prototype/Admin spaces.html:55`, `:76`; the card's actions slot at `:109`). And the freshness decision repeats "on a warning badge" where the built behaviour is one badge each (`rowView.ts:26-38`), which the Arabic and English tests assert.

**Fix.** Correct both sentences; the freshness one can read "…and what is missing on a warning badge each".

**Where the fix belongs:** the next branch touching either document (with R84-004 and R84-008).

---

### R84-010 — No test that a second Restore click while pending writes once
**Severity:** nit · **verified missing** — read against the plan and the guard.
**Where:** `apps/web/src/features/spaces/hooks/menu/useSpaceActionsMenu.ts:43-52`; `apps/web/src/features/spaces/components/menu/SpaceActionsMenu.component.test.tsx:306-320`.

The plan's D2 and the review's fourth question both ask for "no double restore". The guard is real — `waiting: restore.isPending || hold.blocked` (`useSpaceActionsMenu.ts:47`) and `onClick` runs only `if (!menu.waiting)` (`SpaceActionsMenu.tsx:44-46`) — but only the 429 branch is tested (`:306-320` clicks again under the hold and counts one write). Nothing clicks Restore twice while `restore.isPending`, so a regression that dropped the pending half of `waiting` would still pass.

**Fix.** One test: click Restore, let it stay pending (the file's `deferred<FakeAnswer>()` pattern), click again, assert `writes()` is still length 1.

**Where the fix belongs:** the next branch touching the restore or the row actions.

---

### R84-011 — The hook test proves a page transition where the plan asked for a status transition
**Severity:** nit · **verified weaker than planned.**
**Where:** `apps/web/src/features/space-links/hooks/admin-list/useAdminSpacesList.component.test.tsx:287-315`, against `:170-199`.

The plan names "keeps previous rows busy during a status transition". The new test navigates `?status=deleted` → `?status=deleted&page=2`, so it re-proves what `:170-199` already proves for the page; its own additions are the `deletedOn` line and `status=deleted` in the request. No test changes the status and watches the rows stay, which is the transition a deleted list introduces (live rows shown while a deleted page loads).

**Fix.** Navigate from `/s` to `/s?status=deleted` with a deferred answer and assert `busy === true` and that the previous rows are still there.

**Where the fix belongs:** the next branch touching the admin list.

---

### R84-012 — `updatedOn` formats a deletion date but still documents itself as the last-update formatter
**Severity:** nit · **verified**.
**Where:** `apps/web/src/features/space-links/services/updatedOn.ts:11-17`, called from `apps/web/src/features/space-links/services/rowView.ts:50`.

The plan's second stronger decision expected "one focused helper/test adjustment" beside the existing list-date formatter. The helper was reused as it stands, so its name and its comment ("When a space was last updated, as its row shows it") now understate it: it formats `lastUpdatedAt` and `deletedAt`. The rule itself is right — one Gaza/day/year formatter for both dates — and `updatedOn.unit.test.ts:7-25` already covers the Gaza day, the year and the boundary, so no behaviour is at risk.

**Fix.** Widen the comment (and the name, if the owner prefers) to "a row's date".

**Where the fix belongs:** the next branch touching the admin list's services.

---

### R84-013 — Commit `0c062c7f` on its own shows deleted rows with the live menu
**Severity:** nit (history; nothing to rewrite) · **verified.**
**Where:** `0c062c7f`'s file list; `apps/web/src/features/spaces/types/SpaceRef.ts` and `…/menu/SpaceActionsMenu.tsx` as of that commit.

`0c062c7f` is `feat(space-links): show deleted space facts`: it made the list request and render deleted rows and changed nothing under `apps/web/src/features/spaces`. At that commit `SpaceRef` was `Pick<AdminSpaceRow, 'id' | 'nameEn' | 'nameAr' | 'isHidden'>` and `SpaceActionsMenu` always rendered the live menu, so the intermediate build offered Edit, Hide/Show and Delete on a deleted space. `docs/development/workflow.md:111` asks for one commit = one complete, working unit of change; the sentence "show deleted space facts" is only true once the restore-only action is there too.

**Failing scenario.** None for `main`, which has both commits. The cost is the rule: a reader bisecting, or a revert of one commit, lands on a screen that offers to delete a deleted space.

**Fix.** Nothing to change in history. The rule for the next branch: when a new row state needs an action change, the list and the action belong in one commit.

**Where the fix belongs:** no fix; recorded here so the next Work Item's plan says so.

---

---

## The tests the plan names (plan §9), one by one

Read, not run. "Break" = would the break the plan names make this test fail?

### Unit lane

| # | Planned test | Where it is | Status | Break |
|---|---|---|---|---|
| 1 | `filtersOf.unit.test.ts`: `status=deleted` parses, serializes and requests as `deleted` | `services/filtersOf.unit.test.ts:33-37` | present, new | **yes** — restoring the old `isListStatus` guard fails `:34-36` |
| 2 | …an invalid status is omitted | `services/filtersOf.unit.test.ts:39-50` (`status=closed` kept; `status=deleted` removed from the list) | present, corrected | **yes** |
| 3 | `rowView.unit.test.ts`: live verified/hidden rows give verification plus optional hidden | `services/rowView.unit.test.ts:62-89` (`it.each`, four rows) | present | **yes** |
| 4 | …live unverified rows remain unverified | same, row 2 | present | **yes** |
| 5 | …deleted rows produce the deletion label and date | `services/rowView.unit.test.ts:93-104` (both languages, Gaza day) | present | **yes** |
| 6 | …deleted rows produce owner wording | not asserted in that test — it matches on `state` and `deletedOn` only; owners wording is asserted by the desktop component test (`AdminSpacesList.component.test.tsx:207-227`, cell `'⁨Rima⁩'`) | **weaker than planned** | **no** for `rowView`: a regression that dropped a deleted row's owners would pass this lane and fail the component lane |
| 7 | …missing freshness is `warning` | `services/rowView.unit.test.ts:120-140` (both languages, plus `:137-141` for missing alone) | present, updated | **yes** |
| 8 | `updatedOn.unit.test.ts` *(if the helper changed)* | helper unchanged; `services/updatedOn.unit.test.ts:7-25` already covers the Gaza day, the year and the year boundary; wording at `rowView.unit.test.ts:93-104` | not applicable — the plan made it conditional | **yes**, through the shared formatter's own tests |

### Component lane

| # | Planned test | Where it is | Status | Break |
|---|---|---|---|---|
| 9 | Desktop: the status select has All plus four statuses | `AdminSpacesList.component.test.tsx:229-244` | present, new | **yes** |
| 10 | Desktop: a deleted request is sent with `status=deleted` | `AdminSpacesList.component.test.tsx:207-227` (`requests[0].params`) | present | **yes** |
| 11 | Desktop: table cells show both live facts | `AdminSpacesList.component.test.tsx:176-205` (hidden row now `UnverifiedHidden`) | present | **yes** |
| 12 | Desktop: a muted deleted row with owners, date and only its restore action | `AdminSpacesList.component.test.tsx:207-227` (cells, `text-muted-foreground`, no link, no actions button) | present | **yes** |
| 13 | Phone: the deleted card shows the same facts, date and owners and only Restore | `AdminSpacesList.component.test.tsx:455-465` | present | **yes** |
| 14 | Phone: the stale control is a ToggleGroup chip by the count, not a switch | proven on desktop (`AdminSpacesList.component.test.tsx:342-358`: a `toolbar` named "Quick filter", `aria-pressed`, no `switch` anywhere); the phone test only asserts the sheet holds no switch and the chip reads pressed (`:467-478`) | **weaker than planned** — the plan put it in the phone test; the behaviour is covered | **yes**, by the desktop test |
| 15 | `useAdminSpacesList.component.test.tsx`: the view exposes the deleted option and labels | `:252-285` (four options + All, `filters.stale`, `filters.quickFilter`) | present | **yes** |
| 16 | …preserves the filters and the page request | `:287-315` (`status=deleted` on both requests) | present | **yes** |
| 17 | …keeps the previous rows busy during a **status** transition | `:287-315` changes the **page**, repeating `:170-199`; no test changes the status | **weaker than planned** | **no** — a regression that dropped `placeholderData` on a status change would pass every test |
| 18 | `SpaceActionsMenu.component.test.tsx`: a deleted row exposes only Restore | `features/spaces/…/SpaceActionsMenu.component.test.tsx:265-270` | present | **yes** |
| 19 | …keeps its trigger pending and focused while restoring | `:272-295` (`aria-busy`, focus held) | present | **yes** |
| 20 | …succeeds after the admin list refresh | `:272-295` — the toast only fires after `await refresh()` in `useRestoreSpace.ts:26-29` | present (indirect) | **yes** |
| 21 | …shows a named failure on refusal | `:297-304` (named toast + `req-1`) | present | **yes** |
| 22 | …live rows retain Edit / Hide-or-Show / Delete | `:88-262`, pre-existing and unchanged | present | **yes** |
| 23 | …no double restore | **missing** — the second click is only exercised under a 429 hold (`:306-320`) | **missing** | **no** — see R84-010 |
| 24 | Existing accessibility assertions updated and retained, desktop and phone | `AdminSpacesList.component.test.tsx:429-437`, `:490-495`; a new one for the menu's deleted branch `SpaceActionsMenu.component.test.tsx:322-326` | present | **yes** |

**Tests that assert a wrong behaviour:** `AdminSpacesList.component.test.tsx:467-478` — «Filters, 2 applied» for a sheet holding one applied field, then `search` becoming `''` after the sheet's clear — and `useAdminSpacesList.component.test.tsx:273-281` — `label: 'Filters, 2 applied', count: 2`. Both pin the defect in R84-001 rather than the design.

**Not run here:** every lane. CI ran them on the head; the verdicts above come from reading each test against the code it names.

---

## Step 10: the analyst's earlier read, point by point

**(a) The Filters sheet still counts and clears the stale chip, and a test asserts «2 applied» — confirmed.** `useAdminSpacesFilters.ts:85-92` counts three filters and `clearFilters` writes `stale: false`; `useAdminSpacesList.ts:141-152` passes that count to the sheet's label and badge; `AdminSpacesList.component.test.tsx:472` asserts «Filters, 2 applied» with `?status=hidden&stale=true`, and the design counts two (`docs/design/prototype/Admin spaces.html:87`). R84-001.

**(b) `space-links.md` still lists finding 50 as open — confirmed.** `docs/features/space-links.md:138` against `docs/architecture/findings/50-…md:3` (`Resolved`) and `README.md`'s *Resolved* group; `spaces.md` did drop 44 from its own list. R84-004.

**(c) No `#84` in the new decisions, history or finding resolutions — confirmed.** `space-links.md:125-128` and `:163`, `spaces.md:211-213` and `:252`, and both findings' resolutions read "2026-10-15, the deleted-spaces screen" / "The deleted-spaces screen"; `documentation.md:72` and `:75` ask for the PR. R84-008.

**(d) The plan read 69–70 as Issues, so three open questions went unrecorded — confirmed.** `ADMINLIST_PLAN.md` §6 and §7 fold issues `#69`/`#70` as already closed; the folder's highest finding is 67, so the prompt's reserved numbers were unused; the three observations live only in `ADMINLIST_REPORT.md` §7.4 and §8 and `ADMINLIST_BROWSER_ROUND2_REPORT.md` §10. R84-005.

**(e) Finding 50's way out is written only in documents, not on the screen — confirmed.** `spaces.md:82`, `space-links.md:72` and the finding's resolution carry it; no catalogue line does, and the design's own on-screen form («كل مساحاته محذوفة — استرجع المساحة لفك ربطه», `docs/design/CHANGES.md:155`, G4) needs the owners page and an unlink action, which A4 owns. `spaces.md:82` is honest that there is no web unlink UI; `space-links.md:72`'s "the way out … is written there" reads as a path the admin can follow. R84-014 below.

**(f) `space-links.md` quotes the chip as «قديمة أو ناقصة» while the catalogue has «بيانات قديمة أو ناقصة» — confirmed, but the document is the right one.** `docs/design/CHANGES.md:158` (DI-26, the owner's amendment) and `docs/design/prototype/Admin spaces.html:97` both settle on «قديمة أو ناقصة» / "Stale or missing"; the Arabic catalogue reads «بيانات قديمة أو ناقصة», so the defect is in the catalogue, not the document. R84-003.

**(g) Commit `0c062c7f` alone shows deleted rows with the live menu — confirmed.** That commit touches nothing under `apps/web/src/features/spaces`; at it, `SpaceRef` had no `deletedAt` and `SpaceActionsMenu` always rendered Edit/Hide-or-Show/Delete. R84-013.

### R84-014 — Finding 50's on-screen resolution does not exist yet
**Severity:** nit, and an owner's call · **verified.**
**Where:** `docs/features/spaces.md:82`, `docs/features/space-links.md:72`, `docs/architecture/findings/50-…md:9`.

The finding is Resolved on the owner's third option ("the owner accepts the way out as it is, written where the admin will find it"), which the plan and the prompt both record as accepted — so the status is legitimate. What is worth the owner's eye: `docs/design/CHANGES.md:155` (G4) resolves finding 50 *on screen*, on the owners page, where a person whose spaces are all deleted reads «كل مساحاته محذوفة — استرجع المساحة لفك ربطه». No web unlink UI and no owners page exist, so nothing on the dashboard carries the way out, and `space-links.md:72` points the reader at `spaces.md` as if a path were there.

**Fix.** Either say once, in `space-links.md:72` as well as `spaces.md:82`, that the unlink step has no screen yet, or leave the documents and re-open finding 50's status to "Resolved (documentation) — the screen's line follows A4". A finding's status takes only Open/Resolved/Accepted, so the second belongs in the resolution line.

**Where the fix belongs:** an owner decision (Decisions §5); then the next branch touching `space-links.md`.

---

## Checked and fine

- `?status=deleted` is read by the contract's own rule, serialized, sent to `GET /admin/spaces`, and survives the filters' and pages' links; an invalid or absent status still falls back (`filtersOf.unit.test.ts:33-50`, `useAdminSpacesList.component.test.tsx:287-315`).
- A3 holds: the verification badge always, «مخفية» beside it, hidden no longer replacing the verification, decided once in `rowView.ts:39-47` so the table and the card cannot disagree (`rowView.unit.test.ts:62-89`, `AdminSpacesList.component.test.tsx:176-205`, `:444-453`).
- A8 holds: missing and stale both `warning`, "Up to date" `success`, in both languages (`rowView.ts:26-38`, `rowView.unit.test.ts:120-141`).
- «محذوفة» and «حُذفت في …» / «Deleted on …» exist in both catalogues and ride the one Gaza/short-date rule, year only when it differs (`rowView.ts:48-51`, `updatedOn.unit.test.ts:7-25`).
- A deleted name is muted text, not a link, on both widths (`SpaceNameText.tsx:10-19`; `AdminSpacesList.component.test.tsx:207-227`, `:455-465`).
- A deleted row's only action is Restore: no menu, no edit, no hide/show, no delete, no owner action (`useSpaceActionsMenu.ts:36-53`, `SpaceActionsMenu.tsx:30-53`, `SpaceActionsMenu.component.test.tsx:265-270`).
- Hooks all run before the early return in `useSpaceActionsMenu.ts:36`, and both branches keep the same order (`useSpaceActionsMenu.ts:25-33`).
- The accessible name holds the visible label: `aria-label` is «استرجاع {name}», which contains «استرجاع» (`useSpaceActionsMenu.ts:39-41`, `SpaceActionsMenu.tsx:38`).
- No double restore is guarded in code (`waiting = restore.isPending || hold.blocked`; the click runs only when not waiting), and the 429 hold is the same one the Undo records, through `useRestoreSpace`'s `useRecordHold` (`useRestoreSpace.ts:20-36`).
- After a restore the admin scope is refetched before the toast, so the deleted list drops the row and the focus lands on the list region (`useRestoreSpace.ts:26-29`; `AdminSpacesList.component.test.tsx:400-412`; Round 2's D4 evidence).
- A 429 on the list *read* showing the list's own failure state with a retry that waits, rather than `SpaceActionsHold`, is the documented behaviour (`space-links.md:73`, `spaces.md:80`); Round 1's I2 "Fail" is not a defect of this change, as the final report argued.
- Catalogue parity holds: 55 keys in `spaceLinks` in both languages, in the same order, with every new key in both; `spaces.menu.restore`/`restoreNamed` in both.
- Design system only; semantic tokens (`text-muted-foreground`, `text-caption`, `text-label`, `text-body-sm`); no physical direction class (`justify-end` is direction-relative); no hardcoded user-facing string.
- A `ToggleGroup` with `aria-label` outside a `Field` is named by that label, and `type="multiple"` gives `role="toolbar"` — the design system's own test relies on both (`ToggleGroup.component.test.tsx:22-27`).
- The obsolete "the web does not offer `deleted` yet" exception is gone from `space-links.md` and the status select offers the contract's four.
- Findings 44 and 50 are really resolved in code: the deleted list restores (`SpaceActionsMenu.component.test.tsx:272-295`) and both finding files and the index agree.
- The `*Superseded 2026-10-15 …, below.*` form for the two replaced decisions matches the existing precedent (`spaces.md:173`, `:196`).
- Two commits, each carrying the document lines it makes true, as the owner's amendment required; both subjects under 50 characters.
- The overview's Built lines are true: the list shows deleted spaces among its statuses, and the Spaces line names restore from the «deleted» rows.

---

## Decisions for the owner

**1. The phone sheet's count and its clear (R84-001).**
- (a) Count and clear only the sheet's two filters, exactly as the design does; the chip above keeps its own state.
- (b) Put the stale filter back in the sheet as a field, so count and clear are honest — but A7 and DI-26 say a filter is a chip, not a field.
- (c) Keep the count and add a second line in the sheet that clears the chip by name.
*Recommendation: (a).* The design is explicit, it is the least surprising, and it is two lines of code plus two expectations in tests. (c) adds a control the design does not have.

**2. The delete confirmation's line (R84-002).**
- (a) Adopt the design's «وتجدها في «محذوفة» لاسترجاعها» / "you'll find it under «Deleted» to restore it", and amend `spaces.md:167`.
- (b) Leave the Undo-only line and record the divergence as a finding.
*Recommendation: (a).* The screen now has the place the design names, the decision that claims the line "says only what is true" is already false, and the copy is in both catalogues already.

**3. The chip's Arabic words (R84-003).**
- (a) The design's «قديمة أو ناقصة» in the catalogue.
- (b) Keep «بيانات قديمة أو ناقصة» and record a design change.
*Recommendation: (a).* DI-26 is an amendment the owner made about these exact words, and the document already quotes them.

**4. What a deleted row shows (R84-006).**
- (a) Keep the badges as built and record the design change (with the report's freshness question as the same finding).
- (b) Follow the design for deleted rows: one muted «محذوفة · date» line, no verification badge, no freshness — A3 then holds for live rows only.
- (c) Keep the verification badge (the prompt's "always") and drop freshness only.
*Recommendation: (c), or (b) if the badge on a space that no longer exists reads worse than the missing-facts warnings.* Either way the choice has to be written down; it is currently neither in the documents nor in a finding.

**5. Finding 50's resolution now (R84-014, and the three questions in R84-005).**
- (a) Record findings 69, 70 and 71 in a records-only change and leave 50 Resolved as the owner accepted.
- (b) Record only the two design/contract divergences (the deleted row's facts, `invalid_format` vs `invalid_choice`), and re-check the verified-with-no-owner observation on a fresh database before writing it down.
- (c) Re-open 50 until the owners page exists.
*Recommendation: (b), plus a sentence in `space-links.md:72` that the unlink step has no screen yet.* 69 and 70 are free numbers this item was given; leaving them unused is what let three observations stay in a report nobody reads again.

**6. Where the history split is governed (R84-013).**
- (a) Nothing; the next branch's plan states that a new row state and its action change go in one commit.
- (b) Add the rule to `docs/development/workflow.md` §3.
*Recommendation: (a).* `workflow.md:111` already says one commit is one complete unit; the case is recorded here so the next item does not repeat it.

---

*Reviewer note on scope: nothing was run, installed, edited, checked out or written outside this report; the merge commit's objects were read from `masaha-design-b`.*
