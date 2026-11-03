# Lane W2 working notes

## C6.1 db0ebe14 feat(audit): show a space's audit log (37)
- RED (code first, moved aside by red.py): unit — "Cannot find module './actionWords' / './actionGroups' / './detailsOf'" Test Files 4 failed (4); component — Failed to resolve import "./AuditLog". Page test: R-C61-page (the report link removed) × "names the space from the user’s spaces and links each target to its page" — Unable to find link "بلاغ".
- GREEN: unit Test Files 4 passed · Tests 18; component AuditLog Tests 8 passed; space AuditPage 1 passed.
- B150 (one Arabic action removed): × every AUDIT_ACTIONS action has a word in ar — expected [ 'visit.writtenOff' ] to deeply equal []
- B151 (a group of 41): × each platform group holds at most 30 actions — expected 41 to be less than or equal to 30
- B152 (void reason dropped): × words a void's amount, method and reason — expected '₪25 · Cash' to be '₪25 · Cash · reason: Typed twice'
- B153 (the admin named 'Admin'): × the owner’s log: Masaha as «فريق مساحة» — expected [ 'Admin', … ]
- B154 (actor filter always): × hides the actor filter for a period of one actor — expect(element).not.toBeInTheDocument()
- B155 (all neutral): × a void, a staff deactivation… are red — expected [ 'neutral', … ] to deeply equal [ 'destructive', … ]

## C6.2 60589d7a feat(audit): show the platform's audit log (42)
- RED (stub body back): 3 × — Unable to find text "Events: 2"
- GREEN: Test Files 1 passed · Tests 3 passed
- B156 (space omitted): × names the entry’s space — expected 'Sara Odeh' to be 'Sara Odehat ⁨Focus Hub⁩'
- B157 (deleted linked): × a deleted target is marked and not a link — expect(element).not.toBeInTheDocument()
- B158 (address not written): × the filters are in the address and survive a reload — expected '' to be '?q=Rimal&period=all&type=lookups'

## Heavy
- typecheck (C6.1+C6.2 tree): exit 0
- lint (C6.1+C6.2 tree): exit 1, 2 errors in AuditLog.component.test.tsx (unsafe member access, non-null) → fixed before the commit; targeted eslint clean

