# Review — PR #89 (`feat/admin-add-owner`), independent review

## Head

`a074e6d2ccce0c77922df380ec8c03d292bebaaf` (`gh pr view 89` → `CLEAN`, first and last), fetched from
`refs/pull/89/head`; base `origin/main` = `02b1067a` (unchanged since the prompt was written). Four commits:
`d77ecd7c` design-system Combobox, `976c414e` lineParts, `2553f9e3` the password dialog, `a074e6d2` adding an
owner. 53 files, `apps/web` and `docs` only. I ran nothing: no lane, build or browser. CI results, timings, red
outputs and the real run are **read in `4_REPORT_PR2.md`**; everything else below I **saw in the code** at
`a074e6d2` (or in `refs/pull/90/head` = `ea56e225` for §8), unless marked otherwise.

## Verdict

**Not ready — no blocker, one fix round on this PR.** The security step is built and fails safe (no exact
email match, a pending read or a failed read all block the submit), but the upgrade's toast names the wrong
person, the sheet's layout is broken, the planned `users.md` sections are missing, the space search is
misnamed, and several planned rules (names isolated, `NamedLine`) are left as dead code.

## The five most important findings

**1. Should-fix — the upgrade flag is not bound to the email it was confirmed for, and no test proves what is
sent after the email changes.**
`apps/web/src/features/space-links/hooks/add-owner/useAddOwnerForm.ts:55,60,124-127`. `submit` reads
`upgradeRef.current`, which a passive effect copies from the last render's `upgrade`; nothing in `submit`
compares `request.email` with the email whose account was shown. I found **no path in practice** that sends a
stale `true`: typing is a discrete event, whose effects React flushes before the next event, and the only
asynchronous transitions (the users read answering, a refetch) either go false→true (fail-safe: one more
`EMAIL_HAS_ACCOUNT`) or keep the same email. But the approval's guarantee rests on effect timing, and the test
that covers the email change (`useAddOwnerForm.component.test.tsx:159-171`, "goes back to creating once the
email changes") asserts only `notice.kind` and `submit.label`, which come from render state — a ref left stale
(e.g. `upgrade` dropped from the effect's deps) would stay green.
*Fix:* keep the confirmed email beside the flag and send `upgradeExisting` only when
`account.status === 'found' && request.email === rememberedEmail` (computed from state the same render the
submit was made in, or both in one ref); extend the test to submit after the change and assert the second
body has no `upgradeExisting`, with the break "`upgrade` dropped from the effect's deps" seen red.
*Where:* a fix round on this PR (commit 4).

**2. Should-fix — the upgrade toast names the name the admin typed, not the account that was upgraded.**
`apps/web/src/features/space-links/hooks/add-owner/useAddOwner.ts:20`: `lines.upgraded({ name: request.name, … })`.
An upgrade keeps the account's own name (the server's `upgrade`, `adminOwners.service.ts:107-129`; the sheet
itself says «ويحتفظ باسمه»). Scenario: the admin types «Rima» for `rima@example.com`, the confirm shows the
account «Rima Haddad», the admin confirms → toast «رُقّي Rima إلى مالك…» — after a step whose whole point is
to show *whose* account it is. Also, the name field is still required on an upgrade although the server
ignores it (`addOwnerSchema`) — a nit worth a line in `space-links.md`.
*Fix:* pass the confirmed account's name (`account.account.name`) into the mutation's toast; isolate it (see
finding 6). *Where:* a fix round on this PR (commit 4).

**3. Should-fix — the add sheet has no space between its fields and its footer is not at the sheet's end.**
`apps/web/src/features/space-links/components/add-owner/AddOwner.tsx:37-38`: `<form noValidate …>` and
`<SheetBody>` carry no classes. Every other form sheet uses `form className="flex min-h-0 flex-1 flex-col"`
and `SheetBody className="flex flex-col gap-4"` (`features/lookups/components/sheet/LookupForm.tsx:12-13`,
`AmenityForm.tsx:13-14`, `space-links/components/admin-list/FiltersSheet.tsx:46`); `SheetBody` itself is only
`min-h-0 flex-1 overflow-y-auto px-4`. Seen in the executor's own `shots/pr2/upgrade-confirm-ar.png`: each label
touches the input above it, and «ترقية وربط» sits right under the notice in the middle of the sheet, not at its
foot. **Plausible** (not run): with the body unbounded, a phone-height sheet with the upgrade notice and a
failure does not scroll inside the body as the other sheets do.
*Fix:* the two classes, as the other sheets. *Where:* a fix round on this PR (commit 4); the real run's
phone shot proves it.

**4. Should-fix — `users.md` lacks the dialog's behaviour and decisions the plan requires, and
`space-links.md` links to it for them.**
Plan §9 *PR 2 · commit 3 › Docs*: `users.md` — *What it does* (web), *Behaviour* («The one-time password»),
*Web decisions* (D1.3's where and why; no X / Escape / outside click; «تم» only after «نسخ»; design issues 5 and
6; nothing in the cache). The diff adds only the code map, the open finding and a history line. So the dialog's
rules — the copy failure enabling «تم», a password no longer pending (or a 404) closing with «لم تُسجَّل طريقة
التسليم», any other failure staying open — are written nowhere but the commit body. `space-links.md:83` sends
the reader to [`users`](users.md#behaviour-and-flows) for the dialog, a section that says nothing of it
(`check:links` passes because the anchor exists). The fix prompt asked for `space-links.md` only, so the gap
survived both rounds. *Where:* a fix round on this PR (commit 3).

**5. Should-fix — the space search box and its list are both named «اختر المساحة»; the planned words are in the
catalogue and unused.**
`apps/web/src/features/space-links/components/SpaceCombobox.tsx:49-52` passes `placeholder` (the trigger's
«اختر المساحة») as `searchLabel`, `searchPlaceholder` and `listLabel`. Plan §9 *Words, `spaceLinks.choices`*:
`search` «بحث», `spacesPlaceholder` «اسم المساحة», `spaces` «المساحات» — all three are in both catalogues
(`shared/copy/{arabic,english}/spaceLinks.ts`, `choices`) and read by nothing (`git grep` at the head). A screen
reader meets three controls with one name; the empty search box tells the admin to «choose» where it should ask
for a name. No test names the search box or the list. *Fix:* `SpaceCombobox` takes the three words from
`choices` (PR 3's person combobox reuses `search`), and `AddOwner.component.test.tsx`'s search test finds the
search box and the list by these names. *Where:* a fix round on this PR (commit 4).

## The other findings

**6. Should-fix — names inside lines are not isolated or cut, and the `NamedLine` pieces are dead code.**
Plan §9: «a person's name isolated (`isolate`), a space's name its own element with `lang`/`dir` … (`lineParts`,
`NamedLine`)». At the head:
- `useAddOwner.ts:20` — the upgrade toast is a plain string: the person not isolated, an English-only space
  not marked. Departure 4 says it «does not fit `namedLine`'s single-name cut»; the plan's own interface says
  «other values bound by the caller» — `namedLine(({ name }) => lines.upgraded({ name: isolate(person), space: name }), spaceName)` fits.
- `useTemporaryPasswordDialog.ts:63` — `recorded({ name: person.name, … })`, not isolated;
  `TemporaryPasswordDialog.tsx:38` — the name in the description is a bare `<span>` (the email beside it has
  `dir="ltr"`, so it is isolated; the name is not).
- `useSpaceChoices.ts:39` — the owners joined without `isolate`; the plan says «names isolated», and
  `services/rowView.ts:59-62` does it for the same row.
- `services/namedLine.ts`, `components/NamedLine.tsx`, `components/toast/namedToast.tsx`, `types/NamedLineView.ts`
  are imported by nothing but each other (`git grep` at the head). So commit 2's reason for moving `lineParts`
  («a second capability … names a space inside a line», `976c414e`'s body) is not true in this PR, and commit
  4's body lists them as built.
*Fix:* use them for the upgrade toast (finding 2), isolate the three names. *Where:* a fix round on this PR
(commits 3 and 4; the bodies stay true).

**7. Should-fix — the space choices copy the list's row rules, and draw «مخفية» differently.**
`hooks/useSpaceChoices.ts:14-48` re-implements the name rule and the badges of `services/rowView.ts` (and of
`features/spaces/services/spaceName.ts`), inside a hook file rather than `services/`. They already disagree:
`useSpaceChoices.ts:29` draws hidden as `neutral`, `rowView.ts:52` as `warning` — the same space carries two
looks in the list and in the sheet (A3: «the row view decides the set, so the table and the card cannot
disagree», `space-links.md` Web decisions). Also `useSpaceChoices.ts:67-73`: `hasResults ? noResults : noResults`
and the stray comment `// empty is always noResults/searchFailed text; fine.` — a leftover. And (plausible, not
run) with `keepPreviousData` a failed search keeps the previous search's options on screen and shows no
failure line (the empty text shows only when there are no options).
*Fix:* build `SpaceChoiceView` from `rowView`'s name, state and owners (the third instance, engineering
principles §1); drop the dead ternary. *Where:* a fix round on this PR (commit 4).

**8. Should-fix — the acceptance criterion «RTL/LTR, light/dark, phone/768/desktop checked in a real run» has
no evidence.** `shots/pr2/` holds five images, all Arabic, light, 1440 px (one is the showcase). The fix round
says so itself (FR1.8: «Not done … English/dark and the other widths of the new step»), and the round-1 real
run claimed a password dialog that FR1.2 shows could not have appeared. Finding 3 is exactly what a phone shot
catches. *Where:* a fix round on this PR (or the owner waives it explicitly).

**9. Should-fix (small) — a 429 on the handover leaves «تم» enabled during the countdown.**
`useTemporaryPasswordDialog.ts:41` takes only `view` from `useRefusalView`; its `blocked` is dropped, so
`done.disabled` ignores it (`:100`). Plan §11 lists «the countdown in the dialog and the blocked submit» for
the handover. *Fix:* `disabled: !copied || blocked`. *Where:* a fix round on this PR (commit 3).

**10. Finding to record — the confirm cannot show a receptionist's front desks, nor the account's kind.**
`types/EmailAccountView.ts:8`: «the spaces of its active owner links». `EMAIL_HAS_ACCOUNT` is answered only for
an active non-admin, non-owner account (`adminOwners.service.ts:121-127`, checked in that order), so the confirm
shows a `USER`'s «لا مساحات» even when the person works at a front desk (a reception link). Before #90 the row
carries no reception spaces, so nothing can be done here; the executor wrote it only in the report (FR1.9:
«recorded, not done»), which is not a home. *Fix:* a finding (or a line in PR 3's plan) to show
`receptionSpaces` in the confirm once #90 lands. *Where:* a finding to record.

**11. Nit (finding to record) — «لا يُرقّى من هنا — تحقّق من البريد» stands for three different causes.**
`useEmailAccount.ts:24-34` reads page 1 only (default limit, newest first) of a *contains* search on name or
email (`users.repository.ts:60-64`), and `q` is capped at `NAME_MAX_LENGTH` = 100 (`adminUsersQuerySchema`) while
an email may run to 254. So a real exact match is `notFound` when more than a page of newer accounts contain the
email, when the email is over 100 characters (400), or when the read fails — and the line tells the admin to
check an email that is right, with no retry (only editing the email away and back refetches). Fail-safe, so not
a security issue. *Fix:* ask a larger `limit`, and word a failed read apart («تعذّر التحقق — أعد المحاولة»).
*Where:* a finding to record (or this fix round if cheap).

**12. Nits — fold into the fix round where the file is touched anyway.**
- `AddOwnerNotice.tsx:36,58` — `font-medium`, the only one in `features/`; foundation §11's table: a text style
  by role carries the weight (`text-label`).
- `TemporaryPasswordDialog.tsx:85,93` — a hard-coded `id="done-reason"`; `useId`.
- `useTemporaryPasswordDialog.ts:16` — `channelRef` is optional though every caller (the component and the
  test) passes it, and `TemporaryPasswordDialogInput` is also the component's public props, so a page could pass
  a `channelRef` the component overwrites. Make it required on the hook and keep it off the props.
- `useTemporaryPasswordDialog.ts:43-50` — a successful copy after a failed one leaves «تعذّر النسخ…» on screen.
- `pages/dashboard/admin/OwnersPage.tsx:6-11` — the page's JSDoc sits on the `temporaryPassword` constant.
- `docs/architecture/findings/83-…md:8,10` — «The wording is accepted for now» and «Resolves when … the owner
  accepts the wording» contradict each other.
- `ALREADY_OWNER`'s line («اربطه بالمساحة من صفّه في القائمة») points to a row action PR 3 builds; until it
  merges the line leads nowhere (design issue 3's own principle). Accepted if PR 3 follows; else word it.
- **Plausible, not run:** `Combobox.tsx` (the `loading` `role="status"`) and `AddOwnerNotice.tsx:17` mount the
  live region together with its text, which some screen readers do not announce.

## The three breaks that did not go red (FR1.5) — judged

1. **`preventDefault` removed (Escape; outside) → still green.** True, seen in the code: `TemporaryPasswordDialog.tsx:26`
   is `<Dialog open>` with no `onOpenChange`, so nothing can close it; the two `preventDefault`s are a second
   guard. The plan's break is «`closeLabel` given, *or* a `preventDefault` removed», and the first is red. The
   test still proves the behaviour (Escape and an outside click leave it open). Enough.
2. **`dir="ltr"` removed → green in English.** True (the `<html dir="ltr">` matched); the test now runs in Arabic
   and reads the nearest `[dir]` (`TemporaryPasswordDialog.component.test.tsx:51-57`). Enough.
3. **axe with the radio group unnamed → green.** True that axe has no name rule for `role="radiogroup"`
   (`aria-input-field-name` does not cover it); the group's name is proven by `getByRole('radiogroup', { name })`
   (`:77`), red when its `Field` label was emptied. **Plausible doubt:** the report also says «an emptied item
   label also passed» axe; `aria-toggle-field-name` covers `role="radio"`, so that should be red unless the
   `Field` still names it — unverified, not run. The replacement break (radios out of their `Field`s) is fine.

The other §10 *PR 2* tests exist with the planned titles, and each named break is listed red in FR1.2–FR1.5
(read in the report). The approval note's two tests exist (`AddOwner.component.test.tsx:194-246`); their breaks
(read skipped; match not exact) are the right ones. Gap: finding 1 (the request after an email change), and no
test of a failed users read.

## The PR description (must be rewritten)

It still describes round 1. It must say now:
- the account check (approval 2026-10-18): after `EMAIL_HAS_ACCOUNT` the account's name, joined date and
  spaces, «تأكّد أنه الشخص المقصود…», the exact match, and the submit blocked while reading or with no match;
- the defect found and fixed: the password slot rendered beside the sheet (round 1's «password dialog appeared»
  was not possible);
- Evidence from the head `a074e6d2`: `test:unit` 829, `test:component` 154 files / 1034, `check:links` 2153,
  etc. (round 1's 1008/2148 are stale); the run tool (headless Chrome over CDP, not playwright);
- what the real run did **not** cover (English, dark, phone, 768) — and drop the ticked «Real run performed»
  /«RTL and LTR … attached» claims until it is done (finding 8);
- the departures that stand (`channelRef` passed in; `spaceTriggerRef`); the three breaks that did not go red;
- findings 82, 83 and 87; the conflicts with #90 and who resolves them (below).

## Against PR #90 (STAFF, `ea56e225`)

- **Text conflicts** (`git merge-tree a074e6d2 ea56e225`, exit 1): `docs/architecture/findings/README.md` — both
  add index lines after 81 (this PR 82, 83, 87; #90 84), resolved by keeping all four in number order;
  `docs/features/space-links.md` — both add Behaviour / Web decisions / history lines. `docs/features/users.md`
  and `spaceLinksRepository.unit.test.ts` auto-merge.
- **`AdminUserRow` literals this PR adds** that need `receptionSpaces: []` if #90 merges after it:
  `apps/web/src/features/space-links/components/add-owner/AddOwner.component.test.tsx:39` (`RIMA`; the
  `{ ...RIMA, email }` at `:231` inherits it) and
  `apps/web/src/features/space-links/hooks/add-owner/useAddOwnerForm.component.test.tsx:33` (`RIMA`). The
  `joinedAt` literal in `routes.component.test.tsx:792` is PR 1's, inside an untyped fake answer — not this PR's.
- #90 changes no handover code the dialog reads (`TEMPORARY_PASSWORD_NOT_PENDING` and the 404 stay as they are).

## Checked and fine

- The security step's core: the match is exact (`useEmailAccount.ts:33`), on the email normalised as
  `emailSchema` normalises it on both sides (`useAddOwnerForm.ts:115-120`; `request.email` is the schema's
  output through `useServerForm`'s resolver); reading or no match blocks the submit (`:157`), and the disabled
  submit also stops Enter. An admin's, a suspended or an owner's email never reaches the confirm (the server
  refuses those before `EMAIL_HAS_ACCOUNT`).
- The password: held in `useAddOwnerForm`'s state only, cleared only by `done` (the dialog's `onDone`, on a
  recorded or no-longer-pending handover); `useAddOwner` and `useHandover` at `gcTime: 0`, the add reset after
  success, the handover's variables hold no password. The dialog sits beside the `Sheet` and its slot is a
  module-level constant, so it survives the sheet closing and re-renders. No X, Escape or outside click.
  The copy failure enables «تم» with its line; the handover's failures follow design issues 5 and 6.
- `Combobox`: without `search`, `shouldFilter` stays true and the input uncontrolled (`value`/`onValueChange`
  undefined), the empty text drawn as before; the showcase's third example and `foundation.md` §12's row match
  plan §9. Existing Combobox tests unchanged.
- The boundary: `space-links` reads the users list through its own repository and services (no import of
  `users`); the page composes the two features; the `space-links` index is dashboard-only (`dashboardOnly.ts`).
  `TemporaryPasswordDialog` lives in `users`, which `check:build` does not watch; nothing in the site imports it
  beyond the index re-export, which tree-shaking should drop — **not verified** (no build run).
- `lineParts` moved by `git mv` with its test (100 % similarity); `localisation.md`'s line as planned.
- Commit subjects 50 / 39 / 43 / 42; Conventional Commits; no tool attribution; bodies say why (but see
  finding 6 for the two untrue lines).
- Findings 82 (the flat files are as it lists), 83 and 87 in finding 63's format and indexed; 87 is the
  owner's own request (exec prompt).
- No physical direction class, no arbitrary value; both catalogues carry every new key.
