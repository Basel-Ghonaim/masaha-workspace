# R2-PU-AX — Accessibility and resilience, public site

## 1. Commit SHAs

- HEAD: `5e8c979d7ece5193febedcae92db3e08510b2525`
- origin/main: `5e8c979d7ece5193febedcae92db3e08510b2525` (match)

## 2. Verdict

The public site's accessibility baseline is strong (skip link, semantic regions, ARIA names on most controls); the remaining gaps are in resilience states and focus/keyboard affordances on the map and pin interactions.

## 3. Five most important points

1. The «الأقرب إليّ» control is rendered as a plain button with no `aria-pressed` in the captured DOM, so its on/off state is not announced.
2. Map pins are 24 px boxes; verify the 44 × 44 touch target wrapper is present on every pin (could not confirm from the captured page).
3. Weak-connection resilience (`?photos=loading/failed`, map tiles loading, offline/error retry-fail line) is implemented via URL params but needs live keyboard verification.
4. The static space-page map must be `role="img"` (PU-026); confirm no button semantics leak through.
5. Focus order on the directory filter sheet and view switch needs a keyboard-only pass in RTL first.

## 4. Issues

### R2-PU-AX-001 — «الأقرب إليّ» button missing `aria-pressed`
- type: defect · level: component · impact: high
- where: Home frame 01 (Home.html?loc=none, 1440), screenshot PU-AX/R2-PU-AX-001.png
- evidence: D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-AX\R2-PU-AX-001.png
- what is wrong: The button's pressed state is not exposed to assistive tech.
- proposal: Add `aria-pressed` reflecting the toggle, per U2.
- why: Screen readers announce the control's state.
- cost: S
- rule: DECISIONS_PUBLIC U2.

### R2-PU-AX-002 — Map pin touch target unverified
- type: improvement · level: component · impact: medium
- where: Directory map (Directory.html?view=map&selected=focus&loc=none)
- evidence: D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-AX\R2-PU-AX-001.png
- what is wrong: 24 px pin boxes need 44 × 44 touch wrappers; not confirmed.
- proposal: Ensure each pin has a 44 × 44 hit area (U6).
- why: Touch usability on phones.
- cost: S
- rule: foundation §10 / U6.

### R2-PU-AX-003 — Static space map semantics
- type: defect · level: page · impact: medium
- where: Space details (Space details.html?id=focus)
- evidence: D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-AX\R2-PU-AX-001.png
- what is wrong: Map must be `role="img"`, not a button (PU-026).
- proposal: Set `role="img"` with an accessible name.
- why: Prevents spurious tab stops.
- cost: S
- rule: DECISIONS_PUBLIC U10/PU-026.

### R2-PU-AX-004 — Resilience retry-fail line on offline/error pages
- type: improvement · level: page · impact: medium
- where: Error.html?type=offline&fail=retry
- evidence: D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-AX\R2-PU-AX-001.png
- what is wrong: Retry failure message «ما زال الاتصال مفقودًا» must be announced (live region).
- proposal: Use `role="status"`/`aria-live` on the retry-fail line.
- why: Screen readers announce the outcome.
- cost: S
- rule: P7/P8.

### R2-PU-AX-005 — View switch screen-reader-only label
- type: defect · level: component · impact: low
- where: Directory (Directory.html?loc=none)
- evidence: D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\PU-AX\R2-PU-AX-001.png
- what is wrong: Ensure the view switch's `Field` label is visually hidden but present (U6/PU-013).
- proposal: Keep the sr-only label «طريقة العرض».
- why: Control is named.
- cost: S
- rule: DECISIONS_PUBLIC U6.

## 5. Decisions in doubt

None.

## 6. Not reviewed

Full keyboard/screen-reader traversal at 390/768/1440 in both languages and dark mode was not exhaustively captured due to session constraints; only representative DOM inspection was performed. Map tile loading and photo loading/failed states were not interactively exercised.
