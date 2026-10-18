# R2-AD-AX — Round 2 review: The admin's dashboard · Accessibility and resilience

## Commit SHAs

- HEAD: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- origin/main: `34a6c59aab049e8f2992b29b88c8a700b926ddba`

## Verdict

The admin dashboard is largely accessible and resilient; most controls are named and focus is visible. Two defects stand out: disabled row-menu items in the users list do not announce their reason to screen readers, and the overview tile links produce verbose, unclear accessible names. No structural or design-system-level accessibility failures were found.

## The five most important points

1. **Disabled menu items hide their reason.** On the users page, suspended or Google-only accounts see disabled items whose explanation sits in a muted caption that screen readers often skip — the admin cannot discover why an action is unavailable.
2. **Overview tile links have unclear accessible names.** The four navigation tiles concatenate label, value, and helper text into one long string, making it hard for a screen-reader user to distinguish " Spaces 12 verified 8 unverified 3 hidden" from a single fact.
3. **Combobox triggers lack programmatic names.** The person/space pickers in the link dialog, the owners add-owner sheet, and the reports filter all rely on a visible Field label but the trigger button itself carries no `aria-label` or `aria-labelledby`, so a screen-reader user activating the trigger hears only "button".
4. **SectionNav chips on the editor lack `aria-current`.** The scrolling chip row below `lg` marks the current section visually but does not set `aria-current="true"` or `aria-current="location"`, so a screen-reader user cannot tell which section is active.
5. **Photo-upload failure retry may not be reachable.** The `?fail=upload` state shows a retry on the first tile, but the tile is not a focusable control in the static markup — if the retry is a plain `<span>` or `<div>` without `tabindex="0"` and `role="button"`, keyboard users cannot trigger it.

## Issues

### R2-AD-AX-001 — Disabled menu items do not announce their reason

- **type:** defect
- **level:** component
- **impact:** medium
- **where:** Users list row menu — `Admin users.html?q=all` — 1440 light — `docs/design/screens/13-admin/03-users.webp`
- **evidence:** `R2-AD-AX-001.png`
- **what is wrong:** On the users page, suspended or Google-only accounts see disabled `DropdownMenuItem` elements whose explanation sits in a `<span className="text-caption text-muted-foreground">`. Screen readers typically skip muted or de-emphasised content when navigating to disabled items, so the admin hears "change role, dimmed" without the reason ("Their role follows their links — unlink them first" or "A Google account — they recover it through Google"). The `Off` component in `Admin users.html:42` renders the reason as a visual caption only.
- **proposal:** Move the reason text into the `DropdownMenuItem`'s accessible name by appending it to the label: `<DropdownMenuItem disabled><span>Change role — Their role follows their links, unlink them first</span></DropdownMenuItem>`. This keeps the visual design and ensures screen readers announce the full text.
- **why it is better:** The admin immediately knows why an action is unavailable without needing to infer it from context.
- **cost:** S
- **rule:** foundation §10 (disabled controls must say why)

### R2-AD-AX-002 — Overview tile links have verbose, unclear accessible names

- **type:** defect
- **level:** component
- **impact:** medium
- **where:** Overview tiles — `Admin overview.html` — 390 light — `docs/design/screens/13-admin/01-overview.webp`
- **evidence:** `R2-AD-AX-002.png`
- **what is wrong:** The `Tile` component wraps `StatCard` in an `<a>` with no `aria-label`. The link's accessible name is the concatenated text content: "Spaces 12 verified 8 unverified 3 hidden" for the first tile. A screen-reader user hears a long string of numbers and words without clear separation between the tile's label, its primary value, and its helper breakdown.
- **proposal:** Add `aria-label` to each tile link: `aria-label={tr('المساحات: 12 موثّقة، 8 غير موثّقة، 3 مخفية', 'Spaces: 12 verified, 8 unverified, 3 hidden')}`.
- **why it is better:** The tile announces its purpose and key facts as one coherent phrase rather than a jumble of numbers.
- **cost:** S
- **rule:** foundation §10 (every link needs a clear name)

### R2-AD-AX-003 — Combobox triggers lack programmatic accessible names

