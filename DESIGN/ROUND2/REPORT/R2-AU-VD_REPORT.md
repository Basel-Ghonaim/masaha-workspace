# R2-AU-VD report — Signing in and the account · Visual design and consistency

- `git rev-parse HEAD` = `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- `git rev-parse origin/main` = `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- The two SHAs are equal; the review ran on `origin/main`.
- Local server: `http://127.0.0.1:5402/` serving `docs/design/prototype` (stopped at the end; port verified free).

## Verdict

The account holds its settled shapes (auth card, vertical account nav, sent step, `max-w-3xl` settings vs full-width lists), but the same jobs drift apart in the details: headers, success blocks, footer stacks, field-level links, list gaps, empty icons and the resend button each come in two versions.

## Five most important points

1. The forced-change page uses a different header than every other auth page (no language/theme controls).
2. A finished reset (icon + title + action) looks weightier than a sent link (quiet text block) for the same kind of moment.
3. The two twin auth pages align their under-field escape links to opposite edges.
4. Auth footers stack the same three lines in different orders with different gaps.
5. Empty favourites get a domain icon while empty reports get an alert glyph.

## Issues

### R2-AU-VD-001 — Forced-change header breaks the auth-shell header pattern

- **type:** improvement · **level:** pattern · **impact:** medium
- **where:** §18 “Forced change · empty — phone 390”, `http://127.0.0.1:5402/Change%20password.html`, 390, AR light; archive shot `screens/18-forced-password-change/02-forced-change-empty-phone-390.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-VD\R2-AU-VD-001.png` (full frame)
- **what is wrong:** every auth page renders the `AuthShell` bar (wordmark link, language toggle, theme toggle, skip link); `Change password.html` renders its own bar (wordmark span, sign-out only). A user who must pass this page cannot switch language or theme, and the bar reads as a different product.
- **proposal:** reuse the `AuthShell` header on the forced-change page, keeping it chromeless (no navigation, sign-out stays as the only way out). Changes one page.
- **why:** one shell for signing in everywhere; the people most likely to need the language toggle (new staff with a temporary password) meet it here.
- **cost:** S
- **rule:** applies REVIEW_LENS.md §3 B.4 (same job, same way) and DECISIONS_ACCOUNT.md C5 (chromeless of navigation; toggles are not navigation).

### R2-AU-VD-002 — Sent and success blocks speak two visual languages

- **type:** improvement · **level:** pattern · **impact:** medium
- **where:** §08 “Reset · success — desktop 1440”, `http://127.0.0.1:5402/Reset%20password.html?state=success`, 1440, AR light; archive shot `screens/08-forgot-reset-password/11-reset-success-desktop-1440.webp`. Counterpart: §08 “Forgot · sent (60s countdown) — phone 390”, `http://127.0.0.1:5402/Forgot%20password.html?state=sent`.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-VD\R2-AU-VD-002.png` (full frame)
- **what is wrong:** the reset success leads with a success icon, a title and a primary action; the forgot sent step (`LinkSent`, also reused in Settings) is body text with no icon and an outline resend. Both confirm “check your email / you are done” moments, but one looks finished and the other looks interim.
- **proposal:** one sent/success block for the auth cards: success icon, title, body, masked address line, then the action (primary where there is a next step, outline resend where there is a clock) and the secondary link. Changes `Forgot password.html`, `Reset password.html`, `Settings.html`.
- **why:** equal moments carry equal visual weight, so users trust the sent step as done and see the next action first.
- **cost:** M
- **rule:** applies REVIEW_LENS.md §3 B.4.

### R2-AU-VD-003 — Under-field escape links align to opposite edges on the twin pages

- **type:** defect · **level:** pattern · **impact:** low
- **where:** §07 “Register · email already registered — desktop 1440”, `http://127.0.0.1:5402/Register.html?state=exists`, 1440, AR light; archive shot `screens/07-register/07-register-email-already-registered-desktop-1440.webp`. Counterpart: §06 “Sign in · default”, `http://127.0.0.1:5402/Sign%20in.html` (“نسيت كلمة المرور؟”).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-VD\R2-AU-VD-003.png` (full frame)
- **what is wrong:** the taken-account link hugs the inline-start edge (verified: computed `align-self: flex-start`, right edge flush with the error text above it); the forgot-password link on the twin card hugs the inline-end edge. The same job — an escape hatch under a field — produces opposite ragged edges on two cards that otherwise share everything.
- **proposal:** align both escape links to the inline-end edge (the label keeps the start edge, as on the `MethodRow` label/action geometry), on `Sign in.html` and `Register.html`.
- **why:** one edge for secondary field actions keeps the reading edge clean and the two cards visibly twins.
- **cost:** S
- **rule:** applies REVIEW_LENS.md §3 A.1 and B.4.

