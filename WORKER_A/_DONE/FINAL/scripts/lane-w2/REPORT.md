# Lane W2 — hand-over (returned as text; saved by the lead)

Lane W2 · HAND-OVER · 14 of 17 commits · Branch lane/w2 head ba8fedc4 (base 0a1979e1, rebased as asked).
C6.14 (`fix(lookups): keep switches in rows, add positions`, D6.12, T185–T187) buildable but not made — the agent's
context was running out; C6.10 waits for A2's C2.14, C6.15 for C2.15. Lane-wide test runs not yet done.

Commits: b5af2379 feat(audit): show a space's audit log (37) · b8c6ad0e feat(audit): show the platform's audit log (42)
· 38317508 feat(platform-settings): edit the settings (42) · 11607a0c feat(platform-settings): read the public contact
(48) · d09b897a fix(space-links): name a person's front desks (45) C6.8 · 378ca134 fix(space-links): word a link from a
fresh read (47) C6.9 · 386f4982 feat(data-reports): filter by who handles them (45) C6.11 · 59b63b19 feat(space-links):
land the spaces the admin keeps (50) C6.5 · de533977 fix(space-links): read the email's account exactly (50) C6.7 ·
21fd3a3f feat(space-links): link the owner a refusal names (49) C6.6 · 166d6760 fix(space-links): finish the owners and
users (45) C6.13 · 1f53e481 fix(admin): reach a held user action by keyboard (48) C6.17 · adc3eb2a feat(spaces): show a
photo's upload as a bar (44) C6.16 · ba8fedc4 fix(spaces): finish the spaces list and editor (46) C6.12. Fixups folded:
`user.replaced`'s words («استبدال حساب منتهٍ» / "Expired account replaced") into C6.1; the five-status hook test into
C6.5.

Red/green (`scripts\lane-w2\notes.md`): code first in every commit; red shown by moving new files aside or copying in
HEAD's versions, restored from backups: C6.1 "Cannot find module './actionWords'" +3 · C6.2 the stub → 3 failed · C6.3
PlatformSettingsCards unresolvable · C6.4 2 failed, no link from GET /settings/public · C6.8 option text missing · C6.9
"They become another owner of this space." missing · C6.11 radiogroup "Handled by" and dialog "Focus Hub · ساعات
العمل" missing · C6.5 4 choices, not 5 · C6.7 `{q}` sent, failed-read line missing · C6.6 "This email is already an
owner's." missing · C6.13 3 component + 3 unit (join date without year) · C6.17 held item not focused · C6.16 no
progressbar "Uploading photo 4" · C6.12 5 failed, one per gap. Green: every touched file; space-links whole 23 files /
163; C6.12's four files 85; data-reports 10 files.

Breaks (backup copy, red): B150–B171, B178, B178b, B183, B184, B189, B190 (each line in `break-*.txt`); B179–B182 by
C6.12's red.

Heavy checks: typecheck 0 and lint 1 → fixed (10-29, C6.1+C6.2 tree); on head ba8fedc4 (10-31): lint 0 (08:33–08:37),
typecheck 0 (08:37–08:38). Per commit: eslint on touched files, `tsc -p apps/web/tsconfig.app.json`, prettier,
check:links, check:classes. **Not run yet:** test:unit and test:component whole.

Shared files: architecture §3 platform-settings paragraph · setup.md VITE_CONTACT line · `.env.example`,
`vite-env.d.ts` (VITE_CONTACT_* removed) · `pages/site/routes.component.test.tsx` (`renderPublicSite` takes a contact,
answers `/settings/public`) · `src/test/auditEntry.ts` (new) · CHANGES.md one row (74) · the prototype change in
`docs/design/prototype/masaha/profile-b.jsx` (check-parse 50/50, check-classes 0 new) · copy audit, platformSettings,
spaceLinks, dataReports, spaces (own sub-objects) · features audit, platform-settings, space-links, spaces,
data-reports.

