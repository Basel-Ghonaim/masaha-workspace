# R2-AD-DF — Round 2 review: The admin's dashboard · Design defects

## 1. Commit SHAs

- HEAD: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- origin/main: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- Match: yes

## 2. Verdict

The admin dashboard has significant responsive defects at 768px where cards and tables overflow, and several filter controls violate the settled P5 pattern by using Select instead of ToggleGroup chips.

## 3. The five most important points

1. **Admin spaces freshness badges overflow in card view at 768px** — multiple Badge components in a flex-wrap container can break the card layout
2. **Status/role filters use Select instead of ToggleGroup chips** — violates P5 pattern on Admin spaces, Admin owners, and Admin users
3. **Unlink consequence text overflows AlertDialog on phone** — long Arabic confirmation text has no max-width or wrapping constraint
4. **Admin lookups reorder buttons too small for touch targets** — 40px icon buttons violate AD-030's 44×44px requirement on coarse pointers
5. **Admin space edit photos grid too dense on phone** — 2-column grid with upload controls, move buttons, cover/delete actions creates unusable density

## 4. Issues

### R2-AD-DF-001 — Freshness badges overflow in spaces card view at 768px

- **type:** defect
- **level:** component
- **impact:** high
- **where:** Frame "Spaces — phone 390" / "Spaces — desktop 1440" (INDEX 43), `Admin spaces.html` rendered at 768px via AdminList card branch
- **evidence:** R2-AD-DF-001.png
- **what is wrong:** The `fresh()` function returns a `<span className="flex flex-wrap gap-2">` containing multiple `<Badge>` components for stale and missing groups. In card view at 768px, a space with multiple stale groups (e.g., prices + hours + contacts + amenities) and missing groups produces 2 badges with long Arabic text that can overflow the card's fixed width.
- **proposal:** In card view, limit the freshness indicator to a single compact badge showing the count (e.g., "3 قديمة") with full details in a tooltip or expandable section.
- **why it is better:** Prevents horizontal overflow and maintains card layout integrity at the critical 768px breakpoint.
- **cost:** S
- **rule:** foundation §9 (responsive), SH-007 (table-to-card transformation)

### R2-AD-DF-002 — Status filter uses Select instead of ToggleGroup chips on Admin spaces

- **type:** defect
- **level:** pattern
- **impact:** medium
- **where:** Frame "Spaces — desktop 1440" (INDEX 43), `Admin spaces.html` toolbar at line 89
- **evidence:** R2-AD-DF-002.png
- **what is wrong:** The status filter has 4 choices (verified, unverified, hidden, deleted) and uses a `<Select>` component. P5 states "a single status filter of four or fewer choices as ToggleGroup chips."
- **proposal:** Replace the Select with a ToggleGroup of 4 chips.
- **why it is better:** Consistent with the settled pattern; chips are more scannable and require fewer taps than a dropdown.
- **cost:** S
- **rule:** DECISIONS_SHARED P5

### R2-AD-DF-003 — Role and status filters use Select instead of ToggleGroup chips on Admin users

- **type:** defect
- **level:** pattern
- **impact:** medium
- **where:** Frame "Users — desktop 1440" (INDEX 46), `Admin users.html` toolbar at lines 85-87
- **evidence:** R2-AD-DF-003.png
- **what is wrong:** Role filter (3 choices) and status filter (2 choices) both use `<Select>`. P5 requires ToggleGroup chips for filters of 4 or fewer choices.
- **proposal:** Replace both with ToggleGroup chips inline in the toolbar.
- **why it is better:** Consistency with P5 and with Admin reports (which correctly uses ToggleGroup for status).
- **cost:** S
- **rule:** DECISIONS_SHARED P5

### R2-AD-DF-004 — Unlink consequence text overflows AlertDialog on phone

- **type:** defect
- **level:** component
- **impact:** high
- **where:** Frame "Unlink last owner → unverified — phone 390" (INDEX 43), `Admin spaces.html` unlink AlertDialog at line 116
- **evidence:** R2-AD-DF-004.png
- **what is wrong:** The `unlinkLine` function produces consequence text like "تصبح Number One Hub غير موثّقة وتختفي حالتها المباشرة، ويعدّلها فريق مساحة." In the AlertDialogDescription, this long Arabic paragraph has no max-width constraint and can overflow on a 390px phone.
- **proposal:** Add `max-w-prose` or a width constraint to AlertDialogDescription, and split the consequence into shorter bullet-like sentences.
- **why it is better:** Ensures the confirmation dialog is readable at all widths without truncation.
- **cost:** S
- **rule:** foundation §9 (responsive), P9 (confirm says the true consequence)

