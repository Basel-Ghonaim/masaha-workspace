# R2-AD-VD — Round 2 review: the admin's dashboard · visual design and consistency

- HEAD: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- origin/main: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- Match: yes. Detached at `origin/main`, worktree clean. (Note per the prompt: the stray `<<<<<<< HEAD` line before `INDEX.md` §54 was not re-checked/reported.)

## Verdict

The admin's visual system is coherent (one shell, one toolbar/pagination vocabulary, settled badge semantics applied almost everywhere), but four consistency breaks — destructive red on role-grant, `warning` for hidden, a Select where the pattern demands chips, and unmuted deleted rows — plus toolbar/count drift between lists should be fixed before build.

## Five most important points

1. "Make them an admin" is a destructive-red button; granting access is not destruction.
2. «مخفية» is `warning` (amber) in `SpaceStatus` and lookups, but hiding is settled `neutral`.
3. Owners' 3-choice status filter is a Select while Reports' 4-choice status filter is chips (P5).
4. Deleted spaces are only name-muted; the rest of the row/card reads as live.
5. List toolbars use two different grids (spaces `grid md:grid-cols-3` vs owners/users flex) and the count line is worded five ways.

## Issues

### R2-AD-VD-001 — Granting admin uses destructive red

- **type:** defect · **level:** component · **impact:** high
- **where:** frame "Users — Change role" (INDEX §46), `http://127.0.0.1:5416/Admin users.html?changerole=1`, 1440 light; archive screen `docs/design/screens/46-admin-users/05-change-role-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-001.png` (not captured — no browser in this runner; see §6. Closest archive frame above; source `docs/design/prototype/Admin users.html:100-110`)
- **what is wrong:** the role `AlertDialog` uses `<AlertDialogAction variant="destructive">` for both directions. "جعله أدمن" (grant every admin power) renders in destructive red, the same treatment as suspend/delete/unlink. Red here means danger for a non-destructive, access-granting act.
- **proposal:** keep `variant="destructive"` only for admin→user (loses the dashboard at once); use the default/primary variant for user→admin. One rule: red ends access, never grants it.
- **why:** red keeps one meaning (loss/destruction), so the admin reads the button's weight correctly at the moment of highest consequence.
- **cost:** S
- **rule:** foundation §5 (destructive = delete, deactivate, errors) and §11 (verified pairs); DECISIONS_ADMIN A5 (role change is an AlertDialog naming the consequence — the consequence differs by direction).

### R2-AD-VD-002 — «مخفية» is warning instead of neutral

- **type:** defect · **level:** pattern · **impact:** medium
- **where:** frames "Spaces" (INDEX §43) `http://127.0.0.1:5416/Admin spaces.html` and "Governorates and areas" (INDEX §47) `http://127.0.0.1:5416/Admin lookups.html`, 1440 + 390 light; archive screens `docs/design/screens/43-admin-spaces/01-spaces-desktop-1440.webp`, `docs/design/screens/47-admin-lookups/01-governorates-and-areas-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-002.png` (not captured; see §6. Sources `docs/design/prototype/masaha/admin.jsx:94`, `docs/design/prototype/Admin lookups.html:45`)
- **what is wrong:** `SpaceStatus` renders `{s.hidden && <Badge variant="warning">مخفية</Badge>}` and lookups' `HiddenB` is `variant="warning"`. Hidden is a steady visibility fact, but amber is the attention role already used for «ناقصة»/«قديمة», so hidden rows compete with rows that need work.
- **proposal:** `variant="neutral"` for every «مخفية» badge: `SpaceStatus`, lookups `HiddenB`, and the space options inside the link dialogs/sheets that reuse `SpaceStatus`. Warning stays exclusively for missing/stale.
- **why:** two facts read as two colours (G3/A3): verification state vs visibility vs attention, scannable at a glance.
- **cost:** S
- **rule:** DECISIONS_ADMIN amendment 2026-10-12 ("hiding is `neutral`"); A3 (verification + «مخفية» as two facts); foundation §5.

### R2-AD-VD-003 — Owners status filter is a Select, Reports status filter is chips