Findings closed: 14, 94, 95, 158, 89, 83, 73, 74. 105: admin side done (C6.17), file untouched (W1 did the staff
side) — the lead marks it.

Decisions (none SERIOUS): L-W2-D1 (EC19) ALREADY_OWNER opens the link dialog in place from the add sheet, the owner read
by exact email, the sheet's space chosen (no user-by-id read exists) · L-W2-D2 a deleted target is never a link (T157
over D6.1's `?status=deleted`); «في {space}» hidden when the target is that space · L-W2-D3 the admin's actor filter
offers people only (the contract's admin `actor` takes an id) · L-W2-D4 an extension's details count `subscriptionIds`
only; a price correction with a null price shows its reason · L-W2-D5 new "not found" line «لا حساب بهذا البريد تمامًا
الآن…»; `refusals.ALREADY_OWNER` and addOwner's ACCOUNT_SUSPENDED line gone · L-W2-D6 «عرض N نتيجة» its own words in
spaceLinks and audit · L-W2-D7 the space-owners read moved to the hooks root; `userRowView` lost its unused `now` ·
L-W2-D8 «تراجع» reuses `toasts.undo`; 10 s; no undo of the undo · L-W2-D9 «يعالجه» also a removable tag, counted.

Notes: site routes' "shows the Directory under its title" fails the same on HEAD's files (finding 87) — re-check in the
full run; useReportDialog "needs details for «Other»…" and admin AuditPage "the filters are in the address…" timed out
once under load, passed alone. Real run: the audit at 390/768/1024; settings cards max-w-3xl; a section's action
leading on a phone; a saved contact on About (5-minute cache).

## Hand-over 2 — the second agent (C6.14)

Lane W2 · HAND-OVER · 15 of 17 · head b03acccb (base 0a1979e1), clean. **b03acccb fix(lookups): keep switches in rows,
add positions (50) C6.14** — G30.1 no Active switch in the edit sheets (row only; `isActive` no longer sent; its copy
removed); G30.2 «الترتيب» / "Position" in a list of more than ten (1–n, Arabic-Indic digits, helper and error «من 1 إلى
{n}»), saved after the names through the list's order route as the whole order (EC21, `PUT …/order {ids}`), nothing
sent unchanged; G30.3 arrows named «تحريك لأعلى: {name} — {i} من {n}», the row keeps focus, a polite live region in the
row says «{name}: {j} من {n}»; G30.4 a hint per tab. New `services/withPosition.ts`, `placed()` in `services/moved.ts`,
`hooks/useRowPosition.ts`, `components/sheet/PositionField.tsx`, `types/{RowPlace,PositionFieldView}.ts`; lookups.md.
Tests first: T185 × "the edit sheet has no active switch" (found a switch); T186 × "a list of 11 offers «الترتيب»…"
(no textbox Position); T187 × "an arrow's name holds its position…" (no button 'Move down: Al-Rimal — 1 of 2'); the
tab-hint test ×; unit `placed` not a function, `withPosition` cannot find module. Green: lookups component 27 / 146,
unit 3 / 23. Breaks B185 (= the red), B186 (position at 10) ×, B187 (no live region) ×. Lint 0, typecheck 0 on b03acccb
(11:06–11:12). Shared: `pages/dashboard/routes.component.test.tsx` (its lookups hint test), `LookupsPage.tsx` (hint
per tab). Decisions (none SERIOUS): L-W2-D10 a hand-written FormSchema wrapper `withPosition` (the web has no zod) with
`custom` issues mapped by `toFieldErrors` · L-W2-D11 the position saved through the list's existing order mutations ·
L-W2-D12 the live region per row, count fixed when the sheet opens · L-W2-D13 `lookups.hint` → `lookups.governorates.
hint`, `lookups.amenities.hint` added. Left out: CHANGES G5's "the sheet's save keeps its toast" (not asked by D6.12;
the screen fires no toasts by decision). Finding-87 misses noted (dashboard routes' first test; site routes' Directory).

