# R2-OW-AX — Round 2 review: The owner's management · Accessibility and resilience

## 1. Commit SHAs

- HEAD: `18ab1705149773bd05f2f7349ef341e33d175ca3`
- origin/main: `eff0a3d1e332a0161fde267a9a100f889184f550`
- Design unchanged (`git diff --quiet HEAD origin/main -- docs/design` exit 0)

## 2. Verdict

The owner's management shell has a solid accessibility foundation (skip link, semantic landmarks, named icon buttons in the top bar, visible focus on desktop) but has systematic gaps: mobile focus indicators are suppressed, many controls lack accessible names, touch targets are below 44×44 across all widths, and warning badges rely on colour alone.

## 3. The five most important points

1. **Mobile focus invisible** — the language and theme buttons in the mobile top bar compute `outline-style: none`, so keyboard users get no visible focus on the two most frequently used controls.
2. **Missing accessible names** — language buttons, select dropdowns, tab buttons, filter chips, pagination, save buttons, and switches all lack `aria-label` or visible text, so screen readers announce them as unlabeled buttons or comboboxes.
3. **Touch targets below 44×44** — queue links (32px), tab chips (36px), pagination (32px), switches (20×36px), and radio buttons (18px) are all below the minimum at every width.
4. **Warning badges use colour alone** — the "قديمة" (stale) badge in the overview queue uses only the warning colour; no icon or text indicator distinguishes it from an informational badge.
5. **Resilience states are present and correct** — error, offline, 429, and loading states all appear with appropriate messaging and retry mechanisms.

## 4. Issues

### R2-OW-AX-001

- **Title:** Mobile language and theme buttons have no visible focus indicator
- **Type:** defect
- **Level:** design system
- **Impact:** high
- **Where:** Every owner page, mobile top bar. Frame: "Overview — desktop 1440" (also phone 390). URL: `Owner overview.html` at 1440 and 390, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-001.png`
- **What is wrong:** The mobile language button (index 1) and theme button (index 2) compute `outline-width: 3px` but `outline-style: none` when focused. The desktop variants (indices 4–5) correctly compute `outline-style: solid`. Both mobile buttons have `focus-visible:outline-2` in their className, so the CSS rule exists but is being overridden or not applied. A keyboard user on a phone sees no focus ring on these two controls.
- **Proposal:** Remove the `outline-style: none` override or ensure the `focus-visible:outline-2` rule applies. The desktop buttons work correctly, so the mobile variant should match.
- **Why it is better:** Keyboard and switch-device users can see which control is focused.
- **Cost:** S
- **Rule:** foundation §10 (focus visible on every control)

---

### R2-OW-AX-002

- **Title:** Language buttons lack accessible names
- **Type:** defect
- **Level:** component
- **Impact:** high
- **Where:** Every owner page, top bar. Frame: "Overview — desktop 1440". URL: `Owner overview.html`, 1440, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-002.png`
- **What is wrong:** The language toggle buttons (both mobile index 1 and desktop index 4) have `aria-label: null` and visible text "English" (or "العربية"). A screen reader announces "English" or "العربية" but not what the button does — it does not say "Switch language" or "Language: Arabic". The user cannot tell whether the button shows the current language or the target language.
- **Proposal:** Add `aria-label` that describes the action and current state, e.g. `aria-label="اللغة: العربية — English"` or `aria-label="Switch to English"`.
- **Why it is better:** Screen reader users understand what the button does and what the current language is.
- **Cost:** S
- **Rule:** foundation §10 (a name for every control)

---

### R2-OW-AX-003

- **Title:** Select dropdowns across owner pages lack accessible names
- **Type:** defect
- **Level:** pattern
- **Impact:** high
- **Where:** Owner space profile (governorate select), Packages (billing type, audience, shift selects), Payments (date range, employees, payment methods, types selects), Finance (month picker), Owner audit (date range, actor, action selects). Frames: "Space profile — desktop 1440", "Packages & prices — desktop 1440", "Payments · this month — desktop 1440", "Finance — الدخل — desktop 1440", "Audit log — the space's — desktop 1440".
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-003.png`
- **What is wrong:** All `<select>` elements across the owner's pages have `aria-label: null`. They have visible text (e.g. "ساعة", "عام", "كل الموظفين", "سبتمبر 2026", "آخر 30 يومًا") but no `aria-label` or `aria-labelledby` associating the label with the control. Screen readers announce the value but not what the field is for.
- **Proposal:** Add `aria-label` to each select describing its purpose, e.g. `aria-label="نوع الفوترة"`, `aria-label="الفترة"`, `aria-label="الموظف"`.
- **Why it is better:** Screen reader users know what each dropdown controls.
- **Cost:** S
- **Rule:** foundation §10 (a name for every control)

---

### R2-OW-AX-004

- **Title:** Tab buttons lack accessible names
- **Type:** defect
- **Level:** pattern
- **Impact:** high
- **Where:** Announcements (نشطة، مجدولة، منتهية), Finance (الدخل، الديون، الإشغال). Frames: "Active · owner — desktop 1440", "Finance — الدخل — desktop 1440".
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-004.png`
- **What is wrong:** Tab buttons have visible text but `aria-label: null`. They are `<button>` elements inside a `tablist` but lack `aria-label` or `aria-labelledby`. Screen readers announce "نشطة" but not "tab" or "announcements tab, active".
- **Proposal:** Add `aria-label` to each tab, e.g. `aria-label="إعلانات نشطة"`, `aria-label="الدخل"`. The `role="tablist"` and `role="tab` may already be present; if so, the accessible name comes from the text content, but the button should still have an explicit label for clarity.
- **Why it is better:** Screen reader users understand the tab's purpose and state.
- **Cost:** S
- **Rule:** foundation §10 (a name for every control)