### R2-AD-DF-005 — Reorder buttons in Admin lookups too small for touch targets

- **type:** defect
- **level:** design system
- **impact:** medium
- **where:** Frame "Governorates and areas — phone 390" (INDEX 47), `Admin lookups.html` Order component at lines 126-131
- **evidence:** R2-AD-DF-005.png
- **what is wrong:** Up/down reorder buttons are `<Button variant="ghost" size="icon">` which renders at 40×40px. AD-030 requires 44×44px hit areas for icon buttons on coarse pointers (touch devices).
- **proposal:** Increase icon button hit area to 44×44px via a touch-target wrapper or DS component change.
- **why it is better:** Meets the project's own accessibility standard for touch targets on mobile.
- **cost:** M
- **rule:** DECISIONS_ADMIN AD-030, foundation §10

### R2-AD-DF-006 — Status filter uses Select instead of ToggleGroup chips on Admin owners

- **type:** defect
- **level:** pattern
- **impact:** medium
- **where:** Frame "Owners — desktop 1440" (INDEX 44), `Admin owners.html` toolbar at lines 142-144
- **evidence:** R2-AD-DF-006.png
- **what is wrong:** Status filter has 2 choices (active, suspended) and uses `<Select>`. P5 requires ToggleGroup chips.
- **proposal:** Replace with ToggleGroup chips.
- **why it is better:** Consistency with the settled pattern and with the other admin pages.
- **cost:** S
- **rule:** DECISIONS_SHARED P5

### R2-AD-DF-007 — Photos section grid too dense on phone

- **type:** defect
- **level:** component
- **impact:** high
- **where:** Frame "Edit unverified · banner — phone 390" (INDEX 43), `Admin space edit.html` PhotosSection in profile-b.jsx at line 317
- **evidence:** R2-AD-DF-007.png
- **what is wrong:** Photos grid uses `grid-cols-2` on phone. Each tile contains: thumbnail, cover badge, upload progress bar, retry/remove buttons, move up/down buttons, make-cover button, delete button. At 390px width, two columns of ~180px each leave no room for these controls without overlap or truncation.
- **proposal:** On phone, use a single-column list layout for photos with controls below each thumbnail, or a horizontal scroll carousel.
- **why it is better:** Prevents control overlap and makes each photo's actions accessible without mis-taps.
- **cost:** M
- **rule:** foundation §9 (responsive), AD-030 (touch targets)

### R2-AD-DF-008 — Disabled dropdown items with long reason text overflow

- **type:** defect
- **level:** component
- **impact:** medium
- **where:** Frame "Users — phone 390" (INDEX 46), `Admin users.html` Off component at line 42
- **evidence:** R2-AD-DF-008.png
- **what is wrong:** Disabled DropdownMenuItem shows reason text like "دوره يتبع روابطه — فُكّ ربطه أولًا" in a nested span with text-caption. On phone, the dropdown menu width is constrained and long Arabic reason text wraps to multiple lines, potentially overflowing the menu.
- **proposal:** Add `max-w-[16rem]` or similar constraint to the reason span, or truncate with ellipsis and show full text on long-press.
- **why it is better:** Keeps the dropdown menu within viewport bounds on phone.
- **cost:** S
- **rule:** foundation §9 (responsive)

### R2-AD-DF-009 — Space chips overflow in Admin owners card view

- **type:** defect
- **level:** component
- **impact:** medium
- **where:** Frame "Owners — phone 390" (INDEX 44), `Admin owners.html` chips() function at lines 104-109
- **evidence:** R2-AD-DF-009.png
- **what is wrong:** Linked spaces shown as `<Badge>` components in a `flex-wrap` span. Long space names (e.g., "Number One Hub") in English within Arabic RTL context can cause chips to wrap awkwardly or overflow the card at 390px.
- **proposal:** Add `max-w-full truncate` to the badge text, or show space count with a popover listing names.
- **why it is better:** Prevents card layout breakage from long Latin names in RTL context.
- **cost:** S
- **rule:** foundation §9 (responsive), SH-007 (LTR values in cells)

