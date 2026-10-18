# R2-AU-EX report — excess and simplification (AU)

HEAD SHA = origin/main = a82541b1435366854d253f88cfe9258f87d36b8d

Verdict: the account pages are mostly lean; the remaining excess is duplicated caption/badge text and over-loaded personal lists, plus a few redundant exit controls.

Five most important points:
1. Settings' “Signing in” card repeats the method in caption and again in tone/badge.
2. Favourites carries the full location machinery on a list of a few saved spaces.
3. My reports' filter toggle and card-by-card status tags both encode status.
4. Sign-in and register each expose two ways back (AuthWayBack plus the peer link).
5. Forgot-password's sent step keeps resend, masked address and change-address as three separate lines.

## Issues

### R2-AU-EX-001 — Signing-in card repeats the method in caption and badge
type: improvement; level: component; impact: medium.
where: "Settings · email account — phone 390", `Settings.html?auth=1`, screenshot `docs/design/screens/17-settings/02-settings-email-account-phone-390.webp`.
evidence: `C:\Users\basel\Downloads\r2-shots\AU-EX\R2-AU-EX-001.png`
what: MethodRow shows "Google" then a caption "You sign in with Google" and a "Linked" badge for the same fact.
proposal: keep the badge only when it adds state (linked/unlinked); drop the caption, or drop the badge for the active method.
why: one fact, one place; less reading on a phone.
cost: S.
rule: REVIEW_LENS §3 B.1.

### R2-AU-EX-002 — Favourites carries the full location machinery on a short personal list
type: improvement; level: page; impact: medium.
where: "Favourites · saved spaces + one hidden — phone 390", `Favorites.html?auth=1&loc=none`, screenshot `docs/design/screens/15-favourites/02-favourites-saved-spaces-one-hidden-phone-390.webp`.
evidence: `C:\Users\basel\Downloads\r2-shots\AU-EX\R2-AU-EX-002.png`
what: NearMeButton plus LocationStatus (map pick, choose area) below the list header, for a list answered whole and optionally sorted.
proposal: a single «الأقرب إليّ» toggle (NearMeButton) that enables/disables location; remove the status block and its sub-actions, letting the permission prompt do the work.
why: fewer controls; the saved list is already short and complete.
cost: M.
rule: REVIEW_LENS §3 B.5; DECISIONS_ACCOUNT AC-014 (kept, sorting only).

### R2-AU-EX-003 — My reports repeats status in filters and per-card badges
type: improvement; level: pattern; impact: low.
where: "Reports · list — phone 390", `Reports.html?auth=1`, screenshot `docs/design/screens/16-my-reports/02-reports-list-phone-390.webp`.
evidence: `C:\Users\basel\Downloads\r2-shots\AU-EX\R2-AU-EX-003.png`
what: an All/Open/Reviewed toggle sits above cards that each carry a coloured status badge; status is stated twice.
proposal: keep the badge only; turn the toggle into a one-word summary line ("3 in review") or drop filtering on the account view.
why: less reading, single source of status.
cost: S.
rule: REVIEW_LENS §3 B.1.

### R2-AU-EX-004 — Unlisted spaces are a second, differently shaped block
type: improvement; level: page; impact: low.
where: "Favourites · saved spaces + one hidden — phone 390", `Favorites.html?auth=1&loc=none`, screenshot `docs/design/screens/15-favourites/02-...`.
evidence: `C:\Users\basel\Downloads\r2-shots\AU-EX\R2-AU-EX-004.png`
what: spaces that left the directory render in a separate muted card list with a Remove button, while saved (listed) spaces use SpaceCard; two cards for one concept.
proposal: one card component for both, with the unlisted state as a badge + disabled heart (DECISIONS_ACCOUNT C7 keeps Removal + undo).
why: one pattern for a favourite.
cost: M.
rule: REVIEW_LENS §3 B.4.

### R2-AU-EX-005 — Auth cards carry two exit controls
type: improvement; level: pattern; impact: low.
where: "Sign in · default — phone 390", `Sign in.html`, screenshot `docs/design/screens/06-sign-in/02-sign-in-default-phone-390.webp`.
evidence: `C:\Users\basel\Downloads\r2-shots\AU-EX\R2-AU-EX-005.png`
what: AuthWayBack sits beside the peer link (register/sign-in) in the footer of sign-in and register.
proposal: one exit control per card — the peer link; let the shell's back handle the rest.
why: fewer choices at the bottom of the form.
cost: S.
rule: DECISIONS_ACCOUNT C4 (way out) — in doubt, see below.

### R2-AU-EX-006 — Register footer stacks three separate sign-offs
type: improvement; level: page; impact: low.
where: "Register · default — phone 390", `Register.html`, screenshot `docs/design/screens/07-register/02-register-default-phone-390.webp`.
evidence: `C:\Users\basel\Downloads\r2-shots\AU-EX\R2-AU-EX-006.png`
what: peer link, AuthWayBack and an owner-management contact line are stacked under the button.
proposal: fold the owner contact line into the body helper or a single "manage a space?" link; keep one back link.
why: shorter footer; primary action stays obvious.
cost: S.
rule: REVIEW_LENS §3 B.2.

### R2-AU-EX-007 — Forgot-password sent step has three separate controls
type: improvement; level: component; impact: medium.
where: "Forgot · sent (60s countdown) — phone 390", `Forgot password.html?state=sent`, screenshot `docs/design/screens/08-forgot-reset-password/04-forgot-sent-60s-countdown-phone-390.webp`.
evidence: `C:\Users\basel\Downloads\r2-shots\AU-EX\R2-AU-EX-007.png`
what: message, masked address, resend button and "use another email" appear as four separate blocks, even after resend.
proposal: keep resend as the primary button with the masked address inside its label ("Resend to s•••@example.com") and "use another email" beneath only.
why: one primary action; less vertical space on a phone.
cost: S.
rule: REVIEW_LENS §3 B.1, B.5; DECISIONS_ACCOUNT C3 — in doubt, see below.

## Decisions in doubt
- AuthWayBack as a separate control (C4) — two exits per auth card seems like excess; propose collapsing to the peer link.
- Resend + change-address split (C3) — could live on one line; settled C3 keeps them separate.
- «الأقرب إليّ» on a whole-answered favourites list (AC-014) — location machinery may be excess for a small saved list.

## Not reviewed
- Auth and account flows were not exercised in English/dark at all widths (states only spot-checked); the clone's case labels were trusted from INDEX.md.
- No UI interaction exercised beyond query-state frames (toasts, dialogs) due to read-only review.