---

### R2-OW-AX-005

- **Title:** Filter chips lack accessible names
- **Type:** defect
- **Level:** pattern
- **Impact:** high
- **Where:** Data reports (الكل، جديد، تم التصحيح، لم يُعتمد), Payments (إظهار الملغاة). Frames: "List — desktop 1440", "Ledger · this month — desktop 1440".
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-005.png`
- **What is wrong:** Filter chip buttons have visible text but `aria-label: null`. They are `<button>` elements with `data-on` state but no `aria-label` or `aria-pressed`. Screen readers announce "الكل" but not whether it is a toggle or its state.
- **Proposal:** Add `aria-label` and `aria-pressed` (or `aria-selected`) to each chip, e.g. `aria-label="تصفية: الكل"`, `aria-pressed="true"`.
- **Why it is better:** Screen reader users understand the filter's purpose and current state.
- **Cost:** S
- **Rule:** foundation §10 (a name for every control)

---

### R2-OW-AX-006

- **Title:** Pagination buttons lack accessible names
- **Type:** defect
- **Level:** pattern
- **Impact:** high
- **Where:** Staff, Owner audit. Frames: "Staff list — desktop 1440", "Audit log — the space's — desktop 1440".
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-006.png`
- **What is wrong:** Pagination buttons ("السابق", "1", "2", "3", "4", "التالي") have visible text but `aria-label: null`. Screen readers announce "1" or "السابق" but not "page 1" or "previous page".
- **Proposal:** Add `aria-label` to each pagination button, e.g. `aria-label="السابق"`, `aria-label="صفحة 1"`, `aria-label="التالي"`.
- **Why it is better:** Screen reader users understand the pagination context.
- **Cost:** S
- **Rule:** foundation §10 (a name for every control)

---

### R2-OW-AX-007

- **Title:** Save buttons lack accessible names
- **Type:** defect
- **Level:** pattern
- **Impact:** high
- **Where:** Owner space profile, Owner settings, Packages. Frames: "Space profile — desktop 1440", "Owner settings — desktop 1440", "Packages & prices — desktop 1440".
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-007.png`
- **What is wrong:** "حفظ" (Save) buttons have visible text but `aria-label: null`. They appear in multiple sections (hours, prices, contacts, amenities, attendance, pricing, reminder). Screen readers announce "حفظ" but not which section's save it is.
- **Proposal:** Add `aria-label` to each save button, e.g. `aria-label="حفظ ساعات العمل"`, `aria-label="حفظ الأسعار"`.
- **Why it is better:** Screen reader users know which section they are saving.
- **Cost:** S
- **Rule:** foundation §10 (a name for every control)

---

### R2-OW-AX-008

- **Title:** Switches in Owner settings lack accessible names
- **Type:** defect
- **Level:** component
- **Impact:** high
- **Where:** Owner settings (auto check-out at closing, auto check-out after N hours, day price cap, student prices). Frame: "Owner settings — desktop 1440". URL: `Owner settings.html`, 1440, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-008.png`
- **What is wrong:** Switch elements (`role="switch"`) have `aria-label: null`. They have visible labels next to them but no `aria-label` or `aria-labelledby` associating the label with the switch. Screen readers announce "switch, off/on" but not what the switch controls.
- **Proposal:** Add `aria-label` to each switch, e.g. `aria-label="خروج تلقائي عند الإغلاق"`.
- **Why it is better:** Screen reader users understand what each switch controls.
- **Cost:** S
- **Rule:** foundation §10 (a name for every control)

---

### R2-OW-AX-009

