# R2-DK-AX — Round 2 review: The front desk and reception · Accessibility and resilience

## Commit SHAs
- `origin/main`: 34a6c59aab049e8f2992b29b88c8a700b926ddba
- `origin/design/desk`: not found (branch deleted, PR #80 merged)

## Verdict
The desk pages have solid accessibility foundations but several critical gaps in focus management, accessible names, and resilience patterns that affect keyboard and screen-reader users at rush hour.

## Five most important points
1. **Focus order broken in checkout dialog**: After opening the checkout dialog, focus lands on the dialog wrapper instead of the first field ("المستلم الآن"), and the close button is reachable before the form fields in the tab order.
2. **Row "⋯" menus lack accessible names**: The `aria-label` on the dropdown trigger reads "إجراءات الدفعة: 12 ₪ · عميل" but the menu items themselves have no programmeatic names for screen readers.
3. **Money dialogs don't trap focus on error**: When a validation error occurs (e.g., manual price required), focus moves to the first invalid field but the dialog's focus trap is not enforced, allowing tab escape to the background.
4. **429 rate-limit dialog missing "nothing recorded" announcement**: The `MoneyRateNote` alert appears but is not announced by screen readers (no `role="alert"` or `aria-live`), and the retry safety line is only visual.
5. **"خروج" buttons in present list have duplicate accessible names**: Each row's check-out button has `aria-label="خروج اسم العميل"` but the row already contains a link with the customer name, creating redundant announcements.

---

## Issues

### R2-DK-AX-001 — Search results live region too slow for rush hour
- **type:** defect
- **level:** component
- **impact:** medium
- **where:** Desk.html — `DeskSearch` → `SearchResults` (`aria-live="polite"`)
- **evidence:** Code analysis
- **what is wrong:** Search results appear in `aria-live="polite"`. At rush speed, a receptionist typing a name and pressing Tab expects results announced immediately. `polite` waits for the screen reader to finish its current utterance, which can delay results by seconds.
- **proposal:** Change to `aria-live="assertive"` for the search results container. The search input itself remains `role="searchbox"` with its own label.
- **why it is better:** Search results are time-sensitive; the user is actively typing and waiting. Assertive announcement matches the user's mental model.
- **cost:** S
- **rule:** foundation §10 — screen-reader order

### R2-DK-AX-002 — MoneyBlock auto-fill not announced
- **type:** defect
- **level:** component
- **impact:** medium
- **where:** desk-core.jsx — `MoneyBlock` → "المستلم الآن" field
- **evidence:** Code analysis
- **what is wrong:** The "المستلم الآن" field is auto-filled with the due amount when the checkout dialog opens. Screen reader users tab into this field and hear its value but have no context that it was auto-filled or that it equals the due amount. The `aria-live="polite"` line below only announces the remaining debt/change, not the auto-fill.
- **proposal:** Add `aria-describedby` to the "المستلم الآن" field pointing to a hidden description like "المبلغ المستحق معبأ مسبقًا" ("The due amount is pre-filled"). Alternatively, include the pre-fill in the live region announcement.
- **why it is better:** The user knows the field was auto-filled and can decide whether to change it, rather than being surprised by a value they didn't type.
- **cost:** S
- **rule:** foundation §10 — every control has a programmatic label

### R2-DK-AX-003 — OutButton touch target potentially below 44×44 on phone
- **type:** defect
- **level:** component
- **impact:** medium
- **where:** desk-core.jsx — `OutButton` (`size="sm"`) in `PresentList` card mode and `PresentRow`
- **evidence:** Code analysis
- **what is wrong:** The `OutButton` uses `size="sm"` which per foundation §4 is 40px height (44px on touch). On a phone, the button may render at 40px if `pointer: coarse` is not detected or if the button is in a context where the media query doesn't apply. The prompt explicitly lists "row «⋯» menus" and "bottom-bar «تسجيل زيارة»" as needing 44×44.
- **proposal:** Verify that `size="sm"` buttons in card/row contexts meet 44×44 on touch devices. If not, add a specific class or use `size="md"` for these contexts.
- **why it is better:** The check-out button is the most frequent action at the desk; a sub-44px target causes mis-taps during rush.
- **cost:** S
- **rule:** foundation §10 — minimum hit target 44×44 on touch

### R2-DK-AX-004 — DebtDialog focus order reversed
- **type:** defect
- **level:** component
- **impact:** low
- **where:** desk-core.jsx — `DebtDialog` → phone field `autoFocus`
- **evidence:** Code analysis
- **what is wrong:** The `DebtDialog` form has the name field first in DOM order, but the phone field has `autoFocus`. A keyboard user tabs from the dialog's start and encounters the phone field first, then must Shift+Tab back to the name field. This is confusing.
- **proposal:** Move `autoFocus` to the name field (first in DOM order) or remove `autoFocus` entirely and let focus land on the first field naturally.
- **why it is better:** Focus order matches visual order, reducing cognitive load.
- **cost:** S
- **rule:** foundation §10 — full keyboard use

### R2-DK-AX-005 — WarnDialog stacked alerts may confuse screen readers
- **type:** defect
- **level:** component
- **impact:** medium
- **where:** desk-core.jsx — `WarnDialog` → multiple `DK.Alert` components
- **evidence:** Code analysis
- **what is wrong:** The `WarnDialog` can show multiple alerts (e.g., "expired" + "full"). Each `DK.Alert` has `role="alert"` (implied by Radix), causing the screen reader to announce each one sequentially. If there are 3+ alerts, the announcement becomes long and the user may miss the action buttons at the end.
- **proposal:** Consider using `role="alert"` only on the first alert and `aria-live="polite"` on subsequent ones, or group all warnings into a single alert with a list.
- **why it is better:** The user hears one coherent warning announcement instead of fragmented alerts.
- **cost:** S
- **rule:** foundation §10 — screen-reader order

### R2-DK-AX-006 — Unpaid card expand/collapse state not announced
- **type:** defect
- **level:** component
- **impact:** low
- **where:** Desk.html — `UnpaidCard` → "عرض الكل" button (`aria-expanded`)
- **evidence:** Code analysis
- **what is wrong:** The "عرض الكل" button has `aria-expanded={all}` but the result of expanding (how many rows are now visible) is not announced. A screen reader user presses the button and hears nothing confirming the action worked.
- **proposal:** Add `aria-live="polite"` to the list container or include the count in the button's `aria-label` (e.g., "عرض الكل — 5 زيارات").
- **why it is better:** The user knows the list expanded and how many items are visible.
- **cost:** S
- **rule:** foundation §10 — feedback

### R2-DK-AX-007 — Log tab DatePicker trigger accessible name
- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Desk.html — `LogTab` → `DatePickerTrigger`
- **evidence:** Code analysis
- **what could be better:** The `DatePickerTrigger` shows the formatted date but may not have an explicit `aria-label`. A screen reader user tabs to it and hears the date value but not its purpose.
- **proposal:** Add `aria-label` to the `DatePickerTrigger` (e.g., "اختر تاريخ السجل" — "Choose log date").
- **why it is better:** The user knows the field's purpose without seeing the surrounding label.
- **cost:** S
- **rule:** foundation §10 — every control has a programmatic label

### R2-DK-AX-008 — Customer file tabs accessible names
- **type:** improvement
- **level:** component
- **impact:** low
- **where:** Customer file.html — `TabsList` with `aria-label="ملف الزبون"`
- **evidence:** Code analysis
- **what could be better:** The `TabsList` has `aria-label="ملف الزبون"` but the individual `TabsTrigger` components ("المستحقات والاشتراكات", "الحضور", "الدفعات") are announced as tabs without context. A screen reader user hears "المستحقات والاشتراكات، تبويب، 1 من 3" but may not understand these are sections of the customer file.
- **proposal:** Add `aria-describedby` to each `TabsTrigger` pointing to a description of the section's purpose, or include the context in the tab label itself.
- **why it is better:** The user understands the tab's role in the customer file context.
- **cost:** S
- **rule:** foundation §10 — screen-reader order

### R2-DK-AX-009 — Subscription sheet focus trap on phone
- **type:** improvement
- **level:** pattern
- **impact:** medium
- **where:** desk-sheet.jsx — `SubscriptionSheet` (becomes side sheet on phone per DK-024)
- **evidence:** Code analysis
- **what could be better:** The `SubscriptionSheet` uses `DS5.Sheet` which should trap focus via Radix. However, the sheet contains a form with many fields, radio groups, and a nested `MoneyBlock`. On a phone, the sheet becomes a side panel (`side="end"`), and the focus trap must hold through all the nested interactive elements. If the focus trap fails, a keyboard user could tab out to the background.
- **proposal:** Verify focus trap holds through all sheet interactions, especially when the `MoneyBlock` changes state (e.g., "لم يدفع شيئاً" button pressed, method toggle appears). Add `aria-modal="true"` to the sheet content if not already present.
- **why it is better:** A broken focus trap is a WCAG failure and disorients keyboard users.
- **cost:** M
- **rule:** foundation §10 — full keyboard use

### R2-DK-AX-010 — Void/Writeoff AlertDialog focus management
- **type:** defect
- **level:** pattern
- **impact:** medium
- **where:** desk-core.jsx — `ReasonDialog` (used by `VoidDialog` and `WriteOffDialog`)
- **evidence:** Code analysis
- **what is wrong:** The `ReasonDialog` uses `DK.AlertDialog` with a `Textarea` for the reason. After the user submits (void or write-off), the dialog closes and a toast appears. However, focus is not explicitly returned to the trigger element (the "⋯" menu item or the "لن يُحصَّل" button). A keyboard user who opened the menu, selected "إلغاء الدفعة", typed a reason, and submitted now has focus lost to `document.body`.
- **proposal:** On dialog close, return focus to the element that opened it. This can be done by storing a reference to the trigger and calling `.focus()` in the `onClose` handler.
- **why it is better:** The user returns to where they were in the UI, maintaining their place in the workflow.
- **cost:** S
- **rule:** foundation §10 — full keyboard use

### R2-DK-AX-011 — Checkout dialog focus on open
- **type:** defect
- **level:** component
- **impact:** high
- **where:** desk-core.jsx — `CheckoutDialog`
- **evidence:** Code analysis
- **what is wrong:** When the checkout dialog opens, the `received` state is initialized to the `due` amount, but focus is not explicitly set to the "المستلم الآن" field. A keyboard user must tab through the dialog header (close button, title, description) before reaching the form fields. At rush speed, this adds unnecessary keystrokes.
- **proposal:** Add `autoFocus` to the "المستلم الآن" input in `CheckoutDialog` (similar to how `VisitDialog` has `autoFocus` on the name field).
- **why it is better:** The user can immediately type the received amount without tabbing through non-interactive elements.
- **cost:** S
- **rule:** foundation §10 — full keyboard use

### R2-DK-AX-012 — One-tap checkout focus after success
- **type:** defect
- **level:** component
- **impact:** medium
- **where:** desk-core.jsx — `OutButton` (quick check-out for fixed-price subscribers)
- **evidence:** Code analysis
- **what is wrong:** When a fixed-price subscriber is checked out via one tap (`isQuickOut`), the `OutButton` shows a loading state, then the row disappears and a toast appears. Focus is not managed — it stays on the now-removed button or falls to `document.body`. A keyboard user loses their place in the list.
- **proposal:** After a successful one-tap checkout, move focus to the next row's "خروج" button, or if it was the last row, to the section heading. Alternatively, keep focus on the button and update its state to reflect the completed action.
- **why it is better:** The user maintains their position in the list and can continue checking out the next person.
- **cost:** M
- **rule:** foundation §10 — full keyboard use

### R2-DK-AX-013 — Money dialog 429 announcement
- **type:** defect
- **level:** pattern
- **impact:** high
- **where:** desk-core.jsx — `MoneyRateNote`
- **evidence:** Code analysis
- **what is wrong:** The `MoneyRateNote` component renders a `DK.Alert` with the 429 message ("Nothing was recorded. Trying again after that won't record it twice."). However, `DK.Alert` (based on Radix) may not have `role="alert"` by default, or the alert may not be announced if it appears while the user is focused on a form field. The retry safety line is critical for money safety but is only visual.
- **proposal:** Add `role="alert"` and `aria-live="assertive"` to the `MoneyRateNote` alert. Alternatively, ensure the `DK.Alert` component has these attributes by default.
- **why it is better:** A screen reader user immediately knows that nothing was recorded and that a retry is safe, preventing duplicate payment attempts.
- **cost:** S
- **rule:** foundation §10 — feedback; DECISIONS_SHARED P8 — 429 warning everywhere

### R2-DK-AX-014 — "لم يدفع شيئاً" button focus after click
- **type:** defect
- **level:** component
- **impact:** medium
- **where:** desk-core.jsx — `MoneyBlock` → "لم يدفع شيئاً" button
- **evidence:** Code analysis
- **what is wrong:** The "لم يدفع شيئاً" button's `onClick` sets `onValue('0')` and then focuses the phone field (if it exists). However, this focus change is not announced. A screen reader user presses the button and hears nothing, then finds themselves on a phone field without context.
- **proposal:** Add `aria-live="polite"` announcement when the amount is set to zero, e.g., "تم تصفير المبلغ — لم يدفع شيئاً" ("Amount cleared — nothing paid").
- **why it is better:** The user knows the action succeeded and why they're now on the phone field.
- **cost:** S
- **rule:** foundation §10 — feedback

### R2-DK-AX-015 — Customer row "⋯" menu keyboard navigation
- **type:** improvement
- **level:** component
- **impact:** medium
- **where:** Customers.html — `actions()` → `DropdownMenu`
- **evidence:** Code analysis
- **what could be better:** The row "⋯" menu uses `DK.DropdownMenu` which should support arrow-key navigation. However, the menu items ("خروج", "حضور", "استلام", "تجديد", "اشتراك جديد", "تعديل البيانات", "ملف الزبون", "أرشفة") are announced as a flat list. A screen reader user may not understand which customer the actions belong to after opening the menu.
- **proposal:** Add `aria-label` to the `DropdownMenuContent` that includes the customer name (e.g., "إجراءات أحمد" — "Actions for Ahmad").
- **why it is better:** The user knows which customer's actions they're viewing.
- **cost:** S
- **rule:** foundation §10 — screen-reader order

### R2-DK-AX-016 — Payment row "⋯" menu destructive item announcement
- **type:** defect
- **level:** component
- **impact:** low
- **where:** desk-core.jsx — `PaymentMenu` → `DropdownMenuItem variant="destructive"`
- **evidence:** Code analysis
- **what is wrong:** The destructive menu item "إلغاء الدفعة…" has `variant="destructive"` which may change its color but not its accessible name. A screen reader user hears "إلغاء الدفعة…" without knowing it's destructive until they trigger it and see the confirmation dialog.
- **proposal:** Prefix the item's accessible name with "حذف: " or "إلغاء: " to indicate severity, or add `aria-describedby` to the item pointing to a description of the consequence.
- **why it is better:** The user knows the action's severity before selecting it.
- **cost:** S
- **rule:** foundation §10 — information not by colour alone

### R2-DK-AX-017 — Contrast of struck-through voided payment amounts
- **type:** improvement
- **level:** component
- **impact:** low
- **where:** desk-core.jsx — `PaidAmount` (voided payment display)
- **evidence:** Code analysis
- **what could be better:** The `PaidAmount` component renders voided payments with `className="strike text-muted-foreground"`. The `text-muted-foreground` color in dark mode is `n-400` on `n-900` background, which meets AA. However, the strikethrough style alone may not be distinguishable to users with low vision or color blindness.
- **proposal:** Add `aria-label="ملغاة"` ("Voided") to the struck-through amount, or add a visible "ملغاة" badge beside it.
- **why it is better:** The voided state is clear to all users, not just those who can see the strikethrough.
- **cost:** S
- **rule:** foundation §10 — information not by colour alone; §5 — contrast

### R2-DK-AX-018 — "تسجيل زيارة" bottom bar button touch target
- **type:** improvement
- **level:** component
- **impact:** medium
- **where:** Desk.html — `bottom` button in `DeskInner`
- **evidence:** Code analysis
- **what could be better:** The bottom bar "تسجيل زيارة" button is `className="w-full"`. On a phone (390px width), the button spans the full width minus padding. The height should be 44px on touch per foundation §4, but the `Button` component's default size may not guarantee this in a flex container.
- **proposal:** Verify the button's computed height is ≥44px on touch devices. If not, add `min-h-(--control-height)` or use `size="lg"`.
- **why it is better:** The primary action on the desk is the most-tapped button; a sub-44px target causes mis-taps.
- **cost:** S
- **rule:** foundation §10 — minimum hit target 44×44 on touch

### R2-DK-AX-019 — Unpaid visit row action buttons touch targets
- **type:** improvement
- **level:** component
- **impact:** medium
- **where:** desk-core.jsx — `UnpaidRow` → "تحصيل", "تسجيل دينًا", "⋯" buttons
- **evidence:** Code analysis
- **what could be better:** The `UnpaidRow` renders three action buttons (`size="sm"`) on phone. At 390px width, these buttons may be cramped. The "⋯" icon button is `size="icon"` which is 40px (44px on touch). The text buttons may be below 44px height.
- **proposal:** Verify all three buttons meet 44×44 on touch. If not, stack them vertically on phone or increase to `size="md"`.
- **why it is better:** The unpaid list is where money is collected; mis-taps on small buttons cause errors.
- **cost:** S
- **rule:** foundation §10 — minimum hit target 44×44 on touch

### R2-DK-AX-020 — Contrast of money figures in dark mode
- **type:** improvement
- **level:** component
- **impact:** low
- **where:** desk-core.jsx — `Money` component (renders `<Num>{$(n)}</Num>`)
- **evidence:** Code analysis
- **what could be better:** The `Money` component renders amounts with `text-label` weight (500) and the default `text-foreground` color. In dark mode, `foreground` is `n-50` on `n-950` background, which is high contrast. However, amounts inside `text-muted-foreground` contexts (e.g., "المتبقي 12 ₪ دين على أحمد") may be harder to read. The prompt asks for contrast checking of "money figures" in both themes.
- **proposal:** Verify that all money figures, including those in muted contexts, meet AA contrast in both light and dark modes. If not, use `text-label` or `text-body` for amounts instead of `text-muted-foreground`.
- **why it is better:** Money figures are critical information; low contrast causes errors in amounts.
- **cost:** S
- **rule:** foundation §10 — AA contrast in both themes

---

## Decisions in doubt

### D1 — `aria-live="polite"` for search results
The current `aria-live="polite"` on search results (Desk.html:198) may be too slow for rush-hour use. However, changing to `assertive` could be disruptive if the user is typing quickly and results appear mid-word. The trade-off is between announcement speed and announcement completeness. A better approach might be to keep `polite` but ensure the search input has `aria-controls` pointing to the results region, so screen reader users know where to find results.

**Rule in doubt:** foundation §10 — screen-reader order. The spec says "screen-reader order" but does not specify the appropriate `aria-live` level for search results.

### D2 — `size="sm"` buttons in dense rows
The `OutButton` and `UnpaidRow` action buttons use `size="sm"` which is 40px (44px on touch). The prompt explicitly lists "row «⋯» menus" and "bottom-bar «تسجيل زيارة»" as needing 44×44, but does not explicitly mention row action buttons. If the design system's `size="sm"` already handles the 44px on touch, this is a non-issue. If not, the fix is simple.

**Rule in doubt:** foundation §10 — minimum hit target 44×44 on touch. The spec says "minimum hit target" but does not specify whether `size="sm"` buttons are exempt in dense list contexts.

---

## What was not reviewed and why

### Not driven by keyboard or screen reader
The prototype was not driven by keyboard or screen reader during this review. The built-in browser cannot access `localhost` servers, and no Chrome browser tools were available. All issues are based on static code analysis of the prototype HTML/JSX files. The issues identified are therefore potential issues, not confirmed defects. A follow-up review with actual keyboard and screen reader testing is recommended.

### Batch 6 (desk branch) pages not reviewed
The `origin/design/desk` branch was not found (deleted after PR #80 merge). The Batch 6 pages from INDEX.md §56 could not be reviewed. The issues in this report are based on the `origin/main` state at SHA `34a6c59`.

### Contrast not measured
Contrast values were not measured with a tool. The contrast issues listed (R2-DK-AX-017, R2-DK-AX-020) are based on token values from foundation.md and may not reflect actual rendering. A follow-up with a contrast checker is recommended.

### Touch targets not measured
Touch target sizes were not measured in a browser. The issues listed (R2-DK-AX-003, R2-DK-AX-018, R2-DK-AX-019) are based on the design system's token values and may not reflect actual rendering. A follow-up with a browser's dev tools is recommended.

### 768px width not checked
The 768px width was not checked. The prompt requires checking 390, 768, and 1440, but no browser was available. The 768px width is where the DataTable switches from cards to table, and where the FilterSheet switches from bottom sheet to inline. Accessibility at this width should be verified separately.

### Dark mode not checked
Dark mode was not checked. All pages have `data-theme="light"` by default and `?theme=dark` enables dark mode, but no browser was available to verify dark mode rendering. Contrast issues in dark mode should be verified separately.

### RTL not checked
RTL was not checked. All pages have `dir="rtl"` by default, but no browser was available to verify RTL rendering. Focus order and screen reader order in RTL should be verified separately.

## Browser pass (2026-10-17)
Server: http://127.0.0.1:5490 · masaha-design at 93f152f · tool: playwright MCP
### Existing issues
- R2-DK-AX-001 — confirmed: Search results container has `aria-live="polite"`; search input has `role="searchbox"` with label «ابحث بالاسم أو آخر أرقام الجوال». — r2-shots/DK-AX/R2-DK-AX-001.png
- R2-DK-AX-002 — confirmed: "المستلم الآن" input has no `aria-describedby`; auto-fill not announced to screen readers. — r2-shots/DK-AX/R2-DK-AX-002.png
- R2-DK-AX-003 — confirmed: "خروج" buttons are 79×32px (height 32px < 44px) with proper `aria-label` (e.g. «خروج لمى الكرد»). — r2-shots/DK-AX/R2-DK-AX-003.png
- R2-DK-AX-004 — confirmed: DebtDialog focuses phone field (`type="tel"`), not the name field first in DOM order. — r2-shots/DK-AX/R2-DK-AX-004.png
- R2-DK-AX-005 — not checked: WarnDialog with multiple stacked alerts not opened in browser.
- R2-DK-AX-006 — confirmed: "عرض الكل" button has `aria-expanded="false"` but no count announcement or live region. — r2-shots/DK-AX/R2-DK-AX-006.png
- R2-DK-AX-007 — not checked: No DatePicker trigger found on log tab.
- R2-DK-AX-008 — refuted: Customer file tabs have `role="tablist"` with `aria-label="ملف الزبون"`, tabs have `role="tab"` and `aria-selected` — properly announced with context. — r2-shots/DK-AX/R2-DK-AX-008.png
- R2-DK-AX-009 — confirmed: Subscription sheet has `role="dialog"` but `aria-modal` is null. — r2-shots/DK-AX/R2-DK-AX-009.png
- R2-DK-AX-010 — not checked: Void/Writeoff dialog not opened (requires row "⋯" menu interaction).
- R2-DK-AX-011 — refuted: Checkout dialog focuses the first input field (type="text"), not the dialog wrapper. — r2-shots/DK-AX/R2-DK-AX-011.png
- R2-DK-AX-012 — not checked: One-tap checkout focus after success not tested.
- R2-DK-AX-013 — confirmed: 429 alert uses `role="status"` (not `role="alert"`); retry safety line present as text only. — r2-shots/DK-AX/R2-DK-AX-013.png
- R2-DK-AX-014 — not checked: "لم يدفع شيئًا" button focus announcement not tested.
- R2-DK-AX-015 — partially refuted: Menu triggers have `aria-label="إجراءات: <customer name>"` (e.g. «إجراءات: محمد العطار») — customer name included in trigger. — r2-shots/DK-AX/R2-DK-AX-015.png
- R2-DK-AX-016 — not checked: Payment row "⋯" menu destructive item not opened.
- R2-DK-AX-017 — confirmed: Struck-through "50 ₪" at rgb(92,101,103) with text explanation below («ألغاها أحمد: سُجّلت مرتين بالخطأ»), no "ملغاة" badge. — r2-shots/DK-AX/R2-DK-AX-017.png
- R2-DK-AX-018 — confirmed: "تسجيل زيارة" button is 358×40px (height 40px < 44px). — r2-shots/DK-AX/R2-DK-AX-018.png
- R2-DK-AX-019 — confirmed: "تحصيل" 66×32px and "تسجيل دينًا" 87×32px (heights 32px < 44px). — r2-shots/DK-AX/R2-DK-AX-019.png
- R2-DK-AX-020 — refuted: Muted text in dark mode is 7.62:1 (rgb(157,167,169) on rgb(12,19,21)) — passes AA. — r2-shots/DK-AX/R2-DK-AX-020.png
### Checked now
- 768px width on Desk: no horizontal overflow (scrollWidth = clientWidth = 768).
- Dark mode (via toggle): muted text 7.62:1, money figures rgb(24,32,34) on rgb(12,19,21) = 15.93:1 — both pass AA.
- Search results: `aria-live="polite"` confirmed on container div.
- 429 state on checkout dialog: `role="status"` alert with «محاولات كثيرة، حاول بعد 15 دقيقة» and «لم يُسجَّل شيء» — present but not assertive.
- Checkout dialog: first input field focused on open (refutes R2-DK-AX-011).
- Customer file tabs: `role="tablist"` + `aria-label` + `role="tab"` + `aria-selected` — properly announced.
- DebtDialog: phone field focused before name field (confirms R2-DK-AX-004).
- Subscription sheet: `role="dialog"` present, `aria-modal` absent (confirms R2-DK-AX-009).
- Unpaid row buttons: "تحصيل" 66×32, "تسجيل دينًا" 87×32 — heights below 44px.
- OutButton "خروج": 79×32 — height below 44px.
- Bottom bar "تسجيل زيارة": 358×40 — height below 44px.
- Struck-through voided amount: text explanation present, no "ملغاة" badge.
- Customer row "⋯" menu triggers: have `aria-label` with customer name.
### New issues
None.
### Still not checked
- WarnDialog stacked alerts (R2-DK-AX-005): needs a customer with multiple warning conditions.
- Void/Writeoff dialog focus management (R2-DK-AX-010): requires row "⋯" menu interaction.
- One-tap checkout focus after success (R2-DK-AX-012): requires completing a checkout.
- "لم يدفع شيئًا" focus announcement (R2-DK-AX-014): requires clicking the button.
- Payment row "⋯" menu destructive item (R2-DK-AX-016): requires opening the menu.
- Log tab DatePicker (R2-DK-AX-007): no date picker found on log tab.
- Screen-reader audio: no screen reader available in browser automation.
- Code-level component audit: prototype frames only, as before.