# Lane W3 — hand-over 1 (returned as text; saved by the lead)

Lane W3 · HAND-OVER · head b7a9e740 (base 56e639c6), clean. The agent's context nearly used up. Made: c1eec78c fix(desk):
focus the write-off's reason first (45) C7.1 · 9a594a45 feat(desk): show a day's log beside who is here (47) C7.2 ·
da9face0 fix(desk): order the phone's desk and its states (48) C7.6 · 80d531f4 fix(desk): count a full space and show
the rates (48) C7.9 · b1a83af7 feat(desk): name the file a phone adds to (41) C7.10 · 5125a3c7 fix(desk): say a refused
payment recorded nothing (49) C7.11 · e7c8c055 feat(desk): say a usage subscriber's due at out (47) C7.12 · d1c9971e
fix(desk): finish the subscription sheet (40) C7.13 · b7a9e740 docs(visits): name the desk's screen (36) C7.14.
Buildable, not made: C8.1, C8.4, C8.6. Waiting on A2: C7.3 (C2.10), C7.4 (C2.7), C7.5 (C2.8), C7.7, C7.8 (C2.13), C8.2
(C2.12), C8.3 (C2.9), C8.5 (C2.11), C8.7 (EC10: yes, `owners` answered).

Red/green (`scripts\lane-w3\notes.md`): C7.1 × "focuses its reason on opening, not «Back»" (focus on Back; the test drops
`autoFocus` as a browser does; re-shown from backup after the restart) → 2 files / 4 · C7.2 T200 "Cannot find module
'./logRows'" → DeskLog 4/4, logRows 2/2, copy+repository unit 46/46 · C7.6 tests after the code, reds = B210, B210b,
B211 → 41/41 · C7.9 B216–B218 → check-in 5, check-out 2, DeskPage, money/collect/pay 21, copy 33 (first typecheck exit 2
— DeskSearch test passed `full: false`; fixed, 0) · C7.10 B219 → debt 4, check-out/uncollected 17 · C7.11 B220 → 37 + 63
· C7.12 B221, B222 → DeskPage 5, subscriber/search 23 · C7.13 T224 "Cannot find module './endNote'", B223, B225, B225b
→ sheet 7, sheet hooks 18, desk services+copy unit 79.

Breaks (backup copy, restored): B200 · B201 · B202 · B203 · B209 · B210 · B210b · B211 · B216 · B217 · B218 · B219 · B220
· B221 · B222 · B223 · B224 · B225 · B225b — each × its test (lines in `break-*.txt`).

Checks: per commit eslint (grant) and `npm run typecheck`, final runs exit 0 (C7.13's eslint first 3 `String()` errors,
fixed); last lane-w3 END 2026-10-31 09:17:44 UTC. Lane-wide checks not run yet. routes test: "refuses reception the
owner's payments…", "shows reception its own payments today" missed once (finding 87). A loaded wide run: 8 timeouts
≈ 5 s, each file green alone, but its own new 429 assertion (fixed: a warning alert is not role=alert).

Shared files: `features/desk`, `features/occupancy`, `pages/dashboard/space/desk/*`, copy desk.ts (new `log`, `usageOut`;
lines in `uncollected`, `visit`, `checkOut`, `debt`, `failure`, `sheet`), features desk, occupancy, visits docs,
finding 172. Findings closed: 172 (C7.1).

Decisions (none SERIOUS): LW3-D1 the test mocks Textarea to drop `autoFocus` · LW3-D2 the TabsList above both panels, the
log its own h2 «السجل»; view/day/page in the address (`view=log`, `logDay`, `logPage`); reception's visits read with no
range, check-ins today's Gaza date · LW3-D3 two tests changed to the new decisions; offline drawn locally in each list ·
LW3-D4 money block side by side from 768 everywhere; a capped charge's line leaves out "= amount" (the web never
computes) · LW3-D5 one match names the file, none says new, two say nothing · LW3-D6 one `PhoneInput` · LW3-D7 the usage
dialog lives in DeskPage (`usageOut`), payment on the subscription with its own key, focus to who-is-present's heading
on close · LW3-D8 the end note counts days when set, else hours; the published rate the shift's, else HOUR/DAY;
prefilled only while untouched; `sheet.calendar` words.

Notes: C8.1 — a list row knows presence only through a subscriber check-in (a VISIT PresentPerson has no customerId); its
«تجديد» needs the subscription read first. Real run: desk tabs, the log at 390/768/1440, the empty uncollected card
hidden below xl, money block side by side from 768, the sheet's date pickers, the status control's chevron. A stray
file `C:\dev\masaha\workspace\x` was written and deleted by the agent.

## Hand-over 2 — the second agent (U7 complete)