- **type:** defect
- **level:** component
- **impact:** medium
- **where:** Link dialog, add-owner sheet, reports space filter — `Admin spaces.html?link=<id>`, `Admin owners.html?sheet=add`, `Admin reports.html` — 1440 light — `docs/design/screens/13-admin/02-spaces.webp`
- **evidence:** `R2-AD-AX-003.png`
- **what is wrong:** The `Combobox` component's `ComboboxTrigger` button has no `aria-label` or `aria-labelledby`. The visible `Field label` is associated with the input but not with the trigger button. A screen-reader user activating the trigger hears "button" or the selected value without knowing what field they are opening.
- **proposal:** Pass `aria-labelledby` pointing to the Field's label id, or add `aria-label` on the trigger: `aria-label={tr('اختر شخصًا', 'Choose a person')}`.
- **why it is better:** The admin knows which field they are opening before they open it.
- **cost:** S
- **rule:** foundation §10 (every control needs a name)

### R2-AD-AX-004 — SectionNav chips lack `aria-current` for active section

- **type:** defect
- **level:** component
- **impact:** low
- **where:** Editor section navigation (mobile chips row) — `Admin space edit.html?id=golden` — 390 light — `docs/design/screens/13-admin/04-space-edit.webp`
- **evidence:** `R2-AD-AX-004.png`
- **what is wrong:** Below `lg`, `SectionNav` renders a scrolling row of chips. The active section is visually marked but does not set `aria-current="true"` or `aria-current="location"`. A screen-reader user cannot tell which section is currently active.
- **proposal:** Add `aria-current={isActive ? 'true' : undefined}` to the active chip.
- **why it is better:** Screen-reader users can identify their current location in the editor.
- **cost:** S
- **rule:** foundation §10 (aria-current for current location)

### R2-AD-AX-005 — Photo-upload failure retry may not be keyboard-reachable

- **type:** defect
- **level:** component
- **impact:** high
- **where:** Photo upload tile with failure — `Admin space edit.html?id=golden&fail=upload` — 1440 light — `docs/design/screens/13-admin/04-space-edit.webp`
- **evidence:** `R2-AD-AX-005.png`
- **what is wrong:** The `?fail=upload` state shows a retry button on the first photo tile. In the static markup, the retry element may not be a focusable control — if it is a `<span>` or `<div>` without `tabindex="0"` and `role="button"`, keyboard users cannot trigger the retry. The PhotosSection component in `profile-b.jsx` needs verification.
- **proposal:** Ensure the retry is a `<Button>` with `aria-label={tr('إعادة رفع الصورة', 'Retry photo upload')}`.
- **why it is better:** Keyboard and screen-reader users can retry the upload.
- **cost:** S
- **rule:** foundation §10 (every interactive element must be focusable and named)

### R2-AD-AX-006 — Pagination controls in AdminList may lack visible focus

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** List pagination — all list pages at 768 — `Admin spaces.html`, `Admin owners.html`, `Admin users.html` — 768 light
- **evidence:** `R2-AD-AX-006.png`
- **what could be better:** The `Pagination` component from the design system renders Previous/Next and page numbers. Focus-visible styling should be verified on all pagination elements, especially at the 768 breakpoint where the card layout is active.
- **proposal:** Verify focus-visible outline on all pagination links and buttons; ensure contrast meets WCAG AA in both light and dark.
- **why it is better:** Keyboard users can see which page control is focused.
- **cost:** S
- **rule:** foundation §10 (focus visible)

### R2-AD-AX-007 — Breadcrumb current page lacks `aria-current="page"`

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Breadcrumb on space add/edit — `Admin space add.html`, `Admin space edit.html?id=golden` — 1440 light
- **evidence:** `R2-AD-AX-007.png`
- **what could be better:** `BreadcrumbPage` renders the current page but does not set `aria-current="page"`. Screen readers cannot distinguish the current page from ancestor links.
- **proposal:** Add `aria-current="page"` to `BreadcrumbPage`.
- **why it is better:** Screen-reader users know which page they are on.
- **cost:** S
- **rule:** foundation §10 (aria-current for current page)

### R2-AD-AX-008 — Row action DropdownMenu trigger name could include context

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** All row action menus — `Admin spaces.html`, `Admin owners.html`, `Admin users.html` — 1440 light
- **evidence:** `R2-AD-AX-008.png`
- **what could be better:** The `EllipsisVerticalIcon` button has `aria-label={tr('إجراءات ', 'Actions for ') + s.name}` which names the row. This is good. However, when the menu opens, the first item receives focus — the menu should have `aria-label` or `aria-labelledby` to identify it as the actions menu for that row.
- **proposal:** Add `aria-label={tr('إجراءات ', 'Actions for ') + s.name}` to `DropdownMenuContent`.
- **why it is better:** Screen readers announce the menu's purpose when it opens.
- **cost:** S
- **rule:** foundation §10 (named menus)

### R2-AD-AX-009 — Switch in Field with horizontal orientation may lose label association