## C6.3 901ce17f feat(platform-settings): edit the settings (42)
- RED (PlatformSettingsCards.tsx moved aside): Failed to resolve import "./PlatformSettingsCards" — Test Files 1 failed
- GREEN: Test Files 1 passed · Tests 6 passed
- B159 (staleness waits on the contact's read): × each settings card loads, saves and fails on its own — Unable to find textbox "Prices (days)"
- B160 (empty WhatsApp sent as ''): × an empty contact field sends null — Unable to find text "Settings saved"
- B161 (no bound: clamped and sent): × freshness refuses 0 and 366 with its words — Unable to find text "From 1 to 365 days"
- B162 (minutes always): × the rounding minutes field shows only for «تقريب لأعلى…» — expect(element).not.toBeInTheDocument()
- B163 (badge never): × «تغييرات غير محفوظة» and «تجاهل التغييرات» while a card differs — Unable to find text تغييرات غير محفوظة
- checks: targeted eslint clean; tsc -p apps/web/tsconfig.app.json clean; prettier clean

## C6.4 9e6f4e1b feat(platform-settings): read the public contact (48)
- RED (HEAD's PlatformContact + platformContact.ts copied in from git show, restored from backup): × the site’s contact comes from GET /settings/public — expect(element).not.toBeInTheDocument(); × with only the email set — Unable to find link "بريد team@example.com" (2 failed | 1 passed)
- GREEN: component Test Files 2 passed · Tests 9; unit 1 passed · 2
- B164 (no read: answered null): × the site’s contact comes from GET /settings/public; × with only the email set — Unable to find role="link"
- B165 (nothing drawn): × no contact set: the caller’s line — Unable to find text لا توجد وسيلة
- site routes test: 12 passed, × "shows the Directory under its title" (Unable to find role="main") — fails the same at HEAD with HEAD's files (head-dir.txt): not this change; finding 87's family (site test opening /spaces). Re-run in the lane-end run.

## C6.8 7e3cdb72 fix(space-links): name a person's front desks (45)
- RED (HEAD's usePersonChoices + useLinkOwnerDialog copied in, restored): × a receptionist’s option reads «مستخدم · استقبال {spaces}»… — Unable to find text (heard 'User · reception at Sea View, Dawn Desk')
- GREEN: Test Files 1 passed · Tests 5 passed
- B170 (the option «مستخدم»): × same test — Unable to find the text
- B170b (the desk line dropped): × same test — Unable to find the text (the line before the act)

## C6.9 (see log) fix(space-links): word a link from a fresh read (47)
- RED (HEAD's useLinkOwnerDialog + useLinkOwner copied in, restored): × a space linked meanwhile is worded as another owner — Unable to find text "They become another owner of this space."
- GREEN: Test Files 1 passed · Tests 7 passed (space-links whole: 23 files, 163 tests, before the textContent fix)
- B171 (the editor's read, verified false): × a space linked meanwhile… — expected '…' to contain 'They become another owner of Focus Hub; it stays verified.'

## C6.11 5169d31f feat(data-reports): filter by who handles them (45)
- RED (HEAD's six source files copied in, restored): × «يعالجه» filters by ADMIN or OWNER — Unable to find radiogroup "Handled by"; × names an English-only space in the sheet’s Arabic title — Unable to find dialog "Focus Hub · ساعات العمل"
- GREEN: data-reports components+hooks: 10 files passed; 1 × "needs details for «Other» only" (useReportDialog, untouched) timed out at 5000 ms in the whole run, passed alone (2 files, 10 tests) — machine load
- B178 (handledBy not sent): × … expected { page: 1, limit: 20 } to match object { handledBy: 'ADMIN' }
- B178b (the field title for the admin): × both — Unable to find dialog "Focus Hub · Opening hours"
- the admin's useDecideSheet test's dialog name updated to the new title

## Rebase onto 0a1979e1 (2026-10-31)
- one conflict: docs/features/audit.md › History (A1's #PRNUM API line and my Web history): both kept.
- A1's `user.replaced` reached AUDIT_ACTIONS: T150 and the groups' test went red at once (expected [ 'user.replaced' ] to deeply equal []) → words «استبدال حساب منتهٍ» / "Expired account replaced", folded into C6.1 (fixup + autosquash).

## C6.5 b42e9773 feat(space-links): land the spaces the admin keeps (50)
- RED (HEAD filtersOf): × offers every status… (4 not 5 choices); × ?status=editable selects «تعدّلها الإدارة» — toHaveTextContent
- B166 (editable falls back to all): × ?status=editable selects…
## C6.7 a54a1964 fix(space-links): read the email's account exactly (49)
- RED (HEAD useEmailAccount): 3 × — expected [ { q } ] to deeply equal [ { email } ]; Unable to find "Couldn’t check this email right now."
- B168 (q read): 2 × params; B169 (failed as notFound): × a failed read says so and retries
## C6.6 feat(space-links): link the owner a refusal names (48)
- RED (HEAD useAddOwnerForm + AddOwner): × ALREADY_OWNER offers «اربطه بالمساحة»… — Unable to find "This email is already an owner’s."
- B167 (the refusal not caught): same ×
- GREEN: add-owner, its hook, link: 3 files, 26 tests

## C6.13 166d6760 fix(space-links): finish the owners and users (45)
- RED (HEAD's AddOwner, useAddOwnerForm, OwnersList, useOwnersList, ListState, userRowView): × offers «Add owner» when there is no owner yet… (toHaveClass sr-only); × ?sheet=add opens the add sheet… (no dialog "Add owner"); × ACCOUNT_SUSPENDED links the users page… (timed out finding the link); unit × 3 «words the role… when it joined» (no year)
- B183 (?sheet ignored): × ?sheet=add opens… — Unable to find dialog "Add owner"; B184 (plain text): × ACCOUNT_SUSPENDED… — Unable to find link "restore it first"
- the useAdminSpacesList hook test (C6.5's five statuses) folded into C6.5 by fixup; userRowView's unused `now` removed with its callers and OwnerActionsMenu's test
## C6.17 1f53e481 fix(admin): reach a held user action by keyboard (48)
- RED = B190 (`disabled` back): × the users page’s held items are reached by the keyboard — expect(element).toHaveFocus()
## C6.16 adc3eb2a feat(spaces): show a photo's upload as a bar (44)
- RED (HEAD PhotoUploadTile): × an uploading tile shows a progressbar… — Unable to find progressbar "Uploading photo 4"
- B189 (the spinner for an uploading tile too): × — Found multiple elements with the text /^Uploading \d+%$/
- prototype: check-parse 50/50 blocks; check-classes 333 classes, 5 dead uses (as before), 0 new
## C6.12 ba8fedc4 fix(spaces): finish the spaces list and editor (46)
- RED (HEAD's eight source files, the new copy kept): 5 × — hiding offers «تراجع» (B180's state); a verified row’s menu… (B179); the phone’s sheet closes on «عرض N نتيجة»… (B181); a section’s header action leads its content below 768 (B182); a verified space’s notice leads to its reports. Each test red for its own change on the HEAD code = its break.
- GREEN: 4 files, 85 tests (editor, menu, hide, admin-list)

## C6.14 b03acccb fix(lookups): keep switches in rows, add positions (50) — second agent
- RED (tests first, HEAD code; c614/red.txt): T185 × the edit sheet has no active switch (LookupSheet + AmenitySheet) — expected document not to contain element, found <button role=switch>; T186 × a list of 11 offers «الترتيب»… — Unable to find textbox "Position" (areas and amenities); T187 × an arrow's name holds its position; a move is announced — Unable to find button "Move down: Al-Rimal — 1 of 2"; tab hint × — Unable to find text "An inactive amenity is offered in no form…"; hooks × (active still present, isActive sent); unit placed × "placed is not a function"; withPosition × Cannot find module './withPosition' (moved aside, restored).
- GREEN: lookups component 27 files / 146 tests; lookups unit 3 files / 23; routes file alone 68/69 (× only "lists the owner’s twelve pages" — empty body, first lazy load, finding 87; the lookups-page tests pass there; filtered -t run: the lookups test first misses the same way).
- B185 = the red (HEAD's sheet kept the switch). B186 (offered at 10: `>=`): × a list of 10 offers no position… . B187 (live region removed): × an arrow’s name holds its position; a move is announced.
- typecheck 0 (11:06–11:08), lint 0 (11:08–11:12), via grant; prettier, eslint on touched, check:links, check:classes clean.

## Rebase onto a417ed04 (2026-10-31, second agent)
- conflicts, all docs/features/space-links.md: History (W1's two lines + mine: both kept); Code map Web (mine) + Web (staff) (HEAD's); Open findings at C6.5 (158 closed by me, 106 resolved by W1: neither kept). No code conflict.
- touched tests after rebase: unit 8 files/37, component 33 files/371 green; 1 unhandled error: sonner `setPointerCapture` in useSetSpaceHidden's undo test (userEvent.click on a toast action) → plain `.click()` in act, folded into C6.12.
- finding 105: Resolution + status written, line removed from space-links' open findings, folded into C6.17.

## C6.15 4be63ad4 feat(lookups): name the retired amenities kept (46)
- RED (tests first): × "the owner’s checklist names a retired amenity, marked, and drops it when unticked" — Unable to find checkbox "Generator No longer on the platform’s list"; hook × expected [2 items] to equal [3 items]; admin mark × [1, undefined].
- B188 (retired not listed): × both owner tests. B188b (section hands []): × "hands the checklist the retired amenities the space holds".
- GREEN: lookups + spaces amenities/editor 28 files / 159.

## C6.10 656984d9 feat(data-reports): open a report beside its field (50)
- code first; red by breaks (backup copy, restored): B172 (notice not drawn before its section): × a report in the address shows its notice above its section; B173 (PATCH not sent): × «تم التصحيح» resolves it in place — expected undefined to be '/manage/spaces/7/data-reports/41'; B174 (owner named): × the owner’s notice says «زائر», the admin’s the name; B174b (decided drawn) and B174c (verified drawn): × draws nothing for…; B175 (no ?report in the link): × leads the owner to the field’s section… ; B175b (list passes no id): × decides a new report… (href); B176/B176b (?open ignored): × ?open= opens that report’s sheet… (owner 2, admin 1); B177 (landing before the read): × the editor scrolls to and focuses the card its hash names once drawn, × lands on a section’s inner part.
- GREEN: component data-reports+spaces+lookups+admin/space pages 73 files / 480; unit 19 files / 99.
## 4d709ef0 docs: record finding 210