Lane W3 · HAND-OVER · U7's 14 commits made; U8 (C8.1–C8.7) not started; lane-wide checks not run. Head 7a8c2c9a (base
a417ed04), clean. Rebase onto a417ed04: History conflicts only (`occupancy.md` C7.6: A2's audience line then W3's offline
line; `visits.md` C7.14: A2's API line then W3's "### Web history"), both kept; nine earlier commits re-tested
(component 46 / 188, unit 26 / 102); Prisma client regenerated.

Commits: 8c2a6e6a C7.1 · c4296cf1 C7.2 · 42636931 C7.6 · f3944560 C7.9 · 99fd162d C7.10 · bba42da4 C7.11 · 9ae78122 C7.12 ·
1bb39a9b C7.13 · 8830740a C7.14 · 63599430 feat(desk): list and undo the written-off visits (48) C7.3 · 9ddb40fa
feat(desk): check a customer in as their visit (46) C7.4 · 1bde1334 feat(desk): send the price the sheet showed (43) C7.5
· ddaa8082 feat(desk): link names and word who is here (43) C7.7 · 7a8c2c9a feat(desk): renew or subscribe from the desk
(44) C7.8.

Red/green: C7.3 written first, × 4 "Unable to find role="radio" and name "Written off"" → 5 + 9; repository test by break
RWO ("expected {} to deeply equal { page: 2 }") · C7.4 T207 red (the "not added to the file" line still shown) → 18, copy
33 · C7.5 T208 × "subscribes from a published price…" (…(3) vs …(4)), × "keeps the sheet open on a changed price…"
(refreshPrices called 0 times) → sheet 27, services 46 · C7.7 T212/T213 ("no link Sara", "Visit · student" missing) → 47
files / 197, unit 45 · C7.8 T214/T215, CustomerCard × 4 → 180, unit 79 · final at head: component 48 / 202, unit 26 /
103. Breaks: B204, B205 (`retry: 1` → 2 requests), B206, RWO, B207, B208, B208b, B212, B212b, B212e, B213, B212c, B212d,
B212f, B214, B214b, B215, B215b — each × its test. Per commit prettier, eslint and typecheck (grant), last exit 0 (C7.3
typecheck 2 first — stale Prisma; C7.8 eslint 1 first — `fetchQuery` deprecated → `client.query`).

Shared: copy desk.ts (`writtenOff`; `customer.notHere`, `customer.renewFailed`; `subscriber.pre.asVisitNote` removed),
occupancy.ts (`present.studentVisit`; Arabic `HOURS_2` «ساعتين»); `features/occupancy` (`PresentRowView.kind`,
`customerId`, `time`; `PresentPeople`, `PresentName`; `PresentList`/`PresentMatches` take `people`; `usePresentList` a
`plan` option); DeskPage (`fileLink` to UncollectedCard, `people`); desk.md, occupancy.md.

Findings closed: 172 (C7.1), 164 (C7.3), 160 (C7.4), 171 (C7.5).