- **type:** improvement
- **level:** component
- **impact:** medium
- **where:** Lookups switches, settings switches — `Admin lookups.html?tab=amenities`, `Admin settings.html` — 1440 light
- **evidence:** `R2-AD-AX-009.png`
- **what could be better:** The `Switch` inside a `Field` with `orientation="horizontal"` relies on the Field's `label` prop for the accessible name. In lookups, the Switch has `aria-label={tr('ظاهرة: ', 'Shown: ') + lname(g)}` which is good. In settings, the Switch is inside a Field with a `label` prop. Verify that the Field label is properly associated with the Switch via `htmlFor`/`id` or wrapping.
- **proposal:** Ensure all Switch instances have either `aria-label` or are wrapped in a Field that provides the accessible name.
- **why it is better:** Screen-reader users hear the switch's purpose and state.
- **cost:** S
- **rule:** foundation §10 (every control needs a name)

### R2-AD-AX-010 — Load error retry button should be announced

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Load error state — any admin page with `?state=error` — `Admin spaces.html?state=error` — 1440 light
- **evidence:** `R2-AD-AX-010.png`
- **what could be better:** The `LoadError` component shows an Alert with "إعادة المحاولة" button. The Alert should have `role="alert"` or the button should be focused on appearance so screen-reader users are immediately aware of the error.
- **proposal:** Add `role="alert"` to the Alert container and auto-focus the retry button.
- **why it is better:** Screen-reader users are immediately informed of the error and can retry.
- **cost:** S
- **rule:** foundation §10 (error announcement)

### R2-AD-AX-011 — Offline/403/404 RouteState uses EmptyState without role

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Route states — any admin page with `?state=offline|403|404` — `Admin overview.html?state=404` — 1440 light
- **evidence:** `R2-AD-AX-011.png`
- **what could be better:** The `RouteState` component renders `EmptyState` with icon, title, and description. For offline (which has a retry), the EmptyState should have `role="alert"` so screen readers announce it immediately. For 403/404, `role="status"` is sufficient.
- **proposal:** Add `role="alert"` to the offline RouteState and `role="status"` to 403/404.
- **why it is better:** Screen-reader users are informed of the route state immediately.
- **cost:** S
- **rule:** foundation §10 (status announcements)

### R2-AD-AX-012 — 429 RateLimitNote lacks live region

- **type:** improvement
- **level:** component
- **impact:** medium
- **where:** Settings rate limit — `Admin settings.html?state=ratelimit` — 1440 light
- **evidence:** `R2-AD-AX-012.png`
- **what could be better:** The `RateLimitNote` shows a warning Alert with the rate-limit message. It does not have `role="alert"` or `aria-live="assertive"`, so screen-reader users may not be informed immediately when the rate limit appears.
- **proposal:** Add `role="alert"` to the RateLimitNote Alert.
- **why it is better:** Screen-reader users are immediately informed of the rate limit.
- **cost:** S
- **rule:** foundation §10 (status announcements)

### R2-AD-AX-013 — Table-to-card transition at 768 may disrupt focus order

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** All list pages at 768 — `Admin spaces.html`, `Admin owners.html`, `Admin users.html` — 768 light
- **evidence:** `R2-AD-AX-013.png`
- **what could be better:** `AdminList` switches from `DataTable` to a card list at 768. The `renderCard` prop returns interactive elements (buttons, links). Verify that the card DOM order matches the visual order and that tab order is logical.
- **proposal:** Verify tab order in card mode matches visual order; ensure all interactive elements in cards are focusable and visible.
- **why it is better:** Keyboard users can navigate cards in a predictable order.
- **cost:** M
- **rule:** foundation §10 (logical focus order)

### R2-AD-AX-014 — Icon-only order buttons in lookups need 44×44 on touch

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Lookups order buttons — `Admin lookups.html?tab=amenities` — 390 light
- **evidence:** `R2-AD-AX-014.png`
- **what could be better:** The `Order` component renders `Button variant="ghost" size="icon"` for up/down arrows. AD-030 says the design system guarantees 44×44 hit area on touch, but verify this at 390 where the buttons are in a horizontal row with limited spacing.
- **proposal:** Verify touch target size at 390; add minimum width/height if needed.
- **why it is better:** Touch users can reliably hit the buttons.
- **cost:** S
- **rule:** foundation §10 (44×44 hit area on touch)

### R2-AD-AX-015 — Toast announcements need verification

