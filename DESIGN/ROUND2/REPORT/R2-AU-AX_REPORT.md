# R2-AU-AX — Signing in and the account · Accessibility and resilience

HEAD: `a82541b1435366854d253f88cfe9258f87d36b8d` (origin/main: same)

One-line verdict: The auth and account flows are largely traceable by keyboard and screen reader, but the forced password-change landing and the account navigation miss the shared shell's skip link and some controls sit below the 44×44 touch target; weak-connection recovery is modeled everywhere except ordinary sign-in.

## Five most important points
1. `Change password.html` does not use `AuthShell` and has no `SkipLink`, so keyboard users land on the brand/sign-out row before the form on every forced change.
2. Heart, password-toggle, and pagination buttons are mostly icon-sized (`size="icon"`) and read smaller than 44×44px on a phone.
3. Sign-in has no network-failure/retry state, unlike Register and the recovery pages (`?state=network`).
4. The masked address/countdown lines are low-contrast helper text in context (muted) and need checking in dark mode.
5. Report list message truncation only renders its toggle after a runtime height check, so a no-JS/late-load reader sees no disclosure control.

## Issues

### R2-AU-AX-001 — Forced password-change page omits the shared skip link and shell
- type: defect · level: page · impact: high
- where: frame 18 · `Change password.html?auth=1` (390/768/1440, AR/EN) · screenshot [18-forced-password-change/...]
- evidence: `docs/design/screens/...` (use login page crops)
- what is wrong: It builds its own header with a 14px brand and sign-out control and no `SkipLink` (shared.jsx `SkipLink` is used by `AuthShell`, not here), and no page-level shell navigation.
- proposal: Render the forced page through `AuthShell` (or add `<SkipLink />` as the first focusable element and a `<main id="main">` already present), keep sign-out secondary.
- why: Keyboard/AT users reach the new-password form without tabbing through header controls.
- cost: S · rule: lens A.9, SH-018.

### R2-AU-AX-002 — Icon controls under the 44px touch target
- type: defect · level: component · impact: medium
- where: `Favorites.html`, `Reports.html` (hearts, remove, page actions), password toggles
- evidence: Auth/account captures.
- what is wrong: `HeartButton` uses `size="icon"`; the "Remove"/way-back `Button size="sm"` rows; pagination chips inherit small buttons. Each reads below 44×44 on 390.
- proposal: Use a 44×44 hit area (min-h-11 min-w-11 or icon button `size="lg"` equivalent) on phone for heart, remove, pager, password-toggle.
- why: Phone-first thumbs can reliably hit the control; fewer mis-taps.
- cost: S · rule: foundation §10, lens A.7.

### R2-AU-AX-003 — Sign-in has no network-failure/retry state
- type: improvement · level: page · impact: medium
- where: `Sign in.html` (all widths/modes)
- evidence: Register network frames vs. sign-in frames.
- what is wrong: Register exposes `?state=network` with `NetworkAlert`; Forgot/Reset expose `unreachable` + retry. Sign-in only models wrong password and rate limit; a dropped connection leaves no feedback/retry.
- proposal: Add `?state=network` to Sign in rendering `NetworkAlert` with «إعادة المحاولة» that re-runs submit; keep fields.
- why: A reader on a weak connection gets a recoverable next step instead of a spinner/blank.
- cost: M · rule: P7, lens A.8.

### R2-AU-AX-004 — Countdown and masked address are muted helper text
- type: defect · level: component · impact: medium
- where: `Forgot password.html?state=sent`, `Reset password.html?state=checkfailed`, `Settings.html?auth=google&state=linksent`, `Sign in.html?state=ratelimit`
- evidence: sent-countdown captures.
- what is wrong: `RateLimitAlert` is `variant="warning"` (good), but `LinkSent` address line and resend clock use `text-muted-foreground`, which drops contrast in dark mode and for low vision.
- proposal: Promote to `text-foreground` or a semantic `text-body` with a `Ltr` wrapper and check against foundation §10 (AA) in light/dark.
- why: Users who most need the address/clock can read it.
- cost: S · rule: foundation §10.

### R2-AU-AX-005 — Report disclosure only appears after layout measurement
- type: defect · level: component · impact: medium
- where: `Reports.html?auth=1` (rows with long text), all widths
- evidence: reports list frames.
- what is wrong: `ReportItem` measures `scrollHeight` in `useLayoutEffect` and only renders the show more/less button if `cut` is true; before measurement the message is silently clamped (`line-clamp-2`).
- proposal: Always render a focusable "Show more"/"Show less" toggle for any message longer than two lines, or remove clamping until measured with `aria-hidden` guarded.
- why: Screen readers and no-JS readers get a predictable control.
- cost: M · rule: lens A.9.