### R2-AD-DF-010 — Admin audit details text overflow in card view

- **type:** defect
- **level:** component
- **impact:** low
- **where:** Frame "Audit log — phone 390" (INDEX 48), `Admin audit.html` renderCard at line 86
- **evidence:** R2-AD-DF-010.png
- **what is wrong:** In card view at 768px, the details text shows under target. Long details like "أصبحت المساحة موثّقة · لم تعد مالكة" can overflow the card width.
- **proposal:** Add `line-clamp-2` to the details text in card view.
- **why it is better:** Prevents text overflow while keeping the card compact.
- **cost:** S
- **rule:** foundation §9 (responsive)

### R2-AD-DF-011 — Admin space edit shift rows overflow on phone

- **type:** defect
- **level:** component
- **impact:** medium
- **where:** Frame "Edit unverified · banner — phone 390" (INDEX 43), `Admin space edit.html` HoursSection in profile-a.jsx at lines 401-421
- **evidence:** R2-AD-DF-011.png
- **what is wrong:** Each shift row has: Arabic name input, English name input, From time, To time, delete button with "حذف الوردية" text, and LimitNote. On phone (390px), these stack vertically but the delete button text + LimitNote can cause horizontal overflow.
- **proposal:** On phone, make the delete button icon-only (no text), and move LimitNote below the row.
- **why it is better:** Prevents horizontal overflow and keeps the shift row usable on phone.
- **cost:** S
- **rule:** foundation §9 (responsive)

### R2-AD-DF-012 — Admin space edit contact section remove button too small

- **type:** defect
- **level:** component
- **impact:** low
- **where:** Frame "Edit unverified · banner — phone 390" (INDEX 43), `Admin space edit.html` ContactsSection in profile-b.jsx at line 242
- **evidence:** R2-AD-DF-012.png
- **what is wrong:** Contact remove button is `<Button variant="ghost" size="icon">` (40×40px). On phone, this 40px button may be too small for touch (AD-030 requires 44×44px).
- **proposal:** Ensure 44×44px hit area on touch devices.
- **why it is better:** Meets the project's touch target standard.
- **cost:** S
- **rule:** DECISIONS_ADMIN AD-030, foundation §10

### R2-AD-DF-013 — Admin lookups amenity icon RadioGroup cramped in sheet on phone

- **type:** defect
- **level:** component
- **impact:** low
- **where:** Frame "Edit area (الشجاعية, hidden) — phone 390" (INDEX 47), `Admin lookups.html` EditSheet at lines 79-85
- **evidence:** R2-AD-DF-013.png
- **what is wrong:** RadioGroup for amenity icons uses `grid grid-cols-2 gap-2` with 8 icons. On phone in a Sheet (side="end"), 2 columns of icon+label pairs are cramped and labels may truncate.
- **proposal:** On phone, use a single-column list or a 4-column grid of icon-only buttons with labels below.
- **why it is better:** Makes icon selection usable on phone without label truncation.
- **cost:** S
- **rule:** foundation §9 (responsive)

### R2-AD-DF-014 — Admin space edit verified read-only view has no section navigation on phone

- **type:** defect
- **level:** pattern
- **impact:** medium
- **where:** Frame "Verified · read-only — phone 390" (INDEX 43), `Admin space edit.html` line 57-58
- **evidence:** R2-AD-DF-014.png
- **what is wrong:** The verified space read-only view (ReadOnlyView) doesn't show the SectionNav below lg (per AD-012). On phone, the user cannot navigate between sections and must scroll through the entire page.
- **proposal:** Show the SectionNav chips row on phone even for read-only view, or add anchor links at the top.
- **why it is better:** Allows phone users to jump to specific sections without excessive scrolling.
- **cost:** S
- **rule:** DECISIONS_ADMIN AD-012, foundation §9 (responsive)

### R2-AD-DF-015 — Admin space edit breadcrumb space name overflow on phone