### R2-AU-VD-004 — Auth footers stack the same lines in different orders and gaps

- **type:** improvement · **level:** pattern · **impact:** low
- **where:** §07 “Register · default — phone 390”, `http://127.0.0.1:5402/Register.html`, 390, AR light; archive shot `screens/07-register/02-register-default-phone-390.webp`. Counterparts: §06 sign-in footer, §08 forgot footer (`http://127.0.0.1:5402/Forgot%20password.html`).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-VD\R2-AU-VD-004.png` (full frame)
- **what is wrong:** all four auth cards end in a switch line, an optional tertiary caption and the way back, but Register orders them switch → way back → owner caption with a `gap-3` stack, while Forgot orders them contact caption → back with `gap-2` and Sign in has switch → way back with `gap-2`. The way back reads as the footer’s close everywhere except on Register.
- **proposal:** one footer order on all four cards — switch line, tertiary caption (when the page has one), way back last — with `gap-2` throughout. Changes `Sign in.html`, `Register.html`, `Forgot password.html`, `Reset password.html`.
- **why:** a fixed close position lets returning users find the way back without reading the card.
- **cost:** S
- **rule:** applies REVIEW_LENS.md §3 A.2 and B.4.

### R2-AU-VD-005 — Favourites mixes two row gaps inside one list

- **type:** improvement · **level:** page · **impact:** low
- **where:** §15 “Favourites · saved spaces + one hidden — desktop 1440”, `http://127.0.0.1:5402/Favorites.html?auth=1&loc=none`, 1440, AR light; archive shot `screens/15-favourites/01-favourites-saved-spaces-one-hidden-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-VD\R2-AU-VD-005.png` (full frame)
- **what is wrong:** listed space cards sit in a `gap-4` grid while the unlisted-space rows below them stack with `gap-3`, inside a `gap-3` section (Reports’ equivalent section uses `gap-4`). Same list, two rhythms; the unlisted row sits visibly tighter than the card grid.
- **proposal:** `gap-4` for the card grid, the unlisted list and the section stacks on Favourites (and keep Reports’ `gap-4`), so every list row breathes the same.
- **why:** equal gaps between twin rows; the unlisted row already differs by treatment (muted card), it should not also differ by spacing.
- **cost:** S
- **rule:** applies foundation §5 (spacing scale) and REVIEW_LENS.md §3 A.2.

### R2-AU-VD-006 — Empty reports borrow the error icon

- **type:** improvement · **level:** pattern · **impact:** medium
- **where:** §16 “Reports · empty — desktop 1440”, `http://127.0.0.1:5402/Reports.html?auth=1&state=empty`, 1440, AR light; archive shot `screens/16-my-reports/03-reports-empty-desktop-1440.webp`. Counterpart: §15 “Favourites · empty” (heart icon).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-VD\R2-AU-VD-006.png` (full frame)
- **what is wrong:** the empty-reports `EmptyState` uses `CircleAlertIcon` — the glyph of load errors and offline states — for a neutral “nothing here yet”, while empty favourites use a domain heart. An alert glyph on an empty list can read as a failure and invite pointless retries.
- **proposal:** give the empty-reports state a neutral/domain icon from the layer’s closed glyph set (file/report inbox analogue), matching favourites’ domain-icon treatment. If the closed set has no such glyph, say so — that is the new-component case. Changes `Reports.html`.
- **why:** empty is not broken; the icon should say “nothing yet”, not “something failed”.
- **cost:** S
- **rule:** applies foundation §5 (status roles) and REVIEW_LENS.md §3 A.4/B.4.

### R2-AU-VD-007 — Settings is the only account header without a description

- **type:** improvement · **level:** page · **impact:** low
- **where:** §17 “Settings · email account — desktop 1440”, `http://127.0.0.1:5402/Settings.html?auth=1`, 1440, AR light; archive shot `screens/17-settings/01-settings-email-account-desktop-1440.webp`. Counterparts: §15 favourites and §16 reports headers (h1 plus muted description).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-VD\R2-AU-VD-007.png` (full frame)
- **what is wrong:** Favourites and My reports pair the h1 with a `body-sm` muted description; Settings renders the h1 alone above three cards. The odd one out looks unfinished next to its siblings in the same nav.
- **proposal:** add one `body-sm` muted line under the Settings h1 naming what lives here (name, sign-in ways, language, theme). Alternatively drop the descriptions from the two lists; adding is preferred.
- **why:** sibling pages in one nav share one header shape; the line also previews the three cards for first-time openers.
- **cost:** S
- **rule:** applies REVIEW_LENS.md §3 A.3; DECISIONS_ACCOUNT.md C6 settles the name, not the description.

