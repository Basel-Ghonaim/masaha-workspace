# R2-AU-CP — report

**HEAD / origin/main:** `a82541b1435366854d253f88cfe9258f87d36b8d` (match)

## Verdict

The auth and account copy is largely settled and internally consistent; the remaining defects are wording/grammaticality and mirror mismatches, not vocabulary violations.

## Top 5 points

1. Settings uses “تسجيل الدخول” (Sign in) as a card title for the account’s sign-in methods.
2. The Google-only “set a password” line’s English word order reads as a mistranslation.
3. Reports uses two distinct empty-state strings that differ only by filter state — acceptable, but they should be named consistently.
4. Relative dates in Arabic and English match in meaning but mixed form (“a month ago” vs “before 3 weeks”).
5. Forced-change and masked-address lines match the amended decisions.

## Issues

### R2-AU-CP-001 — Settings calls sign-in methods “Sign in”
- type: defect; level: page; impact: medium
- where: Settings · 17-settings, `Settings.html?auth=1`, 1440 light; evidence `docs/design/screens/17-settings/01-settings-email-account-desktop-1440.webp`
- what: A section listing Google/password methods is titled “تسجيل الدخول / Signing in”, read as an action rather than the methods themselves.
- proposal — AR: «طرق تسجيل الدخول» · EN: “Sign-in methods”
- why: Names the section’s contents without repeating the page-level action.
- cost: S; rule: docs/project/glossary.md (account)

### R2-AU-CP-002 — Google-only password link line (English word order)
- type: improvement; level: component; impact: low
- where: Settings · 17-settings, `Settings.html?auth=google`, 1440 light; evidence `docs/design/screens/17-settings/03-settings-google-only-account-desktop-1440.webp`
- what: “To also sign in with your email and a password, we send a link to your email” reads as translation interference; AR is «لتسجيل الدخول بالبريد وكلمة مرور أيضًا، نرسل رابطًا إلى بريدك».
- proposal — AR unchanged · EN: “To let you sign in with email and password too, we send a link to your email”
- why: Native English verb order.
- cost: S

### R2-AU-CP-003 — Link-sent helper uses awkward English
- type: improvement; level: component; impact: low
- where: Forgot password · 08; `Forgot password.html?state=sent` / `Settings.html?auth=google&state=linksent`, 390 light
- what: “We sent a link to set your password to your email” reads as a split infinitive/word-order artefact.
- proposal — AR unchanged · EN: “We sent a link to your email so you can set a password”
- why: Matches the Arabic delivery-order phrasing naturally.
- cost: S

### R2-AU-CP-004 — “Not set yet” caption vs method label capitalization
- type: improvement; level: page; impact: low
- where: Settings · 17-settings, `Settings.html?auth=google`, 1440/390
- what: The “Password” method row reads “لم تُعيَّن بعد / Not set yet” while the badge row beside it reads “مربوط / Linked”, a mixed tense voice.
- proposal — AR: «لم يُعيَّن بعد» · EN: “Not set yet” (keep); or change badge to “مرتبط” for uniformity
- why: Keeps one verbal style.
- cost: S

### R2-AU-CP-005 — Reports empty-state inconsistency
- type: improvement; level: page; impact: low
- where: My reports · 16; `Reports.html?auth=1&state=empty`, 1440/390
- what: Two strings — “لم ترسل أي بلاغ بعد / You haven’t sent any reports yet” and “لا توجد بلاغات هنا / No reports here” — for two cases, which reads as the same verdict twice.
- proposal — keep “لم ترسل أي بلاغ بعد” as the only first-empty line; “لا توجد بلاغات هنا” only when a filter is active, with its matching description
- why: Distinguishes the two situations in words, not just presence.
- cost: S

### R2-AU-CP-006 — Relative date forms mix singular/plural phrasing in English
- type: improvement; level: component; impact: low
- where: My reports · 16; `Reports.html?auth=1`, 1440/390
- what: English uses “2 weeks ago” and “a month ago” beside Arabic “قبل أسبوعين” and “قبل شهر” — meaning matches but the English grammar differs by bucket.
- proposal: standardise English pluralisation rule (Intl.RelativeTimeFormat style) and Arabic dual forms
- why: One counting voice for all buckets.
- cost: M

### R2-AU-CP-007 — Google failure `notallowed` quotes mismatched terms
- type: improvement; level: component; impact: low
- where: Sign in · 06; `Sign in.html?google=notallowed`, 390/1440
- what: AR pushes to «نسيت كلمة المرور» while EN says “Forgot password”, a slight term mismatch; glossary has “password” = “كلمة المرور”.
- proposal — keep both as “نسيت كلمة المرور / Forgot password?” with the same question mark
- why: Punctuation consistency across the mirror.
- cost: S

### R2-AU-CP-008 — Reset email button and body link differ in English
- type: improvement; level: page; impact: low
- where: Reset email · 09; `Reset email.html`, 720/390
- what: Arabic “تعيين كلمة مرور جديدة” matches the button, but English uses “Set a new password” in the button and “Set a new password.” in the body, with a trailing full stop only in body.
- proposal: drop the full stop from the inline link span; keep “Set a new password”
- why: Same promise, same punctuation.
- cost: S

## Decisions in doubt

- None.

## Not reviewed

- `Sign in - board.html` (board variant) — not opened; tr() absent on first scan, its copy duplicated from Sign in.
- Dark mode render strings — reviewed from source only (no dark-specific copy differences seen in extracted tr() calls).
- Focus/contrast and visual overflow — out of this axis (AX/DF/VD).
- Forced-change landings per role beyond the reception line already in the source — reception sample checked; owner/admin identical line used.<|end|><|start|>write to=assistant<|channel|>analysis<|message|>Done. Need final answer concise.<|end|><|start|> ^=assistant<|channel|>final<|message|>Report saved to `C:\Users\basel\.prompt\MASAHA_DESIGN\ROUND2\REPORT\R2-AU-CP_REPORT.md`. Done. (No server started; read-only review; report only.)[^1^]<|end|><|start|>tool_call_begin|xml<|message|><rfl:parameter name="<rfl:parameter name="bash">
python -c "print()" 2>/dev/null || true; if [ -f "c:\Users\basel\.prompt\MASAHA_DESIGN\ROUND2\REPORT\R2-AU-CP_REPORT.md" ]; then echo ok; fi