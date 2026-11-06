## What

The privacy policy (screen 33) in the web app, as `docs/design/prototype/Privacy.html` shows it, and its two links.

- **The page** `/privacy` — public (no guard), lazy-loaded in the site shell like the other site pages, titled «سياسة الخصوصية» / "Privacy Policy" in both languages. One reading column (`max-w-3xl`, the prototype's spacing): the title, «آخر تحديث: 2026-11-05» / "Last updated: 2026-11-05", then the eleven sections, each an `h2` naming its `section`, with paragraphs and bullet lists (`list-disc`, `ps-6`), bold through `<strong>`. The last section, in a card, gives the platform's email from its public contact (`usePlatformContact`, what About reads): nothing while it is read, the sentence alone when no email is set or the read fails.
- **The text** is the owner's approved text, unchanged, in Arabic and English, all in the copy catalogue (`site.privacy`); a list item is its words, or its parts in order where some are bold. Checked line by line against the approved text by a script: 43 lines in each language, none different.
- **The links:** «سياسة الخصوصية» / "Privacy Policy" in the site's footer, between «عن مساحة» and «تواصل معنا», as the prototype's footer; and on Register, under the form, one small muted line «اقرأ سياسة الخصوصية» / "Read the privacy policy", linking to `/privacy`.

## Documents

- `docs/project/overview.md` — *Built*: the privacy page, linked from the footer and Register (2026-11-05, #135), on the platform settings line whose email it gives.
- `docs/features/platform-settings.md` — the site reads its email on the privacy page; a history line.
- `docs/frontend/architecture.md` — the layout tree's and the groups' `public/` name the privacy page; *Built so far* names it, so "every screen of v1 is built" stays true with screen 33.

## The cron (its own commit)

The online cron now runs **every 60 minutes**, not 15 — the owner's decision of 2026-11-04, while the site is not launched: fewer database wake-ups; a late run never corrupts data, as the auto check-out records its due cut-off. Changed: `docs/development/setup.md` (*Timed jobs*, *The deployment*), ADR 0014 (a new *Revised* line, the decision unchanged), `docs/backend/conventions.md` §12, `docs/api/api-contract.md` (*Internal*), finding 213 (a dated note, to revisit at launch), `docs/features/spaces.md` (the photos' reclamation counts the 03:00 hour's runs: one a day now), and `apps/api/src/server.ts`'s comment only. The local timer stays 5.

## Tests (each red first)

- `PrivacyPage.component.test.tsx` — as a guest: the title, the date and every heading in English; every heading in Arabic and the bold parts in `<strong>`; the email link from `GET /settings/public`, the only link; no link when no contact is set. Red: the page did not exist (its module failed to resolve).
- `SiteLayout.component.test.tsx` — the footer's «Privacy Policy» → `/privacy`. Red: no such link.
- `authPages.component.test.tsx` — Register's «Read the privacy policy», its link → `/privacy`, `text-caption`. Red: no such link.
- The page's `<title>` in both languages is held by `app/pageTitles.unit.test.ts`, which walks every route.

## Local verification (on 791e53de)

- `npm run format:check` — pass
- `npm run lint` — pass
- `npm run typecheck` — pass
- `npm run check:classes` — pass
- `npm run check:links` — pass
- `npm run check:conflicts` — pass
- `npm run test:unit` — pass (280 + 917 + 1186 tests)
- `npm run test:component` — pass (2039 tests)
- `NODE_ENV=production npm run build` — pass (`PrivacyPage` its own 2.68 kB chunk)
- `npm run check:build` — pass (no showcase, no dashboard code and no heavy library in the site's first download)

`test:api` is left to CI: this PR changes no API code (one comment in `server.ts`), the owner's decision.

## Screenshots

Taken locally in headless Chrome (kept out of the repository): `/privacy` in Arabic light at 1280 and 390, English light at 1280, Arabic dark at 1280; Home's footer; Register in Arabic at 390 and English at 1280. Each checked: right to left in Arabic and left to right in English, the page's title in both, no raw tag, the 15 bold parts the text has, the email shown, nothing wider than 390. Only the web server ran: the API's in-process timer would run the timed jobs against `masaha_dev`, the owner's demo, so the public contact was answered in the browser with a sample email.

The shots caught one bug, fixed and folded into the first commit: in the Arabic line the date showed as 05-11-2026; it is now its own left-to-right span, and the Arabic test holds it.

## Decisions

- **The text follows the approved text for words, bold and punctuation; the layout follows the prototype.** So, beyond the prototype: «آخر تحديث:» / "Last updated:" is bold, and the contact sentence ends with its period after the email.
- **The contact gives the email only** (the text names the email), read with `usePlatformContact`, not `PlatformContact`, which would also draw WhatsApp and make the email the primary button; the button is the prototype's outline one. With no email set, or a failed read, the sentence stays without it, as About's text stays with no contact.
- **Register's line is "Read the privacy policy"** as the task gives it (the prototype says "Read privacy policy"); the link is "privacy policy", after «لديك حساب؟» as in the prototype.
- **The date is written in the catalogue** (`site.privacy.updated.date`, `2026-11-05`), so a new date is one line per language; the owner sets the real one in review if it differs.
- **Beyond the documents named:** `docs/frontend/architecture.md` (its public pages and *Built so far*) and `docs/features/spaces.md` (the reclamation's runs a day): each would otherwise state a fact this PR makes false.
- **The API was not started for the screenshots** (above).