## DONE — the second agent (2026-10-31)

Lane W2 · DONE · 17 commits + `docs: record finding 210` · head bb05d6aa (base a417ed04), clean. Commits (order: C6.10 and
C6.15 last): ac75fa47 C6.1 · 7b8f9122 C6.2 · c1d22f00 C6.3 · c8568d32 C6.4 · 1b332812 C6.8 · 096630ab C6.9 · 40cc2ee8 C6.11
· d366198f C6.5 · 0770b364 C6.7 · 24a0cfd1 C6.6 · 5f07169c C6.13 · 6f5b808a C6.17 · d3df446f C6.16 · 2deebd67 C6.12 ·
ef94985a C6.14 · 9b397d03 C6.15 `feat(lookups): name the retired amenities kept` (46) · 2dd7289a C6.10 `feat(data-reports):
open a report beside its field` (50) · bb05d6aa docs: record finding 210 (24).

Rebase onto a417ed04: conflicts only in `docs/features/space-links.md` (History both kept; code map both Web lines; Open
findings at C6.5: neither line — 158 closed here, 106 by W1). After it: unit 8 files / 37, component 33 / 371, one
unhandled error (sonner's `setPointerCapture` in C6.12's undo test → a plain `.click()`, folded into C6.12). Finding 105
written in a fold into C6.17. The lane unit run caught `rowView.unit.test.ts` still expecting «غير مُدخلة:» → fixed, folded
into C6.12.

C6.15 tests first: T188 × "the owner's checklist names a retired amenity, marked, and drops it when unticked"; the hook ×
(2 items, not 3) → 28 files / 159. C6.10 code first, red by breaks → 73 component files / 480, 19 unit / 99. Breaks:
B188, B188b · B172 · B173 ("expected undefined to be '/manage/spaces/7/data-reports/41'") · B174, B174b, B174c · B175
("'/dashboard/spaces/7/profile#hours' to be '…?report=41…'"), B175b · B176, B176b · B177 ("Expected element with focus").

Lane-wide (grant, 10-31): lint 0 (12:38–12:41) · typecheck 2 (the worktree's Prisma client predated M2 → `prisma
generate`) then 0 (12:55–12:56) · unit web 1 failed (rowView, fixed, folded) then **179 / 1153** · **component whole 324
files / 1881 tests, exit 0, no finding-87 miss** (12:43–12:53, before the last unit-only fold) · check:classes 0,
check:links 3173.

Shared: `pages/dashboard/fieldSections.ts` (`ownerFieldLink`, `adminEditorLink`, a new unit test); `dataReports.notice`
copy; `features/spaces` SpaceEditor `noticeFor` slot, `useHashLanding` (new), headings `tabIndex={-1}` on SectionCard,
PricesLinkCard, ReadOnlyCard, PhotosCard and the location h3, `AmenitiesFieldProps.retired`.

Findings closed: 14, 73, 74, 83, 89, 94, 95, 99, 105, 158, 184. New: **210** "A later hash change in the space editor
focuses nothing" (`useMainFocus` focuses the named card, a div that takes no focus — the shell's hook, U0's).

Decisions added (none SERIOUS): L-W2-D14 retired amenities listed after the catalogue's, marked «لم يعد في قائمة المنصة»,
kept listed when unticked until the save; the admin's mark stays «غير نشط» · L-W2-D15 the notice resolves with no reply
and keeps «عُلّم «تم التصحيح»» after its read answers decided; the admin's draws nothing for a verified space's report or
another space's; only in the editable editor and above Packages' prices · L-W2-D16 «أخرى» lands on `#report`; the hash
landing runs only in the editor · L-W2-D17 the lists read one report by id only when not shown; `?open` removed on close
(replace); both single reads `retry: false`.