- **Title:** Radio buttons in Owner settings lack accessible names
- **Type:** defect
- **Level:** component
- **Impact:** high
- **Where:** Owner settings (rounding options). Frame: "Owner settings — desktop 1440". URL: `Owner settings.html`, 1440, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-009.png`
- **What is wrong:** Radio buttons have `aria-label: null`. They are inside a `radiogroup` with visible labels but no `aria-label` or `aria-labelledby` on each radio. Screen readers announce "radio, checked/not checked" but not which option it is.
- **Proposal:** Add `aria-label` to each radio or ensure the radiogroup has a proper label association.
- **Why it is better:** Screen reader users understand each radio option.
- **Cost:** S
- **Rule:** foundation §10 (a name for every control)

---

### R2-OW-AX-010

- **Title:** Queue links below 44×44 touch target
- **Type:** defect
- **Level:** pattern
- **Impact:** high
- **Where:** Owner overview (queue links: مراجعة، فتح المكتب، عرض، تجديد). Frame: "Overview — desktop 1440". URL: `Owner overview.html`, 1440 and 390, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-010.png`
- **What is wrong:** Queue action links ("مراجعة", "فتح المكتب", "عرض", "تجديد") measure 32px in height at all widths. The minimum touch target is 44×44. On a phone (390px), these are the primary actions for each queue item.
- **Proposal:** Increase the height of queue action links to at least 44px, or wrap them in a button with `min-h-(--control-height)`.
- **Why it is better:** Users with motor impairments or on touch devices can tap the targets reliably.
- **Cost:** S
- **Rule:** foundation §9 (touch targets of at least 44×44)

---

### R2-OW-AX-011

- **Title:** Tab chips below 44×44 touch target
- **Type:** defect
- **Level:** pattern
- **Impact:** high
- **Where:** Announcements, Finance, Data reports. Frames: "Active · owner — desktop 1440", "Finance — الدخل — desktop 1440", "List — desktop 1440".
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-011.png`
- **What is wrong:** Tab chips have `h-9` (36px) height. On mobile they are the primary navigation between sections. 36px is below the 44px minimum.
- **Proposal:** Change `h-9` to `h-(--control-height)` (44px) for tab chips, or add `min-h-(--control-height)` to the chip component.
- **Why it is better:** Users on touch devices can tap the chips reliably.
- **Cost:** S
- **Rule:** foundation §9 (touch targets of at least 44×44)

---

### R2-OW-AX-012

- **Title:** Pagination buttons below 44×44 touch target
- **Type:** defect
- **Level:** pattern
- **Impact:** high
- **Where:** Staff, Owner audit. Frames: "Staff list — desktop 1440", "Audit log — the space's — desktop 1440".
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-012.png`
- **What is wrong:** Pagination buttons have `size-8` (32px) at all widths. On mobile, these are the only way to navigate between pages.
- **Proposal:** Change `size-8` to `size-(--control-height)` (44px) for pagination buttons, or add `min-h-(--control-height) min-w-(--control-height)`.
- **Why it is better:** Users on touch devices can tap pagination reliably.
- **Cost:** S
- **Rule:** foundation §9 (touch targets of at least 44×44)

---

### R2-OW-AX-013

- **Title:** Switches below 44×44 touch target
- **Type:** defect
- **Level:** component
- **Impact:** high
- **Where:** Owner settings, Owner space profile. Frames: "Owner settings — desktop 1440", "Space profile — desktop 1440".
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-013.png`
- **What is wrong:** Switch elements have `h-5 w-9` (20×36px). The after pseudo-element expands the visual size but the clickable area is the outer container. On a phone, these are difficult to tap.
- **Proposal:** Increase the switch container to at least 44×44, or add padding around the switch to expand the touch area.
- **Why it is better:** Users on touch devices can toggle switches reliably.
- **Cost:** S
- **Rule:** foundation §9 (touch targets of at least 44×44)

---

### R2-OW-AX-014

- **Title:** Radio buttons below 44×44 touch target
- **Type:** defect
- **Level:** component
- **Impact:** high
- **Where:** Owner settings. Frame: "Owner settings — desktop 1440". URL: `Owner settings.html`, 1440, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-014.png`
- **What is wrong:** Radio buttons have `size-4.5` (18px). The after pseudo-element expands the visual size but the clickable area is the outer container. On a phone, these are very difficult to tap.
- **Proposal:** Increase the radio container to at least 44×44, or add padding around the radio to expand the touch area.
- **Why it is better:** Users on touch devices can select radio options reliably.
- **Cost:** S
- **Rule:** foundation §9 (touch targets of at least 44×44)

---

### R2-OW-AX-015