### R2-AU-VD-008 — The resend action carries less weight inside Settings

- **type:** improvement · **level:** pattern · **impact:** low
- **where:** §54 “Account settings · Google-only, the link sent — phone 390”, `http://127.0.0.1:5402/Settings.html?auth=google&state=linksent`, 390, AR light (no archive shot yet). Counterpart: §08 sent step with the full-width resend.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\AU-VD\R2-AU-VD-008.png` (full frame)
- **what is wrong:** the same `LinkSent` resend renders full-width on the forgot card but auto-width, start-aligned, inside the Settings sign-in card — a small button in a full-width card, on the phone width where thumb reach matters most.
- **proposal:** render the resend full-width in Settings too (`fullWidth` on), keeping the in-card placement. Changes `Settings.html`.
- **why:** one action, one weight; the resend is the primary action of the sent state at every width.
- **cost:** S
- **rule:** applies REVIEW_LENS.md §3 B.4.

## Decisions in doubt

None. The settled patterns (one account menu and its phone avatar, the auth card shape with its way back, the sent step, the vertical account nav, settings `max-w-3xl` vs full-width lists) all hold on the pages reviewed; the issues above are about how pages apply them, not the decisions themselves.

## What was not reviewed and why

- **Out-of-axis behaviour (left to the sibling AU prompts):** flow length, dead ends and feedback behaviour (UX); overflow, breakage, mirroring, console errors (DF); element removals (EX); wording and translation (CP); focus order, names, contrast ratios, touch targets, screen-reader order (AX); API/model/v1 truth and permissions (TR). One concrete handoff: the `ToggleGroup` check glyph renders at the inline-end side in RTL on chips (Reports filters, Settings preferences) — whether that mirrors correctly belongs to DF, so it is not reported here.
- **The recorded `<<<<<<< HEAD` line before INDEX.md §54** is a known merge leftover per this prompt’s note; not reported.
- **Widths/modes matrix:** every issue was verified by rendering the real prototype at true device widths via CDP (390/768/1440, plus dark and `?lang=en` spot checks: Sign in dark, Register filled EN, Settings at 768 — all clean, no defect filed). Auth cards share one centred `max-w-md` shell from `md` up, so 768 adds no new geometry beyond what 390 and 1440 prove; account-list behaviour at 768 follows the same horizontal-tabs shell verified on Settings.
- **Key states covered by render:** sign-in default/error/ratelimit/Google `error`+`notallowed`+`linked` paths (code-shared `GoogleBlock`, identical by construction), register default/typing/filled/errors/exists/toolong/ratelimit/network/loading, forgot request/sent/spent/linkopen/ratelimit, reset form/typing/success/invalid/checkfailed, settings email/Google-only/linked/pw-open/wrongpw/ratelimit/linksent, favourites ready/empty/loading/unlisted, reports ready/empty/error/tabs/`demo=pages` (pager footer verified with 7 rows; the 28-row second page was code-reviewed, not rendered), forced change empty/typing and `role=` landings (identical card, code-verified), `?auth=0` redirects (route behaviour, TR/UX), `Reset email.html` (static mail, rendered clean).
- **Evidence format:** captures are full-frame PNGs, not crops — no image tooling exists in this environment (no PIL, no installs per the read-only rule), so programmatic cropping was unavailable. Each file is named per issue (`R2-AU-VD-00N.png`).
