# R2-AU-DF_REPORT — Round 2 review: Signing in and the account · Design defects

## 1. Commit SHAs

- `git rev-parse HEAD`: `02b1067a136d3c86378b3da60937c5f51124dc5b`
- `git rev-parse origin/main`: `02b1067a136d3c86378b3da60937c5f51124dc5b`
- HEAD equals origin/main. Reviewed from `C:\Users\basel\masaha-design`, detached at `origin/main`. No edits were made.

## 2. Verdict

The account/sign-in screens are largely consistent across widths, languages and themes: every matrix state exists and renders, 429 states correctly disable submit, RTL/LTR values are isolated (`dir="ltr"`/`<Ltr>`/`dir="auto"`), dark mode resolves through the design system's semantic tokens, and there are no console errors or blank frames. The principal defect is a state that reports a failure but offers no recovery action.

## 3. Five most important points

1. `Reset password ?state=checkfailed` shows the 429 countdown and "Open the link in your email again" but provides no button or link to act on — the only escape is the footer "Back to sign in".
2. Every 429/ratelimit state (sign in, register, forgot, settings) correctly disables its submit and shows a counting-down `RateLimitAlert`.
3. All masked emails, phone-like strings, times and Latin names are LTR-isolated; no RTL/LTR direction defect was found on the account pages.
4. Light and dark render correctly through semantic tokens on every account page; no lost borders or unreadable text in dark mode.
5. No console errors and no blank frames on any page/parameter combination tested.

## 4. Issues

### R2-AU-DF-001 — Reset password "checkfailed" state has no recovery action

- **type:** defect
- **level:** page
- **impact:** medium
- **where:** INDEX §08 · `Reset password.html?state=checkfailed` · widths 390/768/1440 · AR and EN · light and dark · screenshot `docs/design/screens/08-forgot-reset-password/09-reset-link-expired-or-used-desktop-1440.webp` (frame label: Reset · link expired or used)
- **evidence:** `D:\masahaWorkspace\DESIGN\ROUND2\shots\r2-shots\AU-DF\R2-AU-DF-005.png` (390×844, AR, light)
- **What is wrong:** `?state=checkfailed` (the reset-link check refused with a 429) renders the ratelimit countdown ("محاولات كثيرة، حاول بعد 0:42") and the line "افتح الرابط من بريدك الإلكتروني مرة أخرى." ("Open the link in your email again."), but supplies no actionable control — no "Request a new link" button and no retry. The only way off the page is the footer "Back to sign in". By contrast, the sibling `?state=invalid` state offers a clear "اطلب رابطًا جديدًا" ("Request a new link") button.
- **Proposal:** Add a primary action to the checkfailed card, e.g. "اطلب رابطًا جديدًا" ("Request a new link") leading to `Forgot password.html`, so the user can recover without leaving for sign-in first. Keep the "Back to sign in" footer as the secondary exit.
- **Why it is better:** A failure state should say what happened *and* what to do next (foundation §10 / P8: every failure says what to do). As it stands, a user who hits a 429 on the link check is told to open a link they cannot open from this page, with no supported next step.
- **cost:** S
- **rule:** foundation §10 (every failure says what to do); P8 (every action says it worked or failed). Applies to `Reset password.html` (§08).

---

## 5. Decisions in doubt

None. No settled decision (DECISIONS_ACCOUNT.md C1–C8, DECISIONS_SHARED.md) was found to make the design worse; where settled patterns are applied they hold.

## 6. What was not reviewed and why

- **`Reset email.html`** was opened but not theme-tested as a web page: it is an HTML email template with hardcoded light inline styles and `color-scheme: light`; it is not a themeable screen, so `?theme=dark` does not (and need not) alter it. It remains readable in light.
- **`Sign in - board.html`** is a design-board composite of iframes, not a reviewable page.
- **Width 768** was inspected on Settings, Sign in, Register, Forgot, Reset, Favorites and Reports; no shell/table breakage was found at 768 (the account pages have no multi-column table).
- **States not reproduced as screenshots:** all matrix combinations were loaded and confirmed to render (no blank frame), but screenshots were captured only for the confirmed defect and a few reference frames, per the 25-issue cap and one-issue-per-problem rule.
- **Flow length, feedback wording, focus order, contrast ratios and permissions** are out of the DF axis (UX/VD/AX/TR) per §6–7 and were not judged.