- **Title:** Warning badges use colour alone
- **Type:** defect
- **Level:** component
- **Impact:** medium
- **Where:** Owner overview (queue badges "قديمة"). Frame: "Overview — desktop 1440". URL: `Owner overview.html`, 1440, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-015.png`
- **What is wrong:** The "قديمة" (stale) badge uses `bg-warning-subtle text-warning-subtle-foreground` (warning colour). There is no icon or text prefix to distinguish it from an informational badge. A user who cannot perceive colour (colour blindness, monochrome display) cannot tell that this is a warning state.
- **Proposal:** Add an icon (e.g. a clock or warning triangle) before the text, or add a text prefix like "تنبيه: " (warning).
- **Why it is better:** Users who cannot perceive colour can still understand the badge's meaning.
- **Cost:** S
- **Rule:** foundation §10 (information not by colour alone)

---

### R2-OW-AX-016

- **Title:** Menu button on phone below 44×44 touch target
- **Type:** defect
- **Level:** component
- **Impact:** medium
- **Where:** Owner overview (phone 390). Frame: "Overview — phone 390". URL: `Owner overview.html`, 390, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-016.png`
- **What is wrong:** The menu button ("القائمة") measures 40×40px on a phone. This is below the 44×44 minimum. On a phone, this is the primary navigation control.
- **Proposal:** Increase the menu button to at least 44×44px.
- **Why it is better:** Users on touch devices can tap the menu button reliably.
- **Cost:** S
- **Rule:** foundation §9 (touch targets of at least 44×44)

---

### R2-OW-AX-017

- **Title:** Public state button below 44×44 touch target
- **Type:** defect
- **Level:** component
- **Impact:** medium
- **Where:** Every owner page, top bar. Frame: "Overview — phone 390". URL: `Owner overview.html`, 390, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-017.png`
- **What is wrong:** The public state button ("يظهر للزوار: متاح") measures 50×32px on a phone. The height is 32px, below the 44px minimum. This is a primary action on every page.
- **Proposal:** Increase the public state button height to at least 44px on mobile, or add `pointer-coarse:h-(--control-height)`.
- **Why it is better:** Users on touch devices can tap the state button reliably.
- **Cost:** S
- **Rule:** foundation §9 (touch targets of at least 44×44)

---

### R2-OW-AX-018

- **Title:** Governorate select below 44×44 touch target on phone
- **Type:** defect
- **Level:** component
- **Impact:** medium
- **Where:** Owner space profile (phone 390). Frame: "Space profile — phone 390". URL: `Owner space profile.html`, 390, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-018.png`
- **What is wrong:** The governorate select ("النصر") measures 316×40px on a phone. The height is 40px, below the 44px minimum.
- **Proposal:** Increase the select height to at least 44px on mobile, or add `pointer-coarse:h-(--control-height)`.
- **Why it is better:** Users on touch devices can tap the select reliably.
- **Cost:** S
- **Rule:** foundation §9 (touch targets of at least 44×44)

---

### R2-OW-AX-019

- **Title:** Save buttons below 44×44 touch target on phone
- **Type:** defect
- **Level:** pattern
- **Impact:** medium
- **Where:** Owner space profile, Owner settings (phone 390). Frames: "Space profile — phone 390", "Owner settings — phone 390".
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-019.png`
- **What is wrong:** Save buttons ("حفظ") measure 40px in height on a phone. This is below the 44px minimum.
- **Proposal:** Increase save button height to at least 44px on mobile, or add `pointer-coarse:h-(--control-height)`.
- **Why it is better:** Users on touch devices can tap save buttons reliably.
- **Cost:** S
- **Rule:** foundation §9 (touch targets of at least 44×44)

---

### R2-OW-AX-020

- **Title:** Copy-to-all-days button below 44×44 touch target on phone
- **Type:** defect
- **Level:** component
- **Impact:** medium
- **Where:** Owner space profile (phone 390). Frame: "Space profile — phone 390". URL: `Owner space profile.html`, 390, Arabic light.
- **Evidence:** `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-020.png`
- **What is wrong:** The "نسخ إلى كل الأيام" button measures 115×32px on a phone. The height is 32px, below the 44px minimum.
- **Proposal:** Increase the button height to at least 44px on mobile, or add `pointer-coarse:h-(--control-height)`.
- **Why it is better:** Users on touch devices can tap the button reliably.
- **Cost:** S
- **Rule:** foundation §9 (touch targets of at least 44×44)

---

## 5. Decisions in doubt

None. The settled decisions (P1–P10, O1–O13) are not in doubt; the issues above are defects in how the prototype applies them, not problems with the decisions themselves.

## 6. What was not reviewed and why

- **Screen reader order in detail** — the snapshot shows logical DOM order (queue before money, editor sections in order) but full screen reader testing with NVDA or VoiceOver was not performed in this environment.
- **Sheet save failures with retry** — the `?fail=save` and `?fail=save-attendance` parameters exist but were not systematically tested across all sheets.
- **429 per card** — only the Owner settings 429 state was verified; other pages' 429 states were not tested.
- **Drawer on phone** — the `?drawer=open` parameter does not appear to render the drawer in the prototype; only the menu button is present.
- **Contrast ratios** — colour values were extracted but full WCAG contrast calculations were not performed for all badge and text combinations.