- **type:** defect · **level:** pattern · **impact:** medium
- **where:** frames "Owners" (INDEX §44) `http://127.0.0.1:5416/Admin owners.html` vs "All reports" (INDEX §45) `http://127.0.0.1:5416/Admin reports.html`, 1440 + 768 light; archive screens `docs/design/screens/44-admin-owners/01-owners-desktop-1440.webp`, `docs/design/screens/45-admin-data-reports-all-spaces/01-all-reports-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-003.png` (not captured; see §6. Sources `Admin owners.html:142-144`, `Admin reports.html:64`)
- **what is wrong:** P5 settles a single status filter of four or fewer choices as `ToggleGroup` chips. Owners has one status filter with two choices (active/suspended) yet hides it in the `FilterSheet` Select; Reports (all + 3 statuses = 4) correctly uses chips. Same job, two controls; owners costs an extra tap and reads differently.
- **proposal:** owners status becomes a `ToggleGroup` row (All / Active / Suspended) placed like Reports' chips; the sheet goes away on that page until a second filter needs it.
- **why:** one filter vocabulary — the admin recognises a ≤4-choice status filter as chips on every list.
- **cost:** S
- **rule:** P5 (DECISIONS_SHARED); lens B.4.

### R2-AD-VD-004 — Deleted rows are not muted as rows

- **type:** defect · **level:** page · **impact:** medium
- **where:** frame "Spaces" (INDEX §43), `http://127.0.0.1:5416/Admin spaces.html?status=deleted`, 1440 + 390 light; archive screen `docs/design/screens/43-admin-spaces/01-spaces-desktop-1440.webp` (filtered state has no archive frame)
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-004.png` (not captured; see §6. Sources `Admin spaces.html:47-54,70-76,102-111`)
- **what is wrong:** A3 settles muted deleted rows. Only the name cell is muted (`text-muted-foreground`); area, owner, last-update cells and the card meta line (`AD.areaName · المالك · date`) render exactly as on live rows, and the freshness cell collapses to "—". A deleted row scans as live except for one word.
- **proposal:** mute the whole deleted row/card content (`text-muted-foreground` on area/owner/date/meta cells, keep the «محذوفة · date» line), leaving only «استرجاع» at full emphasis.
- **why:** deleted reads as deleted in a long list; the single way back stays the visual focus.
- **cost:** S
- **rule:** DECISIONS_ADMIN A3 ("muted rows with «استرجاع»").

### R2-AD-VD-005 — Row visibility switch has two designs

- **type:** defect · **level:** pattern · **impact:** medium
- **where:** frame "Governorates and areas" vs "Amenities" (INDEX §47), `http://127.0.0.1:5416/Admin lookups.html` and `http://127.0.0.1:5416/Admin lookups.html?tab=amenities`, 1440 light; archive screens `docs/design/screens/47-admin-lookups/01-governorates-and-areas-desktop-1440.webp`, `docs/design/screens/47-admin-lookups/05-amenities-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-005.png` (not captured; see §6. Sources `Admin lookups.html:146-147,157-158` vs `:181`)
- **what is wrong:** governorate/area rows use a bare `Switch` with only `aria-label`; amenity rows wrap the identical switch in a visible `Field label="نشط" orientation="horizontal"`. The same control (row visible/hidden) shows a text label in one list and none in the other, shifting row rhythm between tabs.
- **proposal:** one pattern for both tabs — the bare switch with `aria-label` (the lists already explain hidden behaviour in their intro lines), or the labelled field in both. Do not mix.
- **why:** row-managed lists at reading width (AD-029) depend on identical row geometry; the switch column should align across tabs.
- **cost:** S
- **rule:** lens B.4; DECISIONS_ADMIN Lookups (AD-025: switches only in the row).

### R2-AD-VD-006 — List toolbars use two different grids