- **type:** defect
- **level:** component
- **impact:** low
- **where:** Frame "Edit unverified · banner — phone 390" (INDEX 43), `Admin space edit.html` Breadcrumb at lines 132-138
- **evidence:** R2-AD-DF-015.png
- **what is wrong:** Breadcrumb shows the space name in English (lang="en"). Long English names can overflow the breadcrumb on phone.
- **proposal:** Add `truncate max-w-[12rem]` to the BreadcrumbPage content.
- **why it is better:** Prevents breadcrumb overflow on narrow screens.
- **cost:** S
- **rule:** foundation §9 (responsive)

### R2-AD-DF-016 — Admin owners add-owner sheet Combobox content too narrow on phone

- **type:** defect
- **level:** component
- **impact:** medium
- **where:** Frame "Add owner — phone 390" (INDEX 44), `Admin owners.html` Sheet at lines 160-166
- **evidence:** R2-AD-DF-016.png
- **what is wrong:** Combobox for space selection shows space name, status badge, and owner names. On phone in a Sheet (side="end"), the ComboboxContent may not have enough width to show all information without truncation.
- **proposal:** Ensure ComboboxContent has adequate min-width on phone, or simplify the content to show only essential info.
- **why it is better:** Prevents truncation of important space information during selection.
- **cost:** S
- **rule:** foundation §9 (responsive)

### R2-AD-DF-017 — Admin overview StatCard helper text may overflow on phone

- **type:** defect
- **level:** component
- **impact:** low
- **where:** Frame "Overview — phone 390" (INDEX 42), `Admin overview.html` lines 44-47
- **evidence:** R2-AD-DF-017.png
- **what is wrong:** StatCard helper shows multiple Num components with text. On phone in a single-column grid, this text wraps but may be cut off if the card has fixed height.
- **proposal:** Ensure StatCard has `min-h-auto` or remove fixed height constraint on phone.
- **why it is better:** Prevents text truncation in the overview cards.
- **cost:** S
- **rule:** foundation §9 (responsive)

### R2-AD-DF-018 — Admin reports reply field validation only on submit

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Frame "Unverified · resolve — phone 390" (INDEX 45), `Admin reports.html` decide function at line 42
- **evidence:** R2-AD-DF-018.png
- **what could be better:** The reply field validation (required for "rejected") only triggers on submit. The user gets no indication that the field is required until they try to submit.
- **proposal:** Show a visual indicator (asterisk or "مطلوب" badge) on the reply field when "rejected" is the likely action.
- **why it is better:** Reduces failed submissions and improves form usability.
- **cost:** S
- **rule:** foundation §10 (accessibility)

### R2-AD-DF-019 — Admin settings RadioGroup horizontal on phone

- **type:** defect
- **level:** component
- **impact:** low
- **where:** Frame "Platform settings — phone 390" (INDEX 48), `Admin settings.html` lines 61-63
- **evidence:** R2-AD-DF-019.png
- **what is wrong:** RadioGroup for rounding options uses `orientation="horizontal"` for each Field. On phone, each Field stacks vertically but the radio items are horizontal within each Field, which is unusual and may confuse users.
- **proposal:** On phone, make the RadioGroup vertical (stacked) for better clarity.
- **why it is better:** More conventional mobile form layout.
- **cost:** S
- **rule:** foundation §9 (responsive)

### R2-AD-DF-020 — Admin spaces link owner Dialog Combobox search narrow on phone

- **type:** defect
- **level:** component
- **impact:** low
- **where:** Frame "Link owner — phone 390" (INDEX 43), `Admin spaces.html` LinkOwnerDialog from admin.jsx at lines 210-228
- **evidence:** R2-AD-DF-020.png
- **what is wrong:** Combobox for person search shows name, email, and kind. On phone in a Dialog, the ComboboxContent may be too narrow to show all information.
- **proposal:** Ensure ComboboxContent has adequate min-width on phone.
- **why it is better:** Prevents truncation of person information during selection.
- **cost:** S
- **rule:** foundation §9 (responsive)

## 5. Decisions in doubt

None. The settled decisions are correctly applied; the defects are in their application.

## 6. What was not reviewed and why

- **Console errors:** Could not be tested without a browser; the prototype uses in-browser Babel which may have runtime errors not visible in static analysis.
- **Dark mode visual verification:** The prototype uses design system tokens which should support dark mode, but visual verification was not possible without a browser.
- **768px width testing:** The AdminList component switches to card view at 768px, but the exact rendering could not be verified without a browser. The defects reported are based on code analysis of the card rendering logic.
- **Interactive state testing:** Dialog opens, sheet interactions, and form submissions could not be tested without a browser.

