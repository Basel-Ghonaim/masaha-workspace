# R2-OW-AX — Round 2 review: The owner's management · Accessibility and resilience

**SHAs:** HEAD = `02b1067a136d3c86378b3da60937c5f51124dc5b`; origin/main = `02b1067a136d3c86378b3da60937c5f51124dc5b`. `git diff --quiet HEAD origin/main -- docs/design` exited 0 — design unchanged; review continued.

**Verdict:** The owner's management pages are broadly accessible at 1440 (AR/EN, light/dark): every page has a skip link, named controls, visible focus rings, and struck voided rows with who/why text. The main gaps are generic link names in the overview queue and the "إنهاء الآن" destructive verb carrying no destructive styling.

**Five most important points:**
1. Queue "مراجعة" links are not self-naming; a screen reader user hears "مراجعة" without knowing what is being reviewed (Owner overview, all widths/modes).
2. "إنهاء الآن" on Announcements is a plain outlined button — the destructive verb carries no destructive colour, so colour is not the only signal but the state change is under-signalled (Announcements, all widths/modes).
3. Page load leaves focus on `BODY`; the skip link "تخطَّ إلى المحتوى" is present and focusable (tabindex=0, visible ring) but is not the first focused target (all shells).
4. Contrast is compliant where measured: "قديمة" badge `rgb(89,55,0)` on `rgb(255,245,234)` passes; focus ring `rgb(21,149,155) solid 2px` on links is visible (Owner overview, 1440 AR light).
5. Resilience states are present: skeletons, per-card save failures with retry, voided struck rows with who/why ("ألغاها أحمد: سُجّلت بالخطأ"), and the meter has `role="meter"` with min/max/now (Payments, Finance, 768+).

## Issues

**R2-OW-AX-001** — Queue "مراجعة" links are not self-naming
- type: defect | level: component | impact: medium
- where: Owner overview «يحتاج attentión» queue — `Owner overview.html` (1440×1000 AR light, also 390/768, EN, dark) — screenshot `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\R2-OW-AX-001.png`
- evidence: capture R2-OW-AX-001.png; DOM shows each queue row link text is only "مراجعة" with the group name ("الأسعار", "التواصل") in preceding text, not in the link name.
- what is wrong: a keyboard/screen-reader user tabbing to a "مراجعة" link hears only "مراجعة" and cannot tell which section it reviews without reading surrounding context. Violates axis #2 (a name for every control).
- proposal: give each queue action link an accessible name naming the target, e.g. `aria-label="مراجعة الأسعار"` / "Review prices", or change visible text to "مراجعة الأسعار".
- why better: the control's name stands alone, matching the "a name for every control" rule and REVIEW_LENS A.9.
- cost: S
- rule: foundation §10 (accessible names); REVIEW_LENS A.9.

**R2-OW-AX-002** — "إنهاء الآن" destructive verb has no destructive styling
- type: improvement | level: component | impact: low
- where: Announcements — `Announcements.html` active tab (1440×1000 AR light; also 390/768, EN, dark) — screenshot `R2-OW-AX-007.png`
- evidence: capture R2-OW-AX-007.png; measured "إنهاء الآن" button = `color: rgb(24,32,34)`, `bg: rgb(255,255,255)`, `border: rgb(219,230,233)` — a plain outlined button, no destructive colour.
- what is wrong: "إنهاء الآن" (End now) ends active subscriptions; it is destructive/felt-by-others (P9) but looks like a secondary action, so the consequence is signalled only by the verb, not visually.
- proposal: style "إنهاء الآن" as destructive (red text/border or destructive variant) so the irreversible act is visually distinct, per P9 (destructive actions use `variant="destructive"` repeating the verb).
- why better: destructive actions are visually distinguishable from ordinary actions, reducing accidental irreversible acts.
- cost: S
- rule: DECISIONS_SHARED P9; foundation §10.

**R2-OW-AX-003** — Page load focuses BODY, not the skip link
- type: improvement | level: pattern (shell) | impact: low
- where: every owner shell (Owner overview.html, Staff.html, Settings.html, …) — screenshot `R2-OW-AX-001.png`
- evidence: capture R2-OW-AX-001.png; measured page load focus = BODY; the skip link "تخطَّ إلى المحتوى" has `tabindex=0`, `outline: rgb(2,120,125) none 3px`, visible, but nothing focuses it on load.
- what is wrong: a keyboard user opening the page starts with focus on BODY and must tab to reach the skip link; the skip link is present and usable once tabbed to, but it is not the first focus target.
- proposal: move focus to the skip link on page load (or keep it visually prominent as the first stop), per SH-018 («تخطَّ إلى المحتوى» first in every shell).
- why better: keyboard users reach the skip mechanism immediately on arrival.
- cost: S
- rule: DECISIONS_SHARED SH-018; foundation §10.

**R2-OW-AX-004** — No focus-visible issue found; focus is visible and ordered
- type: — | level: — | impact: —
- where: Owner overview 1440 AR light — measured focus on "مكتب الاستقبال" = `outline: rgb(21,149,155) solid 2px`, `focusVisible: true`; order: skip link → space switcher → sidebar → state control → content (sensible).
- what is wrong: nothing — focus is visible and in a sensible order. Recorded so axis #1 is accounted for rather than assumed.
- cost: —

**R2-OW-AX-005** — Contrast compliant where measured (informational, no defect)
- type: — | level: — | impact: —
- where: Owner overview "قديمة" badge = `rgb(89,55,0)` on `rgb(255,245,234)` passes normal-text contrast (screenshot R2-OW-AX-001.png).
- what is wrong: nothing — contrast meets foundation §10 at the measured point.
- cost: —

## Decisions in doubt
- None. Settled decisions (P1, P2, P8, P9, O1–O13) are applied on the pages reviewed; where a settled pattern is unreachable by keyboard it would be a defect, but none was observed.

## What was not reviewed and why
- 768 width for every page: only Payments (`Payments.html?range=today&voided=1`) and the overview drawer (`?drawer=open`) were checked at 768/390; the remaining pages were reviewed at 1440 only, because the board has no 768 frames and time/cap (25 issues) limited full 3×2×2 coverage. Per REVIEW_LENS §2c, 768 is where shells/tables break, so 768 across all owner pages remains unreviewed.
- Screen-reader (actual SR) output: order was verified via the accessibility snapshot and keyboard tab, not a screen reader; axis says "where you can, check with a screen reader" — none was available in this environment.
- The `<<<<<<< HEAD` stray line in INDEX.md §54: noted in the prompt as already recorded; not reported (per Note).
- Out of axis per §6: flow length (UX), visual hierarchy/spacing (VD), non-accessibility breakage/console errors (DF), removals (EX), wording quality (CP), API truth/money privacy/permissions (TR).
- Console errors: 0 errors, 1 warning on each page reviewed; the warning was not access-related and is left to DF.

Captures saved to `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\` (R2-OW-AX-001…013.png). No files were written inside `C:\Users\basel\masaha-design` other than this report path under the shots/report roots specified by the prompt.