- **type:** improvement · **level:** pattern · **impact:** medium
- **where:** frames "Spaces" (§43), "Owners" (§44), "Users" (§46), "Audit log" (§48); `http://127.0.0.1:5416/Admin spaces.html`, `Admin owners.html`, `Admin users.html`, `Admin audit.html`; 768 light matters most
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-006.png` (not captured; see §6. Sources `Admin spaces.html:85-91` vs `Admin owners.html:140-145`, `Admin users.html:82-88`)
- **what is wrong:** spaces builds the toolbar as `grid md:grid-cols-3` (search takes one third), owners/users as `flex md:flex-row` with search `md:flex-1`. From 768 the same search field and the same inline filters get different widths on different pages; the second row also differs (spaces: count + stale chip + add; owners: count + add; users/audit: count alone).
- **proposal:** one toolbar pattern for all four lists: search `md:flex-1` + inline filter fields; second row `justify-between` with count (+ quick chip where one exists, i.e. spaces' stale chip) at the start and the add action — or nothing — at the end. Changes spaces, owners, users, audit.
- **why:** the filter bar is one pattern (P5); equal jobs get equal geometry at every width.
- **cost:** S (prototype)
- **rule:** P5; lens B.4.

### R2-AD-VD-007 — ResultCount is worded five ways

- **type:** improvement · **level:** pattern · **impact:** low
- **where:** all list frames §§43–46, 48; e.g. `http://127.0.0.1:5416/Admin users.html` ("العدد: N") vs `http://127.0.0.1:5416/Admin spaces.html` ("عدد المساحات: N"); 1440 light
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-007.png` (not captured; see §6. Sources `Admin spaces.html:96`, `Admin owners.html:147`, `Admin users.html:89`, `Admin reports.html:79`, `Admin audit.html:84`)
- **what is wrong:** the count by the toolbar names the thing on four lists but is a bare «العدد» on users. Same pattern element, five labels.
- **proposal:** name the thing everywhere — «المستخدمون: N» on users, keeping the other four as they are.
- **why:** the count line is the filter feedback (P5); a named count confirms what was counted.
- **cost:** S
- **rule:** P5 ("the result count by the toolbar"); lens B.4.

### R2-AD-VD-008 — Page h1 is set in heading-3

- **type:** defect · **level:** pattern · **impact:** low
- **where:** every AD frame §§42–48, e.g. `http://127.0.0.1:5416/Admin overview.html`, 1440 light (one h1 per page is kept — the style is the issue)
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-008.png` (not captured; see §6. Source `masaha/admin.jsx:66`)
- **what is wrong:** `AdminShell` renders the page `h1` as `text-heading-3` (17px semibold) while foundation §7 assigns page titles `heading-1` (30/24px). Section titles in the editor are `h2` at `heading-2` (22px) via `SectionTitle`, so a page title sets smaller than its own section titles — the hierarchy reads inverted on dense pages (editor, lookups).
- **proposal:** set the dashboard `h1` to the foundation page-title style (or record a dashboard-density exception in foundation §7 and apply it in every dashboard shell, not admin alone). Pattern-level: changes admin, owner and reception shells together.
- **why:** one heading scale everywhere; a page title must outrank its section titles.
- **cost:** S (prototype; M if the exception goes into the layer)
- **rule:** foundation §7 (applies, or is put in doubt if dashboard density is intended).

### R2-AD-VD-009 — Settings cards have no h2; editor sections do

- **type:** defect · **level:** page · **impact:** low
- **where:** frame "Platform settings" (INDEX §48), `http://127.0.0.1:5416/Admin settings.html`, 1440 + 390 light; archive screen `docs/design/screens/48-admin-audit-log-platform-settings/03-platform-settings-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-009.png` (not captured; see §6. Sources `Admin settings.html:28-36` vs `masaha/profile-a.jsx:30`)
- **what is wrong:** editor sections use `SectionTitle` (`h2` inside `CardTitle`); settings' `SCard` uses a plain `CardTitle` (a div), so the page goes h1 → div-titles while the editor on the next menu item goes h1 → h2 sections. Same card-title job, two ranks.
- **proposal:** use the same `SectionTitle` (h2) pattern for the three settings cards.
- **why:** hierarchy is consistent across the dashboard: every card that is a section is an h2.
- **cost:** S
- **rule:** DECISIONS_ADMIN A1 ("section titles are `h2`"); SH-017.

