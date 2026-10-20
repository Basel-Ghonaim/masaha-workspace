# PU-DF · S1 · B01–B08
Images viewed: yes — the top header shows «مساحة», «English», and the hamburger menu.

## Findings

### S1-01 — Account-link toast obscures the Home result card on phone
- frame: B08-390-en-light   (also: B08-390-ar-light, B08-390-ar-dark)
- type: defect · level: component · impact: medium
- where: Home, linked-account success toast, `Home.html?loc=none&toast=linked`, 390px, light/dark
- fact: The green toast «We linked your Google account to your account» is rendered across the Focus Hub card and covers its card content, including the status/details area; the Arabic frame likewise places «ربطنا حساب Google بحسابك» over the card.
- proposal: Place the public-site `Toaster` in a dedicated non-content region below the phone header (or reserve a toast-safe inset in the page shell) at phone widths, keeping it clear of result cards and other interactive content while retaining the existing success styling and dismiss button.
- why: The success confirmation remains readable without hiding the result the user came to browse or making the card's state temporarily unverifiable.
- cost: S · rule: `DECISIONS_SHARED.md` P8

## Decisions in doubt
- None.

## Not judged
- None within B01–B08.