Decisions (none SERIOUS): LW3-D9 (C7.3) a ToggleGroup in the card header, local state, its page in the address
(`writtenOffPage`); undo's toast reuses `writeOff.undone`; **gap:** an empty card stays hidden below xl (D7.6), so an
owner on a phone with nothing uncollected cannot reach the written-off view · LW3-D10 (C7.7) the plan and the file link
come from the page through occupancy's `people` prop (from `useOpenCheckIns`, now returning `plan`); a visit's present row
has no `customerId`, so only subscribers' names link; «ملاحظة»'s optional mark reuses `desk.visit.optional` · LW3-D11
(C7.8) «غير حاضر» on every search card (present subscribers are the search's first group); a customer here on a visit is
not known to the state now; «تجديد» reads the statement first (`useRenewEntry`), a failure toasts with a retry;
`progressLines` split, `limitLines` exported.

Notes for U8: a `components/menu/CustomerActions.tsx` already exists — choose another name for D8.1's component;
`CheckOutAction` reusable for the file header (build the `PresentPerson` from `file.present`; fill `audience`,
`chargeNowAgorot`; terms from `useVisitTermsQuery`); the customers list knows nobody's presence and has no pay dialog
(CustomersPage would need `useStateNowQuery` and its own `PayDialog`); the oldest item's amount is unknown in the list
without the file; `PayDialog` with `{customerId}` alone opens on the oldest item; the file card's «تجديد» is on the
latest card only — D8.1 adds "only while ENDING_SOON or EXPIRED". Helpers in `scripts\lane-w3\py\`.

## DONE — the third agent (U8)

Lane W3 · DONE · head 3b333337 (base a417ed04), clean, 22 commits. U8: 0598e391 feat(desk): offer a customer's actions by
state (47) C8.1 · c22b17c2 feat(desk): remind a customer on WhatsApp (41) C8.2 · 8418fa71 feat(desk): name who recorded
and voided (40) C8.3 · e6785b55 feat(desk): correct a subscription from its card (48) C8.4 · 5b6898ca feat(desk): filter
customers by week and month (46) C8.5 · 7c4cd2d6 fix(desk): finish the customers list and file (45) C8.6 · c1317e89 docs:
record finding 212 (24) · 3b333337 feat(payments): name the space's other owners (45) C8.7.

Red/green: C8.1 T230–T232 × 3 → 3; desk component 15 / 55; unit 79 · C8.2 T233 × 2 → 16 · C8.3 T234 Statement × 2,
CustomerFile × 1 → 20 · C8.4 T235–T238 × 6 → 6 + 14; repository by break RCS · C8.5 T239 → 14 · C8.6 T240–T243 × 5 → 14
files / 63 · C8.7 T244 ('Mona' ≠ 'Mona · owner'; ledgerPeople, useSpaceOwners missing) → payments component 24, unit 49.
Breaks: B230, B230b, B231, B232, B232b, B233, B233b, B234, B234b, B235, B236, B237, B238, B235g (B235f green — Radix's first
focus already lands on the name; the handler dropped), RCS, B239, B240–B240c, B241, B242–B242c, B243, B243b, B243c (first
green — the test found «Clear filters»; strengthened, then ×), B243d, B244, B244b.

Lane-wide (grant, 10-31): lint 0 (12:15:57–12:22:04) · typecheck 0 · unit web 175 / 1134 · component whole 325/328 files,
1877/1880 tests (alongside lint) — 3 "timed out in 5000ms": SpaceSettingsCards "titles each card…", AnnouncementSheet
"focuses the checked type first…", AccountLayout "names its navigation «My account»…" (none in its diff); alone:
SpaceSettingsCards, AnnouncementSheet pass; AccountLayout 1 failed / 2 passed twice — "opens «Favourites» signed in…"
("Unable to find role=navigation My account" at 3011 ms; the lazy first import of /me/favorites; passed in the full run)
— not proven against the base: **the lead's run checks it** · check:classes 1831 · check:links 3176.

Shared: copy desk.ts (`actions.oldest`; `file.hereSince` replaces `here`, `reminder`, `unpaid.counts`; `statement.
recordedBy`, `voidedReason` removed; `correct`), payments.ts `ledger.staff.owner`; `features/spaces/index.ts`
`useSpaceOwners`; payments `ledgerPeople`, `LedgerPerson.owner?`; desk `PayTarget.oldest?`, `useCheckOutSubscriber`
takes `person | null`, `UncollectedRow.payments?`, `currentOf` to `services/currentOf.ts`; pages CustomersPage (top-bar
button removed, `add` to the list), CustomerPage (space name from `useMySpacesQuery`), PaymentsPage (`useSpaceOwners` +
`ledgerPeople`), new `PaymentsPage.component.test.tsx`; docs desk.md, subscriptions.md (new "### Web history"),
payments.md, spaces.md.

Findings closed: 162 (C8.3), 163 (C8.4), 166 (C8.7) (+ 172, 164, 160, 171 earlier). Recorded **212** "An owner on a phone
cannot reach the written-off visits" (Open).

Decisions (none SERIOUS): LW3-D12 `components/customer-actions/StateActions.tsx` + `useStateActions` (the old
`menu/CustomerActions.tsx` kept, takes `state="menu" | "buttons"`); the list's «⋯» reads the file when it opens; «حضور»
only on ACTIVE/ENDING_SOON; the oldest item `openItems(file)[0]`; «أقدم بند: {item}» via `PayTarget.oldest`; a present
visit's person `audience: 'GENERAL'`, `chargeNowAgorot: null`; dialogs in `StateDialogs` · LW3-D13 the reminder's space
name from `useMySpacesQuery` (Arabic first), the first-name rule local · LW3-D14 «سجّلها {name}», voids via the ledger's
line · LW3-D15 one `useServerForm`, only changed fields (vs the last answer), PATCH then PUT, `endsOn` out_of_range,
SUBSCRIPTION_ENDED / PRICE_BELOW_PAID, blank limit null, the card's «⋯» named «More actions: {subscription}», held when
ended early · LW3-D16 local `KIND_ORDER` · LW3-D17 «زبون جديد» at the chip row's end and in the empty state; the owner's
write-off from the file via `WriteOffDialog`; the only-visits line only with no unpaid visit; the ledger's empty icon by
whether «مسح الفلاتر» shows · LW3-D18 pure `ledgerPeople`; `useSpaceOwners` wraps `useSpaceQuery('owner')`.