### R2-AD-VD-010 — Failure Alert sits in two different places

- **type:** improvement · **level:** pattern · **impact:** low
- **where:** frames "Users — Change role" with `?fail=role` (§46) vs link dialogs with `?fail=link` (§§43–44), e.g. `http://127.0.0.1:5416/Admin users.html?changerole=1&fail=role` and `http://127.0.0.1:5416/Admin spaces.html?link=golden&fail=link`, 1440 light
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-010.png` (not captured; see §6. Sources `Admin users.html:106-107` vs `masaha/admin.jsx:207-208`)
- **what is wrong:** the role-fail Alert renders directly between `AlertDialogHeader` and `AlertDialogFooter`; the link-fail Alert renders inside the dialog body stack (`gap-4`). The same failure element gets different spacing and a different relation to the form in two dialogs of one family.
- **proposal:** failure Alert as the first element of the dialog body in both (and in the add-owner sheet path), keeping P8's "stays open, keeps input".
- **why:** one failure pattern — the eye finds the error in the same place in every admin dialog.
- **cost:** S
- **rule:** P8; foundation §5 spacing scale.

### R2-AD-VD-011 — Read-only verified view repeats the h1 in muted meta without hierarchy

- **type:** improvement · **level:** page · **impact:** low
- **where:** frame "Verified · read-only" (INDEX §43), `http://127.0.0.1:5416/Admin space edit.html?id=focus`, 1440 + 390 light; archive screen `docs/design/screens/43-admin-spaces/13-verified-read-only-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AD-VD\R2-AD-VD-011.png` (not captured; see §6. Source `Admin space edit.html:97-126`)
- **what is wrong:** the read-only rows (`Row`: `dt` muted + `dd` body) render every value — including long text (description, address) and joined amenity strings — in identical `text-body`, with empty values as a bare "—". Against the editable editor (labelled fields, helpers, per-section footers) the page reads as a flat ledger: section order matches (profile/hours/prices/amenities/contacts/photos — good), but rows have no emphasis gradient and empty vs filled rows look alike.
- **proposal:** keep order; mute only genuinely empty values further (`text-caption`-scale placeholder is already muted — keep), and let the two key facts (Arabic + English names) keep `text-label` weight as the title block of the profile card, matching the edit mode's first-field emphasis. No new component.
- **why:** the read-only page keeps the editor's section order (settled) while giving the eye one entry point per card.
- **cost:** S
- **rule:** lens A.3 (hierarchy); DECISIONS_ADMIN "verified space's page" (order settled — this changes emphasis only).

## Decisions in doubt

None. The narrowed/ amended decisions held up: P1-narrowed add-button row, P5 chips/select split (except R2-AD-VD-003, which is a misapplication, not a bad rule), P9 red scope (except R2-AD-VD-001, likewise a misapplication), A3 two-fact status, A7 cards/table split, AD-029 reading width, and «ناقصة» as `warning` are all correctly applied where used. R2-AD-VD-008 notes the one place foundation §7 may need a dashboard-density exception rather than a fix — owner's call.

## What was not reviewed and why