### R2-AU-AX-006 — Account navigation is not announced as tabs at phone width
- type: improvement · level: pattern · impact: low
- where: `Favorites.html`, `Reports.html`, `Settings.html` (account nav)
- evidence: account pages.
- what is wrong: The fragment bar uses `<nav aria-labelledby="account-nav-label">` with the label hidden below `lg`; at 390 the active item is still shown only visually.
- proposal: Keep the label in the a11y tree (visually hidden, not `hidden`) and mark items as `role="tab"` / `aria-selected`.
- why: A screen reader tells the user which account section is current.
- cost: S · rule: lens A.9.

### R2-AU-AX-007 — Favourites "remove" on unlisted spaces lacks undo order locality
- type: improvement · level: page · impact: low
- where: `Favorites.html?auth=1` (desktop 1440)
- evidence: favourites desktop frame.
- what is wrong: Unlisted cards offer "Remove" as a text button without the heart affordance; the toast undo is the only confirmation; focus is not returned anywhere.
- proposal: Move focus to the nearest surviving card after removal and keep `aria-live` toast.
- why: Users do not lose their place after an action.
- cost: M · rule: P8, P9.

## Decisions in doubt
None proposed.

## Not reviewed
- Contrast ratios were not measured with a tool; only design intent was checked. Legacy browser/zoom behavior and actual screen-reader audio were not verified. No automated tests run (read-only review).
- Code-level components (design system source) were not audited; only prototype frames.

## Browser pass (2026-10-17)
Server: http://127.0.0.1:5490 · masaha-design at 93f152f · tool: playwright MCP
### Existing issues
- R2-AU-AX-001 — changed: No skip link, no `<main>`, own header all confirmed; first Tab lands on «تسجيل الخروج» button (129×32). Brand is 17px not 14px as written. — r2-shots/AU-AX/R2-AU-AX-001.png
- R2-AU-AX-002 — confirmed: Hearts 40×40, remove 47×32, password toggle 32×32, dark-mode toggle 40×40 — all under 44×44. — r2-shots/AU-AX/R2-AU-AX-002.png
- R2-AU-AX-003 — confirmed: `Sign in.html?state=network` renders the normal sign-in page with no NetworkAlert or retry control. — r2-shots/AU-AX/R2-AU-AX-003.png
- R2-AU-AX-004 — refuted: Muted text measured at 5.74:1 (light, on rgb(244,252,254)) and 7.62:1 (dark, on rgb(12,19,21)) — both pass AA 4.5:1. The claim that contrast drops in dark mode is not supported. — r2-shots/AU-AX/R2-AU-AX-004.png
- R2-AU-AX-005 — confirmed: 5 `line-clamp-2` message elements with 0 disclosure toggle buttons rendered. — r2-shots/AU-AX/R2-AU-AX-005.png
- R2-AU-AX-006 — confirmed: Account nav `aria-labelledby="account-nav-label"` exists but label is `display:none`; items are plain `<a>` with no `role="tab"` or `aria-selected`. — r2-shots/AU-AX/R2-AU-AX-006.png
- R2-AU-AX-007 — confirmed: «إزالة» button on unlisted Palm Hub card at 1440, 47×32, no focus-return mechanism visible. — r2-shots/AU-AX/R2-AU-AX-007.png
### Checked now
- Keyboard Tab order on `Change password.html?auth=1` (390): first focusable is header sign-out button, then password field, toggle, submit — confirms skip-link gap.
- Contrast measured via `getComputedStyle`: Forgot-password masked address `rgb(92,101,103)` on `rgb(244,252,254)` = 5.74:1 light; `rgb(157,167,169)` on `rgb(12,19,21)` = 7.62:1 dark. Both pass AA.
- `Favorites.html?photos=loading` (390): skeleton placeholders (`bg-muted motion-safe:animate-pulse`) shown — proper loading state.
- `Favorites.html?photos=failed` (390): SVG space marks shown in place of images — proper failed state.
- 768px width on Sign in, Favorites, Reports: no horizontal overflow (scrollWidth = clientWidth = 768).
- `Forgot password.html?state=loading` (390): spinner shown — proper loading state.
- English/LTR on `Sign in.html?lang=en`: `dir="ltr"` set, password toggle has `aria-label="Show password"`, Google button 316×40.
- Heart buttons on Favorites: all have descriptive Arabic `aria-label` (e.g. «إزالة فوكس هاب من المفضّلة»).
### New issues
None.
### Still not checked
- Legacy browser behavior and actual screen-reader audio: no browser/screen-reader automation available.
- Code-level component audit: prototype frames only, as before.