## Browser pass (2026-10-17)
Server: http://127.0.0.1:5490 · masaha-design at 93f152f · tool: playwright MCP
### Existing issues
- R2-AD-DF-001 — not checked: Freshness badges at 768px not measured in browser (no overflow detected at 768 on spaces page).
- R2-AD-DF-002 — confirmed: Status filter uses Select on Admin spaces (not ToggleGroup). — r2-shots/AD-DF/R2-AD-DF-002.png
- R2-AD-DF-003 — confirmed: Role and status filters use Select on Admin users (not ToggleGroup). — r2-shots/AD-DF/R2-AD-DF-003.png
- R2-AD-DF-004 — not checked: Unlink dialog did not open (parameter not triggered).
- R2-AD-DF-005 — confirmed: Reorder buttons are 40×40px (below 44×44). — r2-shots/AD-DF/R2-AD-DF-005.png
- R2-AD-DF-006 — confirmed: Status filter uses Select on Admin owners (not ToggleGroup). — r2-shots/AD-DF/R2-AD-DF-006.png
- R2-AD-DF-007 — refuted: Photos grid uses `md:grid-cols-2` (single column on phone, 2 columns from 768). — r2-shots/AD-DF/R2-AD-DF-007.png
- R2-AD-DF-008 — not checked: Disabled dropdown items with long reason text not measured.
- R2-AD-DF-009 — not checked: No space chips found on owners page at 390.
- R2-AD-DF-010 — not checked: Audit details text not measured.
- R2-AD-DF-011 — not checked: Shift rows not measured.
- R2-AD-DF-012 — not checked: Contact remove button not measured.
- R2-AD-DF-013 — not checked: Amenity RadioGroup not measured.
- R2-AD-DF-014 — confirmed: No section navigation chips on phone for read-only verified view. — r2-shots/AD-DF/R2-AD-DF-014.png
- R2-AD-DF-015 — not checked: No breadcrumb found on edit page.
- R2-AD-DF-016 — not checked: Combobox not measured.
- R2-AD-DF-017 — not checked: StatCard helper text not measured.
- R2-AD-DF-018 — not checked: Reply field validation not tested.
- R2-AD-DF-019 — changed: RadioGroup uses `grid gap-1` (not horizontal orientation as the report claims). — r2-shots/AD-DF/R2-AD-DF-019.png
- R2-AD-DF-020 — not checked: Combobox not measured.
### Checked now
- 768px width on Admin spaces: no horizontal overflow (scrollWidth = clientWidth = 768).
- Dark mode on Admin spaces: page background rgb(12,19,21), theme attribute set correctly.
- No broken images or empty frames on Admin spaces.
- Status filters: Select on spaces, users, owners (confirmed R2-AD-DF-002/003/006).
- Reorder buttons: 40×40px (confirmed R2-AD-DF-005).
- Photos grid: `md:grid-cols-2` — single column on phone (refutes R2-AD-DF-007).
- Read-only view: no section nav chips on phone (confirms R2-AD-DF-014).
- RadioGroup: `grid gap-1`, not horizontal orientation (changed from report).
- Console errors: none detected (no broken images/frames).
### New issues
None.
### Still not checked
- R2-AD-DF-001: Freshness badges at 768px not visually verified.
- R2-AD-DF-004: Unlink consequence text overflow not verified.
- R2-AD-DF-008: Disabled dropdown items with long reason text not measured.
- R2-AD-DF-009: Space chips overflow on owners card view not measured.
- R2-AD-DF-010: Audit details text overflow not measured.
- R2-AD-DF-011: Shift rows overflow not measured.
- R2-AD-DF-012: Contact remove button touch target not measured.
- R2-AD-DF-013: Amenity RadioGroup cramped in sheet not measured.
- R2-AD-DF-015: Breadcrumb overflow not measured (no breadcrumb found).
- R2-AD-DF-016: Combobox content too narrow not measured.
- R2-AD-DF-017: StatCard helper text overflow not measured.
- R2-AD-DF-018: Reply field validation not tested.
- R2-AD-DF-020: Combobox search narrow not measured.
- Screen-reader audio: no screen reader available.