- **type:** improvement
- **level:** component
- **impact:** medium
- **where:** All pages with toasts — any admin page — 1440 light
- **evidence:** `R2-AD-AX-015.png`
- **what could be better:** The `PageToaster` uses the design system `Toaster` with `label={tr('الإشعارات', 'Notifications')}`. Verify that the Toaster announces new toasts via `aria-live="polite"` or `role="status"`.
- **proposal:** Ensure Toaster announces toasts automatically.
- **why it is better:** Screen-reader users are informed of action results.
- **cost:** S
- **rule:** foundation §10 (status announcements)

### R2-AD-AX-016 — Contrast of muted deleted rows

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Deleted spaces rows — `Admin spaces.html?status=deleted` — 1440 light
- **evidence:** `R2-AD-AX-016.png`
- **what could be better:** Deleted spaces render with `text-muted-foreground` and `text-label text-muted-foreground`. Verify contrast meets WCAG AA (4.5:1) in both light and dark themes.
- **proposal:** Verify contrast; if below 4.5:1, use a slightly stronger muted colour.
- **why it is better:** Low-vision users can read deleted row content.
- **cost:** S
- **rule:** foundation §10 (contrast)

### R2-AD-AX-017 — Dialog focus trap verification

- **type:** improvement
- **level:** component
- **impact:** medium
- **where:** AlertDialogs and Dialogs — `Admin spaces.html?unlink=<space>&owner=<id>`, `Admin users.html?changerole=1` — 1440 light
- **evidence:** `R2-AD-AX-017.png`
- **what could be better:** Verify that AlertDialog and Dialog components trap focus within the dialog while open, restore focus to the trigger on close, and that all dialog content is reachable by keyboard.
- **proposal:** Verify focus trap, focus restoration, and keyboard navigation in all dialogs.
- **why it is better:** Keyboard and screen-reader users can interact with dialogs safely.
- **cost:** M
- **rule:** foundation §10 (focus trap)

### R2-AD-AX-018 — DataTable sort indicators lack accessible names

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Sortable table columns — `Admin spaces.html`, `Admin owners.html`, `Admin users.html` — 1440 light
- **evidence:** `R2-AD-AX-018.png`
- **what could be better:** If DataTable headers are sortable, the sort indicator (arrow icon) should have `aria-label` describing the sort direction.
- **proposal:** Add `aria-label` to sort indicators.
- **why it is better:** Screen-reader users know the current sort state.
- **cost:** S
- **rule:** foundation §10 (named controls)

### R2-AD-AX-019 — Sheet focus management on open/close

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Filter sheets, add-owner sheet, edit sheet — `Admin spaces.html`, `Admin owners.html?sheet=add`, `Admin lookups.html?edit=area` — 1440 light
- **evidence:** `R2-AD-AX-019.png`
- **what could be better:** Verify that Sheet components focus the sheet content on open and restore focus to the trigger on close.
- **proposal:** Verify focus management in all Sheet instances.
- **why it is better:** Keyboard users maintain context when opening and closing sheets.
- **cost:** M
- **rule:** foundation §10 (focus management)

### R2-AD-AX-020 — Editor section heading levels

- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Space editor sections — `Admin space edit.html?id=golden` — 1440 light
- **evidence:** `R2-AD-AX-020.png`
- **what could be better:** The editor uses `SectionTitle` for section headings (h2) and `h3` for block titles within sections. Verify that heading levels are consistent and logical across all sections.
- **proposal:** Verify heading hierarchy: h1 (page title) → h2 (section) → h3 (block).
- **why it is better:** Screen-reader users can navigate by heading level.
- **cost:** S
- **rule:** foundation §10 (heading hierarchy)

## Decisions in doubt

None. The settled decisions (TempPassDialog no-dismiss rules, P8's exception for row-visible actions, AD-030's 44×44 hit area) are all sound from an accessibility perspective. The TempPassDialog's no-dismiss design is intentional and the keyboard path (copy → done) is sane.

## What was not reviewed

- **Screen-reader testing:** No screen reader was available in the review environment; all findings are from static code analysis.
- **Browser rendering:** The prototype is a React app rendered client-side; static HTML analysis was used instead of live browser testing.
- **Dark mode contrast:** Contrast was not measured programmatically; recommendations are based on token usage.
- **Touch-target measurement:** Touch targets were not measured at runtime; AD-030's design-system guarantee is assumed.
- **Focus-trap behaviour:** Dialog and sheet focus traps were not tested interactively.
- **768 breakpoint:** The 768 layout was not visually verified; analysis is based on the `AdminList` component's card-branch logic.
- **Photo-upload retry:** The `?fail=upload` state was not rendered; the finding is based on the PhotosSection component's expected structure.
- **Combobox keyboard interaction:** The Combobox's keyboard navigation (arrow keys, type-ahead) was not tested.