- **Live rendering at 390/768/1440, Arabic + English, light + dark:** this runner has no browser tooling, so no viewport screenshots or cropped PNG captures could be taken; the evidence folder (`C:\Users\basel\Downloads\r2-shots\AD-VD\`, created) holds no new captures. Judgement is by code inspection of the prototype sources (all ten AD pages plus `masaha/admin.jsx`, `profile-a.jsx`, `profile-b.jsx`, `shared.jsx`, `admin-data.js`) against the settled decisions and foundation tokens. All colour/spacing claims cite the class or variant in the source. A visual pass should confirm R2-AD-VD-004/006/008 at 768 and in dark before build.
- **Out-of-axis matters** (per the prompt §5): flow length and feedback behaviour (UX), breakage/overflow/mirroring/console errors (DF), element removals (EX), wording/translation (CP), focus/names/contrast/touch targets/reader order (AX), API/model/v1 truth and permissions (TR) — left to the sibling AD prompts.
- **Settled patterns as such** (REVIEW_LENS §2b, DECISIONS_SHARED, DECISIONS_ADMIN with amendments, CHANGES SH-007/DI-23/DI-24/DI-26) were not re-reported; only their misapplications above.
- **Server:** prototype served on port 5416 per the prompt; `Admin spaces.html` answered HTTP 200. The server ran in the review shell, which does not persist background jobs between commands; the port was re-checked after the review (connection refused = free).

## Browser pass (2026-10-17)
Server: http://127.0.0.1:5490 · masaha-design at 93f152f · tool: playwright MCP
### Existing issues
- R2-AD-VD-001 — confirmed: `AlertDialogAction` has `variant: "destructive"` for both toAdmin («جعله أدمن») and toUser («إعادته مستخدمًا») directions. — r2-shots/AD-VD/R2-AD-VD-001.png
- R2-AD-VD-002 — confirmed: `SpaceStatus` renders «مخفية» with `variant: "warning"` (amber) instead of neutral. — r2-shots/AD-VD/R2-AD-VD-002.png
- R2-AD-VD-003 — confirmed: Reports uses `ToggleGroup` with chips (الكل, جديد, تم التصحيح); Owners has no visible chips or selects — status filter is in a sheet. — r2-shots/AD-VD/R2-AD-VD-003.png
- R2-AD-VD-004 — confirmed: Deleted spaces have 0 muted cells; name, area, owner, date all render as live. — r2-shots/AD-VD/R2-AD-VD-004.png
- R2-AD-VD-005 — confirmed: Governorate/area switches have `aria-label` («ظاهرة: …»); amenity switches have no aria-label. — r2-shots/AD-VD/R2-AD-VD-005.png
- R2-AD-VD-006 — confirmed: Spaces toolbar uses `grid gap-3 md:grid-cols-3`; Owners uses `flex flex-col gap-3 md:flex-row`. — r2-shots/AD-VD/R2-AD-VD-006.png
- R2-AD-VD-007 — confirmed: Count labels vary: «مساحات: 7», «مساحات: 4», «العدد: 84», «بلاغات: 6». — r2-shots/AD-VD/R2-AD-VD-007.png
- R2-AD-VD-008 — confirmed: h1 uses `text-heading-3` (17px, 600 weight) instead of heading-1. — r2-shots/AD-VD/R2-AD-VD-008.png
- R2-AD-VD-009 — confirmed: Settings page has only h1; no h2 headings for the three cards. — r2-shots/AD-VD/R2-AD-VD-009.png
- R2-AD-VD-010 — not checked: Role dialog not opened in browser (menu interaction failed).
- R2-AD-VD-011 — confirmed: Read-only verified view has h1 + h2 sections, 5 muted elements; flat ledger style. — r2-shots/AD-VD/R2-AD-VD-011.png
### Checked now
- h1 styling: `text-heading-3` at 17px/600 (confirms R2-AD-VD-008).
- SpaceStatus: `variant: "warning"` for «مخفية» (confirms R2-AD-VD-002).
- Role dialog source: `variant: "destructive"` for both directions (confirms R2-AD-VD-001).
- Deleted rows: 0 muted cells, all content renders as live (confirms R2-AD-VD-004).
- Toolbar grids: Spaces `grid md:grid-cols-3` vs Owners `flex md:flex-row` (confirms R2-AD-VD-006).
- Count labels: 5 different wordings across lists (confirms R2-AD-VD-007).
- Settings: only h1, no h2 for cards (confirms R2-AD-VD-009).
- Lookups: governorate/area switches have aria-labels, amenity switches don't (confirms R2-AD-VD-005).
- Reports: ToggleGroup with chips; Owners: no visible chips (confirms R2-AD-VD-003).
- Read-only view: h1 + h2 sections, 5 muted elements (confirms R2-AD-VD-011).
### New issues
None.
### Still not checked
- R2-AD-VD-010: Failure Alert placement in role dialog (not opened).
- Dark mode: not checked for admin pages.
- 768px width: not checked for admin pages.
- English/LTR: not checked for admin pages.
- Screen-reader audio: no screen reader available.
